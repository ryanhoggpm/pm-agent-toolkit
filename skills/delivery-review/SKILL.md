---
name: delivery-review
description: Act as an AI product owner reviewing engineering delivery against committed scope by reading the scope of record live, harvesting recent commits and tracker tickets, mapping both to requirement IDs, flagging divergence in both directions, and drafting tracker-page updates for manual paste-in. Use when the user says "run the delivery review", "what did engineering actually ship", "dev progress review", or on a weekly cadence. Do NOT use for reviewing the quality of individual code changes; it reviews delivery against scope, not code.
aliases: [dev-review]
---

# Delivery Review

Bridge PM requirements and engineering delivery: read what engineering actually shipped or touched this period, compare it against the committed scope, and surface what the PM needs to act on. Done means: a report per `templates/output-template.md` where every commit and ticket is mapped to a requirement ID or flagged Unmapped, and divergence is named in both directions.

Three hard rules:

1. **Read the scope of record live, every run.** The registry, release scope, and priority plan evolve; never cache them locally or trust a version remembered from a prior run. A local mirror recreates exactly the staleness drift this skill exists to catch.
2. **Never fetch on the user's behalf when credentials are involved.** If the sources file says fetching needs VPN or interactive login: check freshness, and if stale, give the user the exact fetch commands, stop, and wait. Verify freshness again after they confirm. Never fall through to commit analysis on stale data.
3. **No direct writes to shared scope pages.** Tracker-page updates are drafted in the report for manual paste-in. Tools that only support full-body page replacement make direct writes risky; the human paste is the safety mechanism.

## Read first

| Source | Path | What to extract |
|---|---|---|
| Delivery sources config | `references/delivery-sources.md` (user-filled) | Scope-of-record locations, repos, attribution rules, tracker queries, blind spots |
| Scope of record | locations named in the config, fetched live | Requirement ID vocabulary, committed set, priority tiers |
| Issues log | `outputs/delivery-review/issues-log.md` | Open ambiguities and flags from prior runs |
| Prior reports | `outputs/delivery-review/` | Last period's findings, so movement reads as movement |

Config unfilled: this skill doesn't degrade gracefully; collect the scope-of-record and repo rows conversationally and save them before running. A review against guessed scope is worse than no review.

## Workflow

### 0. Freshness preflight

Check the last-commit timestamp on every tracked remote branch (`git log -1 --format=%cd origin/<branch>`). All within ~12 hours: proceed. Anything stale: apply hard rule 2.

### 1. Build the working set

From the live scope of record: **committed this cycle**, **active discovery**, and **deferred**. Read the issues log for open items.

### 2. Harvest commits

Per repo and branch from the config, for the review period (default 7 days): oneline log, stat summary, and name-only against the config's hot paths. Attribute commits to tracks using the config's attribution rule (ticket keys, branch prefixes); when nothing matches, that's an Unmapped candidate, not a guess.

### 3. Query the tracker

Run the config's recent-activity and stalled-work queries. Map each ticket to a requirement ID by the config's mapping rule; where mapping is judgment against the registry, judge, and flag anything that doesn't map cleanly as Unmapped in the report and the issues log.

### 4. Read the changed files

For each requirement with activity, read 2-3 of the most-changed files, prioritizing the hot paths. The point is HOW it's being implemented and whether that matches the documented intent, not just that something moved.

### 5. Detect divergence, both directions

- Real effort landing on deferred items with no documented pull-forward reason: the signal engineering may be drifting from the prioritized scope.
- Committed items with zero commits and zero tickets this period: the inverse problem.

Before flagging either, check the priority plan's own notes and the issues log; some pull-forwards are deliberate and named.

### 6. Draft, log, report

Draft the paste-in tracker tables (carry forward unverified rows with their last-synced dates; never drop them). Append issues-log rows; mark resolved ones. Write the report per `templates/output-template.md` and print the 3-bullet summary.

## Worked example (fictional)

Coppermine Systems, weekly run. Commit `a41f2c9 FW-1382: retry logic for cloud check-in` on `fleet-firmware/cm9k` maps to registry row `F-CONN-4` via its ticket key. The gap analysis then shows:

> | F-CONN-4 | Committed | In Progress | 4 commits, FW-1382 active | Low | Implementation matches documented retry intent |
> | F-PROV-2 | Committed | Not Started | No commits, no tickets | High | Second consecutive silent week; flagged for PM follow-up |

And one divergence flag:

> Effort on deferred item C-REP-9 (6 commits) with no pull-forward note in the priority plan. Not necessarily wrong; needs a documented reason or a scope correction.

## Don't rationalize

| If you're thinking | Do this instead |
|---|---|
| "The scope pages haven't changed since last run" | Fetch them anyway. The one run you skip is the run after the cycle rolled. |
| "The fetch will probably work without VPN" | The config's fetch policy is the authority. Prompt and wait; stale-data analysis is silently wrong analysis. |
| "This ticket is probably part of requirement X" | Probably means Unmapped. Force-fit mappings corrupt the gap table, and Unmapped is itself a useful finding (scope creep or undocumented work). |
| "Zero activity on a committed item, that's a delivery miss" | Check delivery status and decision records first. A "Now" priority legitimately sits at Not Started mid-build, and deliberate deprioritization is a decision, not a miss. |
| "I'll just update the tracker page directly, it's one table" | Full-body page replacement can clobber prose you never touched. Draft for paste-in, per hard rule 3. |

## Exit checklist

Before presenting the report, verify:

- [ ] Scope of record fetched live this run; no cached IDs or tiers used
- [ ] Freshness preflight ran; no analysis on stale repos
- [ ] Every commit and ticket mapped to a current requirement ID or flagged Unmapped; no retired ID scheme used
- [ ] Divergence checked in both directions, with the priority plan's own notes consulted before flagging
- [ ] Blind spots from the config stated in the report, not silently under-covered
- [ ] Paste-in tables carry forward unverified rows with last-synced dates
- [ ] Issues log updated: new rows appended, resolved rows marked
- [ ] Specific files, functions, and ticket numbers throughout; nothing says "some changes were made"

## Handoff

- **Before this:** the sources config filled and current; `/context-search` for prior reviews if this is a new workspace.
- **After this:** the user pastes the drafted tracker updates; divergence flags become agenda items with engineering; `/api-review` when a delivery touches the API contract.
