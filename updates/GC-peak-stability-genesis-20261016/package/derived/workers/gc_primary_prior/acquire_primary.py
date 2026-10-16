"""Read-only primary acquisition; never execute acquired programs."""
from pathlib import Path
import datetime, hashlib, json, urllib.request, urllib.error

BASE = Path(__file__).resolve().parent
OUT = BASE / "acquired_excluded_from_publication"
OUT.mkdir(exist_ok=True)
SOURCES = [
    ("obizhaeva_wang_2013.pdf", "https://web.mit.edu/wangj/www/pap/ObizhaevaWang13.pdf"),
    ("harris_kirchheim_lin_v2.pdf", "https://arxiv.org/pdf/1708.07849v2"),
    ("jahnke_reduced_2011.pdf", "https://www.math.kit.edu/iwrmm/seite/preprints/media/preprint%20nr.%2011-2.pdf"),
    ("openai_math_main.json", "https://api.github.com/repos/openai/math/commits/main"),
    ("openai_math_contents.md", "https://raw.githubusercontent.com/openai/math/1581d4cbdd69a0faf34b2089614fe2a814316a6a/CONTENTS.md"),
    ("openai_math_readme.md", "https://raw.githubusercontent.com/openai/math/1581d4cbdd69a0faf34b2089614fe2a814316a6a/README.md"),
    ("pr95_metadata.json", "https://api.github.com/repos/harjassand/astra-research-knowledge/pulls/95"),
]
receipts = []
for name, url in SOURCES:
    receipt = {"file": str(OUT / name), "url": url, "acquired_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Astra-primary-proof-read-only/1.0"})
        with urllib.request.urlopen(request, timeout=45) as response:
            payload = response.read()
            receipt.update(status=response.status, final_url=response.url, content_type=response.headers.get("Content-Type"))
        (OUT / name).write_bytes(payload)
        receipt.update(bytes=len(payload), sha256=hashlib.sha256(payload).hexdigest(), valid_pdf_magic=payload.startswith(b"%PDF") if name.endswith(".pdf") else None)
    except Exception as exc:
        receipt.update(error=repr(exc))
    receipts.append(receipt)
    print(json.dumps(receipt))
(BASE / "receipts" / "ACQUISITION_INITIAL.json").write_text(json.dumps(receipts, indent=2) + "\n")
