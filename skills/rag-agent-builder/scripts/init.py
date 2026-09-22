#!/usr/bin/env python3
"""Scaffold a corpus project.

  python3 init.py --product "CM-900" --out ~/corpus/cm900

Copies the templates, substitutes the product name, and creates the directories
a build expects. It never overwrites an existing file; re-running it after you
have started editing is safe and reports what it skipped.

What it does not do is guess your facts. Two files need you before the first
build is meaningful:

  project.yaml                  point `documents` at your sources, write the
                                product sentence and the version line
  redaction-substitutions.yaml  rewrites applied during the build
  redaction-patterns.yaml       the gate that fails an upload. Keep both: a
                                substitution you forgot to write is what the
                                gate exists to catch

The scanner is generic on purpose. Everything specific to your organisation
lives in that pattern file, which is why the skill itself carries no product.
"""
import argparse
import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
TEMPLATES = HERE.parent / "templates"

# Template file -> destination name. part-header.md is documentation of the
# header the splitter renders, so it travels with the project for reference.
FILES = {
    "project.yaml": "project.yaml",
    "redaction-substitutions.yaml": "redaction-substitutions.yaml",
    "redaction-patterns.yaml": "redaction-patterns.yaml",
    "voice-patterns.yaml": "voice-patterns.yaml",
    "source-manifest.md": "source-manifest.md",
    "eval-set.md": "eval-set.md",
    "part-header.md": "docs/part-header.md",
}

DIRS = ["sources", "staging", "docs"]


def substitute(text, product):
    for token in ("<Product name>", "<Product>", "<PRODUCT>"):
        text = text.replace(token, product)
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--product", required=True, help="the product this corpus describes")
    ap.add_argument("--out", required=True, help="project directory to create")
    args = ap.parse_args()

    out = pathlib.Path(args.out).expanduser()
    out.mkdir(parents=True, exist_ok=True)
    for d in DIRS:
        (out / d).mkdir(parents=True, exist_ok=True)

    written, skipped = [], []
    for src_name, dest_name in FILES.items():
        src = TEMPLATES / src_name
        if not src.exists():
            print(f"missing template: {src}", file=sys.stderr)
            return 1
        dest = out / dest_name
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            skipped.append(dest_name)
            continue
        dest.write_text(substitute(src.read_text(encoding="utf-8"), args.product),
                        encoding="utf-8")
        written.append(dest_name)

    print(f"{args.product} corpus project at {out}\n")
    for name in written:
        print(f"  new   {name}")
    for name in skipped:
        print(f"  kept  {name}  (already present)")

    print(f"""
Next:
  1. put your source documents in {out / 'sources'}
  2. edit project.yaml: one row per document, plus the product sentence
     and the version line that every part header carries
  3. fill in redaction-patterns.yaml with your own facts
  4. pick a platform profile: see {HERE.parent / 'platforms'}. `generic` is the
     honest default until you have measured yours.
  5. python3 {HERE / 'build.py'} --config {out / 'project.yaml'} \\
       --out {out / 'staging' / '<date>' / 'files'}
  6. scan, upload, then verify reach before any eval:
       python3 {HERE / 'reach_probe.py'} --emit --parts <files> --out probes.json

The scripts stay in the skill. Run them against your project by path, so an
update to the skill reaches every project without a copy.""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
