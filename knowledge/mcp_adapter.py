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

from knowledge.evidence import search as evidence_search
from knowledge.model import Inputs, compact_ref, digest, encoded, evidence_refs, flatten, route_id, scientific_text
from knowledge.operations import statement_view
from knowledge.retrieve import Library

PUBLIC = "https://github.com/harjassand/astra-research-knowledge/blob/"


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
        self.frozen_paths = set(self.library.manifest["inputs"]) | set(self.library.manifest["outputs"])
        self.paths = set(self.git("ls-tree", "-r", "--name-only", "-z", "HEAD").split("\0")) - {""}
        self.references, self.contexts = {}, defaultdict(set)
        self.locators, self.artifact_data = {}, {}
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
        fallback, lanes, notice_matches = None, [], {}
        if self.method == "agent":
            try:
                lane = self.library.search(query, method="agent", limit=8)["results"]
                lanes.append(lane)
                notice_matches = {hit["id"]: hit["notice_match"] for hit in lane if "notice_match" in hit}
            except ValueError as error:
                if "Agent runtime missing" not in str(error):
                    raise
                fallback = str(error)
        for method in ("structured", "content"):
            lanes.append(self.library.search(query, method=method, limit=8)["results"])
        # Reciprocal ranks merge independent candidate lanes without comparing
        # incompatible score scales. This is candidate retrieval, not a proof.
        scores, hits = defaultdict(float), {}
        for lane in lanes:
            for rank, hit in enumerate(lane, 1):
                scores[hit["id"]] += 1 / (60 + rank)
                hits[hit["id"]] = hit
        records = []
        for identifier in sorted(hits, key=lambda i: (-scores[i], i))[:5]:
            record = self.library.records[identifier]
            preview = {}
            for field in ("requires", "provides", "assumptions", "costs", "obstruction"):
                text = flatten(record["contract"].get(field, "UNKNOWN"))
                preview[field] = {"text": text[:200], "omitted_characters": max(0, len(text) - 200)}
            records.append({"id": self.handle("record", identifier), "title": record["title"],
                "url": self.record_url(identifier), "metadata": {"record_id": identifier,
                "content_version": record["content_version"], "kind": record["kind"],
                "operation_preview": preview, "preview_scope": "Partial candidate preview; fetch complete conditions/corrections before reuse",
                "current_notice_count": len(record["notices"]), "candidate_only": True}})
            if identifier in notice_matches:
                records[-1]["metadata"]["matching_current_notice"] = notice_matches[identifier]
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
            "scope": "Candidate menu only. Fetch conditions, current corrections and governing passages before reuse; absence is not impossibility."}}

    def reference_view(self, ref):
        return {"source": ref, "url": self.source_url(ref), "citation_locator": self.source_locator(ref), "fetch_id": self.register(ref)}

    def interface_view(self, identifier, preview=False):
        navigation = self.library.peers(identifier, limit=3 if preview else 8)
        navigation["routes"] = [dict(route,
            provider_fetch_id=self.handle("record", route["provider"]),
            consumer_fetch_id=self.handle("record", route["consumer"]))
            for route in navigation["routes"]]
        navigation["consumers"] = [dict(route,
            consumer_fetch_id=self.handle("record", route["consumer"]))
            for route in navigation["consumers"]]
        for item in navigation["candidates"]:
            item["fetch_id"] = self.handle("record", item["provider"])
            item["consumer_fetch_id"] = self.handle("record", item["consumer"])
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
            "contract": record["contract"], "review_overlays": record["review_overlays"],
            "notices": record["notices"], "reported_review": record["review"],
            "historical_reviews": packet["historical_reviews"],
            "dependencies": packet.get("dependencies", "UNKNOWN; this packet has no explicit dependency list"),
            "parents": record["parents"],
            "evidence": [self.reference_view(ref) for ref in record["evidence"]],
            "review_and_correction_sources": list(context_routes.values()),
            "related_units": [dict(unit, fetch_id=self.handle("record", unit["id"])) for unit in packet["related_units"]],
            "transfers": packet.get("transfers", []),
            "shared_consumer_navigation": self.interface_view(record["id"], preview=True),
            "consumer_bindings": [dict(item,
                provider_fetch_id=self.handle("record", item["provider"]),
                consumer_fetch_id=self.handle("record", item["consumer"]))
                for item in packet.get("interface_navigation", {}).get("bindings", [])],
            "consumer_binding_scope": "Complete mappings appear once in transfers[*].slot_binding; consumer_bindings references those same exact-version transfers. Peer previews require fetching the named provider and consumer.",
            "historical_versions": [dict(v, fetch_id=self.register(dict(v, lines=None)), url=self.url(v["path"])) for v in record.get("history", [])],
            "full_packet_url": self.record_url(record["id"])}

    def source_payload(self, ref):
        contexts = [self.library.records[i] for i in sorted(self.contexts[(ref["path"], ref["sha256"])])]
        current_context = [{"id": r["id"], "content_version": r["content_version"],
            "notices": r["notices"], "fetch_id": self.handle("record", r["id"])} for r in contexts]
        if ref.get("lines") is None:
            if (self.root / ref["path"]).is_file():
                raw = Inputs(self.root).read(ref["path"])
                if digest(raw) == ref["sha256"]:
                    try:
                        text = raw.decode("utf-8")
                    except UnicodeError:
                        return {"scope": "Binary original only; no inferred proof passage or acceptance.",
                            "source": ref, "url": self.source_url(ref), "citation_locator": self.source_locator(ref), "current_context": current_context}
                else:
                    text, _ = Inputs(self.root).source(ref)
            else:
                text, _ = Inputs(self.root).source(ref)
            start, end = 1, len(text.splitlines())
            passage, selection = text, "whole declared UTF8 original; not a claim-specific proof range"
        else:
            _, passage = Inputs(self.root).source(ref)
            start, end = ref["lines"]
            passage, selection = scientific_text(passage)
        return {"scope": "Exact declared source version. Current context notices remain applicable to reuse; coarchive and citation do not confer acceptance. A historical unit document retains its historical status and does not inherit the current review.",
            "source": ref, "text_selection": selection, "text": passage,
            "citation_locator": self.source_locator(ref),
            "current_context": current_context,
            "full_source_url": self.source_url(ref), "extracted_text_lines": [start, end]}

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
        return {"id": identifier, "title": title, "text": raw[offset:end].decode("utf-8"), "url": url,
            "metadata": {"input_version": self.version, "revision": self.revision,
                "payload_sha256": digest(raw), "payload_bytes": len(raw), "byte_range": [offset, end],
                "encoding": "UTF8 JSON; concatenate text pages before parsing a multipart payload",
                "partial": offset > 0 or more, "next_id": base_id + ":" + str(end) if more else None,
                "required_action": "Read every continuation before treating conditions/corrections as complete." if offset or more else "Read evidence fetch routes for the governing proof; a capsule is not the proof."}}
