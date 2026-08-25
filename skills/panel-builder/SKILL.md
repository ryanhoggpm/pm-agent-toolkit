---
name: panel-builder
description: Assembles and runs on-demand expert panels, a composition layer over whatever agent libraries you have installed. Charters a team through a guided intake (job to be done, roster, interaction mode, success criteria), generates persona members where no library agent fits, and executes sessions in one of five modes (specialist-consult, weighted-panel, review-board, persona-interview, board-session). Use when the user says "assemble a panel of experts", "I need a board of directors", "interview my user personas", "get this reviewed from multiple perspectives" with a custom roster, or "/panel-builder". Do NOT use for pressure-testing marketing drafts against a fixed buyer panel; that standing panel is /creative-agency.
---

# Panel Builder

Builds the expert team, then runs it. One meta-skill instead of a new orchestration skill
per need. Each panel is defined by a **charter** (its mini-PRD) and executed by the runner
against one of five interaction modes. Charters are standing infrastructure: charter once,
rerun forever. GitHub is full of repos with hundreds of agents; the missing piece is the
layer that composes a few of them, on purpose, around one question. That's this skill.

## Quick Start

```
/panel-builder                      → guided intake for a new panel
/panel-builder run <name> [input]   → execute a chartered panel on a question/draft
/panel-builder list                 → list charters and their modes
/panel-builder amend <name>         → change a charter's roster, mode, or context
```

## Read first

| Source | Path | What to extract |
|---|---|---|
| Interaction modes | `references/interaction-modes.md` | The five choreographies; the charter picks one |
| Charter template | `templates/panel-charter.md` | Every section the intake must fill |
| Persona schema | `templates/persona-schema.md` | Format for generated member files |
| Existing charters | `outputs/panels/*/charter.md` | Don't charter a duplicate; amend instead |
| Installed libraries | `.claude/agents/` + installed plugins | Reuse before generating |

## Workflow: new panel (intake)

### Step 1: Frame the job
Get, conversationally or with a short structured question set: the job to be done (what
decision or output, why now), the interaction mode (recommend one from
`references/interaction-modes.md` and say why), how the user interacts (they present /
the panel interviews them / working session), success criteria, and cadence (one-time,
on-demand, standing). If the request maps onto an existing charter or a dedicated skill,
say so and stop.

### Step 2: Source the roster
For each lens the job needs, check what's already installed before generating:

| Need | First check |
|---|---|
| Engineering, security, ops, and similar practitioner lenses | The user's installed `.claude/agents/` collections and agent plugins |
| Deep scientific/engineering domain rigor | Domain-expert profile libraries (e.g. K-Dense-AI/scientific-agents, installable as a plugin) |
| Famous-expert flavor (board mode, only if asked) | Expert-persona libraries (e.g. K-Dense-AI/mimeographs); adapt, don't install-and-trust |
| Working specialist no library covers (needs its own tools to verify claims against real files) | Build with `/create-agent`; its panel-seat section makes the agent dispatchable here and standalone |
| Product user personas, advisory voices, board members | Generate per `templates/persona-schema.md` |

3-6 members. Each needs a lens that conflicts with at least one other member's. If the
user names a real living person as a model, confirm they want that; default to archetypes.

### Step 3: Write the charter
Fill `templates/panel-charter.md` completely, save to `outputs/panels/<name>/charter.md`.
No TBD sections; an intake that can't fill success criteria isn't done.

### Step 4: Generate member files
For each generated member, write `.claude/agents/panel-<name>-<role>.md` per the schema.
Minimal read-only tools. Library members are referenced in the charter by their existing
agent name, never copied. New agent files load at next session start; offer to run the
first session now with the definitions inlined into the dispatch prompts.

### Step 5: Offer the first run
A charter that's never run is a doc, not a panel.

## Workflow: run

1. Load the charter; read its standing-context files (cap 5).
2. Take the user's input for this session (question, draft, decision memo). One question
   per session; if the input is three questions, say so and have them pick.
3. Execute the charter's mode choreography from `references/interaction-modes.md`,
   dispatching members as subagents. Every dispatch prompt carries: the member's
   role/mandate, the real context for this session (facts and file paths, not vibes),
   and one pointed question. Parallel dispatch wherever the mode allows; for rebuttal
   rounds, continue the same agents so they argue from what they already said.
4. Synthesize per the mode's output format, scored against the charter's success criteria.
5. Save to `outputs/panels/<name>/session-YYYY-MM-DD-<slug>.md`. Present the synthesis
   and the decision (if any); the panel informs, the user decides.

## Hard rules (all modes)

1. **Conflicts flagged, never smoothed.** Disagreement between members is the product,
   not a defect. A unanimous panel gets one extra check: who should have dissented? In
   board mode, assign the counter-case and require a falsifiable test.
2. **Pointed dispatch, never "review this."** Each member gets their mandate, the real
   facts, and a specific question.
3. **Simulated is labeled simulated.** Persona outputs carry the label on every artifact;
   simulated quotes are never formatted as real research.
4. **The panel advises; the user decides.** No mode auto-decides, votes on their behalf,
   or buries the dissent.
5. **One question per session.** Scope creep in the input gets flagged before dispatch.

## Worked example (fictional)

Priya, founder of Harborlight Analytics, charters **personal-board** (board-session mode):
three archetype advisors generated from the persona schema, a revenue pragmatist ("what
does this do to runway"), a product-purist founder mentor ("every services hour is a
product hour you sold"), and an ex-agency owner who scaled then regretted a services arm.
First session: "Should I take the fractional-CPO contract or stay full time on product?"
All three lean take-the-contract, which trips hard rule 1: the chair assigns the
counter-case to the founder mentor, who argues the strongest decline case and ends it
with a falsifiable test: "if trailing-30-day activation doesn't improve by October 15
while you're consulting 15 hours a week, the contract is eating the company; drop it."
The synthesis preserves that as the board's standing tripwire. Second run costs nothing:
the charter, roster, and standing context already exist.

Same skill, different mode: Coppermine Systems' PM charters **cm-thermal** (specialist-
consult) for the CM-900 successor's fanless-enclosure question, sourcing the lead and two
specialists straight from an installed engineering-agent plugin, no personas generated
at all. Sourcing from libraries first is the point of Step 2.

## Don't rationalize

| If you're thinking | Do this instead |
|---|---|
| "I'll just write a quick custom orchestration for this one" | That's what this skill replaces. Charter it; 10 minutes now, reusable forever. |
| "All five members basically agree, clean synthesis" | Re-check the roster. Either the lenses overlap too much or a dissent got smoothed. |
| "The persona would obviously love this idea" | Then the persona is too thin. Answer from scar tissue and triggers, not enthusiasm. |
| "Skip the charter, run it inline" | Inline panels evaporate. The charter is what makes the second run cost nothing. |
| "More members = better coverage" | Past 6, members repeat each other and synthesis mushes. Cut to the conflicting lenses. |

## Exit checklist

Before presenting intake or session output, verify:

- [ ] Charter complete: no TBD sections, success criteria concrete, one mode chosen
- [ ] Roster: 3-6 members, library-first sourcing checked, each lens conflicts with another
- [ ] Dispatches carried mandate + real context + one pointed question each
- [ ] Synthesis names every inter-member conflict and preserves dissent in the member's words
- [ ] Unanimity handled: assigned counter-case with a falsifiable test where the mode requires it
- [ ] Simulated-content label present where the mode requires it
- [ ] Session saved to `outputs/panels/<name>/`; charter amendment logged if roster/mode changed

## Handoff

- **Before this:** `/context-search` for prior work on the session's question.
- **Instead, when it fits:** `/creative-agency` for marketing-draft reaction testing; its
  weighted panel is a permanent instance of what this skill builds on demand.
- **After this:** a decision doc when a session produces a real decision; `/html-render`
  if a synthesis needs to travel as a page.
