# Security Policy

This project is a small local command-line tool. It does not phone home and does not require an API key.

## Reporting a vulnerability

Please open a [GitHub issue](https://github.com/perron/grok-astryx-skill/issues) and mention that it is a security report. Do not include secrets, tokens, or private file contents in the issue.

If the report includes a working exploit against this tool, describe the impact and a minimal reproduction without pasting live credentials.

## Notes for this tool

The helper is a local CLI. `workflow`, `command`, `check`, `mcp`, and `agents` only print text. `install-skill` writes a copy of the bundled skill into a folder you choose (`--root/.grok/skills` by default). It does not call Meta's MCP or CLI for you. This project is unofficial and is not affiliated with Meta Platforms, Inc.

## Supported versions

The `master` branch and the latest tagged release, when one exists, are supported.
