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
from knowledge.model import (ROOT, Inputs, compact_ref, digest, encoded, evidence_refs,
                             field_index, flatten, local, route_id, scientific_text, unique)
from knowledge.evidence import source_indexes

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


def packet_review(review, packet_evidence):
    """Reference review citations through the packet evidence array when complete."""
    result = dict(review)
    refs = [compact_ref(reference) for reference in evidence_refs(review.get("evidence", []))]
    positions = {encoded(reference): index for index, reference in enumerate(packet_evidence)}
    keys = [encoded(reference) for reference in refs]
    if refs and all(key in positions for key in keys):
        result.pop("evidence", None)
        result["evidence_ref_field"] = "evidence"
        result["evidence_ref_indices"] = [positions[key] for key in keys]
    return result


def build(root=ROOT):
    root = Path(root)
    inputs = Inputs(root)
    discovered = inventory(root)
    for name in ("knowledge/model.py", "knowledge/build.py", "knowledge/retrieve.py",
                 "knowledge/search.js", "knowledge/index.html", "knowledge/README.md",
                 "knowledge/INTAKE.md", "knowledge/operations.py", "knowledge/agent_search.py", "knowledge/evidence.py",
                 "knowledge/requirements-agent.txt", "knowledge/runtime/manifest.json",
                 "00_START_HERE.txt", "AGENTS.md", "agent/ACCESS.txt"):
        inputs.read(name)
    for name, expected in inputs.json("knowledge/runtime/manifest.json")["files"].items():
        if digest(inputs.read("knowledge/runtime/" + name)) != expected:
            raise ValueError("INGESTION FAILED: pinned retrieval model bytes changed: " + name)
    concepts = inputs.json("knowledge/concepts.json")
    claims = unique(inputs.rows("indexes/claims.jsonl", "indexes/claims.d"), "id")
    statuses = unique(inputs.rows("frontier/CURRENT_CLAIM_STATUS.jsonl", "frontier/CURRENT_CLAIM_STATUS.d"), "card_id")
    catalog_rows = inputs.json("indexes/agent_catalog.json")["claims"]
    for name in discovered["indexes/agent_catalog.d"]:
        catalog_rows.extend(inputs.json(name)["claims"])
    catalog = unique(catalog_rows, "id")
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

    def references(values):
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
        for index, (name, unit) in enumerate(versions):
            if unit["version"] != index + 1 or unit.get("previous") != (None if index == 0 else inputs.hashes[versions[index - 1][0]]):
                raise ValueError("Broken immutable unit version chain: " + identifier)
            refs = references(unit["evidence"])
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
        review_evidence = references(review["evidence"])
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

    documents = []
    for record in sorted(records, key=lambda item: item["id"]):
        documents.append({key: record[key] for key in ("id", "kind", "parents", "title", "statement", "contract", "body", "notices")}
                         | {"record_id": record["id"], "aliases": record.get("aliases", "")})
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
                       for record in sorted(records, key=lambda item: item["id"])]
    record_indexes = {record["record_id"]: index for index, record in enumerate(catalog_records)}
    catalog = [[record_indexes[document["record_id"]], int(document["kind"] == "source_window")] for document in documents]
    outputs["knowledge/current/catalog.json"] = encoded({"documents": catalog, "records": catalog_records, "concepts": concepts,
                                                        "shards": sorted(shards), "lexical_shards": sorted(lexical_shards)})
    for record in records:
        packet = dict(record)
        packet.pop("body", None)
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
            packet["source_excerpts"].append({"source": ref, "text": passage[:2400], "text_selection": selection,
                                              "excerpt_truncated": len(passage) > 2400})
        packet["transfers"] = [transfer for transfer in transfers if record["id"] in (transfer["from"], transfer["to"])]
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
        outputs["knowledge/current/packets/" + route_id(record["id"]) + ".json"] = encoded(packet)
    coverage = {
        "records_by_kind": dict(Counter(record["kind"] for record in records)),
        "source_windows": len(source_documents),
        "recoverable_exact_source_versions": len({(path, version) for path, version, _ in inputs.sources}),
        "distinct_source_text_hashes": len({version for _, version, _ in inputs.sources}),
        "topics": dict(Counter(topic for record in records for topic in record.get("topics", []))),
        "scope": "Scientific lane: all registered current cards, atlas entries, selected reusable units and latest technology, including located proof AND available evidence ranges. Separate evidence lane: current record evidence ranges and explicit selected-public-source-index entries, with exclusions and no inferred acceptance. Unregistered archives/withheld material remain unassessed.",
        "eligible_mechanism_denominator": "UNKNOWN", "scientific_acceptance": "Only explicit version-bound substantive review overlays confer acceptance; extraction and hashing do not.",
    }
    from knowledge.evidence import projection
    evidence_outputs, evidence_coverage = projection(root, inputs, records, discovered["selected_public_source_indexes"])
    outputs.update(evidence_outputs)
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
    outputs["knowledge/current/search_manifest.json"] = encoded({"input_version": digest(encoded(inputs.hashes)),
        "outputs": {name: digest(data) for name, data in outputs.items() if name.startswith((
            "knowledge/current/catalog", "knowledge/current/postings/", "knowledge/current/lexical/", "knowledge/current/packets/",
            "knowledge/current/operations", "knowledge/current/evidence/", "knowledge/current/content/"))}})
    manifest = {"schema": "astra.knowledge-manifest.v1", "inputs": dict(sorted(inputs.hashes.items())),
                "discovery": discovered, "outputs": {name: digest(data) for name, data in sorted(outputs.items())},
                "counts": coverage, "input_version": digest(encoded(inputs.hashes))}
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
