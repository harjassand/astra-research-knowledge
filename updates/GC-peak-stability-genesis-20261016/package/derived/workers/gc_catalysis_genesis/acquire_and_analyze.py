"""Own read-only extraction and deterministic checks. No acquired code is executed."""
from __future__ import annotations
import concurrent.futures
import datetime
import hashlib
import json
import math
from pathlib import Path
from fractions import Fraction as Q
import urllib.request
import urllib.error
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
INPUT = ROOT.parents[1] / "originals/catalysis/final_Fig2.xlsx"
W = Path("/Users/harjas/Documents/ChatGPT/ultra/work/astra-positive-memory-20261016")
BASE = "https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41557-026-02107-8/MediaObjects/"
SOURCES = {
    "final_SI.pdf": BASE + "41557_2026_2107_MOESM1_ESM.pdf",
    "final_Fig2_fresh.xlsx": BASE + "41557_2026_2107_MOESM20_ESM.xlsx",
    "final_SIFig7.xlsx": BASE + "41557_2026_2107_MOESM8_ESM.xlsx",
    "nature_landing.html": "https://www.nature.com/articles/s41557-026-02107-8",
    "Lim2021_PMC.html": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8395646/",
}
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def read_xlsx(path):
    """Read XML values and formulas without importing or recalculating the workbook."""
    with zipfile.ZipFile(path) as z:
        strings = []
        if "xl/sharedStrings.xml" in z.namelist():
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
                strings.append("".join(si.itertext()))
        rel = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        targets = {x.attrib["Id"]: x.attrib["Target"] for x in rel}
        output = {}
        for sheet in ET.fromstring(z.read("xl/workbook.xml")).findall("m:sheets/m:sheet", NS):
            rid = sheet.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]
            target = targets[rid]
            target = target.lstrip("/") if target.startswith("/") else "xl/" + target
            cells, formulas = {}, {}
            for c in ET.fromstring(z.read(target)).findall(".//m:sheetData/m:row/m:c", NS):
                v = c.find("m:v", NS)
                if v is not None:
                    value = v.text
                    if c.attrib.get("t") == "s":
                        value = strings[int(value)]
                    cells[c.attrib["r"]] = value
                elif c.attrib.get("t") == "inlineStr":
                    cells[c.attrib["r"]] = "".join(c.find("m:is", NS).itertext())
                f = c.find("m:f", NS)
                if f is not None:
                    formulas[c.attrib["r"]] = f.text
            output[sheet.attrib["name"]] = {"cells": cells, "formulas": formulas}
    return output


def acquire(item):
    name, url = item
    result = {"name": name, "requested_url": url, "retrieved_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    request = urllib.request.Request(url, headers={"User-Agent": "Astra-scientific-source-audit/1.0"})
    try:
        response = urllib.request.urlopen(request, timeout=40)
    except urllib.error.HTTPError as exc:
        response = exc
    except Exception as exc:
        return result | {"status": "NETWORK_ERROR", "error": repr(exc)}
    with response:
        payload = response.read()
        valid = ((name.endswith(".pdf") and payload.startswith(b"%PDF")) or
                 (name.endswith(".xlsx") and payload.startswith(b"PK")) or
                 (name.endswith(".html") and b"<html" in payload.lower()))
        expected = ((name != "Lim2021_PMC.html" or b"Non-Faradaic Promotion of Ethylene Hydrogenation" in payload) and
                    (name != "nature_landing.html" or b"Time-dependent surface polarization" in payload))
        ok = response.status == 200 and valid and expected
        path = ROOT / "external_excluded_from_publication" / (name if ok else name + ".failed_response")
        path.parent.mkdir(parents=True, exist_ok=True)
        digest = hashlib.sha256(payload).hexdigest()
        if path.exists() and path.read_bytes() != payload:
            path = path.with_name(path.stem + "_" + digest[:12] + path.suffix)
        path.write_bytes(payload)
        return result | {"status": "ACQUIRED" if ok else "FAILED_OR_WRONG_CONTENT", "status_code": response.status,
                         "bytes": len(payload), "sha256": digest, "effective_url": response.geturl(),
                         "content_type": response.headers.get("content-type"), "path": str(path.relative_to(ROOT))}


def ethane(x, s):
    return x / 100 * (100 / s - 1)


def netethylene(x, s):
    return x / 100 * (2 - 100 / s)


def number(q):
    return {"exact": str(q), "decimal": float(q)}


def threshold_delta(group, vary):
    """Minimum common independent +/- percentage-point box for a nondecreasing fit.

    This is a deterministic sensitivity threshold, never a confidence interval.
    Exact rational bisection conservatively brackets the threshold.
    """
    def feasible(delta):
        running_lower = Q(0)
        for row in group:
            x, s = Q(row["X_percent"]), Q(row["S_percent"])
            dx = delta if "X" in vary else 0
            ds = delta if "S" in vary else 0
            xmin, xmax = max(0, x-dx), min(100, x+dx)
            smin, smax = max(Q(1, 10**12), s-ds), min(100, s+ds)
            lower, upper = ethane(xmin, smax), ethane(xmax, smin)
            running_lower = max(running_lower, lower)
            if running_lower > upper:
                return False
        return True
    lo, hi = Q(0), Q(100)
    for _ in range(65):
        mid = (lo+hi)/2
        if feasible(mid):
            hi = mid
        else:
            lo = mid
    return {"lower_pp": float(lo), "upper_pp": float(hi), "vary_independently": vary}


def analyze():
    workbook = read_xlsx(INPUT)
    (ROOT / "workbook_cells.json").write_text(json.dumps(workbook, indent=2)+"\n")
    c, d = workbook["Figure 2 c"]["cells"], workbook["Figure 2 d"]["cells"]
    groups = {}
    rows = []
    for row in range(2, 32):
        h, duration, x = [Q(c[f"{col}{row}"]) for col in "BCD"]
        hb, db, s = [Q(d[f"{col}{row}"]) for col in "BCD"]
        assert (h, duration) == (hb, db)
        rec = {"row": row, "h_s": str(h), "d_s": str(duration), "period_s": str(h+duration),
               "duty_h_over_d": str(h/duration), "X_percent": c[f"D{row}"], "S_percent": d[f"D{row}"],
               "ethane_per_Ain": number(ethane(x,s)), "netethylene_per_Ain": number(netethylene(x,s)),
               "cells": {"h": f"Figure 2 c!B{row}", "d": f"Figure 2 c!C{row}",
                         "X": f"Figure 2 c!D{row}", "S": f"Figure 2 d!D{row}"}}
        groups.setdefault(str(h/duration), []).append(rec)
        rows.append(rec)
    summaries = {}
    for duty, group in groups.items():
        group.sort(key=lambda item: Q(item["period_s"]))
        if len(group) < 2:
            continue
        values = [Q(x["ethane_per_Ain"]["exact"]) for x in group]
        drop = max(values[i]-values[j] for i in range(len(values)) for j in range(i+1,len(values)))
        relative = max((values[i]-values[j])/(values[i]+values[j]) for i in range(len(values)) for j in range(i+1,len(values)))
        summaries[duty] = {"rows": [g["row"] for g in group], "values": [float(v) for v in values],
                           "strictly_decreasing": all(values[i]>values[i+1] for i in range(len(values)-1)),
                           "max_earlier_minus_later": number(drop), "minimum_symmetric_b_absolute_error": number(max(0,drop/2)),
                           "minimum_symmetric_b_relative_error": number(max(0,relative)),
                           "min_X_and_S_pp_box": threshold_delta(group,"XS"),
                           "min_X_only_pp_box": threshold_delta(group,"X"),
                           "min_S_only_pp_box": threshold_delta(group,"S")}
    b = workbook["Figure 2 b"]["cells"]
    static = []
    for r in range(2,12):
        static.append({"row":r,"label":b.get(f"B{r}"),"X_percent":b.get(f"C{r}"),"S_percent":b.get(f"D{r}"),
                       "b_per_Ain": number(ethane(Q(b[f"C{r}"]),Q(b[f"D{r}"])))})
    output = {"input_path": str(INPUT), "input_sha256":hashlib.sha256(INPUT.read_bytes()).hexdigest(),
              "grid_rows":rows,"equal_duty_groups": summaries,"static_dynamic_sheet":static,
              "scope":"Exact stored decimal values; no replicate identities or uncertainty bounds acquired for grid. Bounds below are sensitivity requirements, not measured error bars.",
              "formula_count":sum(len(x["formulas"]) for x in workbook.values())}
    (ROOT / "workbook_checks.json").write_text(json.dumps(output,indent=2)+"\n")
    return output


def extract_sources(receipts):
    from pypdf import PdfReader
    from html.parser import HTMLParser
    class Text(HTMLParser):
        def __init__(self):
            super().__init__(); self.fragments=[]; self.skip=0
        def handle_starttag(self,tag,attrs):
            if tag in {"script","style"}: self.skip+=1
            if tag in {"p","h1","h2","h3","h4","li","tr","section"}: self.fragments.append("\n")
        def handle_endtag(self,tag):
            if tag in {"script","style"}: self.skip=max(0,self.skip-1)
        def handle_data(self,data):
            if not self.skip: self.fragments.append(data)
    for r in receipts:
        if r["status"] != "ACQUIRED": continue
        path=ROOT/r["path"]
        if path.suffix==".pdf":
            pages=PdfReader(path).pages
            text="\n\n".join(f"=== PDF PAGE {i+1} ===\n"+p.extract_text() for i,p in enumerate(pages))
            path.with_suffix(".txt").write_text(text)
        elif path.suffix==".html":
            parser=Text(); parser.feed(path.read_text(errors="replace"))
            path.with_suffix(".txt").write_text("".join(parser.fragments))
        elif r["name"]=="final_SIFig7.xlsx":
            data=read_xlsx(path)
            (ROOT/"SIFig7_structure.json").write_text(json.dumps({k:{"count":len(v["cells"]),"first_cells":dict(list(v["cells"].items())[:30]),"last_cells":dict(list(v["cells"].items())[-12:])} for k,v in data.items()},indent=2)+"\n")


if __name__=="__main__":
    ROOT.mkdir(parents=True,exist_ok=True)
    output=analyze()
    print(json.dumps({"input_sha256":output["input_sha256"],"groups":output["equal_duty_groups"],"static":output["static_dynamic_sheet"]},indent=2))
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        receipts=list(pool.map(acquire,SOURCES.items()))
    (ROOT/"source_acquisition.json").write_text(json.dumps(receipts,indent=2)+"\n")
    print(json.dumps(receipts,indent=2))
    extract_sources(receipts)
