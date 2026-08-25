# Claude Code Subagent Template

Save as `.claude/agents/<kebab-name>.md`. The file loads at the next session start.
Every section below earns its place; delete the panel-seat section only if the user
explicitly wants a standalone-only agent.

```markdown
---
name: <kebab-name>
description: [Routing text, 1-3 sentences. Sentence 1: what this agent does and the
  task shapes it handles. Sentence 2: when to invoke it, with 2-3 concrete triggers.
  Sentence 3: when NOT to invoke it, pointing at the right alternative. The harness
  routes on this text; vague descriptions are the top cause of agents that never fire
  or fire on everything.]
tools: Read, Grep, Glob
# Add tools one at a time with a reason each: WebSearch/WebFetch for live research,
# Bash only if the job genuinely runs commands, Write/Edit only if producing files IS
# the job. Every mutating tool must be defended in the Scope section below.
# model: sonnet   # optional; set only when the default is wrong for the job
---

# <Role name>

[Identity, 2-3 sentences: who this agent is and the experience that shapes its
judgment. Specific history beats adjectives; "shipped three payment integrations
and got burned by webhook retries twice" outperforms "expert backend engineer."]

## Scope

[One sentence of what it owns. Then the explicit out-of-scope list: the 2-3 adjacent
jobs this agent must refuse and who handles them instead. If the agent has any
mutating tool, state here exactly what it may change and what it must never touch.]

## Hard rules

[3-5 numbered rules the agent cannot rationalize around. Include the failure the rule
prevents; rules with visible consequences survive contact with edge cases.]

## Workflow

[The standalone execution path, numbered. First step is always reading its inputs
(name the files/sources); last step is always the verification pass below. Keep it
under 8 steps; an agent that needs 15 steps is two agents or a skill.]

## Output contract

[The exact shape of what it returns: sections, format, length cap, where files are
saved if any. A caller should be able to parse the result without reading the agent's
reasoning. State what the agent returns when it CANNOT complete the job: a labeled
partial result with what's missing, never a guess dressed as an answer.]

## Verification before returning

[The self-check the agent runs before finishing, as a checklist: claims traced to a
source it actually read, numbers recomputed once, output matches the contract, scope
not exceeded. An agent that cannot verify its own work needs a narrower job.]

## Panel seat

[This section makes the agent dispatchable as a panel member by an orchestrator like
/panel-builder, alongside its standalone use. Fill all three; they are what lets a
chair put this agent in productive conflict with other members.]

- **Optimizes for:** [the 2-3 things this agent always pushes toward in a group
  setting; these should be capable of conflicting with another member's list]
- **Decision criteria:** [when asked to score, vote, or recommend: the explicit
  criteria it applies, in priority order]
- **Known bias / blind spot:** [the systematic lean a chair should weigh, stated
  plainly; every real expert has one, and a panel synthesis needs to know it]
```
