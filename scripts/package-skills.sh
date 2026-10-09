#!/usr/bin/env bash
# Package each skill as a standalone zip for claude.ai upload
# (Customize > Skills > Upload). claude.ai expects <skill-name>/SKILL.md at the
# top of the archive, so each zip is built from the skill's parent folder.
#   bash scripts/package-skills.sh            # all skills into dist/
#   bash scripts/package-skills.sh html-render
set -euo pipefail
cd "$(dirname "$0")/.."

OUT="dist"
rm -rf "$OUT"; mkdir -p "$OUT"

count=0
for dir in plugins/*/skills/*/; do
  name=$(basename "$dir")
  [ $# -gt 0 ] && [[ " $* " != *" $name "* ]] && continue
  parent=$(dirname "$dir")
  ( cd "$parent" && zip -qr "../../../$OUT/$name.zip" "$name" -x '*/__pycache__/*' '*.pyc' '*/.DS_Store' )
  # Fail loudly if the archive shape is wrong; a root-level SKILL.md isn't recognized.
  unzip -Z1 "$OUT/$name.zip" | grep -qx "$name/SKILL.md" || { echo "PACKAGE $name: SKILL.md not at $name/SKILL.md"; exit 1; }
  count=$((count + 1))
done

( cd "$OUT" && sha256sum ./*.zip > SHA256SUMS )
echo "package: $count skill zip(s) in $OUT/"
