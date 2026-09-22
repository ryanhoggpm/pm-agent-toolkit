# Field notes

Every rule in this skill came from something going wrong. The rules live in `SKILL.md` and
`corpus-design.md` and are stated flatly there, because a rule carrying its own anecdote is
harder to read and harder to apply.

The anecdotes live here.

**All examples use Coppermine Systems**, a fictional B2B device-management company: the CM-900
console server, the older CM-400, the Fleet Cloud platform, and Ironvine, a competitor. The
incidents are real, the names are not. This is the only file in the skill allowed to carry a
specific number or a proper noun, and `scripts/check-markers.sh` enforces that.

---

## Example (fictional): the guide the agent could not read

Coppermine stood up an agent on its product documentation. The eval passed, repeatedly, so the
agent went to a pilot group.

Asked which scripting-language versions the CM-900 supports, it answered with a version two
major releases newer than the firmware ships, and cited a source.

The CM-900 user guide is 849,110 bytes. The platform had split it into 14 chunks and the agent
read the first one. The chapter with the right answer was chunk 12. With it unreachable,
retrieval fell through to the Fleet Cloud API specification, which carried
`description: module version example: 3.13.2` inside a schema. An example value, read as a
statement of fact, because nothing in the flattened text marked it as an example.

**What made it survive nine days:** the upload succeeded, the file was listed, and workspace
search found the deep chunks. Every visible signal said the corpus was fine. The verification
that had been run measured the documented 80MB upload limit, which is a fact about acceptance
and not about retrieval.

**Rules from this one:** the invariant, the ceiling, `verify` before `eval`, and never using
file size as a proxy for reach.

## Example (fictional): the agent copied its documents' register, not its instructions

Coppermine's agent instructions forbade, explicitly and at length: naming another document as
wrong, addressing the reader with an imperative, and appending unrelated limitations.

The agent did all three, in front of customers.

The cause was in the sources. One synthesis document opened *"This document exists because the
same question has been answered several different ways across our material."* Another said
*"Do not cross the two tool counts."* The agent reproduced both patterns nearly verbatim in its
answers.

Rewriting those documents fixed it. The instructions were never changed.

**The rule:** the example in the retrieved text beats the abstract instruction. Assume anything
a source document models, the agent will do.

## Example (fictional): the prohibition that kept the wrong number alive

Coppermine's CM-400 once carried a security certificate that the CM-900 does not. Old marketing
cited the old certificate number.

The instructions said: *"Never cite certificate #5103."*

Once the corpus itself was clean, that line was the only remaining source of `#5103` anywhere
the agent could see. It began pre-emptively explaining, unprompted, why that certificate did not
apply — raising a number no one had asked about and that no longer existed in any document.

**The rule:** prohibitions describe the class, not the literal. State the correct certificate
once, in the document that owns the topic, and say nothing about the old one.

## Example (fictional): the grep that proved the wrong thing

A landing page claimed the Fleet Cloud integration exposed 33 tools. The real number was 38; the
33 belonged to a different integration.

Told to find where the wrong count came from, the first search used a lowercase pattern and
matched nothing but CSS colour values. The conclusion drawn was that the agent had invented the
number. It had not. The page carried `<h2>33 Tools. One Connection.</h2>` and the pattern missed
it on case alone.

**Two rules:** a scan misses things, so case, spacing and word order all defeat a pattern that
looked fine when it was written. And an agent stating an odd specific is usually reading it
somewhere. Find the source before concluding it hallucinated.

## Example (fictional): the pattern that matched the document denying it

The redaction scan carried a pattern for device fingerprinting, on the grounds that the CM-900
does not do it and marketing occasionally implied otherwise.

It fired on the one document that says plainly there is no fingerprinting.

**The rule:** a match is a reading list, not a verdict. Read every hit.

## Example (fictional): the password nobody had scanned

The CM-400 and CM-900 guides arrived as PDFs and went into the corpus as PDFs, so the redaction
scan, which ran over markdown, had never seen either of them.

Converted for splitting, they turned out to print a working gateway root password twice each.

**The rule:** redaction applies to every document whatever format it arrived in. A guide left
unredacted because it happened to be a PDF is the copy that gets quoted.

## Example (fictional): the override layer that was not there

Coppermine's platform documents a curated-answers layer that takes precedence over retrieval,
so several facts that had to beat whatever search returned were put there instead of into
documents.

Asked the verbatim title of one of those answers, the agent said it had no source on that
subject. No curated answer was cited anywhere across a full eval run. The flag that was supposed
to enable them was set. The adjacent glossary flag worked fine.

Seventeen answers were unreachable, including three written specifically to scope a question
that the corpus could not resolve on its own.

**The rule:** verify the override layer reaches the agent before relying on it. The test takes a
minute: ask for the verbatim title of an entry whose content is in no document.

## Example (fictional): the contradictions that only surfaced once retrieval worked

With the corpus reachable, the agent began reconciling its sources out loud in front of
customers. Every instance was a real contradiction nobody had known about:

- a heading stating one count while the same page stated another
- a total that did not equal the sum of its parts
- a superseded figure still live in three places
- schema example values read as fact

**Two rules:** fix contradictions at source, because no synthesis layer stops the narration while
the corpus disagrees with itself. And expect to find them late, because they cannot surface
until everything is reachable.

## Example (fictional): the refusal that degraded under bundling

Asked on its own whether Fleet Cloud held a particular compliance attestation, the agent said no,
flatly and correctly.

Asked alongside two questions it legitimately could not answer, the same question came back as
*"I can't confirm this from my sources."*

That is worse than a refusal. It implies the thing might be true.

**The rule:** bundle three or four questions per message when running an eval, the way a person
actually asks. Single-question testing scores a pass on this failure.

## Example (fictional): the document that passed every pattern and still did not belong

A partner-facing explainer passed the redaction scan and passed the voice scan. It was also,
start to finish, instructions to a seller: where Coppermine wins against Ironvine, how to open
the conversation, which objection to expect.

No pattern catches that, because the problem is the genre rather than any phrase in it.

**The rule:** enablement material is the specific trap. If a document's own first line describes
it as guidance rather than documentation, that is your answer. Keep the facts, drop the plays.
