#!/usr/bin/env python3
"""Save public primary-source responses; access failure is an explicit receipt.

These are publications and patents, not raw experiments acquired by this worker.
"""
import concurrent.futures
import datetime
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent
SOURCES = {
    "G17": "https://www.nature.com/articles/s41598-017-13562-2",
    "W22": "https://www.nature.com/articles/s41598-022-07479-8",
    "A21": "https://pubs.aip.org/aip/apm/article/9/9/091108/122923/Fabrication-of-L1-FeNi-films-with-island",
    "I20": "https://pubs.aip.org/aip/apl/article/116/24/242404/986293/Epitaxial-L1-FeNi-films-with-high-degree-of-order",
    "L24": "https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/advs.202302696",
    "H24": "https://www.osti.gov/servlets/purl/2283203",
    "P62": "https://jphysrad.journaldephysique.org/articles/jphysrad/abs/1962/10/jphysrad_1962__23_10_841_0/jphysrad_1962__23_10_841_0.html",
    "N64": "https://pubs.aip.org/jap/article/35/3/873/505184/Magnetic-Properties-of-an-Iron-Nickel-Single-Crystal",
    "ACS23": "https://pubs.acs.org/doi/10.1021/acsomega.2c07869",
    "FPd08": "https://www.jstage.jst.go.jp/article/matertrans/49/9/49_MAW200810/_pdf/-char/en",
    "LAO24": "https://www.sciencedirect.com/science/article/abs/pii/S0925838823042950",
}


class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.lines = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "noscript"}:
            self.skip += 1
        if tag in {"p", "h1", "h2", "h3", "h4", "li", "tr", "section", "div"}:
            self.lines.append("\n")

    def handle_endtag(self, tag):
        if tag in {"script", "style", "noscript"}:
            self.skip = max(0, self.skip - 1)
        if tag in {"p", "li", "tr"}:
            self.lines.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.lines.append(data)


def fetch(item):
    sid, url = item
    rec = {"id": sid, "requested_url": url,
           "retrieved_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=45) as response:
            data = response.read()
            rec.update(final_url=response.geturl(), status=response.status,
                       content_type=response.headers.get("Content-Type"), bytes=len(data),
                       sha256=hashlib.sha256(data).hexdigest())
        ext = ".pdf" if data.startswith(b"%PDF") else ".html"
        raw = ROOT / "sources" / (sid + ext)
        raw.write_bytes(data)
        rec["local_path"] = str(raw.relative_to(ROOT))
        if ext == ".html":
            parser = Text()
            parser.feed(data.decode("utf-8", errors="replace"))
            text = "\n".join(" ".join(line.split()) for line in "".join(parser.lines).splitlines() if line.strip())
            txt = raw.with_suffix(".txt")
            txt.write_text(text + "\n", encoding="utf-8")
            rec["text_path"] = str(txt.relative_to(ROOT))
    except Exception as exc:
        rec.update(status="ACCESS_FAILED", error=repr(exc))
    return rec


if __name__ == "__main__":
    (ROOT / "sources").mkdir(exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        receipts = list(pool.map(fetch, SOURCES.items()))
    (ROOT / "source_receipts.json").write_text(json.dumps(receipts, indent=2) + "\n")
    for receipt in receipts:
        print(json.dumps(receipt))
