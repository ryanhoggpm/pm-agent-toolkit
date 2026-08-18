---
name: tech-writer
description: Draft, review, or rewrite technical documentation (release notes, user guides, quick-starts, upgrade guides, demo scripts, troubleshooting docs) so a real user can complete a real task without calling Support, enforcing workflow-focused structure over feature description. Use when the user says "write release notes", "draft a user guide", "review this doc", "rewrite this quick-start", or "tech-writer". Do NOT use for marketing copy or positioning content; run /creative-agency on those instead.
aliases:
  - tw
---

# Tech Writer

Create and improve documentation that helps real users accomplish real tasks. The problem this skill exists to fix: engineering-written docs describe what the product does, bury critical-path warnings in prose, use undefined jargon, and assume the reader already knows the product. Users can't self-serve, so they call Support. Done means: a document in the right structure from `templates/doc-structures.md` where every step has an expected outcome and nothing critical is buried.

**The core doctrine, applied to every sentence: answer "what does the reader need to DO," never "what does the product do."**

| Wrong (function-focused) | Right (workflow-focused) |
|---|---|
| "The device supports dual boot banks." | "Your device stores two firmware versions. The update installs to the inactive bank, so you can roll back if something goes wrong." |
| "Firmware must be updated to 8.4 and then 9.0 before updating further." | "**Before you upgrade:** if your firmware is older than 8.4, you must upgrade in two steps. Skip this and the upgrade will fail. [See Step Upgrade Path.]" |
| "IPv6 Support in Performance Monitoring" | "You can now use IPv6 addresses in ping, DNS lookup, and HTTP probes." |
| "The minimum provisioning-manager version is 7.2.4." | "If you use the provisioning manager, upgrade it to 7.2.4 or later before applying this firmware." |

## Read first

| Source | Path | What to extract |
|---|---|---|
| Audience profiles | `references/audience-profiles.md` (user-filled) | Who each audience is, doc source paths, terminology decisions |
| Doc structures | `templates/doc-structures.md` | The structure for the requested document type |
| Existing docs | doc-sources paths from the profiles file | Material to improve, and terminology to stay consistent with |
| Product truth | `context/products/`, `context/prds/` | What the product actually does; intended behavior for pre-release docs |
| Reviewer checklist | `references/reviewer-agent.md` | The severity-ranked failure modes for review mode |

Profiles file unfilled: ask audience and product scope conversationally, offer to save the answers into it.

## Workflow

### 1. Orient before writing

Confirm (skipping anything already provided or inferable from a pasted doc): document type (release-notes / user-guide / quick-start / upgrade-guide / demo-script / troubleshooting / partner-brief), primary audience (a key from the profiles file), mode (draft / review / rewrite), and product scope.

### 2. Draft or rewrite

Use the matching structure from `templates/doc-structures.md`, verbatim in shape. While writing, enforce:

- Prerequisites and warnings BEFORE the steps they protect, never after
- An expected result after every step that produces a visible change
- Every conditional note names who it applies to ("If you use X...")
- Every term from the profiles file's jargon list defined on first use
- Every "contact support" carries the actual contact method; every referenced file carries a link or location
- No dead ends: everything that can go wrong ends with what to do about it
- One name per thing, from the profiles file's terminology decisions

### 3. Review mode

Apply the checklist in `references/reviewer-agent.md` from the perspective of a first-time user. Report as `[CRITICAL/MAJOR/MINOR] | location | what's wrong (quote it) | suggested fix`, grouped by severity, with a one-paragraph overall assessment first and a one-sentence bottom line (rewrite vs targeted fixes) last. Review reports the gaps; it doesn't rewrite unless asked.

### 4. Save

`outputs/docs/<type>-<product>-<date>.md`.

## Writing rules (always apply)

Plain language for someone smart but new to the product; technical vocabulary only when necessary and always defined. Active voice ("Click Save"). Numbers for sequential steps, bullets for unordered lists. Screenshots sparingly; words stay accurate longer. Version-specific always ("in 9.2", never "the current version"). Verb-phrase titles.

## Worked example (fictional)

Coppermine Systems, release notes for CM-900 firmware 9.2. The engineering draft opens with a release summary and buries this mid-paragraph: "note that units running firmware prior to 8.4 require an intermediate update." The skill's version opens with:

> ## Before You Upgrade: Read This First
>
> **Step upgrade required if you are on firmware older than 8.4:**
> 1. Upgrade to 8.4.1 first: [download link]
> 2. Then upgrade to 9.2: [download link]
>
> Skip this and the upgrade will fail.
>
> **If you use Fleet Cloud:** update the agent to 3.1 or later before this firmware, or devices will report offline after reboot.

Same information. The difference is that a scanning reader physically cannot miss it.

## Don't rationalize

| If you're thinking | Do this instead |
|---|---|
| "The warning is in there, readers should read carefully" | Findable beats present. The canonical support-call failure had every fact technically in the document. Surface it before the steps. |
| "This term is standard in the industry" | The jargon list in the profiles file is the authority. When in doubt, define on first use; experts skip definitions painlessly, novices can't conjure them. |
| "The steps are obvious, expected results are padding" | Expected results are how a user knows to stop before compounding an error. Every visible-change step gets one. |
| "Review mode: I'll just fix the doc while I'm in there" | Review reports, draft/rewrite changes. Mixing them produces a rewrite nobody can diff against the findings. |
| "The demo script should list more features" | Demos make the prospect feel their problem being solved. A feature tour is the anti-pattern the structure exists to prevent. |

## Exit checklist

Before presenting the document, verify:

- [ ] Structure matches the type's template in `templates/doc-structures.md`
- [ ] All prerequisites and warnings appear before the steps they protect
- [ ] Every visible-change step has an expected result; the doc ends with a verify section where the type calls for one
- [ ] Every jargon term from the profiles file is defined on first use; terminology is one-name-per-thing
- [ ] Every conditional names its audience; every support pointer has a contact method; every referenced file has a location
- [ ] No dead ends: each failure path says what to do next
- [ ] Version numbers explicit; no "current version"
- [ ] Review mode: findings quoted, severity-grouped, with the rewrite-vs-fixes bottom line

## Handoff

- **Before this:** `/context-search` for existing docs on the same topic; `/api-review` findings feed API-adjacent docs with real endpoint gotchas.
- **After this:** `/html-render` for a branded shareable version; `/creative-agency` if any of it becomes public marketing (the claims register applies there, not here).
