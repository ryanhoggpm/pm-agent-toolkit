# Platform profile: GoSearch

Established empirically in September 2026 against an Enterprise workspace. GoSearch publishes
no guidance on source-document structure, length or splitting, so everything below was
measured rather than read.

Re-measure before trusting these numbers on a different tenant or after a platform release.

Selected with `platform: gosearch` in `project.yaml`.

## Capabilities

The table every profile answers. "Measured" means someone ran it here; the rest is the vendor's
claim, which is a different kind of fact.

| | | |
|---|---|---|
| Ceiling | **60,000 bytes of extracted text** | Measured. Load-bearing: over it, the file is partly unreachable |
| Verify | `check-chunk-counts.py`, then the reach probe | Measured. Chunk counts are the fast path here and exist on few platforms |
| Who chunks | The platform, invisibly, at just under 65,000 bytes | Measured |
| Chunks an agent reads | **Chunk 0 only** | Measured. The defect the ceiling exists to route around |
| Native upload formats | PDF, DOCX, XLSX, PPTX, plain text, CSV | Vendor. Markdown is absent and is taken as `text/plain` |
| Override layer | Curated Answers | Vendor says it beats retrieval. **Measured as not reaching the agent.** See below |
| Glossary | Separate store, `include_glossary` flag | Measured working |
| API write path | Enterprise-gated token | Not available here |
| Native skills | Agent Skills format, markdown or `.zip` | Vendor. Instructions only, no execution. Creation untested here |
| Admin levers | Verify, deprecate | Vendor. Both admin-gated |

## Chunking

- GoSearch splits an uploaded file into chunks of just under **65,000 bytes of extracted
  text**. Largest single chunk observed: 64,999. Smallest file that became two chunks: 67,150.
- **Extracted text, not file bytes.** An 80,737-byte HTML file extracted to 50,707 bytes and
  stayed one chunk. For markdown the two are equal.
- Per-chunk metadata is inspectable: `chunk_index`, `total_chunks`, `base_unique_id`.
- **All chunks are indexed.** Workspace search reaches chunk 4 of 7, 12 of 14 and 13 of 16.

## The agent reach problem

**An agent retrieves only chunk 0 of a file.** Agents carry a `useChunkSearch` flag which was
false on every agent in the tenant, with no control for it in the agent editor.

A 435KB document is 7 chunks and the agent reads one of them. That is roughly 15% coverage.

**It fails as a confident wrong answer, not as a refusal.** With the authoritative section
unreachable, retrieval falls through to whatever smaller file mentions the topic. The measured
case: a question about script interpreter versions answered from a stale example value inside
an API specification, because the user guide chunk holding the right answer was out of reach.

**Adopted ceiling: 60,000 bytes of extracted text.** At that size a file is one chunk, so
chunk 0 is the whole file and coverage is complete regardless of the flag. The margin below
the boundary lets a release add content without silently crossing it.

## Verification

Do not use file size as a proxy for reach. It measures a different thing.

`scripts/check-chunk-counts.py` reads `total_chunks` per file from the agent's own record and
fails on anything that is not 1. Run it after every upload and before every eval. An eval over
a partly-indexed corpus measures the layer that works and says nothing about the layer that
does not. An eval can pass repeatedly while most of the product documentation is unreachable.

## Upload formats

Documented: PDF, DOCX, XLSX, PPTX, plain text, CSV. **Markdown is not on the list.** It is
accepted as `text/plain`, which means there is no documented basis for expecting heading-aware
chunking. Headings may be improving readability only.

The documented 80MB per-file upload limit measures upload acceptance, not indexed reach.

## Curated Answers

Documented as taking precedence over retrieval, which makes them the obvious home for a fact
that must beat whatever search turns up.

**Verify they actually reach your agent before relying on them.** In the tenant measured here, with
`include_answers: 1` set, they did not. Asked the verbatim title of an Answer, the agent said
it had no source on that subject, and no Answer was cited across a full eval run. The glossary,
set by the adjacent flag, did work.

The one-minute test: ask the agent the exact title of an Answer whose content appears nowhere
in your documents. If it cannot answer, the layer is not reaching it.

## Ranking levers

Verify and deprecate are the only documented levers for influencing which source wins. Both
are admin-gated. Without them the only remedy for a source producing wrong answers is deleting
it.

## Reading the agent's own record

Chunk counts come from the agent's record, which an authenticated browser session can read.
`scripts/check-chunk-counts.py` carries the export snippet in its docstring and takes byte counts
rather than bodies, so the export stays small.

**Draft ids change on every save.** Whatever id you capture, never record a draft id as a stable
identifier; agents carry a separate id that survives edits.

The published Agents API is read-only. An Enterprise API token additionally unlocks a files
endpoint for chunk counts and a documents endpoint for pushing pre-split content at a documented
16,384 characters per document, which is the one place a caller controls splitting instead of
relying on the platform's own chunker.

## What to raise with an admin

1. Whether `useChunkSearch` can be enabled. It affects every agent in the tenant and no owner
   can see the problem from the UI.
2. Whether `include_answers` is wired to agent retrieval.
3. An API token, so chunk counts can be verified without driving a browser.
4. Verify and deprecate rights.
