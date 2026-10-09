# Source manifest: <Agent name>

Provenance for every file in the corpus. **<N> attached sources.**

A sidecar rather than front matter in the documents themselves, for two reasons: part of a
corpus is usually PDF or spreadsheet that cannot carry front matter, and YAML inside an
uploaded markdown file is content the agent can read aloud.

**Supersedes-if** is the load-bearing column. It is the condition that makes a file stale,
written so a check run can evaluate it rather than a human having to judge it.

## How to read this file

Generated parts are listed **one row per document, not one per part**. A part has no
independent provenance: it is an output of a build. `project.yaml` plus `scripts/build.py` is
the build.

**Every attached file must be a single chunk.** `scripts/check-chunk-counts.py` is the gate and
runs after every upload, before any eval.

## Authored layer (edit these directly)

| File | Pinned to | Verified | Supersedes-if | Claims depending on it |
|---|---|---|---|---|
| | | | | |

## Generated part-sets (never edit a part; re-run the build)

| Document | Parts | Generator input | Verified | Supersedes-if |
|---|---|---|---|---|
| | | | | |

## Standalone files

| File | Pinned to | Verified | Supersedes-if | Notes |
|---|---|---|---|---|
| | | | | |

## Agent configuration (browser-only, mirrored locally)

| Surface | Mirrored to | Verified | Supersedes-if |
|---|---|---|---|
| Agent instructions | `live-mirror/instructions.md` | | |
| Conversation starters | `live-mirror/conversation-starters.md` | | |

Neither is retrievable as a source, so imperatives and guardrail lists are correct there and
are exempt from the voice scan.

## Curated answers

Not files, so not listed individually. **They override retrieval where the platform supports
it, which makes a stale one worse than a stale PDF.** Verify they are actually reaching the
agent before relying on them: ask the agent the verbatim title of one and see whether it
knows.

## Not uploaded, deliberately

| File | Why |
|---|---|
| | |

## Open drift

## Closed this cycle
