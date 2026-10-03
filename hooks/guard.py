#!/usr/bin/env python3
"""Hook PreToolUse do Claude Code: confirmações do AGENTS.md viram regra fixa.

Regra escrita é pedido; este hook é garantia. Comando arriscado no modo padrão vira
pergunta ao usuário ("ask"). Nos outros modos o "ask" não pergunta nada (o harness segue
o fluxo do modo), então negamos e orientamos o usuário a rodar o comando ele mesmo.
"""

import json
import re
import subprocess
import sys
from pathlib import PurePath

# Cada padrão roda sobre um trecho do comando (separado por ; && || | e quebra).
RISKY_PATTERNS: list[tuple[str, str]] = [
    (r"\bgit\s+push\b", "git push publica no remoto"),
    (r"\bgit\s+reset\s+.*--hard\b", "git reset --hard descarta trabalho"),
    (r"\bgit\s+branch\s+.*-D\b", "apagar branch"),
    (r"\bgit\s+clean\s+.*-\w*f", "git clean apaga arquivos não versionados"),
    (r"\bgit\s+commit\s+.*--amend\b", "amend pode reescrever commit publicado"),
    (r"\brm\s+(-\w*[rR]\w*|--recursive)\b", "apagar pasta recursivamente"),
    (
        r"\b(composer|npm|pnpm|yarn|cargo)\s+(update|upgrade)\b",
        "atualizar dependências",
    ),
    (r"\bartisan\s+migrate\b", "executar migration"),
    (r"\b(mysql|mariadb|psql)\b.*<\s*\S+\.sql\b", "executar SQL de arquivo no banco"),
    (r"\b(DROP|TRUNCATE)\s+(TABLE|DATABASE|SCHEMA)?\b", "DROP/TRUNCATE no banco"),
    (r"\bchmod\s+(-\w+\s+)*0?777\b", "permissão 777"),
    (r"\bchown\s+(-\w*R\w*)\b", "chown recursivo"),
    (r"\b(kill|pkill|killall)\b", "encerrar processo"),
    (r"\bgh\s+(release|gist|repo)\s+(create|delete|edit)\b", "publicar no GitHub"),
]

DELETE_WITHOUT_WHERE = re.compile(
    r"\bDELETE\s+FROM\b(?![\s\S]*\bWHERE\b)", re.IGNORECASE
)
SEGMENT_SPLIT = re.compile(r"&&|\|\||[;|\n]")
GIT_ADD_ENV = re.compile(
    r"\bgit\s+add\b.*(?:^|\s)(?:\S*/)?\.env(?:\.(?!example\b)\w+)*(?:\s|$)"
)


def is_env_file(path: str) -> bool:
    name = PurePath(path).name
    return name == ".env" or (name.startswith(".env.") and name != ".env.example")


def staged_env_files(cwd: str) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "-C", cwd, "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    return [f for f in result.stdout.splitlines() if is_env_file(f)]


def risky_reason(command: str) -> str | None:
    for segment in SEGMENT_SPLIT.split(command):
        for pattern, reason in RISKY_PATTERNS:
            # SQL vem em qualquer caixa; comandos de shell, só minúsculos.
            flags = re.IGNORECASE if "DROP" in pattern else 0
            if re.search(pattern, segment, flags):
                return reason
    if DELETE_WITHOUT_WHERE.search(command):
        return "DELETE sem WHERE"
    return None


def respond(decision: str, reason: str) -> None:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": decision,
                    "permissionDecisionReason": reason,
                }
            },
            ensure_ascii=False,
        )
    )


def confirm(mode: str, reason: str, command: str) -> None:
    if mode == "default":
        respond("ask", f"Regra global: {reason}. Confirme antes de executar.")
        return
    respond(
        "deny",
        f"Bloqueado pelo hook ({reason}) no modo '{mode}', que não pergunta. "
        f"Peça ao usuário para rodar ele mesmo: ! {command}",
    )


def check_bash(payload: dict) -> None:
    command = payload.get("tool_input", {}).get("command", "")
    mode = payload.get("permission_mode", "default")
    if GIT_ADD_ENV.search(command):
        respond("deny", ".env nunca entra no git; use .env.example com placeholders.")
        return
    if re.search(r"\bgit\s+commit\b", command):
        staged = staged_env_files(payload.get("cwd", "."))
        if staged:
            respond(
                "deny",
                f"Há .env no stage ({', '.join(staged)}); rode git restore --staged.",
            )
            return
    reason = risky_reason(command)
    if reason:
        confirm(mode, reason, command.strip())


def check_file_edit(payload: dict) -> None:
    path = payload.get("tool_input", {}).get("file_path", "")
    if is_env_file(path):
        confirm(
            payload.get("permission_mode", "default"),
            f"alterar {path}",
            f"edite {path} à mão",
        )


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as error:
        # Entrada inválida não deve travar o agente; registra e segue o fluxo normal.
        print(f"guard: entrada inválida ({error})", file=sys.stderr)
        return 0
    tool = payload.get("tool_name")
    if tool == "Bash":
        check_bash(payload)
    elif tool in ("Edit", "Write", "MultiEdit"):
        check_file_edit(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
