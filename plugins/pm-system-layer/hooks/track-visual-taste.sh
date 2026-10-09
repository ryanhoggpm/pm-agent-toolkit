#!/bin/bash
# Visual taste reminder.
# Fires on PostToolUse for Write|Edit. When the touched file is a visual
# output (HTML/CSS or your brand directory), injects a reminder for Claude to
# log any design feedback the user gave this turn to context/design-taste.md.
# Hooks can't do semantic extraction; this just nudges. Fails silently.

set -e 2>/dev/null || true

TOOL_INPUT=$(cat 2>/dev/null) || exit 0

FILE_PATH=$(echo "$TOOL_INPUT" \
  | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    print(d.get('tool_input', {}).get('file_path', ''))
except Exception:
    print('')
" 2>/dev/null) || exit 0

[ -z "$FILE_PATH" ] && exit 0

# Adjust the patterns to your workspace's visual paths.
case "$FILE_PATH" in
  *.html|*.css|*context/brand/*)
    ;;
  *)
    exit 0
    ;;
esac

cat <<'EOF'
{"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": "Reminder: this edit touched a visual output file. If the user gave visual, design, or style feedback this turn (corrected a color, layout, icon choice, spacing, or component pattern), append it to context/design-taste.md as a short dated entry before moving on. If no visual feedback was given this turn, ignore this reminder."}}
EOF
exit 0
