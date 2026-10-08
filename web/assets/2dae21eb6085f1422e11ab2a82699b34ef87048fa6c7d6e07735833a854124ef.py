#!/usr/bin/env python3
"""Reconstruct a matched-bulk / divergent-clone example from Appold et al. data.

This is a descriptive, finite-data audit. It implements the final published
clone eligibility and escape definitions stated in the Methods of Appold et
al. (2026), rather than the 10/60-um defaults in an older checked-in figure
script. It uses only Python's standard library.

Run from any directory:
    python3 work/agents/c12_evolution_control/scripts/appold_bulk_alias.py
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any


FRAMES_PER_HOUR = 2.0
UM_PER_PIXEL = 8.648
FIRST_DETECTION_FRAME_MIN = 12.5 * FRAMES_PER_HOUR
FIRST_DETECTION_FRAME_MAX = 100.0 * FRAMES_PER_HOUR
ELIGIBLE_BAND_UM = (17.0, 500.0)
MIN_CONSECUTIVE_FRAMES = 3
BREACH_UM = 20.0
RETREAT_UM = 80.0
CHECKPOINT_FRAME = 145
RATE_START_FRAME = 141
FOLLOWUP_END_FRAME = 251
ADAPTIVE_PULSE_FRAMES = ((37, 61), (110, 141), (189, 284))


def _source_dir() -> Path:
    agent_dir = Path(__file__).resolve().parents[1]
    return agent_dir.parent / "c11_evolution_control" / "sources" / "Appold_figuredata" / "adaptive_therapy"


def read_colony(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    required = {"frame", "particle", "distance_to_edge", "colony_area"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError(f"{path}: missing required columns {sorted(required)}")
    return rows


def longest_consecutive_run(frames: list[int]) -> int:
    best = run = 0
    previous: int | None = None
    for frame in sorted(set(frames)):
        run = run + 1 if previous is not None and frame == previous + 1 else 1
        best = max(best, run)
        previous = frame
    return best


def reconstruct(name: str, path: Path) -> dict[str, Any]:
    rows = read_colony(path)
    by_frame: dict[int, list[dict[str, str]]] = {}
    by_particle: dict[str, list[tuple[int, float]]] = {}
    for row in rows:
        frame = int(row["frame"])
        distance_um = float(row["distance_to_edge"]) * UM_PER_PIXEL
        by_frame.setdefault(frame, []).append(row)
        by_particle.setdefault(row["particle"], []).append((frame, distance_um))

    def frame_area(frame: int) -> float:
        values = {float(row["colony_area"]) for row in by_frame[frame]}
        if len(values) != 1:
            raise ValueError(f"{name}, frame {frame}: inconsistent colony_area values {values}")
        return values.pop()

    def min_front_um(frame: int) -> tuple[str, float]:
        pairs = [
            (row["particle"], float(row["distance_to_edge"]) * UM_PER_PIXEL)
            for row in by_frame[frame]
        ]
        return min(pairs, key=lambda pair: pair[1])

    eligible: list[tuple[str, list[tuple[int, float]]]] = []
    for particle, observations in by_particle.items():
        observations.sort()
        first_frame = observations[0][0]
        if not (FIRST_DETECTION_FRAME_MIN <= first_frame <= FIRST_DETECTION_FRAME_MAX):
            continue
        if not any(ELIGIBLE_BAND_UM[0] <= d <= ELIGIBLE_BAND_UM[1] for _, d in observations):
            continue
        if longest_consecutive_run([frame for frame, _ in observations]) < MIN_CONSECUTIVE_FRAMES:
            continue
        eligible.append((particle, observations))

    breaches: list[dict[str, Any]] = []
    escapes: list[dict[str, Any]] = []
    for particle, observations in eligible:
        breach_observations = [(frame, d) for frame, d in observations if d <= BREACH_UM]
        if not breach_observations:
            continue
        breach_frame, breach_distance = breach_observations[0]
        post = [(frame, d) for frame, d in observations if frame > breach_frame]
        retreat_frames = [frame for frame, d in post if d > RETREAT_UM]
        retreated = bool(retreat_frames)
        event = {
            "particle": particle,
            "first_breach_frame": breach_frame,
            "first_breach_time_h": breach_frame / FRAMES_PER_HOUR,
            "distance_at_first_breach_um": breach_distance,
            "observed_through_frame": observations[-1][0],
            "observed_through_time_h": observations[-1][0] / FRAMES_PER_HOUR,
            "followup_hours_after_first_breach": (observations[-1][0] - breach_frame) / FRAMES_PER_HOUR,
            "subsequent_retreat_beyond_80um": retreated,
            "first_retreat_beyond_80um_frame": retreat_frames[0] if retreat_frames else None,
            "first_retreat_beyond_80um_time_h": (
                retreat_frames[0] / FRAMES_PER_HOUR if retreat_frames else None
            ),
        }
        breaches.append(event)
        if not retreated:
            escapes.append(event)

    if RATE_START_FRAME not in by_frame or CHECKPOINT_FRAME not in by_frame:
        raise ValueError(f"{name}: missing checkpoint frames {RATE_START_FRAME}/{CHECKPOINT_FRAME}")
    area_start = frame_area(RATE_START_FRAME)
    area_checkpoint = frame_area(CHECKPOINT_FRAME)
    elapsed_h = (CHECKPOINT_FRAME - RATE_START_FRAME) / FRAMES_PER_HOUR
    log_area_rate = math.log(area_checkpoint / area_start) / elapsed_h
    closest_particle, closest_um = min_front_um(CHECKPOINT_FRAME)

    breaches_after_checkpoint = [e for e in breaches if e["first_breach_frame"] > CHECKPOINT_FRAME]
    escapes_after_checkpoint = [e for e in escapes if e["first_breach_frame"] > CHECKPOINT_FRAME]
    return {
        "colony": name,
        "source_file": str(path),
        "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "rows": len(rows),
        "last_frame": max(by_frame),
        "eligible_track_count": len(eligible),
        "eligible_breach_count": len(breaches),
        "eligible_escape_count_through_observed_horizon": len(escapes),
        "eligible_breaches": breaches,
        "eligible_escapes": escapes,
        "checkpoint": {
            "frame": CHECKPOINT_FRAME,
            "time_h": CHECKPOINT_FRAME / FRAMES_PER_HOUR,
            "colony_area_px2": area_checkpoint,
            "log_area_rate_per_h_over_2h_before_checkpoint": log_area_rate,
            "nearest_tracked_clone_particle": closest_particle,
            "nearest_tracked_clone_clearance_um": closest_um,
            "eligible_breaches_in_followup": breaches_after_checkpoint,
            "eligible_escapes_in_followup": escapes_after_checkpoint,
        },
    }


def main() -> None:
    source_dir = _source_dir()
    p2 = reconstruct("P2", source_dir / "clone_data_fusion_resolved_P2.csv")
    p3 = reconstruct("P3", source_dir / "clone_data_fusion_resolved_P3.csv")
    all_colonies = [
        reconstruct(f"P{i}", source_dir / f"clone_data_fusion_resolved_P{i}.csv")
        for i in range(1, 9)
    ]
    timing_events: list[dict[str, Any]] = []
    for colony in all_colonies:
        for event in colony["eligible_breaches"]:
            frame = event["first_breach_frame"]
            treatment_interval = next(
                (span for span in ADAPTIVE_PULSE_FRAMES if span[0] <= frame <= span[1]),
                None,
            )
            previous_ends = [end for _, end in ADAPTIVE_PULSE_FRAMES if end < frame]
            later_starts = [start for start, _ in ADAPTIVE_PULSE_FRAMES if start > frame]
            previous_end = max(previous_ends) if previous_ends else None
            next_start = min(later_starts) if later_starts else None
            timing_events.append({
                "colony": colony["colony"],
                **event,
                "treatment_phase_at_first_breach": "on" if treatment_interval else "off",
                "pulse_interval_containing_breach_frames": list(treatment_interval) if treatment_interval else None,
                "hours_since_previous_pulse_end": (
                    (frame - previous_end) / FRAMES_PER_HOUR if previous_end is not None else None
                ),
                "hours_until_next_pulse_start": (
                    (next_start - frame) / FRAMES_PER_HOUR if next_start is not None else None
                ),
                "hours_from_next_pulse_start_to_first_retreat_beyond_80um": (
                    (event["first_retreat_beyond_80um_frame"] - next_start) / FRAMES_PER_HOUR
                    if next_start is not None and event["first_retreat_beyond_80um_frame"] is not None
                    else None
                ),
            })
    a2 = p2["checkpoint"]["colony_area_px2"]
    a3 = p3["checkpoint"]["colony_area_px2"]
    g2 = p2["checkpoint"]["log_area_rate_per_h_over_2h_before_checkpoint"]
    g3 = p3["checkpoint"]["log_area_rate_per_h_over_2h_before_checkpoint"]
    d2 = p2["checkpoint"]["nearest_tracked_clone_clearance_um"]
    d3 = p3["checkpoint"]["nearest_tracked_clone_clearance_um"]
    if d2 <= 0 or d3 <= 0:
        raise ValueError("Expected positive checkpoint clone-front clearances")

    result = {
        "title": "Descriptive matched-bulk / divergent-clone audit",
        "source_article": "https://doi.org/10.1038/s41559-026-03178-z",
        "source_data_note": "Published Appold figure-data CSVs; final article Methods eligibility and escape criteria implemented here.",
        "parameters": {
            "frames_per_hour": FRAMES_PER_HOUR,
            "micrometres_per_pixel": UM_PER_PIXEL,
            "eligible_first_detection_hours": [12.5, 100.0],
            "eligible_clearance_band_um_at_least_once": list(ELIGIBLE_BAND_UM),
            "minimum_consecutive_frames": MIN_CONSECUTIVE_FRAMES,
            "breach_um": BREACH_UM,
            "retreat_beyond_um_for_confinement": RETREAT_UM,
            "checkpoint_frame": CHECKPOINT_FRAME,
            "growth_rate_window_frames": [RATE_START_FRAME, CHECKPOINT_FRAME],
        },
        "colonies": [p2, p3],
        "all_eight_colony_contact_timing_screen": {
            "adaptive_pulse_frames_from_source_figure_code": [list(span) for span in ADAPTIVE_PULSE_FRAMES],
            "eligible_track_counts_P1_to_P8": [colony["eligible_track_count"] for colony in all_colonies],
            "eligible_first_breach_count": len(timing_events),
            "source_defined_escape_count_through_observed_horizon": sum(
                not event["subsequent_retreat_beyond_80um"] for event in timing_events
            ),
            "breach_then_retreat_count_through_observed_horizon": sum(
                event["subsequent_retreat_beyond_80um"] for event in timing_events
            ),
            "events": timing_events,
            "interpretation": "The two post-frame-145 breach events have different recorded fates and different timing relative to the next shared pulse; this is a post-hoc pattern, not an estimated rescue-latency law or causal effect.",
        },
        "pair_comparison": {
            "area_px2_absolute_difference_pct_of_P3": abs(a2 - a3) / a3 * 100.0,
            "area_px2_absolute_difference_pct_of_mean": abs(a2 - a3) / ((a2 + a3) / 2.0) * 100.0,
            "log_area_rate_per_h_absolute_difference_pct_of_P3": abs(g2 - g3) / abs(g3) * 100.0,
            "clearance_ratio_P3_over_P2": d3 / d2,
            "interpretation": "One post-hoc pair with similar bulk area/rate and different clone-front clearance and eligible escape histories; descriptive only.",
        },
        "limitations": [
            "Two selected colonies do not estimate predictive accuracy, risk, or policy value.",
            "The data share a treatment protocol; this does not identify a causal effect of using clone clearance to steer treatment.",
            "No cancer or patient-level transfer is tested.",
        ],
    }
    out = Path(__file__).resolve().parents[1] / "outputs" / "appold_bulk_alias.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
