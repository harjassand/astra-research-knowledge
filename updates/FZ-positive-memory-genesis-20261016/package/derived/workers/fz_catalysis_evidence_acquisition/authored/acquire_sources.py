#!/usr/bin/env python3
"""Acquire public original files, preserving every response and an integrity receipt.

External files are analysis inputs and must not enter the authored publication pack.
No bypass of access controls or authenticated requests is attempted.
"""
import concurrent.futures
import datetime
import hashlib
import json
from pathlib import Path
import urllib.error
import urllib.request
import argparse

ROOT = Path(__file__).resolve().parents[1]
EXTERNAL = ROOT / "external_excluded_from_publication"
RECEIPTS = ROOT / "receipts"
BASE = "https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41557-026-02107-8/MediaObjects/"
SOURCES = {
    "final_SI.pdf": BASE + "41557_2026_2107_MOESM1_ESM.pdf",
    "final_Fig2_MOESM20.xlsx": BASE + "41557_2026_2107_MOESM20_ESM.xlsx",
    "final_Fig6_MOESM24.xlsx": BASE + "41557_2026_2107_MOESM24_ESM.xlsx",
    "preprint_v1.pdf": "https://assets-eu.researchsquare.com/files/rs-6845872/v1_covered_135a4fac-50b0-4a57-ac68-a1f9dadbd716.pdf",
    "nature_landing.html": "https://www.nature.com/articles/s41557-026-02107-8",
    "UC_repository_landing.html": "https://escholarship.org/uc/item/78g8x2hb",
}
EXTRA = {
    "final_SIFig1_MOESM2.xlsx": BASE + "41557_2026_2107_MOESM2_ESM.xlsx",
    "final_SIFig2_MOESM3.xlsx": BASE + "41557_2026_2107_MOESM3_ESM.xlsx",
    "final_SIFig3_MOESM4.xlsx": BASE + "41557_2026_2107_MOESM4_ESM.xlsx",
    "final_SIFig7_MOESM8.xlsx": BASE + "41557_2026_2107_MOESM8_ESM.xlsx",
    "final_SIFig8_MOESM9.xlsx": BASE + "41557_2026_2107_MOESM9_ESM.xlsx",
    "final_SIFig11_MOESM12.xlsx": BASE + "41557_2026_2107_MOESM12_ESM.xlsx",
}
ALTERNATES = {
    "preprint_v1_assets.pdf": "https://assets.researchsquare.com/files/rs-6845872/v1_covered_135a4fac-50b0-4a57-ac68-a1f9dadbd716.pdf",
    "preprint_v1_landing.html": "https://www.researchsquare.com/article/rs-6845872/v1",
    "UC_repository_final.pdf": "https://escholarship.org/content/qt78g8x2hb/qt78g8x2hb.pdf",
    "nature_article.pdf": "https://www.nature.com/articles/s41557-026-02107-8.pdf",
}
RESOLVED_PREPRINT = {
    # These URLs were found in the live Research Square v1 landing-page metadata.
    # The search-indexed covered-PDF UUID had returned 403; it is not reused.
    "preprint_v1_live.pdf": "https://assets-eu.researchsquare.com/files/rs-6845872/v1_covered_42a30b57-29b4-4fc7-836c-583fd842d734.pdf",
    "preprint_v1_supplementary.docx": "https://assets-eu.researchsquare.com/files/rs-6845872/v1/102d6f79b9f266fb56927a68.docx",
}
CONTEXT = {
    "final_Fig6_caption.html": "https://www.nature.com/articles/s41557-026-02107-8/figures/6",
    "final_Fig2_caption.html": "https://www.nature.com/articles/s41557-026-02107-8/figures/2",
    "final_Fig3_MOESM21.xlsx": BASE + "41557_2026_2107_MOESM21_ESM.xlsx",
    "final_Fig6_publisher.png": "https://media.springernature.com/lw1200/springer-static/image/art%3A10.1038%2Fs41557-026-02107-8/MediaObjects/41557_2026_2107_Fig6_HTML.png",
}
COMPARATORS = {
    "Pd2_author_correction.html": "https://www.nature.com/articles/s41467-026-76860-2",
    "Chem2026_landing.html": "https://www.sciencedirect.com/science/article/pii/S2451929426001294",
    "Chem2026_cell_landing.html": "https://www.cell.com/chem/fulltext/S2451-9294(26)00129-4",
    # Candidate canonical CDN supplement routes, not yet source-identified titles.
    "Chem2026_candidate_mmc1.pdf": "https://ars.els-cdn.com/content/image/1-s2.0-S2451929426001294-mmc1.pdf",
    "Chem2026_candidate_mmc2.pdf": "https://ars.els-cdn.com/content/image/1-s2.0-S2451929426001294-mmc2.pdf",
    "Chem2026_candidate_mmc3.xlsx": "https://ars.els-cdn.com/content/image/1-s2.0-S2451929426001294-mmc3.xlsx",
}


def acquire(item):
    name, url = item
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    record = {"requested_url": url, "retrieved_at_utc": now, "name": name}
    request = urllib.request.Request(url, headers={"User-Agent": "Astra-evidence-acquisition/1.0 (public scientific source verification)"})
    try:
        response = urllib.request.urlopen(request, timeout=45)
    except urllib.error.HTTPError as exc:
        response = exc
    except Exception as exc:
        record.update(status="NETWORK_ERROR", error=repr(exc))
        return record
    try:
        payload = response.read()
        record.update(status_code=response.status, effective_url=response.geturl(), headers=dict(response.headers), bytes=len(payload), sha256=hashlib.sha256(payload).hexdigest(), magic_hex=payload[:16].hex())
        suffix_valid = (name.endswith(".pdf") and payload.startswith(b"%PDF")) or (name.endswith((".xlsx", ".docx")) and payload.startswith(b"PK")) or (name.endswith(".png") and payload.startswith(b"\x89PNG")) or name.endswith(".html")
        success = response.status == 200 and suffix_valid
        output = EXTERNAL / (name if success else name + ".failed_response")
        if output.exists() and output.read_bytes() != payload:
            # Preserve earlier acquired bytes if a live endpoint changes.
            output = output.with_name(output.stem + "_" + record["sha256"][:12] + output.suffix)
        output.write_bytes(payload)
        record.update(status="ACQUIRED" if success else "FAILED_OR_WRONG_CONTENT", relative_path=str(output.relative_to(ROOT)))
    except Exception as exc:
        record.update(status="READ_ERROR", error=repr(exc))
    finally:
        response.close()
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--group", choices=("primary", "extra", "alternates", "resolved_preprint", "context", "comparators"), default="primary")
    args = parser.parse_args()
    sources = {"primary": SOURCES, "extra": EXTRA, "alternates": ALTERNATES, "resolved_preprint": RESOLVED_PREPRINT, "context": CONTEXT, "comparators": COMPARATORS}[args.group]
    EXTERNAL.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(acquire, sources.items()))
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    (RECEIPTS / ("http_acquisition_" + args.group + "_" + stamp + ".json")).write_text(json.dumps(results, indent=2) + "\n")
    for row in results:
        print(json.dumps({k: row[k] for k in ("name", "status", "status_code", "bytes", "sha256", "error") if k in row}))


if __name__ == "__main__":
    main()
