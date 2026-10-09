#!/usr/bin/env bash
# Company-marker gate: published content must contain no employer-specific
# names, products, internal paths, or private network addresses.
#
# Generic patterns live here. Employer-specific patterns never do: they come
# from a gitignored .markers.local (one extended regex per line, # comments)
# or, in CI, from the MARKER_PATTERNS secret. See .markers.example.
set -euo pipefail
cd "$(dirname "$0")/.."

GENERIC='\b10\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\b|\b192\.168\.|\b172\.(1[6-9]|2[0-9]|3[01])\.[0-9]{1,3}\.[0-9]{1,3}\b|/home/[a-z]|/mnt/c/Users|context-library|reference-files'

LOCAL=""
if [ -n "${MARKER_PATTERNS:-}" ]; then
  LOCAL=$(printf '%s\n' "$MARKER_PATTERNS" | grep -vE '^\s*(#|$)' | paste -sd'|' -)
elif [ -f .markers.local ]; then
  LOCAL=$(grep -vE '^\s*(#|$)' .markers.local | paste -sd'|' -)
else
  echo "markers: no .markers.local or MARKER_PATTERNS; checking generic patterns only"
fi

PATTERN="$GENERIC"
[ -n "$LOCAL" ] && PATTERN="$GENERIC|$LOCAL"

DIRS=""
for d in skills plugins hooks rules docs examples README.md; do
  [ -e "$d" ] && DIRS="$DIRS $d"
done
[ -z "$DIRS" ] && { echo "markers: OK (nothing to scan)"; exit 0; }

# -i so a name can't slip through on case; matches are printed for review.
# marker-patterns.yaml defines scanner regexes, so it matches by design.
if grep -rInEi --exclude=marker-patterns.yaml "$PATTERN" $DIRS; then
  echo "MARKER VIOLATION: employer-specific or private content found (lines above)"
  exit 1
fi
echo "markers: OK"
