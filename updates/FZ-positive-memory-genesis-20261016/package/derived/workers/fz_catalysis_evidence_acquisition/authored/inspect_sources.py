#!/usr/bin/env python3
"""Read-only extraction; originals are never modified. Full extracts stay external."""
import json
import re
from pathlib import Path
import openpyxl
from pypdf import PdfReader
from html.parser import HTMLParser


class TextLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.links = []
        self.active = None
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        if tag == "a":
            self.active = {"href": dict(attrs).get("href"), "text": ""}

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1
        if tag == "a" and self.active:
            self.links.append(self.active)
            self.active = None

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.text.append(data.strip())
            if self.active:
                self.active["text"] += data.strip() + " "

ROOT = Path(__file__).resolve().parents[1]
EXT = ROOT / "external_excluded_from_publication"
OUT = EXT / "extracted"
OUT.mkdir(exist_ok=True)

for path in EXT.glob("*.xlsx"):
    wb = openpyxl.load_workbook(path, data_only=False, read_only=True)
    all_sheets = {}
    print("WORKBOOK", path.name, str(wb.properties))
    for ws in wb.worksheets:
        rows = []
        texts = []
        nonempty = 0
        formulas = 0
        for row in ws:
            vals = []
            for c in row:
                if c.value is not None:
                    nonempty += 1
                    vals.append([c.coordinate, c.value])
                    if c.data_type == "f":
                        formulas += 1
                    if isinstance(c.value, str):
                        texts.append([c.coordinate, c.value])
            if vals:
                rows.append(vals)
        all_sheets[ws.title] = rows
        print(json.dumps({"sheet": ws.title, "dimensions": ws.calculate_dimension(), "populated_cells": nonempty, "formulas": formulas, "text_cells": texts[:150], "first_rows": rows[:8], "last_rows": rows[-3:]}, ensure_ascii=False, default=str))
    (OUT / (path.stem + "_cells.json")).write_text(json.dumps(all_sheets, ensure_ascii=False, indent=2, default=str) + "\n")
    wb.close()

for path in EXT.glob("*.pdf"):
    pdf = PdfReader(path)
    texts = [p.extract_text(extraction_mode="layout") for p in pdf.pages]
    (OUT / (path.stem + ".txt")).write_text("\n\n".join("=== PAGE " + str(i + 1) + " ===\n" + text for i, text in enumerate(texts)) + "\n")
    print("PDF", path.name, "pages", len(texts), "metadata", pdf.metadata)

for path in EXT.glob("*.html"):
    parsed = TextLinks()
    parsed.feed(path.read_text())
    text = "\n".join(parsed.text)
    (OUT / (path.stem + ".txt")).write_text(text + "\n")
    if "nature" in path.name:
        links = [a for a in parsed.links if re.search("MOESM|pdf|figshare|Supplementary|Source Data", str(a))]
        (OUT / "nature_source_links.json").write_text(json.dumps(links, indent=2) + "\n")
        print("NATURE LINKS", json.dumps(links, ensure_ascii=False))
