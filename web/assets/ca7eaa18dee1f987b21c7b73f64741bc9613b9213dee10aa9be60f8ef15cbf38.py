#!/usr/bin/env python3
"""Exact inputs and finite-volume bounds for a two-species CRN fixture.

This computes the Astra N35 global-box certificate and the facet-local
extension derived in proofs/facet_local_stochastic_safety.md. The rational
drift/correction constants are exact; exponentials are evaluated as floats.
"""

from fractions import Fraction as F
from math import ceil, comb, exp
import json

K = F(11, 10)
ell = F(1, 20)
VOLUME_TESTS = (10_000, 15_000, 18_000, 20_000)

# Reactions: 0->A, 2A->A, 0->B, B->0.
# Entries are source complexes and concentration jumps.
REACTIONS = [
    ((0, 0), (1, 0)),
    ((2, 0), (-1, 0)),
    ((0, 0), (0, 1)),
    ((0, 1), (0, -1)),
]
FACETS = [
    {"name": "A_lower", "a": (1, 0), "gamma": F(14, 25), "U_layer": (F(11, 20), F(2))},
    {"name": "A_upper", "a": (-1, 0), "gamma": F(23, 10), "U_layer": (F(2), F(2))},
    {"name": "B_lower", "a": (0, 1), "gamma": F(29, 100), "U_layer": (F(2), F(11, 20))},
    {"name": "B_upper", "a": (0, -1), "gamma": F(13, 20), "U_layer": (F(2), F(2))},
]
U_GLOBAL = (F(2), F(2))
INITIAL_GAPS = {f["name"]: F(1, 2) for f in FACETS}


def monomial(y, U):
    z = F(1)
    for yi, ui in zip(y, U):
        z *= ui**yi
    return z


def factorial_error(y, U):
    """E_y(U)=sum_j binom(y_j,2) U_j^(y_j-1) prod_{l!=j} U_l^y_l."""
    out = F(0)
    for j, yj in enumerate(y):
        if yj < 2:
            continue
        term = F(yj * (yj - 1), 2) * U[j] ** (yj - 1)
        for l, yl in enumerate(y):
            if l != j:
                term *= U[l] ** yl
        out += term
    return out


def dot(a, nu):
    return sum((F(ai) * F(ni) for ai, ni in zip(a, nu)), F(0))


def certificate(local=True):
    data = []
    for facet in FACETS:
        U = facet["U_layer"] if local else U_GLOBAL
        proj = [dot(facet["a"], nu) for _, nu in REACTIONS]
        D = K * sum((abs(v) * factorial_error(y, U)
                     for (y, _), v in zip(REACTIONS, proj)), F(0))
        Q = K * sum((v * v * monomial(y, U)
                     for (y, _), v in zip(REACTIONS, proj)), F(0))
        J = max((abs(v) for v in proj), default=F(0))
        mu = facet["gamma"] / 2
        theta = min(F(1, 1) / J, mu / (3 * Q))
        V0 = ceil(2 * D / facet["gamma"])
        data.append({
            "name": facet["name"],
            "U": [str(v) for v in U],
            "D": D,
            "gamma": facet["gamma"],
            "mu": mu,
            "J": J,
            "Q": Q,
            "theta": theta,
            "V0": V0,
            "ell": ell,
            "c_i": theta * ell,
        })

    c = min(item["c_i"] for item in data)
    V0 = max(item["V0"] for item in data)
    Lambda = K * sum((monomial(y, U_GLOBAL) for y, _ in REACTIONS), F(0))
    m = len(FACETS)
    summaries = []
    for V in VOLUME_TESTS:
        T = exp(float(c * V / 4))
        initial = sum(exp(-float(item["theta"] * V * INITIAL_GAPS[item["name"]]))
                      for item in data)
        excursion = 2 * m * V * float(Lambda) * T * exp(-float(c * V))
        summaries.append({
            "V": V,
            "T_exp_cV_over_4": T,
            "initial_term": initial,
            "time_term": excursion,
            "exit_bound": initial + excursion,
            "candidate_rate_bound_per_time": V * float(Lambda),
            "thinning_candidates_bound": V * float(Lambda) * T,
        })

    replicate = next(item for item in summaries if item["V"] == 20_000)
    p = min(1.0, replicate["exit_bound"])
    n = 200
    replicate["independent_200_replicates_at_least_3_exits_tail"] = sum(
        comb(n, k) * p**k * (1 - p)**(n - k) for k in range(3, n + 1)
    )

    # Compare both certificates at one shared, refined-certificate horizon.
    # This avoids comparing the bounds only at different advertised horizons.
    common = []
    if not local:
        refined = certificate(local=True)
        for V in VOLUME_TESTS:
            refined_row = next(row for row in refined["volume_summaries"]
                               if row["V"] == V)
            T_common = refined_row["T_exp_cV_over_4"]
            global_initial = sum(
                exp(-float(item["theta"] * V * INITIAL_GAPS[item["name"]]))
                for item in data
            )
            global_time = 2 * m * V * float(Lambda) * T_common * exp(-float(c * V))
            common.append({
                "V": V,
                "T_refined_exp_cV_over_4": T_common,
                "global_box_bound_at_same_T": global_initial + global_time,
                "refined_bound_at_same_T": refined_row["exit_bound"],
            })

    return {
        "scope": "fixture only; no theorem or novelty status is implied by calculation",
        "kind": "facet-local" if local else "Astra-N35-global-box",
        "U_global": [str(v) for v in U_GLOBAL],
        "K": str(K),
        "ell": str(ell),
        "Lambda": str(Lambda),
        "V0": V0,
        "facets": [{k: str(v) if isinstance(v, F) else v
                     for k, v in item.items()} for item in data],
        "volume_summaries": summaries,
        "common_horizon_comparison": common,
    }


if __name__ == "__main__":
    print(json.dumps({"global_box": certificate(local=False),
                      "facet_local": certificate(local=True)}, indent=2))
