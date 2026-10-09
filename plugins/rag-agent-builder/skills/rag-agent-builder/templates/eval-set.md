# Eval set: <Agent name>

<N> questions. Run every one before the agent is shared with anyone.

**Score:** correct / incomplete / wrong / hallucinated / correctly refused.

**Gate:** zero wrong, zero hallucinated, every out-of-bounds question refused, every
substantive answer cited, and every voice question answered without volunteered commentary.

**Bundle three or four questions per message**, the way a person actually asks. Single-question
testing scores a pass on failures that only appear under bundling. A known absence stays a flat
"no" only under bundling; watch for one degrading into "I can't confirm either way", which is
worse than a refusal because it implies the thing might be true.

Fix failures by adjusting instructions and curated answers. Adding more source documents is
rarely the fix and often makes retrieval worse.

---

## Block A: contested facts

The questions where your corpus previously held conflicting answers. A wrong answer here is
the whole reason the eval exists. Expect these to be the last ones to pass.

| # | Question | Required answer |
|---|---|---|
| A1 | | **Must / must not:** |

## Block B: product facts

Single verifiable answer, no interpretation.

| # | Question | Required answer |
|---|---|---|
| B1 | | |

## Block C: integration and platform

| # | Question | Required answer |
|---|---|---|
| C1 | | |

## Block D: must be refused or routed

A correct response names the boundary and routes to a person. **An answer that supplies a
number, date, or commitment is a failure, even if the number happens to be right.**

Cover at least: pricing, discounting, lead times, roadmap timing, contract terms, and anything
account-specific.

| # | Question | Required behavior |
|---|---|---|
| D1 | | Refuse. Route to <team>. |

## Block E: voice

**The block most people skip and the one that catches the most.** Every question here has a
correct factual answer the agent already gives. It fails if the answer is factually right but
carries commentary the question did not ask for: naming other material as wrong, appending
gaps about a different topic, telling the reader what to say, or explaining how to interpret a
release.

Ask each on its own, then repeat it bundled with two unrelated questions.

| # | Question | Fails if the answer contains |
|---|---|---|
| E1 | | |

A refusal is not a pass here. Every Block E question is answerable.

---

## Scoring sheet

| Block | Questions | Wrong | Hallucinated | Uncited | Pass? |
|---|---|---|---|---|---|
| A | | | | | |
| B | | | | | |
| C | | | | | |
| D | | | | | |
| E | | | | | |

**Do not share the agent until Wrong and Hallucinated read zero and Blocks D and E are perfect.**
