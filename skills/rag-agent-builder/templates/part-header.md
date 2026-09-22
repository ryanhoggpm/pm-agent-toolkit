# Part header template

Every generated part opens with this block. It is the only thing making a retrieved
chunk self-identifying, because a chunk arrives without its neighbours and, on the
plain-text upload path, possibly without its heading structure carrying any weight.

Five sentences. Prose, not a metadata table. Under about 800 bytes.

`scripts/split_corpus_file.py` renders it from `project.yaml`; the shape below is what
it produces, and what a hand-written document should match.

---

## The shape

```markdown
# {title}, part {n} of {m}

{product_sentence}

This part covers {the section this part holds}.

This is one part of the {title}, split so each part is retrievable on its own.
Across its {m} parts the document covers {areas}.

{version_line}
```

## The five fields

| Field | Comes from | Rule |
|---|---|---|
| `title` | `documents[].title` | The document's own name, identical across its parts |
| `n` of `m` | the splitter | So a reader knows a continuation is a continuation |
| the section | the first heading packed into the part | What this part is about, in a few words |
| `product_sentence` | `product_sentence` in `project.yaml` | One sentence, **verbatim in every part of every document** |
| `areas` | `documents[].areas` | The whole document's scope, described not enumerated |
| version line | `version_line` | What release this describes, and when it was current |

## Example (fictional): Coppermine Systems

Real output from `split_corpus_file.py`, for Coppermine Systems, the fictional
company this skill's examples use throughout:

```markdown
# CM-900 User Guide, part 4 of 6

The CM-900 is a rack-mounted console server that manages network equipment over
serial and network connections, paired with the Fleet Cloud management service.

This part covers chapter 4, Authentication and user accounts.

This is one part of the CM-900 User Guide, split so each part is retrievable on
its own. Across its 6 parts the document covers installation, network and port
configuration, accounts, monitoring and maintenance.

_Describes CM-900 firmware 9.2, current as of March 2027._
```

## Why each rule is there

**The product sentence is verbatim everywhere.** A part retrieved on its own has to
establish what the product even is. Varying the wording per document gives the agent
several slightly different definitions to reconcile.

**Siblings are described by area, never enumerated.** A nineteen-part document that
lists all nineteen siblings in every header spends hundreds of bytes per file on
near-duplicate text, which competes with real content and blurs retrieval. One clause
naming the areas does the same job.

**A continuation says so.** When one chapter spans three parts, the splitter repeats
the parent heading above each continuation as `{chapter}, continued`, so a part that
opens mid-procedure is still placeable.

**Prose, not YAML.** A metadata block inside an uploaded markdown file is content the
agent can read aloud. Anything you put in the file, assume a customer may hear.

**No page numbers, no "see above".** Cross-references to a page or a neighbouring
section mean nothing once the document is parts.
