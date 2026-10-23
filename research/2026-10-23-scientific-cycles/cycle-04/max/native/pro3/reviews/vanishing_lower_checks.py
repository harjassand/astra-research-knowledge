#!/usr/bin/env python3
"""Reproduce the finite adverse-family diagnostics in vanishing_lower_proof.md.

Only Python's standard library is required.  Decimal calculations are numerical
diagnostics, not directed-rounding interval certificates.  The displayed integer
comparison establishing the rational path separation is exact.
"""

from __future__ import annotations

import argparse
from decimal import Decimal, localcontext, ROUND_FLOOR
import hashlib
import json
from pathlib import Path
import platform
import resource
import time


HERE = Path(__file__).resolve().parent
ZERO, ONE, TWO = Decimal(0), Decimal(1), Decimal(2)
COUNTERS = {"matrix_matrix_products": 0, "row_matrix_products": 0,
            "full_chain_laws": 0, "largest_dimension": 0,
            "largest_decimal_precision": 0}


def s(x):
    return str(x)


def zeros(k):
    return [[ZERO for _ in range(k)] for _ in range(k)]


def mm(a, b):
    COUNTERS["matrix_matrix_products"] += 1
    k = len(a)
    return [[sum((a[i][h] * b[h][j] for h in range(k)), ZERO)
             for j in range(k)] for i in range(k)]


def vm(v, a):
    COUNTERS["row_matrix_products"] += 1
    return [sum((v[h] * a[h][j] for h in range(len(v))), ZERO)
            for j in range(len(v))]


def row_power(v, a, n):
    COUNTERS["full_chain_laws"] += 1
    COUNTERS["largest_dimension"] = max(COUNTERS["largest_dimension"], len(v))
    while n:
        if n & 1:
            v = vm(v, a)
        n >>= 1
        if n:
            a = mm(a, a)
    return v


def kernel(pi, q, eta, Q, alpha):
    k, beta = len(q), ONE - alpha
    G, local = zeros(k), zeros(k)
    W = [pi[i] / q[i] for i in range(k)]
    for i in range(k):
        for j in range(k):
            if i == j:
                continue
            G[i][j] = q[j] * min(ONE, W[j] / W[i])
            if Q[i][j]:
                logratio = (q[j] / q[i]).ln()
                first = min(ONE, (eta * logratio).exp())
                second = min(ONE, ((pi[j] / pi[i]).ln() - eta * logratio).exp())
                local[i][j] = Q[i][j] * first * second
        G[i][i] = ONE - sum(G[i], ZERO)
        local[i][i] = ONE - sum(local[i], ZERO)
    C = [[(alpha * G[i][j] + beta * local[i][j]
           + (ONE if i == j else ZERO)) / TWO
          for j in range(k)] for i in range(k)]
    return C, G, local, W


def kl(pi, q):
    return sum((x * (x / y).ln() for x, y in zip(pi, q)), ZERO)


def small_exp_upper(logx, prec):
    """Avoid Decimal exponent-range underflow with a conservative finite cap."""
    cutoff = -Decimal(prec) * Decimal(10).ln()
    return Decimal(10) ** (-prec) if logx < cutoff else logx.exp()


def diagnostics(pi, q, C, law, bound, trap, K, prec, base_prec):
    k = len(q)
    tv = sum((abs(law[i] - pi[i]) for i in range(k)), ZERO) / TWO
    rowerr = max(abs(sum(row, ZERO) - ONE) for row in C)
    balance = max(abs(pi[i] * C[i][j] - pi[j] * C[j][i])
                  for i in range(k) for j in range(k))
    # Matrix-power mass error is amplified by n. The added digits above
    # base_prec absorb log10(n); the retained base, not total precision,
    # determines a justified replay tolerance at these horizons.
    tol = Decimal(10) ** (-(base_prec - 25))
    assert min(pi) > ZERO and min(q) > ZERO
    assert min(min(row) for row in C) >= ZERO
    assert kl(pi, q) <= K
    assert law[trap] + tol >= bound, (law[trap], bound)
    assert tv + tol >= max(ZERO, bound - pi[trap]), (tv, bound)
    assert abs(sum(law, ZERO) - ONE) < tol
    return {
        "D_pi_q": s(kl(pi, q)), "admitted_K": s(K),
        "tv": s(tv), "trap_law": s(law[trap]),
        "trap_target": s(pi[trap]), "event_mass_lower": s(bound),
        "tv_lower_from_event": s(max(ZERO, bound - pi[trap])),
        "row_sum_max_residual": s(rowerr),
        "detailed_balance_max_residual": s(balance),
        "propagated_mass_residual": s(abs(sum(law, ZERO) - ONE)),
        "numeric_assertion_absolute_tolerance": s(tol),
        "pi": list(map(s, pi)), "q": list(map(s, q)),
        "C": [[s(x) for x in row] for row in C],
        "q_C_power_n": list(map(s, law)),
        "assertions": "positive inputs, nonnegative kernel, KL admission, event <= actual trap law, TV lower, propagated mass",
    }


def three_state(k, eta_mode, base_prec):
    prec = base_prec + (k * 302 + 999) // 1000
    COUNTERS["largest_decimal_precision"] = max(COUNTERS["largest_decimal_precision"], prec)
    with localcontext() as ctx:
        ctx.prec = prec
        n_int, alpha, b, M = 2 ** k, Decimal("0.5"), Decimal("0.63"), 4
        n, beta = Decimal(n_int), ONE - alpha
        L = n.ln()
        p = L ** (-M)
        u = L.ln() if eta_mode == "critical_d0" else Decimal(eta_mode)
        eta = u / L
        qA = p / (n * L * L)
        q = [qA, b, ONE - b - qA]
        pi = [p, p / n ** 4, ONE - p - p / n ** 4]
        Q = [[ZERO, ONE, ZERO], [ONE, ZERO, ZERO], [ZERO, ZERO, ONE]]
        C, G, local, W = kernel(pi, q, eta, Q, alpha)
        assert W[1] < W[2] < W[0]
        r = (eta * (qA / b).ln()).exp()
        x = (alpha * qA + beta * r) / TWO
        d = (alpha * (ONE - b) + beta * r) / TWO
        e = alpha * (ONE - p) / (TWO * n * L * L) + beta * r / (TWO * n ** 4)
        tol = Decimal(10) ** (-(prec // 2))
        assert abs(C[1][0] - x) < tol
        assert abs((ONE - C[0][0]) - e) < tol
        retained = (n * (ONE - e).ln()).exp()
        still_B_upper = small_exp_upper(n * (ONE - d).ln(), prec)
        # For d > e (true in these examples), replacing still_B by an upper
        # bound preserves a lower event value. Formula (7) is otherwise exact.
        assert d > e
        event = b * x * (retained - still_B_upper) / (d - e)
        law = row_power(q, C, n_int)
        out = diagnostics(pi, q, C, law, event, 0, ONE, prec, base_prec)
        F = b * beta * (-u).exp() / (alpha * (ONE - b) + beta * (-u).exp())
        out.update({"family": "three_state", "n": str(n_int), "log2_n": k,
                    "eta_mode": eta_mode, "eta": s(eta), "u": s(u),
                    "decimal_precision": prec, "M": M,
                    "F_b_u": s(F), "event_over_F": s(event / F),
                    "log_n_times_tv": s(L * Decimal(out["tv"])),
                    "critical_limit_coefficient_if_d0": s(beta * b / (alpha * (ONE - b)))})
        return out


def path(k, base_prec):
    prec = base_prec + (k * 302 + 999) // 1000
    COUNTERS["largest_decimal_precision"] = max(COUNTERS["largest_decimal_precision"], prec)
    with localcontext() as ctx:
        ctx.prec = prec
        n_int = 2 ** k
        n, alpha, b = Decimal(n_int), Decimal("0.5"), Decimal("0.63")
        beta, M = ONE - alpha, 4
        L, lam, v = n.ln(), Decimal(27) / 25, Decimal(16).ln()
        u = lam * L.ln()
        eta = u / L
        m = max(1, int((u / v).to_integral_value(rounding=ROUND_FLOOR)))
        p = L ** (-M)
        z = ((p / (b * n * L * L)).ln() / Decimal(m)).exp()
        q = [b * z ** i for i in range(m + 1)]
        pi = [p * n ** (-2 * (m - i)) for i in range(m + 1)]
        q.append(ONE - sum(q, ZERO))
        pi.append(ONE - sum(pi, ZERO))
        Q = zeros(m + 2)
        for i in range(m):
            Q[i][i + 1] = Q[i + 1][i] = ONE / TWO
        Q[0][0] = Q[m][m] = ONE / TWO
        Q[-1][-1] = ONE
        C, G, local, W = kernel(pi, q, eta, Q, alpha)
        assert all(W[i] < W[i + 1] for i in range(m))
        assert W[m - 1] < W[-1] < W[m]
        s_eta = (eta * z.ln()).exp()
        f = beta * s_eta / 4
        Sq = b * z / (ONE - z)
        D = alpha * (ONE - b - Sq) / TWO
        delta = alpha / TWO * (Sq + b / n ** 2 / (ONE - ONE / n ** 2)) + beta / (4 * n ** 2)
        E = f + alpha * (ONE - b) / TWO + delta
        assert D > ZERO
        tol = Decimal(10) ** (-(prec // 2))
        for i in range(m):
            actual_exit = ONE - C[i][i]
            assert D <= actual_exit + tol and actual_exit <= E + tol
            assert abs(local[i][i + 1] - s_eta / TWO) < tol
        exact_escape = alpha * (ONE - p) / (TWO * n * L * L) + beta * s_eta / (4 * n ** 2)
        assert abs((ONE - C[m][m]) - exact_escape) < tol
        h = n_int // (2 * m)
        waitfailure_upper = small_exp_upper(Decimal(m).ln() - D * Decimal(h), prec)
        timing = max(ZERO, ONE - waitfailure_upper)
        retention = max(ZERO, ONE - alpha / (TWO * L * L) - beta / (4 * n))
        capture = b * (f / E) ** m
        event = capture * timing * retention
        law = row_power(q, C, n_int)
        out = diagnostics(pi, q, C, law, event, m, ONE, prec, base_prec)
        db = TWO * alpha * (ONE - b) / beta
        phi = (ONE + db * v.exp()).ln() / v
        out.update({"family": "growing_path", "n": str(n_int), "log2_n": k,
                    "eta": s(eta), "u": s(u), "lambda": s(lam),
                    "v": s(v), "m_edges": m, "states": m + 2, "M": M,
                    "decimal_precision": prec, "z": s(z),
                    "screen_per_edge": s(s_eta), "forward_mark_probability": s(f),
                    "exit_upper_E": s(E), "exit_lower_D": s(D),
                    "capture_bound_before_timing_retention": s(capture),
                    "waiting_failure_upper_cap": s(waitfailure_upper),
                    "retention_lower": s(retention), "lambda_phi": s(lam * phi),
                    "log_n_times_tv": s(L * Decimal(out["tv"])),
                    "log_n_times_event_tv_lower": s(L * max(ZERO, event - p))})
        return out


def optimization(base_prec):
    with localcontext() as ctx:
        ctx.prec = base_prec
        d = TWO / ONE.exp()
        lo, hi = Decimal("0.000000000001"), ONE - Decimal("0.000000000001")
        for _ in range(base_prec * 4):
            r = (lo + hi) / TWO
            log_d_r = r.ln() + (ONE - r) / r * (ONE - r).ln()
            if log_d_r < d.ln():
                lo = r
            else:
                hi = r
        r = (lo + hi) / TWO
        exponent = Decimal(27) / 25 * (Decimal(321) / 25).ln() / Decimal(16).ln()
        left, right = 321 ** 27, 25 ** 27 * 16 ** 25
        assert left < right
        return {"K": "1", "alpha": "0.5", "d_star": s(d), "chi": s(r),
                "inverse_chi": s(ONE / r), "v_opt": s(-(ONE - r).ln() / r),
                "root_bracket_width": s(hi - lo),
                "rational_example_lambda_phi": s(exponent),
                "exact_integer_inequality": {"left_321_power_27": str(left),
                    "right_25_power_27_times_16_power_25": str(right),
                    "right_minus_left": str(right - left), "passed": True},
                "exact_KL_slack_integer_check_2405_gt_2400": 2405 > 2400}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-precision", type=int, default=90)
    parser.add_argument("--output", type=Path, default=HERE / "vanishing_lower_checks.json")
    parser.add_argument("--resources", type=Path, default=HERE / "vanishing_lower_resources.json")
    args = parser.parse_args()
    wall0, cpu0 = time.perf_counter(), time.process_time()
    utc0 = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
    records = []
    for k in (20, 80, 320):
        for mode in ("0", "1", "3", "critical_d0"):
            records.append(three_state(k, mode, args.base_precision))
    for k in (20, 80, 320, 1000):
        records.append(path(k, args.base_precision))
    result = {"status": "all finite numerical diagnostics passed",
              "proof_file": "vanishing_lower_proof.md",
              "proof_sha256": sha(HERE / "vanishing_lower_proof.md"),
              "script_sha256": sha(Path(__file__).resolve()),
              "numerical_status": "Decimal, no directed-rounding interval guarantee; symbolic proof and exact integer checks carry the theorem",
              "horizons": "Exact deterministic q C^n laws by repeated squaring; no trajectories or actual n-step runs were simulated",
              "optimization": optimization(args.base_precision), "finite_chains": records}
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    resources = {"utc_start": utc0,
                 "utc_finish": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
                 "wall_seconds": time.perf_counter() - wall0,
                 "process_cpu_seconds": time.process_time() - cpu0,
                 "peak_RSS_KiB_on_this_Linux_host": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                 "python_version": platform.python_version(),
                 "base_decimal_precision": args.base_precision, "counters": COUNTERS,
                 "external_compute_or_spending": "none",
                 "discovery_cost": "Not equated with replay time. Child proof/construction time began before the first recorded clock (2026-10-21 18:08:32 UTC); exact total unavailable. Parent must include orchestration/model costs separately if observable."}
    args.resources.write_text(json.dumps(resources, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "chains": len(records),
                      "output": str(args.output), "resources": resources,
                      "optimization": result["optimization"]}, indent=2))


if __name__ == "__main__":
    main()
