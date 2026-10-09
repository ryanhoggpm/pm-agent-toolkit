# Focus-group output format

The full run prints three parts in order. Save to `outputs/creative-agency/<content-name>-review-<YYYY-MM-DD>.md` when the user wants it kept; otherwise print to the conversation.

## Part 1: Per-persona review (every persona, in panel order)

```
**[Persona name]**
Overall: [One sentence on what they think]
Would cut: "[Exact line or phrase they'd stop at]", [brief reason in their voice]
Would keep/share: "[Exact line or phrase that lands]", [brief reason]
```

## Part 2: Synthesis

```
**Synthesis**
Working across all personas: [What's landing broadly]
Conflict: [Where one persona's needs work against another's, be specific]
Resolution: [How the audience weighting resolves it]
Claims risk: [Register violations found, each with the register line it breaks, or "none"]
```

## Part 3: Revised draft

The full revised draft, tone-calibrated. Lines that deliberately walk a tension
(serving one persona at slight cost to another) get a one-line [bracketed note]
after the draft, not inline.

## Headline mode output

```
| Headline | [P1] | [P2] | [P3] | Weighted read |
|---|---|---|---|---|
| "[candidate]" | nod / cringe / neutral | reads / skips | stays / leaves | [score reasoning] |
```

Then: recommend one, with two sentences of reasoning.
