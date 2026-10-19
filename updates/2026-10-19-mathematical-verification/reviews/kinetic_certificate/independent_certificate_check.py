#!/usr/bin/env python3
"""Independent exact-arithmetic reconstruction; Python standard library only.

No retained certificate is read and neither source module is imported. The
Jacobian uses physical spectral projectors and interval Frechet products,
not the source's eigenbasis entry formula. All numeric comparisons are exact.
"""
from fractions import Fraction as F
from decimal import Decimal, localcontext
from pathlib import Path
import hashlib
import json
import resource
import sys
import time

resource.setrlimit(resource.RLIMIT_CPU, (180, 180))
sys.dont_write_bytecode = True
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)
HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent.parent / "sources" / "ultra"
LOWER = [(i, j) for i in range(4) for j in range(i)]


def zero(m=4, n=4):
    return [[F(0) for _ in range(n)] for _ in range(m)]


def eye(n=4):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(a, c):
    return [[c * x for x in row] for row in a]


def sub(a, b):
    return add(a, scale(b, -1))


def mm(a, b):
    bt = list(zip(*b))
    return [[sum((x * y for x, y in zip(ar, bc)), F(0)) for bc in bt] for ar in a]


def power(a, n):
    out = eye(len(a))
    for _ in range(n):
        out = mm(out, a)
    return out


def inv(a):
    n = len(a)
    out = [row[:] + er for row, er in zip(a, eye(n))]
    pivots = []
    determinant = F(1)
    for j in range(n):
        k = next(k for k in range(j, n) if out[k][j])
        if k != j:
            out[j], out[k] = out[k], out[j]
            determinant = -determinant
        pivot = out[j][j]
        determinant *= pivot
        out[j] = [x / pivot for x in out[j]]
        for k in range(n):
            if k != j:
                c = out[k][j]
                if c:
                    out[k] = [x - c * y for x, y in zip(out[k], out[j])]
        pivots.append(j)
    return [r[n:] for r in out], determinant, pivots


def maxabs(a):
    return max(abs(x) for row in a for x in row)


def norminf(a):
    return max(sum(abs(x) for x in row) for row in a)


def flat(a):
    return [[a[s][i][j]] for s in range(2) for i, j in LOWER]


def diag(entries):
    out = zero(len(entries), len(entries))
    for i, x in enumerate(entries):
        out[i][i] = x
    return out


def q(rates):
    out = scale(diag(rates), -1)
    for i in range(3):
        out[i + 1][i] = rates[i]
    return out


def b(j):
    out = zero()
    out[j][j] = F(-1)
    if j < 3:
        out[j + 1][j] = F(1)
    return out


def eigenvectors(rates):
    # Closed product formula, rather than the source's recursive construction.
    out = eye()
    for col in range(4):
        for row in range(col + 1, 4):
            numerator = F(1)
            denominator = F(1)
            for k in range(col, row):
                numerator *= rates[k]
            for k in range(col + 1, row + 1):
                denominator *= rates[k] - rates[col]
            out[row][col] = numerator / denominator
    return out


def projectors(rates):
    generator = q(rates)
    out = []
    for i, ai in enumerate(rates):
        p = eye()
        for j, aj in enumerate(rates):
            if j != i:
                p = mm(p, scale(add(generator, scale(eye(), aj)), F(1, aj - ai)))
        out.append(p)
    assert add(add(out[0], out[1]), add(out[2], out[3])) == eye()
    for i in range(4):
        assert mm(generator, out[i]) == scale(out[i], -rates[i])
        for j in range(4):
            assert mm(out[i], out[j]) == (out[i] if i == j else zero())
    return out


def exact_jacobian(rates):
    ps = projectors(rates)
    jac = zero(12, 12)
    baselines = []
    for si, speed in enumerate((1, 2)):
        es = [F(2) ** (-speed * a) for a in rates]
        flow = zero()
        for ei, pi in zip(es, ps):
            flow = add(flow, scale(pi, ei))
        powers = [power(flow, k) for k in range(6)]
        baselines.append(powers[5])
        for stage in range(3):
            # Frechet derivative of one interval: the log(2) diagonal spectral
            # terms cancel exactly when the two intervals are compensated.
            lrat = zero()
            for i in range(4):
                for j in range(4):
                    if i != j:
                        factor = (es[j] - es[i]) / (rates[i] - rates[j])
                        lrat = add(lrat, scale(mm(mm(ps[i], b(stage)), ps[j]), factor))
            for ell in range(4):
                derivative = sub(mm(mm(powers[4 - ell], lrat), powers[ell]), mm(lrat, powers[4]))
                assert all(derivative[i][i] == 0 for i in range(4))
                for k, (i, j) in enumerate(LOWER):
                    jac[6 * si + k][4 * stage + ell] = derivative[i][j]
    inverse, determinant, pivots = inv(jac)
    assert mm(jac, inverse) == eye(12) == mm(inverse, jac)
    return jac, inverse, norminf(inverse), baselines, determinant, pivots


def residue_by_label(a, b_rates, order):
    out = {}
    for i, label in enumerate(order):
        val = F(1)
        for j in range(i):
            val *= a[j] / (a[j] - a[i])
        for j in range(i + 1, 4):
            val *= b_rates[j] / (b_rates[j] - b_rates[i])
        out[label] = val
    return out


def controllability(rates):
    out = zero()
    generator = q(rates)
    col = [[F(1)], [F(0)], [F(0)], [F(0)]]
    for j in range(4):
        for i in range(4):
            out[i][j] = col[i][0]
        col = mm(generator, col)
    return out


def dec(x):
    with localcontext() as ctx:
        ctx.prec = 35
        return str(Decimal(x.numerator) / Decimal(x.denominator))


def number(x):
    return {"exact": str(x), "decimal_35_digits": dec(x)}


def main():
    start = time.monotonic()
    labels = list(map(F, (1, 3, 8, 10)))
    orders = ((0, 3, 1, 2), (1, 2, 0, 3))
    eta = F(1, 2**128)
    u = F(108, 25) + eta
    w = (50 * u - 216) / (12 - 5 * u**2)
    mu = [1 - w / 2, 3 - u * w / 2, 8 + u * w / 2, 10 + w / 2]
    t = mu[0] * mu[3] / 10
    assert 12 * (9 + w)**2 - 5 * (5 + u * w)**2 == 847
    assert mu[0] + mu[3] == mu[1] + mu[2] == 11
    assert mu[1] * mu[2] / 24 == t and t != 1 and t > 0
    assert min(mu) > 0 and len(set(mu)) == 4
    ratios = [x / y for x, y in zip(mu, labels)]
    assert len(set(ratios)) == 4
    min_ratio_gap = min(abs(ratios[i] - ratios[j]) for i in range(4) for j in range(i))
    aa = [[labels[i] for i in order] for order in orders]
    bb = [[mu[i] for i in order] for order in orders]
    forward_residues = [residue_by_label(a, b_rates, o) for a, b_rates, o in zip(aa, bb, orders)]
    reverse_residues = [residue_by_label(b_rates, a, o) for a, b_rates, o in zip(aa, bb, orders)]
    assert forward_residues[0] == forward_residues[1]
    assert reverse_residues[0] == reverse_residues[1]

    data = [exact_jacobian(rates) for rates in aa]
    alpha = max(row[2] for row in data)
    lipschitz = F(9216)
    radius = 1 / (4 * alpha * lipschitz)
    assert 0 < radius < F(1, 16)
    assert 1 - 4 * radius > F(3, 4)
    assert 10 + 4 * radius < 11

    all_targets = []
    residuals = []
    jac_records = []
    for order_index, (a, b_rates, row) in enumerate(zip(aa, bb, data)):
        jac, inverse, inverse_norm, baselines, determinant, pivots = row
        va, vb = eigenvectors(a), eigenvectors(b_rates)
        vai, vbi = inv(va)[0], inv(vb)[0]
        assert mm(q(a), va) == mm(va, scale(diag(a), -1))
        assert mm(q(b_rates), vb) == mm(vb, scale(diag(b_rates), -1))
        targets = [[], []]
        for speed in (1, 2):
            damping = diag([F(2) ** (-5 * speed * x) for x in a])
            targets[0].append(mm(mm(vb, damping), vai))
            targets[1].append(mm(mm(va, damping), vbi))
            for direction in range(2):
                target = targets[direction][-1]
                assert all(target[i][i] == F(2) ** (-5 * speed * a[i]) for i in range(4))
        for direction, rs in enumerate(targets):
            beta = maxabs(mm(inverse, sub(flat(baselines), flat(rs))))
            qbound = inverse_norm * lipschitz * radius
            assert beta <= radius / 2
            assert qbound <= F(1, 4)
            assert beta / radius + qbound < 1
            residuals.append({
                "order_zero_based": order_index,
                "direction": ("outward", "return")[direction],
                "beta": number(beta),
                "beta_over_radius": number(beta / radius),
                "contraction_bound": number(qbound),
                "self_map_radius_ratio_bound": number(beta / radius + qbound),
                "displayed_theorem_decimal_upper_bound_is_valid": beta / radius <= F("0.00035429158"),
            })
        all_targets.append(targets)
        jac_records.append({
            "rates": list(map(str, a)),
            "determinant": number(determinant),
            "inverse_norm_inf": number(inverse_norm),
            "pivots": pivots,
            "jacobian": [[str(x) for x in r] for r in jac],
            "inverse": [[str(x) for x in r] for r in inverse],
        })

    ta = mm(controllability(aa[1]), inv(controllability(aa[0]))[0])
    tb = mm(controllability(bb[1]), inv(controllability(bb[0]))[0])
    e = [[F(1)], [F(0)], [F(0)], [F(0)]]
    c = [[F(1)] * 4]
    gauge_residuals = {
        "Ta_e_minus_e": maxabs(sub(mm(ta, e), e)),
        "Tb_e_minus_e": maxabs(sub(mm(tb, e), e)),
        "c_Ta_minus_c": maxabs(sub(mm(c, ta), c)),
        "c_Tb_minus_c": maxabs(sub(mm(c, tb), c)),
        "A_generator_intertwining": maxabs(sub(mm(q(aa[1]), ta), mm(ta, q(aa[0])))),
        "B_generator_intertwining": maxabs(sub(mm(q(bb[1]), tb), mm(tb, q(bb[0])))),
    }
    for speed_index in (0, 1):
        gauge_residuals[f"outward_speed_{speed_index + 1}"] = maxabs(sub(mm(all_targets[1][0][speed_index], ta), mm(tb, all_targets[0][0][speed_index])))
        gauge_residuals[f"return_speed_{speed_index + 1}"] = maxabs(sub(mm(all_targets[1][1][speed_index], tb), mm(ta, all_targets[0][1][speed_index])))
    assert all(x == 0 for x in gauge_residuals.values())

    source_hashes = {}
    for name in (
        "workers/kinetic_frontier/exact_collision_certificate.py",
        "workers/kinetic_realization/fixed_hazard_jacobian.py",
        "workers/kinetic_frontier/THEOREM.md",
    ):
        source_hashes[name] = hashlib.sha256((SOURCE / name).read_bytes()).hexdigest()
    result = {
        "status": "INDEPENDENT_EXACT_RECONSTRUCTION_SUPPORTED",
        "implementation": "Python stdlib Fraction; spectral projectors and interval Frechet products; no source import or receipt input",
        "source_sha256": source_hashes,
        "eta": number(eta), "w": number(w), "t_minus_1": number(t - 1),
        "mu": [number(x) for x in mu],
        "response_ratios": [number(x) for x in ratios],
        "min_pairwise_response_ratio_gap": number(min_ratio_gap),
        "forward_and_reverse_residue_identities_exact": True,
        "jacobians": jac_records,
        "alpha": number(alpha), "radius": number(radius),
        "rate_box_lower": number(1 - 4 * radius),
        "rate_box_upper": number(10 + 4 * radius),
        "all_target_diagonals_tied_exactly": True,
        "residuals": residuals,
        "gauge_residuals_exact": {k: str(v) for k, v in gauge_residuals.items()},
        "ta": [[str(x) for x in row] for row in ta],
        "tb": [[str(x) for x in row] for row in tb],
        "elapsed_seconds": time.monotonic() - start,
        "analytic_premise": "Completed propagator stochastic contraction + two-insertion Duhamel Hessian bound proved in report; not established by running this script",
    }
    (HERE / "independent_checks.json").write_text(json.dumps(result, indent=2) + "\n")
    print("Independent exact branch, residue, Jacobian inverse, rate box, residual, diagonal and gauge checks supported.")
    print("alpha =", dec(alpha))
    print("radius =", dec(radius))
    print("t-1 =", dec(t - 1))
    print("min pairwise response-ratio gap =", dec(min_ratio_gap))
    for item in residuals:
        print(item["order_zero_based"], item["direction"], "beta/r =", item["beta_over_radius"]["decimal_35_digits"], "q <=", item["contraction_bound"]["decimal_35_digits"], "displayed decimal valid:", item["displayed_theorem_decimal_upper_bound_is_valid"])
    print("elapsed_seconds =", result["elapsed_seconds"])


if __name__ == "__main__":
    main()
