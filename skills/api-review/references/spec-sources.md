# Spec sources (fill this in once)

`/api-review` reads this file to find your specs and requirements without asking every run. Replace the example rows; delete any row you don't have. Missing rows degrade gracefully: the review still runs, it just skips the matching section.

| Source | Path or location | Notes |
|---|---|---|
| OpenAPI specs | `context/reference/api/` | Where your spec files live; name the primary spec if there are several |
| Requirements / PRDs | `context/prds/` | The docs that define what the API must cover; an index file if you keep one |
| Personas | `context/research/personas.md` | User types for the worked-example section of the report |
| Prior reviews | `outputs/analyses/` | Earlier evaluations of the same spec, so findings aren't re-reported as new |
| Project tracker | (MCP name + project) | e.g. "Jira, project APX"; used for schedule implications, skipped if unreachable |

## Example (fictional)

At Coppermine Systems, this file reads:

| Source | Path or location | Notes |
|---|---|---|
| OpenAPI specs | `context/reference/api/coppermine-cloud-v2.yaml` | v2 is the live review target; v1 is frozen |
| Requirements / PRDs | `context/prds/prd-index.md` | Functional areas numbered FA-1..FA-9 |
| Personas | `context/research/personas.md` | 5 personas; "field technician" and "NOC operator" matter most for API examples |
| Prior reviews | `outputs/analyses/` | One prior review dated 2026-05-02 |
| Project tracker | Jira, project CMC | Sprint milestones carry GA dates |
