# PROGRESS.md template

Create this at the root of the connected repo during setup. It's the session-to-session memory: Bolt reads it at session start, updates it at session end.

```markdown
# [Project Name]: Bolt Development Progress

## Status: STARTING
Last session: [DATE]

## Completed
- [ ] Vite + React + TypeScript + Tailwind + shadcn/ui scaffold
- [ ] Vite proxy config (API target from backend profile)
- [ ] Auth context + Axios interceptors
- [ ] Login / session management

## In Progress
- [ ] [Current feature]

## Queued
- [ ] [Next features in priority order]

## Architecture Decisions
| Decision | Choice | Rationale |
|---|---|---|
| State | TanStack Query + Zustand | Server/UI state separation |
| Components | shadcn/ui | Unstyled, Tailwind-native, composable |

## Known Issues
None.

## Session Notes
[Dated notes added at the end of each session]
```
