# Getting started

## Install

Install the skills you want, one plugin each, or the `pm-agent-toolkit` bundle for all of them. The [README](../README.md#install) has the steps for Claude Code, claude.ai chat, Cowork, and single-skill zip upload; [platform-support.md](platform-support.md) shows what each surface loads.

In Claude Code, a plugin skill runs as `/<plugin>:<skill>` (for example `/html-render:html-render`) and also loads on its own when a request matches its description. A manually copied skill runs as `/<skill>`.

## First run

1. Set up your workspace folders: [workspace-setup.md](workspace-setup.md)
2. Fill in any `templates/` companion files for the skills you'll use (personas, source paths, brand tokens); each skill's read-first table says what it expects
3. Invoke a skill with a natural request; check the output against the skill's shipped template

## Hooks and rules

Optional but recommended; this is where the compounding starts. See [the-system-layer.md](the-system-layer.md).
