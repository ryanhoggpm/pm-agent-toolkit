#!/bin/bash
# Fires after context compaction. Re-surfaces what's easy to lose.

echo "=== Context compacted ==="
echo "Some prior context was trimmed. If work feels thin:"
echo "  /context-search [topic]  rediscovers files and prior output"
echo "  /cs [initiative name]    finds what was in progress"
echo ""

LOG=".claude/logs/skill-usage.log"
if [ -f "$LOG" ]; then
    echo "Last 3 skills before compact:"
    tail -3 "$LOG" 2>/dev/null
fi
echo "========================="
