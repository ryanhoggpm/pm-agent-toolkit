# Build Type Routing

One build, one primary type. Classify by what ships, not by what's used to make it.

| | `code` | `ui` | `agent-asset` | `doc` |
|---|---|---|---|---|
| **Examples** | MCP server, CLI, web app feature, automation module, script | Landing page, UI mock or clickable prototype, interactive demo | New skill, subagent, panel, hook, rule file | Exec deck, partner guide, release notes, brief, battle card |
| **Build home** | Spec-kit repo `~/src/[slug]/` (existing repo: its clone path) | `outputs/builds/[slug]/` (production UI moves to the target repo as `code`) | `.claude/skills/`, `.claude/agents/`, `outputs/panels/` | `outputs/builds/[slug]/`, final copy to the right `outputs/` folder |
| **Why phase** | PRD (solution-level) | PRD (kickoff or solution-level) | Brief in BUILD.md | Brief in BUILD.md |
| **Spec form** | `speckit-specify` + `speckit-clarify` in repo | `spec.md` in build folder | `spec.md` in build folder | `spec.md` in build folder (stories = reader jobs) |
| **Plan/tasks** | `speckit-plan`, `speckit-tasks`, `speckit-analyze` | `plan.md`, `tasks.md` | `plan.md`, `tasks.md` | `plan.md` (outline, sources, audience), `tasks.md` |
| **Build skills** | `speckit-implement` | Design system or brand skill named in plan.md | `/create-skill`, `/create-agent`, `/panel-builder` | Deck or document skill, `/html-render`, `/tech-writer` |
| **Converge** | `speckit-converge` loop + test run | Acceptance walk + browser screenshot | Acceptance walk + routing smoke test + one live invocation | Acceptance walk + render check (file opens, HTML renders offline) |
| **Default review lenses** | Engineering, security, skeptic, + domain expert | Design, end user, engineering | Skeptic, engineering, + the asset's real user | Executive or audience, skeptic, + domain expert |

## Tie-breakers

- **Clickable demo no one will deploy:** `ui`, not `code`.
- **Skill that wraps a script:** `agent-asset`. The script is a task inside it, not a separate code build.
- **Deck plus a demo app:** two builds. Run the one needed first; log the other in BUILD.md as a follow-on.
- **A repo with its own release process** (a published package, a certified collection): `code`, and that repo's process governs. Skip spec-kit's repo creation; still run specify through tasks for the feature.
- **Changes to another team's product code:** not a pm-build target. Produce a PRD and tickets for that team instead.

## Spec-kit repo notes

- Init: `specify init [slug] --integration claude --non-interactive` from `~/src/`. Existing repo: `specify init --here --integration claude --non-interactive` inside it, then review `git status`.
- Skills land at `[repo]/.claude/skills/speckit-*/SKILL.md`; state at `[repo]/.specify/`; feature artifacts at `[repo]/specs/[NNN-feature]/`.
- The active feature is tracked in `.specify/feature.json`, not the git branch.
- Record `specify --version` in BUILD.md.
