---
name: create-skill
description: Build a new Claude skill to a 10-rule authoring standard (routing-engineered description, read-first table, shipped output template, exit checklist), or audit an existing skill against that standard. Use when the user says "make this a skill", "turn this workflow into a command", "build a skill for X", "review my skill", or catches themselves pasting the same instructions a second time. Do NOT use for one-off prompts or tasks that change shape every run; handle those directly in conversation.
---

# Create Skill

Turn a repeatable workflow into a skill that routes reliably and produces consistent output. Done means: a complete `skills/<name>/` folder that passes every rule in the authoring standard, tested with one trigger prompt and one boundary prompt.

Two hard constraints, before anything else:

1. **Never draft before the existence check (Step 1) and discovery confirmation (Step 2) are done.** A skill built on guessed requirements gets rebuilt.
2. **Fictional companies and people only** in examples, everywhere, always.

## Read first

| Source | Path | What to extract |
|---|---|---|
| Authoring standard | `references/authoring-standard.md` | The 10 rules the new skill must pass; the review bar for audits |
| Skill scaffold | `templates/skill-template.md` | Folder layout and SKILL.md structure to copy |
| Worked example | `references/worked-example.md` | Calibration: discovery depth, description shape, what the checklist catches |
| Installed skills | `.claude/skills/`, installed plugins | Overlap with the proposed skill; conventions already in use |
| Workspace conventions | project `CLAUDE.md`, `docs/workspace-setup.md` | Path defaults the new skill's read-first table should use |

If there's no project CLAUDE.md, use `context/` and `outputs/` as path defaults per workspace-setup.

## Workflow

### 1. Check what exists

List installed skills and scan their descriptions for the proposed job. Three outcomes:

- **Covered:** point at the existing skill; stop.
- **Adjacent:** propose extending it or carving a clean boundary between the two. Two skills sharing one job split the trigger phrases and both under-route.
- **New:** proceed.

### 2. Discover the job

Ask only the questions the user hasn't already answered:

1. The job in one sentence. What do they do today without the skill?
2. Trigger phrases: 3 to 5 things they'd actually type.
3. What does done look like? Output type, location, audience.
4. Which context files does it need? Which tools or MCPs?
5. What runs before or after it (chaining)?
6. What separates a great output from a mediocre one? What would make them edit it heavily?

Then confirm: "Here's what I'm building: [job, triggers, output, key context sources]." Don't draft until confirmed.

### 3. Design before drafting

Settle three things:

- **Shape:** sequential workflow, draft-review-improve loop, multi-source synthesis, or context-routed variants.
- **Scope:** one job, one definition of done. If the design needs "and also", it's two skills; build the smaller one first.
- **Companion files:** anything the user would customize (personas, source paths, criteria, brand tokens) becomes a file in the new skill's `templates/` or `references/`, never hardcoded in the body.

### 4. Draft the skill

Copy the structure from `templates/skill-template.md` and fill every section. While drafting, enforce the standard's load-bearing rules:

- Description: what/when in sentence 1, 3+ trigger phrases in the user's words (from Step 2, verbatim), exactly one "Do NOT use for X" boundary, third person, under 1024 chars.
- Body in imperative voice. Instructions, not documentation.
- Read-first table with specific extraction targets, plus what to do when a file is missing.
- Output template as a real file in the new skill's `templates/`.
- One worked example, fictional company.
- Anti-rationalization table for any step that will tempt skipping.
- Exit checklist of verifiable items.
- Under 350 lines; non-negotiables in the top 100; background to `references/`.

### 5. Validate

Run the full checklist in `references/authoring-standard.md`, including the mechanical requirements (kebab-case name matching the folder, frontmatter delimiters, description length). In this repo, also run `scripts/lint-skills.sh`.

### 6. Test

Run two prompts against the finished skill:

- **Trigger:** a natural request from Step 2's phrases. Output must match the shipped template.
- **Boundary:** a request from the "Do NOT use" clause. The skill should not fire, or should redirect.

When a test fails, fix the section that produced the failure (usually the description or the read-first table). Don't restart, and don't fix it by adding a paragraph of warnings; route the fix into the structure per the worked example.

## Audit mode

For "review my skill" / `/create-skill` pointed at an existing skill:

1. Read the skill folder in full.
2. Score it against the 10 rules; check the description first, since routing failures dominate.
3. Report as **Must fix** (breaks routing or output consistency), **Should fix** (quality drift), **Nice to have** (polish). For each: the finding plus replacement text, not just "improve this".

## Don't rationalize

| If you're thinking | Do this instead |
|---|---|
| "This is obviously new, skip the existence check" | It's one directory listing. Overlap found late means a rebuild or a routing conflict. |
| "The body explains it; the description can be short" | Routing happens on the description alone. The body never loads if the description misses. |
| "I'll inline the output format, a separate file is ceremony" | Shipped templates are what users diff against and customize. Inline sketches drift. |
| "The example can come later" | Examples calibrate depth and tone. Without one, every run reinvents both. Later never comes. |
| "One more section in the template won't hurt" | Templates rot by accretion. Every section must earn its place or be marked optional. |
| "It drafted clean, skip the boundary test" | Under- and over-triggering are invisible until tested. The boundary prompt takes one minute. |

## Exit checklist

Before handing the skill over, verify:

- [ ] Existence check ran; no installed skill covers this job
- [ ] Description: what/when in sentence 1, 3+ verbatim trigger phrases, one Do-NOT boundary, third person, 100 to 1024 chars
- [ ] Folder is kebab-case and matches `name:`; file is exactly `SKILL.md`
- [ ] Read-first table names real paths with specific extraction targets and a missing-file behavior
- [ ] Output template exists as a file in the new skill's `templates/`
- [ ] Worked example present, fictional company only
- [ ] Exit checklist and handoff sections present; SKILL.md is 350 lines or fewer
- [ ] Both test prompts ran: trigger matched the template, boundary didn't fire

## Handoff

- **Before this:** `/context-search` to check whether prior work already covers the job you're about to encode.
- **After this:** run the new skill on a real task within a day; route the first failure back into its skill file while the context is fresh.
