# grok-astryx-skill

An unofficial Grok Bot skill, plus a tiny helper, that teaches an agent to
build UI with Meta's [Astryx](https://astryx.atmeta.com/) design system
using the official CLI and the optional remote MCP.

This project is **not affiliated with, endorsed by, or sponsored by Meta
Platforms, Inc.** "Astryx" and "Meta" are marks of Meta. The repo is named
`grok-astryx-skill` rather than `astryx-grok` because Meta's
[open source trademark policy](https://opensource.fb.com/legal/trademark/)
says OS trademarks may not be used in the name of a project built on top of
Meta's open source software. The word Astryx still appears so people can
find a skill that teaches that CLI. If Meta asks for a rename that drops
the mark entirely, we will.

Astryx itself is MIT-licensed. This repo does not vendor component source.

## Install

Python 3.10 or later.

```bash
python3 -m pip install .
python3 -m pip install -e ".[dev]"  # optional, for tests
grok-astryx-skill --help
```

Or without installing:

```bash
PYTHONPATH=. python3 -m grok_astryx_skill --help
```

The skill itself is the folder `skill/grok-astryx/` (a `SKILL.md` with
`name` and `description` frontmatter). You can point a Grok skill path at
it, or let the helper copy it:

```bash
grok-astryx-skill install-skill --root .
# writes ./.grok/skills/grok-astryx/SKILL.md
```

`--target DIR` writes into that directory. `--global` writes to
`~/.grok/skills`. Those folders are the documented Grok Build skill paths.
Grok Bot (the chat product) also lets you save a private skill in the
product; there is no single official repo-root drop path we could verify
for that product.

## 30-second quick start

```bash
grok-astryx-skill workflow
grok-astryx-skill command component Button
echo 'Run npx astryx component Button' > notes.md
grok-astryx-skill check notes.md
```

Real output (9 Nov 2026, America/Los_Angeles), from an empty folder with no
`package.json`:

```
Unofficial helper. Not affiliated with Meta Platforms, Inc.
Recommended runner: npx @astryxdesign/cli
Why: no package.json; use the scoped package so npx does not hit an unrelated 'astryx' package

Three-step workflow (from official Astryx agent docs):
  1. npx @astryxdesign/cli build "a settings page with a profile form"
     Get the closest page template, alternatives, and supporting blocks.
  2. npx @astryxdesign/cli template <TemplateName>
     Scaffold that template; keep its frame and spacing; replace placeholder content.
  3. npx @astryxdesign/cli component Button
     Read props and examples for each component you will use.

Short output flags: --json  --dense  --detail brief|compact
CLI docs: https://astryx.atmeta.com/docs/cli
```

```
npx @astryxdesign/cli component Button
```

```
warning: unscoped-npx-astryx: Unscoped `npx astryx` can resolve to an unrelated npm package. Use `npx @astryxdesign/cli` or `npm run astryx --`. (notes.md:1)
  excerpt: Run npx astryx component Button
1 warning(s)
```

If the project has an `astryx` script in `package.json`, `command` prints
`npm run astryx -- …` instead. Never use unscoped `npx astryx`.

`grok-astryx-skill mcp` prints the official remote MCP URL,
`https://astryx.atmeta.com/mcp`, and a Cursor config snippet. The helper
does not open a connection. `grok-astryx-skill agents` lists official
`init --agent` values (`claude`, `cursor`, `codex`, `hermes`, `muse`,
`all`) and states that Grok is not one of them.

## Use it with your agent

You can point a coding agent at this repository and ask it to follow the
bundled skill, install it, or write a similar small helper in the same style.

Sample prompt:

```
Use the unofficial grok-astryx skill in this repo. Install the helper with
`python3 -m pip install .`, run `python3 -m pytest -q`, then run
`grok-astryx-skill workflow` and `grok-astryx-skill install-skill --root .`.
When you generate Astryx UI, follow the skill: use `npx @astryxdesign/cli`
or `npm run astryx --`, never unscoped `npx astryx`, and do not invent
component props. This project is unofficial and is not affiliated with
Meta. Do not publish the package or vendor Astryx source. If you want to
build a similar tool, match this repo's layout: a small MIT Python CLI, a
SKILL.md with name and description frontmatter, behavior tests, honest
limits in the README, and no secrets.
```

## How you can help

- Correct a CLI example if official docs have changed, with a link and a
  date. Keep the unofficial notice.
- Send a command string that `check` missed or falsely flagged.
- Improve the skill's wording so an agent is less likely to invent props
  or binary paths.

See `CONTRIBUTING.md`. Please do not paste private project tokens into
issues.

## Credit

CLI commands, flags, the three-step workflow, official `--agent` values,
and the MCP URL were checked against Meta's public Astryx docs on 9 Nov
2026:

- https://astryx.atmeta.com/docs/cli
- https://astryx.atmeta.com/docs/working-with-ai
- https://astryx.atmeta.com/mcp
- https://github.com/meta/astryx (MIT)

The skill text and helper are original. No Astryx source was copied.

## Limits

- This is unofficial. Official Astryx agent setup does not list Grok Bot as a first-class `--agent` target.
- The helper prints recommended commands and copies a skill folder. It does not run the Astryx CLI for you, and it does not call the MCP server.
- Install paths `.grok/skills` and `~/.grok/skills` follow Grok Build's published skill folders. Grok Bot's documented private-skill flow is in-product; use `--target` for a custom folder such as a bot box's `agent-data/workflows` if that is where your skills live.
- CLI flags and package versions change. Re-check the official docs if a command fails.
- Meta's trademark policy is stricter than a typical MIT license. Using "Astryx" in this repo name may still be conservative-insufficient if Meta objects.

From GitHub you can also install with:

```bash
python3 -m pip install git+https://github.com/perron/grok-astryx-skill.git
```

This package is not published to PyPI.

## License

MIT. See `LICENSE`. Please read `SECURITY.md` before filing a vulnerability report.
