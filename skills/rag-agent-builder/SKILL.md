---
name: rag-agent-builder
description: Build and maintain a retrieval-grounded knowledge agent from product documentation: design the corpus, split oversized sources into retrievable parts, scan for redaction and voice problems, prove after upload that the agent can actually read every part, and run an evaluation set before sharing it. Use when the user says "build a knowledge agent", "the agent gives confident wrong answers", "split this corpus", or "rag-agent-builder". Works on any RAG platform via a profile in platforms/. Do NOT use for querying an agent that already works, or for writing the source documentation itself; run /tech-writer on that.
aliases:
  - rab
---

# RAG agent builder

Builds a document corpus an agent can actually read, and keeps it correct across releases.

Product-agnostic and platform-agnostic. What is specific to your product lives in
`project.yaml` and three pattern files; what is specific to your platform lives in a profile
under `platforms/`. Nothing in this skill is specific to either.

Examples throughout use Coppermine Systems, a fictional B2B device-management company.
`scripts/check-markers.sh` enforces that, and enforces that mechanism files carry rules rather
than orphaned specifics.

## Quick start

```
/rag-agent-builder init <product>    scaffold a new corpus project
/rag-agent-builder build             assemble and split the corpus from project.yaml
/rag-agent-builder scan              redaction and voice gates over the staged files
/rag-agent-builder verify            after upload: prove every part is retrievable
/rag-agent-builder eval              run the eval set against the live agent
/rag-agent-builder check             drift report: what has gone stale
/rag-agent-builder sync <release>    a full release pass
```

## The invariant

**Every part of every source must be retrievable.**

That is the whole job. What it costs you is a platform question, which is why the number lives
in a profile rather than in this file. On a platform that chunks invisibly and lets an agent
read only the first chunk, it costs a ceiling small enough that each file is one chunk. On a
platform that does not chunk, it may cost nothing.

The failure mode is the same everywhere and it is why this matters: **an unreachable section
does not produce a refusal, it produces a confident wrong answer with a citation**, because
retrieval falls through to whatever smaller file mentions the topic.

Pick a profile in `platforms/` and set `platform:` in `project.yaml`. `generic` assumes nothing
and is the right choice until you have measured yours. Read `references/corpus-design.md` before
writing or restructuring any document.

## Read first

| Source | Path | What to extract |
|---|---|---|
| Platform profile | `platforms/<your platform>.md` | The ceiling, which verify to run, and what fails silently there |
| Corpus design | `references/corpus-design.md` | Structure, the part header, voice rules, negative claims |
| Field notes | `references/field-notes.md` | The incident behind each rule, when you need the why |
| Project config | `project.yaml` (user-filled) | Every document in the corpus, the product sentence, the version line |
| Pattern files | `redaction-*.yaml`, `voice-patterns.yaml` (user-filled) | What must never reach the index, and what reads wrong when quoted |
| Manifest | `source-manifest.md` (user-filled) | Per-document provenance and the Supersedes-if that makes it stale |

No project yet: run `init` and fill `project.yaml` and the redaction files before anything else.

## Mode: `init <product>`

Scaffold a project. Copies from `templates/`:

- `project.yaml`, the corpus definition. Every document is a row, so the config is the build
- `redaction-patterns.yaml`, what must never reach the index. **Fill this in; it ships with
  shapes, not your facts**
- `voice-patterns.yaml`, prose that reads wrong when quoted to a customer. Generic, usable as-is
- `source-manifest.md`, provenance and staleness conditions per document
- `eval-set.md`, five blocks with the gate defined

Then: point `project.yaml` at your sources, write the product sentence and version line, and
fill in the redaction patterns. Nothing else needs editing to get a first build.

## Mode: `build`

```
python3 scripts/build.py --config project.yaml --out staging/<date>/files
```

Reads `project.yaml` and produces every document's parts. Three document kinds:

| kind | input | what happens |
|---|---|---|
| `split` | assembled markdown or text | cut at heading boundaries, sub-split when a section is oversize |
| `pdf` | a PDF | converted first, headings rebuilt from the PDF's own bookmark tree, then split |
| `openapi` | a bundled spec plus fragments | projected from the spec, self-checked, then emitted as parts |

Redaction substitutions apply to **every** document whatever its source format, so a guide is
not left unredacted because it happened to arrive as markdown. Generated documents are
additionally held to the same scan patterns that gate the upload, so the build and the gate
cannot drift apart.

**Run it twice and diff. The builders are deterministic and the second run must change
nothing.** If it does, something is reading the clock or the filesystem order.

Individual tools are usable directly when you need them: `split_corpus_file.py`,
`pdf_to_markdown.py`, `build_api_corpus.py`.

## Mode: `scan`

```
python3 scripts/scan.py --patterns redaction-patterns.yaml --path staging/<date>/files
python3 scripts/scan.py --patterns voice-patterns.yaml     --path staging/<date>/files
```

Both gate the upload. Nothing stages until both come back clean or every match has been read
and recorded as a known false positive.

**A match is a reading list, not a verdict.** A pattern written to catch a claim also matches
the document that denies it. Read every hit.

They also miss things. Case, spacing and word order all defeat a pattern that looked fine when
it was written, and a miss looks exactly like a pass. See `references/field-notes.md`.

## Mode: `verify`

**The gate. Run it after every upload, before any eval.** Which check you run comes from the
profile.

**Generic, works anywhere** — measures retrieval directly rather than inferring it:

```
python3 scripts/reach_probe.py --emit  --parts staging/<date>/files --out probes.json
# ask the agent each question, save the replies
python3 scripts/reach_probe.py --score --probes probes.json --answers answers.json
```

Each probe asks for a string from the **tail** of a part, because the tail is what a truncating
or first-chunk-only platform loses first.

**Where the platform exposes chunk metadata** there is a faster path:

```
python3 scripts/check-chunk-counts.py --record agent.json
```

Every attached file must report `total_chunks == 1`. The script's docstring carries the browser
snippet that exports the record, and it takes byte counts rather than bodies so the export stays
small.

Run both where both work. A disagreement between them is worth more than either result, because
it means one of the two is measuring something other than what you think.

Do not use file size as a proxy for either. It measures a different thing, and that substitution
is what lets this problem run undetected.

## Mode: `eval`

Drive the published agent and score `eval-set.md`.

**Bundle three or four questions per message**, the way a person actually asks. Single-question
testing scores a pass on failures that only appear under bundling: a known absence that answers
correctly alone can degrade to "I can't confirm either way" when asked alongside two others,
which is worse than a refusal because it implies the thing might be true.

Write the scorecard to a date-stamped file and never overwrite one.

The voice block is the one most people skip and the one that catches the most. It is the only
block that tests what the agent volunteers rather than what it knows.

## Mode: `check`

Read-only drift report. For every document, evaluate its Supersedes-if condition from the
manifest and report what has gone stale.

**Report negative-claim drift first and separately.** A stale document degrades one answer; a
stale absence reverses one. An agent that confidently says a capability does not exist, on the
day it ships, is the worst failure this system produces.

## Mode: `sync <release>`

A full pass, in order:

1. **Establish the new version facts** and update the version-authority file.
2. **Recompute negative claims.** Three states: still true, now false, partially addressed.
   Anything in "now false" blocks the sync until its document, its curated answer and its eval
   question are all updated.
3. **Triage the corpus** against Supersedes-if. Convert and scan anything new.
4. **Rebuild** with `build`, then `scan`.
5. **Re-author affected curated answers.** A claim that flipped from absence to shipping gets
   its answer replaced, not edited, so no fragment of the old absence survives.
6. **Grow the eval set**, and move anything that flipped from the must-refuse block to the
   must-answer block. That move is the proof step 2 actually happened.
7. **Upload, `verify`, then `eval`.** Update the manifest and the state file.

## Worked example (fictional)

Coppermine Systems, standing up an agent on the CM-900 console server and the Fleet Cloud
platform. Sources: two user guides as PDFs, a 435KB platform guide in markdown, and a bundled
OpenAPI spec.

`init` scaffolds, `project.yaml` gets four document rows, `build` produces 38 parts. The one
that matters is what `verify` does next:

> ```
> $ python3 scripts/check-chunk-counts.py --record agent.json
> FAIL  CM-900-User-Guide-07.md
>       14 chunks, about 7% reachable
> ```

The build had been passing all along. The upload had succeeded, the file was listed, and
workspace search returned passages from deep inside it. Every signal available in the product
said the corpus was healthy, and the agent was answering firmware questions from a stale example
value in the API spec because the chapter holding the real answer was out of reach.

That is the shape of every failure this skill is built around: not a refusal, a confident wrong
answer with a citation. `references/field-notes.md` has the rest of them.

## Standing rules

- **Stage, don't apply.** Nothing reaches the live agent without the owner's sign-off.
- **Shipping capability only.** Untagged builds, unreleased features and roadmap items never
  enter a corpus. Absence of a feature is not a statement about when it arrives.
- **Every new file gets the full redaction pass**, with no exceptions for "it's just a
  datasheet". The files most likely to carry a credential are the ones that arrived in a format
  your scanner never ran over. See `references/field-notes.md`.
- **Never edit a generated part.** Edit the config or the source and re-run.
- **Fix contradictions at source.** Once retrieval works, an agent that finds two sources
  disagreeing narrates the conflict to a customer. A synthesis layer cannot paper over it.
- **Verify the curated-answer layer actually reaches the agent** before relying on it. Ask the
  agent the verbatim title of an answer whose content is in no document. If it cannot answer,
  that layer is inert and every fact has to live in a document instead.

## Write path

This skill prepares everything locally and ends with a manual upload checklist, because the
platform API token is Enterprise-gated and may not be available.

The read path is deliberately separable: `check-chunk-counts.py` takes a record file today and
needs only a different fetch to take a token. If a token appears, it enables scripted file and
answer updates. Agent configuration stays browser-driven either way, since the published
Agents API is read-only.

## Exit checklist

Before handing the corpus over, verify:

- [ ] Every staged file is at or under the ceiling
- [ ] Both scans clean, or every match read and recorded
- [ ] The build is idempotent: run twice, no diff
- [ ] Byte total of parts equals the source minus what was deliberately dropped
- [ ] Three parts from different documents read as self-sufficient
- [ ] After upload, every part is reachable to its tail (`reach_probe.py`, and chunk counts
      where the platform has them)
- [ ] `scripts/check-markers.sh` clean, if this skill itself was edited
- [ ] Eval gate met before the agent is shared
- [ ] Manifest has a row, a pin and a Supersedes-if for every live file
- [ ] Nothing unreleased entered the corpus

## References

- `platforms/`, one profile per platform. `gosearch.md` is measured, `generic.md` assumes
  nothing, `profile-template.md` is how to add a third
- `references/corpus-design.md`, structure, the part header, voice, and negative claims
- `references/field-notes.md`, the incidents each rule came from
