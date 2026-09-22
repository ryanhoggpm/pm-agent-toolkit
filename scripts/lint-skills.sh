#!/usr/bin/env bash
# Skill lint: every published SKILL.md meets the authoring standard.
#   - frontmatter is valid YAML with a name and a description
#   - description >= 100 chars and contains a routing boundary ("use /" pointer or "NOT")
#   - SKILL.md <= 350 lines
#   - has a read-first table, references a template, ends with an exit checklist
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

[ "$fail" -eq 1 ] && exit 1
echo "lint: OK"
