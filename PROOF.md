# grok-astryx-skill proof

Captured 2026-11-09, afternoon America/Los_Angeles (PST).

Fresh-venv install: `pip install .` succeeded and `grok-astryx-skill --version` printed `grok-astryx-skill 0.1.0`.

Tests: 18 passed in 0.05s
Local pytest (same tree): 18 passed.

## version
```
grok-astryx-skill 0.1.0
```

## workflow (empty cwd)
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

## command
```
npx @astryxdesign/cli component Button
```

## check notes.md
```
warning: unscoped-npx-astryx: Unscoped `npx astryx` can resolve to an unrelated npm package. Use `npx @astryxdesign/cli` or `npm run astryx --`. (/tmp/ai-tools-proof/grok-astryx-skill/notes.md:1)
  excerpt: Run npx astryx component Button
1 warning(s)
```

## install-skill
```
installed grok-astryx -> /tmp/ai-tools-proof/grok-astryx-skill/.grok/skills/grok-astryx
name: grok-astryx
```
