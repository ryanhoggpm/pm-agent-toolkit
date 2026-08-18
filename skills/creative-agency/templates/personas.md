# Persona panel (fill this in once per audience)

`/creative-agency` runs every draft through the personas defined here. The panel is yours to build; the skill only supplies the process. Weights must sum to 100% and drive how conflicts between personas get resolved.

## The schema

Define 3-6 personas. Richer fields make sharper reviews; the cringe triggers and humor register matter more than the demographics.

```markdown
### [Name], [Role]
**Audience weight: N%**

Background: [2-4 sentences. Tenure, scale they operate at, what their week actually
looks like, one detail that proves they exist (a deadline, a fleet, a budget line).]

Pain points: [3-5, specific to their job, not generic]

Cringe triggers (content that makes them stop reading): [3-5 words/phrases/moves]

What makes them keep reading: [3-4 signals]

What makes them share it: [1-2 things]

Humor register: [What kind of joke lands, what kind backfires]

Trust posture: [What they believe about your product category's promises, and what
would move them]
```

Not every persona needs every field. A budget-holder persona may need "what she skips" more than a humor register; a channel persona may need "what he needs to handle objections" instead of pain points.

## Example panel (fictional): Coppermine Systems, B2B device management

Five voices for marketing aimed at network and infrastructure buyers. Weights reflect who the content must convince first.

### Priya, Senior Network Engineer
**Audience weight: 40%**

Background: 12 years in. Manages devices across 60+ sites. Currently running a legacy CM-400 fleet against an end-of-sale deadline. Half her week goes to tasks that shouldn't need a senior engineer. Has been paged at 2am enough times to spot a vendor who's never been paged at 2am.

Pain points: products that need manual configuration at scale; vendor marketing written by someone who hasn't done her job; management tools that need their own out-of-band management; automation claims that don't survive past the demo.

Cringe triggers: "seamless" / "effortless" / "robust" / "next-generation"; any sentence explaining her own domain to her; the category's stock disaster opener she's heard 400 times; features that are obviously not shipping yet.

What makes her keep reading: technical specificity (real tool names, real version numbers); language that treats her as the expert; proof the vendor has been inside a real network; a line that makes her nod, not laugh.

What makes her share it: a description of her exact pain, stated plainly without drama, in a peer's voice.

Humor register: dry, dark, specific. Never setup/punchline. A knowing observation: "Port 14 is labeled 'firewall-rtp-3'. The firewall was decommissioned in July."

Trust posture: cautious on automation; earned through demonstrated outcomes. Accepts human-in-the-loop today; will consider human-on-the-loop after 12-18 months of it working.

### Warren, IT Operations Manager
**Audience weight: 25%**

Background: Manages 3 network engineers. Owns the budget line. Gets asked quarterly by his VP why this infrastructure exists. Has survived two compliance audits he never wants to repeat.

Pain points: senior-engineer time eaten by rote tasks; any outage that escalates to his VP; budget justification without ROI data; audit prep that takes weeks.

What he responds to: staff hours saved, with numbers; "your team will spend less time on X"; risk reduction stated plainly; audit-trail and compliance language.

What he skips: CLI commands or syntax; feature names without outcomes attached; anything needing deep domain knowledge to evaluate.

### Sam, DevOps/SRE Engineer
**Audience weight: 20%**

Background: Hybrid network/automation role. Thinks in pipelines. Uses Ansible, Terraform, and NetBox daily. Won't read product marketing that doesn't mention programmability in the first 30 seconds.

Pain points: vendor "REST APIs" that are five endpoints and read-only; products that can't be scripted; anything proprietary where a community standard exists.

What he responds to: the OpenAPI spec version, not "REST API"; the actual Ansible collection name, not "Ansible support"; evidence the integration is implemented, not theoretically supported; "works with your stack" framing.

### Ingrid, Security Engineer
**Audience weight: 10%**

Background: Reviews infrastructure purchases for security posture. Will derail a purchase over credential handling or a missing audit trail.

Pain points: appliances storing credentials on-device; no session audit trail; access paths that bypass the IdP; products that assume the management network is trusted.

What she responds to: hardware root of trust; tamper-evident session logs; IdP integration named by protocol; encrypted storage with the spec stated; zero-trust posture signals.

### Leo, Channel Partner / VAR Rep
**Audience weight: 5% (primary for partner-facing pages)**

Background: Sells Coppermine into enterprise accounts. Not the buyer; the person who arms the buyer.

What he needs: a clean SKU table with clear differentiation; the legacy-to-current upgrade path with end-of-sale dates; the platform story vs. the main competitor; enough technical depth to deflect common objections without a callback.
