"""Cache version-pinned primary text sources; no source trees are edited."""
import concurrent.futures
import hashlib
import json
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent
DEST = OUT / "primary"
DEST.mkdir(exist_ok=True)
SOURCES = [
    ("jain_nayak_1103.6067v2", "https://arxiv.org/html/1103.6067v2", "2012-01-12", "Theorem 1, fidelity convention and observational/relative entropy comparison"),
    ("beigi_1306.5920v6", "https://arxiv.org/html/1306.5920v6", "2013-11-22", "Equation 3 and Theorem 6 at alpha=2"),
    ("xie_fang_wang_duan_1705.06071v2", "https://arxiv.org/html/1705.06071v2", "2017-08-08", "Sections III.1/III.2, Lemma 3; IV.1 broadcasting interface"),
    ("seshadreesan_wilde_1410.1441v2", "https://arxiv.org/html/1410.1441v2", "2014-11-19", "Equation 6.17 and Proposition 28; squared fidelity convention"),
    ("piani_1608.02650v1", "https://arxiv.org/html/1608.02650v1", "2016-08-08", "Theorem 5, Section VI.1 and Eq 35"),
    ("piani_1501.06855v1", "https://arxiv.org/html/1501.06855v1", "2015-01-27", "Equation 4 and paragraph after Eq 9; Bose-extendible interface"),
    ("brandao_piani_horodecki_1310.8640v2", "https://arxiv.org/html/1310.8640v2", "2015-08-26", "Theorems 1/2 and Proposition 3; outcome objectivity hypotheses"),
    ("gao_wang_2609.20753v1", "https://arxiv.org/html/2609.20753v1", "2026-09-17", "Section 3.1: strong Lp regularity gate; not a proof premise"),
]


def fetch(row):
    name, url, date, scope = row
    req = urllib.request.Request(url, headers={"User-Agent": "Codex research source verification"})
    with urllib.request.urlopen(req, timeout=30) as response:
        data = response.read(8_000_001)
        assert len(data) <= 8_000_000
        final_url = response.url
    assert b"ltx_document" in data or b"<article" in data
    path = DEST / (name + ".html")
    path.write_bytes(data)
    return {
        "name": name, "url": url, "resolved_url": final_url,
        "version_date": date, "access_date": "2026-10-09",
        "scope_read": scope, "path": str(path.relative_to(OUT)),
        "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
        "status": "CACHED_PRIMARY_HTML",
    }


with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    records = list(pool.map(fetch, SOURCES))
(OUT / "PRIMARY_SOURCE_REGISTRY.json").write_text(json.dumps(records, indent=2) + "\n")
print(json.dumps([{k: x[k] for k in ("name", "sha256", "bytes", "status")} for x in records], indent=2))
