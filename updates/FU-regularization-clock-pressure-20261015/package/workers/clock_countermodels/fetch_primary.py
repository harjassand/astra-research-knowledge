#!/usr/bin/env python3
"""Retain exact primary-source download receipts, including unsuccessful attempts."""
from pathlib import Path
import datetime
import hashlib
import json
import urllib.request

OUT = Path(__file__).resolve().parent
ITEMS = [
    ("absorbing_centrality", "https://arxiv.org/pdf/1509.02533", "pdf"),
    ("kinetic_path_sampling", "https://api.repository.cam.ac.uk/server/api/core/bitstreams/5d46a8bc-353c-4c65-be9f-8b7bb6448093/content", "pdf"),
    ("ill_conditioned_chains", "https://pmc.ncbi.nlm.nih.gov/articles/PMC10200351/", "html"),
    ("kulkarni_abstract", "https://pubsonline.informs.org/doi/abs/10.1287/opre.37.1.151", "html"),
    ("conditioned_markov", "https://pmc.ncbi.nlm.nih.gov/articles/PMC6824481/", "html"),
]

rows = []
for name, url, suffix in ITEMS:
    row = {"name": name, "requested_url": url, "retrieved_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (independent research source audit)"})
        with urllib.request.urlopen(request, timeout=35) as response:
            data = response.read()
            row.update({"http_status": response.status, "final_url": response.url,
                        "content_type": response.headers.get("Content-Type"), "bytes": len(data),
                        "sha256": hashlib.sha256(data).hexdigest()})
        path = OUT / "primary" / f"{name}.{suffix}"
        path.write_bytes(data)
        row["local_path"] = str(path)
        row["pdf_magic_valid"] = data.startswith(b"%PDF") if suffix == "pdf" else None
        row["possible_challenge"] = any(term in data[:10000].lower() for term in [b"recaptcha", b"checking your browser", b"captcha-delivery"])
        row["status"] = "DOWNLOADED_BYTES_NOT_YET_REVIEWED"
    except Exception as exc:
        row.update({"status": "FETCH_FAILED", "error": str(exc)})
    rows.append(row)
    print(json.dumps(row), flush=True)
(OUT / "primary_download_receipts.json").write_text(json.dumps(rows, indent=2)+"\n")
