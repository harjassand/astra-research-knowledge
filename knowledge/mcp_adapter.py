"""Bounded, version-pinned read-only adapter over the existing public library.

No transport, model dependency, corpus copy, source execution or publication.
"""
from __future__ import annotations

from collections import defaultdict
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import quote

from knowledge.build import inventory
from knowledge.evidence import search as evidence_search
from knowledge.model import Inputs, LEGACY_SOURCE_TEXT, compact_ref, digest, encoded, evidence_refs, flatten, route_id, scientific_text
from knowledge.operations import (statement_view, consumer_contract, acceptance_view,
                                  CURRENT_CONSUMER_LAYOUT, current_scope_navigation)
from knowledge.retrieve import Library

PUBLIC = "https://github.com/harjassand/astra-research-knowledge/blob/"
INLINE_SOURCE_CONTEXT = "inline-context-v1"
LINKED_SOURCE_CONTEXT = "linked-current-capsules-v1"


def record_menu(lanes, exact, records, limit=5):
    """Fuse support for a scientific family while retaining independent leaders.

    Different methods can find a parent and a buried unit of the same result.
    Those are one retrieval opportunity, not competing half-votes or two menu
    slots. Exact user-requested identities remain first, including siblings.
    """
    family = lambda identifier: (records[identifier].get("parents") or [identifier])[0]
    scores, member_scores, best_rank = defaultdict(float), defaultdict(float), {}
    members, leaders = defaultdict(set), []
    for lane in lanes:
        seen = set()
        for rank, hit in enumerate(lane, 1):
            identifier = hit["id"]
            group = family(identifier)
            if group in seen:
                continue
            seen.add(group)
            scores[group] += 1 / (60 + rank)
            member_scores[identifier] += 1 / (60 + rank)
            best_rank[identifier] = min(rank, best_rank.get(identifier, rank))
            members[group].add(identifier)
            if rank == 1 and group not in leaders:
                leaders.append(group)
    prefix = list(dict.fromkeys(exact))[:limit]
    represented = {family(identifier) for identifier in prefix}
    order = sorted(scores, key=lambda group: (-scores[group], group))
    remaining = limit - len(prefix)
    chosen = [group for group in leaders if group not in represented][:remaining]
    for group in order:
        if group not in represented and group not in chosen and len(chosen) < remaining:
            chosen.append(group)
    chosen.sort(key=lambda group: (-scores[group], group))
    for group in chosen:
        prefix.append(min(members[group], key=lambda identifier: (
            -member_scores[identifier], best_rank[identifier],
            records[identifier].get("kind") == "result", identifier)))
    return prefix


def source_context_layout(root, manifest):
    # Only a normalizer-declared,validated output can select a new layout.
    # Pre-marker snapshots (and every old source handle) retain their bytes.
    name = "knowledge/current/release.json"
    if name not in manifest["outputs"]:
        return INLINE_SOURCE_CONTEXT
    marker = json.loads((Path(root) / name).read_bytes())
    layout = marker.get("source_context_layout", INLINE_SOURCE_CONTEXT)
    if layout not in (INLINE_SOURCE_CONTEXT, LINKED_SOURCE_CONTEXT):
        raise ValueError("Unsupported published source context layout; deploy its reviewed reader")
    return layout


def consumer_view_layout(root, manifest):
    name = "knowledge/current/release.json"
    if name not in manifest["outputs"]:
        return None
    layout = json.loads((Path(root) / name).read_bytes()).get("consumer_view_layout")
    if layout not in (None, CURRENT_CONSUMER_LAYOUT):
        raise ValueError("Unsupported current consumer layout; deploy its reviewed reader")
    return layout


class ResearchAdapter:
    def __init__(self, root, method="portable", page_bytes=24000):
        if method not in ("portable", "agent") or not 1024 <= page_bytes <= 32768:
            raise ValueError("Use portable/agent and a 1024..32768 byte page budget")
        self.library = Library(root)
        self.root = self.library.root
        self.method, self.page_bytes = method, page_bytes
        self.revision = self.git("rev-parse", "HEAD").strip()
        self.manifest_bytes = (self.root / "knowledge/current/manifest.json").read_bytes()
        committed = self.git("show", "HEAD:knowledge/current/manifest.json").encode()
        if json.loads(committed) != json.loads(self.manifest_bytes):
            raise ValueError("Serve a committed corpus snapshot; generated views differ from HEAD")
        self.version = self.library.manifest["input_version"]
        self.source_text_layout = self.library.source_text_layout
        self.source_context_layout = source_context_layout(self.root, self.library.manifest)
        self.consumer_view_layout = consumer_view_layout(self.root, self.library.manifest)
        self.frozen_paths = set(self.library.manifest["inputs"]) | set(self.library.manifest["outputs"])
        self.paths = set(self.git("ls-tree", "-r", "--name-only", "-z", "HEAD").split("\0")) - {""}
        self.references, self.contexts = {}, defaultdict(set)
        self.locators, self.artifact_data = {}, {}
        self.identities = defaultdict(set)
        for record in self.library.records.values():
            self.identities[record["id"].casefold()].add(record["id"])
            prefix = record["id"].split("-", 1)[0]
            if re.fullmatch(r"[A-Za-z]+\d+", prefix):
                self.identities[prefix.casefold()].add(record["id"])
        for record in self.library.records.values():
            for reference in evidence_refs(record):
                self.register(reference)
                self.contexts[(reference["path"], reference["sha256"])].add(record["id"])
            for previous in record.get("history", []):
                self.register(dict(previous, lines=None))
                self.contexts[(previous["path"], previous["sha256"])].add(record["id"])
        for artifact in self.library.rows("evidence/artifacts.jsonl"):
            ref = artifact["source"]
            self.contexts[(ref["path"], ref["sha256"])].update(artifact["cited_by"])
            self.register(ref)
        for document in self.library.rows("evidence/documents.jsonl"):
            self.register(document["source"])

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.root), *args], text=True)

    def current(self):
        # A server is a read-only snapshot. Restart after the ordinary intake's
        # build/check/commit; old handles must never silently resolve to new data.
        if self.git("rev-parse", "HEAD").strip() != self.revision or (self.root / "knowledge/current/manifest.json").read_bytes() != self.manifest_bytes:
            raise ValueError("Corpus snapshot changed; restart the server and search again")
        # New staged/untracked authoring paths are not in frozen_paths. Use
        # the normalizer's filesystem inventory, including source indexes.
        try:
            discovery = inventory(self.root)
        except (OSError, ValueError):
            raise ValueError("Corpus discovery cannot be validated; finish intake and restart the server") from None
        if discovery != self.library.manifest["discovery"]:
            raise ValueError("Corpus discovery membership changed; finish intake and restart the server")
        if self.frozen_paths.intersection(self.git("diff", "--name-only", "-z", "HEAD").split("\0")):
            raise ValueError("Corpus snapshot has uncommitted source/view edits; finish intake and restart")

    def handle(self, kind, value):
        return "astra:" + self.version + ":" + kind + ":" + value

    def register(self, reference):
        reference = compact_ref(reference)
        key = digest(encoded(reference))
        self.references[key] = reference
        return self.handle("source", key)

    def url(self, path, lines=None):
        if path not in self.paths:
            raise ValueError("No committed public citation path: " + path)
        fragment = "#L%d-L%d" % tuple(lines) if lines else ""
        return PUBLIC + self.revision + "/" + quote(path, safe="/") + fragment

    def source_locator(self, ref):
        key = (ref["path"], ref["sha256"], ref.get("read_path"), tuple(ref.get("lines") or ()))
        if key in self.locators:
            return self.locators[key]
        for name in dict.fromkeys((ref["path"], ref.get("read_path", ""))):
            if name not in self.paths:
                continue
            if name not in self.artifact_data:
                with (self.root / name).open("rb") as stream:
                    actual = hashlib.file_digest(stream, "sha256").hexdigest()
                self.artifact_data[name] = {"sha256": actual}
            cached = self.artifact_data[name]
            actual = cached["sha256"]
            selector = None
            if actual == ref["sha256"]:
                selector = "exact artifact bytes; inclusive text lines where supplied"
                url = self.url(name, ref.get("lines"))
            elif name.endswith(".html"):
                if "pre_hashes" not in cached:
                    blocks = re.findall(r"<pre(?:\s[^>]*)?>(.*?)</pre>", (self.root / name).read_bytes().decode("utf-8"), re.S)
                    cached["pre_hashes"] = {digest(html.unescape(block).encode()) for block in blocks}
                if ref["sha256"] in cached["pre_hashes"]:
                    selector = "HTML pre block matching source text SHA256; extracted-text lines are not HTML-file lines"
                    url = self.url(name)
            if selector:
                value = {"url": url, "artifact_path": name, "artifact_sha256": actual,
                         "source_text_sha256": ref["sha256"], "selector": selector}
                self.locators[key] = value
                return value
        raise ValueError("No hash-matched committed public citation artifact: " + ref["path"])

    def source_url(self, ref):
        return self.source_locator(ref)["url"]

    def record_url(self, identifier):
        return self.url("knowledge/current/packets/" + route_id(identifier) + ".json")

    def search(self, query):
        self.current()
        if not isinstance(query, str) or not query.strip() or len(query) > 10000:
            raise ValueError("query must contain 1..10000 characters")
        exact = []
        for token in re.findall(r"[A-Za-z0-9][A-Za-z0-9_-]*", query):
            matches = self.identities.get(token.casefold(), set())
            if len(matches) == 1:
                identifier = next(iter(matches))
                if identifier not in exact:
                    exact.append(identifier)
        fallback, lanes, lane_names, notice_matches, current_scope_candidates = None, [], [], {}, {}
        if self.method == "agent":
            try:
                lanes.append(self.library.search(query, method="semantic", limit=8)["results"])
                lane_names.append("semantic")
            except ValueError as error:
                if not str(error).startswith(("Contextual runtime missing", "Contextual index unavailable")):
                    raise
                fallback = str(error)
            try:
                lane = self.library.search(query, method="rerank", limit=8)["results"]
                lanes.append(lane)
                lane_names.append("rerank")
                notice_matches = {hit["id"]: hit["notice_match"] for hit in lane if "notice_match" in hit}
                current_scope_candidates = {hit["id"]: hit["current_scope_candidate"] for hit in lane if "current_scope_candidate" in hit}
            except ValueError as error:
                if "Agent runtime missing" not in str(error):
                    raise
                fallback = "; ".join(item for item in (fallback, str(error)) if item)
        for method in ("structured", "content"):
            lanes.append(self.library.search(query, method=method, limit=8)["results"])
            lane_names.append(method)
        records = []
        selected = record_menu(lanes, exact, self.library.records)
        family = lambda identifier: (self.library.records[identifier]["parents"] or [identifier])[0]
        for identifier in selected:
            record = self.library.records[identifier]
            preview = {}
            for field in ("requires", "provides", "assumptions", "costs", "obstruction"):
                text = flatten(consumer_contract(record).get(field, "UNKNOWN"))
                preview[field] = {"text": text[:200], "omitted_characters": max(0, len(text) - 200)}
            records.append({"id": self.handle("current", identifier), "title": record["title"],
                "url": self.record_url(identifier), "metadata": {"record_id": identifier,
                "content_version": record["content_version"], "kind": record["kind"],
                "operation_preview": preview, "preview_scope": "Partial candidate preview; fetch complete conditions/corrections before reuse",
                "current_notice_count": len(record["notices"]), "candidate_only": True}})
            records[-1]["metadata"]["retrieval_lanes"] = [name for name, lane in zip(lane_names, lanes)
                if any(family(hit["id"]) == family(identifier) for hit in lane)]
            if record.get("current_acceptance"):
                records[-1]["metadata"]["acceptance"] = acceptance_view(record, preview=True)
            records[-1]["metadata"]["independent_leader_lanes"] = [name for name, lane in zip(lane_names, lanes)
                if lane and family(lane[0]["id"]) == family(identifier)]
            if identifier in notice_matches:
                records[-1]["metadata"]["matching_current_notice"] = notice_matches[identifier]
            if identifier in current_scope_candidates:
                records[-1]["metadata"]["current_scope_candidate"] = current_scope_candidates[identifier]
            current_scope = current_scope_navigation(record, self.library.records, limit=3)
            if current_scope["total_routes"]:
                for route in current_scope["routes"]:
                    route["fetch_id"] = self.handle("current", route["id"])
                    route["url"] = self.record_url(route["id"])
                records[-1]["metadata"]["current_scope_navigation"] = current_scope
            navigation = self.interface_view(identifier, preview=True)
            if navigation["routes"] or navigation["total_candidates"]:
                records[-1]["metadata"]["shared_consumer_navigation"] = navigation
        sources, seen = [], set()
        for hit in evidence_search(self.library, query, limit=20)["results"]:
            ref = hit["source"]
            key = (ref["path"], ref["sha256"])
            if key in seen:
                continue
            seen.add(key)
            sources.append({"id": self.register(ref), "title": hit["title"],
                "url": self.source_url(ref), "metadata": {"source": ref, "citation_locator": self.source_locator(ref),
                "record_context": sorted(self.contexts[key]), "candidate_only": True}})
            if len(sources) == 3:
                break
        return {"results": records + sources, "metadata": {"input_version": self.version,
            "revision": self.revision, "method": self.method, "fallback": fallback,
            "exact_identifier_matches": exact[:5], "omitted_identifier_matches": max(0, len(exact) - 5),
            "identifier_scope": "Existing canonical IDs and unambiguous numeric prefixes; no topical alias, acceptance or applicability inferred.",
            "record_menu_scope": "Family rank fusion retains independent method leaders and avoids duplicate family slots. Exact requested IDs remain first. Family membership is navigation, not compatible composition or inherited acceptance.",
            "scope": "Candidate menu only. Fetch conditions, current corrections and governing passages before reuse; absence is not impossibility."}}

    def reference_view(self, ref):
        return {"source": ref, "url": self.source_url(ref), "citation_locator": self.source_locator(ref), "fetch_id": self.register(ref)}

    def interface_view(self, identifier, preview=False):
        navigation = self.library.peers(identifier, limit=3 if preview else 8)
        # Old handles keep their original record-view routes/payload bytes.
        route_kind = "current" if getattr(self, "consumer_view_layout", None) else "record"
        navigation["routes"] = [dict(route,
            provider_fetch_id=self.handle(route_kind, route["provider"]),
            consumer_fetch_id=self.handle(route_kind, route["consumer"]))
            for route in navigation["routes"]]
        navigation["consumers"] = [dict(route,
            consumer_fetch_id=self.handle(route_kind, route["consumer"]))
            for route in navigation["consumers"]]
        for item in navigation["candidates"]:
            item["fetch_id"] = self.handle(route_kind, item["provider"])
            item["consumer_fetch_id"] = self.handle(route_kind, item["consumer"])
            if preview:
                # Keep the named quantity and qualification visible. Full
                # bindings and all provider conditions remain fetchable.
                binding = {}
                for key, value in item["binding"].items():
                    text = flatten(value)
                    binding[key] = {"text": text[:160],
                                    "omitted_characters": max(0, len(text) - 160)}
                item["binding"] = binding
        navigation["continuation"] = "Fetch the named consumer for its complete provider bindings; fetch each provider and governing source before reuse. A common consumer does not establish a transfer between providers."
        return navigation

    def record_payload(self, record):
        packet = self.library.packet([record["id"]], max_bytes=16 * 1024 * 1024)["packets"][0]
        route_kind = "current" if getattr(self, "consumer_view_layout", None) else "record"
        context_routes = {}
        for role, value in (("current_review", record["review_overlays"]),
                            ("current_notice", record["notices"]),
                            ("historical_review", packet["historical_reviews"])):
            for ref in evidence_refs(value):
                identifier = self.register(ref)
                route = context_routes.setdefault(identifier, dict(self.reference_view(ref), roles=[]))
                if role not in route["roles"]:
                    route["roles"].append(role)
        return {"scope": "Current operation capsule. Historical reported labels do not override current version-bound reviews. Conditions do not establish acquired inputs, measurements, devices, novelty or advantage.",
            "id": record["id"], "content_version": record["content_version"],
            **statement_view(record, self.library.operation_frames[record["id"]]),
            "contract": consumer_contract(record), "review_overlays": record["review_overlays"],
            "notices": packet["notices"], "reported_review": record["review"],
            "historical_reviews": packet["historical_reviews"],
            "dependencies": packet.get("dependencies", "UNKNOWN; this packet has no explicit dependency list"),
            "parents": record["parents"],
            "evidence": [self.reference_view(ref) for ref in record["evidence"]],
            "review_and_correction_sources": list(context_routes.values()),
            "related_units": [dict(unit, fetch_id=self.handle("record", unit["id"])) for unit in packet["related_units"]],
            "transfers": packet.get("transfers", []),
            "shared_consumer_navigation": self.interface_view(record["id"], preview=True),
            "consumer_bindings": [dict(item,
                provider_fetch_id=self.handle(route_kind, item["provider"]),
                consumer_fetch_id=self.handle(route_kind, item["consumer"]))
                for item in packet.get("interface_navigation", {}).get("bindings", [])],
            "consumer_binding_scope": "Complete mappings appear once in transfers[*].slot_binding; consumer_bindings references those same exact-version transfers. Peer previews require fetching the named provider and consumer.",
            "historical_versions": [dict(v, fetch_id=self.register(dict(v, lines=None)), url=self.url(v["path"])) for v in record.get("history", [])],
            "full_packet_url": self.record_url(record["id"])}

    def source_payload(self, ref):
        contexts = [self.library.records[i] for i in sorted(self.contexts[(ref["path"], ref["sha256"])])]
        current_context = [{"id": r["id"], "content_version": r["content_version"],
            "notices": r["notices"], "fetch_id": self.handle("record", r["id"])} for r in contexts]
        context_scope = {}
        if self.source_context_layout == LINKED_SOURCE_CONTEXT:
            current_context = [{"id": r["id"], "content_version": r["content_version"],
                "notice_count": len(r["notices"]), "fetch_id": self.handle("current", r["id"])} for r in contexts]
            context_scope = {
                "current_context_layout": LINKED_SOURCE_CONTEXT,
                "current_context_scope": "These records cite the same artifact; this is navigation, not a claim-specific proof or acceptance transfer. notice_count counts outer current notice entries, including inherited wrappers.",
                "required_context_action": "Before reusing a result from this source, fetch that result's linked current capsule and every continuation. Its complete conditions, current corrections, source-reported gaps and scoped reviews remain there. This source response links those notices instead of repeating them for every citing record."}
        if ref.get("lines") is None:
            if (self.root / ref["path"]).is_file():
                raw = Inputs(self.root).read(ref["path"])
                if digest(raw) == ref["sha256"]:
                    try:
                        text = raw.decode("utf-8")
                    except UnicodeError:
                        return {"scope": "Binary original only; no inferred proof passage or acceptance.",
                            "source": ref, "url": self.source_url(ref), "citation_locator": self.source_locator(ref), "current_context": current_context, **context_scope}
                else:
                    text, _ = Inputs(self.root).source(ref)
            else:
                text, _ = Inputs(self.root).source(ref)
            start, end = 1, len(text.splitlines())
            passage, selection = text, "whole declared UTF8 original; not a claim-specific proof range"
        else:
            _, passage = Inputs(self.root).source(ref)
            start, end = ref["lines"]
            passage, selection = scientific_text(passage, layout=getattr(self, "source_text_layout", LEGACY_SOURCE_TEXT))
        return {"scope": "Exact declared source version. Current context notices remain applicable to reuse; coarchive and citation do not confer acceptance. A historical unit document retains its historical status and does not inherit the current review.",
            "source": ref, "text_selection": selection, "text": passage,
            "citation_locator": self.source_locator(ref),
            "current_context": current_context,
            **context_scope,
            "full_source_url": self.source_url(ref), "extracted_text_lines": [start, end]}

    def history_payload(self, record):
        original = self.record_payload(record)
        return {"scope": "Source-reported assessment and historical versions. These labels do not override current version-bound acceptance. Fetch the linked current scope before reuse.",
            "id": record["id"], "content_version": record["content_version"],
            "current_scope_fetch_id": self.handle("current", record["id"]),
            "reported_review": original["reported_review"],
            "historical_reviews": original["historical_reviews"],
            "historical_versions": original["historical_versions"],
            "full_packet_url": original["full_packet_url"]}

    def current_payload(self, record):
        # Keep the legacy record/source codecs unchanged: an old continuation
        # must not acquire different bytes merely because the reader upgraded.
        original = self.record_payload(record)
        result = {key: value for key, value in original.items()
                  if key not in ("reported_review", "historical_reviews", "historical_versions")}
        def locator_link(view):
            # The complete hash-matched selector remains on the source fetch.
            # Avoid printing its URL/path/hash a second time in every capsule.
            return {key: value for key, value in view.items() if key != "citation_locator"}
        result["evidence"] = [locator_link(entry) for entry in result["evidence"]]
        routes = {}
        primary = {entry["fetch_id"]: i for i, entry in enumerate(result["evidence"])}
        for route in original["review_and_correction_sources"]:
            roles = [r for r in route["roles"] if r != "historical_review"]
            if roles:
                routes[route["fetch_id"]] = dict(locator_link(self.reference_view(compact_ref(route["source"]))), roles=roles)

        def references(value, role):
            if isinstance(value, list):
                return [references(item, role) for item in value]
            if isinstance(value, dict):
                if isinstance(value.get("path"), str) and isinstance(value.get("sha256"), str):
                    ref = compact_ref(value); handle = self.register(ref)
                    if handle not in primary:
                        route = routes.setdefault(handle, dict(locator_link(self.reference_view(ref)), roles=[]))
                        if role not in route["roles"]:
                            route["roles"].append(role)
                    annotations = {key: data for key, data in value.items() if key not in ref}
                    return {"source_fetch_id": handle, **({"source_ref_annotations": annotations} if annotations else {})}
                return {key: references(data, role) for key, data in value.items()}
            return value

        result["notices"] = references(original["notices"], "current_notice")
        result["review_overlays"] = references(original["review_overlays"], "current_review")
        result["transfers"] = references(original["transfers"], "documented_transfer")
        result["source_reported_gaps"] = references(original["reported_review"].get("gaps", []), "source_reported_gap")
        if any(item.get("legacy_status_fields_are_historical") for item in record.get("current_acceptance", [])):
            result.pop("source_reported_gaps")
            result["historical_source_assessment"] = {"fetch_id": self.handle("history", record["id"]),
                "scope": "Earlier review/status and validation prerequisites are superseded for programme correctness by the explicit current human acceptance. Full original assessment and evidence remain at this history route; current scientific conditions remain in the contract."}
        result["review_and_correction_sources"] = [
            {"fetch_id": identifier, "evidence_ref_field": "evidence", "evidence_ref_index": primary[identifier],
             "roles": route["roles"]} if identifier in primary else route
            for identifier, route in routes.items()]
        result["history"] = {"fetch_id": self.handle("history", record["id"]),
            "scope": "Original source-reported status/validation and historical versions; conditions are not discharged by moving status labels."}
        result["related_units"] = [dict(unit, fetch_id=self.handle("current", unit["id"])) for unit in result["related_units"]]
        result["scope"] = "Current scientific scope. All current conditions, source-reported gaps, corrections and version-bound reviews remain. Original source-reported status/validation and history are linked separately; no scientific qualification is discharged by this view."
        result["reference_scope"] = "source_fetch_id replaces a duplicate citation only. Source specifications and public routes are in evidence or review_and_correction_sources; the complete artifact selector stays on its source fetch. source_ref_annotations retains all original per-citation annotations. Read every correction and governing passage before reuse."
        result["citation_locator_scope"] = "Source fetches retain the complete artifact hash/selector, including HTML pre-block distinctions. This view omits only the duplicated locator; each source and hash-matched public URL remain."
        return result

    def fetch(self, identifier):
        self.current()
        if not isinstance(identifier, str):
            raise ValueError("id must be a search/fetch handle or a known current record ID")
        if not identifier.startswith("astra:"):
            identifier = self.handle("record", self.library.resolve(identifier)["id"])
        fields = identifier.split(":")
        if len(fields) not in (4, 5) or fields[0] != "astra" or fields[1] != self.version:
            raise ValueError("Unknown or stale snapshot handle; search again")
        _, _, kind, value = fields[:4]
        offset = int(fields[4]) if len(fields) == 5 else 0
        base_id = ":".join(fields[:4])
        if kind == "record":
            record = self.library.resolve(value)
            payload, title, url = self.record_payload(record), record["title"], self.record_url(record["id"])
        elif kind in ("current", "history"):
            record = self.library.resolve(value)
            payload = self.current_payload(record) if kind == "current" else self.history_payload(record)
            title, url = record["title"], self.record_url(record["id"])
        elif kind == "source" and value in self.references:
            ref = self.references[value]
            payload, title, url = self.source_payload(ref), Path(ref["path"]).name, self.source_url(ref)
        else:
            raise ValueError("Unknown fetch handle")
        raw = encoded(payload)
        if not 0 <= offset < len(raw) or (offset and raw[offset] & 0xC0 == 0x80):
            raise ValueError("Invalid continuation byte offset")
        end = min(offset + self.page_bytes, len(raw))
        while end < len(raw) and raw[end] & 0xC0 == 0x80:
            end -= 1
        more = end < len(raw)
        complete_action = (payload["required_context_action"] if kind == "source"
            and self.source_context_layout == LINKED_SOURCE_CONTEXT else
            "Read evidence fetch routes for the governing proof; a capsule is not the proof.")
        return {"id": identifier, "title": title, "text": raw[offset:end].decode("utf-8"), "url": url,
            "metadata": {"input_version": self.version, "revision": self.revision,
                "payload_view": kind,
                "payload_sha256": digest(raw), "payload_bytes": len(raw), "byte_range": [offset, end],
                "encoding": "UTF8 JSON; concatenate text pages before parsing a multipart payload",
                "partial": offset > 0 or more, "next_id": base_id + ":" + str(end) if more else None,
                "required_action": "Read every continuation before treating conditions/corrections as complete." if offset or more else complete_action}}
