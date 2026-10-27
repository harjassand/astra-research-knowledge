"""Lossless operation views and conservative premise inspection; no inferred proofs."""
import re

from knowledge.model import digest, flatten, tokens

CARD_LABEL = re.compile(r"(?i)^\s*(?:source-reported\s+)?(exact claim|claim|theorem|interface(?: and assumptions)?|assumptions|boundaries|boundary|costs?(?: and information boundary)?|proof spine|proof|construction|next obligation|evidence|references)\s*(?:\([^\n]*?\))?\s*(?:\||:|\.|$)")


def card_sections(record):
    """Locate existing prose; never synthesize a theorem from a status label."""
    if record["kind"] != "result":
        return []
    lines = record["body"].splitlines(keepends=True)
    label = CARD_LABEL
    # Skip the header/status block, or begin at an explicit scientific label
    # when a compact card has no separating blank line.
    begins = next((i + 1 for i, line in enumerate(lines) if not line.strip()), len(lines))
    first_label = next((i for i, line in enumerate(lines[1:], 1) if label.match(line)), len(lines))
    begins = min(begins, first_label)
    result, block, start, role = [], [], begins + 1, "unlabelled_card_passage"

    def flush():
        while block and not block[-1].strip():
            block.pop()
        if block and role not in ("evidence", "references"):
            result.append({"role": role, "text": "".join(block).rstrip("\r\n"), "lines": [start, start + len(block) - 1]})
        block.clear()

    for number, line in enumerate(lines[begins:], begins + 1):
        if re.match(r"(?i)^(?:status=|notation local\.?$|symbols .*local)", line.strip()):
            flush()
            role = "unlabelled_card_passage"
            continue
        match = label.match(line)
        if match:
            flush()
            role, start = match[1].lower(), number
        elif not line.strip() and role == "unlabelled_card_passage":
            flush()
            continue
        if not block:
            start = number
        block.append(line)
    flush()
    return result


def operation_frame(record):
    contract = record["contract"]
    frame = {
        "id": record["id"], "content_version": record["content_version"],
        "operation": record["title"], "statement": record["statement"],
        "construction": record["body"] if record["kind"] != "result" else "Read the card and cited construction",
        "requires": contract.get("requires", "UNKNOWN"),
        "returns": contract.get("provides", "UNKNOWN"),
        "conditions": contract.get("assumptions", "UNKNOWN"),
        "costs": contract.get("costs", "UNKNOWN"), "units": contract.get("units", "UNKNOWN"),
        "obstruction": contract.get("obstruction", "UNKNOWN"),
        "scope": "Verbatim normalized fields. Objects/types remain source-local; this view does not infer an interface or acceptance.",
    }
    passages = card_sections(record)
    if passages:
        labelled = [p for p in passages if p["role"] in ("claim", "exact claim", "theorem")]
        frame["scientific_excerpt"] = (labelled or passages)[0]
        frame["card_roles"] = [p for p in passages if p["role"] != "unlabelled_card_passage"]
        frame["card_reference"] = {"authority": record["authority"], "sha256": digest(record["body"].encode()),
                                   "read": ["card", record["id"]]}
        frame["card_scope"] = "Verbatim historical card passages, not a new theorem, inferred premise, or acceptance. Reported status is kept separately in the canonical record; current review overlays and corrections govern. Unlabelled excerpts have no inferred role."
    return frame


def historical_summary(record):
    statement = record["statement"]
    header_lines = re.split(r"\r?\n\s*\r?\n", record["body"], maxsplit=1)[0].splitlines()
    metadata = []
    for line in header_lines:
        if CARD_LABEL.match(line):
            break
        metadata.append(line)
    header = "\n".join(metadata)
    return record["kind"] == "result" and isinstance(statement, str) and bool(statement.strip()) and (
        statement.startswith("status=") or statement.strip() in header)


def statement_view(record, frame):
    excerpt = frame.get("scientific_excerpt")
    if historical_summary(record) and excerpt:
        return {"statement": excerpt["text"], "statement_origin": {"kind": "verbatim_card_excerpt",
                    "role": excerpt["role"], "lines": excerpt["lines"], "reference": frame["card_reference"],
                    "scope": "An unlabelled excerpt has no inferred theorem role; current proof/review/conditions govern."},
                "historical_reported_status": record["statement"]}
    return {"statement": record["statement"], "statement_origin": {"kind": "canonical_statement"}}


def premise_check(frame, available=(), unavailable=()):
    """Surface literal overlaps with requirements, without treating absence as falsity.

    Negation, quantifiers and units require the full passage. In particular a
    match against 'without X' is not evidence that X is a required input.
    """
    fields = {key: flatten(frame[key]) for key in ("requires", "conditions", "costs", "units", "obstruction")}
    for passage in frame.get("card_roles", []):
        if passage["role"].startswith(("interface", "assumption", "boundar", "cost")):
            fields["verbatim_card_" + passage["role"]] = passage["text"]
    checks = []
    for role, phrases in (("available", available), ("unavailable", unavailable)):
        for phrase in phrases:
            wanted = set(tokens(phrase))
            spans = []
            for field, text in fields.items():
                for clause in re.split(r"(?<=[.;\n])\s+", text):
                    overlap = sorted(wanted & set(tokens(clause)))
                    if overlap:
                        spans.append({"field": field, "text": clause, "overlap": overlap})
            checks.append({"role": role, "input": phrase, "literal_spans": spans,
                           "state": "INSPECT POTENTIAL CONFLICT" if role == "unavailable" and spans else "NOT DISCHARGED"})
    return {"checks": checks, "compatibility": "NOT ESTABLISHED",
            "scope": "Literal premise triage only, including possible negated mentions. Available facts are not verified and no requirement is automatically discharged. Inspect full conditions, units, notices and governing source; use bridge for documented transfers."}
