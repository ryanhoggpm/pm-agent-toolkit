# Recommended workflows

Skill-chain recipes for the toolkit's published skills. Copy into your project's rules and extend as more skills land.

## Before any substantial task

1. `/context-search <topic>`: has this been written already?
2. If yes, read it and build on it. If no, proceed, now knowing the neighbors.

The most expensive failure in a mature workspace is regenerating existing work.

## API lifecycle

1. `/api-review <spec>`: severity-tagged findings and requirements gaps
2. Findings become tickets; "Known API quirks" feed the frontend's backend profile
3. `/bolt-dev`: build the connected frontend against the reviewed API
4. Local review pass before each merge to main

## Hiring cycle

1. `/hiring-manager jd`, then post
2. `/hiring-manager screen <candidate>` per applicant
3. `/hiring-manager prep <candidate>` before each interview (screen findings become probes)
4. `/hiring-manager debrief` after, `/hiring-manager advance` when the panel's done
5. Document the final decision for the record

## Capacity management

- Rate-limited or drafting something that should stay local: `/delegate-to-ollama <prompt>`, then refine the draft in a full-context session.

## Workspace maintenance

- A workflow you've pasted twice: `/create-skill` to encode it
- Weekly: read `.claude/logs/skill-usage.log`; heavily edited outputs become skill fixes per `rules/system-learning.md`
