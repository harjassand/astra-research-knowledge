"""Conventional two-component GLS/NNLS comparator; no chemistry data bundled.

This is a comparator component, not a new assay or a validation result. Its
confidence bounds condition on a fixed correct calibration matrix and known
noise covariance. It does not claim calibration-uncertainty coverage.

Run with an independently acquired measured-data NPZ and provenance JSON:
  python conditional_gls_nnls.py measured.npz provenance.json output.json

NPZ keys:
  wavelength_nm (m,), response_matrix (m,2), mixture_spectra (n,m),
  covariance (m,m) or (n,m,m), truth_concentrations (n,2).
Optional key: nuisance_matrix (m,q), fixed before observing test truth.
Concentrations and calibration columns must use the same declared units.
NPZ loading forbids object/pickle arrays. No synthetic inputs are generated.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import sys
import time

import numpy as np


CHI2_2_95 = 5.991464547107979


def whiten_and_project(A, y, covariance, nuisance=None):
    A = np.asarray(A, dtype=float)
    y = np.asarray(y, dtype=float)
    covariance = np.asarray(covariance, dtype=float)
    if A.ndim != 2 or A.shape[1] != 2 or y.shape != (A.shape[0],):
        raise ValueError("Two aligned calibration columns and one spectrum required")
    if covariance.shape != (len(y), len(y)):
        raise ValueError("Noise covariance has wrong shape")
    if not all(np.isfinite(z).all() for z in [A, y, covariance]):
        raise ValueError("Non-finite measurement or calibration")
    if not np.allclose(covariance, covariance.T, rtol=1e-10, atol=1e-12):
        raise ValueError("Noise covariance is not symmetric")
    L = np.linalg.cholesky(covariance)
    Aw, yw = np.linalg.solve(L, A), np.linalg.solve(L, y)
    nuisance_rank = 0
    if nuisance is not None:
        nuisance = np.asarray(nuisance, dtype=float)
        if nuisance.ndim != 2 or nuisance.shape[0] != len(y):
            raise ValueError("Nuisance columns have wrong shape")
        if not np.isfinite(nuisance).all():
            raise ValueError("Non-finite nuisance columns")
        Nw = np.linalg.solve(L, nuisance)
        U, singular, _ = np.linalg.svd(Nw, full_matrices=False)
        tolerance = max(Nw.shape) * np.finfo(float).eps * singular[0] if len(singular) else 0
        nuisance_rank = int(np.sum(singular > tolerance))
        Q = U[:, :nuisance_rank]
        Aw, yw = Aw - Q @ (Q.T @ Aw), yw - Q @ (Q.T @ yw)
    singular = np.linalg.svd(Aw, compute_uv=False)
    tolerance = max(Aw.shape) * np.finfo(float).eps * singular[0]
    if singular[-1] <= tolerance:
        raise ValueError("Calibration is rank deficient after nuisance projection")
    return Aw, yw, singular, nuisance_rank


def fit_nonnegative_two(Aw, yw):
    """Globally solve the two-variable convex NNLS problem by active sets."""
    best = None
    for size in range(3):
        for active in itertools.combinations(range(2), size):
            c = np.zeros(2)
            if active:
                ca = np.linalg.lstsq(Aw[:, active], yw, rcond=None)[0]
                if np.any(ca < 0):
                    continue
                c[list(active)] = ca
            residual = yw - Aw @ c
            loss = float(residual @ residual)
            if best is None or loss < best[0]:
                best = (loss, c)
    return best


def conditional_joint_bounds(Aw, yw, c_hat, min_loss, cutoff=CHI2_2_95):
    """Coordinate projections of a conservative 95% joint confidence set.

    With fixed full-rank A and Gaussian noise of *known* covariance, the set
    {c>=0: SSE(c)-SSE(c_hat)<=chi2_2(.95)} has at least 95% joint coverage.
    Nuisance coefficients have already been profiled out. These assumptions
    are essential; estimated covariance/calibration do not inherit the claim.
    """
    level = min_loss + cutoff

    def profile(x, j):
        other = 1 - j
        partial = yw - x * Aw[:, j]
        denom = float(Aw[:, other] @ Aw[:, other])
        z = max(0.0, float(Aw[:, other] @ partial) / denom)
        residual = partial - z * Aw[:, other]
        return float(residual @ residual)

    bounds = []
    for j in range(2):
        center = float(c_hat[j])
        if profile(0.0, j) <= level:
            low = 0.0
        else:
            left, right = 0.0, center
            for _ in range(100):
                mid = (left + right) / 2
                if profile(mid, j) <= level:
                    right = mid
                else:
                    left = mid
            low = right
        scale = np.sqrt(cutoff) / np.linalg.norm(Aw[:, j])
        left, right = center, center + max(scale, abs(center), np.finfo(float).tiny)
        for _ in range(1024):
            if profile(right, j) > level:
                break
            right = center + 2 * (right - center)
        else:
            raise ValueError("Could not bracket finite concentration bound")
        for _ in range(100):
            mid = (left + right) / 2
            if profile(mid, j) <= level:
                left = mid
            else:
                right = mid
        bounds.append([float(low), float(right)])
    return bounds


def main(argv):
    if len(argv) != 4:
        print(json.dumps({
            "status": "NOT_EXECUTED_MISSING_MEASURED_INPUTS",
            "required": ["measured.npz", "provenance.json", "output.json"],
            "scientific_validation": "NOT_ESTABLISHED",
        }, indent=2))
        return 2
    data_path, metadata_path, output_path = map(Path, argv[1:])
    metadata = json.loads(metadata_path.read_text())
    required = ["measurement_origin", "concentration_unit", "calibration_provenance",
                "mixture_provenance", "truth_method", "truth_provenance", "sample_ids"]
    if any(not metadata.get(k) for k in required):
        raise ValueError("Missing measured-data provenance contract")
    if metadata["measurement_origin"] != "measured":
        raise ValueError("This benchmark accepts acquired measurements only")
    if metadata["truth_method"] in {"source_deconvolution", "model_prediction", "synthetic"}:
        raise ValueError("Independent mixture truth is required")
    start = time.perf_counter()
    with np.load(data_path, allow_pickle=False) as data:
        A = np.asarray(data["response_matrix"], float)
        Y = np.asarray(data["mixture_spectra"], float)
        truth = np.asarray(data["truth_concentrations"], float)
        covariance = np.asarray(data["covariance"], float)
        wavelength = np.asarray(data["wavelength_nm"], float)
        nuisance = np.asarray(data["nuisance_matrix"], float) if "nuisance_matrix" in data else None
    if Y.ndim != 2 or Y.shape[1] != len(wavelength) or A.shape != (len(wavelength), 2):
        raise ValueError("Wavelength/grid alignment failed")
    if truth.shape != (len(Y), 2) or not np.isfinite(truth).all() or np.any(truth < 0):
        raise ValueError("Independent truth shape/values invalid")
    if len(metadata["sample_ids"]) != len(Y):
        raise ValueError("Sample provenance does not align")
    if not np.isfinite(wavelength).all() or np.any(np.diff(wavelength) <= 0):
        raise ValueError("Wavelength grid must be finite and increasing")
    if covariance.shape not in {(len(wavelength), len(wavelength)),
                                (len(Y), len(wavelength), len(wavelength))}:
        raise ValueError("Covariance shape invalid")
    rows = []
    for i, y in enumerate(Y):
        sigma = covariance if covariance.ndim == 2 else covariance[i]
        Aw, yw, singular, rank = whiten_and_project(A, y, sigma, nuisance)
        loss, estimate = fit_nonnegative_two(Aw, yw)
        intervals = conditional_joint_bounds(Aw, yw, estimate, loss)
        source_ols = np.linalg.lstsq(A, y, rcond=None)[0]
        rows.append({
            "sample_id": metadata["sample_ids"][i],
            "source_form_unweighted_ols": source_ols.tolist(),
            "gls_nnls": estimate.tolist(),
            "independent_truth": truth[i].tolist(),
            "conditional_joint_95_bounds": intervals,
            "whitened_condition_number": float(singular[0] / singular[-1]),
            "noise_weighted_sse": loss,
            "nuisance_rank": rank,
        })
    ols = np.array([r["source_form_unweighted_ols"] for r in rows])
    fit = np.array([r["gls_nnls"] for r in rows])
    output = {
        "status": "MEASURED_BENCHMARK_EXECUTED_PROVENANCE_REQUIRES_REVIEW",
        "concentration_unit": metadata["concentration_unit"],
        "source_sha256": hashlib.sha256(data_path.read_bytes()).hexdigest(),
        "provenance_sha256": hashlib.sha256(metadata_path.read_bytes()).hexdigest(),
        "comparison_scope": "same acquired integrated spectra and fixed standard responses",
        "full_raw_pipeline_comparison": False,
        "calibration_uncertainty_included": False,
        "conditional_bounds_assume_known_covariance_and_correct_fixed_calibration": True,
        "rmse_by_component": {
            "source_form_unweighted_ols": np.sqrt(np.mean((ols - truth) ** 2, axis=0)).tolist(),
            "gls_nnls": np.sqrt(np.mean((fit - truth) ** 2, axis=0)).tolist(),
        },
        "wall_seconds": time.perf_counter() - start,
        "rows": rows,
    }
    output_path.write_text(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
