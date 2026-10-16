#!/usr/bin/env python3
"""Acquire only named public primary endpoints; never solve access challenges."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json

HERE = Path(__file__).resolve().parent
TARGETS = [
    ("ht_v2.pdf", "https://arxiv.org/pdf/2212.08437v2"),
    ("ht_v2.html", "https://arxiv.org/html/2212.08437v2"),
    ("lss_publisher_response.bin", "https://projecteuclid.org/journals/annals-of-probability/volume-25/issue-1/Domination-by-product-measures/10.1214/aop/1024404279.pdf"),
    ("lss_author_response.bin", "https://www.math.ucla.edu/~rhs/papers/lss.dvi"),
    ("lss_jstor_response.bin", "https://www.jstor.org/stable/pdf/2959530.pdf"),
]

def fetch(item):
    name, url = item
    rec = {"url": url, "retrieved_at_utc": datetime.now(timezone.utc).isoformat()}
    try:
        req = Request(url, headers={"User-Agent": "Astra mathematical source verification"})
        with urlopen(req, timeout=20) as response:
            data = response.read()
            rec.update(final_url=response.url, status=response.status,
                       content_type=response.headers.get("Content-Type", ""),
                       byte_count=len(data), sha256=sha256(data).hexdigest())
        rec["is_pdf"] = data.startswith(b"%PDF-")
        rec["is_access_challenge"] = any(token in data.lower() for token in
            [b"hcaptcha", b"captcha", b"security challenge", b"just a moment",
             b"incapsula", b"client challenge"])
        if not name.startswith("lss_") or rec["is_pdf"]:
            (HERE / "primary" / name).write_bytes(data)
            rec["saved_file"] = "primary/" + name
        else:
            rec["body_not_retained"] = "Access response, not theorem pages; raw challenge identifiers omitted."
    except Exception as exc:
        rec.update(error=repr(exc), is_pdf=False)
    return rec

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=5) as executor:
        receipts = list(executor.map(fetch, TARGETS))
    (HERE / "primary" / "RETRIEVAL_RECEIPTS.json").write_text(json.dumps(receipts, indent=2) + "\n")
    print(json.dumps([{k: rec[k] for k in ("url", "status", "is_pdf", "is_access_challenge", "byte_count", "error") if k in rec} for rec in receipts], indent=2))
