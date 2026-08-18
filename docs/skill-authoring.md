# Skill authoring

The full authoring standard lives inside the `create-skill` skill, where it's enforced rather than just documented:

- **The 10 rules:** [skills/create-skill/references/authoring-standard.md](../skills/create-skill/references/authoring-standard.md). Routing-engineered descriptions, imperative bodies, read-first tables, line caps, shipped templates, worked examples, anti-rationalization tables, exit checklists, handoffs, existence checks.
- **The scaffold:** [skills/create-skill/templates/skill-template.md](../skills/create-skill/templates/skill-template.md)
- **A worked example:** [skills/create-skill/references/worked-example.md](../skills/create-skill/references/worked-example.md)

To author a new skill, run `/create-skill` and it walks the whole standard. To contribute one here, the same standard is the PR bar, and CI enforces the mechanical parts (`scripts/lint-skills.sh`) plus two repo-specific gates: no company-internal markers (`scripts/check-markers.sh`) and no name collisions with non-redistributable commercial content (`scripts/check-provenance.sh`; see the README's Credits section for why).

Fictional companies only in examples. This repo's examples share one fictional universe (Coppermine Systems, a B2B device-management company); reusing it keeps examples consistent, but any clearly fictional company works.
