#!/usr/bin/env python3
"""Pin public chemistry sources and failed access attempts without credentials."""
import hashlib
import json
from pathlib import Path
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parent
SOURCES = [
    ("article.html", "https://pmc.ncbi.nlm.nih.gov/articles/PMC13339639/"),
    ("si_pmc_response.bin", "https://pmc.ncbi.nlm.nih.gov/articles/instance/13339639/bin/ja6c05959_si_001.pdf"),
    ("si_acs_response.bin", "https://pubs.acs.org/doi/suppl/10.1021/jacs.6c05959/suppl_file/ja6c05959_si_001.pdf"),
    ("pmc_oa_api.xml", "https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id=PMC13339639"),
    ("acs_figshare_response.html", "https://acs.figshare.com/doi/suppl/10.1021/jacs.6c05959"),
    ("github_tree.json", "https://api.github.com/repos/cernak-lab/cernakHTE/git/trees/449db5a012aca0cb24181ddcbb51d3fad6c2f98e?recursive=1"),
    ("globus_paper_unauth.json", "https://transfer.api.globus.org/v0.10/endpoint/1e0ff2e8-9139-4f7e-97a7-4954714bd34d/ls?path=/"),
    ("globus_notebook_unauth.json", "https://transfer.api.globus.org/v0.10/endpoint/bfd43535-052a-46bb-911a-b1cdfb1e92d7/ls?path=/spectral_deconvolution/matrix_completion"),
]


def fetch(name, url):
    item = {"url": url, "file": name, "access": "public request without authentication", "started_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    request = urllib.request.Request(url, headers={"User-Agent": "Astra evidence audit (public-source retrieval)", "Accept": "*/*"})
    start = time.monotonic()
    try:
        response = urllib.request.urlopen(request, timeout=45)
    except urllib.error.HTTPError as exc:
        response = exc
    except Exception as exc:
        item.update(error=type(exc).__name__ + ": " + str(exc), wall_seconds=time.monotonic() - start)
        return item
    with response:
        data = response.read()
        item.update(http_status=response.code, final_url=response.url, content_type=response.headers.get("Content-Type"), content_length_header=response.headers.get("Content-Length"), bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), wall_seconds=time.monotonic() - start, is_pdf=data.startswith(b"%PDF"))
    if b"reCAPTCHA" in data or b"Checking your browser" in data:
        item["semantic_status"] = "ACCESS_CHALLENGE_NOT_REQUESTED_ARTICLE_OR_PDF"
    elif name == "si_acs_response.bin" and not data.startswith(b"%PDF"):
        item["semantic_status"] = "ACCESS_DENIED_HTML_NOT_PDF"
    elif name.startswith("globus_"):
        item["semantic_status"] = "API_ERROR_NO_RAW_DATA_ACQUIRED" if response.code >= 400 else "RESPONSE_REQUIRES_SEMANTIC_INSPECTION"
    elif not data:
        item["semantic_status"] = "EMPTY_RESPONSE_NOT_SOURCE_CONTENT"
    elif response.code >= 400:
        item["semantic_status"] = "HTTP_ERROR_NOT_SOURCE_CONTENT"
    else:
        item["semantic_status"] = "SOURCE_BYTES_ACQUIRED"
    (ROOT / name).write_bytes(data)
    return item


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    receipts = [fetch(name, url) for name, url in SOURCES]
    inherited = ROOT.parent / "chemistry_search"
    existing = [inherited / "ord_dataset-805ad863feef48579d95d86a728035f4.parquet", *sorted((inherited / "source_code").rglob("*"))]
    si = ROOT.parent / "chemistry_incumbent" / "ja6c05959_si_001.pdf"
    if si.exists():
        existing.append(si)
    local = []
    for path in existing:
        if path.is_file():
            data = path.read_bytes()
            acquisition = "downloaded by chemistry_incumbent; independently rehashed here" if path == si else "already downloaded by chemistry_search worker; independently rehashed here"
            item = {"file": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "acquisition": acquisition}
            if path == si:
                item["source_url"] = "https://ndownloader.figshare.com/files/65650732"
            local.append(item)
    result = {"retrievals": receipts, "local_rehashes": local, "reproduction_scope": "Byte acquisition only; no chemistry or spectrometer measurement reproduced."}
    (ROOT / "SOURCE_BYTES_RECEIPT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
