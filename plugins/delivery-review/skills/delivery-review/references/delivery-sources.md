# Delivery sources (fill this in once, keep it current)

`/delivery-review` runs entirely off this file: where the committed scope lives, which repos and tracker projects carry the evidence, and what it can't see. An unfilled row degrades the matching section; a wrong row produces confident nonsense. Date the file when you change it.

## Scope of record (read live every run, never cached)

| Document | Where it lives | What it provides |
|---|---|---|
| Requirement registry | [Confluence/Notion page, or repo doc path] | The master requirement/feature ID list and delivery status. The ID vocabulary for every run. |
| Current release scope | [page or doc; note how to find the newest cycle's version] | What's committed for the active cycle |
| Priority/sequencing plan | [page or doc] | Which uncommitted items are in active discovery vs deferred |

## Repos

| Repo | Branches to track | Attribution rule |
|---|---|---|
| [path or URL] | [branches] | [how to tell which product/track a commit belongs to: ticket key in message, branch prefix, path] |

**Hot paths:** [directories whose changes matter most, for the read-the-diff step]

**Fetch policy:** [If fetching needs a VPN or interactive login, say so here. The skill will check freshness, prompt you with the exact fetch commands, and wait; it never fetches on your behalf.]

## Tracker

| Project keys | Recent-activity query | Stalled-work query |
|---|---|---|
| [keys] | [e.g. updated >= -7d, no subtasks] | [e.g. In Progress/Blocked and untouched 5+ days] |

**Requirement mapping:** [Is there a field/epic linking tickets to requirement IDs? If not, state that mapping is by judgment against the registry, and unmappable tickets get flagged "Unmapped", never force-fit.]

## Known blind spots

[Repos, teams, or backends whose work you cannot see. The report discloses these every run instead of silently under-covering them.]

## Issues log

Path: `outputs/delivery-review/issues-log.md`. Read at start, append at end; mark rows Resolved with a one-line note, never delete.

## Example (fictional): Coppermine Systems

- Registry: Confluence "Fleet Program Requirement Registry" (IDs `F-`/`C-` prefixed); release scope under the "Program Overview" folder, newest-modified page wins
- Repos: `fleet-firmware` (branches `main`, `cm9k`; attribution by `FW-`/`CM9K-` ticket keys), `console-frontend` (`develop`)
- Blind spot: the cloud backend lives in a partner org's repos; tracker project `FC` is the only signal for it
- Fetch policy: VPN-gated; prompt and wait
