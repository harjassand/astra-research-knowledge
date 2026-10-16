#!/usr/bin/env python3
"""Acquire only primary papers into the segregated acquired/ directory."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import urllib.request

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "acquired"
SOURCES = [
    ("watrous_2009_cb_sdp", "https://cs.uwaterloo.ca/~watrous/Papers/SDPforCBnorms.pdf"),
    ("gutoski_watrous_2007_games", "https://cs.uwaterloo.ca/~watrous/Papers/GeneralTheoryQuantumGames.pdf"),
    ("gutoski_strategy_distance", "https://arxiv.org/pdf/1008.4636"),
    ("terhal_burkard_local_nonmarkov", "https://arxiv.org/pdf/quant-ph/0402104"),
    ("aharonov_kitaev_preskill_correlated", "https://preskill.caltech.edu/pubs/preskill-2006-long-range.pdf"),
    ("viola_knill_eulerian", "https://arxiv.org/pdf/quant-ph/0208056"),
    ("khodjasteh_viola_corrected_gates", "https://arxiv.org/pdf/0906.0525"),
]


def acquire(item):
    key, url = item
    entry = {"id": key, "requested_url": url, "retrieved_utc": datetime.now(timezone.utc).isoformat()}
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Astra-local-research-audit/1.0"})
        with urllib.request.urlopen(request, timeout=35) as response:
            data = response.read()
            entry["final_url"] = response.url
            entry["content_type"] = response.headers.get("Content-Type")
        if not data.startswith(b"%PDF"):
            raise ValueError("Response is not a PDF")
        path = OUT / (key + ".pdf")
        path.write_bytes(data)
        reader = PdfReader(path)
        text = "\n\n".join(f"[PDF PAGE {i+1}]\n{page.extract_text() or ''}" for i, page in enumerate(reader.pages))
        text_path = OUT / (key + ".txt")
        text_path.write_text(text, encoding="utf-8")
        entry.update(status="ACQUIRED", pdf_path=str(path.relative_to(ROOT)),
                     text_path=str(text_path.relative_to(ROOT)), bytes=len(data), pages=len(reader.pages),
                     sha256=hashlib.sha256(data).hexdigest(), text_sha256=hashlib.sha256(text.encode()).hexdigest())
    except Exception as error:
        entry.update(status="FAILED", error=f"{type(error).__name__}: {error}")
    return entry


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=7) as pool:
        entries = list(pool.map(acquire, SOURCES))
    (OUT / "acquisition_manifest.json").write_text(json.dumps(entries, indent=2) + "\n")
    print(json.dumps([{k: v for k, v in entry.items() if k in ("id", "status", "pages", "bytes", "error")} for entry in entries], indent=2))
