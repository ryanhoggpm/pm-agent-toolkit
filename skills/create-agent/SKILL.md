---
name: create-agent
description: Designs and writes well-scoped working agents, either Claude Code subagents (.claude/agents/*.md) or Claude Managed Agents (API config), from a structured design interview covering scope-as-refusals, routing description, least-privilege tools and permission policies, output contract, self-verification, and a panel seat so every agent is usable standalone AND as a /panel-builder member. Use when the user says "create an agent", "I need a subagent for X", "turn this role into an agent", or when /panel-builder needs a working specialist no installed library covers. Do NOT use for advisory-only voices (use /panel-builder's persona schema) or repeatable workflows without their own context (use /create-skill).
---

# Create Agent

Builds agents that perform, not personas that pose. The output is a definition file
that survives three tests: it routes correctly (fires when it should, refuses when it
shouldn't), it returns a parseable result including a defined failure shape, and it can
take a seat on a `/panel-builder` panel without rewriting. One design core, two targets:
a Claude Code subagent or a Claude Managed Agent.

## Quick Start

```
/create-agent                        → design interview for a new agent
/create-agent <role or job>          → seed the interview, e.g. "API changelog auditor"
/create-agent review <path>          → audit an existing agent definition against the checklist
```

## Read first

| Source | Path | What to extract |
|---|---|---|
| Design reference | `references/agent-design.md` | The 9 decisions, in order; deployment-target comparison |
| Subagent template | `templates/subagent-template.md` | Output shape for Claude Code agents |
| Managed Agent template | `templates/managed-agent-template.yaml` | Output shape for API agents |
| Existing agents | `.claude/agents/` | Don't duplicate; extend or point at what exists |
| Panel persona schema | `/panel-builder`'s `templates/persona-schema.md` | The boundary: advisory voices go there, not here |

## Workflow

### Step 1: Gate
Run Decision 0 from `references/agent-design.md`. Advisory voice → persona schema.
Repeatable workflow → `/create-skill`. One-off task → just do the task. Only an
autonomous worker with its own context and tools proceeds. Say which gate fired and why.

### Step 2: Design interview
Walk decisions 1-8 with the user, in order: scope as refusals, routing description,
identity and hard rules, tools by least privilege, output contract with failure shape,
verification, model/effort, panel seat. Short questions, concrete defaults offered.
Two decisions are not skippable: the when-NOT clause in the routing description, and
the failure shape in the output contract. An interview that can't produce those isn't
done; the agent isn't ready to exist.

### Step 3: Pick the target and write the definition
Claude Code subagent (default for personal/workspace use) → fill
`templates/subagent-template.md`, save to `.claude/agents/<name>.md`. Managed Agent
(server-side, long-running, or part of a coordinator roster) → fill
`templates/managed-agent-template.yaml` and hand the user the create command. Same
design core either way; the reference's deployment table covers the differences. Note
that subagent files load at next session start; offer an immediate first run with the
definition inlined into the dispatch prompt.

### Step 4: Smoke test the routing
Write 3 prompts that should route to this agent and 2 that shouldn't. Check all 5
against the description text alone and show the user the result. Fix the description
before shipping, not after the first misfire.

### Step 5: Register the panel seat
If `/panel-builder` charters exist, tell the user which chartered panels (if any) this
agent could join, and add it to the sourcing answer for future intakes. The panel-seat
section is what makes that a one-line addition instead of a rewrite.

## Hard rules

1. **Every mutating tool is defended in writing.** Write, Edit, Bash, or any
   side-effecting MCP tool appears only with a stated reason and an exact
   what-may-change scope. Default toolset is read-only.
2. **No agent without a failure shape.** "Returns a labeled partial with what's
   missing" is the minimum. Confident guesses are the failure mode this rule kills.
3. **The definition carries identity, never the task.** Tasks arrive at dispatch;
   a task baked into the definition makes the agent single-use and stale.
4. **Autonomy is earned, not designed.** New agents with mutating tools start
   supervised (`always_ask` on Managed Agents; reviewed output in Claude Code) and
   loosen only after real runs.
5. **The panel seat ships by default.** Omit it only when the user explicitly wants a
   standalone-only agent, and say what that forfeits.

## Worked example (fictional)

Coppermine Systems needs pricing analysis on the CM-900 successor. The gate says agent
(it must read spreadsheets and prior deal files itself, not argue from a persona). The
interview yields `pricing-analyst`: scope refuses legal terms and final pricing
authority (names who owns each); tools `Read, Grep, Glob` plus `WebSearch` defended for
competitor list pricing; output contract is a margin table plus a 3-line recommendation,
failure shape "data gaps listed, no extrapolated margins"; verification recomputes every
margin once from source cells. Its panel seat: optimizes for realized margin and
discount discipline; decision criteria ordered margin floor → win rate → strategic
logo value; known bias "prices for margin, will underweight land-and-expand." Six weeks
later the same file joins Coppermine's `launch-review` panel (review-board mode)
unchanged, and the chair quotes its known bias when weighing it against the growth
lead's position. One definition, both uses. The routing smoke test caught that
"analyze our pricing page copy" wrongly matched the draft description; the when-NOT
clause now routes that to the marketing skill.

## Don't rationalize

| If you're thinking | Do this instead |
|---|---|
| "More tools make it more capable" | Every tool is attack surface and drift surface. Add each with a reason or not at all. |
| "The description is close enough" | Run the 5-prompt smoke test. Close enough is how agents fire on everything. |
| "It'll never fail, skip the failure shape" | It fails on its first missing input. Define the partial-result shape now. |
| "This agent could also handle..." | Scope creep at birth. New job, new agent, or explicit scope amendment with the user. |
| "Skip the panel seat, it's just a worker" | Three fields now versus a rewrite when a panel needs this expertise later. |

## Exit checklist

Before presenting the definition, verify:

- [ ] Gate result stated (agent, not skill or persona) with the reason
- [ ] Routing description has what / when / when-NOT, and passed the 5-prompt smoke test
- [ ] Scope includes explicit refusals with named owners for out-of-scope work
- [ ] Tool list is least-privilege; every mutating tool defended; Managed Agent configs gate bash and MCP toolsets `always_ask`
- [ ] Output contract defined, including the failure shape
- [ ] Verification-before-returning checklist present in the definition
- [ ] Panel seat present (optimizes-for, decision criteria, known bias) or its omission explicitly chosen
- [ ] Saved to the right target path; first-run option offered

## Handoff

- **Before this:** `/context-search` for prior agents or skills covering the job;
  Decision 0 may route away entirely.
- **Instead, when it fits:** `/create-skill` for workflows; `/panel-builder`'s persona
  schema for advisory voices.
- **After this:** `/panel-builder` to seat the agent on a chartered panel; a supervised
  first run before any autonomy expands.
