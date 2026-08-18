# Getting started

## Install

**Claude Code plugin (recommended):**

```
/plugin marketplace add ryanhoggpm/pm-agent-toolkit
/plugin install pm-agent-toolkit@pm-agent-toolkit
```

Skills are then invocable as `/pm-agent-toolkit:<skill-name>` and auto-load when your request matches a skill's description.

**Manual copy (any project):** copy a `skills/<name>/` folder (the whole folder, including its `templates/` and `references/`) into your project's `.claude/skills/`. The skill is then `/<skill-name>` in that project.

**claude.ai:** ZIP one skill folder, then Settings → Capabilities → Skills → Upload. Skills that read workspace files will ask you questions instead when files aren't available.

## First run

1. Set up your workspace folders: [workspace-setup.md](workspace-setup.md)
2. Fill in any `templates/` companion files for the skills you'll use (personas, source paths, brand tokens); each skill's README section says what it expects
3. Invoke a skill with a natural request; check the output against the skill's shipped template

## Hooks and rules

Optional but recommended; this is where the compounding starts. See [the-system-layer.md](the-system-layer.md).
