#!/usr/bin/env python3
"""Recompute scoped source-data checks for the Ji et al. 2026 battery paper.

Uses only the Python standard library and the publisher-provided XLSX files
stored in ../sources. It does not establish that the phase-field model matches
real cells; it checks unit conversions, source-data transforms, and the stated
conditional Sand-column bound.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources"
RESULTS = ROOT / "results" / "source_audit.json"
FARADAY = 96485.33212  # C mol^-1

NS = {
    "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "p": "http://schemas.openxmlformats.org/package/2006/relationships",
}


def _col_index(cell_ref: str) -> int:
    letters = re.match(r"[A-Z]+", cell_ref).group(0)
    out = 0
    for ch in letters:
        out = out * 26 + ord(ch) - ord("A") + 1
    return out - 1


def read_xlsx_sheet(path: Path, requested: str) -> list[list[object]]:
    """Read a basic numeric/string worksheet without third-party packages."""
    with zipfile.ZipFile(path) as zf:
        workbook = ET.fromstring(zf.read("xl/workbook.xml"))
        relroot = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
        rels = {rel.attrib["Id"]: rel.attrib["Target"]
                for rel in relroot.findall("p:Relationship", NS)}
        sheets = workbook.find("m:sheets", NS)
        target = None
        for sheet in sheets.findall("m:sheet", NS):
            if sheet.attrib["name"] == requested:
                target = rels[sheet.attrib["{" + NS["r"] + "}id"]]
                break
        if target is None:
            raise KeyError(f"No sheet {requested!r} in {path.name}")
        target = target.lstrip("/")
        if not target.startswith("xl/"):
            target = "xl/" + target
        shared: list[str] = []
        if "xl/sharedStrings.xml" in zf.namelist():
            ss = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            for si in ss.findall("m:si", NS):
                shared.append("".join(t.text or "" for t in si.findall(".//m:t", NS)))
        root = ET.fromstring(zf.read(target))
        rows: list[list[object]] = []
        for row in root.findall(".//m:sheetData/m:row", NS):
            cells: dict[int, object] = {}
            for cell in row.findall("m:c", NS):
                idx = _col_index(cell.attrib["r"])
                typ = cell.attrib.get("t")
                v = cell.find("m:v", NS)
                if typ == "inlineStr":
                    value = "".join(t.text or "" for t in cell.findall(".//m:t", NS))
                elif v is None or v.text is None:
                    value = None
                elif typ == "s":
                    value = shared[int(v.text)]
                elif typ in ("str", "e"):
                    value = v.text
                else:
                    try:
                        value = float(v.text)
                    except ValueError:
                        value = v.text
                cells[idx] = value
            width = max(cells, default=-1) + 1
            values: list[object] = [None] * width
            for idx, value in cells.items():
                values[idx] = value
            rows.append(values)
        return rows


def ols(xs: list[float], ys: list[float]) -> dict[str, float]:
    n = len(xs)
    xm, ym = sum(xs) / n, sum(ys) / n
    sxx = sum((x - xm) ** 2 for x in xs)
    sxy = sum((x - xm) * (y - ym) for x, y in zip(xs, ys))
    slope = sxy / sxx
    intercept = ym - slope * xm
    sst = sum((y - ym) ** 2 for y in ys)
    sse = sum((y - (intercept + slope * x)) ** 2 for x, y in zip(xs, ys))
    slope0 = sum(x * y for x, y in zip(xs, ys)) / sum(x * x for x in xs)
    sse0 = sum((y - slope0 * x) ** 2 for x, y in zip(xs, ys))
    return {
        "n": n,
        "slope_per_mA_cm2": slope,
        "intercept_s_minus_half": intercept,
        "r_squared_with_intercept": 1.0 - sse / sst,
        "slope_through_origin_per_mA_cm2": slope0,
        "r_squared_origin_fit_vs_mean": 1.0 - sse0 / sst,
        "vsc_from_free_slope_SI_A2_s_m4": 1.0 / (slope / 10.0) ** 2,
        "vsc_from_origin_slope_SI_A2_s_m4": 1.0 / (slope0 / 10.0) ** 2,
    }


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def nearest(points: list[tuple[float, float]], target: float) -> tuple[float, float]:
    return min(points, key=lambda point: abs(point[0] - target))


def main() -> int:
    f2 = read_xlsx_sheet(SOURCES / "ji2026_source_data_fig2.xlsx", "Fig2f")
    # Row 1 is group headings; row 2 contains the variable labels.
    raw_lmgl = [(float(r[0]), float(r[1])) for r in f2[2:]
                if len(r) > 1 and isinstance(r[0], (int, float))
                and isinstance(r[1], (int, float)) and r[1] > 0]
    raw_limg = [(float(r[2]), float(r[3])) for r in f2[2:]
                if len(r) > 3 and isinstance(r[2], (int, float))
                and isinstance(r[3], (int, float)) and r[3] > 0]
    fits = {}
    for name, data in (("LiMgLa", raw_lmgl), ("LiMg", raw_limg)):
        xs = [j for j, _ in data]
        ys = [1.0 / math.sqrt(hours * 3600.0) for _, hours in data]
        fit = ols(xs, ys)
        fit["raw_j_time_mA_cm2_h"] = [[j, t] for j, t in data]
        fits[name] = fit

    # Publisher source-data columns E:F and G:H duplicate t^(-1/2) in SI seconds.
    transform_errors = {"LiMgLa": [], "LiMg": []}
    for row in f2[2:]:
        if len(row) >= 8 and isinstance(row[0], (int, float)) and isinstance(row[1], (int, float)):
            transform_errors["LiMgLa"].append(abs(1 / math.sqrt(row[1] * 3600) - row[5]))
        if len(row) >= 8 and isinstance(row[2], (int, float)) and isinstance(row[3], (int, float)):
            transform_errors["LiMg"].append(abs(1 / math.sqrt(row[3] * 3600) - row[7]))

    # Independent dimensional reconstruction of Supplementary Table 3.
    table3 = {
        "LiMetal": {"D_cm2_s": 5.6e-11, "c0_mol_m3": 7.64e4, "reported_VSC": 2.39e5},
        "LiMg": {"D_cm2_s": 3.4e-11, "c0_mol_m3": 7.45e4, "reported_VSC": 1.42e5},
        "LiMgLa": {"D_cm2_s": 3.5e-10, "c0_mol_m3": 7.45e4, "reported_VSC": 1.46e6},
    }
    for row in table3.values():
        row["computed_VSC_SI"] = (math.pi * row["D_cm2_s"] * 1e-4
                                  * row["c0_mol_m3"] ** 2 * FARADAY ** 2 / 4.0)
        row["reported_over_computed"] = row["reported_VSC"] / row["computed_VSC_SI"]

    f4 = read_xlsx_sheet(SOURCES / "ji2026_source_data_fig4.xlsx", "Fig4f")
    current_points = [(float(r[2]), float(r[3])) for r in f4[2:]
                      if len(r) > 3 and isinstance(r[2], (int, float))
                      and isinstance(r[3], (int, float))]
    model_amp = {}
    for target in (1.10, 1.50, 1.94, 2.10):
        cap, eff_current = nearest(current_points, target)
        kappa = eff_current / 1.0  # source case is imposed 1.0 mA cm^-2
        model_amp[str(target)] = {
            "nearest_capacity_mAh_cm2": cap,
            "source_model_effective_current_mA_cm2": eff_current,
            "model_amplification_kappa": kappa,
            "model_active_fraction_proxy_1_over_kappa": 1.0 / kappa,
            "sufficient_global_current_multiplier_1_over_kappa2": 1.0 / kappa ** 2,
        }

    # 1 (mA cm^-2)*(mAh cm^-2) = 3.6e5 A^2 s m^-4.
    target_q, global_j = 1.1, 2.2
    vsc_estimates = {
        "Table3_reported": table3["LiMgLa"]["reported_VSC"],
        "Table3_recalculated_from_rounded_D_c0": table3["LiMgLa"]["computed_VSC_SI"],
        "Fig2f_free_intercept_slope_transform": fits["LiMgLa"]["vsc_from_free_slope_SI_A2_s_m4"],
        "Fig2f_origin_constrained_slope_transform": fits["LiMgLa"]["vsc_from_origin_slope_SI_A2_s_m4"],
    }
    bound_estimates = {}
    for name, vsc_si in vsc_estimates.items():
        vsc_units = vsc_si / 360000.0
        kappa_limit = math.sqrt(vsc_units / (global_j * target_q))
        bound_estimates[name] = {
            "vsc_mA2_h_cm_minus4": vsc_units,
            "kappa_limit_for_target": kappa_limit,
            "uniform_contact_fraction_minimum": 1.0 / kappa_limit,
        }
    checks = {
        "LiMgLa_raw_point_count_is_8": len(raw_lmgl) == 8,
        "LiMg_raw_point_count_is_3": len(raw_limg) == 3,
        "LiMgLa_publisher_transform_matches_raw_times": max(transform_errors["LiMgLa"]) < 1e-12,
        "Table3_LiMgLa_VSC_recalculates_within_3pct": abs(table3["LiMgLa"]["reported_over_computed"] - 1.0) < 0.03,
        "nominal_to_local_flux_bound_is_squared": math.isclose(
            bound_estimates["Table3_reported"]["kappa_limit_for_target"] ** 2
            * global_j * target_q,
            bound_estimates["Table3_reported"]["vsc_mA2_h_cm_minus4"],
            rel_tol=1e-12,
        ),
    }
    if not all(checks.values()):
        raise AssertionError({k: v for k, v in checks.items() if not v})
    result = {
        "scope": "internal arithmetic/source-data check only; no physical validation",
        "formula": {
            "Sand": "tau^(-1/2)=2*j/(sqrt(pi*D)*c0*F)",
            "VSC": "pi*D*c0^2*F^2/4 = j^2*tau",
            "conditional_spatial_bound": "kappa^2*jbar*Q < VSC",
            "units_conversion": "1 (mA cm^-2)(mAh cm^-2) = 360000 A^2 s m^-4",
        },
        "raw_data_linear_fits": fits,
        "publisher_transform_max_abs_error_s_minus_half": {
            k: max(v) for k, v in transform_errors.items()
        },
        "supplementary_table3_recalculation": table3,
        "phase_field_source_data_effective_current": model_amp,
        "conditional_example": {
            "target_Q_mAh_cm2": target_q,
            "average_j_mA_cm2": global_j,
            "source_reported_pair": "2.2 mA cm^-2 / 1.1 mAh cm^-2",
            "bounds_by_VSC_estimator": bound_estimates,
            "scope": "conditional independent-column comparison; not a cell-performance forecast",
        },
        "finite_checks_passed": checks,
        "sha256": {
            p.name: sha256(p) for p in sorted(SOURCES.iterdir())
            if p.is_file() and p.suffix.lower() in {".pdf", ".xlsx"}
        },
    }
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
