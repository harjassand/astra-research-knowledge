#!/usr/bin/env python3
"""Build a deterministic, whole-card task evidence bundle from ASTRA retrieval."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import knowledge

ROOT = Path(__file__).resolve().parents[1]
CLAIMS = ROOT / "indexes/claims.jsonl"
BLOCKERS = ROOT / "indexes/blockers.json"
BUILD = ROOT / "indexes/BUILD.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def revision() -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL, text=True,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        try:
            data = json.loads(BUILD.read_text())
            return "snapshot:" + str(data.get("updated_at_utc", "unknown"))
        except (OSError, json.JSONDecodeError):
            return "snapshot:unknown"


def load_claims() -> dict[str, dict]:
    out = {}
    with CLAIMS.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                row = json.loads(line)
                out[row["id"]] = row
    return out


def load_blockers() -> list[dict]:
    """Read W11's scoped index, tolerating its absence during index generation."""
    if not BLOCKERS.is_file():
        return []
    try:
        value = json.loads(BLOCKERS.read_text(encoding="utf-8"))
        rows = value.get("blockers", []) if isinstance(value, dict) else value
        return rows if isinstance(rows, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def blocker_fields(row: dict) -> tuple[list[str], list[str], list[str]]:
    affected = row.get("affected_cards", row.get("affected_card_ids", row.get("attach_to", [])))
    required = row.get("required_cards", row.get("required_contrasting_card_ids", row.get("cards", [])))
    terms = row.get("trigger_terms", [])
    if isinstance(affected, str):
        affected = [affected]
    if isinstance(required, str):
        required = [required]
    if isinstance(terms, str):
        terms = [terms]
    return list(affected or []), list(required or []), list(terms or [])


def choose_blockers(query: str, selected: list[str], rows: list[dict]) -> list[dict]:
    q = set(knowledge.query_terms(query)) if hasattr(knowledge, "query_terms") else set(query.lower().split())
    found = []
    for row in rows:
        affected, _, terms = blocker_fields(row)
        matched_terms = any(set(knowledge.query_terms(t) if hasattr(knowledge, "query_terms") else t.lower().split()) <= q
                            for t in terms if t)
        if set(affected) & set(selected) or matched_terms:
            found.append(row)
    return found


def card_record(identifier: str, claims: dict[str, dict]) -> tuple[dict, str] | None:
    row = claims.get(identifier)
    if row is None:
        return None
    path = ROOT / row["path"]
    if not path.is_file():
        return None
    return row, path.read_text(encoding="utf-8")


def scoped_dependencies(row: dict) -> list[str]:
    deps = list(row.get("depends_on", []))
    for dep in row.get("scoped_dependencies", []):
        ident = dep.get("id")
        relation = str(dep.get("relation", "requires"))
        # Only explicit card requirements are silently resolved as cards.
        if ident and relation.startswith("requires"):
            deps.append(ident)
    return list(dict.fromkeys(deps))


def source_pointers(row: dict, blockers: list[dict]) -> list[tuple[str, str]]:
    refs = []
    for source_id in row.get("source_ids", []):
        page = ROOT / "web/pages" / (source_id + ".html")
        if page.is_file():
            refs.append((source_id, "web/pages/" + source_id + ".html"))
    for blocker in blockers:
        for ptr in blocker.get("source_pointers", blocker.get("source_anchors", [])):
            if ptr.get("card_id") == row["id"] or ptr.get("card_path") == row["path"]:
                evidence_id = ptr.get("evidence_id")
                evidence_path = ptr.get("evidence_path")
                if evidence_id and evidence_path:
                    page = ROOT / "web/pages" / (evidence_id + ".html")
                    if page.is_file():
                        # evidence_path is retained as provenance text, while
                        # the emitted pointer is a path that exists in this export.
                        refs.append((evidence_id, "web/pages/" + evidence_id + ".html"))
    return list(dict.fromkeys(refs))


def render_card(row: dict, text: str, attached: list[dict], claims: dict[str, dict]) -> str:
    # The source card bytes are included verbatim; surrounding metadata is additive.
    status = row.get("status", "status_unavailable")
    card_path = ROOT / row["path"]
    digest = sha256(card_path)[:12] if card_path.is_file() else "unavailable"
    lines = [f'\n<CARD id="{row["id"]}" status="{status}" completeness="complete_card" sha256="{digest}">\n', knowledge.decision.banner(row['id']), text]
    if not text.endswith("\n"):
        lines.append("\n")
    pointers = source_pointers(row, attached)
    if pointers:
        ident, path = pointers[0]
        lines.append(f"OPEN: {path}; local: python3 tools/knowledge.py read {ident}; more: indexes/agent_catalog.json\n")
    deps = scoped_dependencies(row)
    unresolved = [d for d in deps if d not in claims]
    if unresolved:
        lines.append("REQUIRES (external/interface; unresolved by this bundle): " + ", ".join(unresolved) + "\n")
    lines.append("</CARD>\n")
    return "".join(lines)


def make_bundle(query: str, budget: int = 1500, max_bytes: int = 6000, limit: int = 5) -> dict:
    claims = load_claims()
    blocker_rows = load_blockers()
    hits = knowledge.search(query, limit=max(limit, 1))
    roots = []
    for hit in hits:
        row = claims.get(hit.get("source_id"))
        if row and row.get("record_type") == "curated_claim":
            cid = row["id"]
        else:
            cid = next((c["id"] for c in claims.values() if c.get("path") == hit.get("path")), None)
        if cid and cid not in roots:
            roots.append(cid)

    # Required cards are inserted adjacent to their triggering root, before any
    # optional lexical hit. This keeps a positive claim and its contrast together.
    order: list[str] = []
    attachments: dict[str, list[dict]] = {}
    omissions: list[dict] = []
    for cid in roots:
        block_rows = choose_blockers(query, [cid], blocker_rows)
        attachments[cid] = block_rows
        if cid not in order:
            order.append(cid)
        for blocker in block_rows:
            _, required, _ = blocker_fields(blocker)
            for required_id in required:
                if required_id in claims and required_id not in order:
                    order.append(required_id)
                    attachments[required_id] = [blocker]
    # Query-triggered blockers may be relevant even if lexical search missed the
    # affected card. Add affected cards and required contrasts as a minimal pair.
    for blocker in choose_blockers(query, [], blocker_rows):
        affected, required, _ = blocker_fields(blocker)
        for cid in affected + required:
            if cid in claims and cid not in order:
                order.append(cid)
                attachments.setdefault(cid, [blocker])

    # Close over explicit card dependencies, including dependencies of required
    # contrast cards. They follow direct blocker pairs and precede optional hits.
    cursor = 0
    while cursor < len(order):
        row = claims.get(order[cursor], {})
        for dep in scoped_dependencies(row):
            if dep in claims and dep not in order:
                order.append(dep)
                attachments.setdefault(dep, [])
        cursor += 1

    selected: list[str] = []
    blocks: list[str] = []
    reasons: dict[str, str] = {}
    full_revision = revision()
    full_hashes = {
        "claims": sha256(CLAIMS),
        "blockers": sha256(BLOCKERS) if BLOCKERS.is_file() else None,
        "build": sha256(BUILD) if BUILD.is_file() else None,
        "current_status": sha256(ROOT/'frontier/CURRENT_CLAIM_STATUS.jsonl'),
    }
    header = (
        "ASTRA TASK BUNDLE v1\n"
        f"q: {query}\n"
        f"rev: {full_revision}\n"
        f"inputs: claims={full_hashes['claims'][:12]} blockers={full_hashes['blockers'][:12] if full_hashes['blockers'] else 'absent'}\n"
        "Card statuses are preserved; this bundle does not audit full proofs.\n"
    )
    def trailer_for(omitted: list[dict], included: list[str]) -> str:
        short_reason = {
            "card_exceeds_remaining_budget_or_byte_cap": "size",
            "max_cards_limit": "limit",
            "card_missing": "missing",
            "budget_or_byte_cap": "size",
        }
        omitted_text = ",".join("{}:{}".format(x["id"], short_reason.get(x["reason"], x["reason"])) for x in omitted) if omitted else "none"
        included_text = ",".join(included) if included else "none"
        return (
        f"\nIN: {included_text}\nOUT: {omitted_text}\n"
        "OUT is scoped; dependency closure is not implied.\n"
        )

    def blocker_section(included: list[str]) -> str:
        used = []
        for cid in included:
            for blocker in attachments.get(cid, []):
                if blocker not in used:
                    used.append(blocker)
        if not used:
            return ""
        lines = ["\nSCOPED LIMITATIONS (full index: indexes/blockers.json):\n"]
        for blocker in used:
            lines.append(f'{blocker.get("id", "unknown")}: {blocker.get("limitation", blocker.get("scope", "scope recorded in blocker index"))}\n')
            for ptr in blocker.get("source_pointers", blocker.get("source_anchors", [])):
                if ptr.get("evidence_id"):
                    page = ROOT / "web/pages" / (ptr["evidence_id"] + ".html")
                    if page.is_file():
                        lines.append(f'proof pointer: web/pages/{ptr["evidence_id"]}.html; read ID {ptr["evidence_id"]}\n')
                        break
        return "".join(lines)

    # Reserve header + trailer; build in deterministic order and recheck exact
    # final counts after every admission. No card is ever cut to meet a cap.
    for cid in order:
        if cid in selected:
            continue
        if len(selected) >= limit:
            reasons[cid] = "max_cards_limit"
            continue
        item = card_record(cid, claims)
        if not item:
            reasons[cid] = "card_missing"
            continue
        row, text = item
        attached = attachments.get(cid, [])
        block = render_card(row, text, attached, claims)
        candidate_selected = selected + [cid]
        candidate_blocks = blocks + [block]
        omitted_now = [{"id": x, "reason": reasons[x]} for x in sorted(reasons)]
        candidate_text = header + "".join(candidate_blocks) + blocker_section(candidate_selected) + trailer_for(omitted_now + [
            {"id": x, "reason": "budget_or_byte_cap"} for x in order if x not in candidate_selected and x not in reasons
        ], candidate_selected)
        token_count = knowledge.count(candidate_text)
        byte_count = len(candidate_text.encode("utf-8"))
        if token_count <= budget and byte_count <= max_bytes:
            selected, blocks = candidate_selected, candidate_blocks
        else:
            reasons[cid] = "card_exceeds_remaining_budget_or_byte_cap"

    omitted = [{"id": cid, "reason": reasons.get(cid, "budget_or_byte_cap")}
               for cid in order if cid not in selected]
    rendered = header + "".join(blocks) + blocker_section(selected) + trailer_for(omitted, selected)
    token_count = knowledge.count(rendered)
    byte_count = len(rendered.encode("utf-8"))
    # Even empty bundles must be honest when caller caps cannot hold framing.
    if token_count > budget or byte_count > max_bytes:
        raise ValueError(
            f"caps too small for bundle framing: need {token_count} tokens/{byte_count} bytes"
        )
    return {
        "text": rendered,
        "query": query,
        "selected_ids": selected,
        "omitted": omitted,
        "tokens": token_count,
        "bytes": byte_count,
        "budget": budget,
        "max_bytes": max_bytes,
        "revision": full_revision,
        "input_hashes": full_hashes,
        "card_hashes": {cid: sha256(ROOT / claims[cid]["path"]) for cid in selected},
        "current_status": {cid: knowledge.decision.notice(cid) for cid in selected},
        "omitted_current_status": {cid: knowledge.decision.notice(cid) for cid in order if cid not in selected},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query")
    parser.add_argument("--budget", type=int, default=1500)
    parser.add_argument("--max-bytes", type=int, default=6000)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--json", action="store_true", help="emit text plus full hash/count provenance as JSON")
    args = parser.parse_args()
    if args.budget <= 0 or args.max_bytes <= 0 or args.limit <= 0:
        parser.error("--budget, --max-bytes, and --limit must be positive")
    result = make_bundle(args.query, args.budget, args.max_bytes, args.limit)
    if args.json:
        sys.stdout.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    else:
        sys.stdout.write(result["text"])
    sys.stderr.write(f"COUNT tokens={result['tokens']} bytes={result['bytes']}\n")


if __name__ == "__main__":
    main()
