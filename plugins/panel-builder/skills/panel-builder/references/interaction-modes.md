# Interaction Modes

Five choreographies. The charter picks one; the runner executes it. Every mode obeys the
hard rules in SKILL.md (one question per session, conflicts flagged, pointed dispatch
prompts, simulated labeled simulated).

A mechanical note that applies to any mode with a second round: dispatch the first round
as parallel subagents, then continue the SAME agents for rebuttals (send a follow-up
message to each rather than spawning fresh ones), so each member argues from the context
of what they already said.

---

## 1. specialist-consult

**Use for:** a technical or domain decision needing multiple expert disciplines
(engineering trade study, architecture call, compliance question).

**Roles:** one lead (frames the problem), 2-4 domain specialists, chair synthesizes.

**Choreography:**
1. Lead agent frames the question as verifiable requirements (shall/will/should where it
   fits) and names which specialists actually need to weigh in. Not always all of them.
2. Dispatch the named subset in parallel. Each prompt carries: the framed requirement,
   the relevant facts from standing context, and one pointed question for that discipline.
3. Synthesize into a trade study: options as rows, criteria as columns, weighted scores
   defensible from specialist input. A decision matrix is optional but preferred for 3+
   options.
4. Flag every inter-specialist conflict explicitly ("electrical wants X, mechanical wants
   Y") and state what evidence would resolve it.

**Output:** requirement statement, per-domain findings, trade-off matrix, conflicts,
recommendation, tiered open items (blockers separated from routine confirmations).

**Failure mode to watch:** specialists answering a generic "review this" instead of their
pointed question. If a response reads like a book report, the dispatch prompt was too thin.

---

## 2. weighted-panel

**Use for:** reaction-testing a draft (messaging, a proposal, positioning) against a
defined audience mix.

**Roles:** 3-6 personas with explicit audience weights summing to 100%. Chair synthesizes.

**Choreography:**
1. Every persona reads the full draft. Dispatch in parallel.
2. Each returns: what they'd keep, what they'd cut, where they stopped reading, and
   whether they'd share/act on it. In their voice.
3. Weighted synthesis: a line that delights a 10% persona but stalls a 40% persona loses.
   Show the math when a call is close.
4. Produce a revised draft calibrated to the weighting, with a change list tied to
   specific persona reactions.

**Output:** per-persona reactions, weighted synthesis, revised draft.

**Failure mode:** personas converging into one polite reviewer. If all reactions could
have come from the same person, re-read the persona definitions before rerunning; the
triggers and optimization sections are probably too similar.

---

## 3. review-board

**Use for:** cross-functional review of a PRD, product concept, or plan before it ships
to stakeholders.

**Roles:** 3-5 reviewers with deliberately conflicting mandates (feasibility, user value,
business case, risk, and one designated skeptic whose job is the strongest case against).
Chair runs it.

**Choreography:**
1. All reviewers read the artifact. Dispatch in parallel; each prompt names their mandate
   and the 2-3 sections most load-bearing for it.
2. Each returns findings as: severity (blocker / major / minor), the specific claim or
   section, why it fails their mandate, and what would fix it.
3. Chair de-duplicates, then surfaces disagreements between reviewers as their own
   section; a feasibility "blocker" that the business reviewer calls essential is the
   most valuable output the mode produces.
4. Verdict per reviewer (ship / ship with fixes / rework) plus the chair's consolidated
   fix list, ordered by severity, not by reviewer.

**Output:** findings table, disagreements, per-reviewer verdicts, consolidated fix list.

**Failure mode:** findings inflation. Cap each reviewer at their top 5; twenty minor
comments bury the one blocker.

---

## 4. persona-interview

**Use for:** discovery interviews or journey walkthroughs with simulated users/customers
of your product when the real ones aren't available this week.

**Roles:** 1-3 user personas per session (more dilutes depth), the chair as interviewer
or the user interviewing directly.

**Choreography:**
1. Session setup names the research question and the interview style (jobs-to-be-done,
   journey walkthrough, concept reaction).
2. Interview each persona separately, sequential not parallel: 5-8 questions, following
   up on surprises instead of marching through a script. In journey mode, walk one
   scenario end to end and capture friction at each step.
3. Personas answer from their definition (pains, triggers, decision criteria), including
   "I don't care about that," which is often the finding.
4. Synthesis across personas: themes, disagreements between personas, and implications.

**Output:** per-persona transcript excerpts + synthesis. **Every artifact is labeled
"Simulated personas, not real user research"** at the top, and quotes are attributed to
the persona name, never formatted like verbatim customer quotes.

**Failure mode:** the interviewer leading the witness. If every answer confirms the
product thesis, rerun with the skeptical follow-ups the persona's scar tissue implies.
Simulated research validates framing and question guides; it never substitutes for real
users in a decision that needs them. Say so in the synthesis when that line is near.

---

## 5. board-session

**Use for:** decision guidance and mentorship from a standing advisory board: strategy
calls, career decisions, "am I thinking about this right."

**Roles:** 3-5 advisors with distinct lenses, one chair (an advisor or the orchestrating
model), the user as the executive bringing the question.

**Choreography:**
1. **Agenda:** the user brings one question plus a short brief (the charter says what
   format). Chair restates the question sharply; if it's actually three questions, the
   chair says so and the user picks one. Sharpening includes timing: if the decision
   isn't live yet (no offer in hand, no bid received), reframe to the decision that IS
   live, usually "what is X actually worth" and "how hard to pursue Y now."
2. **Positions:** every advisor takes an independent position in parallel: their
   recommendation, top reasoning, and the single assumption they're least sure of.
3. **Cross-examination:** chair identifies the 2-3 genuine disagreements and runs one
   targeted round: each advisor responds to the strongest opposing argument quoted to
   them, not to a summary of it.
4. **Chair synthesis:** the board's guidance, the dissent (named advisor, preserved in
   their words), what new information would change the answer, and a suggested next
   action sized to a week.
5. The user decides. The board advises; it never votes on their behalf.

**Output:** positions, disagreement map, chair synthesis with preserved dissent,
one-week next action.

**Failure mode:** the board becoming a cheering section. Every session, at least one
advisor must argue against the direction the user is leaning; if none naturally does,
the chair assigns the strongest counter-case to the advisor best equipped to make it,
labels it as assigned, and requires it to end with a falsifiable test: the specific
evidence, on a deadline, that would prove the counter-case right. In live runs the
assigned counter-case is routinely the session's most actionable output, precisely
because it converts a vague "but what if you stayed/held/waited" into a checkable bet.
