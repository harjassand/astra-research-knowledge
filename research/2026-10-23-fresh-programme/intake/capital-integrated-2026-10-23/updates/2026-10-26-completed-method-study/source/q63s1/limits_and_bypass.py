#!/usr/local/bin/python3
"""Supplementary exact depth, calibration-gauge and leakage-removal checks.

Does not overwrite the first experiment or its data. No hardware is operated.
"""
import csv
import json
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy.special import ndtri
from tomography import fraction_inverse

HERE = Path(__file__).resolve().parent


def path_matrix(n, all_leaks=True):
    a = [[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n-1):
        a[i][i] += 1
        a[i+1][i+1] += 1
        a[i][i+1] = a[i+1][i] = F(-1)
    for i in range(n):
        if all_leaks or i == 0:
            a[i][i] += 1
    return a


def main():
    rows = []
    sigma = 1e-6
    z = float(ndtri(.75))
    for depth in (1,2,4,6,8,10,12,16,20,30):
        r = fraction_inverse(path_matrix(depth+1))
        signal = r[0][-1]**2/(1+r[-1][-1])
        isolated = fraction_inverse(path_matrix(depth+1, all_leaks=False))
        assert all(v == 1 for v in isolated[0])
        isolated_signal = isolated[0][-1]**2/(1+isolated[-1][-1])
        assert isolated_signal == F(1, depth+2)
        # For this particular pair, PROOF.md proves that signal is the exact
        # largest signal over every nonnegative diagonal load configuration.
        rows.append({"depth":depth,"leaky_max_signal_all_nonnegative_shunts":float(signal),
                     "signal_exact":str(signal),
                     "necessary_unit_current_T_75pct_sigma_1e-6_Pinsker":sigma**2/float(signal)**2,
                     "optimal_unloaded_real_T_75pct_sigma_1e-6":(2*sigma*z/float(signal))**2,
                     "hidden_leaks_removed_signal":float(isolated_signal),
                     "hidden_leaks_removed_signal_exact":str(isolated_signal),
                     "removed_background_leak_switches":depth,
                     "optimal_isolated_real_T_75pct_sigma_1e-6":(2*sigma*z/float(isolated_signal))**2})
    with (HERE/"limits_and_bypass.csv").open("w",newline="") as out:
        writer = csv.DictWriter(out, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)

    rng = np.random.default_rng(767)
    max_ratio = 0
    for depth in (2,4,6,8,10):
        n = depth+1
        k = np.array(path_matrix(n),dtype=float)
        r0 = np.linalg.inv(k)
        max_signal = r0[0,-1]**2/(1+r0[-1,-1])
        for _ in range(100):
            r = np.linalg.inv(k+np.diag(rng.exponential(3,n)))
            signal = r[0,-1]**2/(1+r[-1,-1])
            assert signal <= max_signal*(1+1e-12)
            max_ratio = max(max_ratio,float(signal/max_signal))

    # Unknown actuator gains and capacities leave an exact congruence gauge.
    k = np.array([[4.,-1.,-1.],[-1.,4.,-1.],[-1.,-1.,4.]])
    c = np.diag([1.,2.,3.])
    s = np.diag([1.,2.,1.])
    kp, cp = s@k@s, s@c@s
    gains = np.array([1.,1.,1.])
    gp = np.array([1.,4.,1.])
    largest_gap = 0
    for freq in (0.,.1,1.,10.,.1j,1j,10j):
        for _ in range(20):
            command = rng.uniform(0,10,3)
            r = np.linalg.inv(k+freq*c+np.diag(gains*command))
            rp = np.linalg.inv(kp+freq*cp+np.diag(gp*command))
            largest_gap = max(largest_gap,float(abs(r[0,0]-rp[0,0])))
    assert largest_gap < 1e-14
    gauge = {"K":k.tolist(),"C":c.tolist(),"load_gains":gains.tolist(),
             "S":s.tolist(),"K_prime":kp.tolist(),"C_prime":cp.tolist(),
             "load_gains_prime":gp.tolist(),"physical_leaks":k.sum(axis=1).tolist(),
             "physical_leaks_prime":kp.sum(axis=1).tolist(),
             "frequency_command_checks":140,"largest_scalar_response_gap":largest_gap,
             "arbitrary_shunt_optimality_checks":500,
             "largest_loaded_signal_ratio_to_unloaded_signal":max_ratio}
    (HERE/"calibration_gauge.json").write_text(json.dumps(gauge,indent=2)+"\n")

    # The exact inverse formula is not advertised as a physical noisy estimator.
    with (HERE/"comparison.csv").open() as inp:
        comparison = list(csv.DictReader(inp))
    status = []
    for row in comparison:
        bad = row["direct_failure"]
        if not bad and float(row["direct_max_offdiag"]) > 1e-9:
            bad = "returned positive offdiagonal: not a passive conductance matrix"
        if not bad and float(row["direct_min_leak"]) < -1e-9:
            bad = "returned negative grounded leak"
        status.append({"fixture":row["fixture"],"kind":row["kind"],
                       "noise_rel":row["noise_sigma_relative_to_baseline"],
                       "direct_physical_failure":bad})
    (HERE/"direct_physical_status.json").write_text(json.dumps(status,indent=2)+"\n")
    print(json.dumps(gauge,indent=2))
    print(json.dumps(status,indent=2))


if __name__ == "__main__":
    main()
