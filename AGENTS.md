# AGENTS.md

This repository is grok-astryx-skill, an unofficial MIT-licensed Grok Bot
skill and a tiny Python helper for Meta's Astryx CLI and remote MCP.

## Layout

- `skill/grok-astryx/SKILL.md` and `grok_astryx_skill/data/grok-astryx/SKILL.md`
  (keep these two files identical)
- `grok_astryx_skill/cli.py` — `workflow`, `command`, `check`, `install-skill`,
  `mcp`, `agents`
- `tests/test_grok_astryx_skill.py`

## How to work here

1. `pip install -e ".[dev]"` and `python3 -m pytest -q`.
2. Recommended invocations must stay scoped (`npx @astryxdesign/cli`) or use
   `npm run astryx --`. Never emit unscoped `npx astryx`.
3. Official `--agent` values are `claude`, `cursor`, `codex`, `hermes`,
   `muse`, and `all`. There is no official `--agent grok`. Do not invent one.
4. MCP is `https://astryx.atmeta.com/mcp` with tools `search` and `get`. The
   helper prints the URL; it does not open a client session.
5. This project is unofficial. Keep that wording in the skill and the README.
   The package is named `grok-astryx-skill` rather than `astryx-grok` because
   Meta's open-source trademark policy restricts using OS marks in a project
   name: https://opensource.fb.com/legal/trademark/.

## Do not

- Do not publish, force-push, or change repository visibility.
- Do not vendor `@astryxdesign/core` source or generated docs.
- Do not claim affiliation with Meta.

## Checks before you finish

```bash
python3 -m pytest -q
grok-astryx-skill --version
grok-astryx-skill command component Button
```
