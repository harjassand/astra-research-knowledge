#!/usr/bin/env python3
"""Reproduce the released ED8i 53BP1 3x2 category contrast.

Uses only Python's standard library and the preserved publisher workbook at
`data/panagopoulos_2025_source_data.xlsx`. This is a test of the aggregate
released table only; rows are treated as independent for Pearson's statistic.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
WORKBOOK = HERE / "data" / "panagopoulos_2025_source_data.xlsx"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"


def read_ed8i_53bp1(path: Path) -> list[list[int]]:
    with ZipFile(path) as book:
        workbook = ET.fromstring(book.read("xl/workbook.xml"))
        rels = ET.fromstring(book.read("xl/_rels/workbook.xml.rels"))
        targets = {r.attrib["Id"]: r.attrib["Target"] for r in rels.findall(f"{{{PKG_REL_NS}}}Relationship")}
        sheet_path = None
        for sheet in workbook.find("m:sheets", NS):
            if sheet.attrib["name"] == "ED8i":
                rid = sheet.attrib[f"{{{REL_NS}}}id"]
                target = targets[rid]
                sheet_path = target if target.startswith("xl/") else f"xl/{target}"
                break
        if sheet_path is None:
            raise ValueError("ED8i worksheet is absent")

        shared = ET.fromstring(book.read("xl/sharedStrings.xml"))
        strings = ["".join(item.itertext()) for item in shared]
        ws = ET.fromstring(book.read(sheet_path))
        cells: dict[str, str] = {}
        for cell in ws.findall(".//m:c", NS):
            value = cell.find("m:v", NS)
            if value is None:
                cells[cell.attrib["r"]] = ""
            elif cell.attrib.get("t") == "s":
                cells[cell.attrib["r"]] = strings[int(value.text)]
            else:
                cells[cell.attrib["r"]] = value.text or ""

    if [cells.get(f"A{r}") for r in range(3, 6)] != ["High", "Medium", "Low"]:
        raise ValueError("ED8i rows do not match expected High/Medium/Low categories")
    # Columns B/C are the 53BP1 UT/4-Gy counts, rows 3–5 are High/Medium/Low.
    return [[int(cells[f"{col}{row}"]) for col in ("B", "C")] for row in range(3, 6)]


def pearson_3x2(table: list[list[int]]) -> tuple[float, float, float, int]:
    row_totals = [sum(row) for row in table]
    col_totals = [sum(table[r][c] for r in range(3)) for c in range(2)]
    total = sum(row_totals)
    statistic = 0.0
    for r in range(3):
        for c in range(2):
            expected = row_totals[r] * col_totals[c] / total
            statistic += (table[r][c] - expected) ** 2 / expected
    # For df=2, chi-square survival function is exp(-x/2).
    p_value = math.exp(-statistic / 2)
    cramers_v = math.sqrt(statistic / total)
    return statistic, p_value, cramers_v, total


def main() -> None:
    table = read_ed8i_53bp1(WORKBOOK)
    expected = [[1, 7], [9, 28], [22, 19]]
    if table != expected:
        raise AssertionError(f"released counts changed: {table!r}")
    statistic, p_value, v, total = pearson_3x2(table)
    result = {
        "source_sheet": "ED8i",
        "category_order": ["High", "Medium", "Low"],
        "condition_order": ["UT", "4 Gy"],
        "counts": table,
        "pearson_chi_square": statistic,
        "degrees_of_freedom": 2,
        "N": total,
        "p_value_df2": p_value,
        "cramers_v": v,
        "scope_limit": "aggregate released categories only; no pair IDs, continuous measurements, event times, or replicate labels",
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
