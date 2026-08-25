# The platform-diagnostic pattern

A design pattern for a read-only skill that answers "where does our platform actually stand" with live data instead of guesses. It ships here as a pattern rather than a runnable skill because the implementation is inseparable from your platform's specific API or MCP tools; the design, which is where the hard-won lessons live, transfers whole.

## The problem it solves

A question every B2B SaaS team eventually gets from leadership: how much of what's provisioned is actually in use? Licensed seats versus active users, enrolled devices versus devices doing real work, connected integrations versus integrations that ran this month. In young platforms the honest answer is often days of manual digging, because product analytics either doesn't exist yet or only instruments the web frontend while the real activity lives in APIs, agents, and background jobs. A recurring read-only diagnostic skill is the stopgap that turns out to be worth keeping: dated snapshots on a standing cadence make drift visible in a way ad hoc queries never do.

## The seven design rules

**1. Read-only, enforced by an allowlist.** The skill names the exact query tools it may call, and the exit checklist requires confirming no mutating tool (reboot, config write, credential change) was touched. A diagnostic that can also change state will eventually be run by someone who doesn't know that.

**2. Mandatory blind-spot disclosure, every run, kept current.** State what the credentials cannot see and whether that's architectural (on-prem or network-isolated deployments no permission change reaches) or a pending permission ask (with its status: not sent / sent date / granted date). This section is never boilerplate; it updates each run. The failure it prevents is specific and expensive: a partial-visibility number getting quoted upward as a company-wide figure.

**3. One metric formula, reused verbatim from its source of truth.** If your activity metric ("active device," "weekly active seat," or equivalent) is defined in a North Star or metrics doc, the skill quotes that formula rather than restating it. Two drifting definitions of the same metric are worse than none. If the source doc is missing or changed, the skill flags it and stops rather than inventing a formula.

**4. Dated snapshots, never overwritten.** Each run writes `<name>-YYYY-MM-DD.md` alongside its predecessors. The snapshots ARE the analytics layer; drift only becomes visible because prior runs still exist.

**5. Multi-source activity evidence, sources named.** Platform APIs rarely offer one unified "was this thing active in the last 30 days" query. Use several signals (audit/session events, job executions, telemetry check-ins, firmware/config status), count an entity active if any one qualifies within the window, and report which sources succeeded, failed, or returned empty this run, so a gap in the data is distinguishable from genuine zero activity.

**6. Segment before you aggregate.** Active-vs-enrolled per device family (or per tenant, per plan tier) is usually the informative number; the aggregate mostly hides the story. Report both, segment first.

**7. Watch for the active-to-inactive transition.** Any entity that was active last snapshot and is enrolled-only now is a churn or renewal-risk signal, worth flagging by name even at small scale. It's the cheapest early-warning system the pattern provides.

## Skeleton

```
1. Authenticate (read-only credentials). On failure: stop, report; never
   proceed on stale or cached data.
2. Enumerate visible scope (tenants, entities, metadata). What these calls
   return IS the universe for this run; say so.
3. Compute the activity metric per entity from the multi-source evidence,
   formula quoted verbatim from its source doc.
4. Segment breakdown (family / tenant / tier): active vs enrolled-only.
5. Write the Known Blind Spots section (rule 2), updated for this run.
6. Delta vs the previous snapshot, naming any active→inactive transitions.
7. Save the dated snapshot; never overwrite.
```

The exit checklist mirrors the rules: read-only allowlist confirmed, blind spots current and specific, formula matched verbatim, every number labeled with its visibility scope, every count from a live call this run (nothing carried forward unverified).

## Building it with this toolkit

Run `/create-skill` with this doc as the design input; the skeleton above becomes the workflow, the seven rules become the hard rules and exit checklist, and your platform's actual query tools fill the allowlist. Set a standing cadence (biweekly works well) so snapshots accumulate; the first run's only job is to exist, since every later run gets a delta.
