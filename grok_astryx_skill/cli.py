"""Tiny helper plus bundled unofficial skill for building UI with Astryx."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

__version__ = "0.1.0"

SCOPED = "npx @astryxdesign/cli"
OFFICIAL_MCP = "https://astryx.atmeta.com/mcp"
CLI_DOCS = "https://astryx.atmeta.com/docs/cli"
AI_DOCS = "https://astryx.atmeta.com/docs/working-with-ai"
TRADEMARK_POLICY = "https://opensource.fb.com/legal/trademark/"
OFFICIAL_AGENTS = ("claude", "cursor", "codex", "hermes", "muse", "all")
SKILL_NAME = "grok-astryx"

UNSCOPED_NPX_RE = re.compile(r"\bnpx(?:\s+--yes|\s+-y)*\s+astryx\b", re.I)
INVENTED_BIN_RE = re.compile(
    r"@astryxdesign/cli/(?:bin|dist|cli)/|@astryxdesign/cli/bin/docs\.mjs",
    re.I,
)
# The documented script body is allowed; do not flag it.
DOCUMENTED_BIN = "node_modules/@astryxdesign/cli/clients/cli/bin/astryx.mjs"


def bundled_skill() -> Path:
    here = Path(__file__).resolve().parent
    packaged = here / "data" / "grok-astryx"
    if (packaged / "SKILL.md").is_file():
        return packaged
    repo = here.parent / "skill" / "grok-astryx"
    if (repo / "SKILL.md").is_file():
        return repo
    raise FileNotFoundError("bundled grok-astryx skill not found")


def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    data: dict = {}
    for raw in parts[1].splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("\"'")
    return data


def detect_runner(cwd: Path) -> dict:
    package = cwd / "package.json"
    result = {
        "runner": SCOPED,
        "reason": "no package.json; use the scoped package so npx does not hit an unrelated 'astryx' package",
        "has_script": False,
        "has_cli_dep": False,
        "package_manager": "npm",
    }
    if not package.is_file():
        return result
    try:
        data = json.loads(package.read_text(encoding="utf-8", errors="replace"))
    except json.JSONDecodeError:
        result["reason"] = "package.json is invalid; falling back to the scoped package"
        return result
    scripts = data.get("scripts") or {}
    deps = {}
    for key in ("dependencies", "devDependencies", "optionalDependencies"):
        block = data.get(key) or {}
        if isinstance(block, dict):
            deps.update(block)
    has_script = isinstance(scripts, dict) and "astryx" in scripts
    has_cli = "@astryxdesign/cli" in deps
    result["has_script"] = has_script
    result["has_cli_dep"] = has_cli
    lock_pm = "npm"
    if (cwd / "pnpm-lock.yaml").is_file():
        lock_pm = "pnpm"
    elif (cwd / "yarn.lock").is_file():
        lock_pm = "yarn"
    elif (cwd / "bun.lockb").is_file() or (cwd / "bun.lock").is_file():
        lock_pm = "bun"
    result["package_manager"] = lock_pm
    if has_script:
        result["runner"] = "npm run astryx --"
        result["reason"] = "package.json has an astryx script; use it so agents do not invent a binary path"
    elif has_cli:
        if lock_pm == "pnpm":
            result["runner"] = "pnpm exec astryx"
            result["reason"] = "project depends on @astryxdesign/cli and has a pnpm lockfile"
        elif lock_pm == "yarn":
            result["runner"] = "yarn exec astryx"
            result["reason"] = "project depends on @astryxdesign/cli and has a yarn lockfile"
        else:
            result["runner"] = SCOPED
            result["reason"] = "project depends on @astryxdesign/cli; the scoped npx command uses the installed version"
    else:
        result["runner"] = SCOPED
        result["reason"] = "no astryx script or @astryxdesign/cli dependency; the scoped npx command will fetch or run the CLI"
    return result


def build_command(runner: str, args: list[str]) -> str:
    if not args:
        return runner if not runner.endswith(" --") else runner[:-3].rstrip()
    joined = " ".join(args)
    if runner.endswith(" --"):
        return f"{runner} {joined}"
    return f"{runner} {joined}"


def workflow_steps(runner: str) -> list[dict]:
    def cmd(args: list[str]) -> str:
        return build_command(runner, args)

    return [
        {
            "step": 1,
            "name": "build",
            "purpose": "Get the closest page template, alternatives, and supporting blocks.",
            "command": cmd(["build", '"a settings page with a profile form"']),
        },
        {
            "step": 2,
            "name": "template",
            "purpose": "Scaffold that template; keep its frame and spacing; replace placeholder content.",
            "command": cmd(["template", "<TemplateName>"]),
        },
        {
            "step": 3,
            "name": "component",
            "purpose": "Read props and examples for each component you will use.",
            "command": cmd(["component", "Button"]),
        },
    ]


def check_text(text: str, path: str) -> list[dict]:
    findings: list[dict] = []
    for i, line in enumerate(text.splitlines() or [""], 1):
        if UNSCOPED_NPX_RE.search(line):
            findings.append(
                {
                    "severity": "warning",
                    "code": "unscoped-npx-astryx",
                    "path": path,
                    "line": i,
                    "excerpt": line.strip()[:240],
                    "message": (
                        "Unscoped `npx astryx` can resolve to an unrelated npm "
                        "package. Use `npx @astryxdesign/cli` or `npm run astryx --`."
                    ),
                }
            )
        if INVENTED_BIN_RE.search(line) and DOCUMENTED_BIN not in line:
            findings.append(
                {
                    "severity": "warning",
                    "code": "invented-bin-path",
                    "path": path,
                    "line": i,
                    "excerpt": line.strip()[:240],
                    "message": (
                        "This looks like an invented CLI path. Prefer a project "
                        f"`astryx` script whose body is `{DOCUMENTED_BIN}`, or run {SCOPED}."
                    ),
                }
            )
    return findings


def emit(data: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(data, indent=2))
        return
    # Human output is built by each command.


def cmd_workflow(args: argparse.Namespace) -> int:
    info = detect_runner(Path(args.cwd).resolve())
    steps = workflow_steps(info["runner"])
    payload = {
        "unofficial": True,
        "runner": info["runner"],
        "reason": info["reason"],
        "steps": steps,
        "flags": ["--json", "--dense", "--detail brief", "--detail compact"],
        "docs": {"cli": CLI_DOCS, "ai": AI_DOCS},
    }
    if args.json:
        print(json.dumps(payload, indent=2))
        return 0
    print("Unofficial helper. Not affiliated with Meta Platforms, Inc.")
    print(f"Recommended runner: {info['runner']}")
    print(f"Why: {info['reason']}")
    print()
    print("Three-step workflow (from official Astryx agent docs):")
    for step in steps:
        print(f"  {step['step']}. {step['command']}")
        print(f"     {step['purpose']}")
    print()
    print("Short output flags: --json  --dense  --detail brief|compact")
    print(f"CLI docs: {CLI_DOCS}")
    return 0


def cmd_command(args: argparse.Namespace) -> int:
    info = detect_runner(Path(args.cwd).resolve())
    command = build_command(info["runner"], list(args.cli_args))
    payload = {
        "unofficial": True,
        "command": command,
        "runner": info["runner"],
        "reason": info["reason"],
        "warning": "never use unscoped npx astryx",
    }
    if args.json:
        print(json.dumps(payload, indent=2))
        return 0
    print(command)
    if args.verbose:
        print(f"# {info['reason']}", file=sys.stderr)
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    findings: list[dict] = []
    if args.command:
        findings.extend(check_text(args.command, "<command>"))
    else:
        target = Path(args.path) if args.path else Path("-")
        if args.path == "-" or not args.path:
            # If no path and no --command, that is an error unless stdin is piped.
            if args.path == "-":
                findings.extend(check_text(sys.stdin.read(), "<stdin>"))
            else:
                print("error: pass a file path, '-' for stdin, or --command TEXT", file=sys.stderr)
                return 1
        else:
            path = Path(args.path)
            if not path.exists():
                print(f"error: path not found: {path}", file=sys.stderr)
                return 1
            if path.is_dir():
                for file in sorted(path.rglob("*")):
                    if not file.is_file():
                        continue
                    if any(part in {".git", "node_modules", ".venv", "venv", "__pycache__"} for part in file.parts):
                        continue
                    if file.suffix.lower() not in {".md", ".mdc", ".txt", ".json", ".sh", ".bash", ".yml", ".yaml", ".js", ".ts", ""} and file.name not in {"SKILL.md", "AGENTS.md", "CLAUDE.md", "Makefile", "package.json"}:
                        if file.suffix and file.suffix.lower() not in {".md", ".mdc", ".txt", ".sh"}:
                            continue
                    findings.extend(check_text(file.read_text(encoding="utf-8", errors="replace"), str(file)))
            else:
                findings.extend(check_text(path.read_text(encoding="utf-8", errors="replace"), str(path)))
    warnings = len(findings)
    if args.json:
        print(json.dumps({"findings": findings, "warnings": warnings}, indent=2))
    else:
        if not findings:
            print("ok: no unscoped npx astryx or invented CLI paths found")
        else:
            for item in findings:
                loc = f"{item['path']}:{item['line']}"
                print(f"{item['severity']}: {item['code']}: {item['message']} ({loc})")
                if item.get("excerpt"):
                    print(f"  excerpt: {item['excerpt']}")
            print(f"{warnings} warning(s)")
    return 1 if findings else 0


def cmd_install_skill(args: argparse.Namespace) -> int:
    src = bundled_skill()
    if args.target:
        dest_parent = Path(args.target)
    elif args.global_install:
        dest_parent = Path.home() / ".grok" / "skills"
    else:
        dest_parent = Path(args.root).resolve() / ".grok" / "skills"
    dest = dest_parent / SKILL_NAME
    dest_parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() or dest.is_symlink():
        if dest.is_dir() and not dest.is_symlink():
            shutil.rmtree(dest)
        else:
            dest.unlink()
    shutil.copytree(src, dest)
    skill_md = dest / "SKILL.md"
    payload = {"installed": str(dest), "skill": SKILL_NAME, "unofficial": True}
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"installed {SKILL_NAME} -> {dest}")
        if skill_md.is_file():
            meta = parse_frontmatter(skill_md.read_text(encoding="utf-8", errors="replace"))
            print(f"name: {meta.get('name', '')}")
    return 0


def cmd_mcp(args: argparse.Namespace) -> int:
    payload = {
        "url": OFFICIAL_MCP,
        "tools": ["search(query)", "get(name)"],
        "note": "Official remote MCP. This helper does not start a server or proxy requests.",
        "cursor": {"mcpServers": {"astryx": {"url": OFFICIAL_MCP}}},
        "docs": AI_DOCS,
    }
    if args.json:
        print(json.dumps(payload, indent=2))
        return 0
    print(f"Official MCP URL: {OFFICIAL_MCP}")
    print("Documented tools: search(query), get(name)")
    print("This helper does not connect to the server; it only prints the published URL.")
    print("Cursor example (.cursor/mcp.json):")
    print(json.dumps(payload["cursor"], indent=2))
    return 0


def cmd_agents(args: argparse.Namespace) -> int:
    payload = {
        "official_init_agents": list(OFFICIAL_AGENTS),
        "official_command": f"{SCOPED} init --features agents --agent claude",
        "grok_first_class": False,
        "unofficial_skill": SKILL_NAME,
        "docs": AI_DOCS,
        "trademark_policy": TRADEMARK_POLICY,
    }
    if args.json:
        print(json.dumps(payload, indent=2))
        return 0
    print("Official `init --agent` values: " + ", ".join(OFFICIAL_AGENTS))
    print("There is no official --agent grok. This repo ships an unofficial skill named grok-astryx.")
    print(f"Example: {payload['official_command']}")
    print(f"AI setup docs: {AI_DOCS}")
    return 0


def cmd_skill_path(args: argparse.Namespace) -> int:
    path = bundled_skill()
    if args.json:
        print(json.dumps({"path": str(path), "skill": SKILL_NAME}, indent=2))
    else:
        print(path)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="grok-astryx-skill",
        description=(
            "Unofficial helper that teaches an agent to build UI with Meta's "
            "Astryx CLI and optional MCP. Not affiliated with Meta."
        ),
    )
    parser.add_argument("--version", action="version", version=f"grok-astryx-skill {__version__}")
    parser.add_argument("--json", action="store_true", help="JSON output (also accepted on subcommands)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_workflow = sub.add_parser("workflow", help="print the official three-step CLI workflow with a safe runner")
    p_workflow.add_argument("--cwd", default=".", help="project directory used to pick a runner")
    p_workflow.add_argument("--json", action="store_true")
    p_workflow.set_defaults(func=cmd_workflow)

    p_command = sub.add_parser("command", help="print a recommended CLI invocation")
    p_command.add_argument("cli_args", nargs="*", help="arguments after the runner, e.g. component Button")
    p_command.add_argument("--cwd", default=".")
    p_command.add_argument("--json", action="store_true")
    p_command.add_argument("--verbose", action="store_true")
    p_command.set_defaults(func=cmd_command)

    p_check = sub.add_parser("check", help="flag unscoped npx astryx and invented CLI paths")
    p_check.add_argument("path", nargs="?", help="file, directory, or '-' for stdin")
    p_check.add_argument("--command", dest="command", help="check a single command string")
    p_check.add_argument("--json", action="store_true")
    p_check.set_defaults(func=cmd_check)

    p_install = sub.add_parser("install-skill", help="copy the bundled unofficial skill into a Grok skills folder")
    p_install.add_argument("--root", default=".", help="project root (installs to ROOT/.grok/skills/grok-astryx)")
    p_install.add_argument("--target", help="directory that should contain the grok-astryx folder")
    p_install.add_argument("--global", dest="global_install", action="store_true", help="install to ~/.grok/skills")
    p_install.add_argument("--json", action="store_true")
    p_install.set_defaults(func=cmd_install_skill)

    p_mcp = sub.add_parser("mcp", help="print the official remote MCP URL and a Cursor snippet")
    p_mcp.add_argument("--json", action="store_true")
    p_mcp.set_defaults(func=cmd_mcp)

    p_agents = sub.add_parser("agents", help="list official init --agent values and the unofficial Grok gap")
    p_agents.add_argument("--json", action="store_true")
    p_agents.set_defaults(func=cmd_agents)

    p_path = sub.add_parser("skill-path", help="print the path of the bundled skill folder")
    p_path.add_argument("--json", action="store_true")
    p_path.set_defaults(func=cmd_skill_path)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if getattr(args, "json", False) is False and hasattr(args, "json"):
        # top-level --json is parsed on the root parser only when it appears
        # before the subcommand; that's argparse's default. Fine.
        pass
    try:
        return int(args.func(args))
    except (FileNotFoundError, ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
