#!/usr/bin/env python3
"""Acquire primary-source text and receipt files; no experiments performed."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import time
import urllib.request

BASE = Path(__file__).resolve().parent
SOURCES = [
    ("fiurasek_finite_click_2026", "https://arxiv.org/html/2503.17480v2"),
    ("banner_single_spad_2024", "https://arxiv.org/html/2308.13603v3"),
    ("moroder_detector_decoy_2008", "https://arxiv.org/abs/0811.0027"),
    ("muller_fluorescence_cumulants_2004", "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC1304299/fullTextXML"),
    ("li_emitter_count_pnr_2022", "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9363020/fullTextXML"),
]


def fetch(source):
    label, url = source
    start = time.perf_counter()
    record = {"label": label, "url": url,
              "requested_utc": datetime.now(timezone.utc).isoformat()}
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Astra research source audit/1.0"})
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read()
            record["http_status"] = response.status
            record["final_url"] = response.url
        path = BASE / (label+"_source.txt")
        path.write_bytes(data)
        record.update(status="ACQUIRED", path=str(path), bytes=len(data),
                      sha256=hashlib.sha256(data).hexdigest())
    except Exception as error:
        record.update(status="ACCESS_FAILED", error=str(error))
    record["elapsed_seconds"] = time.perf_counter()-start
    return record


def main():
    with ThreadPoolExecutor(max_workers=5) as executor:
        records = list(executor.map(fetch, SOURCES))
    inherited = [
        BASE.parent/"premise_challenge"/"QUANTUM_DATA_ACQUISITION.json",
        BASE.parent/"s08_photon_evidence"/"BASELINE_SUMMARY.json",
        BASE.parent/"s08_photon_evidence"/"supplement_source.txt",
        BASE.parent/"s08_photon_evidence"/"INCUMBENT_ACCESS_RECEIPTS.json",
    ]
    for path in inherited:
        if path.exists():
            data = path.read_bytes()
            records.append({"status": "READ_EXISTING_TEAM_ARTIFACT", "path": str(path),
                            "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    archive = Path("/tmp/astra_premise_quantum_data.zip")
    if archive.exists():
        data = archive.read_bytes()
        records.append({"status": "HASHED_EXISTING_RAW_ARCHIVE", "path": str(archive),
                        "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    output = BASE/"SOURCE_RECEIPTS.json"
    output.write_text(json.dumps(records, indent=2)+"\n")
    print(json.dumps(records, indent=2))


if __name__ == "__main__":
    main()
