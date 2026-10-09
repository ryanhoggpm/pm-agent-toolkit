# Constitution Seed

Pass the relevant principles as `$ARGUMENTS` to `speckit-constitution` for `code` builds. For non-code builds, copy the applicable lines into plan.md under "Constraints." Adapt to the repo and drop what doesn't apply. Five tight principles beat twelve vague ones.

## Principles

1. **Spec is the source of truth.** Code changes trace to a story in spec.md. A requirement found during build goes back into the spec first.
2. **Secrets never enter git.** No passwords, tokens, tenant IDs, private-network IPs, absolute home paths, or personal emails in tracked files. Config comes from the environment or an untracked `.env`. Run a secret scan (gitleaks or equivalent) before every push to an external remote; public repos also get a CI gate.
3. **Production is read-only unless approved per action.** Tests and development run against a sandbox or mocks. Any mutating call against a live system needs the user's explicit approval for that call.
4. **Verify the API, not just its docs.** Published API specs drift from live behavior. Confirm an endpoint's real response before coding to it, and record the verified shape in plan.md.
5. **Tests prove acceptance criteria.** Every P1 acceptance scenario has an automated test or a recorded manual verification. Converged requires a passing run, not a read-through.
6. **Match the codebase.** Existing repos keep their framework, structure, naming, and comment density. No new dependency without a line in plan.md saying why.
7. **Branded UI uses the design system.** Tokens and components come from the project's design system; no ad hoc colors or fonts.
8. **Repo hygiene.** Follow the repo's commit attribution rules. Public repos keep internal ticket IDs, roadmap language, and private names out of commits, PRs, and docs, and the README gets a human review before the first public push.
9. **Simplicity gate.** Start with the smallest structure that meets P1. Added layers need a written reason in plan.md's Complexity Tracking.

## Governance line

"Amendments require the build owner's approval and a dated entry in BUILD.md. Plans that violate a principle record the violation and its justification in Complexity Tracking."
