# Bolt Project Knowledge template

Generate this from the backend profile and paste it into Bolt: gear icon → All project settings → Knowledge. It's Bolt's persistent system prompt; without it you re-explain the project every session.

```
## Project: [name from profile]

**Purpose:** [What this frontend does and why it's being built]
GitHub: [repo URL] | Branch: bolt-dev

## Tech Stack (non-negotiable)
- Framework: React 18 + TypeScript (strict mode)
- Build: Vite (default Bolt stack)
- Styling: Tailwind CSS + shadcn/ui components
- HTTP: Axios with interceptors for auth headers
- Server state: TanStack Query (React Query v5)
- UI state: Zustand
- Real-time: [from profile: MQTT.js / WebSocket / SSE / none]

## API Access
All API calls use the `/api/...` prefix (Vite proxy rewrites to [API base URL]).
Auth: [header names and token pattern from profile]
Store tokens in React context, never in localStorage.
[API version quirks from profile.]

## Design System
[Design direction from profile. If you have brand tokens, paste the CSS custom
properties here with usage notes: which color is primary action, which is CTA,
which fonts for headings vs body.]

## Component Rules
- One feature per component file. Max ~200 lines; extract helpers when larger.
- Shared UI: `src/components/ui/` (shadcn wrappers)
- Feature components: `src/features/[feature-name]/`
- Types: `src/types/`
- No mock or hardcoded data in components; use TanStack Query loading states.

## Development Rules
- Read PROGRESS.md at the start of every session.
- Use Plan mode before implementing any new feature.
- Build one component at a time; test in preview before moving on.
- Say "checkpoint" before major refactors to save version history.

## Domain Glossary
[5-8 terms from the profile, one line each]

## Do Not
- Use localStorage for tokens or credentials
- Import heavy libraries without asking first
- Write data fetching outside TanStack Query
- Create new Tailwind color tokens (use the existing palette)
```
