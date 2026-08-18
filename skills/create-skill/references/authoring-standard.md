# The authoring standard

Every skill shipped in this repo passes all ten rules below. `/create-skill` enforces them when drafting; CI lints the mechanical ones on every push. If you're contributing a skill, this is the review bar.

The rules exist because skills fail in predictable ways: they don't trigger, they produce generic output, or they drift into bloat that Claude stops following. Each rule closes one of those failure modes.

## The ten rules

### 1. Engineer the description for routing

Claude decides whether to load a skill from its name and description alone. The body never gets read if the description misses. So the description carries the routing load:

- Sentence 1 says what the skill does and when to use it.
- At least 3 trigger phrases, worded the way a user would actually type them.
- Exactly one boundary clause: "Do NOT use for X; use /other-skill instead" (or "handle directly"). One boundary keeps routing crisp; a pile of exclusions dilutes it.
- Third person throughout. The description is read by a router, not a person.
- Under 1024 characters.

### 2. Write the body in imperative voice

The body is instructions to Claude, not documentation about the skill. "Read the spec, extract every endpoint" beats "This skill reads the spec and extracts endpoints." Descriptive voice invites summarizing; imperative voice gets executed.

### 3. Ship a read-first table

Before generating anything, the skill names what to read. Format:

| Source | Path | What to extract |
|---|---|---|

Paths use the [workspace conventions](../../../docs/workspace-setup.md): `context/` for the user's knowledge base, `outputs/` for generated work. State what to do when a listed file is missing (ask, assume, or proceed with a flag). A skill without a read-first table produces boilerplate that ignores the workspace.

### 4. Keep SKILL.md under 350 lines, constraints in the top 100

Long skill files stop being followed; instructions past a certain depth get skimmed. Hard cap 350 lines, target under 300. Anything that must never be violated (approval gates, scope limits, data rules) lives in the top 100 lines. Background, rationale, and reference material move to `references/`.

### 5. Put the output template in `templates/`

The exact output structure ships as a file, not an inline sketch. Two reasons: the user can diff real output against it, and they can customize it without editing the workflow. Anything else a user would customize (personas, source paths, brand tokens, gate criteria) is also a companion file, never hardcoded in SKILL.md.

### 6. Include at least one worked example

A worked example shows a real input and the shaped output, using a fictional company only. Examples are how Claude calibrates depth and tone; without one, every run reinvents both. In this repo, fictional means fictional: no real employers, colleagues, customers, or internal hostnames, and CI greps for known markers.

### 7. Add an anti-rationalization table where steps get skipped

If a step is regularly tempting to skip ("the existence check is unnecessary, this is obviously new"), name the temptation and the counter in a two-column table. Claude rationalizes exactly like people do; pre-empting the specific excuse works better than repeating "always do X."

### 8. End with an exit checklist

A short, checkable list run before presenting output. Items are verifiable ("every claim has a source file cited"), not aspirational ("output is high quality"). The checklist is the last thing in the file so it's the last thing read before finishing.

### 9. Point at neighbors in a handoff section

Name what runs before this skill (what context to have ready) and after it (the natural next step), referencing only skills that exist in the same collection. Handoffs are how a toolkit becomes a workflow instead of a pile of commands.

### 10. Check for existing work before creating anything expensive

If the skill produces something costly to regenerate (a long document, a data pull, a scaffold), it first checks whether a prior version exists and offers to update instead of overwrite. Same rule at authoring time: before building a new skill, list installed skills and check for overlap. Two skills covering one job split the trigger phrases and both under-route.

## Mechanical requirements (CI-linted)

- Folder name is kebab-case and matches the frontmatter `name:` exactly.
- The file is named `SKILL.md`, case-sensitive.
- YAML frontmatter opens and closes with `---`; no angle brackets inside frontmatter.
- Description is 100 to 1024 characters and contains a routing boundary.
- SKILL.md is 350 lines or fewer.
- A read-first table, a `templates/` reference, and an exit checklist are present.

Run the same checks locally before a PR: `scripts/lint-skills.sh`.

## Common failure modes

**Under-triggering.** The skill exists but never loads. Almost always a description problem (Rule 1). Fix the description before touching the body.

**Generic output.** The skill runs but the output could have come from any workspace. Missing or vague read-first table (Rule 3).

**Template rot.** The output template has so many sections that Claude fills them all even when most don't apply. Mark optional sections "(only if relevant)".

**Scope sprawl.** The skill does three jobs and users keep redirecting it. Split it. A skill covers one job with one definition of done.

**Bloat.** Every edit adds a paragraph, nothing gets removed, and eventually the file stops steering behavior. When SKILL.md nears the cap, move background to `references/` before adding anything.
