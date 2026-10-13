"""Frequency-resolved partial-secular control for Sol01's pair mechanism.

This is a model-sensitivity check, not a claim that the grouped white-bath
input-output model is wrong. It rebuilds the same Floquet transitions and
compares (i) collapse operators grouped by harmonic k, as in the source model,
with (ii) operators grouped only for lines in <=1 MHz-wide frequency clusters
within each (bath,k). Matched logical g/f carrier lines remain coherent; lines
separated by 90 MHz do not. The finite RF waveform is imported from the exact
current Sol01 script, including its continuous-envelope midpoint refinement.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SOL01 = ROOT / "work/continuation/sol01_quantum"
SOURCE = Path("/Users/harjas/Documents/Codex/2026-10-13/astra-genesis-civilization-enabling-breakthrough-discovery")
sys.path.insert(0, str(SOL01))
import pair_fluorescence_test as pair  # noqa: E402
import alternative_control_gates as controls  # noqa: E402
from pair_fluorescence_test import f  # noqa: E402


def _frequency_clusters(lines, tolerance_mhz):
    """Assign sorted lines to clusters whose full span is <= tolerance."""
    order = sorted(range(len(lines)), key=lambda i: lines[i]["frequency_MHz"])
    clusters = []
    for ix in order:
        nu = lines[ix]["frequency_MHz"]
        if not clusters or nu - clusters[-1]["low"] > tolerance_mhz:
            clusters.append({"low": nu, "high": nu, "members": [ix]})
        else:
            clusters[-1]["high"] = nu
            clusters[-1]["members"].append(ix)
    for cluster_id, cluster in enumerate(clusters):
        for ix in cluster["members"]:
            lines[ix]["cluster"] = cluster_id
    return clusters


def build_models(qdim=5, nf=6, epsilon=217.28013507543088, tolerance_mhz=1.0):
    """Reconstruct the source transition map into grouped and split channels."""
    f.ecr.MEASURED_HALF_GE_CAVITY_SHIFT_MHZ = 0.5
    g = f.ecr.calibrate_g()
    f.f.G = g
    f.f.DELTA = -2203.0

    scan = []
    for omega in np.arange(2463.0, 2484.0, 1.0):
        block = f.f.floquet_block(3, epsilon, omega, sambe_half=5, ramp_steps=24)
        ee = block["values"][1] + omega
        hh = block["values"][3] + 3 * omega
        scan.append({"omega_MHz": float(omega), "e2_h0_gap_MHz": float(abs(ee - hh))})
    omega = min(scan, key=lambda row: row["e2_h0_gap_MHz"])["omega_MHz"]
    blocks = {N: f.f.floquet_block(N, epsilon, omega, sambe_half=5, ramp_steps=24)
              for N in range(qdim + nf)}
    basis = [(q, n) for q in range(qdim) for n in range(nf)]
    index = {state: i for i, state in enumerate(basis)}
    dim = len(basis)
    energies = np.array([blocks[q + n]["values"][q] + q * omega for q, n in basis])
    rf_detuning = (energies[index[(3, 0)]] - energies[index[(1, 0)]]) / 2
    totals = np.array([q + n for q, n in basis])
    energies -= rf_detuning * totals
    calibration = f.static_vacuum_rates(g)

    # Retain each physical-frequency component until the secular grouping rule
    # has been applied. A transition record is one matrix element of a jump.
    lines = {"a": {}, "b": {}}
    outside = np.zeros(dim)
    drive = np.zeros((dim, dim), complex)
    vacuum = []
    for i, (qi, n) in enumerate(basis):
        N = qi + n
        if N == 0:
            continue
        source, target = blocks[N], blocks[N - 1]
        for qo in range(len(target["values"])):
            no = N - 1 - qo
            for bath, extractor in [("a", f.f.cavity_loss_harmonics), ("b", f.bath_harmonics)]:
                harmonics = extractor(source, target, qi, qo)
                scale = f.KAPPA if bath == "a" else calibration[2 if qi >= 2 else 1]["bath_scale"]
                for ell, z in harmonics.items():
                    physical = 7153.0 + source["values"][qi] - target["values"][qo] - ell * omega
                    if physical <= 0 or abs(z) < 1e-10:
                        continue
                    k = ell + qi - qo
                    if (qo, no) in index:
                        j = index[(qo, no)]
                        line = {"bath": bath, "k": k, "frequency_MHz": float(physical),
                                "i": i, "j": j, "amp": complex(np.sqrt(scale) * z),
                                "qi": qi, "qo": qo, "n": n, "no": no,
                                "ell": ell, "rate": float(scale * abs(z) ** 2)}
                        lines[bath].setdefault(k, []).append(line)
                        if bath == "b" and k == 1:
                            # Same commensurate RF drive projection as Sol01.
                            drive[j, i] += z
                    else:
                        outside[i] += scale * abs(z) ** 2
                    if n == 0 and scale * abs(z) ** 2 > 1e-6:
                        vacuum.append({"input_q": qi, "output_q": qo, "output_n": no,
                                       "bath": bath, "harmonic_k": k,
                                       "frequency_MHz": float(physical),
                                       "rate_per_us": float(scale * abs(z) ** 2)})

    grouped = {"a": {}, "b": {}}
    split = {"a": {}, "b": {}}
    cluster_summary = {}
    for bath in ("a", "b"):
        for k, by_frequency in lines[bath].items():
            grouped[bath][k] = np.zeros((dim, dim), complex)
            for line in by_frequency:
                grouped[bath][k][line["j"], line["i"]] += line["amp"]
            clusters = _frequency_clusters(by_frequency, tolerance_mhz)
            cluster_summary[f"{bath}:k={k}"] = [
                {"frequency_low_MHz": float(c["low"]), "frequency_high_MHz": float(c["high"]),
                 "span_MHz": float(c["high"] - c["low"]), "matrix_elements": len(c["members"])}
                for c in clusters
            ]
            for cluster_id, cluster in enumerate(clusters):
                C = np.zeros((dim, dim), complex)
                for ix in cluster["members"]:
                    line = by_frequency[ix]
                    C[line["j"], line["i"]] += line["amp"]
                split[bath][(k, cluster_id)] = C

    def make_model(collapse):
        return {"dim": dim, "basis": basis, "energies": energies, "drive": drive,
                "collapse": collapse, "outside": outside}

    # The representative 90 MHz pair is from the vacuum h0 source. Compute its
    # grouped jump cross term directly; splitting removes this one-click
    # e1/f0 coherence, though not all physical coherences in the device.
    by_q0 = {(x["output_q"], x["output_n"]): x for x in vacuum
             if x["bath"] == "a" and x["input_q"] == 3 and x["harmonic_k"] == 0}
    h_e = by_q0[(1, 1)]
    h_f = by_q0[(2, 0)]
    r1, r2 = h_e["rate_per_us"], h_f["rate_per_us"]

    # Exact near-degenerate matched logical carrier pair at n=1, k=0.
    logical_lines = {}
    for q in (0, 2):
        N = q + 1
        src, dst = blocks[N], blocks[N - 1]
        matching = []
        for ell, z in f.f.cavity_loss_harmonics(src, dst, q, q).items():
            nu = 7153.0 + src["values"][q] - dst["values"][q] - ell * omega
            if ell == 0 and nu > 0:
                matching.append((nu, abs(z)))
        logical_lines["g" if q == 0 else "f"] = {"frequency_MHz": float(matching[0][0]),
                                                    "matrix_element_abs": float(matching[0][1])}
    logical_delta = abs(logical_lines["g"]["frequency_MHz"] - logical_lines["f"]["frequency_MHz"])
    # The two dressed routes into the same e1 target highlighted by Sol01.
    # They share k=0, but differ by 1.77695 MHz because the h0 route uses
    # ell=-2; a 1 MHz partial-secular grouping resolves them.
    target = blocks[2]
    source_ef = blocks[3]
    route_records = {}
    for label, source, qi, ell in [
        ("e1_n2_to_e1_n1", source_ef, 1, 0),
        ("h0_to_e1_n1", source_ef, 3, -2),
    ]:
        z = f.f.cavity_loss_harmonics(source, target, qi, 1)[ell]
        nu = 7153.0 + source["values"][qi] - target["values"][1] - ell * omega
        route_records[label] = {"harmonic_ell": ell, "harmonic_k": 0,
                               "frequency_MHz": float(nu), "matrix_element_abs": float(abs(z)),
                               "rate_per_us": float(f.KAPPA * abs(z) ** 2)}
    pair_r1 = route_records["e1_n2_to_e1_n1"]["rate_per_us"]
    pair_r2 = route_records["h0_to_e1_n1"]["rate_per_us"]
    return make_model(grouped), make_model(split), {
        "G_MHz": float(g), "epsilon_MHz": float(epsilon), "omega_MHz": float(omega),
        "rf_frequency_MHz": float(7153.0 - omega + rf_detuning),
        "rf_detuning_MHz": float(rf_detuning), "higher_level_b_bath_scale_per_us": float(calibration[2]["bath_scale"]),
        "frequency_cluster_width_cap_MHz": float(tolerance_mhz),
        "channel_cluster_summary": cluster_summary,
        "grouped_channel_count": int(sum(len(chs) for chs in grouped.values())),
        "split_channel_count": int(sum(len(chs) for chs in split.values())),
        "matched_logical_carriers_n1_k0": logical_lines,
        "matched_gf_carrier_separation_MHz": float(logical_delta),
        "shared_target_dressed_pair_routes": {
            **route_records,
            "frequency_gap_MHz": float(abs(route_records["e1_n2_to_e1_n1"]["frequency_MHz"] - route_records["h0_to_e1_n1"]["frequency_MHz"])),
            "clustered_together_at_1MHz": bool(abs(route_records["e1_n2_to_e1_n1"]["frequency_MHz"] - route_records["h0_to_e1_n1"]["frequency_MHz"]) <= tolerance_mhz),
            "grouped_jump_cross_amplitude_per_us": float(math.sqrt(pair_r1 * pair_r2)),
            "grouped_jump_normalized_visibility": float(2 * math.sqrt(pair_r1 * pair_r2) / (pair_r1 + pair_r2)),
        },
        "h0_vacuum_a_k0_line_pair": {
            "h0_to_e1": h_e, "h0_to_f0": h_f,
            "frequency_gap_MHz": float(abs(h_e["frequency_MHz"] - h_f["frequency_MHz"])),
            "rate_cross_amplitude_per_us": float(math.sqrt(r1 * r2)),
            "normalized_jump_coherence_abs": float(math.sqrt(r1 * r2) / (r1 + r2)),
            "normalized_jump_visibility": float(2 * math.sqrt(r1 * r2) / (r1 + r2)),
        },
        "vacuum_channels": vacuum,
        "maximum_unrepresented_loss_per_us": float(outside.max()),
        "current_sol01_script_sha256": hashlib.sha256((SOL01 / "pair_fluorescence_test.py").read_bytes()).hexdigest(),
    }


def main():
    started = time.perf_counter()
    merged, resolved, diagnostics = build_models(tolerance_mhz=1.0)
    params = {"eta": 0.5, "amplitude_MHz": 4.0, "flat_us": 1.0,
              "ramp_us_each": 0.1, "tail_us": 0.8, "ramp_segments_each": 6,
              "modulation_MHz": 10.0, "modulation_steps_per_period": 12,
              "maxcount": 4, "partial_secular_tolerance_MHz": 1.0}
    print("running source grouped-harmonic schedule", flush=True)
    base = pair.run(merged, params["eta"], params["amplitude_MHz"], params["flat_us"],
                    params["ramp_us_each"], params["tail_us"], params["ramp_segments_each"],
                    params["maxcount"], params["modulation_MHz"], params["modulation_steps_per_period"])
    print("running split-frequency partial-secular schedule", flush=True)
    control = pair.run(resolved, params["eta"], params["amplitude_MHz"], params["flat_us"],
                       params["ramp_us_each"], params["tail_us"], params["ramp_segments_each"],
                       params["maxcount"], params["modulation_MHz"], params["modulation_steps_per_period"])
    _, ancilla = controls.ancilla_cycle(2.0)
    selected_base = base["count_threshold_cases"][0]
    selected_control = control["count_threshold_cases"][0]
    result = {
        "status": "PARTIAL_SECULAR_FREQUENCY_GROUPING_SENSITIVITY_CHECK",
        "model_scope": (
            "Frequency-resolved partial-secular control, not a device bath model. The parent grouped-harmonic model is also a legitimate white-Markov "
            "input-output scenario. Distinguishing physical bath spectra, coherent RF sidebands, detector bandwidth, and full driven Floquet treatment remain unacquired."),
        "parameters": params,
        "diagnostics": diagnostics,
        "grouped_harmonic_result": base,
        "split_frequency_result": control,
        "same_duration_ancilla_comparator": ancilla,
        "threshold_one_comparison": {
            "grouped_harmonic_accepted_Choi_infidelity": selected_base["accepted_Choi_infidelity"],
            "split_frequency_accepted_Choi_infidelity": selected_control["accepted_Choi_infidelity"],
            "difference_split_minus_grouped": selected_control["accepted_Choi_infidelity"] - selected_base["accepted_Choi_infidelity"],
            "same_2us_ancilla_accepted_Choi_infidelity": ancilla["metrics"]["accepted_Choi_infidelity"],
            "split_minus_ancilla": selected_control["accepted_Choi_infidelity"] - ancilla["metrics"]["accepted_Choi_infidelity"],
            "grouped_minus_ancilla": selected_base["accepted_Choi_infidelity"] - ancilla["metrics"]["accepted_Choi_infidelity"],
        },
        "runtime_seconds": time.perf_counter() - started,
    }
    out = HERE / "SPLIT_FREQUENCY_CONTROL_RESULTS.json"
    out.write_text(json.dumps(result, indent=2, default=lambda z: z.real if isinstance(z, complex) else str(z)) + "\n")
    print(json.dumps(result["threshold_one_comparison"], indent=2), flush=True)
    print(json.dumps({"runtime_seconds": result["runtime_seconds"], "output": str(out)}, indent=2), flush=True)


if __name__ == "__main__":
    main()
