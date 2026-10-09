#!/usr/bin/env python3
"""Build a whole corpus from project.yaml.

This replaces a hand-written build script. Every document the corpus carries is
a row in the config, so the build is the config, and a new release is a re-run
rather than a reconstruction from someone's shell history.

  python3 build.py --config project.yaml --out staging/<date>/files

Document kinds:
  split   an assembled text or markdown file, cut at heading boundaries
  pdf     a PDF, converted first with headings rebuilt from its bookmarks
  openapi a bundled OpenAPI spec plus hand-authored fragments

Every part it writes fits under the ceiling the platform profile sets. See
../platforms/ for the profiles.
"""
import argparse
import pathlib
import re
import subprocess
import sys

import yaml

HERE = pathlib.Path(__file__).resolve().parent


def run(cmd):
    print("  $ " + " ".join(str(c) for c in cmd[:3]) + " ...")
    r = subprocess.run([str(c) for c in cmd])
    return r.returncode


def common_args(doc, cfg, out, redactions):
    args = ["--out", out, "--slug", doc["slug"], "--title", doc["title"],
            "--product-sentence", doc.get("product_sentence") or cfg["product_sentence"],
            "--areas", doc["areas"],
            "--ceiling", str(cfg.get("ceiling", 60000))]
    if redactions:
        args += ["--redactions", redactions]
    if doc.get("version_line") or cfg.get("version_line"):
        args += ["--version-line", doc.get("version_line") or cfg["version_line"]]
    for key, flag in (("note", "--note"), ("level", "--level"),
                      ("max_level", "--max-level"), ("start_at", "--start-at"),
                      ("drop_section", "--drop-section"), ("promote", "--promote")):
        if doc.get(key) is not None:
            args += [flag, str(doc[key])]
    return args


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="project.yaml")
    ap.add_argument("--out", required=True, help="staging files directory")
    ap.add_argument("--only", default=None, help="build one document by slug")
    args = ap.parse_args()

    cfg = yaml.safe_load(pathlib.Path(args.config).read_text(encoding="utf-8"))
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    converted = out.parent / "converted"

    # Substitutions rewrite text during the build. The scan pattern files are a
    # separate gate run over the result; see scan.py.
    redactions = cfg.get("redaction_substitutions")
    if redactions and not pathlib.Path(redactions).exists():
        print(f"redaction_substitutions not found: {redactions}", file=sys.stderr)
        return 1

    # An unfilled placeholder is the same failure this skill exists to stop: text
    # that is obviously an example to its author and reads as fact to everyone
    # else. The part header goes into every file, so a placeholder there reaches
    # the whole corpus.
    placeholders = []
    for key in ("product", "product_sentence", "version_line"):
        val = str(cfg.get(key) or "")
        if re.search(r"<[^<>\n]{2,40}>", val):
            placeholders.append(f"  {key}: {val.strip()[:90]}")
    for doc in cfg["documents"]:
        for key in ("title", "areas", "product_sentence", "version_line"):
            val = str(doc.get(key) or "")
            if re.search(r"<[^<>\n]{2,40}>", val):
                placeholders.append(f"  documents[{doc.get('slug')}].{key}: {val.strip()[:90]}")
    if placeholders:
        print("template placeholders still in project.yaml:\n"
              + "\n".join(placeholders)
              + "\n\nFill these in. They render into every part header.", file=sys.stderr)
        return 1

    python = cfg.get("python", sys.executable)
    failures = []

    for doc in cfg["documents"]:
        if args.only and doc["slug"] != args.only:
            continue
        kind = doc.get("kind", "split")
        print(f"\n=== {doc['title']} ({kind})")

        if kind == "pdf":
            converted.mkdir(parents=True, exist_ok=True)
            md = converted / (doc["slug"] + ".md")
            cmd = [cfg.get("pdf_python", python), HERE / "pdf_to_markdown.py",
                   "--in", doc["in"], "--out", md, "--title", doc["title"]]
            if redactions:
                cmd += ["--redactions", redactions]
            if run(cmd):
                failures.append(doc["slug"]); continue
            source = md
        elif kind == "openapi":
            cmd = [python, HERE / "build_api_corpus.py", "--spec", doc["in"],
                   "--parts", doc["parts"], "--out", out,
                   "--ceiling", str(cfg.get("ceiling", 60000))]
            if redactions:
                cmd += ["--redactions", redactions]
            for f in cfg.get("scan_patterns") or []:
                cmd += ["--scan-patterns", f]
            if run(cmd):
                failures.append(doc["slug"])
            continue
        else:
            source = doc["in"]

        cmd = [python, HERE / "split_corpus_file.py", "--in", source] + \
            common_args(doc, cfg, str(out), redactions)
        if run(cmd):
            failures.append(doc["slug"])

    print()
    if failures:
        print(f"FAILED: {len(failures)} document(s): {', '.join(failures)}", file=sys.stderr)
        return 1
    n = len(list(out.glob("*")))
    print(f"ok  {n} file(s) in {out}")
    print(f"    platform profile: {cfg.get('platform', 'generic')}  (see ../platforms/)")
    print("    next: scan, upload, then verify reach before any eval:")
    print(f"      python3 {HERE / 'reach_probe.py'} --emit --parts {out} --out probes.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
