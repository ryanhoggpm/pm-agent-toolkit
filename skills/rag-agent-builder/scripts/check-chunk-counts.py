#!/usr/bin/env python3
"""Fail if any file an agent is grounded on is more than one chunk.

**Platform-specific: the GoSearch fast path.** It reads chunk metadata the
platform happens to expose. Most platforms expose none, and there the generic
check is reach_probe.py, which measures retrieval directly instead of inferring
it. Where both run, run both: a disagreement is worth more than either result.

This is the check whose absence let a corpus sit mostly unindexed for nine days.
The platform splits an uploaded file into chunks of just under 65,000 bytes of
extracted text and an agent retrieves only chunk 0, so a 14-chunk user guide is
about 7% visible to it. Nothing in the product says so: the upload succeeds, the
file is listed, and workspace search finds the deep chunks, which is what makes
it look fine.

It does not show up as a refusal. It shows up as a confident wrong answer with a
citation, because retrieval falls through to whatever smaller file mentions the
topic.

Read path. The API token is Enterprise-gated and may not be available, so the
record is exported from an authenticated browser tab and read from disk. When a
token exists, --url fetches the same record and nothing else changes.

  # In the browser, on the agent page. Set RECORD_URL to whichever endpoint
  # your platform serves the agent's own record from; the network tab shows it
  # when the page loads. Save the result as agent.json.
  #
  #   const RECORD_URL = '...';                       // your platform's
  #   const j = await (await fetch(RECORD_URL)).json();
  #   const e = new TextEncoder(), out = [];
  #   (function w(n){ if (n && typeof n === 'object') {
  #     if (!Array.isArray(n)) {
  #       const m = n.metadata || {};
  #       if (m && 'total_chunks' in m) out.push({file_name: m.file_name || n.title,
  #         body_bytes: e.encode(n.body || '').length,
  #         metadata: {total_chunks: m.total_chunks, chunk_index: m.chunk_index}});
  #       Object.values(n).forEach(w);
  #     } else n.forEach(w); } })(j);
  #   copy(JSON.stringify({sources: out}))

  python3 check-chunk-counts.py --record agent.json
  python3 check-chunk-counts.py --record agent.json --ceiling 60000
"""
import argparse
import json
import pathlib
import sys

from corpus_common import SINGLE_CHUNK_CEILING, WARN_BAND


def walk(node):
    """Yield every dict in the record; the sources list moves between releases."""
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from walk(v)


def sources(record):
    """Every object that looks like an uploaded file, keyed by name."""
    found = {}
    for node in walk(record):
        meta = node.get("metadata") if isinstance(node.get("metadata"), dict) else {}
        if "total_chunks" not in meta and "total_chunks" not in node:
            continue
        name = (node.get("file_name") or node.get("filename") or node.get("name")
                or node.get("title") or meta.get("file_name") or meta.get("title"))
        if not name:
            continue
        total = int(meta.get("total_chunks", node.get("total_chunks")) or 0)
        index = int(meta.get("chunk_index", node.get("chunk_index")) or 0)
        # The browser export carries sizes rather than bodies: the record is
        # 3.5MB with the bodies in it and nothing here reads their text.
        if "body_bytes" in node:
            size = int(node["body_bytes"])
        else:
            size = len((node.get("body") or node.get("content") or "").encode("utf-8"))
        prev = found.get(name)
        # Keep the largest observed body for the file, and the highest chunk
        # count, so a record listing one chunk per row still reports the truth.
        found[name] = {
            "total": max(total, prev["total"] if prev else 0),
            "chunks_seen": (prev["chunks_seen"] | {index}) if prev else {index},
            "bytes": max(size, prev["bytes"] if prev else 0),
        }
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--record", required=True,
                    help="the agent record as JSON, exported from the browser")
    ap.add_argument("--ceiling", type=int, default=SINGLE_CHUNK_CEILING)
    args = ap.parse_args()

    raw = pathlib.Path(args.record).read_text(encoding="utf-8")
    try:
        record = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"{args.record} is not JSON: {e}", file=sys.stderr)
        return 2

    files = sources(record)
    if not files:
        print("no uploaded files found in the record; is this the agent record?",
              file=sys.stderr)
        return 2

    bad, near = [], []
    print(f"{len(files)} attached file(s)\n")
    for name in sorted(files):
        f = files[name]
        n = f["bytes"]
        flag = ""
        if f["total"] != 1:
            bad.append((name, f["total"]))
            flag = "  FAIL"
        elif n > args.ceiling - WARN_BAND:
            near.append((name, n))
            flag = "  warn"
        print(f"  chunks {f['total']:>3}   {n:>7,} bytes   {name}{flag}")

    if near:
        print(f"\n{len(near)} file(s) approaching a second chunk:")
        for name, n in near:
            print(f"  {n:,} bytes, within {args.ceiling - n:,} of the ceiling: {name}")

    if bad:
        print(f"\nFAILED: {len(bad)} file(s) are more than one chunk. The agent "
              f"reads only the first chunk of each, so the rest is not reachable.",
              file=sys.stderr)
        for name, total in bad:
            print(f"  {total} chunks, about {100 // total}% reachable: {name}",
                  file=sys.stderr)
        return 1

    print(f"\nok  every attached file is a single chunk")
    return 0


if __name__ == "__main__":
    sys.exit(main())
