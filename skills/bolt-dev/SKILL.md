---
name: bolt-dev
description: Set up and run multi-session frontend development in Bolt.new against a real backend API, producing a Bolt Project Knowledge document, a PROGRESS.md session tracker, a Vite proxy config for CORS-free live API calls, and a Bolt-to-local-review production handoff. Use when the user says "build this in bolt", "set up a bolt project", "bolt-dev", or wants a connected frontend in a real GitHub repo that graduates to production code. Do NOT use for one-off demos or concept mockups with mock data; write a single throwaway prototype prompt for those instead.
---

# Bolt Dev

Build real frontends in Bolt.new: connected to a live backend, versioned in GitHub, headed for production. Done means: the project is set up once (Project Knowledge, proxy, tracker) and every later session starts from restored context instead of re-explanation.

Hard rules, before anything else:

1. **Bolt works on a `bolt-dev` branch, never `main`.** Bolt auto-commits every accepted change; diffs get reviewed in GitHub before merging.
2. **Tokens live in memory (React context), never localStorage.** This goes in the Project Knowledge's Do Not list and is non-negotiable.

## Read first

| Source | Path | What to extract |
|---|---|---|
| Backend profile | `references/backend-profile.md` (user-filled) | Repo, API base URL, auth pattern, real-time transport, glossary, quirks |
| Requirements | `context/prds/` | What the current phase must build |
| Prior API review | `outputs/analyses/` (from `/api-review`) | Endpoint realities and gotchas that belong in "Known API quirks" |
| Design assets | wherever the profile points | Brand tokens and visual direction for the Design System section |

If the backend profile isn't filled in, collect its fields conversationally (repo, API URL, auth, real-time, glossary) and offer to save them into the profile before generating anything.

## One-time project setup

### 1. Connect GitHub

In Bolt.new: GitHub icon → connect the target repo → create and select the `bolt-dev` branch.

### 2. Configure the Vite proxy

Bolt's WebContainer is browser-based, so a local proxy script can't run there. Vite's dev-server proxy forwards API calls server-side instead, bypassing CORS. In `vite.config.ts`:

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: '[API base URL from the backend profile]',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})
```

Components call `/api/...`; the proxy rewrites to the real host. Some backends also require an `Origin` header on proxied requests; add a `headers` block if auth fails from the preview. For production deployment, replicate the rewrite as a hosting-platform rule (Vercel/Netlify redirect or edge function).

### 3. Generate Project Knowledge

Fill `templates/project-knowledge.md` from the backend profile and have the user paste it into Bolt (gear icon → All project settings → Knowledge). This is the highest-leverage step: it's Bolt's persistent system prompt, and without it every session starts from zero.

### 4. Create PROGRESS.md

Add `templates/progress-tracker.md`'s structure to the repo root. It's the cross-session memory.

### 5. Write the first session prompt

A single opening prompt: read PROGRESS.md, state the stack and API access in two lines, name one session goal, and require a plan (folder structure, auth design, first component) for approval before any code.

## Per-session workflow

1. **Restore:** "Read PROGRESS.md and summarize where we left off." Correct anything wrong before proceeding.
2. **Plan in Discussion mode:** state the single feature goal; ask for components, data flow, and endpoints involved. No code yet.
3. **Approve, then build one component at a time.** Test each in the preview before the next.
4. **Checkpoint before risk:** before any refactor, save a version-history checkpoint (free rollback, no tokens).
5. **Close:** "Update PROGRESS.md: what we completed, decisions made, open issues." Verify the auto-commit landed on `bolt-dev`.

## Token efficiency

- Buttons (publish, version history) are free; prompting Bolt to do the same things costs tokens.
- Discussion mode for questions and debugging; Build mode only when ready to write code.
- Turn unused connectors off; each adds paid context.
- Use the heavier agent tier only for new architecture or gnarly debugging; standard tier for planned features and styling.

## Debugging playbook

After 2 failed "attempt fix" clicks, stop clicking:

1. Switch to Discussion mode.
2. "Don't write code yet. Explain what's causing [error] and propose 2-3 fixes."
3. Pick one, switch to Build mode, implement it.

For API errors: check the preview's network tab first. Requests hitting the right host means the proxy works and the problem is auth or payload; requests hitting the WebContainer origin means `vite.config.ts` needs fixing.

## Worked example (fictional)

First-session prompt for Coppermine Systems' console frontend, generated from the example profile in `references/backend-profile.md`:

```
Read PROGRESS.md first and tell me what's been done.

Project: Coppermine Console (github.com/coppermine-io/console-frontend, branch bolt-dev)
Stack: React 18, TypeScript strict, Vite, Tailwind, shadcn/ui, TanStack Query, Zustand
API: /api prefix routes through the Vite proxy to api.coppermine.example
Auth: X-Session-Token and X-CSRF-Token headers on every request, tokens in React context

Today's goal: scaffold the project and build the login screen.

Before writing any code, enter Plan mode and propose:
1. Folder structure (src/features, src/components/ui, src/lib, src/types, src/hooks)
2. Auth context design: in-memory token storage, Axios interceptor setup
3. Login form component: fields, submit flow, error states
4. TanStack Query setup for the auth mutation

I'll review and approve before you build anything.
```

## Handoff: Bolt → local review → production

Bolt for velocity, local tooling for quality:

1. Feature works in Bolt, committed to `bolt-dev`.
2. Open a PR `bolt-dev` → `main`; pull the branch locally.
3. In Claude Code: simplify and consolidate, then run a code review before merging.
4. Merge to `main`.

## Don't rationalize

| If you're thinking | Do this instead |
|---|---|
| "Skip Project Knowledge, I'll explain in the first prompt" | Prompts die with the session. Project Knowledge persists; it's 10 minutes once vs. re-explaining forever. |
| "Bolt can work on main, I'll be careful" | Bolt auto-commits every accepted change. One bad accept on main is a force-push conversation. |
| "localStorage for the token is fine for dev" | Dev code graduates. The rule exists because "temporary" auth shortcuts ship. |
| "One more auto-fix click will get it" | After 2 failures the error class is wrong. Discussion mode diagnosis is cheaper than a fix loop. |
| "I'll update PROGRESS.md next session" | Next session starts by reading it. Unwritten progress means restored context is wrong from minute one. |

## Exit checklist

Before finishing a setup run, verify:

- [ ] Backend profile filled (or its fields collected and offered for saving)
- [ ] Project Knowledge generated from `templates/project-knowledge.md` with no unfilled brackets
- [ ] Vite proxy targets the profile's API base URL; components use the `/api` prefix
- [ ] PROGRESS.md created in the repo root from `templates/progress-tracker.md`
- [ ] First-session prompt names one goal and requires a plan before code
- [ ] `bolt-dev` branch confirmed as Bolt's working branch

## Handoff

- **Before this:** `/api-review` on the backend's spec; its findings populate the profile's "Known API quirks" row and prevent building against endpoints that don't behave as documented.
- **After this:** per-session workflow above, session by session; local review pass before each merge to `main`.
