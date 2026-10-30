#!/usr/bin/env python3
"""Forward-only finite-ADC identification on a passive persistent specimen.

The controller receives only signs, quantized reports, saturation flags and
calibrations. Hidden-state quantities are used only for a separate audit.
Run with Python 3 and numpy. All generated files stay beside this script.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent


def rotation(theta):
    c, s = math.cos(theta), math.sin(theta)
    return np.array([[c, -s], [s, c]])


class PassivePlant:
    """An orthogonal scattering colligation, with an unchanged dark mode.

    x' = diag(rho) x + diag(tau) U u
    y  = V [diag(tau) x - diag(rho) U u], tau^2 + rho^2 = 1.
    Therefore ||x'||^2 + ||y||^2 = ||x||^2 + ||u||^2, pathwise.
    """

    def __init__(self, rho, state, dark=0.0, U=None, V=None):
        self.rho = np.asarray(rho, dtype=float)
        self.tau = np.sqrt(1.0 - self.rho**2)
        self.x = np.asarray(state, dtype=float).copy()
        self.dark = float(dark)
        self.d = len(self.rho)
        self.U = np.eye(self.d) if U is None else U
        self.V = np.eye(self.d) if V is None else V
        self.A = -self.V @ np.diag(self.rho) @ self.U
        self.initial_energy = self.energy()
        self.incident = self.emitted = self.old_field_energy = 0.0
        self.max_balance_residual = 0.0

    def energy(self):
        return float(self.x @ self.x + self.dark**2)

    def step(self, u):
        before = self.energy()
        v = self.U @ u
        w = self.V @ (self.tau * self.x)
        y = self.V @ (self.tau * self.x - self.rho * v)
        self.x = self.rho * self.x + self.tau * v
        incident, emitted = float(u @ u), float(y @ y)
        self.incident += incident
        self.emitted += emitted
        self.old_field_energy += float(w @ w)
        residual = self.energy() + emitted - before - incident
        self.max_balance_residual = max(self.max_balance_residual, abs(residual))
        return y


def adc(y, C, levels, rng):
    """Fresh stochastic rounding AFTER clipping; every flag is retained."""
    delta = 2.0 * C / (levels - 1)
    clipped = np.clip(y, -C, C)
    pos = np.clip((clipped + C) / delta, 0, levels - 1)
    lower = np.floor(pos).astype(int)
    frac = pos - lower
    index = lower + (rng.random(y.shape) < frac)
    return -C + delta * index, np.abs(y) > C


def confidence_record(counts, sum_z, sum_z2, warnings, *, C, r, L, delta, K=20):
    """Joint time-uniform rectangular confidence set; see PROOF.md.

    Fixed eta grid and Ville's inequality permit stopping from this record.
    Clipping attenuates each scalar slope, hence the asymmetric intervals.
    """
    m, d = sum_z.shape
    H = C / r
    eta = np.exp2(-np.arange(K)) / (2.0 * H)
    log_mean = math.log(4.0 * K * m * d / delta)
    log_warning = math.log(2.0 * m * d / delta)
    n = counts[None, :]
    raw = sum_z / n
    mean_error = np.min(
        eta[:, None, None] * sum_z2[None, :, :]
        + log_mean / eta[:, None, None], axis=0
    ) / n
    upper_warning_compensator = (warnings + log_warning) / (1.0 - math.exp(-1.0))
    beta = np.minimum(1.0, 2.0 * upper_warning_compensator / n)
    lo_mean, hi_mean = raw - mean_error, raw + mean_error
    denom = np.maximum(1.0 - beta, np.finfo(float).tiny)
    lo = np.where(lo_mean >= 0.0, lo_mean, lo_mean / denom)
    hi = np.where(hi_mean <= 0.0, hi_mean, hi_mean / denom)
    lo = np.maximum(lo, -L)
    hi = np.minimum(hi, L)
    # beta=1: a nonzero conditional mean still lower-bounds |a|.
    lo = np.where(beta == 1.0, np.where(lo_mean > 0.0, np.maximum(-L, lo_mean), -L), lo)
    hi = np.where(beta == 1.0, np.where(hi_mean < 0.0, np.minimum(L, hi_mean), L), hi)
    if np.any(lo > hi):
        raise RuntimeError("Empty confidence set: calibration inconsistency or confidence failure")
    center, radii = (lo + hi) / 2.0, (hi - lo) / 2.0
    return {
        "raw": raw,
        "center": center,
        "lower": lo,
        "upper": hi,
        "entry_radii": radii,
        # The exact largest spectral norm over an entrywise symmetric box is
        # ||radii||_2: |E x| <= radii |x|, with equality attained by E=radii.
        "operator_error_bound": float(np.linalg.norm(radii, 2)),
        "mean_error": mean_error,
        "beta": beta,
    }


def ridge_task(cert, b, lam, norm_A, radius):
    Ahat = cert["center"]
    u = np.linalg.solve(Ahat.T @ Ahat + lam * np.eye(Ahat.shape[1]), Ahat.T @ b)
    if np.linalg.norm(u) > radius:
        raise RuntimeError("This executable uses an interior fixture; need constrained ridge solver")
    e = cert["operator_error_bound"]
    # Global ridge-map Lipschitz bound. It applies simultaneously to every
    # later b with this norm bound. The skew-block inverse proof is in PROOF.md.
    distance = e * np.linalg.norm(b) / lam
    return u, float(distance)


def run(name, plant, *, r, C, levels, max_per_column, seed, target=None, b=None,
        lam=0.5, command_radius=0.7, delta=0.01, record=False, E0_bound=100.0):
    d = plant.d
    L = 1.0  # calibrated upper bound, NOT read from the hidden population matrix
    rng_sign = np.random.default_rng(seed)
    rng_adc = np.random.default_rng(seed + 100_003)
    counts = np.zeros(d, dtype=int)
    sum_z = np.zeros((d, d))
    sum_z2 = np.zeros((d, d))
    warnings = np.zeros((d, d), dtype=int)
    checkpoints, rows = [], []
    cert, uhat, task_radius = None, None, None
    for t in range(d * max_per_column):
        j = t % d
        sign = 2 * int(rng_sign.integers(2)) - 1
        u = np.zeros(d)
        u[j] = r * sign
        y = plant.step(u)
        q, warning = adc(y, C, levels, rng_adc)
        z = sign * q / r
        counts[j] += 1
        sum_z[:, j] += z
        sum_z2[:, j] += z * z
        warnings[:, j] += warning
        if record:
            rows.append([j, sign, *q.tolist(), *warning.astype(int).tolist()])
        n = int(min(counts))
        if (t + 1) % (d * 512) == 0 or t + 1 == d * max_per_column:
            cert = confidence_record(counts, sum_z, sum_z2, warnings,
                                     C=C, r=r, L=L, delta=delta)
            if b is not None:
                uhat, task_radius = ridge_task(cert, b, lam, L, command_radius)
            checkpoints.append({
                "windows": t + 1, "samples_per_column": n,
                "operator_error_bound": cert["operator_error_bound"],
                "task_distance_radius": task_radius,
                "saturation_flags": int(warnings.sum()),
                "incident_energy": plant.incident,
            })
            if target is not None and task_radius is not None and task_radius < target:
                break
    if cert is None:
        raise RuntimeError("No checkpoint")
    result = {
        "name": name, "seed": seed,
        "calibration": {"probe_radius": r, "ADC_range": C, "ADC_levels": levels,
                        "ADC_step": 2*C/(levels-1), "entry_A_bound": L,
                        "operator_A_bound": L, "joint_anytime_failure_probability": delta,
                        "command_radius": command_radius, "initial_energy_upper_bound": E0_bound},
        "controller": {"counts": counts, "sum_z": sum_z, "sum_z2": sum_z2,
                       "warnings_by_entry": warnings, "confidence": cert,
                       "task_command": uhat, "task_distance_radius": task_radius},
        "physical_cost": {"windows": int(counts.sum()), "active_windows": int(counts.sum()),
                          "zero_input_wait_windows": 0, "hidden_state_resets_after_start": 0,
                          "vector_ADC_reads": int(counts.sum()),
                          "scalar_ADC_reports": int(d*counts.sum()),
                          "saturated_scalar_reports_retained": int(warnings.sum()),
                          "incident_normalized_energy": plant.incident,
                          "adjoint_calls": 0},
        "audit_only": {"A": plant.A, "initial_energy": plant.initial_energy,
                       "final_energy": plant.energy(), "unchanged_dark_energy": plant.dark**2,
                       "emitted_energy": plant.emitted,
                       "exposed_old_field_energy": plant.old_field_energy,
                       "maximum_energy_balance_residual": plant.max_balance_residual,
                       "raw_operator_error": float(np.linalg.norm(cert["raw"]-plant.A, 2)),
                       "center_operator_error": float(np.linalg.norm(cert["center"]-plant.A, 2)),
                       "every_true_entry_in_confidence_interval": bool(np.all(plant.A>=cert["lower"]) and np.all(plant.A<=cert["upper"]))},
        "checkpoints": checkpoints,
    }
    if b is not None:
        true_u = np.linalg.solve(plant.A.T @ plant.A + lam*np.eye(d), plant.A.T @ b)
        result["task"] = {"b": b, "lambda": lam, "requested_radius": target,
                          "zero_command_universal_radius": float(np.linalg.norm(b)/(2*math.sqrt(lam))),
                          "audited_optimum": true_u,
                          "audited_task_error": float(np.linalg.norm(uhat-true_u)),
                          "uniform_radius_for_all_b_of_this_norm_or_smaller": task_radius,
                          "audited_uniform_task_error": float(np.linalg.norm(
                              np.linalg.solve(cert["center"].T @ cert["center"] + lam*np.eye(d), cert["center"].T)
                              -np.linalg.solve(plant.A.T @ plant.A + lam*np.eye(d), plant.A.T), 2)*np.linalg.norm(b))}
    if record:
        np.savez_compressed(OUT / f"{name}_record.npz", reports=np.asarray(rows),
                            C=C, r=r, levels=levels, delta=delta, L=L)
    return result


def algebra_checks():
    x = np.linspace(-0.5, 0.5, 100_001)
    exp_inequality_violation = float(np.max(x-x*x-np.log1p(x)))
    max_defect_violation = 0.0
    for a in np.linspace(-1, 1, 41):
        r, C = 0.12, 0.8
        w = np.linspace(-2.0, 2.0, 40_001)
        yp, ym = w+r*a, w-r*a
        mu = (np.clip(yp,-C,C)-np.clip(ym,-C,C))/(2*r)
        prob_warning = ((np.abs(yp)>C).astype(float)+(np.abs(ym)>C).astype(float))/2
        max_defect_violation = max(max_defect_violation, float(np.max(np.abs(mu-a)-2*abs(a)*prob_warning)))
    return {"max_exp_inequality_violation": exp_inequality_violation,
            "max_clipping_defect_inequality_violation": max_defect_violation}


def deadline_bound(N, r, *, m=2, d=2, E0=100.0, C=0.8, levels=257,
                   L=1.0, delta=0.01, K=20):
    """Deterministic upper bound on the record radius under pathwise passivity.

    The radius is valid with probability 1-delta, simultaneously in time.
    No unknown rate or population matrix is used. See PROOF.md, finite ceiling.
    """
    step = 2*C/(levels-1)
    ell = math.log(4*K*m*d/delta)
    ell_w = math.log(2*m*d/delta)
    H = C/r
    squared_reports_bound = 2*E0/r**2 + 2*d*N + 2*m*d*N*step**2/r**2
    if squared_reports_bound > ell * H**2 * 4**K:
        raise ValueError("Increase the predeclared eta grid: its smallest value is too large")
    mean = 3*math.sqrt(ell*squared_reports_bound)/N + 2*C*ell*math.sqrt(m*d)/(r*N)
    attenuation = 2*L/((1-math.exp(-1))*N)*((E0+d*N*r*r)/C**2+math.sqrt(m*d)*ell_w)
    return mean + attenuation


def choose_deadline_design():
    # This grid is evaluated using calibrations only, before the model exists.
    # Optimize the proved ceiling, NOT measured error or a preferred trajectory.
    target_operator_radius = 0.15*0.5/0.4
    candidates = []
    for milli in range(20, 121, 2):
        r = milli/1000
        lower, upper = 1, 1_000_000
        while lower < upper:
            mid = (lower+upper)//2
            if deadline_bound(mid,r) >= target_operator_radius:
                lower = mid+1
            else:
                upper = mid
        if deadline_bound(lower,r) < target_operator_radius:
            candidates.append((lower,r))
    N, r = min(candidates)
    N_checkpoint = 512*math.ceil(N/512)
    return {"probe_radius":r, "samples_per_column":N_checkpoint,
            "physical_windows":2*N_checkpoint,
            "incident_normalized_energy":2*N_checkpoint*r*r,
            "proved_operator_radius_ceiling":deadline_bound(N_checkpoint,r),
            "proved_uniform_task_radius_ceiling":0.4/0.5*deadline_bound(N_checkpoint,r),
            "grid": {"minimum_radius":0.02, "maximum_radius":0.12,"step":0.002},
            "calibrations":{"m":2,"d":2,"E0_upper_bound":100.0,"C":0.8,
                            "ADC_levels":257,"entry_A_bound":1.0,"delta":0.01,
                            "lambda":0.5,"task_b_norm_bound":0.4,"task_target":0.15}}


def jsonable(x):
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, np.generic):
        return x.item()
    raise TypeError(type(x).__name__)


def main():
    design = choose_deadline_design()
    # First attack: dense fixed amplitude with fresh signs, same ADC, lossless
    # passive plant. Its warm fields cause sustained clipping and erase slope.
    failure = run("fixed_amplitude_failure", PassivePlant([-0.1], [0.0]),
                  r=0.5, C=0.2, levels=257, max_per_column=65536, seed=1701, E0_bound=0.0)
    repair = run("small_amplitude_same_plant", PassivePlant([-0.1], [0.0]),
                 r=0.02, C=0.2, levels=257, max_per_column=65536, seed=1701, E0_bound=0.0)
    # Persistent multimode fixture: two observable rates, non-symmetric A,
    # initial warm energy, and a dark coordinate that never relaxes.
    plant = PassivePlant([0.98, 0.9999], [8.0, -4.0], dark=3.0,
                         U=rotation(0.31), V=rotation(-0.47))
    constructive = run("persistent_mimo_r012", plant, r=0.12, C=0.8, levels=257,
                       max_per_column=131072, seed=271828, target=0.15,
                       b=np.array([0.32, -0.24]), record=True)
    plant_designed = PassivePlant([0.98, 0.9999], [8.0, -4.0], dark=3.0,
                                 U=rotation(0.31), V=rotation(-0.47))
    designed_run = run("persistent_mimo_designed", plant_designed,
                       r=design["probe_radius"], C=0.8, levels=257,
                       max_per_column=design["samples_per_column"], seed=271828,
                       target=0.15,b=np.array([0.32,-0.24]),record=True)
    results = {"algebra_checks": algebra_checks(), "failed_attack": failure,
               "same_plant_repair": repair, "persistent_mimo_r012": constructive,
               "calibration_only_deadline_design":design,"persistent_mimo_designed":designed_run}
    path = OUT / "RESULTS.json"
    path.write_text(json.dumps(results, indent=2, default=jsonable)+"\n")
    for x in [failure, repair, constructive, designed_run]:
        print(json.dumps({"name": x["name"],
                          "windows": x["physical_cost"]["windows"],
                          "saturations": x["physical_cost"]["saturated_scalar_reports_retained"],
                          "estimate": x["controller"]["confidence"]["raw"],
                          "operator_certificate": x["controller"]["confidence"]["operator_error_bound"],
                          "task_radius": x["controller"]["task_distance_radius"],
                          "audit_error": x["audit_only"]["center_operator_error"],
                          "energy": x["physical_cost"]["incident_normalized_energy"]}, default=jsonable))
    print(path)


if __name__ == "__main__":
    main()
