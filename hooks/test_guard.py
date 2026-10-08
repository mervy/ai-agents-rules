import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GUARD = Path(__file__).with_name("guard.py")


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


def bash(command: str, mode: str = "default", cwd: str = ".") -> dict | None:
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
