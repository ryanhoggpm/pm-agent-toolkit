# Build Team Composition

Two groups per build. **Builders** do work with tools. **Reviewers** advise at gates. A builder never reviews its own output.

## Builders

Map task groups (from tasks.md) to builders. Source in this order and stop at the first fit:

1. **Main session.** Default for sequential work, merges, and anything touching shared files. Most small builds need no other builder.
2. **Installed working agents** in `.claude/agents/` or from plugins (code architects, code reviewers, security or SRE specialists).
3. **`/create-agent`** when a task group needs its own context and tools no installed agent has, and the role will recur. One-off needs get an inline dispatch prompt, not a new file. New agent files load next session, so dispatch the first run with the definition inlined.

**Dispatch rules:**
- Every builder prompt carries the task IDs, the relevant stories and acceptance criteria, the constitution or plan constraints, the exact file paths it owns, and what to return (diff summary, tests run, open questions).
- Parallel code builders work in separate git worktrees; only `[P]` tasks with disjoint files run in parallel. The main session merges and runs the full test suite after each merge.
- Cap parallel builders at 3 unless the user raises it.
- A builder that hits a spec gap stops and returns the gap. It does not decide requirements.

## Review panel

One panel per build, chartered with `/panel-builder` at `outputs/panels/build-[slug]/charter.md`, mode `review-board`. Without panel-builder, dispatch each reviewer lens directly with the gate question and collect answers side by side. It runs at Gate 2 (spec), Gate 4 (deliverable), and Gate 3 only when the plan carries a major architecture choice.

**Roster:** 3-5 members, starting from the type's default lenses in `routing.md`. Each lens must conflict with at least one other. Sources: installed reviewer agents, domain specialists, and generated personas for the deliverable's real users (a field engineer, a partner admin).

**Charter success criteria** come from spec.md: the P1 acceptance criteria plus the Gate 1 success signal.

**Gate questions:**
- Gate 2: "What requirement here will we regret, or is missing?"
- Gate 3 (optional): "Which plan decision is hardest to reverse, and is the spec behind it?"
- Gate 4: "Does this meet the spec and the why, and what would block shipping it?"

Panel output is advisory. Present conflicts in members' words; the user decides.

## When not to build a team

`--short` builds and single-file deliverables run with the main session as the only builder and skip the Gate 2 panel run. They still get a Gate 4 review from at least two lenses (skeptic plus the type's primary reviewer), dispatched directly.
