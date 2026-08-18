---
name: api-review
description: Review an OpenAPI spec for structural defects (wrong HTTP verbs, empty responses, broken security schemes), CRUD and documentation gaps, and coverage of stated product requirements, producing a severity-tagged report with a prioritized fix list. Use when the user says "review this spec", "run an api review", "check this OpenAPI file", "does the API cover the PRD", or points at a .yaml/.json API spec. Do NOT use for reviewing implementation code or probing a live API; this reviews the contract document only.
argument-hint: "[path-to-openapi-spec.yaml] [optional-path-to-prd.md]"
---

# API Review

Evaluate an OpenAPI specification for structural correctness, REST conventions, documentation completeness, and requirements coverage. Done means: a severity-tagged report at `outputs/analyses/<spec-name>-evaluation-<date>.md` that engineering can prioritize from directly.

Two hard rules:

1. **Read the entire spec before forming any finding.** Large file: read in chunks until consumed. A review of half a spec produces false gaps.
2. **Findings name endpoints.** Every issue cites the specific path(s) and operation(s) it appears on. "Some endpoints lack error responses" is not a finding.

## Read first

| Source | Path | What to extract |
|---|---|---|
| Spec sources config | `references/spec-sources.md` (user-filled) | Where specs, PRDs, personas, prior reviews, and the tracker live |
| The spec itself | from argument or config | Everything: paths, schemas, security, servers, tags |
| Requirements | second argument, or PRD path from config | Required capabilities, functional areas, NFRs (auth, scale, error handling) |
| Prior reviews | `outputs/analyses/` | Findings already reported; re-list them only under a "still open" note, not as new |
| Personas | persona doc from config | 3-5 user types for consumer examples |
| Tracker (optional) | MCP named in config | Milestone dates and ticket IDs for schedule implications |

Missing context degrades by section, never blocks the review: no requirements found means structural review only (flag the limitation in the report); no tracker means skip schedule implications; no personas means infer 3 consumer types from the API's domain and label them inferred.

## Workflow

### 1. Inventory the spec

Read the full spec. Build the inventory: endpoint count by method, all paths and operations, declared tags and their assignments, security scheme definitions and where they're applied, the `servers` array, the OpenAPI version. Note every endpoint with `responses: {}` by name as you go.

### 2. Load requirements context

From the PRD argument or configured sources, extract named functional areas, specific required capabilities, and non-functional requirements. Check `outputs/analyses/` for a prior review of the same spec so known findings aren't re-reported as discoveries.

### 3. Run the structural checks

Evaluate against OpenAPI 3.x practice and REST conventions, tagging each finding:

**Critical (blocks correct client behavior or code generation):**
- Wrong HTTP verbs: POST for reads or updates of a single resource, GET with a requestBody, DELETE on non-resource URIs
- Path parameter names violating `[A-Za-z0-9_-]+`
- Content-Type/Accept declared as parameters instead of `content` objects
- Empty `responses: {}` on any endpoint
- Missing `requestBody` on POST/PUT/PATCH that clearly needs one
- Missing `operationId` anywhere
- Security scheme referenced but undefined, or defined but never applied

**Significant (reduces usability or correctness):**
- Placeholder content: TBD, lorem ipsum, boilerplate example data
- Environment-specific values hardcoded in `servers` (lab IPs, dev URLs)
- Schema fields from an unrelated domain (copy-paste contamination)
- Typos in schema field names
- Same concept typed inconsistently across schemas (string here, integer there)
- Tags declared but unused, or endpoints untagged

**Minor (polish and developer experience):**
- Missing 404 on resource lookups; missing 403 anywhere; missing 5xx responses
- No pagination on list endpoints
- Mixed naming conventions (snake_case vs camelCase, singular vs plural resources)
- Parameters or schema fields without descriptions

### 4. Check CRUD completeness

For each primary resource, check create / read-one / list / update / delete. Flag missing operations, and distinguish intentional partial coverage (read-only telemetry) from unintentional gaps.

### 5. Build the requirements gap table

With requirements context: one row per functional area or requirement, mapped to covering endpoints, status Complete / Partial / Missing. Without it: build the table from what a reasonable consumer of this domain expects, and label it domain-inferred. Note gaps that belong to a different API layer by architecture, as framing rather than findings.

### 6. Write consumer examples

For 3-5 personas: what they're trying to accomplish, a minimal happy-path Python example using endpoints that actually exist in the spec, and one gotcha specific to this API.

### 7. Write the report

Follow `templates/output-template.md`. Save to `outputs/analyses/`. If a prior review of this spec exists, add a delta line to the executive summary: fixed / still open / new since last review.

## Worked example (fictional)

Coppermine Systems' device-cloud spec, `coppermine-cloud-v2.yaml`, 41 operations. Two findings as they should read:

> **Critical: `POST /devices/{device id}/reboot` has an invalid path parameter.**
> `{device id}` contains a space, which breaks code generation in every mainstream client generator. Appears on 3 operations under `/devices/`. Fix: rename to `{device_id}` in the path and the parameter object (spec-only change).

> **Significant: `ShippingAddress` schema fields inside `FirmwareImage`.**
> `street`, `postal_code`, and `recipient_name` appear in the firmware schema, an artifact of copy-paste from an order-management spec. No endpoint uses them. Fix: delete the six fields (spec-only change).

And a gap-table row:

> | FA-4 Scheduled jobs | None | Missing | PRD requires recurring firmware jobs; spec has one-shot `POST /jobs` only, no schedule object or cron field |

## Don't rationalize

| If you're thinking | Do this instead |
|---|---|
| "The spec is 6,000 lines, I'll sample it" | Read it all in chunks. Sampled reviews produce false gaps and miss copy-paste contamination, which clusters in unread regions. |
| "No PRD available, so I'll skip coverage analysis" | Build the domain-inferred gap table and label it. Coverage is the section PMs run this skill for. |
| "This finding may be intentional, I'll soften it" | Report it plainly and add "confirm intent with engineering." Softened findings don't get fixed. |
| "The persona examples are decorative, cut them" | They're the fastest empathy check a spec gets; writing one exposes unusable auth or missing endpoints instantly. |
| "Prior review covered this, skip re-checking" | Re-check and report status as fixed or still open. A review that silently drops known issues reads as a clean bill. |

## Exit checklist

Before presenting the report, verify:

- [ ] Whole spec was read; inventory counts match the spec
- [ ] Every Critical and Significant finding names endpoint(s) and the specific fix, tagged spec-only vs implementation
- [ ] Every endpoint with `responses: {}` is listed individually
- [ ] Gap table covers every stated requirement, or is labeled domain-inferred
- [ ] Example code uses only endpoints that exist in the spec
- [ ] No softening language: "breaks code generation", not "may cause issues"
- [ ] Prior-review findings reported as fixed / still open, not rediscovered
- [ ] Report follows `templates/output-template.md`; empty-input sections dropped

## Handoff

- **Before this:** have requirements written down; a review without requirements context is structure-only.
- **After this:** turn Critical and Significant findings into tickets in your tracker; `/bolt-dev` if the next step is building a frontend against this API (the review's findings feed its backend profile).
