#!/usr/bin/env bash
# Skill lint: every published SKILL.md meets the authoring standard.
#   - description >= 100 chars and contains a routing boundary ("use /" pointer or "NOT")
#   - SKILL.md <= 350 lines
#   - has a read-first table, references a template, ends with an exit checklist
set -euo pipefail
cd "$(dirname "$0")/.."

[ -d skills ] || { echo "lint: OK (no skills yet)"; exit 0; }

fail=0
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
