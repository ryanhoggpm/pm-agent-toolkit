# The self-learning loop

The workspace improves itself through two files. Copy this rule into your project and wire the hooks in `hooks/README.md`; the loop doesn't run on good intentions.

## What gets tracked

**`.claude/logs/skill-usage.log`** (automated): the `track-skill-usage.sh` hook appends one line per skill invocation: `timestamp | skill | args`. Reviewed weekly.

**`context/learning-log.md`** (human-curated): updated at natural endpoints, i.e. after major outputs, weekly reviews, and corrections. Tracks:

- Skill quality notes: outputs you edited heavily, and what you changed
- Writing corrections: style adjustments that diverge from the current rules
- Stakeholder behavior that differs from their profiles
- Process wins worth repeating
- Calibration data: impact estimates vs. actuals after launches

## What Claude proactively does

- After 3+ similar writing corrections, suggests updating the style rule instead of eating the correction a fourth time
- After launches, prompts to capture estimate vs. actual
- At the end of major initiatives: "want me to update the context library with what we learned?"

## What Claude suggests but never does without approval

- New skill ideas, when a workflow keeps recurring uncovered
- Flagging stale context files
- Combining skills you always chain
- Updating stakeholder profiles when observed behavior diverges

**The rule: Claude always asks before changing anything in `context/`.** All learning lives in your own files; review, edit, or delete any observation at any time.

## The loop, end to end

1. Hooks log what actually gets used.
2. A weekly review reads the log: which skills fired, which outputs needed heavy editing.
3. Corrections become rule updates or skill fixes (route the fix into the file, once, instead of into every future session).
4. Next week starts better than this one.
