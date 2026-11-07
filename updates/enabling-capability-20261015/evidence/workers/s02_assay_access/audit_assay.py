#!/usr/bin/env python3
"""Reproduce scoped numerical audits from acquired primary experimental data.

No chemistry is executed. Isotope values are transcribed from Kozlowski SI S35
and Code S2. NMR observations and incumbent outputs are acquired source files.
HPLC comparison uses published manual-calibration reference yields, not a new
independent determination of the same samples.
"""
from pathlib import Path
import itertools
import hashlib
import json
import re
import time
import math
import csv
import numpy as np
from scipy.optimize import nnls

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def isotope_audit():
    # Columns [D]2a,[D]2b,[D]2c; isotope-fingerprint percentages from Code S2.
    p = np.array([[.4478, .1961, 20.625], [50.118, 22.384, 86.974],
                  [100., 90.695, 100.], [19.938, 100., 19.164],
                  [2.0508, 14.733, 1.8829]])
    p /= p.sum(axis=0)
    # Actual triplicate base-peak-normalized loop-injection observations, SI S35.
    obs = np.array([[9.19, 59.07, 100., 46.47, 6.31],
                    [9.19, 59.18, 100., 46.28, 6.32],
                    [9.16, 59.28, 100., 46.48, 6.32]])
    # Printed average is the quantity used in the source table.
    y = np.array([9.18, 59.18, 100., 46.41, 6.32])
    coef = np.linalg.lstsq(np.column_stack([np.ones(5), p]), y, rcond=None)[0]
    reconstructed = coef[1:] / coef[1:].sum()
    printed = np.array([.201, .337, .462])
    reference = np.array([.208, .427, .365])
    response = np.array([1.16, 1., 1.54])
    corrected = printed / response
    corrected /= corrected.sum()
    sensitivity = []
    for da, dc in itertools.product([-1, 1], repeat=2):
        r = response + np.array([da * .02, 0., dc * .07])
        q = printed / r
        sensitivity.append(q / q.sum())
    # Elementary exact gauge: every positive composition q is compatible with
    # the same response-weighted isotope spectrum by changing unknown response.
    n1 = reconstructed
    n2 = np.array([.20, .60, .20])
    rho1 = np.ones(3)
    rho2 = n1 / n2
    a = p @ (rho1 * n1)
    b = p @ (rho2 * n2)
    assert np.max(np.abs(a - b)) < 1e-14
    assert np.max(np.abs(reconstructed - printed)) < .001
    return {
        "source": "oc4c01765_si_001.pdf S35, Figure S6 and Table S1; Code S2",
        "structures": ["[D]2a", "[D]2b", "[D]2c"],
        "triplicate_measured_channels": obs.tolist(),
        "isotope_matrix_rank": int(np.linalg.matrix_rank(p)),
        "ols_intercept": float(coef[0]),
        "replayed_ols_response_fractions": reconstructed.tolist(),
        "source_printed_ols_fractions": printed.tolist(),
        "qNMR_calibrated_UV_reference_fractions": reference.tolist(),
        "uncorrected_max_fraction_error_pp": float(100 * max(abs(printed-reference))),
        "measured_MS_response_factors": response.tolist(),
        "response_factors_require_isolated_target_standards": True,
        "response_corrected_fractions": corrected.tolist(),
        "corrected_max_fraction_error_pp": float(100 * max(abs(corrected-reference))),
        "response_one_reported_SD_corner_range": {
            "min": np.min(sensitivity, axis=0).tolist(),
            "max": np.max(sensitivity, axis=0).tolist(),
            "scope": "Sensitivity only; source standard deviations do not define a coverage interval."
        },
        "gauge_counterexample": {
            "mole_fractions_model_1": n1.tolist(),
            "response_model_1": rho1.tolist(),
            "mole_fractions_model_2": n2.tolist(),
            "response_model_2": rho2.tolist(),
            "max_observation_difference": float(max(abs(a-b))),
            "scope": "Constructed mathematical countermodels, not extra physical observations."
        },
        "scope": "Mole fractions only; absolute reaction yield needs a total-mole scale. Vendor raw bytes acquired separately but not decoded here."
    }


def nmr_audit():
    repo = next((ROOT / "magnetstein_repository").iterdir())
    config = json.loads((repo / "config.json").read_text())
    folder = repo / "experiment_10_bcaa"
    rows = []
    for i in range(1, 5):
        mixfile = folder / f"preprocessed_mix_variant_{i}.csv"
        mix = np.loadtxt(mixfile, delimiter=",")
        compfiles = [folder / f"preprocessed_variant_{i}_comp{j}.csv" for j in range(3)]
        comps = [np.loadtxt(f, delimiter=",") for f in compfiles]
        assert all(np.array_equal(c[:, 0], mix[:, 0]) for c in comps)
        matrix = np.column_stack([c[:, 1] for c in comps])
        t0 = time.perf_counter()
        coef, residual = nnls(matrix, mix[:, 1])
        elapsed = time.perf_counter() - t0
        q = coef / np.array([10., 10., 8.])
        q /= q.sum()
        truth = np.array(config["ground_truth_molar_proportions"]["experiment_10"][i-1])
        incumbent_file = folder / f"results_concentration_default_parameters_variant_{i}.csv"
        incumbent = np.loadtxt(incumbent_file, delimiter=",", skiprows=1)[1:]
        rows.append({
            "mixture": i, "channels_after_source_preprocessing": len(mix),
            "high_field_NMR_reference_fractions": truth.tolist(),
            "replayed_ordinary_NNLS_fractions": q.tolist(),
            "nnls_max_target_fraction_error_pp": float(100 * max(abs(q-truth))),
            "nnls_wall_seconds": elapsed,
            "archived_Magnetstein_default_fractions": incumbent.tolist(),
            "magnetstein_max_target_fraction_error_pp": float(100 * max(abs(incumbent-truth))),
            "incumbent_reexecuted": False,
            "nnls_uses_purified_component_library": True,
            "inputs_sha256": {f.name: digest(f) for f in [mixfile, *compfiles, incumbent_file]}
        })
    import nmrglue as ng
    fidpath = ROOT / "magnetstein_data/Article_data/MANIQ_and_ACD_TP_project_files_and_raw_mixture_data/Exp_2/1H_limonene_pinene_CDCl3_2.fid"
    header, signal = ng.varian.read(str(fidpath))
    assert np.isfinite(signal).all()
    raw = {
        "file": str(fidpath / "fid"), "sha256": digest(fidpath / "fid"),
        "complex_samples": int(signal.size), "dtype": str(signal.dtype),
        "nonzero_samples": int(np.count_nonzero(signal)),
        "acquisition_parameters": {k: header["procpar"].get(k, {}).get("values")
                                   for k in ["sfrq", "sw", "np", "nt", "d1", "at", "pw"]},
        "scope": "Actual raw FID decoded and checked finite; no new NMR measurement or raw-to-reference reintegration claimed."
    }
    return {
        "source": "Magnetstein publication 10.1021/acs.analchem.3c03594; data commit 72df0be7820e851a3b971722ebd1bf168bf3e890",
        "targets": ["Leucine", "Isoleucine", "Valine"],
        "truth_provenance": "Resolved-peak integration in complementary high-field NMR; not claimed gravimetric truth. Source does not provide reference uncertainty here.",
        "actual_low_field_observations": True,
        "raw_BCAA_FID_in_acquired_Zenodo_archive": False,
        "raw_high_field_FID_decode": raw,
        "comparisons": rows,
        "scope": "Four public composition examples. Both compared methods receive pure measured component spectra. No standards-free capability or absolute yield benchmark."
    }


def hplc_audit():
    data = ROOT / "MCDONALD_FIGURE_ROWS.json"
    if not data.exists():
        return {"status": "NOT_ACQUIRED"}
    rows = json.loads(data.read_text())["Figure4_data.xlsx:Sheet1"]
    numeric = [r for r in rows[1:] if isinstance(r[2], (int, float))
               and isinstance(r[3], (int, float)) and re.fullmatch(r"[A-H][0-9]+", str(r[1]))]
    manual = np.array([r[2] for r in numeric])
    auto = np.array([r[3] for r in numeric])
    e = auto-manual
    rawfolder = ROOT / "mcdonald_data/reaction_set_1"
    raw_coverage = {plate: sum(r[0] == plate for r in numeric) for plate in sorted({r[0] for r in numeric})}
    pda = next(f for f in rawfolder.glob("PDA*.txt")
               if "\\A5.lcd" in f.read_text()[:1000])
    lines = pda.read_text().splitlines()
    start = next(i for i, line in enumerate(lines) if len(line) > 200)
    wavelengths = np.array([float(s)/100 for s in lines[start].split(",")[1:]])
    matrix = np.array([[float(s) for s in r] for r in csv.reader(lines[start+1:]) if r])
    assert matrix.shape == (751, 497) and np.isfinite(matrix).all()
    a5 = next(r for r in numeric if r[0] == "plate_1" and r[1] == "A5")
    return {
        "source": "McDonald et al. 10.1039/D4SC01881H; Zenodo10845991 Figure4_data.xlsx columns C and D",
        "rows_with_manual_and_automated_yields": len(numeric),
        "reference_rows_by_source_plate": raw_coverage,
        "raw_archive_acquired": "reaction_set_1 only; reaction_set_2 not acquired",
        "A5_endpoint_example": {
            "source_figure_table_manual_yield": a5[2],
            "source_figure_table_automated_yield": a5[3],
            "abs_yield_error_pp": 100*abs(a5[3]-a5[2]),
            "PDA_file": str(pda), "PDA_sha256": digest(pda),
            "PDA_numeric_shape": list(matrix[:,1:].shape),
            "wavelength_min_nm": float(wavelengths.min()),
            "wavelength_max_nm": float(wavelengths.max()),
            "scope": "Decoded actual PDA observation matrix; source assigned target identity and source manual calibration are supplied, not independently regenerated."
        },
        "manual_reference_provenance": "Calibrated HPLC against pure authentic target references, per primary paper; no independent raw recalibration executed here.",
        "yield_MAE_pp": float(100 * np.mean(abs(e))),
        "yield_RMSE_pp": float(100 * np.sqrt(np.mean(e*e))),
        "yield_max_abs_error_pp": float(100 * max(abs(e))),
        "reference_yields_above_100_percent": int(sum(manual > 1)),
        "prediction_yields_above_100_percent": int(sum(auto > 1)),
        "coeluting_isomer_transfer": "UNSUPPORTED. Paper explicitly states it cannot differentiate isomers/isobars; reference sample needed to assign the two amination isomers in Reaction 2.",
        "model_transfer": "Primary paper used a proprietary Reaxys 38k model; archive supplies Deep4Chem model. Published values are not a replay of the supplied public model.",
        "scope": "Recomputed published endpoint errors; no new ML predictions or chemistry."
    }


def crude_relaxation_audit():
    source = ROOT / "KOZLOWSKI_CRUDE_FID_METADATA.json"
    metadata = json.loads(source.read_text()) if source.exists() else []
    # Illustrative steady-state recovery of a 30 degree single-pulse experiment.
    # This uses hypothetical T1 values, not measured relaxation data.
    examples = []
    aq = 65536/(2*8196.722)
    for d1 in [1., 20.]:
        tr = d1+aq
        factors = {}
        for t1 in [1., 5., 10., 20.]:
            e = math.exp(-tr/t1)
            factors[str(t1)] = (1-e)/(1-math.cos(math.pi/6)*e)
        examples.append({"D1_seconds": d1, "minimum_repetition_seconds": tr,
                         "hypothetical_T1_seconds_to_recovery": factors})
    return {"acquired_raw_metadata": metadata,
            "caption_claim": "600 MHz for SI Figures S136-S138",
            "resolution": "UNRESOLVED: archived crude FIDs are 400.172 MHz; possible caption error or different deposited acquisition cannot be chosen from present evidence.",
            "relaxation_examples": examples,
            "scope": "D1 alone does not establish invalidity: acquisition time is approximately 3.998s and pulse is 30 degrees. Unequal T1 can bias target/reference ratios. Need measured or defensible T1 bounds, actual acquisition identity, and reference integration uncertainty."}


if __name__ == "__main__":
    results = {"isotope": isotope_audit(), "nmr": nmr_audit(), "hplc": hplc_audit(),
               "crude_reference_provenance": crude_relaxation_audit()}
    out = ROOT / "ASSAY_AUDIT_RESULTS.json"
    out.write_text(json.dumps(results, indent=2))
    print(json.dumps({
        "output": str(out),
        "isotope_OLS_max_error_pp": results["isotope"]["uncorrected_max_fraction_error_pp"],
        "isotope_after_standard_response_correction_max_error_pp": results["isotope"]["corrected_max_fraction_error_pp"],
        "nmr_examples": len(results["nmr"]["comparisons"]),
        "hplc_rows": results["hplc"].get("rows_with_manual_and_automated_yields"),
        "hplc_MAE_pp": results["hplc"].get("yield_MAE_pp")
    }, indent=2))
