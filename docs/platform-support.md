# Platform support

The same plugin installs everywhere you use Claude, but each surface loads a different part of it. Skills travel everywhere. Hooks and agents need Cowork or Claude Code. Rules, CLAUDE.md, and the auto-memory folder are Claude Code features.

| Piece of this toolkit | claude.ai chat (web, desktop, mobile) | Cowork (desktop app) | Claude Code (terminal, IDE, desktop Code tab) |
|---|---|---|---|
| Skills | Loads. Scripts run in the code-execution sandbox | Loads | Loads |
| Hooks (`pm-system-layer`) | Ignored | Loads | Loads |
| Subagents a skill creates (`create-agent`, `panel-builder`) | Not available | Loads | Loads |
| Rules (`rules/`, copied to `.claude/rules/`) | Not read. Paste into project instructions | Not documented. Use project instructions | Loads |
| `CLAUDE.md` | Not read. Use personal preferences or project instructions | Not documented. Use project instructions | Loads |
| Memory | Chat's own memory feature | Per-project memory store | Auto-memory folder and CLAUDE.md |

**Claude Design** builds from design systems you import (a GitHub repo, design files, uploads). Anthropic's docs don't say whether it uses account skills, so treat the skills here as chat, Cowork, and Code tools.

## Where installs live

- **claude.ai and the desktop app** (Customize > Plugins or Customize > Skills): saved to your account. Plugins also sync into Claude Code at the next session start.
- **Claude Code CLI** (`/plugin install`): saved to that machine only.

## Per-skill notes

Each skill's frontmatter has a `compatibility` line naming where it works and what it needs. The ones with real limits:

| Skill | Limit |
|---|---|
| `context-search` | Needs a workspace folder to search; not useful in chat |
| `create-agent`, `panel-builder` | Write and dispatch subagents, so Claude Code or Cowork |
| `delegate-to-ollama` | Needs network access to an Ollama host; not chat |
| `delivery-review`, `bolt-dev` | Need a local git repo |
| `pm-build` | Full flow in Claude Code; Cowork handles non-code builds |
| `rag-agent-builder` | Python scripts; chat needs code execution enabled |

Sources: [Plugin feature support across platforms](https://claude.com/docs/plugins/platform-support), [Plugins](https://claude.com/docs/plugins/overview), [Cowork projects](https://claude.com/docs/cowork/guide/projects), [Create custom skills](https://claude.com/docs/skills/how-to). Checked 2026-10-09; Anthropic updates these surfaces often.
