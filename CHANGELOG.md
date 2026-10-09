# Changelog

## 0.2.0 (2026-10-09)

**Install only what you need.** Every skill is now its own plugin, so the marketplace lists each one separately in Claude Code (`/plugin`) and in claude.ai and Cowork (Customize > Plugins). `pm-agent-toolkit` remains as a bundle that installs everything, so existing installs keep working. Each release also attaches one zip per skill for Customize > Skills > Upload.

- **New skill:** `pm-build`, a gated orchestrator from why to a converged deliverable.
- **New plugin:** `pm-system-layer` carries the hooks, which now wire themselves on install in Claude Code and Cowork.
- **Portable frontmatter:** skills use only Agent Skills spec keys, so every one uploads to claude.ai. `aliases` and `argument-hint` are gone; invoke skills by their names. Each skill gains a `compatibility` line.
- **Standalone skills:** no skill depends on files outside its own folder.
- **Current models:** the Managed Agent template defaults to `claude-opus-5-5` with the `auto` permission policy.
- **Layout:** skills moved from `skills/<name>/` to `plugins/<name>/skills/<name>/`; hooks moved to `plugins/pm-system-layer/hooks/`.

## 0.1.0 (2026-08-18)

Initial release.
