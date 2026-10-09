# Agent Design Reference

The decisions behind both templates, in the order to make them. Grounded in Anthropic's
published guidance: the Managed Agents docs (platform.claude.com/docs/en/managed-agents),
"Building Effective Agents," and "Building Effective Human-Agent Teams."

## Decision 0: Should this be an agent at all?

The simplest thing that works wins. Route before designing:

| The need | Build |
|---|---|
| A repeatable workflow the main session runs (steps, templates, checklists) | A skill, via `/create-skill` |
| An advisory voice that reasons and argues but never executes | A panel persona, via `/panel-builder`'s `templates/persona-schema.md` |
| An autonomous worker: own context, own tools, produces work product | An agent, this skill |
| A one-off task | Nothing; just do the task |

A skill is instructions the current context follows. An agent is a separate context
with its own tools and judgment. If the job doesn't need isolation or autonomy, the
skill is cheaper and easier to debug.

## Decision 1: Scope, stated as refusals

Write what the agent owns in one sentence, then the out-of-scope list. Scope defined
only positively creeps; the refusals are what hold. Each refusal names who handles the
job instead, so the agent degrades into a handoff, not a guess.

## Decision 2: The routing description

For subagents, the frontmatter `description` is the routing surface: sentence 1 what,
sentence 2 when (concrete triggers), sentence 3 when NOT (pointing at the alternative).
Vague descriptions are the top authoring failure: the agent either never fires or fires
on everything. Test it by writing three prompts that should route to the agent and two
that shouldn't, and checking all five against the description text alone.

## Decision 3: System prompt = identity + rules, never the task

The task arrives at dispatch time (a subagent prompt, a Managed Agent user event). The
definition carries what's true across every run: identity with real scar tissue, hard
rules with the failure each prevents, output contract, verification. A task baked into
the definition makes the agent single-use and stale.

## Decision 4: Tools by least privilege

Start from `Read, Grep, Glob` and add each tool with a written reason. Mutating tools
(Write, Edit, Bash, anything with side effects) get added only when producing that
change IS the job, and the Scope section must say exactly what may change. On Managed
Agents this becomes permission policy: `always_allow` for the read toolset, `always_ask`
on bash and on MCP toolsets until the agent has earned autonomy on supervised runs.
Autonomy expands in proportion to demonstrated reliability, not at design time. Never
give an agent credentials it can read as files; on Managed Agents, keep secrets in
vaults or behind authenticated proxies, out of the sandbox.

## Decision 5: Output contract, including the failure shape

Callers compose agents; composition needs parseable results. Define the sections,
format, and length cap, and define what comes back when the job can't be done: a
labeled partial with what's missing. An agent without a failure shape returns
confident guesses, which is worse than no agent.

## Decision 6: Verification before returning

The best agents check their own work before a human or coordinator sees it. Give every
agent a pre-return checklist (claims traced to sources actually read, numbers
recomputed, contract matched, scope not exceeded). For high-stakes outputs, split the
job into a doer-verifier pair: a second agent with fresh context reviewing against a
rubric catches what the author-context can't see.

## Decision 7: Model and effort

Default to the mid-tier model at high effort; step up to the top model only when a
supervised run shows quality gaps, and step down to the fast tier for high-volume
mechanical work. Record why in the definition when you deviate from the default;
"opus because it felt fancier" doesn't survive a cost review.

## Decision 8: The panel seat (dual-use)

Every agent built here should also be dispatchable as a panel member by an orchestrator
(this toolkit's `/panel-builder`, or a Managed Agents coordinator via `multiagent`).
That costs one section, three fields:

- **Optimizes for:** the pushes it brings to a group, capable of conflicting with
  another member's
- **Decision criteria:** explicit, ordered, so scores and votes are defensible
- **Known bias:** the systematic lean a chair should weigh in synthesis

The panel seat is what separates a reusable expert from a one-shot worker. A panel of
working agents (that can each read the actual artifact with their own tools) is
strictly stronger than a panel of prose personas when the question is technical:
personas argue from definition, agents argue from evidence. Keep persona-schema for
advisory voices where the value IS the argument (boards, mentors, buyer reactions);
build agents when the member should verify claims against real files before opining.

## Deployment targets

| | Claude Code subagent | Managed Agent |
|---|---|---|
| Definition | `.claude/agents/<name>.md`, YAML frontmatter + markdown body | Versioned API resource (`/v1/agents`), YAML/JSON config |
| Loads | Next session start (or inline the definition in a dispatch prompt to use it immediately) | Immediately on create; referenced by ID |
| Tools | Frontmatter `tools` allowlist | Toolsets + per-tool permission policies |
| Orchestration | Dispatched by the main session or a skill like `/panel-builder` | `multiagent` coordinator with a pinned agent roster; persistent context-isolated threads |
| Update | Edit the file | Versioned update API; coordinators pin roster versions and must be updated to pick up new ones |

Same design core, two serializations; the templates in `templates/` carry one each.
