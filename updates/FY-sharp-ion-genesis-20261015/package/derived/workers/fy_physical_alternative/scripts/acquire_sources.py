"""Acquire public primary-source bytes without modifying the Astra source checkout."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import urllib.request
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sources"
OUT.mkdir(exist_ok=True)
manifest = {
    "acquired_at_utc": datetime.now(timezone.utc).isoformat(),
    "astra_source_revision": "b32943eeb62d0d79929a9e572a344219a785ebf9",
    "record_doi": "10.5281/zenodo.13331446",
    "article_doi": "10.1038/s44286-024-00125-2",
    "preprint_doi": "10.26434/chemrxiv-2024-hb013",
    "downloads": [],
}

def acquire(url, name, expected_md5=None):
    entry = {"url": url, "local": "sources/" + name}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Astra-source-review/1.0"})
        with urllib.request.urlopen(req, timeout=60) as response:
            body = response.read()
            entry.update(final_url=response.url, content_type=response.headers.get("Content-Type"))
        if name.endswith(".pdf") and not body.startswith(b"%PDF"):
            raise ValueError("Response is not a PDF")
        if name.endswith(".xlsx") and not body.startswith(b"PK"):
            raise ValueError("Response is not an XLSX ZIP")
        entry.update(bytes=len(body), sha256=hashlib.sha256(body).hexdigest(),
                     md5=hashlib.md5(body).hexdigest(), status="acquired")
        if expected_md5:
            entry["repository_md5"] = expected_md5
            entry["repository_md5_matches"] = entry["md5"] == expected_md5
            if not entry["repository_md5_matches"]:
                raise ValueError("Repository checksum mismatch")
        (OUT / name).write_bytes(body)
    except Exception as exc:
        entry.update(status="failed", error=f"{type(exc).__name__}: {exc}")
        body = None
    manifest["downloads"].append(entry)
    (OUT / "SOURCE_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(name, entry["status"], entry.get("bytes", ""), entry.get("error", ""), flush=True)
    return body

api_bytes = acquire("https://zenodo.org/api/records/13331446", "zenodo_record_13331446.json")
if api_bytes:
    record = json.loads(api_bytes)
    manifest["zenodo_record_metadata"] = {
        key: record.get(key) for key in ["id", "created", "updated", "conceptrecid"]
    }
    for source in record["files"]:
        if source["key"].endswith(".xlsx"):
            acquire(source["links"]["self"], source["key"],
                    source["checksum"].removeprefix("md5:"))
else:
    # URLs and hashes are published in the record's file table.
    checksums = {
        "Source_Data_Fig.2.xlsx": "8d1330c89c1ddf0f03edb9266bc03f11",
        "Source_Data_Fig.3.xlsx": "b6deb17652e543cf6bc3d9abdcb30627",
        "Source_Data_Fig.4.xlsx": "ccd37cb921dee2c53f03775abc837928",
        "Source_Data_ED_Fig.4.xlsx": "57e4d7a143fd77b0692ff1cf80ac6dcd",
        "Source_Data_ED_Fig.6.xlsx": "6e228c0835d498d8077606de758310ef",
        "Source_Data_ED_Fig.7.xlsx": "3a35ed43094aea1568979252b95706dc",
    }
    for name, checksum in checksums.items():
        acquire("https://zenodo.org/records/13331446/files/" + name + "?download=1", name, checksum)

acquire("https://www.nature.com/articles/s44286-024-00125-2.pdf", "published_article.pdf")
acquire("https://www.cambridge.org/engage/api-gateway/coe/assets/orp/resource/item/66a1627a01103d79c58aaa83/original/flash-separation-of-metals-by-electrothermal-chlorination.pdf", "chemrxiv_v1_article.pdf")
manifest["warning"] = "Source bytes and checksums establish acquisition integrity only; source experiments were not independently reproduced."
(OUT / "SOURCE_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
