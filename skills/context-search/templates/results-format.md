# Search results format

Results print to the conversation (no file is written). Format each hit as:

```
[TYPE] path/to/file.md  (modified: YYYY-MM-DD)
  → matching line or 1-2 lines of surrounding context
```

TYPE is one of: `ANALYSIS`, `STRATEGY`, `PRD`, `RESEARCH`, `DECISION`, `MEETING`, `LAUNCH`, `METRICS`, `MEMORY`.

Example (fictional workspace):

```
ANALYSIS  outputs/analyses/fleet-api-pricing-brief.md  (2026-06-02)
  → recommend removing legacy-tier pricing from the public selector...

STRATEGY  context/strategy/coppermine-console-positioning.md  (2026-05-28)
  → the legacy console is maintained but not the forward investment path...

PRD  context/prds/prd-index.md  (2026-05-15)
  → FA-3: legacy API bridge (deferred; see deferred-work-tracker.md)
```

Cap at 15 results, ranked by: recency first, query-in-filename second, directory priority third.
