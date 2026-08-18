#!/usr/bin/env bash
# Provenance gate: fail if any published skill name collides with content from
# a commercially licensed package this repo's author uses privately but may
# not redistribute. Names only; prose-level review is a manual gate.
set -euo pipefail
cd "$(dirname "$0")/.."

BLOCKLIST=(
  # skills
  activation-analysis code-first-draft competitor-analysis connect-mcps
  create-tickets daily-plan decision-doc define-north-star expansion-strategy
  experiment-decision experiment-metrics feature-metrics feature-results
  generate-ai-prototype impact-sizing interview-feedback interview-guide
  interview-prep journey-map launch-checklist meeting-agenda meeting-cleanup
  meeting-feedback meeting-notes metrics-framework napkin-sketch prd-draft
  prd-review-panel prioritize prototype prototype-feedback ralph-wiggum
  retention-analysis slack-message status-update strategy-sprint user-interview
  user-research-synthesis weekly-plan weekly-review write-prod-strategy
  # sub-agents
  customer-voice designer-reviewer engineer-reviewer executive-reviewer
  legal-advisor skeptic uxr-analyst
  # templates
  prd-template roadmap-template interview_template launch-checklist-template
  retrospective-template okr-template
)

fail=0
for name in "${BLOCKLIST[@]}"; do
  if [ -d "skills/$name" ] || [ -f "rules/$name.md" ] || [ -f "templates/$name.md" ]; then
    echo "PROVENANCE VIOLATION: '$name' matches the non-redistributable blocklist"
    fail=1
  fi
done

if [ "$fail" -eq 1 ]; then
  echo "See README Credits section. These assets may not be published from this repo."
  exit 1
fi
echo "provenance: OK"
