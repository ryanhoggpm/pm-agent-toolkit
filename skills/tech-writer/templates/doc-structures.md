# Document structures

One structure per document type. These are the shapes `/tech-writer` drafts into; each exists to fix a specific way engineering-written docs fail users.

## Release notes

Fixes: critical warnings buried mid-prose where scanning readers miss them.

```markdown
# [Product] Firmware [Version] Release Notes
[Date]

## Before You Upgrade: Read This First
[Everything that causes failure if missed. Step-upgrade paths HERE, with
download links to intermediate versions. Firmware filename and checksum HERE.]

**Step upgrade required if you are on firmware older than [X]:**
1. Upgrade to [intermediate version] first: [download link]
2. Then upgrade to [target version]: [download link]
Skip this and the upgrade will fail.

**Check these dependencies:**
- [Tool]: minimum version [X] required, and who this applies to ("If you use...")

## What's New
[User-impact framing, one sentence per item: what changed and what it means
for you. Grouped by who it affects, never by internal component.]

## What to Watch Out For (Known Issues)
[Per issue: what happens, who is affected, workaround or "no workaround; fix
planned for [version]". Severity stated.]

## Fixed in This Release
[One line per fix, only fixes a user might recognize.]

## How to Get Help
[Actual support contact method, firmware download link, prior versions link.]
```

## User guide topic

Fixes: docs organized by menu path instead of by task; no prerequisites; no way to tell whether it worked.

```markdown
## [Verb-phrase title: "Configure a Serial Port for Console Access"]

**What this does:** [One sentence: why would I do this?]
**Who this is for:** [audience filter, if not everyone]

### Before You Begin
- [Access/permissions required]
- [Information to have ready]
- [Anything that must be done first]

### Steps
1. [Specific action: where to navigate, what to type.]
   *After this step you should see: [expected result.]*
2. ...

> **If you see an error here:** [what it means, what to do]

### Verify It Worked
[How to confirm the configuration is active.]

### What to Do If It Doesn't Work
[The 2-3 most common failure modes, with resolution steps.]
```

## Quick-start guide

Fixes: new users drowning in options before first value. One path, most-common choices pre-made, under 30 minutes.

```markdown
# Get Started with [Product]: [Outcome] in 30 Minutes

**What you need:** [hardware / access / credentials]
**Time required:** [X minutes]

## Step 1: [First action]
[Exactly what to do.]
Done when: [specific expected state]

## Step 2: ...

## You're Set Up
[What they can now do.]

## Next Steps
[User guide link for depth; support link if something didn't work.]
```

## Upgrade guide

The highest-risk document type; mistakes cause outages.

```markdown
# Upgrading [Product] to Version [X]
**Estimated time:** [X] · **Downtime required:** [Yes/No, how long] · **Reversible:** [Yes/No, how]

## Critical: Read Before You Start
[Step-upgrade requirements with exact versions and links. Compatibility.
Backup requirements.]

## What You Need
[Current-version check method; required access; exact filenames and checksums.]

## Before You Upgrade
1. [Back up configuration: specific steps]
2. [Verify current version: specific command or UI location]
3. [Verify the file checksum]

## Upgrade Steps
[Numbered, with expected output at each stage.]

## Verify the Upgrade
[The version string that should now show, and where.]

## If the Upgrade Fails
[Recovery path; how to boot the previous firmware bank; who to contact, with
the actual contact method.]
```

## Demo script (for field engineers / partners)

Fixes: demos that tour features instead of making the prospect feel their problem being solved.

```markdown
# Demo: [Outcome-framed title]
**Duration:** [X min] · **Audience:** [who] 
**Objective:** by the end, the prospect should [feel/understand/decide X]

## Setup Checklist (before the call)
- [ ] [Environment ready, credentials verified, scenario configured]
- [ ] [Backup demo environment ready]

## The Story (say this before touching the product)
[2-3 sentences establishing the problem in the prospect's world.]

## Demo Flow
### Scene 1: [name]
**What you do:** [actions]
**What you say:** "[conversational script, not a feature list]"
**What they see:** [expected screen]
**Question to ask:** "[engagement question that surfaces objections]"

## Common Objections
| Objection | Response |
|---|---|
| "We already have [competitor]" | [specific differentiation] |

## If Something Goes Wrong
[Specific failure → recovery action; unresponsive product → backup plan]

## Close
[What to offer next; the leave-behind to send after.]
```

## Troubleshooting doc and partner brief

Follow the user-guide topic shape: symptom as a verb-phrase-adjacent title ("Fix X when Y"), who it affects, diagnosis steps with expected outputs, resolution, escalation with real contact info. Partner briefs stay at positioning depth: what it is, who buys it, the three questions prospects ask, where to send them next; no datasheet specifics.
