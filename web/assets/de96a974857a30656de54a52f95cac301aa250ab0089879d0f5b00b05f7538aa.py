"""Bounded finite diagnostic of the exact beta=2 local spin marginals.

No theorem is inferred from these floating-point checks. Uses only Python/numpy.
The Clebsch-Gordan partial trace is summed exactly over legal spin labels; log
arithmetic avoids the Gibbs exponential's overflow. Fresh preparation costs
are not modeled by this classical finite calculation.
"""
import json
import math
from pathlib import Path
import numpy as np


def logsum(a):
    a = np.asarray(a, dtype=float)
    m = float(np.max(a))
    return m + math.log(float(np.exp(a - m).sum()))


def white(n):
    labels = np.arange(n % 2, n + 1, 2, dtype=np.int64)
    lw = np.array([
        math.log(2) + 2 * math.log(int(m) + 1) - math.log(n + int(m) + 2)
        + math.lgamma(n + 1) - math.lgamma((n - int(m)) // 2 + 1)
        - math.lgamma((n + int(m)) // 2 + 1) - n * math.log(2)
        for m in labels
    ])
    return labels, lw


def global_law(n):
    m, lw = white(n)
    log_g = lw + m.astype(float) * (m + 2) / (2 * n)
    log_z = logsum(log_g)
    p = np.exp(log_g - log_z)
    mu2 = float(np.dot(p, (m / n**.75)**2))
    casimir = float(np.dot(p, m.astype(float) * (m + 2)))
    c = (casimir - 3*n) / (3*n*(n-1))
    dg = casimir / (2*n) - log_z
    return log_z, mu2, c, dg


def marginal(n, r, log_z):
    l, log_wr = white(r)
    k, log_wk = white(n-r)
    m = np.arange(n % 2, n+1, 2, dtype=np.int64)
    tilt_dimension = np.log(m+1) + m.astype(float)*(m+2)/(2*n)
    prefix = np.logaddexp.accumulate(tilt_dimension)
    log_ratio = []
    for ell in l:
        upper = (k + ell - n % 2)//2
        lower_before = (np.abs(k-ell) - n % 2)//2 - 1
        high = prefix[upper]
        low = np.full(k.shape, -np.inf)
        valid = lower_before >= 0
        low[valid] = prefix[lower_before[valid]]
        log_interval = high + np.log(-np.expm1(low-high))
        lr = logsum(log_wk - np.log(k+1) + log_interval)
        log_ratio.append(lr - math.log(int(ell)+1) - log_z)
    log_ratio = np.asarray(log_ratio)
    log_p = log_wr + log_ratio
    p, w = np.exp(log_p), np.exp(log_wr)
    tv = float(.5*np.abs(p-w).sum())
    kl = float(np.dot(p, log_ratio))
    chi = float(np.expm1(logsum(log_wr + 2*log_ratio)))
    return {
        "N": n, "r": r, "a": r/math.sqrt(n),
        "target_mass_error": float(p.sum()-1),
        "white_mass_error": float(w.sum()-1),
        "half_trace": tv, "KL": kl, "Petz_chi_square": chi,
        "max_abs_r1_log_ratio": float(np.max(np.abs(log_ratio))) if r == 1 else None,
    }


def main():
    mu2 = math.sqrt(12)*math.gamma(1.25)/math.gamma(.75)
    global_rows, local_rows = [], []
    for n in [64, 256, 1024, 4096, 16384]:
        z, observed_mu2, c, dg = global_law(n)
        global_rows.append({"N": n, "scaled_E_M2": observed_mu2,
            "limit_mu2": mu2, "sqrtN_c": math.sqrt(n)*c,
            "limit_sqrtN_c": mu2/3, "D_global_over_sqrtN": dg/math.sqrt(n),
            "limit_D_global_over_sqrtN": mu2/2,
            "logZ_minus_threequarter_logN": z-.75*math.log(n)})
        rs = sorted(set([1, 2, 4, 8, int(math.sqrt(n)),
                         min(n, int(4*math.sqrt(n))), n if n<=1024 else 16]))
        for r in rs:
            row = marginal(n, r, z)
            if r >= 2:
                degree2 = 3*r*(r-1)*c*c/2
                leading = mu2*mu2*r*(r-1)/(6*n)
                row.update({"exact_degree2_chi": degree2,
                            "asymptotic_degree2_chi": leading,
                            "chi_over_asymptotic_leading": row["Petz_chi_square"]/leading,
                            "KL_over_a": row["KL"]/row["a"],
                            "KL_over_a2": row["KL"]/row["a"]**2})
                assert row["Petz_chi_square"] >= degree2 - 2e-8
            if r == 1:
                assert row["max_abs_r1_log_ratio"] < 2e-8
            assert abs(row["target_mass_error"]) < 2e-8
            assert abs(row["white_mass_error"]) < 2e-8
            assert row["KL"] <= r/n*dg + 2e-8
            assert row["KL"] + 2e-8 >= 2*row["half_trace"]**2
            assert row["KL"] <= math.log1p(max(0,row["Petz_chi_square"]))+2e-8
            local_rows.append(row)
    out = {"status": "FINITE_FLOATING_POINT_DIAGNOSTIC_ONLY",
        "formula": "p_r(L)/w_r(L)=Z_N^-1 sum_K w_(N-r)(K)/[(L+1)(K+1)] sum_(M=|L-K|,step2)^(L+K) (M+1) exp[M(M+2)/(2N)]",
        "global": global_rows, "local": local_rows}
    dest = Path(__file__).with_name("exact_marginals.json")
    dest.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"passed": len(local_rows),
        "max_mass_error": max(abs(q["target_mass_error"]) for q in local_rows),
        "last_global": global_rows[-1],
        "last_N_local": local_rows[-len(rs):]}, indent=2))


if __name__ == "__main__":
    main()
