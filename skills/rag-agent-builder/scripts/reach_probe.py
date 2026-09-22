#!/usr/bin/env python3
"""Measure what an agent can actually retrieve, one part at a time.

The generic verify. `check-chunk-counts.py` is faster but needs a platform that
publishes chunk metadata, and most do not. This needs nothing but the ability to
ask the agent a question, so it works everywhere, including on a platform whose
chunking nobody has measured.

It also measures the right thing. Chunk counts are an inference: one chunk, so
presumably reachable. A probe is an observation: this string is in the file, the
agent either produces it or does not.

  python3 reach_probe.py --emit  --parts staging/<date>/files --out probes.json
  # ask the agent each question, save the replies
  python3 reach_probe.py --score --probes probes.json --answers answers.json

**Probes come from the tail of each part.** A platform that truncates, or that
reads only the first chunk, loses the end of a file first, so the end is where a
probe carries information. A probe drawn from the opening of a part would pass
on a file that is 90% invisible.

answers.json is `{"<probe id>": "<what the agent said>"}`. Scoring is a substring
test against the probe string, so paste the reply in whole; surrounding prose
does not matter.

Exit status is 1 if any part is unreachable, so it can gate a release.
"""
import argparse
import json
import pathlib
import re
import sys

# How far from the end to look for a probe. Far enough in that a trailing
# heading or version line is not the whole probe, close enough to the end that
# it is genuinely testing the tail.
TAIL_BYTES = 4000

# A probe wants to be a phrase no other part shares and no model would guess:
# long enough to be distinctive, short enough that an agent will reproduce it
# rather than paraphrase it.
MIN_WORDS, MAX_WORDS = 6, 14


def candidate_lines(text):
    """Prose lines from the tail, longest first. Skips what will not round-trip."""
    tail = text.encode("utf-8")[-TAIL_BYTES:].decode("utf-8", errors="ignore")
    out = []
    for line in tail.split("\n"):
        line = line.strip()
        if not line or line.startswith(("#", "|", ">", "```", "---", "- ", "* ")):
            continue
        # A table row or a code fragment is reproduced unreliably; prose is not.
        if line.count("`") or line.count("|"):
            continue
        words = line.split()
        if len(words) < MIN_WORDS:
            continue
        out.append(" ".join(words[:MAX_WORDS]))
    out.sort(key=len, reverse=True)
    return out


def emit(parts_dir, out_path, question):
    parts = sorted(p for p in pathlib.Path(parts_dir).glob("*")
                   if p.is_file() and p.suffix.lower() in {".md", ".txt"})
    if not parts:
        print(f"no parts under {parts_dir}", file=sys.stderr)
        return 2

    seen, probes, skipped = set(), [], []
    for part in parts:
        text = part.read_text(encoding="utf-8", errors="replace")
        for line in candidate_lines(text):
            key = line.lower()
            if key in seen:
                continue  # shared boilerplate proves nothing about this part
            seen.add(key)
            probes.append({"id": part.stem, "file": part.name, "probe": line,
                           "question": question.format(probe=line)})
            break
        else:
            skipped.append(part.name)

    out = pathlib.Path(out_path)
    out.write_text(json.dumps({"probes": probes}, indent=1), encoding="utf-8")
    print(f"{len(probes)} probe(s) written to {out}")
    if skipped:
        print(f"\n{len(skipped)} part(s) gave no usable probe. Their tails are all "
              f"headings, tables or code:")
        for name in skipped:
            print(f"  {name}")
        print("Probe these by hand, or they go unverified.")
    print("\nAsk the agent each question, then save the replies as\n"
          '  {"<id>": "<reply>", ...}\n'
          "and score them. Ask them in small batches, the way the eval does.")
    return 0


def score(probes_path, answers_path):
    probes = json.loads(pathlib.Path(probes_path).read_text(encoding="utf-8"))["probes"]
    answers = json.loads(pathlib.Path(answers_path).read_text(encoding="utf-8"))

    def norm(s):
        return re.sub(r"\s+", " ", s or "").strip().lower()

    reached, missing, unanswered = [], [], []
    for p in probes:
        reply = answers.get(p["id"])
        if reply is None:
            unanswered.append(p)
        elif norm(p["probe"]) in norm(reply):
            reached.append(p)
        else:
            missing.append(p)

    print(f"{len(reached)} of {len(probes)} part(s) reachable\n")
    for p in missing:
        print(f"UNREACHABLE  {p['file']}")
        print(f"             wanted: {p['probe']}")
    if unanswered:
        print(f"\n{len(unanswered)} part(s) not asked yet: "
              f"{', '.join(p['file'] for p in unanswered)}")

    if missing:
        print(f"\n{len(missing)} part(s) unreachable. The agent holds the file and "
              f"cannot read to its end.\nShrink the ceiling in project.yaml, rebuild, "
              f"re-upload, re-probe.")
        return 1
    if unanswered:
        print("\nIncomplete. Every part must be asked before this is a pass.")
        return 1
    print("\nEvery part reachable to its tail.")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit", action="store_true")
    ap.add_argument("--score", action="store_true")
    ap.add_argument("--parts", help="the built files directory")
    ap.add_argument("--out", default="probes.json")
    ap.add_argument("--probes", default="probes.json")
    ap.add_argument("--answers")
    ap.add_argument("--question",
                    default='Quote the passage from your sources that begins "{probe}".',
                    help="how to ask. Keep it a quote request; a paraphrase "
                         "request cannot be scored.")
    args = ap.parse_args()

    if args.emit:
        if not args.parts:
            ap.error("--emit needs --parts")
        return emit(args.parts, args.out, args.question)
    if args.score:
        if not args.answers:
            ap.error("--score needs --answers")
        return score(args.probes, args.answers)
    ap.error("pass --emit or --score")


if __name__ == "__main__":
    sys.exit(main())
