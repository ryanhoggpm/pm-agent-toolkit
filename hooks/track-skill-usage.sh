#!/bin/bash
# Skill usage tracker.
# Fires on PostToolUse when a skill is invoked; appends one line to
# .claude/logs/skill-usage.log. Fails silently, never interrupts the session.

set -e 2>/dev/null || true

TOOL_INPUT=$(cat 2>/dev/null) || exit 0

SKILL_NAME=$(echo "$TOOL_INPUT" \
  | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    ti = d.get('tool_input', d)
    print(ti.get('skill', 'unknown'))
except Exception:
    print('unknown')
" 2>/dev/null) || SKILL_NAME="unknown"

SKILL_ARGS=$(echo "$TOOL_INPUT" \
  | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    ti = d.get('tool_input', d)
    args = str(ti.get('args', ''))
    print(args[:80] + '...' if len(args) > 80 else args)
except Exception:
    print('')
" 2>/dev/null) || SKILL_ARGS=""

TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M UTC" 2>/dev/null) || TIMESTAMP="unknown"

LOG_FILE=".claude/logs/skill-usage.log"
mkdir -p "$(dirname "$LOG_FILE")" 2>/dev/null || true
printf "%s\t%s\t%s\n" "$TIMESTAMP" "$SKILL_NAME" "$SKILL_ARGS" >> "$LOG_FILE" 2>/dev/null || true

exit 0
