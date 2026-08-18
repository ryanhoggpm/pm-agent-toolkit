---
name: guerrilla-marketing-agent
description: Zero-budget marketing intelligence and content drafting for a product line: a weekly SERP, news, and community sweep that diffs against your baseline and surfaces 3 concrete actions, plus draft modes for blogs, competitor-comparison pages, social posts, FAQ schema, and customer emails. Use when the user says "run the marketing monitor", "what are competitors publishing", "draft a comparison page", "draft a blog post", or on a weekly cadence. Do NOT use for pressure-testing finished copy against buyer personas; run /creative-agency on drafts before they publish.
---

# Guerrilla Marketing Agent

Marketing execution for teams without a marketing budget line: watch the market weekly, and turn what you see into content the same week. Two modes: **monitor** (sweep + 3 actions) and **draft** (a specific piece). Done means: a dated file in `outputs/marketing/` per `templates/content-formats.md`, routed to an owner from the distribution table.

Two hard rules:

1. **Product claims obey the claims register.** Every draft that names a capability checks `/creative-agency`'s `templates/claims-register.md` (if the user runs that skill); unregistered claims get flagged in the draft, not published.
2. **Competitor content is factual and verifiable only.** Honest comparison tables, no invented scores, and any competitor-specific legal guidance in the config is binding.

## Read first

| Source | Path | What to extract |
|---|---|---|
| Market config | `references/market-config.md` (user-filled) | Queries, competitors, differentiators, community venues, distribution owners |
| Baseline analysis | path named in the config | Prior SERP/positioning state, so monitor reports deltas, not rediscoveries |
| Content formats | `templates/content-formats.md` | The shape and save path for every mode |
| Positioning docs | `context/strategy/` | Messaging pillars drafts must stay inside |
| Prior monitor reports | `outputs/marketing/` | Last sweep, for trend continuity |

Config unfilled: build it conversationally first (category terms, top competitor, 3 differentiators minimum) and save it; a sweep on generic queries returns noise. No baseline yet: run monitor once, save it AS the baseline, and say that's what happened.

## Mode: monitor (default)

1. **SERP sweep:** run the config's 5-7 watch queries in parallel with your web search tooling (Firecrawl, Tavily, or built-in search).
2. **News sweep:** the config's 3-5 news queries, in parallel with the SERP pass.
3. **Community pulse:** search the config's venues; pull the top 3-5 threads. Note which vendor gets recommended, any mention of you (either polarity), and unanswered questions you could credibly answer.
4. **Delta analysis:** compare against the baseline; position changes, new attack content, threads needing presence, news to ride.
5. **Output:** the monitor report format, ending in exactly 3 actions with owners from the distribution table. Ten actions is a backlog; three is a week.

## Mode: draft [type]

Types: `blog`, `comparison`, `social`, `faq`, `email`; formats and save paths in `templates/content-formats.md`. For each: confirm the topic/target if not given (offer 3-4 options grounded in the latest monitor report), draft in practitioner tone, and end with the distribution row (channel, owner, format they need).

## Mode: news

The news sweep alone: dated bullets plus 1-2 content-opportunity callouts. For when the user wants signal without the full monitor.

## Writing rules for all content

Practitioner audience: write for the people who run the gear, not for buyers of slideware. Lead with the answer. Specific numbers, real tool names. Apply the workspace style rules (`rules/writing-style.md`). Comparison tables score honestly; conceding two rows you genuinely lose buys credibility for the rows you win.

## Worked example (fictional)

Coppermine Systems, Monday monitor run. The sweep finds competitor Ironvine shipped a "Coppermine alternative" page targeting `coppermine alternative console server`, and an unanswered r/networking thread asking how to manage console servers at 40 branch sites. The report's actions:

> 1. Draft the counter-comparison page "Ironvine Alternative: Coppermine for Enterprise OOB" targeting the same query. Owner: web manager. (This week; their page is 4 days old and thinly sourced.)
> 2. Answer the r/networking thread factually from the personal account; no product pitch unless asked. Owner: PM.
> 3. Blog: "What the new federal OOB guidance actually requires", riding this week's agency announcement. Owner: PM drafts, web manager publishes.

Then `draft comparison` produces the page per the format, with the honest-scoring table conceding Ironvine's larger reseller network.

## Don't rationalize

| If you're thinking | Do this instead |
|---|---|
| "Generic category queries are close enough" | The config's specific queries are the product. Generic queries return the same ten listicles every week. |
| "Five more actions would all be valuable" | Three actions with owners ship; ten actions rot. Cut to the three with the clearest this-week payoff. |
| "Score us 10/10 on every comparison row" | A clean sweep converts nobody. Concede real weaknesses; the table's credibility is what sells the strong rows. |
| "This claim is probably fine to include" | Probably means check the claims register or flag it. Marketing is where not-yet-GA features leak first. |
| "Skip the community pass, nothing changes there" | The community pass is where displacement happens sentence by sentence. It's three searches; run it. |

## Exit checklist

Before presenting output, verify:

- [ ] Sweeps used the config's queries, not improvised generic ones
- [ ] Monitor report diffs against the baseline; first-run baselines labeled as such
- [ ] Exactly 3 actions, each with an owner from the distribution table
- [ ] Drafts follow their format in `templates/content-formats.md`, saved to `outputs/marketing/`
- [ ] Product claims checked against the claims register or flagged; competitor content factual with honest scoring
- [ ] Every draft ends with its distribution row (channel, owner, format)

## Handoff

- **Before this:** `references/market-config.md` filled; `/context-search marketing` for prior sweeps and analyses.
- **After this:** `/creative-agency` on every draft before it publishes (the persona panel catches what the sweep can't); `/html-render` for briefing formats the owner wants as a page.
