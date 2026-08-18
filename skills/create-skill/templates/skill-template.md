# Skill scaffold

Copy this structure for every new skill. Replace every bracketed placeholder; delete any optional section that genuinely doesn't apply, don't leave it empty. The rules behind each section are in [references/authoring-standard.md](../references/authoring-standard.md).

Folder layout:

```
skills/<skill-name>/
├── SKILL.md              # the workflow, <=350 lines
├── templates/
│   └── output-template.md    # exact output structure
└── references/           # optional: background too long for SKILL.md
```

## SKILL.md scaffold

```markdown
---
name: [skill-name-kebab-case]
description: [What it does and what "done" looks like, one sentence]. Use when the user says "[trigger 1]", "[trigger 2]", "[trigger 3]", or [situation trigger]. Do NOT use for [adjacent job it will be confused with]; use /[other-skill] instead.
---

# [Skill Display Name]

[One sentence: the job, and what the user has when it's finished.]

[Any non-negotiable constraint goes here, in the top 100 lines: approval gates, scope limits, data rules.]

## Read first

| Source | Path | What to extract |
|---|---|---|
| [User's context] | `context/[folder]/` | [Specific facts to pull, not "relevant info"] |
| [Prior outputs] | `outputs/[type]/` | [Existing version to update instead of overwrite] |
| [Companion file] | `templates/[file].md` | [The user-customized config this skill runs on] |

If a listed file is missing: [ask the user / state the assumption and proceed / stop].

## Workflow

### 1. [Verb-first step name]

[Specific instruction. "Read context/strategy/ and extract the current-quarter goals," not "analyze the context."]

### 2. [Clarify]

[Questions to ask, and which to skip when already answered. If none, delete this step.]

### 3. [Generate]

[Core logic. Reference templates/output-template.md for structure. State depth and length expectations.]

### 4. [Verify]

[How to check the output against reality before presenting it.]

## Output

Follow `templates/output-template.md`. Save to `outputs/[type]/[descriptive-name]-YYYY-MM-DD.md`.

## Worked example

[Input a user would give, then the key sections of the output it should produce. Fictional companies and people only. If the example runs long, move it to references/worked-example.md and summarize here.]

## Don't rationalize

| If you're thinking | Do this instead |
|---|---|
| "[The specific excuse for skipping a step]" | [The counter, and what skipping actually costs] |

## Exit checklist

Before presenting output, verify:

- [ ] [Checkable item specific to this output type]
- [ ] [Common failure mode, stated as a check]
- [ ] Output follows templates/output-template.md; optional sections dropped, not left empty
- [ ] Every name, number, and quote traces to a source file or the user's input

## Handoff

- **Before this:** /[skill] ([what it prepares])
- **After this:** /[skill] ([the natural next step])
```

## Output template scaffold (`templates/output-template.md`)

```markdown
# [Output title pattern, e.g. "API review: <spec name>"]

[Real section names with one-line guidance per section on what belongs there.
Mark optional sections "(only if relevant)".
Where format isn't obvious, include a filled-in example line.]
```
