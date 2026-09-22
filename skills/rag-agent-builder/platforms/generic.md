# Platform profile: generic

The default for a platform nobody has measured. It assumes nothing, which means it assumes the
worst: that the platform chunks invisibly, tells you nothing about how, and gives an agent less
of each file than you uploaded.

Selected with `platform: generic` in `project.yaml`, or by leaving `platform` unset.

Use this until you have run the measurements at the foot of this file. Then write a real profile
from `profile-template.md` and stop using this one.

## Capabilities

| | | |
|---|---|---|
| Ceiling | 60,000 bytes of extracted text | **Advisory, not measured.** A starting number, not a law |
| Verify | `reach_probe.py` | The only check that works without platform metadata |
| Who chunks | Assume the platform, invisibly | Unknown |
| Chunks an agent reads | Assume fewer than all of them | Unknown, and the assumption that matters |
| Native upload formats | Assume plain text and PDF | Unknown |
| Override layer | Assume none | Put every fact the agent must state into a document |
| Glossary | Assume none | |
| API write path | Assume none | Prepare locally, upload by hand |
| Native skills | Assume none | |
| Admin levers | Assume none | The only remedy for a bad source is deleting it |

## Why the ceiling is still here

A platform that chunks at all loses the tail of a long file first, and a platform that does not
chunk has a context budget that a long file eats. Neither case is improved by a 400KB document.
60,000 bytes is small enough to be one chunk on every chunker measured so far and large enough
that a document does not shatter into fragments that each say too little.

It is a default, not a finding. The profile's job is to replace it with a number you measured.

## Verification

`check-chunk-counts.py` does not apply: it reads a record format this profile cannot assume
exists. `reach_probe.py` replaces it and is strictly more honest, because it measures what an
agent can actually retrieve rather than inferring it from metadata.

```
python3 scripts/reach_probe.py --emit  --parts staging/<date>/files --out probes.json
# ask the agent each question, paste the answers back
python3 scripts/reach_probe.py --score --probes probes.json --answers answers.json
```

Any part whose tail does not come back is unreachable. Shrink the ceiling and rebuild.

## Measure these, then write a real profile

Each is an experiment, not a question for a vendor doc. The answers vendors publish describe
upload acceptance far more often than they describe retrieval.

1. **Where does chunking start?** Upload the same content at several sizes and find the size at
   which the tail stops being retrievable. That boundary, minus a margin, is your ceiling.
2. **How much does an agent read?** Put a distinctive string at the very end of a long file and
   ask for it. This is the reach probe, run once by hand.
3. **Is there an override layer?** If the platform has one, ask the agent for the verbatim title
   of an entry whose content is in no document. If it cannot answer, the layer is inert and every
   fact has to live in a document instead.
4. **What formats are native?** Uploading a format the platform merely tolerates means no
   heading-aware anything, whatever the file extension suggests.
5. **What can an admin change that you cannot?** Find this before you need it.
