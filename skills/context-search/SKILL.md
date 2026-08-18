---
name: context-search
description: Search prior work across the workspace's outputs/, context/, and memory folders before starting any task that might duplicate it, returning up to 15 ranked results with file paths, modified dates, and matching snippets. Use when the user says "have we already written about X", "find prior work on", "what did we decide about", "/cs", or before drafting a document that may already exist. Do NOT use for web research or code search; this searches the local markdown knowledge base only.
aliases:
  - cs
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Context Search

Make prior work findable in seconds. A working PM workspace accumulates 100+ files within months; the most common waste of a session is regenerating something that already exists. Done means: ranked hits with paths and snippets, and an offer to pull the most relevant file.

Search only; never modify anything. Results print to the conversation, formatted per `templates/results-format.md`.

## Read first

| Source | Path | What to extract |
|---|---|---|
| Workspace conventions | project `CLAUDE.md` | Any path mapping that overrides the defaults below |
| Search targets | the priority table in step 2 | Which directories exist in this workspace; skip missing ones silently |

## Usage

```
/context-search <terms>            multi-term AND search
/cs <terms>                        alias
/cs "exact phrase"                 phrase match
/cs --strategy | --prds | --analyses <terms>    scope to one type
/cs --recent <terms>               only files modified in the last 30 days
```

## Workflow

### 1. Parse the query

Terms, scope flag, phrase vs keyword.

### 2. Search by directory priority

| Priority | Directory | What to extract |
|---|---|---|
| 1 | `outputs/analyses/` | Analyses, briefs, forecasts |
| 2 | `context/strategy/` | Strategy, roadmaps, OKRs, positioning |
| 3 | `context/prds/` + `outputs/prds/` | PRDs, specs, feature briefs |
| 4 | `context/research/` + `outputs/research-synthesis/` | Competitive intel, user research |
| 5 | `context/decisions/` + `outputs/decisions/` | Decision logs |
| 6 | `context/meetings/` + `outputs/meeting-notes/` | Meeting notes, action items |
| 7 | `context/launches/` + `outputs/launches/` | Launch plans, GTM material |
| 8 | `context/metrics/` | Metrics and analytics reports |
| 9 | agent memory directory (if present) | Durable facts and prior-session state |

Grep case-insensitively across the existing directories; apply `--recent` via file modification time.

### 3. Rank and cap

Recency first, query-in-filename second, directory priority third. Top 15.

### 4. Print results

Per `templates/results-format.md`: `[TYPE] path (modified date)` plus the matching line in context.

### 5. Offer the next step

- 0 hits: say so, suggest broader terms.
- 1-5 hits: offer to read the most relevant file in full.
- 6-15 hits: offer to narrow by type or date.
- Hits clearly related to the task in flight: offer to pull key points before continuing.

## Worked example (fictional)

A PM at Coppermine Systems about to draft a pricing one-pager runs `/cs console pricing`:

```
ANALYSIS  outputs/analyses/fleet-api-pricing-brief.md  (2026-06-02)
  → recommend removing legacy-tier pricing from the public selector...

DECISION  context/decisions/2026-05-20-console-packaging.md  (2026-05-20)
  → per-device pricing stays; per-seat rejected because fleet admins share logins...
```

Two minutes of search shows the packaging decision already exists; the one-pager cites it instead of re-deciding it.

## Don't rationalize

| If you're thinking | Do this instead |
|---|---|
| "The query is specific, I'll just search one folder" | Priorities 1-9 take one grep pass. Cross-type hits (a decision behind an analysis) are the whole value. |
| "Zero hits, so the work doesn't exist" | Retry once with broader or alternative terms before declaring it new; naming drifts across months. |
| "I'll dump all 40 matches" | Cap at 15 and offer to narrow. A wall of hits gets skimmed, which defeats the search. |

## Exit checklist

Before finishing, verify:

- [ ] All existing priority directories were searched, not just the obvious one
- [ ] Results follow `templates/results-format.md` with real modified dates
- [ ] Capped at 15, ranked recency-first
- [ ] A next step was offered (read the top hit, narrow, or broaden)

## Handoff

- **Before this:** nothing; this is the skill that runs first.
- **After this:** whatever task triggered the search, now grounded in the prior work it surfaced. Pairs with `/create-skill` (its existence check is this same discipline applied to skills).
