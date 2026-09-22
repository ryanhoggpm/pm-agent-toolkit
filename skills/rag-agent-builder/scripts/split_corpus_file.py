#!/usr/bin/env python3
"""Split an existing corpus markdown file into single-chunk parts.

For documents that are already assembled and have no generator behind them.
The file is cut only at heading boundaries, and sections are packed into parts
under the ceiling. A section larger than the ceiling is cut at the next heading
level down, as far as --max-level, and each piece after the first repeats its
parent heading so the text still says which chapter it belongs to.

If a section is still too large at --max-level the split fails rather than
cutting mid-section, because a part that begins halfway through a procedure is
worse than a part that is too big.

  python3 split_corpus_file.py --in FILE --out DIR \
      --title "Command Reference" \
      --product-sentence "..." --areas "..." [--level 1] [--max-level 3] \
      [--promote 'REGEX']
"""
import argparse
import pathlib
import re
import sys

import yaml

from corpus_common import (SINGLE_CHUNK_CEILING, WARN_BAND, join_areas, render_part_header,
                           report)


def split_sections(text, level):
    """[(heading_or_None, block_text)] cut at ATX headings of `level`, fences respected."""
    marker = "#" * level + " "
    out, cur_head, buf, fence = [], None, [], False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fence = not fence
        if not fence and line.startswith(marker):
            if buf or cur_head is not None:
                out.append((cur_head, "\n".join(buf).rstrip()))
            cur_head, buf = line[len(marker):].strip(), [line]
            continue
        buf.append(line)
    out.append((cur_head, "\n".join(buf).rstrip()))
    return [(h, b) for h, b in out if b.strip()]


def collect(text, level, max_level, budget, parent=None):
    """[(parent_label, heading, body)] with any oversize section cut finer.

    A chapter too big for one part is divided at the next heading level. Every
    piece but the first loses the chapter heading that opened the chapter, so
    the heading is repeated above it: a retrieved part that starts at "IP
    Filter" with no sign it belongs to Networking is hard to place.
    """
    out = []
    for head, body in split_sections(text, level):
        if len(body.encode("utf-8")) <= budget or level >= max_level:
            out.append((parent, head, body))
            continue
        label = head or parent
        pieces = collect(body, level + 1, max_level, budget, parent=label)
        for i, (gp, sub_head, sub_body) in enumerate(pieces):
            if i and label:
                sub_body = f"{'#' * level} {label}, continued\n\n{sub_body}"
            out.append((gp or label, sub_head, sub_body))
    return out


def _name(label):
    """'10: Device Ports' reads as a stray number mid-sentence; say chapter."""
    m = re.match(r"^(\d+):\s+(.+)$", label)
    return f"chapter {m.group(1)}, {m.group(2)}" if m else label


def describe(group):
    """Readable 'this part covers' phrase for a packed group of sections."""
    runs = []
    for parent, head, _ in group:
        name = head or parent
        if not name:
            continue
        if parent and head and head != parent:
            if runs and runs[-1][0] == parent:
                runs[-1][1].append(head)
            else:
                runs.append((parent, [head]))
        else:
            runs.append((None, [name]))
    out = []
    for parent, heads in runs:
        out.append(f"{_name(parent)} ({join_areas(heads)})" if parent else _name(heads[0]))
    return out


def _greedy(sections, budget):
    parts, cur, cur_n = [], [], 0
    for section in sections:
        n = len(section[-1].encode("utf-8")) + 2
        if cur and cur_n + n > budget:
            parts.append(cur)
            cur, cur_n = [], 0
        cur.append(section)
        cur_n += n
    if cur:
        parts.append(cur)
    return parts


def _size(part):
    return sum(len(s[-1].encode("utf-8")) + 2 for s in part)


def _balanced(sections, count, hi):
    """Smallest budget that still packs into `count` parts or fewer."""
    lo = max(len(s[-1].encode("utf-8")) + 2 for s in sections)
    while lo < hi:
        mid = (lo + hi) // 2
        if len(_greedy(sections, mid)) <= count:
            hi = mid
        else:
            lo = mid + 1
    return _greedy(sections, lo)


def pack(sections, budget, soft=None):
    """Order-preserving, balanced, and kept clear of the ceiling.

    Greedy packing fills the first part to the ceiling and leaves the last one
    nearly empty. Packing into the fewest parts the ceiling allows has a quieter
    version of the same problem: the parts come out even, but even means every
    one of them sits just under the limit, so the next release that adds a page
    splits the document all over again. Parts are cheap, so spend them until the
    largest one clears `soft`.
    """
    soft = budget if soft is None else soft
    floor = max(len(s[-1].encode("utf-8")) + 2 for s in sections)
    target = max(soft, floor)
    fewest = len(_greedy(sections, budget))
    for count in range(fewest, fewest + 10):
        trial = _balanced(sections, count, budget)
        if max(_size(p) for p in trial) <= target:
            return trial
    return _balanced(sections, fewest, budget)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", required=True, help="document name, without a part number")
    ap.add_argument("--product-sentence", required=True)
    ap.add_argument("--areas", required=True,
                    help="one phrase describing what the whole document covers")
    ap.add_argument("--version-line", default="")
    ap.add_argument("--note", default="",
                    help="extra sentence for every part header, e.g. what was left out")
    ap.add_argument("--start-at", default=None,
                    help="regex; drop everything before the first line that matches")
    ap.add_argument("--drop-section", default=None,
                    help="regex; drop any --level section whose heading matches")
    ap.add_argument("--level", type=int, default=1)
    ap.add_argument("--max-level", type=int, default=None,
                    help="deepest heading level to cut at when a section is oversize")
    ap.add_argument("--promote", default=None,
                    help="regex for plain lines to turn into level-N headings first")
    ap.add_argument("--promote-to", type=int, default=2)
    ap.add_argument("--slug", required=True)
    ap.add_argument("--redactions", default=None,
                    help="YAML holding a `redactions` list of {re, to}")
    ap.add_argument("--ceiling", type=int, default=SINGLE_CHUNK_CEILING)
    ap.add_argument("--header-budget", type=int, default=1100)
    args = ap.parse_args()

    text = pathlib.Path(args.src).read_text(encoding="utf-8")
    src_total = len(text.encode("utf-8"))

    # Applied before anything is cut, so every part of every document gets the
    # same treatment. A guide that is redacted only because it happened to
    # arrive as a PDF is the kind of inconsistency nobody notices until the
    # unredacted one is the source that gets quoted.
    if args.redactions:
        rules = yaml.safe_load(pathlib.Path(args.redactions).read_text())["redactions"]
        n = 0
        for r in rules:
            text, k = re.subn(r["re"], r["to"], text)
            n += k
        print(f"  {n} redactions applied")

    # Front matter is a cover page, a table of contents and lists of figures and
    # tables. As flat text it is a few thousand bytes of page numbers that
    # retrieve against almost any query.
    if args.start_at:
        m = re.search(args.start_at, text, re.M)
        if not m:
            print(f"--start-at matched nothing: {args.start_at!r}", file=sys.stderr)
            return 1
        text = text[m.start():]

    if args.promote:
        rx = re.compile(args.promote)
        hashes = "#" * args.promote_to
        out, fence = [], False
        for line in text.split("\n"):
            if line.lstrip().startswith("```"):
                fence = not fence
            if not fence and not line.startswith("#") and rx.match(line.strip()):
                line = f"{hashes} {line.strip()}"
            out.append(line)
        text = "\n".join(out)

    budget = args.ceiling - args.header_budget
    # Sections are cut down to the soft target, not the hard ceiling. A chapter
    # that merely fits leaves the packer nothing to work with: one 57KB section
    # sets the floor for the whole document and drags every part into the warn
    # band with it. Cutting at the soft target costs nothing when the chapter
    # would have fitted anyway, because the packer puts the pieces back together.
    soft = args.ceiling - WARN_BAND - args.header_budget
    max_level = args.max_level if args.max_level is not None else args.level
    if args.drop_section:
        rx = re.compile(args.drop_section)
        kept, dropped = [], []
        for head, body in split_sections(text, args.level):
            (dropped if head and rx.search(head) else kept).append((head, body))
        if not dropped:
            print(f"--drop-section matched nothing: {args.drop_section!r}", file=sys.stderr)
            return 1
        for head, body in dropped:
            print(f"  dropped {len(body.encode('utf-8')):,} bytes  {head!r}")
        text = "\n\n".join(b for _, b in kept)

    sections = collect(text, args.level, max_level, soft)
    oversize = [(p_, h, len(b.encode("utf-8"))) for p_, h, b in sections
                if len(b.encode("utf-8")) > budget]
    if oversize:
        print(f"a section is still oversize at level {max_level}; raise --max-level:",
              file=sys.stderr)
        for p_, h, n in oversize:
            print(f"  {n:,} bytes  {p_!r} / {h!r}", file=sys.stderr)
        return 1

    groups = pack(sections, budget, soft)
    total = len(groups)

    emitted = []
    for i, group in enumerate(groups):
        areas = describe(group)
        covers = (f"This part covers {join_areas(areas)}." if areas
                  else "This part continues the document.")
        header = render_part_header(
            title=f"{args.title}, part {i + 1} of {total}",
            product_sentence=args.product_sentence,
            covers=covers,
            siblings=(f"This is one part of the {args.title}, split so each part is "
                      f"retrievable on its own. Across its {total} parts the document "
                      f"covers {args.areas}."
                      + (f" {args.note}" if args.note else "")),
            version_line=args.version_line,
        )
        body = "\n\n".join(s[-1] for s in group)
        emitted.append((f"{args.slug}-{i + 1:02d}.md", header + "\n---\n\n" + body + "\n"))

    problems = report(emitted, args.title, args.ceiling)
    src_n = len("\n".join(s[-1] for s in sections).encode("utf-8"))
    kept = sum(len("\n\n".join(s[-1] for s in g).encode("utf-8")) for g in groups)
    if abs(kept - src_n) > len(sections) * 4:
        problems.append(f"content mismatch: {src_n:,} in, {kept:,} out")

    if problems:
        print(f"\nFAILED: {len(problems)} problem(s)", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1

    out_dir = pathlib.Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, doc in emitted:
        (out_dir / name).write_text(doc, encoding="utf-8")
    print(f"\nok  {total} parts written to {out_dir}  ({len(sections)} sections)")
    print(f"    {src_n:,} bytes of content kept from {src_total:,} in the source")
    return 0


if __name__ == "__main__":
    sys.exit(main())
