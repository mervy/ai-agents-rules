import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GUARD = Path(__file__).with_name("guard.py")
# Pasta vazia fora de qualquer repositório: o resultado não depende de onde a suíte
# roda (o hook consulta a branch atual do cwd ao ver um git commit).
NEUTRAL = tempfile.TemporaryDirectory()


def run_guard(payload: dict) -> dict | None:
    result = subprocess.run(
        [sys.executable, str(GUARD)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout) if result.stdout.strip() else None


def bash(command: str, mode: str = "default", cwd: str = NEUTRAL.name) -> dict | None:
    return run_guard(
        {
            "hook_event_name": "PreToolUse",
            "permission_mode": mode,
            "cwd": cwd,
            "tool_name": "Bash",
            "tool_input": {"command": command},
        }
    )


def edit(path: str, mode: str = "default", tool: str = "Edit") -> dict | None:
    return run_guard(
        {
            "hook_event_name": "PreToolUse",
            "permission_mode": mode,
            "cwd": ".",
            "tool_name": tool,
            "tool_input": {"file_path": path},
        }
    )


def decision(output: dict | None) -> str | None:
    return output["hookSpecificOutput"]["permissionDecision"] if output else None


RISKY_COMMANDS = [
    "git push",
    "git push origin main",
    "git push --force origin main",
    "git status && git push -u origin dev",
    "git reset --hard HEAD~1",
    "git branch -D old",
    "git push origin --delete old",
    "git clean -fd",
    "git commit --amend --no-edit",
    "rm -rf build",
    "rm -r dist",
    "composer update",
    "npm update",
    "cargo update",
    "php artisan migrate",
    "mysql -u root app < schema.sql",
    "mysql -e 'DROP TABLE users'",
    "psql -c 'TRUNCATE posts'",
    "psql -c 'truncate table posts'",
    "psql -c 'drop database bitwise'",
    "mysql -e 'DROP INDEX idx_slug ON posts'",
    "psql -c 'ALTER TABLE posts DROP COLUMN body'",
    "mysql -e 'DELETE FROM users'",
    "chmod 777 public",
    "chown -R www-data .",
    "pkill node",
    "kill -9 1234",
    "gh release create v1.0.0",
    "gh gist create notes.md",
]

SAFE_COMMANDS = [
    "git status",
    "git log --oneline",
    "git commit -m 'feat: x'",
    "git add src/app.php",
    "git pull",
    "rm build/tmp.txt",
    "composer install",
    "npm ci",
    "mysql -e 'DELETE FROM users WHERE id = 1'",
    "ls -la",
    "echo pushing",
    "grep -r reset src",
    # "drop"/"truncate" fora de SQL: trait e métodos do Rust, texto, utilitário de shell
    "cat > c1.rs <<'EOF'\nimpl Drop for Comanda {\n    fn drop(&mut self) {}\n}\nEOF",
    "echo 'o hook bloqueia DROP no modo auto'",
    "grep -n 'v.truncate(3)' src/main.rs",
    "truncate -s 0 app.log",
]


class RiskyCommandsTest(unittest.TestCase):
    def test_default_mode_asks(self) -> None:
        for command in RISKY_COMMANDS:
            with self.subTest(command=command):
                self.assertEqual(decision(bash(command)), "ask")

    def test_auto_mode_denies_with_instructions(self) -> None:
        for mode in ("auto", "acceptEdits", "bypassPermissions", "dontAsk"):
            with self.subTest(mode=mode):
                out = bash("git push", mode=mode)
                self.assertEqual(decision(out), "deny")
                reason = out["hookSpecificOutput"]["permissionDecisionReason"]
                self.assertIn("! git push", reason)

    def test_safe_commands_pass_through(self) -> None:
        for command in SAFE_COMMANDS:
            with self.subTest(command=command):
                self.assertIsNone(bash(command))


class EnvFileTest(unittest.TestCase):
    def test_editing_env_asks(self) -> None:
        for path in (".env", "/app/.env", "config/.env.production"):
            for tool in ("Edit", "Write"):
                with self.subTest(path=path, tool=tool):
                    self.assertEqual(decision(edit(path, tool=tool)), "ask")

    def test_editing_env_example_is_free(self) -> None:
        self.assertIsNone(edit(".env.example"))
        self.assertIsNone(edit("src/env.php"))

    def test_git_add_env_is_always_denied(self) -> None:
        for mode in ("default", "auto"):
            with self.subTest(mode=mode):
                self.assertEqual(decision(bash("git add .env", mode=mode)), "deny")
        self.assertIsNone(bash("git add .env.example"))

    def test_commit_with_staged_env_is_denied(self) -> None:
        with tempfile.TemporaryDirectory() as repo:
            git = ["git", "-C", repo]
            subprocess.run([*git, "init", "-q"], check=True)
            Path(repo, ".env").write_text("DB_PASS=troque-aqui\n", encoding="utf-8")
            subprocess.run([*git, "add", "-f", ".env"], check=True)
            out = bash("git commit -m 'chore: x'", cwd=repo)
            self.assertEqual(decision(out), "deny")

    def test_commit_without_env_passes(self) -> None:
        with tempfile.TemporaryDirectory() as repo:
            git = ["git", "-C", repo]
            subprocess.run([*git, "init", "-q"], check=True)
            Path(repo, "a.txt").write_text("x\n", encoding="utf-8")
            subprocess.run([*git, "add", "a.txt"], check=True)
            self.assertIsNone(bash("git commit -m 'chore: x'", cwd=repo))


def make_repo(repo: str, branch: str = "main") -> list[str]:
    """Repositório com um commit inicial em `branch`; devolve o prefixo do git."""
    git = ["git", "-C", repo, "-c", "user.name=t", "-c", "user.email=t@t.dev"]
    subprocess.run([*git, "init", "-q", "-b", branch], check=True)
    Path(repo, "a.txt").write_text("x\n", encoding="utf-8")
    subprocess.run([*git, "add", "a.txt"], check=True)
    subprocess.run([*git, "commit", "-q", "-m", "chore: inicial"], check=True)
    return git


class MergeTreeTest(unittest.TestCase):
    """Árvore de merges: integração só com --no-ff e nada de commit direto em dev/main."""

    def test_merge_without_no_ff_is_denied(self) -> None:
        for command in (
            "git merge feature/x",
            "git switch dev && git merge fix/y",
            "git merge --squash feature/x",
            "git merge --ff feature/x",
        ):
            for mode in ("default", "auto"):
                with self.subTest(command=command, mode=mode):
                    out = bash(command, mode=mode)
                    self.assertEqual(decision(out), "deny")
                    self.assertIn("--no-ff", out["hookSpecificOutput"]["permissionDecisionReason"])

    def test_merge_after_cd_or_with_options_is_denied(self) -> None:
        for command in ("cd repo && git merge feat/x", "git -C repo merge feat/x"):
            with self.subTest(command=command):
                self.assertEqual(decision(bash(command)), "deny")

    def test_git_merge_in_prose_passes(self) -> None:
        # Texto que só cita o comando (docs, heredoc, mensagem) não é um merge.
        for command in (
            "cat >> README.md <<'EOF'\n- `git merge` sem `--no-ff` é bloqueado\nEOF",
            "echo 'use git merge com cuidado'",
        ):
            with self.subTest(command=command):
                self.assertIsNone(bash(command))

    def test_git_commit_in_prose_on_dev_passes(self) -> None:
        with tempfile.TemporaryDirectory() as repo:
            make_repo(repo, "dev")
            command = "cat >> notas.md <<'EOF'\nNunca faça git commit direto na dev.\nEOF"
            self.assertIsNone(bash(command, cwd=repo))

    def test_allowed_merges_pass(self) -> None:
        for command in (
            "git merge --no-ff feature/x",
            "git merge --no-ff feature/x -m 'Merge branch feature/x into dev'",
            "git merge --ff-only origin/dev",
            "git merge --abort",
            "git merge --continue",
        ):
            with self.subTest(command=command):
                self.assertIsNone(bash(command))

    def test_commit_on_dev_or_main_is_denied(self) -> None:
        for branch in ("dev", "main"):
            with self.subTest(branch=branch), tempfile.TemporaryDirectory() as repo:
                make_repo(repo, branch)
                out = bash("git commit -m 'fix: x'", mode="auto", cwd=repo)
                self.assertEqual(decision(out), "deny")
                self.assertIn("git switch -c", out["hookSpecificOutput"]["permissionDecisionReason"])

    def test_commit_on_feature_branch_passes(self) -> None:
        with tempfile.TemporaryDirectory() as repo:
            git = make_repo(repo, "dev")
            subprocess.run([*git, "switch", "-q", "-c", "feat/x"], check=True)
            self.assertIsNone(bash("git commit -m 'feat: x'", cwd=repo))

    def test_commit_follows_cd_and_dash_c(self) -> None:
        # O cwd da sessão é um repo na dev, mas o comando entra em outro repo.
        with tempfile.TemporaryDirectory() as dev_repo, tempfile.TemporaryDirectory() as feat:
            make_repo(dev_repo, "dev")
            git = make_repo(feat, "dev")
            subprocess.run([*git, "switch", "-q", "-c", "feat/x"], check=True)
            for command in (f"cd {feat} && git commit -m 'feat: x'", f"git -C {feat} commit -m x"):
                with self.subTest(command=command):
                    self.assertIsNone(bash(command, cwd=dev_repo))
            out = bash(f"cd {dev_repo} && git add a.txt && git commit -m x", cwd=feat)
            self.assertEqual(decision(out), "deny")

    def test_initial_commit_on_main_passes(self) -> None:
        with tempfile.TemporaryDirectory() as repo:
            subprocess.run(["git", "-C", repo, "init", "-q", "-b", "main"], check=True)
            self.assertIsNone(bash("git commit -m 'chore: inicial'", cwd=repo))

    def test_finishing_merge_conflict_on_dev_passes(self) -> None:
        with tempfile.TemporaryDirectory() as repo:
            git = make_repo(repo, "dev")
            head = subprocess.run(
                [*git, "rev-parse", "HEAD"], capture_output=True, text=True, check=True
            ).stdout.strip()
            # MERGE_HEAD presente = merge em andamento, esperando o commit da resolução.
            Path(repo, ".git", "MERGE_HEAD").write_text(head + "\n", encoding="utf-8")
            self.assertIsNone(bash("git commit --no-edit", cwd=repo))


class RobustnessTest(unittest.TestCase):
    def test_other_tools_are_ignored(self) -> None:
        self.assertIsNone(
            run_guard({"tool_name": "Read", "tool_input": {"file_path": ".env"}})
        )

    def test_invalid_json_does_not_block(self) -> None:
        result = subprocess.run(
            [sys.executable, str(GUARD)],
            input="não é json",
            capture_output=True,
            text=True,
            timeout=10,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "")
        self.assertIn("guard", result.stderr)


if __name__ == "__main__":
    unittest.main()
