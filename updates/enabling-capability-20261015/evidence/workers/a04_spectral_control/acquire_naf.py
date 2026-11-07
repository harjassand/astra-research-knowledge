"""Reacquire the selected public source files, verifying deposit checksums.

Only downloads data. No deposited code is executed, no contact with authors.
The source metadata snapshot is pinned locally and immutable in this script.
"""
from pathlib import Path
import concurrent.futures
import datetime
import hashlib
import json
import time
import urllib.request

ROOT = Path(__file__).resolve().parent
WANTED = {"README.md", "Plot_FWM.py", "Make_Figures.py", "NaFFWMCrossed.zip",
          "NaFFWMBrightDark.zip", "Processed.zip", "Plot_Static.py", "NaFStatic.zip"}


def acquire(item):
    start = time.perf_counter()
    url = item["links"]["self"]
    data = urllib.request.urlopen(url, timeout=120).read()
    md5 = hashlib.md5(data).hexdigest()
    if item["checksum"] != "md5:" + md5 or len(data) != item["size"]:
        raise RuntimeError(f"Source verification failed for {item['key']}")
    path = ROOT / "data" / item["key"]
    path.write_bytes(data)
    return {"file": item["key"], "source": url, "bytes": len(data),
            "md5": md5, "checksum_matches": True,
            "sha256": hashlib.sha256(data).hexdigest(),
            "wall_seconds": time.perf_counter()-start}


if __name__ == "__main__":
    (ROOT / "data").mkdir(exist_ok=True)
    meta = json.loads((ROOT / "sources" / "zenodo_19443440_metadata.json").read_text())
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(acquire, [f for f in meta["files"] if f["key"] in WANTED]))
    out = {"acquired_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "source_record": meta["id"], "files": rows,
           "bytes_total": sum(f["bytes"] for f in rows),
           "wall_seconds_total": time.perf_counter()-start,
           "physical_experiment_performed": False,
           "model_inference_tokens": "UNAVAILABLE", "model_inference_cost": "UNAVAILABLE",
           "energy": "UNAVAILABLE"}
    # Preserve original acquisition receipt on replay.
    target = ROOT / "DATA_REACQUISITION_RECEIPT.json"
    target.write_text(json.dumps(out, indent=2)+"\n")
    print(f"Verified {len(rows)} source files, {out['bytes_total']} bytes.")
