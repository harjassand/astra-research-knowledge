#!/usr/bin/env python3
"""One public intake path: normalize existing authorities, validate support, project."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import sys
import tempfile

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from knowledge.model import (ROOT, Inputs, TYPED_SOURCE_TEXT, compact_ref, digest, encoded, evidence_refs,
                             field_index, flatten, local, route_id, scientific_text, unique)
from knowledge.evidence import source_indexes
from knowledge.interfaces import compile_navigation, packet_navigation

MANIFEST = "knowledge/current/manifest.json"
DISCOVERY = {
    "indexes/claims.d": "*.jsonl", "indexes/agent_catalog.d": "*.json",
    "indexes/query_aliases.d": "*.json", "frontier/CURRENT_CLAIM_STATUS.d": "*.jsonl",
    "agent/SEMANTIC_NOTICES.d": "*.jsonl", "literature/lemmas": "*.json",
    "knowledge/units": "*/*.json", "knowledge/reviews": "*.json",
    "knowledge/transfers": "*.json", "technology/records": "*/*.json",
}


def inventory(root):
    return {folder: sorted(path.relative_to(root).as_posix() for path in (root / folder).glob(pattern)
                           if path.is_file()) for folder, pattern in DISCOVERY.items()} | {"selected_public_source_indexes": source_indexes(root)}


def authority_layers(claim_base, claim_current, status_base, status_current,
                     catalog_base, catalog_current):
    """Keep checkpoint-pinned baselines while replacing current rows explicitly.

    A baseline ID can have one full current row in each existing shard family.
    All three families must agree on replacements and retain the card identity.
    Duplicate current rows are errors, rather than filesystem-order precedence.
    """
    base = [unique(claim_base, "id"), unique(status_base, "card_id"), unique(catalog_base, "id")]
    current = [unique(claim_current, "id"), unique(status_current, "card_id"), unique(catalog_current, "id")]
    replaced = [old.keys() & new.keys() for old, new in zip(base, current)]
    if not replaced[0] == replaced[1] == replaced[2]:
        raise ValueError("Current baseline replacements must agree across claim/status/catalog shards")
    for identifier in replaced[0]:
        paths = [(base[0][identifier]["path"], current[0][identifier]["path"]),
                 (base[1][identifier]["card_path"], current[1][identifier]["card_path"]),
                 (base[2][identifier]["pointers"]["card_local"],
                  current[2][identifier]["pointers"]["card_local"])]
        if any(old != new for old, new in paths):
            raise ValueError("Current baseline replacement changed card identity: " + identifier)
    return tuple(old | new for old, new in zip(base, current))


def sections(text):
    result = defaultdict(list)
    heading = "body"
    for line in text.splitlines():
        match = re.match(r"^([A-Z][A-Z /_-]{3,})(?:\s*\||:)(.*)$", line)
        if match:
            heading = match[1].strip()
            result[heading].append(match[2].strip())
        elif re.fullmatch(r"[A-Z][A-Z /_-]{4,}", line.strip()):
            heading = line.strip()
        else:
            result[heading].append(line)
    return {key: "\n".join(value).strip() for key, value in result.items()}


def packet_review(review, packet_evidence, preserve_annotations=False, evidence_field="evidence"):
    """Reference review citations through the packet evidence array when complete."""
    result = dict(review)
    original_field = review.get(evidence_field, [])
    originals = list(evidence_refs(original_field))
    # Do not replace a mixed annotation/container with only its nested refs.
    if not isinstance(original_field, list) or originals != original_field:
        return result
    refs = [compact_ref(reference) for reference in originals]
    positions = {encoded(reference): index for index, reference in enumerate(packet_evidence)}
    keys = [encoded(reference) for reference in refs]
    if refs and all(key in positions for key in keys):
        result.pop(evidence_field, None)
        result["evidence_ref_field"] = evidence_field
        result["evidence_ref_indices"] = [positions[key] for key in keys]
        if preserve_annotations:
            annotations = [{key: value for key, value in original.items()
                            if key not in compact_ref(original)} for original in originals]
            if any(annotations):
                result["evidence_ref_annotations"] = annotations
    return result



def packet_transfer_references(packet):
    """Share only identical complete citations already elsewhere in this packet."""
    pointers = {}
    def visit(value, pointer=""):
        if isinstance(value, dict):
            if {"path", "sha256", "lines"} <= value.keys():
                pointers.setdefault(encoded(value), pointer)
                return
            for key, child in value.items():
                if not pointer and key == "transfers":
                    continue
                visit(child, pointer + "/" + key.replace("~", "~0").replace("/", "~1"))
        elif isinstance(value, list):
            for index, child in enumerate(value):
                visit(child, pointer + "/" + str(index))
    visit(packet)
    return [dict(transfer, evidence=[
        {"evidence_ref_pointer": pointers[encoded(reference)]}
        if encoded(reference) in pointers else reference
        for reference in transfer.get("evidence", [])])
        for transfer in packet["transfers"]]


def packet_shared_citations(packet):
    """Share identical complete citations through existing packet-root pointers.

    Origins are limited to fields retained by both full and compact MCP views.
    Primary evidence remains inline and in its original order. Different ranges,
    quotes or qualifications never share a pointer.
    """
    origins = {}
    def index(value, pointer):
        if isinstance(value, dict):
            if {"path", "sha256", "lines"} <= value.keys():
                origins.setdefault(encoded(value), pointer)
                return
            for key, child in value.items():
                index(child, pointer + "/" + key.replace("~", "~0").replace("/", "~1"))
        elif isinstance(value, list):
            for number, child in enumerate(value):
                index(child, pointer + "/" + str(number))
    for field in ("evidence", "notices", "review_overlays", "transfers"):
        index(packet.get(field, []), "/" + field)
    def replace(value, pointer):
        if isinstance(value, dict):
            if {"path", "sha256", "lines"} <= value.keys():
                origin = origins.get(encoded(value))
                return {"evidence_ref_pointer": origin} if origin and origin != pointer else dict(value)
            return {key: replace(child, pointer + "/" + key.replace("~", "~0").replace("/", "~1"))
                    for key, child in value.items()}
        if isinstance(value, list):
            return [replace(child, pointer + "/" + str(number)) for number, child in enumerate(value)]
        return value
    result = dict(packet)
    # Never put a pointer into a history-only payload that lacks its origin.
    # Keep notice/review capsule structures byte-for-byte as before. They can
    # supply complete origins without themselves becoming references.
    for field in ("transfers", "relationships", "review", "current_acceptance"):
        if field in result:
            result[field] = replace(result[field], "/" + field)
    return result


def packet_default_read_paths(value):
    """Omit only a citation's redundant read_path == path, an existing default."""
    if isinstance(value, list):
        return [packet_default_read_paths(child) for child in value]
    if not isinstance(value, dict):
        return value
    return {key: packet_default_read_paths(child) for key, child in value.items()
            if not (key == "read_path" and {"path", "sha256", "lines"} <= value.keys()
                    and child == value["path"])}


def packet_excerpt(reference, passage, selection):
    """Keep navigation from re-publishing a legacy host-local locator.

    Original bytes, source identity and the complete source route are untouched.
    Never silently rewrite scientific evidence while rendering a packet.
    """
    excerpt = {"source": reference, "text_selection": selection,
               "excerpt_truncated": len(passage) > 2400}
    if re.search(r"/(?:Users|home)/[^/\s'\"<>]+/|file:[/]{2}", passage[:2400]):
        excerpt["text_omitted"] = "Read this exact source range; optional navigation text omitted because the historical source contains host-local locators. Original evidence remains unchanged."
    else:
        excerpt["text"] = passage[:2400]
    return excerpt


def build(root=ROOT):
    root = Path(root)
    inputs = Inputs(root)
    discovered = inventory(root)
    from knowledge.evidence import public_derivatives
    historical_derivatives = public_derivatives(inputs, discovered["selected_public_source_indexes"])
    for name in ("knowledge/model.py", "knowledge/build.py", "knowledge/retrieve.py",
                 "knowledge/search.js", "knowledge/index.html", "knowledge/README.md",
                 "knowledge/INTAKE.md", "knowledge/operations.py", "knowledge/agent_search.py", "knowledge/evidence.py", "knowledge/interfaces.py",
                 "knowledge/mcp_adapter.py", "knowledge/published.py", "plugins/astra-research/server.py",
                 "knowledge/requirements-agent.txt", "knowledge/runtime/manifest.json",
                 "00_START_HERE.txt", "AGENTS.md", "agent/ACCESS.txt"):
        inputs.read(name)
    for name, expected in inputs.json("knowledge/runtime/manifest.json")["files"].items():
        if digest(inputs.read("knowledge/runtime/" + name)) != expected:
            raise ValueError("INGESTION FAILED: pinned retrieval model bytes changed: " + name)
    concepts = inputs.json("knowledge/concepts.json")
    claims, statuses, catalog = authority_layers(
        inputs.rows("indexes/claims.jsonl"),
        [row for name in discovered["indexes/claims.d"] for row in inputs.rows(name)],
        inputs.rows("frontier/CURRENT_CLAIM_STATUS.jsonl"),
        [row for name in discovered["frontier/CURRENT_CLAIM_STATUS.d"] for row in inputs.rows(name)],
        inputs.json("indexes/agent_catalog.json")["claims"],
        [row for name in discovered["indexes/agent_catalog.d"] for row in inputs.json(name)["claims"]])
    if claims.keys() != statuses.keys() or claims.keys() != catalog.keys():
        raise ValueError("INGESTION FAILED: claim/status/catalog ID sets disagree")
    short_ids = unique([{"short": route_id(identifier), "id": identifier} for identifier in claims], "short")

    def canonical(identifier):
        if identifier in claims:
            return identifier
        stem = Path(identifier).stem
        resolved = short_ids.get(route_id(stem), {}).get("id")
        if resolved is None and re.match(r"^[NL]\d+(?:-|$)", stem):
            raise ValueError("Dangling numeric result identity: " + identifier)
        return resolved

    aliases = inputs.json("indexes/query_aliases.json")
    for name in discovered["indexes/query_aliases.d"]:
        for identifier, value in inputs.json(name).items():
            if identifier in aliases and aliases[identifier] != value:
                raise ValueError("Conflicting alias shard for " + identifier)
            aliases[identifier] = value
    legacy_bridges = []
    bridge_path = "mechanisms/bridge_candidates.json"
    if (root / bridge_path).is_file():
        bridges = inputs.json(bridge_path)
        legacy_bridges = bridges["bridges"] + bridges["rejected_transfers"]
    graph_by_card = defaultdict(list)
    graph_path = "indexes/agent_graph.json"
    if (root / graph_path).is_file():
        for edge in inputs.json(graph_path)["edges"]:
            for identifier in (canonical(edge["from"]), canonical(edge["to"])):
                if identifier:
                    graph_by_card[identifier].append(edge)
    notices = inputs.rows("agent/SEMANTIC_NOTICES.jsonl", "agent/SEMANTIC_NOTICES.d")
    unique(notices, "notice_id")
    by_card = defaultdict(list)
    for notice in notices:
        for identifier in notice["card_ids"]:
            if canonical(identifier) is None:
                raise ValueError("Unknown semantic-notice card " + identifier)
            by_card[canonical(identifier)].append(notice)
    for status in statuses.values():
        for relation in ("material_updates", "supersedes", "invalidates"):
            for update in status.get(relation, []):
                target = canonical(update.get("target", "") if isinstance(update, dict) else update)
                if target:
                    by_card[target].append({"relation": relation, "source_card": status["card_id"],
                                            "assertion": update, "scope": update.get("scope", "UNKNOWN")
                                            if isinstance(update, dict) else "UNKNOWN; read governing source"})
    records = []
    support = {}
    sources = []

    def references(values, historical=False, source_derivatives=None):
        result = {}
        for reference in evidence_refs(values):
            ref = compact_ref(reference)
            try:
                text, _ = inputs.source(ref)
            except UnicodeError:
                if ref.get("lines") is not None:
                    raise ValueError("Binary source cannot support a text passage: " + ref["path"])
                data = inputs.read(ref["path"])
                if digest(data) != ref["sha256"]:
                    raise ValueError("Binary artifact hash mismatch: " + ref["path"])
                ref["locator_scope"] = "binary artifact only; no statement or text passage inferred"
                result[encoded(ref)] = ref
                continue
            except ValueError as error:
                replacement = historical_derivatives.get((ref["path"], ref["sha256"]))
                if not historical or replacement is None or "required source bytes missing/mismatched" not in str(error):
                    raise
                original = ref
                ref = dict(ref, **replacement)
                # Exact old range/quotation must still exist in the declared
                # public derivative. This is not verification of old full bytes.
                text, _ = inputs.source(ref)
                if source_derivatives is not None:
                    source_derivatives.append({
                        "original_path": original["path"], "original_sha256": original["sha256"],
                        "original_lines": original.get("lines"), "public_derivative": ref,
                        "scope": "Historical original identity preserved; quoted scientific range available in explicit public derivative. Original full bytes are privately preserved, not acquired from this current tree."})
            if ref.get("lines") is None:
                ref["lines"] = [1, len(text.splitlines())]
                ref["locator_scope"] = "whole file; original record supplied no statement-specific lines"
            result[encoded(ref)] = ref
        return list(result.values())

    references(notices)
    references(legacy_bridges)

    for identifier, claim in sorted(claims.items()):
        status = statuses[identifier]
        body = inputs.read(claim["path"])
        if digest(body) != status["card_sha256"] or digest(body) != catalog[identifier]["card_sha256"]:
            raise ValueError("INGESTION FAILED: card/status/catalog bytes disagree: " + identifier)
        sidecar = inputs.json("frontier/cards/" + identifier + ".json")
        if sidecar != status:
            raise ValueError("Stale status sidecar: " + identifier)
        refs = references(status)
        if not refs:
            raise ValueError("INGESTION FAILED: card has no required evidence: " + identifier)
        support[identifier] = {(ref["path"], ref["sha256"]) for ref in refs}
        text = body.decode("utf-8")
        parts = sections(text)
        alerts = list(by_card[identifier])
        dependencies = []
        for dependency in status.get("depends_on", []):
            target = canonical(dependency.get("target", "") if isinstance(dependency, dict) else dependency)
            if target:
                dependencies.append(target)
                if by_card[target]:
                    alerts.append({"dependency": target, "scope": dependency.get("scope", "UNKNOWN")
                                   if isinstance(dependency, dict) else "explicit dependency",
                                   "notices": by_card[target]})
        record = {
            "id": identifier, "kind": "result", "parents": [], "title": claim["title"],
            "topics": claim.get("topics", []), "body": text, "aliases": aliases.get(identifier, ""),
            "statement": parts.get("EXACT CLAIM", parts.get("SOURCE-REPORTED THEOREM CLAIMS", status.get("reported_status", "UNKNOWN"))),
            "contract": {
                "requires": parts.get("SOURCE-REPORTED INTERFACE", parts.get("INTERFACE", catalog[identifier].get("quoted_fields", {}).get("interface", "UNKNOWN; read cited source"))),
                "provides": status.get("scientific_scope_status", "UNKNOWN; read cited source"),
                "assumptions": parts.get("BOUNDARIES", parts.get("BOUNDARY", "UNKNOWN; read cited source")),
                "costs": parts.get("COST AND INFORMATION BOUNDARY", parts.get("COST", "UNKNOWN; read cited source")),
                "units": "source-local; no automatic conversion", "obstruction": parts.get("NEXT OBLIGATION", "UNKNOWN"),
            },
            "evidence": refs, "dependencies": dependencies,
            "relationships": {key: status.get(key, []) for key in ("supersedes", "invalidates", "material_updates", "scoped_dependencies", "contrasting_blockers")}
                | {"declared_dependencies": status.get("depends_on", []), "incident_graph_edges": graph_by_card[identifier],
                   "legacy_bridge_candidates": [bridge for bridge in legacy_bridges if identifier in bridge["cards"]]},
            "notices": alerts, "review": {"acceptance": "not_assessed_by_normalizer",
                "reported_status": status["claim_status"], "validation": status.get("validation", {}),
                "gaps": status.get("requires_external_validation", [])},
            "authority": "frontier/cards/" + identifier + ".json",
        }
        records.append(record)
        proof = status["proof_availability"]
        retrieval_refs = proof.get("located_proof_sources", []) + proof.get("available_evidence_sources", [])
        for reference in references(retrieval_refs):
            text, passage = inputs.source(reference)
            searchable, selector = scientific_text(passage)
            if selector != "unchanged_utf8":
                source_id = "S-" + digest(encoded({"parent": identifier, "source": reference}))[:24]
                sources.append({"id": source_id, "kind": "source_window", "record_id": identifier,
                                "parents": [identifier], "title": reference.get("range_scope", claim["title"]),
                                "body": searchable, "evidence": [reference], "text_selection": selector,
                                "scope": "Derived searchable values, not a theorem; read the governing original source"})
                continue
            lines = text.splitlines(keepends=True)
            start, end = reference["lines"]
            for window_start in range(start, end + 1, 64):
                window_end = min(end, window_start + 79)
                window = "".join(lines[window_start - 1:window_end])
                source_ref = dict(reference, lines=[window_start, window_end])
                if source_ref.get("quote") and source_ref["quote"] not in window:
                    # The governing range was validated above. A search window
                    # must not claim that its parent's anchor occurs inside it.
                    source_ref.pop("quote")
                source_id = "S-" + digest(encoded({"parent": identifier, "source": source_ref}))[:24]
                sources.append({"id": source_id, "kind": "source_window", "record_id": identifier,
                                "parents": [identifier], "title": reference.get("range_scope", claim["title"]),
                                "body": window, "evidence": [source_ref],
                                "scope": "Search window, not an extracted theorem or complete proof"})
                if window_end == end:
                    break

    result_records = {record["id"]: record for record in records}

    def parent_notices(parents):
        return [dict(notice, parent_context_card=parent, context_only_notice=True)
                for parent in parents for notice in result_records[parent]["notices"]]

    atlas = inputs.rows("literature/LEMMA_ATLAS.jsonl")
    unique(atlas, "id")
    for lemma in atlas:
        path = "literature/lemmas/" + lemma["id"] + ".json"
        if inputs.json(path) != lemma:
            raise ValueError("Stale lemma sidecar: " + path)
        refs = []
        for source in lemma["source"]:
            for line_range in source["locators"]["lines"]:
                ref = {"path": source["path"], "sha256": source.get("text_sha256", source["sha256"]),
                       "lines": line_range, "read_path": source.get("web_page", source["path"]),
                       "hash_kind": "indexed_utf8_text", "doc_id": source.get("doc_id")}
                inputs.source(ref)
                refs.append(ref)
        parents = [canonical(identifier) for identifier in lemma["claim_ids"]]
        if None in parents or not refs:
            raise ValueError("Unresolved lemma parent/support: " + lemma["id"])
        records.append({"id": lemma["id"], "kind": lemma["kind"], "parents": parents,
            "title": lemma["title"], "topics": lemma["topics"], "statement": lemma["statement"],
            "contract": {"requires": lemma["interface"]["inputs"], "provides": lemma["interface"]["outputs"],
                         "assumptions": lemma["statement"]["assumptions"], "costs": lemma["interface"]["costs"],
                         "precision": lemma["interface"]["precision"], "units": "source-local",
                         "obstruction": lemma["obstructions"]},
            "body": flatten(lemma["proof_mechanism"]), "aliases": lemma["search_terms"],
            "evidence": refs, "dependencies": lemma["depends_on"],
            "relationships": {"potential_uses": lemma["potential_uses"], "generalisations": lemma["generalisations"]},
            "notices": parent_notices(parents), "review": lemma["review"],
            "authority": path})

    unit_versions = defaultdict(list)
    for name in discovered["knowledge/units"]:
        unit = inputs.json(name)
        unit_versions[unit["id"]].append((name, unit))
    for identifier, versions in sorted(unit_versions.items()):
        versions.sort(key=lambda item: item[1]["version"])
        version_derivatives = {}
        for index, (name, unit) in enumerate(versions):
            if unit["version"] != index + 1 or unit.get("previous") != (None if index == 0 else inputs.hashes[versions[index - 1][0]]):
                raise ValueError("Broken immutable unit version chain: " + identifier)
            notes = []
            refs = references(unit["evidence"], historical=index < len(versions) - 1,
                              source_derivatives=notes)
            if notes:
                version_derivatives[name] = notes
            parents = [canonical(parent) for parent in unit["parents"]]
            if None in parents or not parents or not refs:
                raise ValueError("Unresolved unit parent/support: " + identifier)
            if index == len(versions) - 1 and any((ref["path"], ref["sha256"]) not in set().union(*(support[parent] for parent in parents)) for ref in refs):
                raise ValueError("Wrong-card source mapping: " + identifier)
            if any(ref["path"].startswith("cards/") for ref in refs):
                raise ValueError("A reusable unit needs a governing source, not a card summary: " + identifier)
            if not all(ref.get("quote") for ref in refs):
                raise ValueError("Reusable unit requires a checked supporting passage quote: " + identifier)
            for field in ("requires", "provides", "assumptions", "costs", "units", "obstruction"):
                if not unit["contract"].get(field):
                    raise ValueError("Missing contract field " + field + ": " + identifier)
        name, unit = versions[-1]
        record = dict(unit, parents=parents, authority=name, evidence=refs,
                      notices=parent_notices(parents),
                      history=[{"path": path, "sha256": inputs.hashes[path], "version": value["version"]}
                               | ({"source_derivatives": version_derivatives[path]} if path in version_derivatives else {})
                               for path, value in versions])
        records.append(record)

    technology_versions = defaultdict(list)
    for name in discovered["technology/records"]:
        technology = inputs.json(name)
        if not technology.get("fixture"):
            technology_versions[technology["id"]].append((name, technology))
    if technology_versions:
        from technology.validate import validate as validate_technology
        for name in ("technology/validate.py", "technology/contracts.py", "technology/schema.json",
                     "technology/routes.tsv", "frontier/OPEN_PROOF_GATES.jsonl"):
            inputs.read(name)
    for identifier, versions in sorted(technology_versions.items()):
        versions.sort(key=lambda item: item[1]["version"])
        name, technology = versions[-1]
        validate_technology(technology, root=root)
        refs = references(technology["refs"])
        if not refs:
            raise ValueError("Technology missing support: " + identifier)
        parents = sorted({canonical(card) for bridge in technology.get("bridges", [])
                          for card in bridge["source_card_ids"]} - {None})
        capability = technology["capability"]
        native_contract = technology.get("contract", {})
        records.append({"id": identifier, "kind": "technology", "parents": parents,
            "title": capability["problem"], "topics": [technology["domain"]],
            "statement": capability, "contract": {"requires": native_contract.get("inputs", "UNKNOWN; read field-specific details and supplied-input boundary"),
                "provides": capability["proposed_mechanism"], "assumptions": capability["target"]["conditions"],
                "costs": native_contract.get("resources", "UNKNOWN; no physical cost conversion inferred"),
                "units": capability["target"]["unit"], "obstruction": capability["limitation"], "field_details": native_contract},
            "body": flatten({key: technology.get(key, []) for key in ("assessment", "failures", "handoffs", "bridges", "next_obligation")}),
            "evidence": refs, "notices": parent_notices(parents),
            "review": {"stage": technology["stage"], "disposition": technology["disposition"],
                       "acceptance": "development gate, not automatic scientific acceptance"}, "authority": name,
            "version": technology["version"], "history": [{"path": path, "sha256": inputs.hashes[path]} for path, _ in versions]})

    current = unique(records, "id")
    for record in records:
        record["schema"] = "astra.knowledge.v1"
        record["content_version"] = digest(encoded({key: record.get(key) for key in (
            "id", "kind", "title", "statement", "contract", "body", "evidence", "dependencies", "relationships")}))
        record["review_overlays"] = []
        record["historical_reviews"] = []
    for name in discovered["knowledge/reviews"]:
        review = inputs.json(name)
        historical_only = bool(review.get("subjects")) and all(
            subject.get("id") in current and subject.get("content_version") != current[subject["id"]]["content_version"]
            for subject in review["subjects"])
        review_derivatives = []
        review_evidence = references(review["evidence"], historical=historical_only,
                                     source_derivatives=review_derivatives)
        if review_derivatives:
            # Preserve the authoring review bytes and subjects. Its historical
            # projection states which public copy now supplies the quotation.
            review = dict(review, evidence=review_evidence, source_derivatives=review_derivatives)
        if not review.get("subjects") or not review.get("scope") or not review_evidence:
            raise ValueError("Acceptance requires subjects, actual scope and substantive audit evidence")
        if review["decision"] not in ("accepted_internally_verified", "rejected", "open"):
            raise ValueError("Unknown review decision")
        for subject in review["subjects"]:
            if not re.fullmatch(r"[0-9a-f]{64}", subject["content_version"]):
                raise ValueError("Review requires an exact content version")
            if subject["id"] not in current:
                raise ValueError("Unknown review subject: " + subject["id"])
            record = current[subject["id"]]
            for ref in review_evidence:
                if not ref.get("quote"):
                    raise ValueError("Acceptance requires a substantive audit passage")
            if subject["content_version"] != record["content_version"]:
                record["historical_reviews"].append(dict(review, authority=name,
                    applicability="HISTORICAL VERSION ONLY; no current acceptance conferred"))
                continue
            record["review_overlays"].append(dict(review, authority=name))

    transfers = []
    for name in discovered["knowledge/transfers"]:
        transfer = inputs.json(name)
        for endpoint in ("from", "to"):
            if transfer[endpoint] not in current:
                raise ValueError("Unknown transfer endpoint")
            if transfer[endpoint + "_version"] != current[transfer[endpoint]]["content_version"]:
                raise ValueError("Stale transfer endpoint version: " + name)
        refs = references(transfer["evidence"])
        if not refs or not all(ref.get("quote") for ref in refs):
            raise ValueError("Transfer requires a scoped supporting passage")
        from knowledge.model import TRANSFER_STATES
        if transfer["state"] not in TRANSFER_STATES:
            raise ValueError("Unknown transfer state")
        if not transfer.get("scope") or not transfer.get("remaining_obligations"):
            raise ValueError("Transfer must retain scope/obligations")
        transfers.append(dict(transfer, authority=name))

    # Reviewed output-to-input bindings share one named consumer slot. Store
    # each binding once and source/parent routes separately, with linear size.
    # This derived navigation does not change scientific content versions or
    # create provider-to-provider transfers.
    navigation = compile_navigation(records, transfers)
    for record in records:
        if record["id"] in navigation:
            record["interface_navigation"] = navigation[record["id"]]

    # Current authority is a version-bound projection, not a new source claim,
    # review or scientific content identity. Preserve the original contract.
    from knowledge.operations import (compile_current_consumers, consumer_contract,
                                      acceptance_view, consumer_notice_view, CURRENT_CONSUMER_LAYOUT)
    compile_current_consumers(records)
    # A broken declared current-scope outlink is an ingestion failure, rather
    # than stale or silently missing guidance in later agent search menus.
    from knowledge.operations import current_scope_navigation
    current_records = {record["id"]: record for record in records}
    for record in records:
        current_scope_navigation(record, current_records)

    documents = []
    for record in sorted(records, key=lambda item: item["id"]):
        documents.append({key: record[key] for key in ("id", "kind", "parents", "title", "statement", "contract", "body", "notices")}
                         | {"record_id": record["id"], "aliases": record.get("aliases", "")})
        if record.get("current_consumer"):
            documents[-1].update(statement=record["current_consumer"]["statement"],
                                 contract=consumer_contract(record))
    source_documents = {}
    for source in sources:
        if source["id"] in source_documents and source_documents[source["id"]] != source:
            raise ValueError("Conflicting source-window identity: " + source["id"])
        source_documents[source["id"]] = source
    documents.extend(sorted(source_documents.values(), key=lambda item: item["id"]))
    postings = field_index(documents)
    content_lexical = field_index([{"body": document["title"] + " " + document["body"]
        if document["kind"] == "source_window" else flatten({key: document.get(key, "")
        for key in ("title", "statement", "contract", "body", "aliases", "notices")})} for document in documents])
    result_documents = [document for document in documents if document["kind"] == "result"]
    lexical = field_index([{"body": document["body"]} for document in result_documents])
    document_indexes = {document["id"]: index for index, document in enumerate(documents)}
    for values in lexical.values():
        for entry in values:
            entry[0] = document_indexes[result_documents[entry[0]]["id"]]
    outputs = {
        "knowledge/current/records.jsonl": b"".join(encoded(record) for record in sorted(records, key=lambda item: item["id"])),
        "knowledge/current/documents.jsonl": b"".join(encoded({key: document[key] for key in (
            "id", "kind", "record_id", "parents", "title", "evidence", "scope", "text_selection") if key in document}) for document in documents),
        "knowledge/current/transfers.json": encoded(transfers),
    }
    from knowledge.operations import operation_frame, historical_summary
    outputs["knowledge/current/operations.jsonl"] = b"".join(
        encoded(operation_frame(record)) for record in sorted(records, key=lambda item: item["id"]))
    shards = defaultdict(dict)
    for term, entries in postings.items():
        shards[digest(term.encode())[:2]][term] = entries
    for shard, values in sorted(shards.items()):
        outputs["knowledge/current/postings/" + shard + ".json"] = encoded(values)
    content_shards = defaultdict(dict)
    for term, entries in content_lexical.items():
        content_shards[digest(term.encode())[:2]][term] = entries
    for shard, values in sorted(content_shards.items()):
        outputs["knowledge/current/content/" + shard + ".json"] = encoded(values)
    lexical_shards = defaultdict(dict)
    for term, entries in lexical.items():
        lexical_shards[digest(term.encode())[:2]][term] = entries
    for shard, values in sorted(lexical_shards.items()):
        outputs["knowledge/current/lexical/" + shard + ".json"] = encoded(values)
    catalog_records = [{"record_id": record["id"], "title": record["title"], "kind": record["kind"], "parents": record["parents"]}
                       | ({"acceptance": acceptance_view(record, preview=True)} if record.get("current_acceptance") else {})
                       for record in sorted(records, key=lambda item: item["id"])]
    record_indexes = {record["record_id"]: index for index, record in enumerate(catalog_records)}
    catalog = [[record_indexes[document["record_id"]], int(document["kind"] == "source_window")] for document in documents]
    outputs["knowledge/current/catalog.json"] = encoded({"documents": catalog, "records": catalog_records, "concepts": concepts,
                                                        "shards": sorted(shards), "lexical_shards": sorted(lexical_shards)})
    for record in records:
        packet = dict(record)
        packet.pop("body", None)
        packet["notices"] = consumer_notice_view(record["notices"])
        if record.get("current_consumer"):
            packet["contract"] = consumer_contract(record)
            packet["statement"] = record["current_consumer"]["statement"]
            packet["current_consumer"] = {key: value for key, value in record["current_consumer"].items()
                                           if key not in ("statement", "contract")}
            packet["source_reported_contract_route"] = ["card", record["id"]]
        frame = operation_frame(record)
        if historical_summary(record) and frame.get("scientific_excerpt"):
            packet["scientific_card_excerpt"] = dict(frame["scientific_excerpt"],
                source={"path": claims[record["id"]]["path"], "sha256": digest(record["body"].encode()),
                        "lines": frame["scientific_excerpt"]["lines"]},
                scope="Verbatim historical card excerpt, not a governing proof or new acceptance. Current reviews, conditions and corrections still govern; canonical historical statement remains unchanged.")
        packet["review_overlays"] = [packet_review(review, packet["evidence"])
                                     for review in record.get("review_overlays", [])]
        packet["historical_reviews"] = [packet_review(review, packet["evidence"])
                                        for review in record.get("historical_reviews", [])]
        packet["related_units"] = [{"id": child["id"], "title": child["title"], "kind": child["kind"],
                                     "packet": "knowledge/current/packets/" + route_id(child["id"]) + ".json"}
                                    for child in records if record["id"] in child.get("parents", [])]
        packet["source_excerpt_scope"] = "Bounded navigation excerpts; read the complete cited argument and imports before reuse"
        packet["source_excerpts"] = []
        for ref in record["evidence"][:3]:
            if ref.get("lines") is None:
                continue
            _, passage = inputs.source(ref)
            passage, selection = scientific_text(passage)
            packet["source_excerpts"].append(packet_excerpt(ref, passage, selection))
        packet["transfers"] = [transfer for transfer in transfers if record["id"] in (transfer["from"], transfer["to"])]
        if "interface_navigation" in packet:
            packet["interface_navigation"] = packet_navigation(packet["interface_navigation"], packet["transfers"])
        def default_output_size():
            return len(encoded({"packets": [packet], "input_version": "0" * 64, "checkout_revision": "0" * 40}))
        new_excerpt = packet.pop("scientific_card_excerpt", None)
        prior_fits_default = default_output_size() <= 32768
        if new_excerpt:
            packet["scientific_card_excerpt"] = new_excerpt
        if new_excerpt and prior_fits_default and default_output_size() > 32768:
            # Optional new navigation must not break a previously usable
            # complete packet. Never remove review, corrections or conditions.
            packet["scientific_card_excerpt"].pop("text")
            packet["scientific_card_excerpt"]["text_omitted"] = "Read the exact card range; excerpt text omitted here to preserve the default complete-packet budget."
            if default_output_size() > 32768:
                packet.pop("scientific_card_excerpt")
                packet["scientific_card_reader"] = ["card", record["id"]]
                if default_output_size() > 32768:
                    packet.pop("scientific_card_reader")
        # Newly acquired proofs and completed reviews can push navigation
        # excerpts beyond the default packet budget. Keep every condition,
        # correction, review and source locator; omit only optional excerpt
        # text, with an explicit route to the complete supporting passage.
        for excerpt in reversed(packet["source_excerpts"]):
            if default_output_size() <= 32768:
                break
            if excerpt.pop("text", None) is not None:
                excerpt["text_omitted"] = "Read this exact source range; navigation text omitted to preserve the default complete-packet budget."
        if default_output_size() > 32768:
            # Every locator is already retained in evidence. Empty optional
            # excerpt wrappers need not duplicate those complete references.
            packet["source_excerpts"] = []
            packet["source_excerpt_scope"] = "Optional excerpts omitted for budget; read complete evidence."
        if default_output_size() > 32768 and packet["review"].get("gaps"):
            # Preserve each actual gap and all historical source annotations;
            # only exact duplicate citations use the existing index convention.
            # Copy the review so canonical records remain unchanged.
            packet["review"] = dict(packet["review"], gaps=[
                packet_review(gap, packet["evidence"], preserve_annotations=True)
                if isinstance(gap, dict) else gap for gap in packet["review"]["gaps"]])
        if default_output_size() > 32768:
            validation = packet["review"].get("validation", {})
            if isinstance(validation, dict) and validation.get("reported_status_evidence"):
                packet["review"] = dict(packet["review"], validation=packet_review(
                    validation, packet["evidence"], preserve_annotations=True,
                    evidence_field="reported_status_evidence"))
        if default_output_size() > 32768:
            shared = packet_shared_citations(packet)
            if shared != packet:
                packet = shared
                packet["evidence_reference_scope"] = (
                    "evidence_ref_pointer resolves within this complete packet to an identical full citation. "
                    "Every source qualification, mapping, condition and correction remains; reuse confers no acceptance.")
        if default_output_size() > 32768:
            # These projected fields do not replace the native capsule's
            # scientific citation. A missing read_path already means path;
            # different extraction/HTML branches remain explicit.
            if not packet["source_excerpts"]:
                packet.pop("source_excerpt_scope", None)
            for field in ("evidence", "notices", "relationships", "review", "current_acceptance"):
                if field in packet:
                    packet[field] = packet_default_read_paths(packet[field])
        outputs["knowledge/current/packets/" + route_id(record["id"]) + ".json"] = encoded(packet)
    coverage = {
        "records_by_kind": dict(Counter(record["kind"] for record in records)),
        "source_windows": len(source_documents),
        "recoverable_exact_source_versions": len({(path, version) for path, version, _ in inputs.sources}),
        "distinct_source_text_hashes": len({version for _, version, _ in inputs.sources}),
        "topics": dict(Counter(topic for record in records for topic in record.get("topics", []))),
        "scope": "Scientific lane: all registered current cards, atlas entries, selected reusable units and latest technology, including located proof AND available evidence ranges. Separate evidence lane: current record evidence ranges and explicit selected-public-source-index entries, with exclusions and no inferred acceptance. Unregistered archives/withheld material remain unassessed.",
        "eligible_mechanism_denominator": "UNKNOWN", "scientific_acceptance": "Actual version-bound substantive reviews and explicit standing human acceptance retain their stated scope; extraction and hashing confer neither.",
    }
    from knowledge.evidence import projection
    evidence_outputs, evidence_coverage = projection(root, inputs, records, discovered["selected_public_source_indexes"], transfers)
    outputs.update(evidence_outputs)
    from knowledge.contextual_search import projection as contextual_projection, VECTORS
    outputs.update(contextual_projection(root, inputs, records))
    coverage["evidence_navigation"] = evidence_coverage
    outputs["knowledge/current/coverage.json"] = encoded(coverage)
    topic_records = defaultdict(dict)
    topic_names = defaultdict(set)
    for record in records:
        for topic in record.get("topics", []):
            slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-") or digest(topic.encode())[:12]
            topic_records[slug][record["id"]] = record
            topic_names[slug].add(topic)
    browse = ["PUBLIC STATIC BROWSE | choose a scientific topic, then read one compact packet.",
              "Counts are exact record-topic associations, not field completeness or accepted-result counts.",
              "Routing aliases share a page only; this establishes no scientific connection.",
              "topic\trecords\tpath"]
    for slug, selected in sorted(topic_records.items()):
        path = "knowledge/current/browse/" + slug + ".tsv"
        rows = ["id\tkind\ttitle\tstatement_preview_not_a_proof\tpacket"]
        for record in selected.values():
            preview = re.sub(r"\s+", " ", flatten(record["statement"]))[:240]
            title = re.sub(r"\s+", " ", record["title"])
            rows.append("\t".join([record["id"], record["kind"], title, preview,
                                   "knowledge/current/packets/" + route_id(record["id"]) + ".json"]))
        outputs[path] = ("\n".join(rows) + "\n").encode()
        browse.append("\t".join([" / ".join(sorted(topic_names[slug])), str(len(selected)), path]))
    outputs["knowledge/current/browse/index.txt"] = ("\n".join(browse) + "\n").encode()
    input_version = digest(encoded({"authoring_inputs": inputs.hashes,
                                    "contextual_vectors_sha256": digest(outputs[VECTORS])}))
    outputs["knowledge/current/release.json"] = encoded({
        "schema": "astra.public-corpus-release.v1", "input_version": input_version,
        "manifest": "knowledge/current/manifest.json", "records": len(records),
        "source_context_layout": "linked-current-capsules-v1",
        "source_text_layout": TYPED_SOURCE_TEXT,
        "consumer_view_layout": CURRENT_CONSUMER_LAYOUT,
        "scope": "Complete ordinary build/check projection. Corpus identity covers cards, units, sources, corrections, runtime readers and exact contextual vector bytes; indexing confers no scientific acceptance."})
    outputs["knowledge/current/search_manifest.json"] = encoded({"input_version": input_version,
        "outputs": {name: digest(data) for name, data in outputs.items() if name.startswith((
            "knowledge/current/catalog", "knowledge/current/postings/", "knowledge/current/lexical/", "knowledge/current/packets/",
            "knowledge/current/operations", "knowledge/current/evidence/", "knowledge/current/content/"))}})
    manifest = {"schema": "astra.knowledge-manifest.v1", "inputs": dict(sorted(inputs.hashes.items())),
                "discovery": discovered, "outputs": {name: digest(data) for name, data in sorted(outputs.items())},
                "counts": coverage, "input_version": input_version}
    outputs[MANIFEST] = encoded(manifest)
    return outputs, manifest


def check(root=ROOT, regenerate=True):
    root = Path(root)
    path = root / MANIFEST
    if not path.is_file():
        raise ValueError("Current knowledge missing; run python3 knowledge/build.py build")
    manifest = json.loads(path.read_bytes())
    if inventory(root) != manifest["discovery"]:
        raise ValueError("Stale knowledge: input membership changed; run python3 knowledge/build.py build")
    actual = {path.relative_to(root).as_posix() for path in (root / "knowledge/current").rglob("*") if path.is_file()}
    if actual != set(manifest["outputs"]) | {MANIFEST}:
        raise ValueError("Stale knowledge: generated output membership changed")
    for group in ("inputs", "outputs"):
        for name, expected in manifest[group].items():
            if not local(root, name).is_file() or digest(local(root, name).read_bytes()) != expected:
                raise ValueError("Stale knowledge " + group + ": " + name + "; run python3 knowledge/build.py build")
    if regenerate:
        outputs, _ = build(root)
        for name, data in outputs.items():
            if not local(root, name).is_file() or local(root, name).read_bytes() != data:
                raise ValueError("Generated knowledge differs: " + name)
    return manifest


def publish(root, outputs):
    prior_path = root / MANIFEST
    prior = json.loads(prior_path.read_bytes()) if prior_path.is_file() else {"outputs": {}}
    for name, expected in prior["outputs"].items():
        target = local(root, name)
        if name not in outputs and target.is_file():
            if digest(target.read_bytes()) != expected:
                raise ValueError("Refusing to remove edited prior generated output: " + name)
            target.unlink()
    for name, data in outputs.items():
        target = local(root, name)
        if target.is_file() and target.read_bytes() == data:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as temporary:
            temporary.write(data)
            staged = Path(temporary.name)
        staged.replace(target)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "check"))
    args = parser.parse_args()
    try:
        if args.command == "build":
            outputs, manifest = build()
            publish(ROOT, outputs)
        else:
            manifest = check()
        print(json.dumps({"result": "ok", "command": args.command, "counts": manifest["counts"]}, ensure_ascii=False))
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
