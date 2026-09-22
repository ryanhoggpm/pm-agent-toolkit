# Platform profile: <platform>

<One line: what this platform is, and which tenant or tier these numbers came from.>

Measured <month year>. Re-measure after a platform release.

Selected with `platform: <slug>` in `project.yaml`.

---

**Every row below is an experiment you ran, or it is marked as the vendor's claim.** Those are
different kinds of fact and a profile that blurs them is worse than no profile. The whole reason
this skill exists is that a documented 80MB upload limit was read as a statement about what an
agent could retrieve, and it was not one.

Write "unknown" freely. An honest gap sends the next person to measure it; a guess sends them to
trust it.

## Capabilities

| | | |
|---|---|---|
| Ceiling | `<bytes>` | Measured / vendor / unknown. Load-bearing or advisory? |
| Verify | `<script or method>` | |
| Who chunks | you / the platform / nobody | |
| Chunks an agent reads | | The row that decides the ceiling |
| Native upload formats | | Anything else is tolerated, not supported |
| Override layer | | And whether it actually reaches the agent |
| Glossary | | |
| API write path | | |
| Native skills | | |
| Admin levers | | What you cannot change yourself |

## How the numbers were established

<The experiments, with their results. Someone will want to repeat them.>

## What fails silently here

<The most valuable section. What looks fine and is not: an upload that succeeds but is not
retrievable, a setting with no UI, a limit that measures something other than what it appears
to. Every platform has these and none of them document them.>

## Verification

<The exact command, and what a pass looks like.>

## What to raise with an admin

<Numbered. Each one should name who else it affects, because a setting that degrades every
agent in the tenant is a different conversation from one that affects yours.>
