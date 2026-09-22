"""Shared pieces for building corpus files.

The invariant everything here exists to enforce: **every part of every source
must be retrievable.** What that costs depends on the platform, so the number
lives in a platform profile rather than here. On a platform that chunks
invisibly and lets an agent read only the first chunk, it costs a ceiling small
enough that each file is one chunk. On a platform that does not chunk, it may
cost nothing.

See ../platforms/ for the profiles, and ../platforms/generic.md for what to
assume when nobody has measured yours.
"""
import re

# Bytes of extracted text. A DEFAULT, not a finding: a platform profile is
# expected to override it, and `ceiling` in project.yaml overrides both. 60,000
# is small enough to be a single chunk on every chunker measured so far, and it
# leaves room for the part header and for a release adding content without
# silently pushing a part over the line.
#
# Do not raise it because a build complained. Raising it is a claim about a
# platform, and the way to make that claim is to measure it and write a profile.
SINGLE_CHUNK_CEILING = 60_000

# How close to the ceiling a file may get before the build complains. A file
# inside this band still passes, but it is reported, because the next release
# is what pushes it over.
WARN_BAND = 5_000


def demote_headings(text, levels=1):
    """Push every ATX heading down by `levels`, leaving fenced code alone."""
    out, in_fence = [], False
    for line in text.split("\n"):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            out.append(line)
            continue
        if not in_fence:
            m = re.match(r"^(#{1,6})(\s+)(.*)$", line)
            if m:
                line = "#" * min(6, len(m.group(1)) + levels) + m.group(2) + m.group(3)
        out.append(line)
    return "\n".join(out)


def resolve_link_refs(text):
    """Inline reference-style links, then drop the definition block.

    A corpus file is read as flat text, so a trailing list of `[ref]: url`
    definitions is noise, and stripping it without inlining leaves every
    `[text][ref]` dangling.
    """
    defs = {}
    for m in re.finditer(r"^\[([^\]]+)\]:\s*(\S+).*$", text, re.M):
        defs[m.group(1).lower()] = m.group(2)
    if defs:
        def sub(m):
            label = (m.group(2) or m.group(1)).lower()
            url = defs.get(label)
            return f"[{m.group(1)}]({url})" if url else m.group(1)
        text = re.sub(r"\[([^\]]+)\]\[([^\]]*)\]", sub, text)
    text = re.sub(r"^\[[^\]]+\]:\s*\S+.*$\n?", "", text, flags=re.M)
    return text


def strip_markup(text):
    """Remove what carries nothing once the file is read as plain text.

    Images keep their alt text. The alt is often the only name a step gives an
    icon it tells you to click, so dropping the whole reference leaves
    sentences like "click and then select Settings".
    """
    text = re.sub(r"<!--+.*?--+>", "", text, flags=re.S)          # HTML comments

    # A line that is nothing but an image is a screenshot. Its alt text is a
    # caption, and left behind it becomes an orphan noun on its own line
    # ("Login", "Web Interface") that reads as stray content.
    text = re.sub(r"^[ \t]*!\[[^\]]*\]\([^)]*\)[ \t]*$\n?", "", text, flags=re.M)

    # An image inside a sentence is an icon being named. Its alt text is often
    # the only word identifying what to click, so it stays.
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return text


def flatten_admonitions(text):
    """mkdocs `!!! note` blocks mean nothing as plain text; label and dedent."""
    out, i, lines = [], 0, text.split("\n")
    while i < len(lines):
        m = re.match(r"^(\s*)!!!\s+(\w+)\s*(.*)$", lines[i])
        if not m:
            out.append(lines[i]); i += 1; continue
        indent, kind, inline = m.group(1), m.group(2), m.group(3).strip()
        label = f"**{kind.capitalize()}:**"
        out.append(f"{indent}{label} {inline}".rstrip())
        i += 1
        while i < len(lines) and (lines[i].strip() == "" or lines[i].startswith(indent + "    ")):
            if lines[i].strip() == "":
                if i + 1 < len(lines) and lines[i + 1].startswith(indent + "    "):
                    out.append(""); i += 1; continue
                break
            out.append(indent + lines[i][len(indent) + 4:])
            i += 1
    return "\n".join(out)


def join_areas(items):
    """Readable list of part areas. Semicolons only when items contain commas."""
    items = list(items)
    if len(items) == 1:
        return items[0]
    sep = "; " if any("," in i for i in items) else ", "
    return sep.join(items[:-1]) + (sep if len(items) > 2 else " ") + "and " + items[-1]


def render_part_header(*, title, product_sentence, covers, siblings, version_line):
    """The block that makes one part self-identifying.

    A retrieved chunk arrives without its neighbours, so each part has to say
    on its own which product, which version, which document and which part it
    is, and where the rest lives. Prose, not a metadata table: the house style
    across the existing corpus is a `#` title then sentences.

    Kept deliberately short. Longer and it competes with real content for chunk
    space and reads as a near-duplicate across every part, which is its own
    retrieval problem.
    """
    block = (
        f"# {title}\n\n"
        f"{product_sentence}\n\n"
        f"{covers}\n\n"
        f"{siblings}\n\n"
        f"{version_line}\n"
    )
    return block


def check_parts(parts, ceiling=SINGLE_CHUNK_CEILING):
    """parts: list of (name, text). Returns (problems, warnings, rows)."""
    problems, warnings, rows = [], [], []
    for name, text in parts:
        n = len(text.encode("utf-8"))
        rows.append((name, n))
        if n > ceiling:
            problems.append(
                f"{name}: {n:,} bytes exceeds the single-chunk ceiling of {ceiling:,}"
            )
        elif n > ceiling - WARN_BAND:
            warnings.append(
                f"{name}: {n:,} bytes, within {ceiling - n:,} of the ceiling"
            )
    return problems, warnings, rows


def report(parts, label, ceiling=SINGLE_CHUNK_CEILING):
    """Print the size table and return a non-zero-worthy problem list."""
    problems, warnings, rows = check_parts(parts, ceiling)
    total = sum(n for _, n in rows)
    print(f"{label}: {len(rows)} part(s), {total:,} bytes total")
    for name, n in rows:
        flag = "  FAIL" if n > ceiling else ("  warn" if n > ceiling - WARN_BAND else "")
        print(f"    {n:>7,}  {name}{flag}")
    for w in warnings:
        print(f"  warn: {w}")
    return problems
