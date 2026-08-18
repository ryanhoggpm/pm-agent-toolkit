---
paths:
  - "sensitive-data/**"
  - "*.csv"
  - "*.xlsx"
  - "*.xls"
---

# Sensitive data rules

This file demonstrates a **path-scoped rule**: the `paths:` frontmatter means it loads only when Claude touches spreadsheets or the `sensitive-data/` directory, so it costs zero context the rest of the time. Copy the pattern for any rule that's only relevant to certain files. (If your Claude Code version doesn't support path-scoped rules, reference this file from CLAUDE.md with a "read before touching CSV/Excel" instruction instead.)

When customer names, individual account revenue, email addresses, or PII appear in data shared for analysis:

1. Flag it before proceeding and ask whether to run the masking workflow first
2. Never write customer names or account-level data to `context/` or `outputs/`
3. Direct sensitive analysis outputs to `sensitive-data/outputs/` only
4. Don't proceed with analysis of clearly sensitive data until acknowledged

## Data classification

| Data type | Sensitivity | Action |
|---|---|---|
| Customer names, account IDs | High | Mask before sharing |
| Individual account revenue | High | Mask or exclude |
| Deal pipeline, forecast data | High | Mask before sharing |
| Internal financial targets | High | Mask or exclude |
| Aggregate revenue by product family | Medium | OK if not customer-attributed |
| Part numbers, SKUs, product names | Low | OK to share |
| Regional aggregates | Low | OK to share |
| Public competitive data | Low | OK to share |

## Pseudonymization workflow

Bring your own masker; any deterministic pseudonymizer works (consistent fake name per real name, mapping file kept locally). The workflow shape:

1. Raw file lands in `sensitive-data/raw/`
2. Masking script writes to `sensitive-data/masked/`, mapping to `sensitive-data/mappings/`
3. Only the masked file is shared or analyzed in context

Optionally keep a gitignored `sensitive-data/known-customers.json` list so recurring names are always caught. Never put real customer names in any tracked config file.

**Gitignore these paths:** `sensitive-data/raw/`, `sensitive-data/masked/`, `sensitive-data/mappings/`, `sensitive-data/outputs/`, `.env`, `*.xlsx`, `*.xls`, `*.csv`.

## About AI training

Check your Claude plan's current data policy before analyzing sensitive data at all, and re-verify periodically; policies change. API-based tools and consumer plans differ on whether conversations may be used for training.
