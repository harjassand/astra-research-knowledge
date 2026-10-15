#!/usr/bin/env python3
"""Create an explicit public allowlist and sanitized source receipts.

Transport headers/cookies, acquired fulltexts, original workbooks, spectra arrays,
PDF renders and extracted source text are preserved only in the excluded directory.
"""
from pathlib import Path
import hashlib
import json
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "external_excluded_from_publication" / "transport_receipts"
RAW.mkdir(exist_ok=True)
RECEIPTS = ROOT / "receipts"
allow_headers = {"content-type", "content-length", "content-disposition", "last-modified", "etag"}


def without_query(url):
    p = urlsplit(url)
    return urlunsplit((p.scheme, p.netloc, p.path, "", ""))


records = []
for path in sorted(RECEIPTS.glob("http_acquisition*.json")):
    original = RAW / path.name
    if not original.exists():
        original.write_bytes(path.read_bytes())
    rows = json.loads(original.read_text())
    public = []
    for row in rows:
        cleaned = {k: v for k, v in row.items() if k not in ("headers", "effective_url")}
        if "effective_url" in row:
            cleaned["effective_url_without_session_query"] = without_query(row["effective_url"])
        if "headers" in row:
            cleaned["public_content_headers"] = {k.lower(): v for k, v in row["headers"].items() if k.lower() in allow_headers}
        public.append(cleaned)
        records.append(cleaned)
    path.write_text(json.dumps(public, indent=2) + "\n")
unique = {}
for r in records:
    unique[(r["requested_url"], r.get("sha256"), r["status"])] = r
(RECEIPTS / "public_source_inventory.json").write_text(json.dumps({
    "scope": "public acquisition receipts only, not independent experimental verification",
    "source_response_count_deduplicated": len(unique),
    "sources": list(unique.values()),
    "private_transport_receipts": "preserved in excluded directory, no cookies published"
}, indent=2) + "\n")
public_files = []
for folder in (ROOT / "authored", RECEIPTS):
    for path in sorted(folder.glob("*")):
        if path.is_file():
            public_files.append({"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size,
                                 "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
(ROOT / "PUBLICATION_MANIFEST.json").write_text(json.dumps({
    "status": "authored material and sanitized receipts permitted for publication intake",
    "allowlist": public_files,
    "exclude_recursively": ["external_excluded_from_publication/", "authored/__pycache__/"],
    "instruction": "Copy only the explicit allowlist. Do not recursively copy this worker directory.",
    "scientific_scope": "Public-source acquisition and conditional reanalysis; no new experiment, calibrated transient flux, or acquired useful retained state."
}, indent=2) + "\n")
print(json.dumps({"public_file_count": len(public_files), "unique_source_responses": len(unique), "external_exclusion": True}))
