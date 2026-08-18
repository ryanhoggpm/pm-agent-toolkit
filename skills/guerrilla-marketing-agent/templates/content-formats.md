# Content formats

Every draft mode produces one of these shapes. Save paths per format; all drafts are review-ready, not publish-ready, and route through the config's distribution table.

## Monitor report (`outputs/marketing/monitor-<YYYY-MM-DD>.md`)

```markdown
## Marketing Monitor, [date]

### SERP Position Snapshot
| Query | Our position | Notable changes |
|---|---|---|

### Competitor Moves
[New pages, messaging changes, attack content. Bullets with links.]

### Community Opportunities
[Threads to engage, mentions of us (either polarity), unanswered questions we could answer.]

### News / Events to Ride
[Regulatory announcements, industry news, launches to attach to.]

### 3 Actions This Week
1. [Specific action, estimated impact, owner from the distribution table]
2. ...
3. ...
```

## Blog post (`outputs/marketing/blog-<slug>-<date>.md`)

Title optimized for the target query; primary + 2 secondary keywords stated in metadata. 600-900 words, practitioner tone. One concrete scenario. One CTA. A 2-3 question FAQ section formatted for schema markup. Suggested tags from the config's category terms.

## Comparison page (`outputs/marketing/comparison-<slug>-<date>.md`)

The highest-value asset: it intercepts buyers at decision stage.

```
H1: [Competitor] Alternative: [Your product] for [category]
Meta description: [60-65 chars, primary keyword included]

Intro (2 paragraphs): frame the choice, who this page is for
Comparison table: 8-10 features, honest scoring (a table that scores you 10/10
  reads as marketing and converts nobody)
Why buyers switch: 3 specific reasons with proof
Your strengths: the config's differentiators, substantiated
Migration path: "Moving from [competitor]: what it takes"
FAQ: 4 questions, schema-formatted
CTA: demo / talk to an expert
```

## Social post (`outputs/marketing/social-<topic>-<date>.md`)

150-250 words. First line is the hook; no "excited to announce". 2-3 short paragraphs, one concrete data point or scenario, one question or CTA, 4-5 hashtags from the config's category terms. State which account it's written for (personal vs company voice differ; the distribution table says which needs approval).

## FAQ schema entries (`outputs/marketing/faq-<page>-<date>.md`)

4-6 entries per page, JSON-LD plus plain-English version. Target the questions buyers actually type: differences vs the competitor, compliance-standard fit, end-of-sale replacements, scale limits.

## Customer email (`outputs/marketing/email-<purpose>-<date>.md`)

Plain text, under 150 words, direct subject line, one specific ask. Segment note from the distribution table.
