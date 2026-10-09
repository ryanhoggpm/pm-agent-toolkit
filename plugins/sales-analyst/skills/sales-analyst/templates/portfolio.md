# Portfolio context (fill this in once, update on strategy changes)

`/sales-analyst` reads this file to ground financial analysis in what the products actually are, who buys them, and what's already been decided about them. Without it, the analysis degrades to generic hardware commentary. Update it when strategy shifts; the skill trusts this file over its own inferences.

## The schema

```markdown
# Portfolio: [company] (updated YYYY-MM-DD)

## Product families
| Family | Category / use case | Deployment profile | Variants that matter | Lifecycle facts |
|---|---|---|---|---|
| [name] | [what job it does, who uses it] | [where it lives: DC, branch, carrier NOC] | [cellular vs wired, DC vs AC power, form factors] | [EoS/EoL dates, launch dates] |

## Customer segments
[Ranked list with one line each on why they buy]

## Competitive set
[Primary competitor and stance; secondary competitors; any legal guidance on naming them]

## Strategic decisions already made
[Invest/maintain/harvest calls that are settled. The analysis should test these
against the data, not re-litigate them silently.]

## SKU decoding notes
[Naming conventions: how to read power type, connectivity, port count from a SKU string]
```

## Example (fictional): Coppermine Systems, updated 2026-06-10

### Product families

| Family | Category / use case | Deployment profile | Variants that matter | Lifecycle facts |
|---|---|---|---|---|
| CM-900 | Console server / OOB management, current flagship | Enterprise DC and large branch | 16/32/48-port; AC and DC power | Launched 2026-06 |
| CM-400 | Console server, prior generation | Installed base across all segments | Cellular and wired SKUs | EoS 2026-12-31, EoL 2031-12-31 |
| EdgeLink | Compact remote-access gateway | Small branch, no on-site IT | Cellular-primary | Mature |
| Fleet Cloud | SaaS management platform | Attaches to all hardware | Per-device subscription | Growth investment |

### Customer segments

1. Enterprise IT (financial, healthcare, retail): buys for uptime and audit posture
2. Telco/MSP: DC-powered appliances in carrier NOCs, long refresh cycles
3. Federal/defense: compliance-driven, lumpy procurement

### Competitive set

Primary: one entrenched market leader with a strong software story. Secondary: two hardware-first vendors competing on price. Factual, verifiable comparisons only in any output.

### Strategic decisions already made

CM-900 + Fleet Cloud is the growth path. CM-400 is harvest through EoS. EdgeLink is maintain pending cellular refresh data.

### SKU decoding notes

Trailing `-DC` = DC power. `C` before the port count = embedded cellular. Port count is the last two digits.
