# Delivery review report template

Save as `outputs/delivery-review/<YYYY-MM-DD>-delivery-review.md`. After writing, print a 3-bullet executive summary to the conversation so the user sees it without opening the file.

```markdown
# Delivery Review, [DATE]
**Period:** [start] to [end]
**Repos:** [repo (branches) list from the sources file]
**Current cycle:** [cycle name from the scope of record], [status if the page states one]

## Executive Summary
[2-3 sentences: what shipped, biggest movement, most concerning gap or divergence.]

## [Track 1, e.g. Firmware] Changes
### Commits this period: [N]
| SHA | Repo/Branch | Author | Date | Message | Requirement ID |
|---|---|---|---|---|---|

### Implementation Analysis
**[Requirement ID], [Name]:** [what changed, how it implements the requirement,
any deviation from the documented intent]

### No-activity items (committed and active-discovery tiers only)
[Committed requirements with zero commits and zero tickets this period.]

## [Track 2, e.g. Frontend] Changes
[Same structure. State the blind spots from the sources file explicitly here,
e.g. "backend not visible in any readable repo; tracker project X is the only signal".]

## Gap Analysis vs Current Scope
| Requirement ID | Tier | Delivery status (registry) | This period | Risk | Notes |
|---|---|---|---|---|---|

## Divergence Flags
[Both directions: real effort landing on deferred items with no documented
pull-forward reason, and committed items with zero activity.]

## Tracker-Page Updates to Paste In
[One drafted table per requirement page with new ticket data this run, with the
page link. Carry forward unverified existing rows with their last-synced dates;
the user pastes these in manually.]

## Issues Log Changes
[Rows appended this run; rows marked Resolved.]

## Where the PM Should Interject
[Specific named actions: requirement IDs, file names, ticket numbers.]

## Tasks Well-Suited for Claude
[Concrete offers: name the file, endpoint, or artifact.]
```
