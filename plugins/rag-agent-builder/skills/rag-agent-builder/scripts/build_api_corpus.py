#!/usr/bin/env python3
"""Build an API reference corpus from a bundled OpenAPI spec.

Deterministic, no network. Most of the output is a projection of the OpenAPI
document; the rest is hand-authored fragments named by the overrides file.
Self-checks run before anything is written.

Nothing here knows which product it is building. Every product string, every
fragment name and every correction lives in `<parts>/overrides.yaml`, so a
second API is a second parts directory rather than a second script.

  python3 build_api_corpus.py \
      --spec  path/to/api-bundled.yaml \
      --parts outputs/knowledge-agent/build/api-reference-parts \
      --out   outputs/knowledge-agent/staging/<date>/files
"""
import argparse
import json
import pathlib
import re
import sys
import textwrap

import yaml

from corpus_common import (SINGLE_CHUNK_CEILING, join_areas, render_part_header, report)

METHODS = ("get", "post", "put", "delete", "patch")


# ---------------------------------------------------------------- spec model

def security_class(op, default=None):
    """Which auth an operation needs.

    An absent `security` key inherits the document-level default; `security: []`
    is an explicit opt out. Treating the two alike prints "no authentication" on
    every operation of a spec that declares its scheme once at the top, which is
    how many specs are written.
    """
    sec = op.get("security", default)
    if sec is None:
        return "none"
    names = sorted(k for d in sec for k in d)
    return ",".join(names) if names else "none"


def load_operations(spec):
    ops = []
    default_security = spec.get("security")
    for path, item in spec["paths"].items():
        for method, op in item.items():
            if method not in METHODS:
                continue
            params = op.get("parameters") or []
            ops.append({
                "path": path,
                "method": method.upper(),
                "tag": (op.get("tags") or ["Other"])[0],
                "summary": op.get("summary", "").strip(),
                "description": (op.get("description") or "").strip(),
                "security": security_class(op, default_security),
                "has_csrf_param": any(p.get("name") == "x-csrf-token" for p in params),
                "request_ref": ref_name(
                    (op.get("requestBody", {}).get("content", {})
                       .get("application/json", {}).get("schema", {}) or {}).get("$ref")),
                "responses": {
                    code: ref_name((r.get("content", {}).get("application/json", {})
                                     .get("schema", {}) or {}).get("$ref"))
                    for code, r in (op.get("responses") or {}).items()
                },
            })
    return ops


def ref_name(ref):
    return ref.split("/")[-1] if ref else None


def type_of(prop):
    t = prop.get("type")
    if t == "array":
        return "array"
    if t:
        return t
    if "$ref" in prop:
        return ref_name(prop["$ref"])
    return "object"


def field_rows(schema):
    """One row per top-level property: name, type, required, notes."""
    if not schema:
        return []
    required = set(schema.get("required") or [])
    rows = []
    for name, prop in (schema.get("properties") or {}).items():
        note = (prop.get("description") or "").strip().replace("\n", " ")
        note = re.sub(r"\s+", " ", note).rstrip(".")
        enum = prop.get("enum") or (prop.get("items", {}) or {}).get("enum")
        if enum:
            vals = ", ".join(f"`{v}`" for v in enum)
            note = f"{note}. One of {vals}" if note else f"One of {vals}"
        rows.append({
            "name": name,
            "type": type_of(prop),
            "required": "yes" if name in required else "no",
            "note": note or "-",
        })
    return rows


def example_payload(schema, schemas):
    """Prefer the spec's own example, else synthesize from the properties."""
    if not schema:
        return None
    xe = schema.get("x-examples")
    if isinstance(xe, dict) and xe:
        return list(xe.values())[0]
    required = set(schema.get("required") or [])
    props = schema.get("properties") or {}
    if not props:
        return None
    out = {}
    for name, prop in props.items():
        if name not in required and len(out) >= 4:
            continue
        out[name] = synth_value(name, prop, schemas)
    return out or None


def synth_value(name, prop, schemas):
    if "example" in prop and prop["example"] not in ("", None):
        return prop["example"]
    enum = prop.get("enum")
    if enum:
        return enum[0]
    t = type_of(prop)
    if t == "array":
        item = prop.get("items", {}) or {}
        return [synth_value(name, item, schemas)]
    if t == "number" or t == "integer":
        return 0
    if t == "boolean":
        return True
    if t == "object" or t in schemas:
        return {}
    return name.upper()


# ------------------------------------------------------------ rendering bits

def table(headers, rows):
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(r) + " |")
    return "\n".join(out)


def chunk(seq, size):
    return [seq[i:i + size] for i in range(0, len(seq), size)]


def render_index_tables(ops, cfg):
    """One small table per functional area. Never one long table."""
    by_tag = {}
    for o in ops:
        by_tag.setdefault(o["tag"], []).append(o)
    blocks = []
    for tag in sorted(by_tag, key=lambda t: (-len(by_tag[t]), t)):
        rows = []
        for o in sorted(by_tag[tag], key=lambda x: x["path"]):
            auth = cfg["auth_labels"][o["security"]]
            rows.append([f"`{o['method']} {cfg['path_prefix']}{o['path']}`",
                         o["summary"], auth])
        body = [f"## {cfg['heading_prefix']} operations: {tag}", "",
                f"The {tag} area of the {cfg['api_label']} holds "
                f"{len(rows)} operation{'s' if len(rows) != 1 else ''}. "
                f"All paths are relative to `{cfg['production_base']}`.", ""]
        for part in chunk(rows, 8):
            body.append(table(["Operation", "Summary", "Token"], part))
            body.append("")
        blocks.append("\n".join(body).rstrip())
    return blocks


def render_operation(o, schemas, cfg):
    title = (f"## {cfg['heading_prefix']}: {o['method']} "
             f"{cfg['path_prefix']}{o['path']} ({o['summary']})")
    lines = [title, ""]

    desc = re.sub(r"\n+", " ", o["description"]).strip()
    desc = re.sub(r"\s+", " ", desc)
    if desc:
        lines += [desc, ""]

    headers = ["Content-Type: application/json"] if o["request_ref"] else []
    headers += cfg["auth_headers"][o["security"]]
    lines.append("```http")
    lines.append(f"{o['method']} {cfg['production_base']}{o['path']}")
    lines += headers
    lines.append("```")
    lines.append("")

    note = (cfg.get("security_notes") or {}).get(o["security"])
    if note:
        lines += [note, ""]

    schema = schemas.get(o["request_ref"]) if o["request_ref"] else None
    rows = field_rows(schema)
    if rows:
        req = [r["name"] for r in rows if r["required"] == "yes"]
        if req:
            named = ", ".join(f"`{n}`" for n in req)
            lines.append(f"Request body. Required: {named}.")
        else:
            lines.append("Request body. No field is required.")
        lines.append("")
        for part in chunk(rows, 8):
            lines.append(table(
                ["Field", "Type", "Required", "Notes"],
                [[f"`{r['name']}`", r["type"], r["required"], r["note"]] for r in part]))
            lines.append("")
        ex = example_payload(schema, schemas)
        if ex:
            lines += ["```json", json.dumps(ex, indent=4), "```", ""]
    elif o["request_ref"]:
        lines += ["This operation takes a JSON request body.", ""]

    ok = o["responses"].get("200")
    if o["path"] in cfg["response_field_ops"] and ok and ok in schemas:
        rrows = field_rows(schemas[ok])
        if rrows:
            lines.append("The 200 response carries these top-level fields.")
            lines.append("")
            for part in chunk(rrows, 8):
                lines.append(table(
                    ["Field", "Type", "Notes"],
                    [[f"`{r['name']}`", r["type"], r["note"]] for r in part]))
                lines.append("")

    unauth = cfg["unauthorized"][o["security"]]
    lines.append(
        "Responses: 200 on success; 400 with a numeric `status`, a `code` such as "
        f"`VALIDATION_FAILED`, and a `message` array; 401 when {unauth}.")
    return "\n".join(lines).rstrip()


# ------------------------------------------------------------------ cookbook

def prepare_cookbook(description, cfg):
    lines = description.split("\n")
    close_after = cfg.get("unclosed_fence_close_after_line")
    if close_after:
        target = lines[close_after - 1]
        indent = re.match(r"\s*", target).group(0)
        lines.insert(close_after, indent + "```")
    text = "\n".join(lines)

    for fix in cfg.get("cookbook_fixes", []):
        text = text.replace(fix["from"], fix["to"])
    for fix in cfg.get("cookbook_regex_fixes", []):
        text = re.sub(fix["re"], fix["to"], text)

    # Anchors are dead links once the document is chunked. Keep the link text.
    text = re.sub(r"\[([^\]]+)\]\(#[^)]*\)", r"\1", text)
    # Normalize fence languages so rendering is predictable.
    text = re.sub(r"^(\s*)```JSON\s*$", r"\1```json", text, flags=re.M)
    text = re.sub(r"^(\s*)```Python\s*$", r"\1```python", text, flags=re.M)

    # A published block that is an explicitly partial response, with an elision
    # in place of the omitted fields, is not parseable JSON and is not labelled
    # as if it were. Decided by parsing, not by matching a known block.
    def relabel(m):
        indent, body = m.group(1), m.group(2)
        try:
            json.loads(textwrap.dedent(body))
        except ValueError:
            return f"{indent}```text\n{body}{indent}```"
        return m.group(0)

    text = re.sub(r"^([ \t]*)```json\n(.*?)^\1```", relabel, text, flags=re.S | re.M)
    return text


def split_recipes(text, cfg):
    """Every H3 in the published cookbook becomes one standalone H2 recipe."""
    heads = [(m.start(), len(m.group(1)), m.group(2).strip())
             for m in re.finditer(r"^(#{2,6})\s+(.*)$", text, re.M)]
    recipes = []
    for i, (pos, level, name) in enumerate(heads):
        if level != 3:
            continue
        end = len(text)
        for pos2, level2, _ in heads[i + 1:]:
            if level2 <= 3:
                end = pos2
                break
        body = text[pos:end]
        body = re.sub(r"^#{3}\s+.*$", "", body, count=1, flags=re.M).strip()
        body = re.sub(r"^#{4}\s+", "### ", body, flags=re.M)
        kind = ("device recipe" if name in cfg["device_recipes"] else "recipe")
        title = f"## {cfg['heading_prefix']} {kind}: {name}"
        tail = ("\nIn this recipe, any all-capitalized value is a placeholder. "
                "`X_MYSTQ_TOKEN` and `X_CSRF_TOKEN` are the `token` and `csrf_token` "
                "values returned by `POST /api/v2/user/login`."
                if kind == "recipe" else
                "\nIn this recipe, any all-capitalized value is a placeholder. "
                "`AUTH_TOKEN` is the token returned by "
                "`POST /api/v1/device/register`.")
        recipes.append(f"{title}\n\n{body}\n{tail}")
    return recipes


# --------------------------------------------------------------- self-checks

def scanner_patterns(pattern_file):
    """Read a scan pattern file's own patterns rather than restating them.

    Same schema scan.py uses, so the build enforces exactly what the gate
    enforces and the two cannot drift apart.
    """
    spec = yaml.safe_load(pathlib.Path(pattern_file).read_text(encoding="utf-8"))
    return [(e["name"], e["re"]) for e in (spec.get("patterns") or [])]


def self_check(doc, ops, cfg, scan_files, problems, spec_paths=()):
    lines = doc.split("\n")

    # Any /api path named anywhere in the document must be a real path in the
    # spec. This is what catches a wrong path in the published recipe prose.
    known = set(spec_paths) | set(cfg.get("extra_valid_paths") or [])
    for m in sorted(set(re.findall(cfg["path_guard_re"], doc))):
        cleaned = m.rstrip("/")
        if cleaned not in known:
            problems.append(f"path {cfg['path_prefix']}{cleaned} is named in the "
                            "output but is not an operation in the spec")

    # Headers that must travel together. A token line printed without the
    # companion the API requires is a recipe that returns 403.
    for first, second in cfg.get("paired_headers") or []:
        for i, line in enumerate(lines):
            if line.strip().startswith(first):
                nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
                if not nxt.startswith(second):
                    problems.append(f"line {i+1}: {first} not followed by {second}")

    for host, want in (cfg.get("host_counts") or {}).items():
        n = doc.count(host)
        if n != want:
            problems.append(f"{host} appears {n} times, expected exactly {want}")
    for placeholder in cfg.get("forbidden_literals") or []:
        if placeholder in doc:
            problems.append(f"{placeholder} survived into the output")

    n_ops = len(re.findall(rf"^## {re.escape(cfg['heading_prefix'])}: ", doc, re.M))
    if n_ops != len(ops):
        problems.append(f"emitted {n_ops} operation sections, spec has {len(ops)}")

    fences = [l for l in lines if l.strip().startswith("```")]
    if len(fences) % 2:
        problems.append(f"unbalanced code fences: {len(fences)}")

    i = 0
    while i < len(lines):
        if lines[i].startswith("|"):
            j = i
            while j < len(lines) and lines[j].startswith("|"):
                j += 1
            body_rows = (j - i) - 2
            if body_rows > 8:
                problems.append(f"line {i+1}: table has {body_rows} body rows, limit 8")
            i = j
        else:
            i += 1

    heads = re.findall(r"^#{1,6} .*$", doc, re.M)
    dupes = {h for h in heads if heads.count(h) > 1}
    if dupes:
        problems.append(f"duplicate headings: {sorted(dupes)[:3]}")

    for scan_file in scan_files:
        label = pathlib.Path(scan_file).name
        for name, pat in scanner_patterns(scan_file):
            try:
                rx = re.compile(pat, re.I)
            except re.error:
                continue
            for i, line in enumerate(lines):
                if rx.search(line):
                    problems.append(f"{label}: {name}, line {i+1}: {line[:110]}")
                    break
    return problems


# -------------------------------------------------------------------- driver

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--parts", required=True)
    ap.add_argument("--out", required=True, help="output DIRECTORY")
    ap.add_argument("--ceiling", type=int, default=SINGLE_CHUNK_CEILING)
    ap.add_argument("--redactions", default=None,
                    help="shared YAML of {re, to}, applied on top of the overrides")
    ap.add_argument("--scan-patterns", action="append", default=[],
                    metavar="FILE",
                    help="scan pattern YAML (repeatable). The generated document "
                         "is held to the same patterns that gate the upload.")
    args = ap.parse_args()

    parts_dir = pathlib.Path(args.parts)
    cfg = yaml.safe_load((parts_dir / "overrides.yaml").read_text(encoding="utf-8"))
    shared_redactions = []
    if args.redactions:
        shared_redactions = yaml.safe_load(
            pathlib.Path(args.redactions).read_text(encoding="utf-8"))["redactions"]

    spec = yaml.safe_load(pathlib.Path(args.spec).read_text(encoding="utf-8"))
    schemas = spec.get("components", {}).get("schemas", {})
    ops = load_operations(spec)

    problems = []
    csrf_class = cfg.get("csrf_security_class")
    if csrf_class:
        for o in ops:
            if o["security"] == csrf_class and not o["has_csrf_param"]:
                problems.append(f"{o['method']} {o['path']} takes a user token but "
                                "declares no required x-csrf-token header")

    ops.sort(key=lambda o: (o["tag"], o["path"]))

    def fragments(names):
        return [(parts_dir / n).read_text(encoding="utf-8").strip() for n in (names or [])]

    concepts = fragments(cfg["concept_parts"]) + render_index_tables(ops, cfg)
    operations = [render_operation(o, schemas, cfg) for o in ops]

    # Some specs publish a task cookbook inside info.description. A spec that
    # carries no cookbook simply has no recipes part.
    recipes = []
    if cfg.get("cookbook_in_description"):
        recipes += split_recipes(prepare_cookbook(spec["info"]["description"], cfg), cfg)
    recipes += fragments(cfg.get("recipe_parts"))

    ver = cfg["version_label"]
    version_line = (parts_dir / cfg["version_line_part"]).read_text(encoding="utf-8").strip()
    n = len(ops)
    product_sentence = cfg["product_sentence"].format(n=n)
    groups = [(g["area"], g["covers"].format(n=n),
               {"concepts": concepts, "operations": operations, "recipes": recipes}[g["blocks"]])
              for g in cfg["groups"]]
    groups = [g for g in groups if any(g[2])]
    total = len(groups)
    others = {i: join_areas([g[0].lower() for j, g in enumerate(groups) if j != i])
              for i in range(total)}

    emitted = []
    for i, (area, covers, blocks) in enumerate(groups):
        header = render_part_header(
            title=f"{cfg['doc_title']} {ver}, part {i + 1} of {total}, {area}",
            product_sentence=product_sentence,
            covers=covers,
            siblings=(f"This is one part of the {cfg['doc_title']} {ver}, split so each "
                      f"part is retrievable on its own. The other parts cover {others[i]}."),
            version_line=version_line,
        )
        doc = header + "\n---\n\n" + "\n\n".join(b for b in blocks if b) + "\n"
        for r in shared_redactions + (cfg.get("redactions") or []):
            doc = re.sub(r["re"], r["to"], doc)
        slug = re.sub(r"[^a-z0-9]+", "-", area.lower()).strip("-")
        emitted.append((f"{cfg['file_prefix']}-{i + 1}-{slug}.md", doc))

    whole = "\n\n".join(d for _, d in emitted)
    self_check(whole, ops, cfg, args.scan_patterns, problems, list(spec["paths"]))
    problems += report(emitted, f"{cfg['doc_title']} {ver}", args.ceiling)

    if problems:
        print(f"SELF-CHECK FAILED: {len(problems)} problem(s)", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1

    out_dir = pathlib.Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, doc in emitted:
        (out_dir / name).write_text(doc, encoding="utf-8")
    print(f"\nok  {len(emitted)} parts written to {out_dir}")
    print(f"    {len(ops)} operations, "
          f"{len(re.findall(r'^## ', whole, re.M))} H2 chunk units")
    return 0


if __name__ == "__main__":
    sys.exit(main())
