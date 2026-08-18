---
name: sales-analyst
description: Analyze multi-year sales pivot tables into YoY revenue, unit, and ASP trends, lifecycle classification, external market-event correlation, and Invest/Maintain/Harvest/Exit portfolio verdicts with a data quality audit. Use when the user says "analyze this sales data", "run sales-analyst", "why did revenue move", "which products should we invest in", or shares a revenue or unit pivot table. Do NOT use for pipeline forecasting or single-deal analysis; it interprets shipped historical revenue and unit data only.
argument-hint: "[product-line] [fiscal-year(s)]"
---

# Sales Analyst

Correlate internal revenue and unit data with external market forces to explain what the numbers mean, why they moved, and what to do about it. Done means: a report per `templates/output-template.md` in `outputs/analyses/` where every trend claim has a period and a number, every inflection has a named external factor, and every family has a portfolio verdict.

Three hard rules, in order:

1. **Sensitivity gate before any analysis.** Scan incoming data for customer/account/reseller names, account-attributed revenue, or PII. If found, stop and point at the masking workflow in `rules/sensitive-data.md`; proceed only after the user confirms the data is masked or explicitly accepts sending it unmasked. Aggregates by family, units by SKU, ASPs, and regional totals are safe.
2. **Scope before running.** More than 4 product families or 5+ years: offer to start with one family or period, then expand.
3. **Confidence is always labeled.** Every hypothesis carries High / Medium / Hypothesis. Nothing speculative gets stated as fact.

## Read first

| Source | Path | What to extract |
|---|---|---|
| Portfolio context | `templates/portfolio.md` (user-filled) | Families, use cases, segments, competitors, settled strategy calls, SKU decoding |
| Event inventory | `references/market-events.md` | External factors overlapping the data's time range |
| Prior analyses | `outputs/analyses/` | Earlier runs to compare against instead of restarting |
| Strategy docs | `context/strategy/` | Portfolio decisions and roadmap direction the verdicts must engage with |
| Metrics history | `context/metrics/` | Baselines and previous financial summaries |

Portfolio file unfilled: collect family descriptions and segment context conversationally, offer to save them into the template, and label the analysis as running on user-supplied context. Data in a connected source (Airtable, a BI tool with MCP): query it directly, but the sensitivity gate applies to query results exactly as to pasted files.

## Workflow

### 1. Intake and orientation

After the sensitivity gate: identify the structure (rows, columns, metrics present), map SKUs to families using the portfolio file's decoding notes, confirm the time range and any gaps, note geographic dimensions, and state every classification assumption explicitly before analyzing.

### 2. External factor mapping

From `references/market-events.md`, build the event timeline for this dataset's period and product mix. Only events within or immediately preceding the period; note which families each touches. This backdrop comes before the numbers so trends get interpreted against it rather than decorated with it afterward.

### 3. Financial analysis (per family)

- **Trends:** YoY revenue growth and YoY unit growth separately (their divergence is the ASP signal). Flag inflection points where growth rate moved more than 15 points, and tag each with the most likely external factor.
- **ASP:** rising means premium mix, shortage pricing, or volume collapse on fixed-price products; falling means commoditization, price pressure, or down-market mix. Say which, and why.
- **Lifecycle:** Introduction / Growth / Maturity / Decline.
- **Contribution:** rank families by revenue over the full period; flag shrinking contribution share even where absolute revenue is flat.
- **Segments/geo** (if the data has them): over/under-indexing regions with hypotheses.

### 4. Hypothesis generation

For each inflection point, one specific falsifiable hypothesis: "[Family] [trend] beginning [period], likely driven by [factor] because [reasoning connecting the product's use case to the factor]." Rate confidence. A hypothesis that could describe any hardware company fails the grounding test; it must use this portfolio's deployment reality.

### 5. Portfolio verdicts

Invest / Maintain / Harvest / Exit per family, each with rationale, the key risk if the verdict is wrong, and a time horizon. Where a verdict contradicts a settled decision in the portfolio file, surface the disagreement explicitly with the driving data; never silently re-litigate, never silently defer.

### 6. Opportunity and risk flags

Tailwinds the portfolio can capture, underserved segments, competitor gaps; then early-warning declines, threats 12-18 months out, concentration risk.

### 7. Data quality assessment

Always present, even for clean data: the dimension table, anomalies, and concrete structural recommendations for the next cycle's pivot table.

## Worked example (fictional)

Two Coppermine Systems hypotheses at the required specificity:

> CM-400 revenue peaked in FY2021 and declined through FY2023 while ASP rose 9%, consistent with component-shortage supply constraints suppressing unit shipments and shortage pricing masking the volume decline. Maturity-stage buyers likely delayed rather than switched, which predicts pent-up refresh demand in FY2024 data. Confidence: Medium.

> EdgeLink cellular units dropped 31% in Q1 2022, consistent with the January 2022 AT&T 3G sunset forcing replacement of 3G-connected units; if fulfillment lagged during that window, competitive displacement is likely and should show as permanently lower share in FY2023. Confidence: High.

And a verdict row:

> | CM-400 | Harvest | Declining but profitable installed base through EoS 2026-12-31 | Refresh demand leaks to competitors instead of CM-900 | 18-24 months |

## Don't rationalize

| If you're thinking | Do this instead |
|---|---|
| "The data looks aggregated, skip the sensitivity scan" | The scan takes seconds; a distributor name in a column header is exactly what it catches. Gate first, always. |
| "Revenue is up, so units must be up" | Compute them separately every time. Shortage-era ASP inflation hiding unit decline is the single most common misread. |
| "Market headwinds explain the dip" | Unnamed headwinds explain nothing. Cite the specific event, its dates, and why THIS product's use case is exposed to it. |
| "The strategy file already settled this family's verdict" | Settled decisions get tested against the data, not assumed. Agreement is a finding too; state it. |
| "The data is clean, skip the quality section" | The section is always present. Clean data deserves the structural recommendations that keep it clean. |

## Exit checklist

Before presenting the report, verify:

- [ ] Sensitivity gate ran and its outcome is recorded in the report's assumptions
- [ ] Every trend claim carries a period and a specific percentage or absolute change
- [ ] Every inflection point names an external factor with dates, none say "market conditions"
- [ ] Revenue and unit trends computed separately; ASP movement interpreted, not just reported
- [ ] Every hypothesis rated High / Medium / Hypothesis
- [ ] Every verdict has rationale, key risk, and time horizon; conflicts with settled strategy surfaced
- [ ] Data quality section present with concrete structural recommendations
- [ ] Report follows `templates/output-template.md`; dull families dispatched in two sentences

## Handoff

- **Before this:** `/context-search sales analysis` for prior runs on the same lines, and fill `templates/portfolio.md`; the grounding is the difference between analysis and commentary.
- **After this:** capture the portfolio verdicts as a decision record; feed opportunity gaps into your PRD process; `/creative-agency` if a finding becomes customer-facing messaging (the claims register keeps the numbers honest in public).
