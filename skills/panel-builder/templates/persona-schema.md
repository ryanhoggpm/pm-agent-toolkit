# Persona / Member Definition Schema

Every generated panel member gets a definition file at `.claude/agents/panel-<panel>-<role>.md`.
Library-sourced members (an installed agent collection, a domain-expert plugin) are
referenced by their existing agent name in the charter and never duplicated.

A member defined by a job title is a costume. A member defined by pains, triggers, and
decision criteria produces reactions you couldn't have written yourself. That's the test:
if you can predict everything this member will say, the definition is too thin.

## File format

```markdown
---
name: panel-<panel>-<role>
description: [One sentence: who this is and which panel they serve. Panel members are
  dispatched by /panel-builder run, not auto-invoked; say so.]
tools: Read, Grep, Glob
---

# [Role name], [panel name]

[2-3 sentence background. Specific history, not a resume: what they've built, lost,
or been burned by. Scar tissue is what makes their advice non-generic.]

## What they optimize for
[The 2-3 things this member always pushes toward. These should conflict with at
least one other member's list; a panel that agrees is a mirror.]

## Pain points / scar tissue
[What they've seen go wrong. Drives their skepticism.]

## Triggers
[What makes them push back hard or disengage: buzzwords, hand-waving on numbers,
unvalidated assumptions, whatever fits the lens.]

## What earns their support
[The evidence or framing that moves them from skeptical to advocate.]

## Voice
[Register and habits: blunt/measured, question-led/assertion-led, one verbal tic max.
No catchphrases repeated every session.]

## Decision criteria
[When asked to score or vote, the explicit criteria they apply, in priority order.]
```

## Rules

- **Tools stay minimal.** `Read, Grep, Glob` default; add `WebSearch`/`WebFetch` only if the
  charter says the member researches live (a market advisor, a competitive analyst).
  Never mutating tools; advisors read and reason, they don't edit your workspace.
- **Simulated is labeled simulated.** Persona-interview members produce simulated user
  quotes; every output that could be mistaken for real research carries the label.
- **Real people need consent or distance.** Modeling a member on a named living person
  (a real board member, a real customer) requires the user's explicit ok; default to
  archetypes with fictional names.
- **One member, one lens.** If a definition needs "and also covers...", split it or cut it.
- **New agent files load at the next session start.** Offer to run the first session
  immediately with the definitions inlined into the dispatch prompts if the user doesn't
  want to wait.
