# Audience profiles and doc sources (fill this in once)

`/tech-writer` reads this file to know who it's writing for and where your product truth lives. Without it, the skill asks each time.

## Audiences

Define each audience the docs serve. The default four cover most B2B hardware/software companies; rename and adjust.

| Key | Who they are | What they know | What they need from docs |
|---|---|---|---|
| `customer` | [e.g. network/IT engineer at an enterprise] | Knows the domain, not your product | Task completion without a support call |
| `partner` | [channel SE or sales rep] | Sells your product, isn't an expert in it | Enough depth to demo and answer objections |
| `fae` | [your field application engineer] | Knows the product deeply | Demo scaffolding, not product education |
| `sales` | [your sales rep] | Surface-level | Just enough for a credible technical conversation |

## Doc sources

| Source | Path | What's there |
|---|---|---|
| Existing product docs | `context/reference/docs/` | Docs to improve or stay consistent with |
| Product context | `context/products/` | What the products actually do |
| PRDs | `context/prds/` | Intended behavior, for docs written pre-release |
| User research | `context/research/` | Real pain points and vocabulary users actually use |

## Terminology decisions

[One name per thing, used everywhere. List the chosen term and the banned synonyms,
e.g. "console server (never: appliance, box, unit)". Also list your product's jargon
that must be defined on first use in every customer-facing doc.]

## Example (fictional): Coppermine Systems

- `customer` = enterprise network engineer; knows BGP, has never seen a CM-900
- Jargon requiring first-use definition: boot bank, step upgrade, fleet group, provisioning manager
- Terminology: "console server" (never "appliance"); "Fleet Cloud" (never "the cloud platform")
