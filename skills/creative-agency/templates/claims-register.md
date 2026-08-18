# Claims register (fill this in, and keep it current)

The register is what keeps marketing honest about what has actually shipped. `/creative-agency` checks every draft against it before producing a revised draft, and `claims-check` mode runs the check alone. Date the register every time you update it; a stale register is how not-yet-GA features leak into public copy.

## The schema

```markdown
# Claims register: [product] (updated YYYY-MM-DD)

## Include fully
[Shipped, GA, verifiable. Name the feature the way copy should name it,
with the specific version/spec/cert that makes it credible.]

## Include conservatively (one mention, hedged language only)
[Real but partial, or shipping-soon-with-risk. Give the exact approved
phrasing, and name what must NOT be claimed until confirmed.]

## Exclude entirely (flag if present in a draft)
[Not GA, internal-only, PoC, or legally risky. For each: why it's excluded,
so the flag explains itself.]
```

## Rules

- Every entry in "conservatively" carries its approved phrasing verbatim; writers copy it, not paraphrase it.
- Anything not in the register defaults to a flag, not a pass. The register is an allowlist for claims, not a blocklist.
- Competitor mentions: factual, verifiable comparisons only; note any competitor-specific legal guidance here.

## Example (fictional): Coppermine Fleet Cloud, updated 2026-06-10

### Include fully
- Zero-touch provisioning
- Device REST API: OpenAPI 3.1
- Fleet Cloud platform: firmware compliance tracking, fleet groups, config backup/restore
- Security: TPM 2.0, tamper-evident audit logs, encrypted storage (128 GB), LDAP/SAML
- Ansible collection `coppermine.fleet` (available on GitHub)

### Include conservatively
- Connected-device identification: use "your ports identify what's connected; when something changes, they know that too." Do NOT claim automated CLI interaction or make/model/version capture until confirmed at GA.
- Container hosting: "container hosting capability" only; no named third-party apps.

### Exclude entirely
- JIT credential delivery from the IdP (not GA)
- The integration-server proof of concept (personal-repo PoC, not a product)
- Ansible Galaxy certification (collection is GitHub-available; certification claim would be false)
- Any Terraform provider not yet published
