#!/usr/bin/env bash
# Skill lint: every published SKILL.md meets the authoring standard.
#   - frontmatter is valid YAML with a name and a description
#   - description >= 100 chars and contains a routing boundary ("use /" pointer or "NOT")
#   - SKILL.md <= 350 lines
#   - has a read-first table, references a template, ends with an exit checklist
#   - frontmatter keys limited to the Agent Skills spec (claude.ai upload rejects others)
#   - name matches folder; compatibility present; no cross-skill paths; no em dashes
set -euo pipefail
cd "$(dirname "$0")/.."

[ -d skills ] || { echo "lint: OK (no skills yet)"; exit 0; }

fail=0

# Parse the frontmatter before anything else reads it. The checks below pull the
# description with awk, which is happy to read a line that no YAML parser will
# accept: an unquoted `key: value` colon inside a description is valid text and
# invalid YAML, and it renders as an error banner on GitHub while every other
# gate passes. Two skills shipped that way before this check existed.
if command -v python3 >/dev/null 2>&1; then
  python3 - <<'PYEOF' || fail=1
import pathlib, sys
try:
    import yaml
except ImportError:
    print("lint: PyYAML absent, skipping frontmatter parse"); sys.exit(0)

import re
ALLOWED = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
bad = 0
for f in sorted(pathlib.Path("skills").glob("*/SKILL.md")):
    text = f.read_text(encoding="utf-8")
    if not text.startswith("---"):
        print(f"LINT {f.parent.name}: no YAML frontmatter"); bad = 1; continue
    try:
        meta = yaml.safe_load(text.split("---", 2)[1])
    except yaml.YAMLError as e:
        mark = getattr(e, "problem_mark", None)
        where = f" (line {mark.line}, column {mark.column})" if mark else ""
        print(f"LINT {f.parent.name}: frontmatter is not valid YAML{where}")
        print(f"       {getattr(e, 'problem', e)}")
        print( "       a colon followed by a space inside an unquoted value is "
               "the usual cause; quote the whole value")
        bad = 1; continue
    if not isinstance(meta, dict) or not meta.get("name") or not meta.get("description"):
        print(f"LINT {f.parent.name}: frontmatter needs both name and description")
        bad = 1; continue
    # claude.ai upload rejects any key outside the Agent Skills spec, so a
    # Claude Code-only field (argument-hint, aliases, model) breaks the zip.
    extra = set(meta) - ALLOWED
    if extra:
        print(f"LINT {f.parent.name}: frontmatter keys not portable to claude.ai: {sorted(extra)}")
        bad = 1
    if meta["name"] != f.parent.name or not NAME.fullmatch(meta["name"]):
        print(f"LINT {f.parent.name}: name must be kebab-case and match the folder")
        bad = 1
    if len(meta["description"]) > 1024:
        print(f"LINT {f.parent.name}: description over 1024 chars")
        bad = 1
    if not meta.get("compatibility"):
        print(f"LINT {f.parent.name}: add a compatibility line (where it works, what it needs)")
        bad = 1
    elif len(meta["compatibility"]) > 500:
        print(f"LINT {f.parent.name}: compatibility over 500 chars")
        bad = 1
sys.exit(bad)
PYEOF
else
  echo "lint: python3 absent, skipping frontmatter parse"
fi
while IFS= read -r f; do
  name=$(basename "$(dirname "$f")")
  lines=$(wc -l < "$f")
  desc=$(awk '/^description:/{sub(/^description:[[:space:]]*/,""); print; exit}' "$f")

  [ "$lines" -gt 350 ] && { echo "LINT $name: SKILL.md is $lines lines (max 350)"; fail=1; }
  [ "${#desc}" -lt 100 ] && { echo "LINT $name: description is ${#desc} chars (min 100)"; fail=1; }
  echo "$desc" | grep -qiE "NOT|use /" || { echo "LINT $name: description has no routing boundary"; fail=1; }
  grep -qiE "read.first|What to extract" "$f" || { echo "LINT $name: no read-first table"; fail=1; }
  grep -qiE "templates/" "$f" || { echo "LINT $name: no template reference"; fail=1; }
  grep -qiE "exit checklist|before finishing" "$f" || { echo "LINT $name: no exit checklist"; fail=1; }
done < <(find skills -name SKILL.md)

# Each skill must stand alone when zipped, so no links that climb out of its folder.
if grep -rnE '\.\./\.\./' skills; then
  echo "LINT: cross-skill relative paths found (lines above); each skill zips on its own"; fail=1
fi
if grep -rn $'\u2014' skills hooks rules docs README.md 2>/dev/null; then
  echo "LINT: em dashes found (lines above)"; fail=1
fi

[ "$fail" -eq 1 ] && exit 1
echo "lint: OK"
