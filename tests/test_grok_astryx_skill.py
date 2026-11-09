from __future__ import annotations

import json
from pathlib import Path

import pytest

import grok_astryx_skill.cli as gax


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_help_and_version():
    with pytest.raises(SystemExit) as exc:
        gax.main(["--help"])
    assert exc.value.code == 0
    with pytest.raises(SystemExit) as exc:
        gax.main(["--version"])
    assert exc.value.code == 0


def test_workflow_mentions_three_steps(tmp_path, capsys):
    assert gax.main(["workflow", "--cwd", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "build" in out
    assert "template" in out
    assert "component" in out
    assert "npx @astryxdesign/cli" in out
    assert "npx astryx " not in out


def test_command_uses_scoped_npx_by_default(tmp_path, capsys):
    assert gax.main(["command", "component", "Button", "--cwd", str(tmp_path)]) == 0
    out = capsys.readouterr().out.strip()
    assert out == "npx @astryxdesign/cli component Button"
    assert "npx astryx" not in out


def test_command_prefers_npm_script(tmp_path, capsys):
    write(
        tmp_path / "package.json",
        json.dumps({"name": "demo", "scripts": {"astryx": "node node_modules/@astryxdesign/cli/clients/cli/bin/astryx.mjs"}}),
    )
    assert gax.main(["command", "search", "button", "--cwd", str(tmp_path)]) == 0
    assert capsys.readouterr().out.strip() == "npm run astryx -- search button"


def test_command_uses_pnpm_exec_when_dep_and_lockfile(tmp_path, capsys):
    write(
        tmp_path / "package.json",
        json.dumps({"name": "demo", "devDependencies": {"@astryxdesign/cli": "0.7.11"}}),
    )
    write(tmp_path / "pnpm-lock.yaml", "lockfileVersion: '9.0'\n")
    assert gax.main(["command", "doctor", "--cwd", str(tmp_path)]) == 0
    assert capsys.readouterr().out.strip() == "pnpm exec astryx doctor"


def test_check_flags_unscoped(tmp_path, capsys):
    path = write(tmp_path / "notes.md", "Run npx astryx component Button\n")
    assert gax.main(["check", str(path)]) == 1
    assert "unscoped-npx-astryx" in capsys.readouterr().out


def test_check_flags_invented_bin(tmp_path, capsys):
    path = write(tmp_path / "notes.md", "node node_modules/@astryxdesign/cli/bin/docs.mjs\n")
    assert gax.main(["check", str(path)]) == 1
    assert "invented-bin-path" in capsys.readouterr().out


def test_check_allows_documented_script_body(tmp_path, capsys):
    path = write(
        tmp_path / "package.json",
        json.dumps({"scripts": {"astryx": "node node_modules/@astryxdesign/cli/clients/cli/bin/astryx.mjs"}}),
    )
    assert gax.main(["check", str(path)]) == 0
    assert "ok:" in capsys.readouterr().out


def test_check_command_flag(capsys):
    assert gax.main(["check", "--command", "npx --yes astryx search button"]) == 1
    assert "unscoped-npx-astryx" in capsys.readouterr().out


def test_check_clean_scoped(capsys):
    assert gax.main(["check", "--command", "npx @astryxdesign/cli component Button"]) == 0


def test_install_skill(tmp_path, capsys):
    project = tmp_path / "proj"
    project.mkdir()
    assert gax.main(["install-skill", "--root", str(project)]) == 0
    dest = project / ".grok" / "skills" / "grok-astryx" / "SKILL.md"
    assert dest.is_file()
    text = dest.read_text(encoding="utf-8")
    meta = gax.parse_frontmatter(text)
    assert meta["name"] == "grok-astryx"
    assert "description" in meta
    assert "unofficial" in text.lower()
    assert capsys.readouterr().out.startswith("installed grok-astryx")


def test_bundled_skill_frontmatter_and_folder():
    skill = gax.bundled_skill()
    assert skill.name == "grok-astryx"
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    meta = gax.parse_frontmatter(text)
    assert meta["name"] == "grok-astryx"
    assert "when" in meta["description"].lower()
    assert "astryx" in meta["description"].lower()
    repo = Path(__file__).resolve().parents[1] / "skill" / "grok-astryx" / "SKILL.md"
    packaged = Path(__file__).resolve().parents[1] / "grok_astryx_skill" / "data" / "grok-astryx" / "SKILL.md"
    assert repo.read_text(encoding="utf-8") == packaged.read_text(encoding="utf-8")


def test_mcp_prints_official_url(capsys):
    assert gax.main(["mcp"]) == 0
    out = capsys.readouterr().out
    assert "https://astryx.atmeta.com/mcp" in out
    assert "search(query)" in out


def test_agents_lists_official_and_notes_gap(capsys):
    assert gax.main(["agents", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert "claude" in data["official_init_agents"]
    assert "cursor" in data["official_init_agents"]
    assert "codex" in data["official_init_agents"]
    assert data["grok_first_class"] is False
    assert data["unofficial_skill"] == "grok-astryx"


def test_workflow_json(tmp_path, capsys):
    assert gax.main(["workflow", "--cwd", str(tmp_path), "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["unofficial"] is True
    assert [s["name"] for s in data["steps"]] == ["build", "template", "component"]
    for step in data["steps"]:
        assert "npx astryx " not in step["command"]


def test_missing_check_path(tmp_path, capsys):
    assert gax.main(["check", str(tmp_path / "missing.md")]) == 1
    assert "path not found" in capsys.readouterr().err


def test_unicode_skill_copy(tmp_path):
    # install should preserve unicode already in the bundled skill if present;
    # also confirm a Japanese notes file can be checked without crashing.
    path = write(tmp_path / "メモ.md", "npx @astryxdesign/cli docs tokens\n漢字 ✅\n")
    assert gax.main(["check", str(path)]) == 0


def test_command_never_returns_unscoped():
    info = gax.detect_runner(Path("/tmp"))
    cmd = gax.build_command(info["runner"], ["init", "--features", "agents"])
    assert "npx astryx" not in cmd
    assert "@astryxdesign/cli" in cmd or cmd.startswith("npm run") or "exec astryx" in cmd
