# pm-agent-toolkit

Claude Code skills for the technical PM: the workflows generic PM packs don't cover.

## The problem

Every PM skill collection covers the same ground: PRDs, meeting notes, daily plans. None of them cover the work that actually distinguishes a technical PM at a B2B or infrastructure company: reviewing an OpenAPI spec against requirements, answering a customer's CVE inquiry with a defensible posture statement, writing the business case that gets a phase gate approved, auditing engineering delivery against committed scope, or pressure-testing marketing copy against a simulated buyer panel before it ships.

I built these skills for my own job running a network infrastructure product line. They run my actual weeks. This repo is the generalized version.

## What's inside

*Skills land in waves; this table tracks what's live.*

| Skill | What it does | Status |
|---|---|---|
| `create-skill` | Scaffolds new skills to this repo's authoring standard | **Live** |
| `context-search` | Searches your prior work before you duplicate it | **Live** |
| `api-review` | OpenAPI spec review: structure, security, requirements coverage | **Live** |
| `bolt-dev` | Bolt.new frontend against a real API, graduating to production code | **Live** |
| `hiring-manager` | Full-cycle hiring: JDs, screens, interview kits, decisions | **Live** |
| `delegate-to-ollama` | Route drafting work to a local LLM | **Live** |
| `creative-agency` | Simulated buyer focus group for marketing drafts | Planned |
| `sales-analyst` | Multi-year sales data analysis with portfolio recommendations | Planned |
| `security-inquiry-response` | Formal risk posture statements for CVE/scanner inquiries | Planned |
| `delivery-review` | AI product owner: engineering delivery vs committed scope | Planned |
| `business-case-gate` | Phase-gate business feasibility documents | Planned |
| more... | | |

Plus the system layer most skill collections skip:

- **hooks/**: skill-usage logging, session-start context injection, post-compaction recovery
- **rules/**: writing style enforcement, path-scoped rules, a data-sensitivity workflow
- **docs/**: workspace setup, skill authoring standard, the self-learning loop

## Quickstart

Three ways to install (pick one):

1. **Plugin (Claude Code):** `/plugin marketplace add ryanhoggpm/pm-agent-toolkit`, then install the plugin.
2. **Manual copy:** copy any `skills/<name>/` folder into your project's `.claude/skills/`.
3. **claude.ai:** ZIP a skill folder, Settings → Capabilities → Skills → Upload.

Then set up your workspace folders per [docs/workspace-setup.md](docs/workspace-setup.md).

## Tradeoffs and decisions

- **Depth over coverage.** Fewer skills, each with routing-engineered descriptions, read-first tables, output templates, worked examples, and exit checklists. A 12-skill toolkit that routes correctly beats a 50-skill dump that doesn't.
- **Companion files over monoliths.** Anything you'd customize (personas, brand tokens, source paths, gate criteria) lives in `templates/` or `references/` next to the SKILL.md, never hardcoded in the workflow.
- **The system layer ships too.** Hooks and rules are half the leverage of a skill workspace and almost nobody publishes theirs.

## What I learned

(Filled in as waves ship.)

## Credits

The workspace conventions here (context-first skills, slash-command workflows) were shaped by running [Aakash Gupta's PM OS](https://www.news.aakashg.com/p/pm-os) daily since March 2026. None of his paid content is included in this repo; everything here is my own work, built for the technical-PM problems his system doesn't cover. If you want the generic PM lifecycle covered well, buy his.

## License

MIT. Use it, fork it, ship it.

---

Ryan Hogg · [GitHub](https://github.com/ryanhoggpm) · [LinkedIn](https://www.linkedin.com/in/ryan-hogg-product-manager/)
