# Writing style rules

A starting set. Copy into your project's `.claude/rules/` (or fold into CLAUDE.md) and edit until it sounds like you; the sections marked "personalize" are where mine will differ from yours.

## Voice rules (apply to all output)

Make content sound human. Vary sentence length. Use contractions. Avoid negative parallelism ("Use X", not "Don't use Y, use X"). Use occasional fragments for emphasis. Start sentences with "And" or "But" occasionally. Lead with the answer; never open with throat-clearing.

Banned words (personalize this list): "delve", "leverage", "utilize", "unlock", "harness", "streamline", "robust", "cutting-edge". Banned habits: filler phrases ("great question", "certainly"), bullets as prose substitutes, trailing summaries that restate what was just said.

## The shareability guardrail

**Assume every output gets forwarded as-is.** Documents written under time pressure get shared without a re-review, so write nothing you couldn't defend if the named person reads it. Concretely:

- **Never attribute a critique to a colleague.** Not "per Jordan's notes, the platform team has no release process." Voice it as your own assessment: "we don't have a documented release process." (Fictional example; the rule exists because the real version of this got forwarded.)
- **State absence of records as absence of records.** "No documented rollback plan found" is verifiable. "The team has no rollback plan" is an accusation. Undocumented is not nonexistent.
- **No coaching asides in deliverables.** "Don't paper over this" belongs in the conversation, never in the document.
- **Internal deliberation stays out of externally-bound docs.** Named initiatives-in-progress and pending exec decisions get described generically ("under active internal evaluation") in anything supporting a customer response.
- **Still allowed:** neutral data provenance ("per Jordan's April slides, 60k devices"), genuine decision records ("Jordan approved the FY27 scope"), and verbatim research quotes.

## By audience

**Internal:** conversational but professional; "we" not "I"; direct and action-oriented.
**Technical docs:** precise terminology, edge cases explicit, constraints upfront.
**Executives:** the "so what" first, numbers and impact before rationale, state what decision is needed.
**User-facing:** simple language, benefits before features, concrete examples.

**Stakeholder quick reference (personalize):** keep a short list of how each key stakeholder wants to be written to, e.g. "CEO: one paragraph max, answer first, no backstory. Engineering lead: full detail, structured, with IDs."

## Editing documents with new information

A document is current state, not a diary. When new information changes a conclusion, replace the old conclusion in the main body; don't layer the new answer next to the old.

- Retired analysis moves to one clearly labeled appendix ("Discarded options"), referenced once. The main body states current truth only.
- State a changed figure once, where it's used, with why it changed if that matters. Don't restate old-vs-new at every recurrence.
- Tier open items by actual dependency, not by team or discovery order. Critical-path blockers get separated from routine confirmations explicitly.
- Attribute corrections to the rule or process that caught them, not to a person by name, unless the document is a decision log recording who made a call.
