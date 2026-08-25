# Companion tools

Nothing in this doc is vendored or required. Every skill in the toolkit runs on workspace files alone; companions are accelerants that swap pasted context for live data, or fill panel seats you'd otherwise write yourself. Install what matches your stack and skip the rest.

## Claude plugins

All of these are in the [Claude plugin directory](https://claude.com/plugins) (`/plugin` in Claude Code).

| Plugin | What it unlocks here |
|---|---|
| **GitHub** | `delivery-review` against real PRs, issues, and commit history instead of pasted summaries |
| **Firecrawl** | `guerrilla-marketing-agent` market sweeps and competitor page scrapes; research inputs for `creative-agency` |
| **Playwright** | Browser capture for prototype review loops; walking a competitor's UX to brief a `creative-agency` panel |
| **Frontend Design** | Raises the output bar for `html-render` pages and `bolt-dev` frontends |
| **Context7** | Version-accurate library docs during `api-review` and `bolt-dev` sessions |
| **Superpowers** | A process layer (brainstorming, TDD, systematic debugging) under any build work these skills feed into |
| **Skill Creator** | Anthropic's skill eval/benchmark harness; complements `create-skill`'s authoring standard with measurement |

The directory is deep (language servers, security scanners, deploy targets); browse it for your stack rather than treating this table as complete.

## Agent libraries (panel-builder sourcing pools)

`panel-builder` checks installed libraries before generating any panel member:

- [K-Dense-AI/scientific-agents](https://github.com/K-Dense-AI/scientific-agents): 500+ practitioner profiles, plugin-installable. Best pool for technical specialist seats.
- [K-Dense-AI/mimeographs](https://github.com/K-Dense-AI/mimeographs): famous-expert voices for board flavor. Adapt rather than install-and-trust; depth varies.
- General engineering-subagent collections (security engineer, SRE, network engineer, compliance auditor and kin) fill specialist-consult seats well; several circulate on GitHub as `.claude/agents/` drops.

When no library covers a seat, `create-agent` builds the missing specialist to a standard (least-privilege tools, output contract with a failure shape, panel-seat section) that works standalone and as a panel member.

## MCP servers

| Server | Feeds |
|---|---|
| GitHub, Jira, or Linear | `delivery-review` (committed scope vs actual delivery, straight from the tracker) |
| Tavily or another web-search MCP | `guerrilla-marketing-agent`, `creative-agency` competitive context |
| Postman | `api-review` follow-through: turn findings into a tested collection |
| A local Ollama endpoint | `delegate-to-ollama` (that skill is the client; the endpoint is yours) |
| Your product's own API as an MCP server | The [platform-diagnostic pattern](platform-diagnostic-pattern.md); the highest-leverage integration on this list |

The routing rule worth copying into your workspace: prefer the MCP when connected, fall back to context files when not, and never let a skill hard-fail because a server is down.

## Related, already in the README

- [PleasePrompto/notebooklm-skill](https://github.com/PleasePrompto/notebooklm-skill) for source-grounded Q&A over document sets.
- The `panel-builder` positioning notes on why the composition layer, not the agent count, is the thing worth shipping.
