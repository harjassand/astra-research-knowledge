#!/usr/bin/env python3
"""Acquire public primary-source bytes; keep external content outside publication.

No experiments, account credentials or private session headers are used. The receipts
retain requested public URLs, response status, content type/signature and hashes.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import hashlib
import json
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
EXT = ROOT / "external_excluded_from_publication"
REC = ROOT / "receipts"
EXT.mkdir(parents=True, exist_ok=True)
REC.mkdir(parents=True, exist_ok=True)


def acquire(item):
    name, url = item
    rec = {"name": name, "requested_url": url,
           "retrieved_at_utc": datetime.now(timezone.utc).isoformat()}
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0 (scientific source audit)"})
        try:
            response = urlopen(req, timeout=35)
        except HTTPError as e:
            response = e
        with response:
            data = response.read()
            rec.update(status_code=response.status, bytes=len(data),
                       content_type=response.headers.get("Content-Type"),
                       effective_url=response.url.split("?")[0],
                       sha256=hashlib.sha256(data).hexdigest(), magic_hex=data[:20].hex())
        ok = rec["status_code"] == 200
        if name.endswith(".pdf"):
            ok = ok and data.startswith(b"%PDF-")
        if name.endswith(".zip"):
            ok = ok and data.startswith(b"PK")
        if name.endswith(".html"):
            # HTTP 200 alone is not acquisition of an article body.
            low = data.lower()
            ok = ok and b"non-faradaic promotion of ethylene" in low and b"checking your browser" not in low
        if name.endswith(".xml"):
            try:
                parsed = ET.fromstring(data)
                rec["xml_root"] = parsed.tag
                if name == "Lim2021_fulltext.xml":
                    ok = ok and parsed.tag == "article"
            except ET.ParseError:
                ok = False
        rec["status"] = "ACQUIRED" if ok else "FAILED_OR_WRONG_CONTENT"
        dest = EXT / (name if ok else name + ".failed_response")
        dest.write_bytes(data)
        rec["relative_path"] = str(dest.relative_to(ROOT))
    except Exception as e:
        rec.update(status="NETWORK_ERROR", error=repr(e))
    return rec


URLS = [
    ("Lim2021_fulltext.xml", "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8395646/fullTextXML"),
    ("Lim2021_pmc.html", "https://pmc.ncbi.nlm.nih.gov/articles/PMC8395646/"),
    ("Lim2021_acs.html", "https://pubs.acs.org/doi/10.1021/jacsau.1c00044"),
    ("Lim2021_si.pdf", "https://pubs.acs.org/doi/suppl/10.1021/jacsau.1c00044/suppl_file/au1c00044_si_001.pdf"),
    ("Lim2021_oa.xml", "https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id=PMC8395646"),
    ("Lim2021_supplementary.zip", "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8395646/supplementaryFiles"),
    ("Lim2021_si_cdn.pdf", "https://cdn.ncbi.nlm.nih.gov/pmc/blobs/6b69/8395646/ecffa52629c4/au1c00044_si_001.pdf"),
    ("Lim2021_main_cdn.pdf", "https://cdn.ncbi.nlm.nih.gov/pmc/blobs/6b69/8395646/ad6acacc3006/au1c00044.pdf"),
]
LINKED_URLS = [
    ("Lim2021_si_pmc.pdf", "https://pmc.ncbi.nlm.nih.gov/articles/instance/8395646/bin/au1c00044_si_001.pdf"),
    ("Lim2021_main_pmc.pdf", "https://pmc.ncbi.nlm.nih.gov/articles/PMC8395646/pdf/au1c00044.pdf"),
]
if __name__ == "__main__":
    items = LINKED_URLS if "--linked-only" in sys.argv else URLS
    with ThreadPoolExecutor(max_workers=5) as pool:
        results = list(pool.map(acquire, items))
    for result in results:
        print(json.dumps({k: result[k] for k in ("name", "status", "status_code", "bytes") if k in result}))
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    (REC / ("primary_acquisition_" + stamp + ".json")).write_text(json.dumps(results, indent=2) + "\n")
    old = REC / "primary_acquisition.json"
    if "--linked-only" in sys.argv and old.exists():
        results = json.loads(old.read_text()) + results
    old.write_text(json.dumps(results, indent=2) + "\n")
    xml = EXT / "Lim2021_fulltext.xml"
    if xml.exists():
        doc = ET.fromstring(xml.read_bytes())
        (EXT / "Lim2021_fulltext.txt").write_text("\n\n".join("".join(x.itertext()) for x in doc.findall(".//p")))
