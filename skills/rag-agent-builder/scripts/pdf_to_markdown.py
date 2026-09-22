#!/usr/bin/env python3
"""Convert a user guide PDF to markdown with real heading structure.

Headings come from the PDF's own bookmark tree, not from font-size guessing.
The bookmarks in these guides are three levels deep and match the printed
chapter and section titles exactly, so they can be matched back to the extracted
text and promoted in place.

Two things have to be removed or the corpus fills with them: the running header
repeated on all several hundred pages, and the printed page numbers, which mean
nothing once the document is split into parts that have no pages.

  python3 pdf_to_markdown.py --in GUIDE.pdf --out GUIDE.md --title "..."
"""
import argparse
import pathlib
import re
import sys
from collections import Counter

import pymupdf
import yaml


def page_lines(doc):
    return [[l.rstrip() for l in doc[i].get_text("text").split("\n")]
            for i in range(doc.page_count)]


def running_lines(pages, threshold=0.25):
    """Lines appearing near the top of a quarter of all pages are furniture."""
    seen = Counter()
    for lines in pages:
        for l in lines[:4]:
            s = l.strip()
            if s and not s.isdigit():
                seen[s] += 1
    cutoff = len(pages) * threshold
    return {s for s, n in seen.items() if n >= cutoff}


def norm(s):
    return re.sub(r"\s+", " ", s.replace("™", "").replace("®", "")).strip().lower()


def strip_furniture(pages, furniture):
    """Drop the running header and the page number from the top of each page."""
    out = []
    for lines in pages:
        i = 0
        while i < len(lines) and i < 5:
            s = lines[i].strip()
            if not s or s.isdigit() or s in furniture:
                i += 1
                continue
            # The header line is the guide title with a stray glued-on word
            # (e.g. "rightAcme 8000 ... User Guide"), so it varies and is not caught
            # by exact repetition.
            if norm(s).endswith("user guide") and len(s) < 90:
                i += 1
                continue
            break
        out.append(lines[i:])
    return out


def insert_headings(pages, toc):
    """Promote each bookmark title to a heading where it appears in the text.

    A bookmark title is also the running header of every page in its chapter, so
    a match is only accepted on the bookmark's own page or the one after it.
    Where the title never appears as a line of body text, the heading is placed
    at the top of its page instead, which keeps the structure complete.
    """
    # Keyed on the bookmark's position, not its title: "Overview" is the name of
    # a section in a dozen different chapters, and keying on the text would place
    # the first one and silently drop the rest.
    wanted = {}
    for i, (level, title, pno) in enumerate(toc):
        wanted.setdefault(pno - 1, []).append((i, level, title))

    out, done, placed, forced = [], set(), 0, 0
    for pi, lines in enumerate(pages):
        todo = [x for x in wanted.get(pi, []) + wanted.get(pi - 1, []) if x[0] not in done]
        rendered = []
        for line in lines:
            hit = next((x for x in todo if norm(x[2]) == norm(line)), None)
            if hit:
                rendered.append(f"{'#' * (hit[1] + 1)} {hit[2]}")
                done.add(hit[0])
                todo.remove(hit)
                placed += 1
            else:
                rendered.append(line)
        # Anything that belonged to this page and never matched a line of text.
        head = []
        for x in wanted.get(pi, []):
            if x[0] not in done:
                head.append(f"{'#' * (x[1] + 1)} {x[2]}")
                done.add(x[0])
                forced += 1
        out.append("\n".join(head + rendered))
    return "\n".join(out), placed, forced


def tidy(text):
    text = re.sub(r"\s*\(on page \d+\)", "", text)     # page refs mean nothing now
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # A numbered or bulleted list comes out of the PDF with each marker in its
    # own text block, so "1." lands on a line by itself above its step.
    marker = re.compile(r"^\s*(\d+\.|[a-z]\.|[-\u2022\u25cf])\s*$")
    joined, lines = [], text.split("\n")
    i = 0
    while i < len(lines):
        if marker.match(lines[i]) and i + 1 < len(lines) and lines[i + 1].strip():
            joined.append(f"{lines[i].strip()} {lines[i + 1].strip()}")
            i += 2
        else:
            joined.append(lines[i])
            i += 1

    # PDF extraction hard-wraps paragraphs. Rejoin a line with the next only
    # when the break is plainly mid-sentence, so tables and lists survive.
    out = []
    for line in joined:
        prev = out[-1] if out else ""
        nxt = line.strip()
        if (prev and not prev.startswith("#") and not prev.endswith("|")
                and not marker.match(prev)
                and ((not re.search(r"[.:;!?]$", prev) and len(prev) > 55
                      and re.match(r"^[a-z(]", nxt))
                     # "See the section," then the cross-reference title, which
                     # starts with a capital and so escapes the rule above.
                     or (re.search(r"(,|\bSee|\bsee)$", prev) and len(prev) > 40 and nxt))):
            out[-1] = prev.rstrip() + " " + nxt
        else:
            out.append(line)
    return "\n".join(out).strip() + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--redactions", default=None,
                    help="YAML holding a `redactions` list of {re, to}")
    args = ap.parse_args()

    doc = pymupdf.open(args.src)
    toc = doc.get_toc()
    if not toc:
        print("no bookmarks; headings cannot be rebuilt", file=sys.stderr)
        return 1

    pages = page_lines(doc)
    pages = strip_furniture(pages, running_lines(pages))
    body, placed, forced = insert_headings(pages, toc)
    text = f"# {args.title}\n\n" + tidy(body)

    redacted = 0
    if args.redactions:
        rules = yaml.safe_load(pathlib.Path(args.redactions).read_text())["redactions"]
        for r in rules:
            text, n = re.subn(r["re"], r["to"], text)
            redacted += n

    pathlib.Path(args.out).write_text(text, encoding="utf-8")
    n = len(text.encode("utf-8"))
    print(f"ok  {args.out}")
    print(f"    {doc.page_count} pages -> {n:,} bytes")
    print(f"    {len(toc)} bookmarks: {placed} matched in the text, {forced} placed by page")
    if args.redactions:
        print(f"    {redacted} redactions applied")
    for lvl in (2, 3, 4):
        print(f"    H{lvl}: {len(re.findall(rf'^{"#" * lvl} ', text, re.M))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
