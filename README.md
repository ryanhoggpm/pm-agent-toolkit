# pm-agent-toolkit

Claude Code skills for the technical PM: the workflows generic PM packs don't cover.

## The problem

Every PM skill collection covers the same ground: PRDs, meeting notes, daily plans. None of them cover the work that actually distinguishes a technical PM at a B2B or infrastructure company: reviewing an OpenAPI spec against requirements, answering a customer's CVE inquiry with a defensible posture statement, writing the business case that gets a phase gate approved, auditing engineering delivery against committed scope, or pressure-testing marketing copy against a simulated buyer panel before it ships.

I built these skills for my own job running a network infrastructure product line. They run my actual weeks. This repo is the generalized version.

## What's inside

*14 skills, all live. More land as they're generalized from daily use.*

| Skill | What it does |
|---|---|
| `api-review` | OpenAPI spec review: structure, security, requirements coverage |
| `bolt-dev` | Bolt.new frontend against a real API, graduating to production code |
| `context-search` | Searches your prior work before you duplicate it |
| `create-agent` | Design working agents (Claude Code subagents or Managed Agents) that double as panel members |
| `create-skill` | Scaffolds new skills to this repo's authoring standard |
| `creative-agency` | Simulated buyer focus group for marketing drafts |
| `delegate-to-ollama` | Route drafting work to a local LLM |
| `delivery-review` | AI product owner: engineering delivery vs committed scope |
| `guerrilla-marketing-agent` | Weekly market sweep + content drafting on zero budget |
| `hiring-manager` | Full-cycle hiring: JDs, screens, interview kits, decisions |
| `html-render` | Renders finished content as self-contained branded HTML |
| `panel-builder` | Composable expert panels: charter a team once, run it forever |
| `sales-analyst` | Multi-year sales data analysis with portfolio recommendations |
| `tech-writer` | Workflow-focused technical docs: release notes, guides, demo scripts |

Plus the system layer most skill collections skip:

- **hooks/**: skill-usage logging, session-start context injection, post-compaction recovery
- **rules/**: writing style enforcement, path-scoped rules, a data-sensitivity workflow
- **docs/**: workspace setup, skill authoring standard, the self-learning loop, and the [platform-diagnostic pattern](docs/platform-diagnostic-pattern.md), a design for read-only state-of-the-platform skills you build against your own stack

These skills get sharper with the right plugins, MCP servers, and agent libraries alongside them; [docs/companions.md](docs/companions.md) maps which companion unlocks what, skill by skill.

**On `panel-builder`:** GitHub has no shortage of repos shipping 80, 163, or 500 agents. What none of them ship is the composition layer: a way to assemble a few of those agents, plus personas no library can define for you (your users, your advisors), around one question with defined success criteria. `panel-builder` is that layer. It charters a panel through a guided intake, sources members from whatever agent libraries you've installed before generating anything, and runs sessions in one of five interaction modes, from parallel specialist consults to a chaired board of directors that's required to argue with you. Panels it builds pair well with member libraries like [K-Dense-AI/scientific-agents](https://github.com/K-Dense-AI/scientific-agents) (500+ practitioner profiles, plugin-installable) and [K-Dense-AI/mimeographs](https://github.com/K-Dense-AI/mimeographs) (famous-expert voices; adapt rather than install-and-trust). Neither is vendored here; they're sourcing pools, not dependencies. And when no library covers a seat, `create-agent` builds the missing specialist to a standard (least-privilege tools, output contract with a failure shape, self-verification) that makes it useful standalone and as a panel member, one definition for both.

**Pairs well with:** [PleasePrompto/notebooklm-skill](https://github.com/PleasePrompto/notebooklm-skill) (third-party, MIT) for source-grounded Q&A over document sets you've loaded into NotebookLM. Install it from upstream; it's not vendored here because it isn't my work and it manages its own local auth state.

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
