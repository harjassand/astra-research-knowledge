#!/usr/bin/env python3
"""Independent Gillespie audit of the published adaptive-MPR model.

The implementation follows the APS Supplemental Material reactions S10-S15,
the adaptive force law Eq. (3), and the public repository's stopping rules.
It records force-assisted barrier lowering as a model-level energetic proxy,
not as ATP consumption or experimentally calibrated mechanical work.
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable

import numpy as np


K0 = 1126.92
EA = 12.6
EB_LOW = 13.3
EPS_E = 0.5
KON = 0.05
XA_NM = 1.5
XB_NM = 2.0
KBT_PN_NM = 1.380649e-23 * 310.2 / 1e-21
TMIN = 1.0
TMAX = 1800.0


def exact_hit_probability(l0: int, mc: int, eb: float = EB_LOW) -> float:
    """P_1(hit mc before 0) for the preforce m birth-death chain.

    This is exact for the step-force (beta=infinity) idealization with no
    minimum-contact restart.  The m-marginal rates are lambda_m=(L0-m)kon
    and mu_m=m*(ka0+kb0).
    """
    if l0 < mc or mc < 1:
        return 0.0
    q0 = K0 * math.exp(-EA) + K0 * math.exp(-eb)
    prod = 1.0
    denom = 1.0
    for j in range(1, mc):
        prod *= j * q0 / ((l0 - j) * KON)
        denom += prod
    return 1.0 / denom


def force_t(t: float, tc: float, beta: float, f0: float) -> float:
    if math.isinf(beta):
        return 0.0 if t < tc else f0
    tb = t**beta
    tcb = tc**beta
    return f0 * tb / (tb + tcb) if tb + tcb else 0.0


def force_m(mmax: int, mc: float, beta: float, f0: float) -> float:
    if math.isinf(beta):
        return 0.0 if mmax < mc else f0
    mb = float(mmax) ** beta
    mcb = float(mc) ** beta
    return f0 * mb / (mb + mcb) if mb + mcb else 0.0


@dataclass
class Trajectory:
    score: int
    duration_s: float
    max_cluster: int
    force_work_proxy_pN_nm: float
    rupture_events: int
    hit_threshold: bool
    tmax_censored: bool
    emergency_terminated: bool


def simulate_one(
    l0: int,
    eb: float,
    policy: str,
    control: float,
    beta: float,
    f0: float,
    rng: np.random.Generator,
    tmin: float = TMIN,
    tmax: float = TMAX,
) -> Trajectory:
    """One cluster extraction trajectory, following public Gillespie code.

    policy is 'mmax' or 'time'. control is mc (mmax policy) or tc seconds.
    The energetic proxy adds f*x for each force-biased bond rupture, where
    f=F/m is per-bond load and x is the Bell distance for that interface.
    """
    if l0 < 1:
        return Trajectory(0, 0.0, 0, 0.0, 0, False, False, False)
    m, n, mmax, t = 1, 0, 1, 0.0
    # Initial BCR binding is drawn separately in the published implementation.
    t += -math.log(max(rng.random(), np.finfo(float).tiny)) / (l0 * KON)
    work = 0.0
    ruptures = 0
    reached = False
    censored = False
    emergency = False
    steps = 0
    while m != 0 or t < tmin:
        steps += 1
        if steps > 2_000_000:
            raise RuntimeError("trajectory step limit exceeded")
        if policy == "mmax":
            f = force_m(mmax, control, beta, f0)
            reached = reached or (mmax >= control)
        elif policy == "time":
            f = force_t(t, control, beta, f0)
        else:
            raise ValueError(policy)

        if m == 0:
            # Reproduce public code's tmin restart: one ligand binds, either
            # newly tethered or via rebinding of an extracted BCR-Ag complex.
            rate_rebind = n * KON
            rate_new = (l0 - n) * KON
            total = rate_rebind + rate_new
            if total <= 0:
                break
            if rng.random() < rate_rebind / total:
                n -= 1
            m = 1
            mmax = max(mmax, m)
            t += -math.log(max(rng.random(), np.finfo(float).tiny)) / total
            if t >= tmax:
                break
            continue

        per_bond = f / m
        if per_bond > 1517.5:
            m = 0
            emergency = True
            break
        # Clip only against floating-point overflow; this branch lies far
        # above the published parameter range used here.
        log_ka = math.log(K0) - EA + per_bond * XA_NM / KBT_PN_NM
        log_kb = math.log(K0) - eb + per_bond * XB_NM / KBT_PN_NM
        ka = math.exp(min(log_ka, 700.0))
        kb = math.exp(min(log_kb, 700.0))
        r1 = m * ka
        r2 = m * kb
        r3 = n * KON
        r4 = (l0 - m - n) * KON
        rates = (r1, r2, r3, r4)
        total = sum(rates)
        if total <= 0:
            break
        dt = -math.log(max(rng.random(), np.finfo(float).tiny)) / total
        if t + dt > tmax:
            t = tmax
            m = 0
            censored = True
            break
        t += dt
        z = rng.random() * total
        if z < r1:
            # Ag-tether interface ruptures; antigen is extracted.
            work += per_bond * XA_NM
            ruptures += 1
            m -= 1
            n += 1
        elif z < r1 + r2:
            # BCR-Ag interface ruptures; antigen remains tethered.
            work += per_bond * XB_NM
            ruptures += 1
            m -= 1
        elif z < r1 + r2 + r3:
            m += 1
            n -= 1
        else:
            m += 1
        mmax = max(mmax, m)

    return Trajectory(int(n), float(t), int(mmax), float(work), ruptures,
                      reached, censored, emergency)


def sample_l0(rng: np.random.Generator, distribution: str, sigma: float, mean: float = 100.0) -> int:
    if distribution == "normal":
        return max(5, int(round(rng.normal(mean, sigma))))
    if distribution == "uniform_wide":
        return int(rng.integers(5, 196))
    if distribution == "uniform_low":
        return int(rng.integers(5, 61))
    if distribution == "lognormal_cv50":
        # Parameters yield the requested mean and CV=.5 before rounding.
        s2 = math.log(1.0 + 0.5**2)
        mu = math.log(mean) - s2 / 2
        return max(1, int(round(rng.lognormal(mu, math.sqrt(s2)))) )
    raise ValueError(distribution)


def run_pairs(
    policy: str,
    distribution: str,
    sigma: float,
    pairs: int,
    seed: int,
    control: float,
    beta: float = 5.0,
    f0: float = 800.0,
) -> dict:
    rng = np.random.default_rng(seed)
    wins = ties = strict_wins = 0
    scores_low, scores_high = [], []
    doses_low, doses_high = [], []
    times_low, times_high = [], []
    works_low, works_high = [], []
    threshold_low = threshold_high = 0
    censored_low = censored_high = 0
    for _ in range(pairs):
        l_low = sample_l0(rng, distribution, sigma)
        l_high = sample_l0(rng, distribution, sigma)
        low = simulate_one(l_low, EB_LOW, policy, control, beta, f0, rng)
        high = simulate_one(l_high, EB_LOW + EPS_E, policy, control, beta, f0, rng)
        scores_low.append(low.score)
        scores_high.append(high.score)
        doses_low.append(l_low)
        doses_high.append(l_high)
        times_low.append(low.duration_s)
        times_high.append(high.duration_s)
        works_low.append(low.force_work_proxy_pN_nm)
        works_high.append(high.force_work_proxy_pN_nm)
        threshold_low += int(low.hit_threshold)
        threshold_high += int(high.hit_threshold)
        censored_low += int(low.tmax_censored)
        censored_high += int(high.tmax_censored)
        if high.score > low.score:
            strict_wins += 1
            wins += 1
        elif high.score == low.score:
            ties += 1
            wins += 0.5

    return {
        "policy": policy,
        "distribution": distribution,
        "sigma": sigma,
        "pairs": pairs,
        "seed": seed,
        "control": control,
        "beta": beta,
        "f0_pN": f0,
        "epsilon_Eb_kBT": EPS_E,
        "auc_random_tie": wins / pairs,
        "strict_win_probability": strict_wins / pairs,
        "tie_probability": ties / pairs,
        "mean_dose_low_Eb": float(np.mean(doses_low)),
        "mean_dose_high_Eb": float(np.mean(doses_high)),
        "mean_score_low_Eb": float(np.mean(scores_low)),
        "mean_score_high_Eb": float(np.mean(scores_high)),
        "mean_time_low_Eb_s": float(np.mean(times_low)),
        "mean_time_high_Eb_s": float(np.mean(times_high)),
        "mean_force_barrier_work_low_Eb_pN_nm": float(np.mean(works_low)),
        "mean_force_barrier_work_high_Eb_pN_nm": float(np.mean(works_high)),
        "threshold_hit_low_Eb": threshold_low / pairs,
        "threshold_hit_high_Eb": threshold_high / pairs,
        "tmax_censor_low_Eb": censored_low / pairs,
        "tmax_censor_high_Eb": censored_high / pairs,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--pairs", type=int, default=2500)
    p.add_argument("--seed", type=int, default=74129)
    p.add_argument("--out", type=Path, default=Path(__file__).with_name("model_audit_results.json"))
    args = p.parse_args()

    cases = [
        ("normal", 0.0),
        ("normal", 10.0),
        ("normal", 20.0),
        ("normal", 30.0),
        ("uniform_wide", 0.0),
        ("uniform_low", 0.0),
        ("lognormal_cv50", 0.0),
    ]
    rows = []
    for idx, (dist, sigma) in enumerate(cases):
        for policy, control in (("mmax", 60.0), ("time", 60.0)):
            rows.append(run_pairs(policy, dist, sigma, args.pairs, args.seed + idx * 101 + int(policy == "time"), control))
    exact = {str(l): exact_hit_probability(l, 60) for l in (5, 20, 40, 50, 59, 60, 65, 70, 100, 130, 160, 195, 250)}
    payload = {
        "source_parameters": {
            "k0_s-1": K0, "Ea_kBT": EA, "Eb_low_kBT": EB_LOW,
            "kon_s-1": KON, "mc": 60, "beta": 5, "F0_pN": 800,
            "xa_nm": XA_NM, "xb_nm": XB_NM, "kBT_pN_nm": KBT_PN_NM,
            "tmin_s": TMIN, "tmax_s": TMAX,
        },
        "step_force_exact_hit_probability_beta_inf": exact,
        "results": rows,
    }
    args.out.write_text(json.dumps(payload, indent=2) + "\n")
    for r in rows:
        print(r["policy"], r["distribution"], r["sigma"],
              f"auc={r['auc_random_tie']:.4f}",
              f"strict={r['strict_win_probability']:.4f}",
              f"ties={r['tie_probability']:.4f}",
              f"censor={r['tmax_censor_low_Eb']:.3f}",
              f"time={r['mean_time_low_Eb_s']:.2f}s",
              f"work={r['mean_force_barrier_work_low_Eb_pN_nm']:.2f} pN nm")


if __name__ == "__main__":
    main()
