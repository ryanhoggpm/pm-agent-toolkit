#!/bin/bash
# Injects lightweight context at session start: recent skill usage and
# uncommitted work, so the session opens knowing what was in flight.

echo "=== Session start ==="

LOG=".claude/logs/skill-usage.log"
if [ -f "$LOG" ]; then
    COUNT=$(wc -l < "$LOG" 2>/dev/null || echo 0)
    echo "Recent skills (last 5 of $COUNT logged):"
    tail -5 "$LOG" 2>/dev/null
else
    echo "Skill log: not yet created."
fi
echo ""

CHANGES=$(git status --short 2>/dev/null | head -8)
if [ -n "$CHANGES" ]; then
    echo "Uncommitted changes:"
    echo "$CHANGES"
else
    echo "Working tree: clean"
fi
echo "====================="
