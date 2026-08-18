# API evaluation report template

Save as `outputs/analyses/<spec-name-kebab>-evaluation-<YYYY-MM-DD>.md`. Drop sections marked "(only if...)" when their inputs are missing; don't leave them empty.

```markdown
# [Spec Title] API Evaluation

**Spec:** `[filename]` · **OpenAPI:** [version] · **Reviewed:** [date]
**Scope:** [N] paths, [N] operations, [N] schemas

## Executive summary

- [Overall quality in one honest sentence]
- [Highest-risk item for the nearest milestone]
- [Most user-visible or embarrassing defect]
- [Requirements-coverage bottom line]

## Endpoint inventory

| Tag | Endpoints |
|---|---|
| [Tag] | [N] |

[One line on anything out of scope and why.]

## 1. Structural issues

### Critical

**[Issue title]**
What's wrong, which endpoint(s), why it matters, the specific fix.
*(repeat per issue; same format under Significant and Minor)*

### Significant

### Minor

## 2. Documentation gaps

[Missing response codes, pagination, descriptions; name each affected endpoint.]

## 3. CRUD coverage

| Resource | Create | Read one | List | Update | Delete | Gap intentional? |
|---|---|---|---|---|---|---|

## 4. Requirements gap analysis (only if requirements context exists)

| Req / Area | Current coverage | Status | Gap description |
|---|---|---|---|
| [ID or name] | [Endpoint(s) or None] | Complete / Partial / Missing | [What's absent] |

[Framing note: gaps that belong to a different API layer by design, stated as such.]

## 5. Schedule implications (only if tracker context exists)

[What ships at the nearest milestone given current state; which issues threaten it;
which fixes are spec-only vs. implementation changes. Cite real ticket IDs and dates.]

## 6. Consumer examples

### [Persona name and role]

Goal: [what they're trying to do with this API]

```python
# minimal happy path with the requests library, using real endpoints from the spec
```

**Tip:** [one gotcha specific to this API]

*(3-5 personas)*

## 7. Recommended priorities

Ordered by risk to the nearest milestone.

1. **[Fix]**: why now, where in the spec, effort class (spec-only / implementation required)
2. ...
```
