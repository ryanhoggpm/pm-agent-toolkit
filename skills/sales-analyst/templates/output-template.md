# Sales analysis report template

Save as `outputs/analyses/sales-analysis-<YYYY-MM-DD>.md`. Sections marked "(only if...)" get dropped when their inputs are missing, not left empty. The data quality section is never dropped.

```markdown
# Sales Analysis: [Product line / dataset name]
**Date:** [YYYY-MM-DD]
**Data scope:** [Time range] | [Product families] | [Geographies if applicable]

## Assumptions and context

[Every assumption made about product classification, use cases, or data
interpretation. Flag anything the user should confirm.]

## External market context

[Table of applicable events from references/market-events.md, scoped to this
dataset's time period and product mix.]

## Financial analysis

### Portfolio overview

[Summary table: family, total revenue over period, YoY growth rates,
lifecycle stage, contribution share.]

### [Product family]

**Trend:** [1-2 sentences on revenue and unit trajectory]

**Key inflection points:**
- [Period]: [what changed, with the external-factor correlation]

**ASP analysis:** [rising / falling / stable, and the interpretation]

**Lifecycle stage:** Introduction / Growth / Maturity / Decline

**Hypothesis:** [Specific, falsifiable, tied to a named external factor,
with confidence: High / Medium / Hypothesis]

*(repeat per family; a family with no interesting story gets two sentences)*

## Segment and geographic analysis (only if data supports it)

[Regions or segments over/under-indexing, with hypotheses.]

## Portfolio recommendations

| Family | Verdict | Rationale | Key risk if wrong | Time horizon |
|---|---|---|---|---|
| | Invest / Maintain / Harvest / Exit | [1 sentence] | [1 sentence] | [e.g. "harvest over 18-24 months"] |

[Where a verdict contradicts a settled decision in templates/portfolio.md, say so
explicitly and show the data driving the disagreement.]

## Opportunity flags

[Tailwinds the portfolio can capture; underserved segments; competitor gaps.]

## Revenue risk alerts

[Accelerating declines not yet in headline numbers; external threats 12-18
months out; concentration risk if the data shows it.]

## Data quality assessment

**Overall rating:** High / Medium / Low

| Dimension | Present? | Quality | Improvement |
|---|---|---|---|
| Revenue | | H/M/L | |
| Unit volumes | | H/M/L | |
| ASP (or calculable) | | H/M/L | |
| Margin | | H/M/L | |
| Customer segment dimension | | H/M/L | |
| Geographic dimension | | H/M/L | |
| SKU naming consistency | | H/M/L | |
| Time period consistency | | H/M/L | |
| Channel dimension | | H/M/L | |

**Anomalies:** [outliers, zero-value gaps, SKU duplication, missing periods]

**Structural recommendations:** [concrete pivot-table changes for next cycle,
e.g. "add a Power Type column (AC/DC/PoE) so segment filtering doesn't need
manual SKU lookup"]

## Suggested next steps

- [ ] [Action tied to the highest-confidence finding]
- [ ] [Action tied to the top revenue risk]
- [ ] [Data collection or query that would validate the weakest hypothesis]
```
