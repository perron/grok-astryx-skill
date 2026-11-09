# Contributing to grok-astryx-skill

Thanks for helping. This repo is an unofficial skill plus a tiny helper. It
must stay clearly unofficial, and it must not vendor Meta's component source.

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e ".[dev]"
python3 -m pytest -q
grok-astryx-skill --help
```

The skill text lives in two places on purpose and must stay identical:

- `skill/grok-astryx/SKILL.md` (the copy people read in the repo)
- `grok_astryx_skill/data/grok-astryx/SKILL.md` (the copy the package installs)

A test checks that they match. Edit both, or edit one and copy it to the other.

## Rules

- Verify CLI examples against https://astryx.atmeta.com/docs/cli before you
  add them. Never recommend unscoped `npx astryx`.
- Keep the unofficial / trademark notice at the top of the skill and README.
- Do not copy Astryx component source, tokens, or generated agent-doc blocks
  into this repo.
- Do not suggest that Meta endorses this skill. Official `init --agent`
  values do not include `grok`.

## What not to do

- Do not add network calls that scrape or republish the component catalog.
- Do not rename the repo to start with `astryx-` without a trademark review.
  See https://opensource.fb.com/legal/trademark/.
- Do not change repository visibility or publish to PyPI unless the
  maintainer asks for that exact action.

## Pull requests

Cite the official doc URL and the date you checked it.
