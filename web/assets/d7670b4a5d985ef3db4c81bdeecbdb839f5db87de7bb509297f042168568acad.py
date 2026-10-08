#!/usr/bin/env python3
"""Read-only source-data / model-observable interface audit.

Reads the official source workbook and companion CSVs without modifying them,
then replays two already-identified finite-PDE speed aliases at a modest grid.
The outputs are intentionally scoped to source observables and conditional
model predictions; the script does not fit biological parameters.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, stdev

import numpy as np
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[3]
ATTACK = ROOT / "work/agents/c8_morphogenesis_control/cycle9/deeper_attack"
DATA = ATTACK / "source_data"
BOOK = DATA / "41467_2025_59164_MOESM10_ESM.xlsx"
OUT = Path(__file__).with_name("observable_interface_results.json")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def by_video_velocity() -> dict:
    rows = load_csv("Velocities_all_videos.csv")
    grouped: dict[tuple[int, str], list[float]] = defaultdict(list)
    all_by_location: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        video = int(float(row["Video"]))
        loc = row["Location"]
        value = float(row["Velocity"])
        grouped[(video, loc)].append(value)
        all_by_location[loc].append(value)
    videos = {}
    for (video, loc), values in sorted(grouped.items()):
        videos.setdefault(str(video), {})[loc] = {
            "n_cells": len(values), "mean_speed_norm": mean(values),
            "within_cell_sd": stdev(values) if len(values) > 1 else None,
        }
    location = {}
    for loc, values in all_by_location.items():
        m = mean(values)
        byvid = [videos[str(v)][loc]["mean_speed_norm"] for v in sorted(map(int, {x[0] for x in grouped if x[1] == loc}))]
        location[loc] = {
            "n_cells": len(values), "mean_speed_norm": m,
            "within_cell_sd": stdev(values), "per_video_means": byvid,
            "between_video_mean_sd": stdev(byvid) if len(byvid) > 1 else None,
            "between_video_sem": stdev(byvid) / math.sqrt(len(byvid)) if len(byvid) > 1 else None,
            "estimand": "individual 2D endpoint-displacement norm over six hours per article Methods; not signed Eulerian x velocity",
        }
    return {"source_rows": len(rows), "by_video_location": videos, "by_location": location}


def source_track_summaries() -> dict:
    # Worksheet positions: field descriptions in rows 3:8, table header row 11,
    # records rows 12:14263.
    wb = load_workbook(BOOK, read_only=True, data_only=True)
    ws = wb["Fig1H"]
    records = []
    for row in ws.iter_rows(min_row=12, values_only=True):
        if row[0] is None:
            continue
        cell, ti, x, y, video, loc = row[:6]
        records.append((int(cell), int(ti), float(x), float(y), int(video), str(loc)))
    tracks: dict[tuple[int, int, str], list[tuple[int, float, float]]] = defaultdict(list)
    for cell, ti, x, y, video, loc in records:
        tracks[(video, cell, loc)].append((ti, x, y))
    by_group: dict[tuple[int, str], list[int]] = defaultdict(list)
    npoints = []
    time_max = 0
    for (video, cell, loc), points in tracks.items():
        by_group[(video, loc)].append(len(points))
        npoints.append(len(points))
        time_max = max(time_max, max(p[0] for p in points))
    grp = {
        f"video_{video}|{loc}": {
            "n_tracks": len(lengths),
            "track_points_median": float(np.median(lengths)),
            "track_points_min": min(lengths), "track_points_max": max(lengths),
        }
        for (video, loc), lengths in sorted(by_group.items())
    }
    # These records use raw X/Y coordinates; the sheet does not supply a length unit.
    wb.close()

    # Companion longitudinal mean-displacement table has an explicit micrometre label
    # in the companion plotting Rmd, but keeps each video/location separate.
    live = load_csv("data_ex_vivo_tracked_cells_all.csv")
    live_groups: dict[tuple[str, str], list[tuple[float, float]]] = defaultdict(list)
    for row in live:
        live_groups[(row["data_set"], row["location"])].append(
            (float(row["time"]), float(row["mean_displacement"]))
        )
    displacements = {}
    for (dataset, loc), values in sorted(live_groups.items()):
        ordered = sorted(values)
        fit = np.polyfit([t for t, _ in ordered if t <= 6], [x for t, x in ordered if t <= 6], 1)
        at6 = float(np.interp(6.0, [t for t, _ in ordered], [x for _, x in ordered]))
        displacements.setdefault(dataset, {})[loc] = {
            "n_time_rows": len(ordered), "time_min_hr": ordered[0][0],
            "time_max_hr": ordered[-1][0], "x_displacement_at_6h_um": at6,
            "x_displacement_ols_slope_0_6h_um_per_h": float(fit[0]),
        }
    aggregate = {}
    locations = sorted({loc for item in displacements.values() for loc in item})
    for loc in locations:
        pairs = [(dataset, item[loc]["x_displacement_at_6h_um"])
                 for dataset, item in sorted(displacements.items()) if loc in item]
        values = [x for _, x in pairs]
        sd = stdev(values) if len(values) > 1 else None
        sem = sd / math.sqrt(len(values)) if sd is not None else None
        # Four source experiments => t_(.975,3)=3.182. This interval is a
        # descriptive video-level uncertainty summary, not a fitted-model test.
        half = 3.182 * sem if sem is not None and len(values) == 4 else None
        aggregate[loc] = {
            "n_independent_datasets": len(values), "by_dataset_um": dict(pairs),
            "mean_x_displacement_at_6h_um": mean(values),
            "between_dataset_sd_um": sd, "between_dataset_sem_um": sem,
            "descriptive_t95_ci_for_mean_um": [mean(values) - half, mean(values) + half] if half is not None else None,
        }
    return {
        "Fig1H": {
            "source_range": "Fig1H!A1:F14263; title row 1; field descriptions A3:B8; header row 11; records rows 12:14263",
            "records": len(records), "unique_tracks": len(tracks),
            "time_point_max_index": time_max,
            "time_step_from_sheet_metadata": "10 min",
            "groups": grp,
            "unit_boundary": "X/Y are raw source coordinates; worksheet gives no physical unit or scale calibration",
        },
        "companion_x_displacement": {
            "source_csv": "data_ex_vivo_tracked_cells_all.csv",
            "groups_by_dataset_location": displacements,
            "aggregate_at_6h_by_location": aggregate,
            "unit_provenance": "plot_results_with_data.Rmd labels displacement in microns; time column in hours",
        },
    }


def workbook_summaries() -> dict:
    wb = load_workbook(BOOK, read_only=True, data_only=True)
    fig3b = wb["Fig3B"]
    rows3b = list(fig3b.iter_rows(min_row=13, values_only=True))
    # The final merged Figure 3B export pools ex-vivo locations for this plotted
    # series (location overwritten to 'cells' in the author's Rmd before export).
    groups3b: dict[tuple[str, str], list[tuple[float, float, float]]] = defaultdict(list)
    for r in rows3b:
        if r[0] is None:
            continue
        _id, time, x, dataset, location, source, x_avg, x_sem = r[:8]
        if str(time).upper() == "NA" or str(x_avg).upper() == "NA":
            continue
        sem = None if str(x_sem).upper() == "NA" else float(x_sem)
        groups3b[(str(_id), str(location))].append((float(time), float(x_avg), sem))
    fig3b_summary = {}
    for (identity, loc), vals in sorted(groups3b.items()):
        at6 = [x for t, x, _ in vals if abs(t - 6.0) < 1e-6]
        fig3b_summary[f"{identity}|{loc}"] = {
            "n_rows": len(vals), "x_avg_at_6h": at6[0] if at6 else None,
            "time_range_hr": [min(t for t, _, _ in vals), max(t for t, _, _ in vals)],
        }
    # Fig2D is average GFP intensity over pixel-indexed medial-lateral position.
    fig2d = wb["Fig2D"]
    cols = fig2d.max_column - 2  # B:EEW = 3532 values; A is time, B onward profile
    profiles = {}
    for row in fig2d.iter_rows(min_row=5, max_row=41, min_col=1,
                               max_col=fig2d.max_column, values_only=True):
        time_i = row[0]
        if time_i is None:
            continue
        vals = np.asarray(row[1:], dtype=float)
        # Shape-only dynamic range and normalized 10--90% transition width in pixels.
        # Use the global row min/max as a descriptive observable; no phi calibration is claimed.
        lo, hi = float(np.min(vals)), float(np.max(vals))
        frac = (vals - lo) / (hi - lo) if hi > lo else np.zeros_like(vals)
        target_lo, target_hi = 0.1, 0.9
        ix_lo = int(np.argmin(np.abs(frac - target_lo)))
        ix_hi = int(np.argmin(np.abs(frac - target_hi)))
        profiles[str(int(time_i))] = {
            "n_pixels": len(vals), "intensity_min": lo, "intensity_max": hi,
            "intensity_range": hi - lo,
            "normalized_10_90_nearest_pixel_span": abs(ix_hi - ix_lo),
        }
    fig3c = wb["Fig3C"]
    fig3c_measured = {}
    for row in fig3c.iter_rows(min_row=9, max_row=11, min_col=1, max_col=5, values_only=True):
        loc, xmean, xsd, vmean, vsd = row
        if loc is None:
            continue
        fig3c_measured[str(loc)] = {
            "mean_initial_x_coordinate_um": float(xmean),
            "sd_initial_x_coordinate_um": float(xsd),
            "mean_2d_speed_norm_um_per_h": float(vmean),
            "sd_cell_speed_norm_um_per_h": float(vsd),
        }
    wb.close()
    return {
        "Fig3B": {
            "source_range": "Fig3B!A1:H889; metadata rows 1:10; blank row 11; column header row 12; records rows 13:889",
            "groups": fig3b_summary,
            "source_code_boundary": "companion Rmd final plotting table pools all ex-vivo locations into location='cells'; model cell path retained only Bone Front",
        },
        "Fig2D": {
            "source_range": "Fig2D!A1:EEW41; title row 1; axis metadata row 3; profile header row 4; profile records rows 5:41",
            "profiles_by_time_index": profiles,
            "time_index": "0..36; sheet labels index but gives no minute-per-index conversion",
            "unit_boundary": "position is pixel index and intensity is GFP fluorescence; workbook does not supply pixel-to-um calibration or a fluorescence-to-phi calibration",
        },
        "Fig3C": {
            "source_range": "Fig3C!A1:E147; measured location summaries rows 9:11; model velocity profile header row 14 and data rows 15:147",
            "measured_cell_velocity_summaries": fig3c_measured,
            "unit_provenance": "article Methods define measured speed as 2D endpoint displacement norm divided by six hours; model output V is signed 1D Eulerian velocity",
        },
    }


def pde_aliases() -> dict:
    module_path = ATTACK / "replay_coupled_fd.py"
    spec = importlib.util.spec_from_file_location("replay_coupled_fd", module_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    x0s = (0.0, -200.0, -400.0)
    results = {}
    for name, steep, alpha in (("released", 4.0, 3.5e-6), ("speed_alias", 8.0, 1.934e-6)):
        sim = mod.run(nx=800, nt=3200, a_phi=steep, alpha=alpha, a_rho=steep, fast_solve=True)
        x = sim["x"]
        t = sim["time"]
        phi, vel = sim["phi"], sim["velocity"]
        dphi = np.gradient(phi, sim["dx_um"], axis=0, edge_order=2)
        v_b = vel - 15.0 * dphi / np.maximum(phi, 1e-10)
        crossings = mod.front_crossings(x, phi, 0.5)
        secant = float((crossings[-1] - crossings[0]) / (t[-1] - t[0]))
        profiles = {}
        for x0 in x0s:
            ix = int(np.argmin(np.abs(x - x0)))
            profiles[str(x0)] = {
                "grid_x_um": float(x[ix]),
                "phi_t0": float(phi[ix, 0]),
                "eulerian_V_initial_t0_um_per_h": float(vel[ix, 0]),
                "conditional_vB_initial_t0_um_per_h": float(v_b[ix, 0]),
                "eulerian_V_t1h_um_per_h": float(np.interp(1.0, t, vel[ix, :])),
                "conditional_vB_t1h_um_per_h": float(np.interp(1.0, t, v_b[ix, :])),
                "eulerian_V_mean_0_6h_um_per_h": float(np.trapezoid(vel[ix, t <= 6], t[t <= 6]) / 6.0),
                "conditional_vB_mean_0_6h_um_per_h": float(np.trapezoid(v_b[ix, t <= 6], t[t <= 6]) / 6.0),
            }
        # Characteristic paths under two distinct field-to-marker mappings:
        # (i) source-plotted Eulerian field V; (ii) conditional B-species velocity.
        def field_value(field: np.ndarray, xx: float, tt: float) -> float:
            xx = float(np.clip(xx, x[0], x[-1]))
            tt = float(np.clip(tt, t[0], t[-1]))
            ix = int(np.clip(np.searchsorted(x, xx) - 1, 0, len(x) - 2))
            it = int(np.clip(np.searchsorted(t, tt) - 1, 0, len(t) - 2))
            ax = (xx - x[ix]) / (x[ix + 1] - x[ix])
            at = (tt - t[it]) / (t[it + 1] - t[it])
            a = field[ix, it] * (1 - ax) + field[ix + 1, it] * ax
            b = field[ix, it + 1] * (1 - ax) + field[ix + 1, it + 1] * ax
            return float(a * (1 - at) + b * at)

        paths = {"V": {}, "v_B_conditional": {}}
        dt = float(t[1] - t[0])
        steps = int(round(6.0 / dt))
        for mapping, field in (("V", vel), ("v_B_conditional", v_b)):
            for xinit in x0s:
                xx = xinit
                for j in range(steps):
                    tt = j * dt
                    u0 = field_value(field, xx, tt)
                    up = field_value(field, xx + dt * u0, tt + dt)
                    xx += 0.5 * dt * (u0 + up)
                paths[mapping][str(xinit)] = {
                    "x_displacement_0_6h_um": xx - xinit,
                    "mean_signed_x_speed_0_6h_um_per_h": (xx - xinit) / 6.0,
                }
        results[name] = {
            "a_rho": steep, "a_phi": steep, "alpha": alpha,
            "grid": {"nx": sim["nx"], "nt": sim["nt"], "dx_um": sim["dx_um"], "dt_hr": sim["dt_hr"]},
            "phi_half_front_secant_0_8h_um_per_h": secant,
            "three_location_model_profiles": profiles,
            "conditional_paths": paths,
            "mapping_formula": "from the published phenotype PDE in conservative form, candidate osteoblast species velocity v_B = V - D*(partial_x phi)/phi, D=15 um^2/h; this is a conditional mapping, not an observed source-data equivalence",
        }
        del sim
    # At fixed positions, profile distance between alternatives conditional on each mapping.
    r = results["released"]["three_location_model_profiles"]
    a = results["speed_alias"]["three_location_model_profiles"]
    contrasts = {}
    for x0 in map(str, x0s):
        contrasts[x0] = {}
        for key in ("eulerian_V_initial_t0_um_per_h", "conditional_vB_initial_t0_um_per_h", "eulerian_V_t1h_um_per_h", "conditional_vB_t1h_um_per_h", "eulerian_V_mean_0_6h_um_per_h", "conditional_vB_mean_0_6h_um_per_h"):
            contrasts[x0][key] = a[x0][key] - r[x0][key]
    observed = source_track_summaries()["companion_x_displacement"]["aggregate_at_6h_by_location"]
    model_x0 = {"Bone Front": "0.0", "In Bone": "-200.0", "Further In Bone": "-400.0"}
    trajectory_match = {}
    loc_order = ["Bone Front", "In Bone", "Further In Bone"]
    m0 = np.asarray([results["released"]["conditional_paths"]["v_B_conditional"][model_x0[loc]]["x_displacement_0_6h_um"] for loc in loc_order])
    m1 = np.asarray([results["speed_alias"]["conditional_paths"]["v_B_conditional"][model_x0[loc]]["x_displacement_0_6h_um"] for loc in loc_order])
    delta = m1 - m0
    unit_delta = delta / np.linalg.norm(delta)
    dataset_ids = sorted(observed[loc_order[0]]["by_dataset_um"])
    data_vectors = np.asarray([[observed[loc]["by_dataset_um"][dataset] for loc in loc_order] for dataset in dataset_ids])
    discriminant_scores = data_vectors @ unit_delta
    score_mean = float(np.mean(discriminant_scores))
    score_sd = float(np.std(discriminant_scores, ddof=1))
    score_sem = score_sd / math.sqrt(len(dataset_ids))
    score_halfwidth = 3.182 * score_sem if len(dataset_ids) == 4 else None
    model_score0 = float(unit_delta @ m0)
    model_score1 = float(unit_delta @ m1)
    for loc, x0 in model_x0.items():
        exp = observed[loc]
        released_pred = results["released"]["conditional_paths"]["v_B_conditional"][x0]["x_displacement_0_6h_um"]
        alias_pred = results["speed_alias"]["conditional_paths"]["v_B_conditional"][x0]["x_displacement_0_6h_um"]
        trajectory_match[loc] = {
            "empirical_four_video_mean_x_displacement_at_6h_um": exp["mean_x_displacement_at_6h_um"],
            "empirical_between_video_sd_um": exp["between_dataset_sd_um"],
            "empirical_descriptive_t95_ci_for_mean_um": exp["descriptive_t95_ci_for_mean_um"],
            "released_pair_conditional_vB_prediction_um": released_pred,
            "speed_alias_conditional_vB_prediction_um": alias_pred,
            "alias_minus_released_prediction_um": alias_pred - released_pred,
        }
    return {
        "mesh_scope": "Nx=800,Nt=3200; the previously documented Nx=3200,Nt=25600 run controls the high-resolution speed-match claim",
        "cases": results,
        "alias_minus_released_fixed_position_contrasts": contrasts,
        "conditional_comparison_to_four_video_x_displacements": {
            "mapping": "compare 1D phenotype-material characteristic v_B=V−Dφ_x/φ, initialized at the three model positions used by the source Rmd, with measured signed x-projected mean cell displacement by source video/location",
            "independent_sample_unit": "four ex-vivo datasets/videos; not individual cell counts or repeated time rows",
            "comparison": trajectory_match,
            "boundary": "conditional observable map; not a new fit or validation claim; empirical trajectory is a location-level mean while the PDE path is deterministic",
        },
        "named_pair_discriminating_projection": {
            "definition": "u=(m_alias-m_released)/||m_alias-m_released|| across the three initial locations; each independent video contributes u dot its 3-location vector of 6h mean x displacements",
            "locations_order": loc_order,
            "released_model_vector_um": m0.tolist(),
            "speed_alias_model_vector_um": m1.tolist(),
            "unit_discriminant_direction": unit_delta.tolist(),
            "observed_video_scores_um": {dataset: float(score) for dataset, score in zip(dataset_ids, discriminant_scores)},
            "empirical_projected_mean_um": score_mean,
            "between_video_sd_um": score_sd,
            "n_independent_videos": len(dataset_ids),
            "descriptive_t95_ci_for_projected_mean_um": [score_mean - score_halfwidth, score_mean + score_halfwidth] if score_halfwidth is not None else None,
            "released_model_projected_value_um": model_score0,
            "speed_alias_projected_value_um": model_score1,
            "boundary": "exploratory one-contrast comparison of this named model pair; t interval assumes four independent video-level values and does not cover model, mapping, or parameter uncertainty",
        },
    }


def main() -> None:
    result = {
        "source": {
            "paper_doi": "10.1038/s41467-025-59164-9",
            "repository_commit": "b2cbb61097cdc25bfff1e0a89ba690a31c2a4adc",
            "workbook_path": str(BOOK.resolve()),
            "workbook_sha256": sha256(BOOK),
            "workbook_bytes": BOOK.stat().st_size,
            "source_data_csv_sha256": {n: sha256(DATA / n) for n in (
                "Velocities_all_videos.csv", "data_ex_vivo_tracked_cells_all.csv",
                "data_ex_vivo_videos_1_to_4_all_interfaces.csv")},
        },
        "velocity_observations": by_video_velocity(),
        "position_observations": source_track_summaries(),
        "workbook_summaries": workbook_summaries(),
        "pde_alias_observation_interface": pde_aliases(),
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUT.resolve()), "workbook_sha256": result["source"]["workbook_sha256"],
        "tracks": result["position_observations"]["Fig1H"]["unique_tracks"],
        "velocity_n": result["velocity_observations"]["source_rows"],
        "alias_contrasts": result["pde_alias_observation_interface"]["alias_minus_released_fixed_position_contrasts"],
    }, indent=2))


if __name__ == "__main__":
    main()
