# The system layer

Skills are half of a working PM workspace. The other half is the machinery around them. This toolkit ships that machinery. Stubs below are filled in as each piece lands.

## Hooks (`hooks/`)

- `track-skill-usage.sh`: logs every skill invocation (`timestamp | skill | args`) to a file. Feeds the weekly review.
- `session-start.sh`: injects your last few skill usages and git status at session start.
- `post-compact.sh`: after context compaction, re-surfaces what you were doing.
- `track-visual-taste.sh`: on HTML/CSS edits, nudges Claude to log design feedback to a taste file.

Wiring instructions and settings.json snippets: `hooks/README.md`.

## Rules (`rules/`)

- `writing-style.md`: voice rules and audience-specific formats, enforced every session.
- `sensitive-data.md`: a data-classification and masking workflow that loads only when you touch spreadsheets or a sensitive-data folder (path-scoped rule).
- `system-learning.md`: the usage-log → weekly-review → learning-log loop that makes the workspace improve itself.

## The loop

1. Hooks log what you actually use.
2. Weekly review reads the log: which skills fired, which outputs you edited heavily.
3. Corrections become rule updates or skill fixes.
4. Next week starts better than this one.
