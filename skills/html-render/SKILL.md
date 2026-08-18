---
name: html-render
description: Render existing content (a markdown file or the conversation's output) as a self-contained, brand-themed HTML file with a gradient header, stat cards, callouts, and themed tables, then run a pre-save QA pass that catches templated-looking output. Use when the user says "render as HTML", "make this HTML", "branded output", "create a deck", "slides", or passes an --html flag. Do NOT use to write or restructure content; it renders what already exists, and asks before any restructuring a format demands.
argument-hint: "[content or file path] [--template report|analysis|brief|presentation]"
---

# HTML Render

Convert finished content into a self-contained branded HTML file. Done means: a single .html in `outputs/` that embeds all CSS, passes the exit checklist below, and reads as authored rather than templated.

Two hard rules:

1. **Render, never rewrite.** The content is done; this skill changes its form. If the format demands restructuring (prose into slides), ask first: "this needs splitting into N slides, proceed?"
2. **All assets inline.** No external CSS, JS, or font dependencies; named fonts fall back to system faces offline.

## Read first

| Source | Path | What to extract |
|---|---|---|
| Brand CSS | `assets/brand-tokens.css` (user re-skins the `:root` block) | Tokens and the `.pm-*` component classes |
| Canonical template | `templates/report.html` | The embed marker and `CONTENT_*` injection-point pattern |
| Source content | argument, or the file just produced in-session | The content to render, as-is |
| Prior renders | `outputs/` (matching .html) | An existing render of this content to update instead of duplicate |

If the CSS still has the neutral starter palette and the user has a brand, offer once to capture their tokens (colors, two fonts, radius) into `assets/brand-tokens.css`; every later render inherits them.

## Workflow

### 1. Select the template

- "presentation" / "slides" / "deck" → a slide-format page
- Data-heavy (2+ tables or 4+ H2 sections) → report layout
- Otherwise ask: report, analysis, brief, or presentation?

`templates/report.html` ships as the canonical layout. For other formats, generate the template on first use following its exact pattern (CSS embed marker, `CONTENT_*` injection comments, section rhythm) and save it to the user's workspace so later renders reuse it.

### 2. Embed the CSS

Read the template, replace the `PM_CSS_EMBED` comment in `<style>` with the full contents of `assets/brand-tokens.css`.

### 3. Fill the injection points

Convert markdown structures to their HTML equivalents (`##` → h2, tables → `.pm-table`, key insights → `.pm-callout`). Reach for `.pm-pull-quote` and `.pm-icon-badge` where they add real visual interest, not on every section. Stat cards show outcomes, not specs; a GA date or an endpoint count reads as "sure, but so what."

### 4. Save and report

`outputs/<type>/<descriptive-name>-<date>.html`, alongside the source markdown. Report the path.

## The quality bar

Section-to-section visual variance (alternating bands, the header glow), one accent color used consistently, one corner-radius system, and small finished-page details: themed `::selection`, focus rings, tabular numerals. The failure mode to avoid is the flat single-color header with uniform white sections; that's the templated look this skill exists to prevent.

## Worked example (fictional)

Coppermine Systems renders `sales-analysis-2026-06-10.md`. The report's "CM-400 revenue -14% YoY" line becomes a stat card with a `down` trend; the harvest verdict becomes a `.pm-callout warn` in the analysis band; the recommendation table renders as `.pm-table` with `.pm-badge` states for Invest/Harvest. Nothing is reworded; the one restructuring (splitting a 14-row table into two grouped clusters) was asked about first.

## Don't rationalize

| If you're thinking | Do this instead |
|---|---|
| "I'll tighten the copy while I'm converting it" | Rendering is form only. Copy edits go back to the source document, by request. |
| "A second accent color would help this section pop" | One accent, everywhere. Per-section accent swaps are the top templated-look tell. |
| "The stat row needs a fifth number, I'll derive one" | Every stat traces to source content. An invented or round-derived number is worse than an empty slot. |
| "Badges on every heading make it look designed" | Badges and dots carry state (risk, priority) or they don't exist. Decoration without meaning reads as AI filler. |
| "The checklist is long and the page looks fine" | The checklist exists because pages that "look fine" ship with white-on-white badges and jittering digits. Run it. |

## Exit checklist (pre-save QA)

Run before writing the final file; skip only boxes that can't apply to the content type.

- [ ] Zero em dashes anywhere: headlines, badges, body, captions
- [ ] No AI buzzwords; concrete verbs only
- [ ] No placeholder names ("Jane Doe", "Acme Corp"); realistic specifics or nothing
- [ ] Every number traces to source content; nothing invented to fill a stat card
- [ ] One accent color and one radius system across the whole document
- [ ] Contrast check on every badge, button, and callout (WCAG AA)
- [ ] Re-read every visible string for phrasing garbled during conversion
- [ ] Tables over 8 rows use grouped sparse dividers, not a hairline per row
- [ ] Pull-quotes at most 2-3 lines, trimmed to the sharpest sentence
- [ ] `::selection`, focus rings, and scrollbars themed, not browser-default
- [ ] Stat cards and data tables use tabular numerals
- [ ] Multi-tab documents: Overview tab first and active, outcome-based stat row, full-bleed tab bars use the inner wrapper so labels align with the content column
- [ ] File is fully self-contained; opens correctly offline

## Handoff

- **Before this:** the skill that produced the content (`/sales-analyst`, `/api-review`); render finished work, not drafts mid-revision.
- **After this:** `/creative-agency` if the page is customer-facing marketing; internal reports ship as-is.
