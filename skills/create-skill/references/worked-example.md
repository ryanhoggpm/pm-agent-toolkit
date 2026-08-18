# Worked example: building `churn-postmortem`

A PM at Harborlight Analytics (fictional B2B SaaS, ~200 customers) keeps writing the same document every time a logo churns: what happened, what the signals were, what changes. Third time pasting the same instructions, they run `/create-skill`.

## Discovery (condensed)

**Job in one sentence?**
"When a customer churns, produce a one-page postmortem: timeline, missed signals, root cause, and one process change, so the exec team stops getting a different format every time."

**Trigger phrases?**
"churn postmortem for Acme", "we lost [customer], write it up", "why did [customer] leave".

**What does done look like?**
A one-pager in `outputs/postmortems/`, exec-readable, ending with exactly one recommended process change. Multiple recommendations is the failure mode; nobody acts on a list of five.

**Context needed?**
`context/customers/<name>.md` (account notes), `context/meetings/` (QBR and support escalation notes mentioning the customer), prior postmortems in `outputs/postmortems/` for signal patterns.

**Chains with?**
After: their status-update workflow picks up the process change. Before: nothing.

**Great vs. mediocre output?**
"Great names the first missed signal with a date. Mediocre says 'communication could have been better.'"

## The resulting description

```yaml
description: Write a one-page churn postmortem (timeline, missed signals,
  root cause, one process change) when a customer cancels. Use when the user
  says "churn postmortem for X", "we lost [customer], write it up", "why did
  [customer] leave", or names a churned account. Do NOT use for save-plays on
  at-risk accounts that haven't churned; handle those directly in conversation.
```

What/when in sentence 1, three trigger phrases, one boundary, third person, routable.

## The shipped folder

```
skills/churn-postmortem/
├── SKILL.md                      # 96 lines
└── templates/
    └── output-template.md        # Timeline / Signals we missed / Root cause / The one change
```

Key excerpts from the SKILL.md body:

```markdown
## Read first

| Source | Path | What to extract |
|---|---|---|
| Account notes | `context/customers/<name>.md` | Contract dates, owner, expansion/contraction history |
| Meeting notes | `context/meetings/` (grep customer name) | Escalations, QBR sentiment, dates of each |
| Prior postmortems | `outputs/postmortems/` | Recurring signals; whether this churn repeats a known pattern |

If no account notes exist, say so in the output's first line and build the
timeline from meeting notes alone. Don't invent account history.

## Don't rationalize

| If you're thinking | Do this instead |
|---|---|
| "Several changes are justified, I'll recommend three" | Pick the one with the earliest missed signal. The template has one slot on purpose. |
| "No meeting notes mention them, I'll generalize" | State "no recorded touchpoints found" as a finding. A silent account IS the missed signal. |
```

## What the exit checklist caught

First test run produced a postmortem whose root cause ("product gaps") didn't cite a date or source. The checklist item "every claim traces to a source file or the user's input" flagged it; the fix went into the read-first table (extract *dates*, not just events), not into a longer prompt. That's the loop working: failures route back into the skill file, once, instead of into every future conversation.
