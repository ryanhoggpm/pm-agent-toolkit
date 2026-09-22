#!/usr/bin/env python3
"""Scan staged corpus files against a pattern file.

Two pattern files ship as templates and do different jobs.

  redaction-patterns.yaml  things that must not reach the index at all:
                           credentials, real device identities, lab addressing,
                           internal-only detail.

  voice-patterns.yaml      prose that is factually fine but reads wrong when the
                           agent quotes it to a customer: corrections of other
                           documents, imperatives to the reader, talk tracks.

Both are gates. Nothing stages until both come back clean, or until a match has
been read and recorded as a known false positive.

  python3 scan.py --patterns voice-patterns.yaml --path staging/2026-01-01/files
  python3 scan.py --patterns redaction-patterns.yaml --path corpus/ --quiet

Exit status is 1 if any pattern matched, so it can gate a build.

A match is a reading list, not a verdict. A pattern written to catch a claim
also matches the document that denies it. Read every hit before acting.
"""
import argparse
import pathlib
import re
import sys

import yaml

TEXT_SUFFIXES = {".md", ".txt", ".html", ".htm", ".csv", ".json", ".yaml", ".yml"}


def files_under(path, exclude=()):
    """Text files under `path`, minus anything matching an exclude regex.

    A pattern file lists the very strings it is hunting for, so scanning it
    reports itself and buries the real hits. Exclude it rather than weakening
    the patterns.
    """
    p = pathlib.Path(path)
    found = [p] if p.is_file() else sorted(
        f for f in p.rglob("*")
        if f.is_file() and f.suffix.lower() in TEXT_SUFFIXES)
    if not exclude:
        return found
    rx = [re.compile(e) for e in exclude]
    return [f for f in found if not any(r.search(str(f)) for r in rx)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--patterns", required=True)
    ap.add_argument("--path", required=True)
    ap.add_argument("--quiet", action="store_true", help="print only failures")
    ap.add_argument("--exclude", action="append", default=[], metavar="REGEX",
                    help="skip paths matching this regex (repeatable). Use it "
                         "for the pattern file itself.")
    ap.add_argument("--max-hits", type=int, default=8,
                    help="lines to show per pattern before truncating")
    args = ap.parse_args()

    spec = yaml.safe_load(pathlib.Path(args.patterns).read_text(encoding="utf-8"))
    patterns = spec.get("patterns") or []
    if not patterns:
        print(f"no patterns in {args.patterns}", file=sys.stderr)
        return 2

    targets = files_under(args.path, args.exclude)
    if not targets:
        print(f"no text files under {args.path}", file=sys.stderr)
        return 2

    print(f"{spec.get('name', args.patterns)}   {len(targets)} file(s) under {args.path}\n")
    failed = 0
    for entry in patterns:
        name = entry["name"]
        try:
            rx = re.compile(entry["re"], re.I if entry.get("ignore_case", True) else 0)
        except re.error as e:
            print(f"BAD PATTERN  {name}: {e}", file=sys.stderr)
            failed += 1
            continue

        hits = []
        for f in targets:
            try:
                text = f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for i, line in enumerate(text.split("\n"), 1):
                if rx.search(line):
                    hits.append((f, i, line.strip()[:150]))

        if hits:
            failed += 1
            print(f"FAIL  {name}")
            if entry.get("why"):
                print(f"      {entry['why']}")
            for f, i, line in hits[:args.max_hits]:
                print(f"      {f}:{i}:{line}")
            if len(hits) > args.max_hits:
                print(f"      ... and {len(hits) - args.max_hits} more")
            print()
        elif not args.quiet:
            print(f"ok    {name}")

    print()
    if failed:
        print(f"{failed} pattern(s) matched. Read every hit before staging.")
        if spec.get("footer"):
            print("\n" + spec["footer"])
        return 1
    print(f"clean across {len(targets)} file(s).")
    if spec.get("footer"):
        print("\n" + spec["footer"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
