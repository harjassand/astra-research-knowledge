"""Finite sanity checks for the unknown-field archive derivation.

These are not theorem certificates. They exercise envelope coarsening on
irregular sector laws and the exact engineered Gibbs-sector example.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def log_sinhc(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    out = np.zeros_like(x)
    small = (x > 0) & (x < 1e-3)
    out[small] = np.log1p(x[small] ** 2 / 6 + x[small] ** 4 / 120)
    mid = (x >= 1e-3) & (x <= 20)
    out[mid] = np.log(np.sinh(x[mid]) / x[mid])
    big = x > 20
    out[big] = x[big] - np.log(2 * x[big]) + np.log1p(-np.exp(-2 * x[big]))
    return out


def log_weights(j: np.ndarray, t: float) -> np.ndarray:
    return log_sinhc((j + 0.5) * t) - log_sinhc(np.array(t / 2))


def normalize(log_mass: np.ndarray) -> np.ndarray:
    p = np.exp(log_mass - np.max(log_mass))
    return p / p.sum()


def sector_law(j: np.ndarray, log_q0: np.ndarray, t: float) -> np.ndarray:
    return normalize(log_q0 + log_weights(j, t))


def score(j: np.ndarray, t: float) -> np.ndarray:
    if t == 0:
        return np.zeros_like(j)
    x = (j + 0.5) * t
    y = t / 2
    xcth = np.empty_like(x)
    tiny = x < 1e-3
    xcth[tiny] = 1 + x[tiny] ** 2 / 3 - x[tiny] ** 4 / 45
    xcth[~tiny] = x[~tiny] / np.tanh(x[~tiny])
    ycth = 1 + y**2 / 3 - y**4 / 45 if y < 1e-3 else y / np.tanh(y)
    return (xcth - ycth) / t


def mass_bins(h: np.ndarray, delta: float) -> list[np.ndarray]:
    bins = []
    pending = []
    mass = 0.0
    for i, atom in enumerate(h):
        if atom > delta:
            if pending:
                bins.append(np.array(pending, dtype=int))
                pending, mass = [], 0.0
            bins.append(np.array([i]))
        elif pending and mass + atom > delta:
            bins.append(np.array(pending, dtype=int))
            pending, mass = [i], float(atom)
        else:
            pending.append(i)
            mass += float(atom)
    if pending:
        bins.append(np.array(pending, dtype=int))
    return bins


def radial_refinement(bins: list[np.ndarray], j: np.ndarray, R: float, eta: float):
    log_id = np.floor(np.log1p(2 * R * j) / eta).astype(int)
    refined = []
    for B in bins:
        for k in np.unique(log_id[B]):
            refined.append(B[log_id[B] == k])
    return refined, len(np.unique(log_id))


def coherent_density(j: np.ndarray, t: float, x: np.ndarray) -> np.ndarray:
    natural = np.cosh(t / 2) + np.sinh(t / 2) * x
    return np.exp(2 * j[:, None] * np.log(natural)[None, :] - log_weights(j, t)[:, None])


def irregular_laws():
    rng = np.random.default_rng(712047)
    j = np.arange(56, dtype=float)
    V, S = 110, 0.5
    x, quad = np.polynomial.legendre.leggauss(180)
    quad /= 2
    delta, eta = 0.04, 0.04
    records = []
    for case in range(16):
        R = [0.005, 0.03, 0.15, 0.75][case % 4]
        log_q0 = rng.normal(0, 8, len(j))
        if case == 1:
            log_q0 = np.zeros_like(j)
        if case % 3 == 0:
            # Disconnected-looking peaks and rare high-spin mass.
            log_q0 -= 0.03 * j**2
            log_q0[-1] += 15
        ts = np.linspace(0, R, 501)
        laws = np.stack([sector_law(j, log_q0, float(t)) for t in ts])
        # A discrete parameter envelope is sufficient for these grid fixtures.
        h = laws.max(axis=0)
        H = h.sum()
        H_bound = 1 + 0.5 * np.sqrt(S * V * R)
        assert H <= H_bound + 1e-10
        endpoint_response = float(R * ((laws[-1] - laws[0]) @ j))
        endpoint_envelope_bound = 1 + 0.5 * np.sqrt(max(0, endpoint_response))
        assert H <= endpoint_envelope_bound + 1e-10
        bins = mass_bins(h, delta)
        assert len(bins) <= 2 * H / delta + 2
        for B in bins:
            assert len(B) == 1 or h[B].sum() <= delta + 1e-14
        refined, n_log = radial_refinement(bins, j, R, eta)
        assert len(refined) <= len(bins) + n_log - 1
        max_radial_tv = max_raw_radial_tv = max_joint_tv = max_quotient_variation = 0.0
        for idx in np.linspace(0, len(ts) - 1, 31).astype(int):
            t = float(ts[idx])
            p = laws[idx]
            s = score(j, t)
            assert np.min(np.diff(s)) >= -1e-10
            assert np.max(np.diff(s)) <= 1 + 1e-10
            centered_s = s - p @ s
            fisher = float(p @ centered_s**2)
            sector_response_derivative = float(p @ ((j - p @ j) * centered_s))
            assert fisher <= sector_response_derivative + 1e-8
            g = p / h
            variation = np.abs(np.diff(g)).sum()
            assert variation <= 2 + 1e-10
            max_quotient_variation = max(max_quotient_variation, float(variation))
            raw_radial = np.empty_like(p)
            for B in bins:
                raw_radial[B] = h[B] * p[B].sum() / h[B].sum()
            raw_radial_tv = 0.5 * np.abs(p - raw_radial).sum()
            assert raw_radial_tv <= delta + 1e-10
            max_raw_radial_tv = max(max_raw_radial_tv, float(raw_radial_tv))
            radial = np.empty_like(p)
            for B in refined:
                radial[B] = h[B] * p[B].sum() / h[B].sum()
            radial_tv = 0.5 * np.abs(p - radial).sum()
            assert radial_tv <= delta + 1e-10
            max_radial_tv = max(max_radial_tv, float(radial_tv))
            f = coherent_density(j, t, x)
            assert np.max(np.abs(f @ quad - 1)) < 1e-9
            measured = p[:, None] * f
            coarsened = np.empty_like(measured)
            for B in refined:
                coarsened[B] = (h[B] / h[B].sum())[:, None] * measured[B].sum(axis=0)[None, :]
            joint_tv = 0.5 * (np.abs(measured - coarsened) @ quad).sum()
            assert joint_tv <= delta + eta + 1e-8
            max_joint_tv = max(max_joint_tv, float(joint_tv))
        records.append(dict(
            case=case, V=V, R=R, envelope_mass=float(H), envelope_bound=float(H_bound),
            endpoint_response=endpoint_response,
            endpoint_envelope_bound=endpoint_envelope_bound,
            raw_bins=len(bins), logarithmic_bins=n_log, refined_bins=len(refined),
            max_quotient_variation=max_quotient_variation,
            max_raw_radial_tv=max_raw_radial_tv,
            max_radial_tv=max_radial_tv, radial_bound=delta,
            max_joint_tv=max_joint_tv, joint_bound=delta + eta,
        ))
    return records


def engineered_laws():
    records = []
    m = c = 0.125
    for V, R in [(8192, 1 / 16), (32768, 1 / 32), (131072, 1 / 64)]:
        j = np.arange(V // 2 + 1, dtype=float)
        A = V * R
        sigma2 = c * V / R
        log_q0 = np.log(2 * j + 1) - (j - m * V) ** 2 / (2 * sigma2)
        q0 = normalize(log_q0)
        field_records = []
        for fraction in [0.25, 0.5, 0.75]:
            t = fraction * R
            p = sector_law(j, log_q0, t)
            mu = m * V + sigma2 * t
            gauss = normalize(-(j - mu) ** 2 / (2 * sigma2))
            tv = 0.5 * np.abs(p - gauss).sum()
            moment = p @ (j - mu) ** 2
            assert moment <= 2 * sigma2
            assert tv < 1e-5
            field_records.append(dict(
                fraction=fraction, mean=float(p @ j), predicted_mean=mu,
                gaussian_tv=float(tv), variance_ratio=float(moment / sigma2),
                low_spin_mass=float(p[j < m * V / 2].sum()),
                chebyshev_radial_error_bound=2 / 16**2,
            ))
        h = np.zeros_like(j)
        for t in np.linspace(0, R, 301):
            h = np.maximum(h, sector_law(j, log_q0, float(t)))
        records.append(dict(
            V=V, R=R, A=A, sigma=float(np.sqrt(sigma2)),
            zero_field_mean_over_V=float(q0 @ j / V),
            zero_field_sd_over_V=float(np.sqrt(q0 @ (j - q0 @ j) ** 2) / V),
            grid_envelope_mass=float(h.sum()),
            envelope_over_sqrt_A=float(h.sum() / np.sqrt(A)),
            fields=field_records,
        ))
    return records


def main():
    report = {
        "status": "finite sanity fixtures passed; not theorem certification",
        "seed": 712047,
        "irregular_sector_laws": irregular_laws(),
        "engineered_gaussian_sector_laws": engineered_laws(),
    }
    path = Path(__file__).with_name("unknown_field_checks.json")
    path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({
        "status": report["status"],
        "irregular_law_count": len(report["irregular_sector_laws"]),
        "engineered_law_count": len(report["engineered_gaussian_sector_laws"]),
        "max_checked_radial_tv": max(x["max_radial_tv"] for x in report["irregular_sector_laws"]),
        "max_checked_raw_radial_tv": max(x["max_raw_radial_tv"] for x in report["irregular_sector_laws"]),
        "max_checked_joint_tv": max(x["max_joint_tv"] for x in report["irregular_sector_laws"]),
        "report": str(path),
    }, indent=2))


if __name__ == "__main__":
    main()
