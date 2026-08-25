# Panel Charter: [panel-name]

**Created:** [date]
**Status:** Active / Retired
**Mode:** [specialist-consult | weighted-panel | review-board | persona-interview | board-session]
**Cadence:** [on-demand | standing (weekly/monthly) | one-time]

## Job to Be Done

[What you need from this panel and why now. One paragraph. If the panel exists to
support a specific decision, name the decision and its deadline.]

## Success Criteria

[What a good session produces. Concrete: "a ranked option list I can act on Monday,"
not "useful insights." The synthesis step scores itself against this section. One test
worth stealing: "would I have paid for this hour?"]

## Roster

| Member | Lens / expertise | Sourcing | Weight |
|---|---|---|---|
| [role name] | [what they bring, stated as pains and decision criteria, not job title] | [library: `<agent name>` \| generated: `.claude/agents/panel-<name>-<role>.md`] | [% if weighted-panel mode, else n/a] |

**Chair / lead / synthesizer:** [which member frames and synthesizes, or "the orchestrating model directly"]

## Inter-Agent Protocol

- **Dispatch:** [parallel | sequential | staged (lead first, then subset)]
- **Debate rules:** [none (collect and synthesize) | cross-examination round | positions then rebuttal]
- **Conflict handling:** flagged explicitly in synthesis, never smoothed. Minority opinions preserved.

## How You Interact

[They interview you / you present to them / working session. State what you bring to
each session (a question, a draft, a decision memo) and what format you get back.]

## Session Output

- **Format:** [per the mode template in `references/interaction-modes.md`, plus any charter-specific sections]
- **Save path:** `outputs/panels/[panel-name]/session-YYYY-MM-DD-<slug>.md`
- **Sharing constraint:** [team-shareable | internal-only | personal, never shared]

## Standing Context

[Files each session loads before dispatch: strategy docs, prior session outputs, product
context from `context/`. Cap at 5 sources; a panel that reads everything reads nothing.]

## Amendment Log

[Date + one line per roster/mode change. The charter is current state; retired members
and abandoned modes get a line here, not residue in the sections above.]
