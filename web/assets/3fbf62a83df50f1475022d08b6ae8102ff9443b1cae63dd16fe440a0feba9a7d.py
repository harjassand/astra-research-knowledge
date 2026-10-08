"""Grid probe of bounded transport-distribution moment optimization.

This finite discretization is diagnostic only; the interval theorem is proved
separately in FINAL_REPORT.md and no material is claimed to realize the profile.
"""
from __future__ import annotations
import json
import math


def cumulative_moments(xmin=-1.0, xmax=15.0, dx=0.02):
    n = round((xmax - xmin) / dx)
    xs = [xmin + i * dx for i in range(n + 1)]
    vals = [[], [], []]
    for x in xs:
        # Stable logistic derivative -f'(x)=1/(4 cosh^2(x/2)).
        w = 0.25 / (math.cosh(x / 2.0) ** 2)
        vals[0].append(w)
        vals[1].append(x * w)
        vals[2].append(x * x * w)
    pref = [[0.0] for _ in range(3)]
    for k in range(3):
        for i in range(n):
            pref[k].append(pref[k][-1] + 0.5 * dx * (vals[k][i] + vals[k][i + 1]))
    return xs, pref


def optimize_for_ratio(ratio, pf_floor=None):
    xs, pref = cumulative_moments()
    best_zt = {"zt": -1.0}
    best_pf = {"pf": -1.0}
    # The report's equal-first-two-moments argument reduces the exact model
    # frontier to intervals. This grid probes endpoint optimization only.
    n = len(xs)
    for i in range(n - 1):
        A0 = pref[0][i]
        B0 = pref[1][i]
        C0 = pref[2][i]
        for j in range(i + 1, n):
            A = pref[0][j] - A0
            B = pref[1][j] - B0
            if B <= 0 or A <= 0:
                continue
            C = pref[2][j] - C0
            pf = B * B / A
            if pf > best_pf["pf"]:
                den_pf = A * (C + ratio) - B * B
                zt_pf = B * B / den_pf if den_pf > 0 else 0.0
                best_pf = {"lo": xs[i], "hi": xs[j], "pf": pf,
                           "zt_at_this_profile": zt_pf}
            if pf_floor is not None and pf + 1e-10 < pf_floor:
                continue
            den = A * (C + ratio) - B * B
            if den <= 0:
                continue
            zt = B * B / den
            if zt > best_zt["zt"]:
                best_zt = {"lo": xs[i], "hi": xs[j], "pf": pf, "zt": zt}
    return {"pf_max_on_grid": best_pf, "best_interval": best_zt}


def attach_linear_response_efficiency(case):
    for item in (case["pf_max_on_grid"], case["best_interval"]):
        zt = item.get("zt", item.get("zt_at_this_profile"))
        root = math.sqrt(1.0 + zt)
        item["eta_over_carnot_linear_response"] = (root - 1.0) / (root + 1.0)


def main():
    result = {"status": "finite grid diagnostic only; not proof or material validation",
              "transport_cap_normalized_to_one": True,
              "energy_grid": {"min": -1.0, "max": 15.0, "step": 0.02},
              "cases": []}
    for a in (0.1, 1.0, 10.0):
        unconstrained = optimize_for_ratio(a)
        constrained = optimize_for_ratio(a, 1.23)
        attach_linear_response_efficiency(unconstrained)
        attach_linear_response_efficiency(constrained)
        result["cases"].append({"lattice_ratio_a": a,
                                "ZT_unconstrained": unconstrained,
                                "ZT_with_PF_floor_1.23": constrained})
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
