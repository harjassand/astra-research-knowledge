#!/usr/bin/env python3
"""Cache exactly the five primary versions already read; no search or proofs."""
from pathlib import Path
import hashlib, json, urllib.request
ROOT = Path(__file__).resolve().parent
PRIMARY = ROOT / "primary"
SOURCES = [
    dict(id="SFR2015", url="https://arxiv.org/html/1504.07251v2",
         version="1504.07251v2", version_date="2015-06-09",
         filename="1504.07251v2.html",
         read_scope="Theorem 2.1 Eq7, Remark2.3; selected Section4 tightness/completion passages. Primary theorem imported; complete proof not independently reconstructed.",
         web_line_spans=["76-90", "346-515 selected"]),
    dict(id="SHIROKOV2015", url="https://arxiv.org/html/1506.06377v2",
         version="1506.06377v2", version_date="2015-08-13",
         filename="1506.06377v2.html",
         read_scope="Natural-log preliminaries; Section6.1 Eq36/S1/C3 and Theorem2 Eq40-41; Section8.4 qualification. Extended-CMI interface, not whole-proof reconstruction.",
         web_line_spans=["118 footnote", "511-561", "Section8.4"]),
    dict(id="HAYASHI_ZHAO2026", url="https://arxiv.org/html/2601.09995v1",
         version="2601.09995v1", version_date="2026-01-15",
         filename="2601.09995v1.html",
         read_scope="Abstract, Theorem1 and its proof, selected conclusion; finite exact double-Markov common-label classification. Not an approximate theorem and not independently validated as a new proof.",
         web_line_spans=["124-187"]),
    dict(id="HJPW2003", url="https://arxiv.org/html/quant-ph/0304007v2",
         version="quant-ph/0304007v2", version_date="2003-08-22",
         filename="quant-ph-0304007v2.html",
         read_scope="Theorem6 finite-dimensional equality decomposition and stated finite scope/base2 convention; equality theorem imported.",
         web_line_spans=["245-254"]),
    dict(id="CSW2011", url="https://arxiv.org/html/0910.4151v3",
         version="0910.4151v3", version_date="2011-01-21",
         filename="0910.4151v3.html",
         read_scope="SectionIII Lemma6 proof: uniform wedge extension, one-sided CMI ratio and k=d/2+1 choice; construction known prior art.",
         web_line_spans=["180-195"]),
]
PRIMARY.mkdir(exist_ok=True)
for src in SOURCES:
    path = PRIMARY / src["filename"]
    try:
        request = urllib.request.Request(src["url"],
                    headers={"User-Agent":"Codex research source cache"})
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read()
            src["resolved_url"] = response.geturl()
        if not data or b"<html" not in data.lower()[:5000]:
            raise ValueError("Expected nonempty primary HTML")
        path.write_bytes(data)
        src.update(cache_status="CACHED", cache_path=str(path.relative_to(ROOT)),
                   bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    except Exception as exc:
        src.update(cache_status="FAILED", error=str(exc))
registry = {
    "schema":1, "date":"2026-10-09",
    "source_boundary":"Exact primary versions actually read live. HTML web-line spans are reader coordinates, not immutable cached-file line numbers. Cache integrity is not theorem validation.",
    "sources":SOURCES,
    "reviewer_only_import": {
        "version":"1509.07127v3",
        "url":"https://arxiv.org/html/1509.07127v3",
        "scope":"JRSSWW Theorem2.1/Remark2.2/2.4 checked by authorized reviewer; primary not opened by this origin worker.",
        "status":"IMPORTED_VIA_AUTHORIZED_REVIEW"
    }
}
(ROOT/"PRIMARY_SOURCE_REGISTRY.json").write_text(
    json.dumps(registry,indent=2)+"\n", encoding="utf-8")
print(json.dumps({"cached":sum(s["cache_status"]=="CACHED" for s in SOURCES),
                  "failed":sum(s["cache_status"]=="FAILED" for s in SOURCES)}))

