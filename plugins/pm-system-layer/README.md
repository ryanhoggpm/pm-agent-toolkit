# pm-system-layer

Four small shell hooks that make a skill workspace self-aware. All fail silently; none can interrupt a session. They assume the [workspace conventions](../../docs/workspace-setup.md) and write logs to `.claude/logs/` (add it to `.gitignore` if you don't want usage logs committed).

| Hook | Event | What it does |
|---|---|---|
| `session-start.sh` | SessionStart | Prints recent skill usage and uncommitted git changes into the opening context |
| `track-skill-usage.sh` | PostToolUse (Skill) | Appends `timestamp \| skill \| args` to `.claude/logs/skill-usage.log` |
| `post-compact.sh` | PostCompact | After compaction, re-surfaces the last skills used and points at `/context-search` for recovery |
| `track-visual-taste.sh` | PostToolUse (Write\|Edit) | When a visual file is touched, reminds Claude to log any design feedback from the turn to `context/design-taste.md` |

Why they matter: the usage log powers the weekly review of which skills earn their keep; session-start means no session opens blind; post-compact turns compaction from silent amnesia into a recoverable event; visual-taste accumulates your design preferences instead of re-litigating them per session. More in [the-system-layer.md](../../docs/the-system-layer.md).

## Install

**As a plugin (Claude Code and Cowork).** The hooks wire themselves through `hooks/hooks.json`:

```
/plugin marketplace add ryanhoggpm/pm-agent-toolkit
/plugin install pm-system-layer@pm-agent-toolkit
```

In claude.ai or the desktop app, add the marketplace at **Customize > Plugins > Add > Add marketplace** and add `pm-system-layer`. Cowork runs the hooks; Chat ignores hooks.

**By hand (Claude Code).** Copy `hooks/*.sh` into your project's `.claude/hooks/`, make them executable, then wire them in `.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      { "matcher": "startup|resume", "hooks": [
        { "type": "command", "command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/session-start.sh" }
      ] }
    ],
    "PostCompact": [
      { "hooks": [
        { "type": "command", "command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/post-compact.sh" }
      ] }
    ],
    "PostToolUse": [
      { "matcher": "Skill", "hooks": [
        { "type": "command", "command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/track-skill-usage.sh" }
      ] },
      { "matcher": "Write|Edit", "hooks": [
        { "type": "command", "command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/track-visual-taste.sh" }
      ] }
    ]
  }
}
```

The scripts need bash and python3, so on native Windows run Claude Code under Git Bash or WSL. `track-visual-taste.sh` has a path-pattern case statement near the top; point it at your workspace's visual directories.
