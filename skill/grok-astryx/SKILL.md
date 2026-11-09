---
name: grok-astryx
description: Teach a coding agent to build UI with Meta's Astryx design system using the official CLI and optional remote MCP. Use when the user wants Astryx components, themes, templates, or agent docs, or when generating React UI in an Astryx project.
license: MIT
---

# Build UI with Astryx (unofficial skill)

This skill is unofficial. It is not published, endorsed, or sponsored by Meta
Platforms, Inc. "Astryx" and "Meta" are marks of Meta Platforms, Inc. Use them
here only to name the design system this skill teaches.

Do not vendor Astryx component source. Do not invent props, tokens, or CLI
paths. Ask the official CLI (or the official MCP) and follow what it returns.

## When to use this skill

- The project already uses `@astryxdesign/core` or `@astryxdesign/cli`.
- The user wants a page, component, theme, or template from Astryx.
- You need to set up or refresh Astryx agent docs.

## How to invoke the CLI

Prefer, in this order:

1. A project script, if `package.json` has one named `astryx`:
   `npm run astryx -- <subcommand> …`
2. The scoped package, which works whether or not the CLI is already installed:
   `npx @astryxdesign/cli <subcommand> …`
3. After a global install (`npm i -g @astryxdesign/cli`), the short name
   `astryx` is fine *inside that environment*. In a project, the project's own
   installed version still wins.

Never run unscoped `npx astryx` before the CLI is installed. That name can
hit an unrelated npm package. Do not invent a binary path such as
`node_modules/@astryxdesign/cli/bin/docs.mjs`. If you add a project script,
the documented body is:

`node node_modules/@astryxdesign/cli/clients/cli/bin/astryx.mjs`

## Three-step workflow (before writing UI)

Use this order, from the official Astryx agent-docs workflow, with the
invocation style above:

1. Find a starting template:
   `npx @astryxdesign/cli build "a settings page with a profile form"`
2. Scaffold that template, then replace its placeholder content:
   `npx @astryxdesign/cli template <TemplateName>`
3. Read props and examples for each component you use:
   `npx @astryxdesign/cli component Button`

Useful lookups:

- `npx @astryxdesign/cli search button`
- `npx @astryxdesign/cli component Button`
- `npx @astryxdesign/cli template --list`
- `npx @astryxdesign/cli docs tokens`
- `npx @astryxdesign/cli hook --list`
- `npx @astryxdesign/cli manifest --json`
- `npx @astryxdesign/cli doctor`

Prefer short output when you will paste it into a prompt: `--dense`,
`--detail brief`, or `--detail compact`. Every useful command supports
`--json` for a typed envelope. Branch on the `code` field when you handle
errors, not on the human-readable `error` string.

## Project setup

```bash
npx @astryxdesign/cli init --features agents
```

That writes Astryx-managed agent docs (by default `AGENTS.md`, and Claude
files when needed). Official `--agent` values are `claude`, `cursor`,
`codex`, `hermes`, `muse`, and `all`. There is no official `--agent grok`.
This skill is the unofficial Grok Bot / Grok-path stand-in.

Computer-level skill (official): `npx @astryxdesign/cli init --user`.

After a dependency bump, refresh docs with the project's upgrade command
(`npx @astryxdesign/cli upgrade`, plus `--apply` when you want the refresh
written). Run `npx @astryxdesign/cli doctor` to see project health.

## Optional MCP

The official remote MCP is `https://astryx.atmeta.com/mcp`. Documented tools
are `search(query)` and `get(name)`. Prefer the local CLI when
`@astryxdesign/cli` is already in the project.

## Practical rules

- Start a page from a template when the CLI offers one. Keep its frame and
  spacing; replace the placeholder content.
- Use documented Astryx components and tokens. Do not invent prop names or
  magic style values when the CLI already lists the real ones.
- If you do not know a component's import path or props, ask the CLI.
  Guessing is how these UIs go wrong.
- This skill does not replace reading the CLI output. If the CLI errors,
  fix the invocation or the project setup; do not ignore it.

## Official docs

- CLI: https://astryx.atmeta.com/docs/cli
- Working with AI: https://astryx.atmeta.com/docs/working-with-ai
- Homepage: https://astryx.atmeta.com/
- Source (MIT): https://github.com/meta/astryx
