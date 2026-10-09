# The system layer

Skills are half of a working PM workspace. The other half is the machinery around them. This toolkit ships that machinery.

## Hooks (`pm-system-layer` plugin)

- `track-skill-usage.sh`: logs every skill invocation (`timestamp | skill | args`) to `.claude/logs/skill-usage.log`. Feeds the weekly review.
- `session-start.sh`: injects your last few skill usages and git status at session start, so no session opens blind.
- `post-compact.sh`: after context compaction, re-surfaces the last skills used and points at `/context-search` for recovery.
- `track-visual-taste.sh`: on HTML/CSS edits, nudges Claude to log design feedback to `context/design-taste.md`, so taste accumulates instead of being re-litigated per session.

Install as a plugin and the hooks wire themselves (Claude Code and Cowork; claude.ai chat ignores hooks). Manual wiring and the settings.json snippet: [plugins/pm-system-layer/README.md](../plugins/pm-system-layer/README.md).

## Rules (`rules/`)

- [`writing-style.md`](../rules/writing-style.md): voice rules, audience formats, the shareability guardrail, and how to edit documents when new information changes a conclusion. A starting set to personalize.
- [`recommended-workflows.md`](../rules/recommended-workflows.md): skill-chain recipes for the published skills.
- [`system-learning.md`](../rules/system-learning.md): the usage-log → weekly-review → learning-log loop that makes the workspace improve itself.
- [`sensitive-data.md`](../rules/sensitive-data.md): a data-classification and masking workflow, and the toolkit's demonstration of a **path-scoped rule**: `paths:` frontmatter loads it only when spreadsheets or a sensitive-data folder are touched, costing zero context otherwise. Copy that pattern for any rule with a natural file scope.

Install rules by copying into your project's `.claude/rules/`. Plugins can't carry rules, and rules load only in Claude Code. In claude.ai chat or Cowork, paste the parts you want into project instructions.

## The loop

1. Hooks log what you actually use.
2. Weekly review reads the log: which skills fired, which outputs you edited heavily.
3. Corrections become rule updates or skill fixes, routed into the file once instead of into every future session.
4. Next week starts better than this one.
