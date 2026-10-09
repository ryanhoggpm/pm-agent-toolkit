---
name: pm-build
description: Gated orchestrator that takes a new build from why to a converged deliverable. Defines the problem, writes a testable spec, plans tasks, assembles a builder team and a review panel, builds, and converges against acceptance criteria, with an approval gate after each phase and all state in a resumable BUILD.md. Routes code to a spec-kit repo and non-code (UI mocks, skills or agents, decks, docs) to outputs/builds/. Use when starting a project or multi-step deliverable that needs requirements, a spec, and a team, or when resuming one. Do NOT use for a PRD alone, a one-off deck, a throwaway prototype, or a single skill or agent whose requirements are already clear; use /create-skill or /create-agent for those.
compatibility: Claude Code for the full flow (spec-kit repos, worktree builders). Cowork runs non-code builds; code builds need a local repo. Needs uv for spec-kit on code builds.
---

# PM Build

Chains definition, spec-driven development (spec-kit), and review panels so every build has a stated why, a testable spec, a named team, and a verified finish. Done means: the deliverable exists, every P1 acceptance criterion has evidence, and the user chose ship, iterate, or park at Gate 4.

## Quick start

```
/pm-build [idea or PRD path]       start a build at Phase 0
/pm-build resume [slug]            continue from BUILD.md's current phase
/pm-build status [slug]            print phase, gate decisions, open items; no work
/pm-build --short [idea]           small build: skip clarify, analyze, and the spec panel run
```

**What you get:** `outputs/builds/[slug]/` with `BUILD.md` (state and decision log), `spec.md`, `plan.md`, `tasks.md`, the review panel charter, and the deliverable (in the build folder, its workspace home, or a spec-kit repo at `~/src/[slug]/`).

Resume is the normal case. Non-code builds take one or two sessions; code builds take several.

## Hard rules

1. **Gates wait.** Each gate stops for the user's explicit approve, revise, or kill. Never auto-pass a gate, and approval at one gate never carries to the next.
2. **One build, one primary type.** If the idea spans two (an API client plus a launch deck), the secondary becomes a follow-on build logged in BUILD.md.
3. **The spec changes before the code does.** A gap found mid-build stops the task and goes back through spec.md as a logged change.
4. **Existing skills do the work.** Call the installed PRD, design, ticket, and panel skills; don't re-implement them inline.

## Read first

| Source | Path | What to extract |
|---|---|---|
| Type routing | `references/routing.md` | Build home, spec form, build skills, default review roster per type |
| Team composition | `references/build-team.md` | Builder and reviewer sourcing, dispatch rules, parallelism |
| Constitution seed | `references/constitution-seed.md` | Principles for `speckit-constitution` (code) or plan.md constraints (non-code) |
| State template | `templates/build-state.md` | `BUILD.md` structure |
| Existing builds | `outputs/builds/*/BUILD.md` | Don't start a duplicate; offer resume |
| Prior work | `/context-search [topic]` if installed, else a search of `context/` and `outputs/` | PRDs, analyses, prototypes, decisions already done |
| Workspace rules | `.claude/rules/`, project `CLAUDE.md` or project instructions | Writing style, product framing, repo hygiene that every document follows |

If a listed skill isn't installed, do that step directly and say so in BUILD.md.

## Workflow

Each phase writes its result to `BUILD.md` before moving on.

### Phase 0: Intake and route

1. If the argument is a PRD or a `BUILD.md`, load it. `resume` reads `BUILD.md` and jumps to its recorded phase.
2. Search prior work on the topic. Surface overlapping PRDs, prototypes, or builds; if a build exists, offer resume.
3. Classify the deliverable as `code`, `ui`, `agent-asset`, or `doc` using `references/routing.md`.
4. Pick a kebab-case slug and create `outputs/builds/[slug]/BUILD.md` from the template.
5. Name the output files now. If the build looks bigger than one deliverable, flag it.

### Phase 1: Define the why, then Gate 1

1. **PRD exists:** check it against the Gate 1 bar and list gaps.
2. **No PRD:** for `code` and `ui`, run the workspace's PRD skill if one is installed, or write a short PRD into the build folder. For `agent-asset` and `doc`, write a one-page brief in `BUILD.md`: problem, user, trigger, what done looks like, non-goals, success signal.
3. If the build needs budget or headcount, or its value is unproven, flag a business case or sizing step. Flag it; don't run it unless asked.

**Gate 1 bar:** named persona, trigger, and outcome; explicit non-goals; one measurable success signal; build type and home confirmed. Present the why in five lines or fewer plus the gap list. Wait.

### Phase 2: Spec the what, then Gate 2

**`code`:**
1. Check `specify --version`; if missing, `uv tool install specify-cli`.
2. Create or confirm the repo at `~/src/[slug]/` (on WSL, the Linux filesystem, not `/mnt/c`). Run `specify init [slug] --integration claude --non-interactive`, or `specify init --here --integration claude --non-interactive` inside an existing repo.
3. Follow the spec-kit skills by reading `[repo]/.claude/skills/speckit-[step]/SKILL.md` with the repo as working directory (absolute paths). The PRD supplies `$ARGUMENTS`. If script execution fails, write a handoff prompt to `BUILD.md` for a session opened in the repo.
4. `speckit-constitution` with the seed from `references/constitution-seed.md`, adapted to the repo.
5. `speckit-specify` with the PRD's problem, users, stories, and non-goals, no stack. Then `speckit-clarify` (skip with `--short`).

**Non-code:** write `outputs/builds/[slug]/spec.md` in spec-kit shape: prioritized user stories (P1, P2, P3), Given/When/Then acceptance criteria, edge cases, non-goals. Each story is independently demoable.

**Spec review (skip with `--short`):** charter the build's review panel (`references/build-team.md`) and run it on the spec with one question: "What requirement here will we regret, or is missing?"

**Gate 2 bar:** every P1 story has testable acceptance criteria; no `[NEEDS CLARIFICATION]` markers left; panel conflicts listed, not smoothed. Wait.

### Phase 3: Plan and assemble the team, then Gate 3

1. **Plan.** `code`: `speckit-plan` with the stack the user gives (ask if absent and offer a recommendation), then `speckit-tasks`, then `speckit-analyze` unless `--short`. Non-code: write `plan.md` (approach, design source, constraints from the constitution seed) and `tasks.md` (ordered, `[P]` marks parallel-safe, each task tagged with its story).
2. **Design source** for `ui` or any visual deliverable: the project's design system or brand skill. Record which one and its version in `plan.md`.
3. **Builder roster.** Group tasks and map each group to a builder per `references/build-team.md`, installed agents first. A recurring gap that needs its own tools gets `/create-agent`; a gap that needs only a voice goes to the panel.
4. **Review panel.** Confirm or amend the charter at `outputs/panels/build-[slug]/charter.md`.
5. Write the roster, task-to-builder map, and parallel plan into `BUILD.md`.

**Gate 3 bar:** every task has an owner; parallel tasks touch disjoint files; any new agent's routing smoke test passed; the plan passes the constitution check. Wait.

### Phase 4: Build

Execute `tasks.md` in dependency order, one phase or user story at a time, marking tasks `[x]` as they finish.

| Type | Build path |
|---|---|
| `code` | `speckit-implement`, scoped per phase. Parallel builders run in separate worktrees; the main session merges. |
| `ui` | The design system skill from `plan.md`; production UI follows the target repo's conventions |
| `agent-asset` | `/create-skill` for workflows, `/create-agent` for workers, `/panel-builder` for panels. Spec acceptance criteria answer their design interviews. |
| `doc` | The workspace's deck, document, or `/html-render` skill; `/tech-writer` for product docs |

### Phase 5: Converge and review, then Gate 4

1. **Converge.** `code`: run `speckit-converge` and implement whatever it appends until it reports Converged. Non-code: walk every acceptance criterion and mark pass or fail with evidence (file, screenshot, render, test output).
2. **Verify for real.** Run tests, render the deck, smoke-test skill or agent routing, open the UI. Converged without execution evidence is not converged.
3. **Panel run** on the deliverable: "Does this meet the spec and the why, and what would block shipping it?"
4. **Pre-ship checks:** secret scan before any external push; the repo's attribution and commit-message rules.

**Gate 4:** present pass/fail by story, panel conflicts, and open items tiered as blocking or post-ship. The user picks ship, iterate (back to Phase 4 with named tasks), or park. On ship, offer to file follow-ons in the team's tracker (Jira, Linear, GitHub Issues) and to move finalized docs into `context/`.

## Worked example (fictional)

A PM at Coppermine Systems runs `/pm-build a CLI that exports CM-900 port inventory to CSV`. Phase 0 classifies it `code`, slug `port-export`. Gate 1 pins the persona (a field engineer auditing a rack), the trigger (pre-migration inventory), and the success signal (export of 48 ports in under 10 seconds). Phase 2 inits `~/src/port-export/` with spec-kit; Gate 2's panel flags a missing story for partial-failure output. The build runs one builder, converges with a passing test run, and Gate 4 ships with two post-ship items filed as issues.

## Exit checklist

- [ ] **BUILD.md is current:** phase, every gate decision with date, every spec change, roster
- [ ] **Traceability:** every task maps to a story, every story to the why, every acceptance criterion has evidence at Gate 4
- [ ] **No silent scope growth:** anything not in spec.md is logged as a spec change or deferred
- [ ] **Existing skills did the work:** no re-implemented PRD, design, ticket, or panel logic inline
- [ ] **Panel dissent preserved** in members' words at each gate
- [ ] **Specificity:** real file paths, repo names, versions, and ticket keys

## Related skills

**Before:** `/context-search`. **Inside:** `/panel-builder`, `/create-agent`, `/create-skill`, `/html-render`, `/tech-writer`, spec-kit skills in the build repo. All optional; each step names its fallback.
