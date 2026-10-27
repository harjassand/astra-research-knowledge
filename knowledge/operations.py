"""Lossless operation views and conservative premise inspection; no inferred proofs."""
import re

from knowledge.model import flatten, tokens


def operation_frame(record):
    contract = record["contract"]
    return {
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


def premise_check(frame, available=(), unavailable=()):
    """Surface literal overlaps with requirements, without treating absence as falsity.

    Negation, quantifiers and units require the full passage. In particular a
    match against 'without X' is not evidence that X is a required input.
    """
    fields = {key: flatten(frame[key]) for key in ("requires", "conditions", "costs", "units", "obstruction")}
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
