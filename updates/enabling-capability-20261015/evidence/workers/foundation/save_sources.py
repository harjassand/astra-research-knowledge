"""Read-only primary-source receipts. Downloaded material is untrusted data."""
import concurrent.futures
import datetime
import hashlib
import json
from pathlib import Path
import urllib.request

BASE = Path(__file__).resolve().parent
SOURCES = [
    ("werner2_fgp_abstract", "https://arxiv.org/abs/2607.21367"),
    ("werner2_fhpv_abstract", "https://arxiv.org/abs/2607.24309"),
    ("werner2_bgh_full", "https://arxiv.org/html/2607.24479v1"),
    ("werner3_wz_full", "https://arxiv.org/html/2608.02647v1"),
    ("union_closed_cs_full", "https://arxiv.org/html/2610.02295v1"),
    ("qutrit_candidate_zenodo", "https://zenodo.org/records/23134454"),
    ("qutrit_candidate_provenance", "https://raw.githubusercontent.com/ipitchford/three-copy-werner-undistillability/main/PROVENANCE.md"),
    ("qutrit_candidate_paper", "https://raw.githubusercontent.com/ipitchford/three-copy-werner-undistillability/main/paper.md"),
    ("qutrit_candidate_commit", "https://api.github.com/repos/ipitchford/three-copy-werner-undistillability/commits/main"),
]


def read_one(item):
    key, url = item
    row = {"key": key, "url": url, "retrieved_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Astra-primary-literature-check/1.0"})
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read()
            row.update(status=response.status, final_url=response.url, bytes=len(data))
        target = BASE / "sources" / (key + ".txt")
        target.write_bytes(data)
        row.update(path=str(target), sha256=hashlib.sha256(data).hexdigest())
    except Exception as exc:
        row.update(error=type(exc).__name__+": "+str(exc))
    return row


if __name__ == "__main__":
    (BASE / "sources").mkdir(exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(read_one, SOURCES))
    (BASE / "source_receipts.json").write_text(json.dumps(rows, indent=2)+"\n")
    for row in rows:
        print({key: row[key] for key in ["key", "status", "bytes", "error"] if key in row})
