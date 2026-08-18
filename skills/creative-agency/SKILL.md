---
name: creative-agency
description: Run a marketing draft through a simulated focus group of weighted buyer personas, producing per-persona reactions (what each would cut or share), a conflict-resolving synthesis, a shipped-claims check, and a revised draft calibrated to audience weighting. Use when the user says "run this through creative-agency", "focus group this draft", "how would customers react to this copy", "test these headlines", or before publishing any customer-facing content. Do NOT use for internal communications or PRD review; it reviews outbound marketing content against buyer personas only.
---

# Creative Agency

Simulate a mixed-audience focus group for marketing content. Exists because category marketing is easy to write for a vendor echo chamber and hard to write for the people who actually buy and use the product. Done means: five sharp per-persona reactions, one weighted synthesis, and a revised draft that survived the claims check.

Two hard rules:

1. **Never invent product capabilities in a revised draft.** Every claim passes `templates/claims-register.md`; anything not in the register gets flagged, not passed.
2. **No content, no run.** If the user invokes without a draft, ask for it.

## Read first

| Source | Path | What to extract |
|---|---|---|
| Persona panel | `templates/personas.md` (user-filled) | The personas, their weights, cringe triggers, humor registers |
| Claims register | `templates/claims-register.md` (user-filled) | What's claimable fully / conservatively / not at all |
| Output format | `templates/review-format.md` | Structure for the three-part output and headline mode |
| Messaging context | `context/strategy/` (positioning, messaging pillars) | Current pillars the revised draft must stay inside |
| Prior reviews | `outputs/creative-agency/` | Earlier runs on the same content; iterate, don't restart |

If the panel is only the shipped example (fictional Coppermine personas), say so and offer to build the user's real panel from the schema before running; running real copy through example personas produces confident nonsense. If the claims register is missing or stale (no update date within the product's release cycle), flag that the claims check is running blind.

## Modes

```
/creative-agency [content]                 full run, professional tone (default)
/creative-agency tone:peer [content]       peer tone
/creative-agency tone:full-voice [content] full-voice tone
/creative-agency headlines [list]          headline testing only
/creative-agency personas                  show the panel, run nothing
/creative-agency claims-check [content]    register check only, no focus group
```

## The process

### 1. Per-persona review

Run every persona in panel order. For each: one-sentence overall read, one exact quote they'd cut with the reason in their voice, one exact quote they'd keep or share. Format per `templates/review-format.md`. Reactions must use the persona's own triggers from the panel file; a review that any persona could have given means the panel wasn't actually applied.

### 2. Synthesis

What's landing across personas; the specific conflict where one persona's needs work against another's; the resolution the weights dictate; and the claims-risk list, each violation citing the register line it breaks.

### 3. Revised draft

Rewrite incorporating the synthesis, at the requested tone. Flag deliberate tensions (serving the 40% persona at slight cost to the 25%) in bracketed notes after the draft, never inline. Apply the workspace writing rules (`rules/writing-style.md`) and any banned-word list the user's panel or style rules define.

## Tone calibration

- **`professional`** (briefs, datasheets, web copy): humor in word choice and subtext only; one knowing observation per section is the ceiling; the primary persona nods, doesn't laugh; specificity is the credibility signal.
- **`peer`** (technical blogs, conference content, social posts by humans): written as if the primary persona wrote it; dry wit visible; jargon appropriate and expected; the filter is lower, the facts aren't.
- **`full-voice`** (video scripts, event activations, community-forum register): the culture and humor on the surface, contempt for bad tools included; still factually accurate, the claims register applies at every tone.

## Headline mode

For each candidate: primary persona nod/cringe/neutral, budget-holder reads/skips, technical persona stays/leaves, one sentence each. Rank by weighted score, recommend one. Table format in `templates/review-format.md`.

## Worked example (fictional)

Coppermine Systems runs a launch-page paragraph through the example panel:

> Draft line: "Coppermine's next-generation platform delivers seamless zero-touch provisioning, so you're covered when the network goes down."

> **Priya (Sr NE, 40%)**
> Overall: Stopped reading in the first clause.
> Would cut: "next-generation... seamless", "two of my cringe words in nine words, and the disaster cliché to finish. A vendor who's never been paged."
> Would keep/share: "zero-touch provisioning", "real feature, just say what it does at 60 sites."

> **Synthesis (excerpt)**
> Conflict: Sam wants the API spec named in sentence one; Warren skips anything with a spec number in it.
> Resolution: 40/20 outweighs 25; lead technical, give Warren an outcomes line immediately after.
> Claims risk: none in this excerpt; register check passed.

> Revised: "Provision a new site before the courier's van leaves the parking lot. Zero-touch provisioning through the OpenAPI 3.1 API, with a fleet dashboard your ops manager can read without you translating."

## Don't rationalize

| If you're thinking | Do this instead |
|---|---|
| "The draft is short, skip straight to a revised version" | The per-persona pass IS the product. Without named reactions, the revision is just your taste with extra steps. |
| "This persona wouldn't care about this piece" | Run them anyway, briefly. "Warren skips this entirely" is a finding that changes where the piece gets used. |
| "The claim is probably shipped by now" | The register is the authority, not probability. Flag it; the user updates the register if reality moved. |
| "The personas agree, so no conflict section" | Unanimous panels usually mean the reviews were generic. Re-check reactions against each persona's specific triggers before accepting agreement. |
| "Full-voice tone means looser facts" | Tone changes the register of the writing, never the truth of the claims. |

## Exit checklist

Before presenting the output, verify:

- [ ] Every persona reviewed, in order, with exact quotes from the actual draft (not paraphrases)
- [ ] Each reaction traces to that persona's defined triggers, not generic marketing critique
- [ ] Synthesis names a real conflict and resolves it by the stated weights
- [ ] Claims check ran against the register; violations cite the register line; register staleness flagged if applicable
- [ ] Revised draft contains no capability absent from the register's include lists
- [ ] Output follows `templates/review-format.md`; tension notes bracketed after the draft, not inline

## Handoff

- **Before this:** `/context-search` for current positioning and any prior review of the same content; a revised draft that contradicts the messaging pillars trades one problem for another.
- **After this:** publish, and when the user reports real audience reaction, log where the panel's prediction missed (per `rules/system-learning.md`); persona files improve the same way skills do.
