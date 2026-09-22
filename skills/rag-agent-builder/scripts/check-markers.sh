#!/usr/bin/env bash
# Two gates over a skill's own source, before it is published anywhere.
#
#   1. NAMES     no employer, product, competitor, colleague or internal path.
#   2. ANECDOTES no orphaned specific in a mechanism file.
#
# Gate 2 is the one people miss. A name denylist passes happily while the text
# still carries a certificate number, a tool count or a capability name lifted
# from a real corpus: facts from real incidents with the context that made them
# meaningful stripped off, leaving examples only their author can read.
#
# The fix is structural. Mechanism files carry rules, references/field-notes.md
# carries the stories, and the stories are told about a fictional company.
#
#   bash scripts/check-markers.sh                  # scan this skill
#   bash scripts/check-markers.sh --path ../other  # scan somewhere else
#
# The names themselves live in marker-patterns.yaml, never in this script, so
# publishing this file does not publish the list of things you were hiding.
set -uo pipefail
cd "$(dirname "$0")/.."

TARGET="."
PATTERNS=""
while [ $# -gt 0 ]; do
  case "$1" in
    --path) TARGET="$2"; shift 2 ;;
    --patterns) PATTERNS="$2"; shift 2 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

if [ -z "$PATTERNS" ]; then
  if [ -f marker-patterns.yaml ]; then
    PATTERNS=marker-patterns.yaml
  else
    PATTERNS=templates/marker-patterns.yaml
  fi
fi

fail=0

# --- 1. names -------------------------------------------------------------
# Delegates to the skill's own scanner, so there is one pattern-file format and
# the gate cannot drift from the thing it gates.
echo "== names =="
if [ "$PATTERNS" = "templates/marker-patterns.yaml" ]; then
  echo "note  using the unfilled template. Copy it to marker-patterns.yaml and"
  echo "      put your own employer, products and colleagues in it, or this gate"
  echo "      is checking for placeholder text and nothing else."
fi
# The pattern files list the strings they hunt for; scanning them reports
# themselves and buries the real hits.
python3 scripts/scan.py --patterns "$PATTERNS" --path "$TARGET" --quiet \
  --exclude 'marker-patterns\.yaml$' || fail=1

# --- 2. anecdotes ---------------------------------------------------------
# A mechanism file states a rule. The moment it states a *specific* -- a
# certificate number, a tool count, a version string -- it is carrying an
# anecdote, and an anecdote belongs in the field notes where it can be told
# properly and fictionally.
#
# field-notes.md is the sole exemption. templates/ and platforms/ are exempt
# too: a template's job is to show a filled-in example, and a platform profile's
# whole purpose is measured numbers.
EXEMPT='references/field-notes\.md|/templates/|/platforms/|check-markers\.sh|marker-patterns\.yaml'

# The shared fictional universe. Anything here is fine anywhere.
UNIVERSE='Coppermine|CM-900|CM-400|Fleet Cloud|EdgeLink|Ironvine|coppermine\.example'

# POSIX ERE only. `grep -E` does not support (?:...) or lookarounds: it fails,
# and a swallowed error turns a gate into a pass.
declare -A CHECKS=(
  ["certificate or ticket number"]='#[0-9]{3,}|\b(cert|certificate) ?#?[0-9]{4,}'
  ["bare tool or feature count"]='\b[0-9]{2,} (tools|endpoints|operations|connectors)\b'
  ["dotted version string"]='\b[0-9]+\.[0-9]+\.[0-9]+(\.[0-9]+)?[A-Za-z]?[0-9]*\b'
)

echo
echo "== anecdotes in mechanism files =="
files=$(find "$TARGET" -type f \( -name '*.md' -o -name '*.py' -o -name '*.sh' \) \
        | grep -vE "$EXEMPT" | sort)

if [ -z "$files" ]; then
  echo "no mechanism files under $TARGET"
else
  for name in "${!CHECKS[@]}"; do
    err=$(echo "$files" | xargs grep -InE "${CHECKS[$name]}" 2>&1 >/dev/null || true)
    if [ -n "$err" ]; then
      echo "FAIL: pattern for '$name' is not valid POSIX ERE"
      echo "$err" | sed 's/^/      /'
      fail=1
      continue
    fi
    hits=$(echo "$files" | xargs grep -InE "${CHECKS[$name]}" 2>/dev/null \
           | grep -vE "$UNIVERSE" || true)
    if [ -n "$hits" ]; then
      echo "FAIL: $name"
      echo "$hits" | sed 's/^/      /'
      echo "      -> move the story to references/field-notes.md and state the rule without it"
      fail=1
    else
      echo "ok    $name"
    fi
  done
fi

echo
if [ "$fail" -ne 0 ]; then
  echo "check-markers: FAILED"
  exit 1
fi
echo "check-markers: clean"
