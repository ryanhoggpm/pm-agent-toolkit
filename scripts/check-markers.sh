#!/usr/bin/env bash
# Company-marker gate: published content must contain no employer-specific
# names, products, internal paths, or lab addresses.
set -euo pipefail
cd "$(dirname "$0")/.."

PATTERN='Lantronix|Percepxion|SLC9|SLC 9|SLC8|LM-Series|Opengear|consoleflow|Saleel|Mathi|Chirjeev|Farheen|192\.168\.|context-library|reference-files'

DIRS=""
for d in skills hooks rules docs examples; do
  [ -d "$d" ] && DIRS="$DIRS $d"
done
[ -z "$DIRS" ] && { echo "markers: OK (nothing to scan)"; exit 0; }

if grep -rInE "$PATTERN" $DIRS; then
  echo "MARKER VIOLATION: employer-specific content found (patterns above)"
  exit 1
fi
echo "markers: OK"
