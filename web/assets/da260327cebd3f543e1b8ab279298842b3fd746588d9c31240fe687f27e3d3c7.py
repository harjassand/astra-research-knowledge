#!/usr/bin/env python3
"""Independent exact checks of selected c06 peer claims; no peer code imported."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations
import json
import math
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "work/cycle6/c06_l07"))
from xxz_homogeneous_compiler import Gate, HomogeneousCompiler  # noqa: E402


def qstr(x: F) -> str:
    return f"{x.numerator}/{x.denominator}"


def bitsets(n: int, size: int | None = None):
    if size is None:
        for mask in range(1 << n):
            yield frozenset(i for i in range(n) if mask >> i & 1)
    else:
        for c in combinations(range(n), size):
            yield frozenset(c)


def exact_small_soft_law(c_nonzero: bool = False) -> dict:
    if c_nonzero:
        compiler = HomogeneousCompiler(1, (Gate.field(0, F(1, 2), F(1, 3), F(1, 4)),))
        label = "single_field_nonzero_Z_control"
    else:
        compiler = HomogeneousCompiler(2, (
            Gate.pair(0, 1, F(1, 2), F(-1, 4), F(1, 3)),
            Gate.field(1, F(2, 3), F(0), F(1, 5)),
        ))
        label = "pair_plus_c0_field"
    n = compiler.ground_size
    d = compiler.target_degree
    U = frozenset(range(n))
    mu_support = [(S, compiler.mu_query(S)) for S in bitsets(n, d)]
    mu_support = [(S, w) for S, w in mu_support if w]
    nu_support = [(T, F(compiler.nu_query(T))) for T in bitsets(n, d)]
    nu_support = [(T, w) for T, w in nu_support if w]
    t = F(1, 256 * n * n)
    Z = F(0)
    p = [[F(0), F(0), F(0)] for _ in range(n)]
    hard = F(0)
    for S, mu in mu_support:
        for T, nu in nu_support:
            w = mu * nu * t ** len(S & T)
            Z += w
            if T == U - S:
                hard += w
            for i in range(n):
                copies = int(i in S) + int(i in T)
                p[i][copies] += w
    p = [[x / Z for x in row] for row in p]
    return {
        "case": label,
        "ground_size": n,
        "t": qstr(t),
        "normalizer": qstr(Z),
        "coordinate_probabilities_statuses_0_1_2": [[qstr(x) for x in row] for row in p],
        "complement_balance_p0_equals_p2": all(row[0] == row[2] for row in p),
        "hard_complement_probability": qstr(hard / Z),
        "hard_probability_at_least_3_4": hard / Z >= F(3, 4),
        "mu_complement_invariant": all(
            compiler.mu_query(S) == compiler.mu_query(U - S) for S in bitsets(n)),
        "nu_complement_invariant": all(
            compiler.nu_query(S) == compiler.nu_query(U - S) for S in bitsets(n)),
    }


def first_order_complement_checks() -> dict:
    rng = random.Random(60407)
    pair_count = field_c0_count = 0
    field_nonzero_failures = []
    for _ in range(32):
        alpha = F(rng.randint(0, 4), rng.randint(1, 7))
        gamma = alpha * F(rng.choice([-1, 0, 1]) * rng.randint(0, 3), 3)
        s = F(rng.randint(0, 4), rng.randint(1, 9))
        c = HomogeneousCompiler(2, (Gate.pair(0, 1, alpha, gamma, s),))
        f = c.factors[0]
        Uloc = frozenset(f.variables)
        assert all(f.terms.get(S, F(0)) == f.terms.get(Uloc - S, F(0))
                   for S in bitsets(4))
        pair_count += 1

        b = F(rng.randint(0, 4), rng.randint(1, 7))
        sf = F(rng.randint(0, 4), rng.randint(1, 9))
        c0 = HomogeneousCompiler(1, (Gate.field(0, b, 0, sf),))
        ff = c0.factors[0]
        Uff = frozenset(ff.variables)
        assert all(ff.terms.get(S, F(0)) == ff.terms.get(Uff - S, F(0))
                   for S in bitsets(4))
        field_c0_count += 1

        if b and sf:
            cn = HomogeneousCompiler(1, (Gate.field(0, b, F(1, 3), sf),))
            fn = cn.factors[0]
            Un = frozenset(fn.variables)
            if not all(fn.terms.get(S, F(0)) == fn.terms.get(Un - S, F(0))
                       for S in bitsets(4)):
                field_nonzero_failures.append({"b": qstr(b), "c": "1/3", "s": qstr(sf)})
    # Opposite pure-Z fields do not generally cancel the complement defect:
    # the complement ratio depends on each field-factor support choice.
    balanced_z = HomogeneousCompiler(2, (
        Gate.field(0, F(0), F(1, 3), F(1, 5)),
        Gate.field(1, F(0), F(-1, 3), F(1, 5)),
    ))
    S = frozenset((0, 2, 5, 6))
    U = frozenset(range(balanced_z.ground_size))
    ratio = balanced_z.mu_query(S) / balanced_z.mu_query(U - S)
    assert ratio == F(289, 225) and ratio != 1
    return {
        "pair_local_complement_checks": pair_count,
        "c0_field_local_complement_checks": field_c0_count,
        "nonzero_Z_field_counterexamples_to_symmetry": field_nonzero_failures[:3],
        "opposite_pure_Z_field_balance_attempt": {
            "fields": ["c=1/3", "c=-1/3"], "b": "0", "s": "1/5",
            "ground_size": balanced_z.ground_size,
            "chosen_support_vs_complement_ratio": qstr(ratio),
            "global_complement_invariance": False,
        },
        "interpretation": "pair factors are complement invariant; field factors are so at c=0; this finite check does not prove the all-size gap or sampling theorem",
    }


def p2(x: F) -> F:
    return 1 + x + x * x / 2


def second_order_gate_checks() -> dict:
    rng = random.Random(2601007)
    edge_checks = field_checks = 0
    max_margin_edge = None
    min_margin_field = None
    for _ in range(80):
        alpha = F(rng.randint(0, 5), rng.randint(1, 8))
        gamma = alpha * F(rng.choice([-1, 0, 1]) * rng.randint(0, 4), 4)
        h = F(rng.randint(0, 5), rng.randint(1, 10))
        low = p2(h * (alpha - gamma))
        mid = p2(h * (3 * alpha + gamma))
        high = p2(h * (5 * alpha - gamma))
        a = mid
        b = (high + low) / 2
        c = (high - low) / 2
        assert low >= 0 and low <= mid <= high
        margins = (a - b + c, -a + b + c, a + b - c)
        assert min(margins) >= 0
        assert b >= c >= 0 and a > 0
        current = min(margins)
        max_margin_edge = current if max_margin_edge is None else min(max_margin_edge, current)
        edge_checks += 1

        bx = F(rng.randint(0, 5), rng.randint(1, 8))
        bz = F(rng.choice([-1, 1]) * rng.randint(0, 5), rng.randint(1, 8))
        r = bx + abs(bz)
        q2 = bx * bx + bz * bz
        U = 1 + h * r + h * h * (r * r + q2) / 2
        w = h + h * h * r
        u, v, d = U - w * bz, U + w * bz, w * bx
        margin = u * v - d * d
        assert u > 0 and v > 0 and d >= 0 and margin > 0
        # Independent direct calculation of P_2(h A_v).
        direct_u = 1 + h * (r - bz) + h * h * ((r - bz) ** 2 + bx * bx) / 2
        direct_v = 1 + h * (r + bz) + h * h * ((r + bz) ** 2 + bx * bx) / 2
        direct_d = h * bx + h * h * r * bx
        assert (u, v, d) == (direct_u, direct_v, direct_d)
        min_margin_field = margin if min_margin_field is None else min(min_margin_field, margin)
        field_checks += 1
    return {
        "rational_edge_gate_cases": edge_checks,
        "rational_field_gate_cases": field_checks,
        "edge_triangle_margins_nonnegative": True,
        "smallest_uv_minus_d_squared": qstr(min_margin_field),
        "scope": "finite exact checks of second-order local formulas; universal validity rests on the derivation in peer_audit.txt",
    }


def projector_matrix(q: int) -> list[list[F]]:
    dim = 1 << q
    out = [[F(0) for _ in range(dim)] for _ in range(dim)]
    for row in range(dim):
        r = row.bit_count()
        for col in range(dim):
            if col.bit_count() == r:
                out[row][col] = F(1, math.comb(q, r))
    return out


def matmul(a, b):
    n, mid, m = len(a), len(b), len(b[0])
    out = [[F(0) for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for k in range(mid):
            if a[i][k]:
                for j in range(m):
                    out[i][j] += a[i][k] * b[k][j]
    return out


def projector_checks() -> dict:
    q_sizes = list(range(1, 6))
    results = []
    signature_derivatives = 0
    for q in q_sizes:
        Pi = projector_matrix(q)
        assert matmul(Pi, Pi) == Pi
        assert sum(Pi[i][i] for i in range(len(Pi))) == q + 1
        support_count = 0
        for row_mask in range(1 << q):
            for colbar_mask in range(1 << q):
                r = row_mask.bit_count()
                cbar = colbar_mask.bit_count()
                expected = F(1, math.comb(q, r)) if r + cbar == q else F(0)
                col_mask = ((1 << q) - 1) ^ colbar_mask
                assert Pi[row_mask][col_mask] == expected
                support_count += expected != 0
        assert support_count == math.comb(2 * q, q)
        if q >= 2:
            for a in range(q - 1):
                b = q - 2 - a
                m, ell = q - a, q - b
                A = F(1, math.comb(q, a + 2))
                B = F(1, math.comb(q, a + 1))
                D = F(1, math.comb(q, a))
                assert A * D * (m - 1) * (ell - 1) == B * B * m * ell
                assert A * (m - 1) + D * (ell - 1) > 0
                signature_derivatives += 1
        results.append({"q": q, "projector_idempotent": True,
                        "trace": q + 1, "polynomial_support_size": support_count})
    qA, qB = 2, 1
    Pi = kron(projector_matrix(qA), projector_matrix(qB))
    nconst = qA + qB
    dim = 1 << nconst
    alpha, gamma, bx, bz = F(2, 3), F(-1, 4), F(1, 2), F(2, 5)
    H = [[F(0) for _ in range(dim)] for _ in range(dim)]
    pair = [[gamma, 0, 0, 0], [0, -gamma, 2 * alpha, 0],
            [0, 2 * alpha, -gamma, 0], [0, 0, 0, gamma]]
    field = [[bz / 2, bx / 2], [bx / 2, -bz / 2]]
    for a in range(qA):
        H = add_matrices(H, embed_local(nconst, (a, qA),
                                        [[x / 4 for x in row] for row in pair]))
        H = add_matrices(H, embed_local(nconst, (a,), field))
    for b in range(qB):
        H = add_matrices(H, embed_local(nconst, (qA + b,), field))
    comm = add_matrices(matmul(Pi, H), [[-x for x in row] for row in matmul(H, Pi)])
    assert all(x == 0 for row in comm for x in row)
    return {"projector_sizes": results,
            "exact_q_minus_2_derivative_signature_identities": signature_derivatives,
            "embedded_spin2_plus_spin1_half_commutator_zero": True,
            "scope": "finite checks support the all-q formula; Lorentzian implication relies on Branden-Huh theorem, not these checks"}


def kron(a, b):
    out = []
    for ar in a:
        for br in b:
            out.append([x * y for x in ar for y in br])
    return out


def add_matrices(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def embed_local(nqubits: int, qubits: tuple[int, ...], local):
    dim = 1 << nqubits
    out = [[F(0) for _ in range(dim)] for _ in range(dim)]
    for row in range(dim):
        ri = 0
        for q in qubits:
            ri = (ri << 1) | ((row >> (nqubits - q - 1)) & 1)
        for col in range(dim):
            if any(((row >> (nqubits - q - 1)) & 1) !=
                   ((col >> (nqubits - q - 1)) & 1)
                   for q in range(nqubits) if q not in qubits):
                continue
            ci = 0
            for q in qubits:
                ci = (ci << 1) | ((col >> (nqubits - q - 1)) & 1)
            out[row][col] = local[ri][ci]
    return out


def local_boundary_checks() -> dict:
    alpha, s = F(1), F(1, 10)
    results = []
    for gamma in (F(11, 10), F(-11, 10)):
        a = 1 + s * (3 * alpha + gamma)
        b = 1 + s * (3 * alpha - gamma)
        c = 2 * s * alpha
        bad = (a - b - c, -a + b - c, -a - b + c)
        assert a + b + c > 0 and max(bad) > 0
        if gamma > alpha:
            witness = (a - b - c) / (2 * (a + b + c))
        else:
            witness = (-a + b - c) / (2 * (a + b + c))
        results.append({"alpha": qstr(alpha), "gamma": qstr(gamma), "s": qstr(s),
                        "positive_hessian_eigenvalue": qstr(max(bad)),
                        "log_hessian_positive_eigenvalue_at_ones": qstr(witness)})
    assert results[0]["log_hessian_positive_eigenvalue_at_ones"] == "1/280"
    assert results[1]["log_hessian_positive_eigenvalue_at_ones"] == "1/280"
    # The c06_l04 shifted-scalar fixture changes q(1) but leaves the bad
    # anisotropy eigenvalue unchanged.
    kappa = F(10)
    gamma = F(11, 10)
    a = 1 + s * (kappa + gamma)
    b = 1 + s * (kappa - gamma)
    c = 2 * s * alpha
    shifted_hessian = (a - b - c, -a + b - c)
    shifted_log_curvature = shifted_hessian[0] / (2 * (a + b + c))
    assert shifted_hessian == (F(1, 50), F(-21, 50))
    assert shifted_log_curvature == F(1, 420)
    return {
        "outside_cone_witnesses": results,
        "large_scalar_shift_witness": {
            "kappa": qstr(kappa),
            "hessian_anisotropy_eigenvalues": [qstr(x) for x in shifted_hessian],
            "positive_log_hessian_eigenvalue_at_ones": qstr(shifted_log_curvature),
        },
        "interpretation": "a direct local specialization/coefficient lift cannot extend beyond |gamma|<=alpha because restriction or differentiation preserves LC; this is not a hardness result",
    }


def prior_art_scope_checks() -> dict:
    """Independent exact fixtures for the attributed c06_l01 scope audit."""
    alpha, s = F(1), F(1, 10)
    outputs = []
    for gamma in (F(1, 2), F(-1, 2)):
        a = 1 + s * (3 * alpha + gamma)
        b = 1 + s * (3 * alpha - gamma)
        c = 2 * s * alpha
        linear = abs(a - b) <= c and c <= a + b
        gaps = (a * a - b * b - c * c,
                b * b - a * a - c * c,
                c * c - a * a - b * b)
        assert linear and sum(gap > 0 for gap in gaps) == 1
        assert max(gaps) == F(11, 50)
        outputs.append({
            "alpha": qstr(alpha), "gamma": qstr(gamma), "s": qstr(s),
            "linear_triangle": linear,
            "squared_triangle_all_permutations": all(gap <= 0 for gap in gaps),
            "positive_squared_triangle_gap": qstr(max(gaps)),
        })
    # P_{Psi+}=(I+XX+YY-ZZ)/4, so XX+YY-ZZ=4P_{Psi+}-I.
    pauli_identity = {"I": F(1, 4), "XX": F(1, 4), "YY": F(1, 4), "ZZ": F(-1, 4)}
    assert pauli_identity == {"I": F(1, 4), "XX": F(1, 4), "YY": F(1, 4), "ZZ": F(-1, 4)}
    return {
        "cai_liu_lu_scope_fixtures": outputs,
        "epr_endpoint_projector_coefficients": {k: qstr(v) for k, v in pauli_identity.items()},
        "interpretation": "The old squared-triangle condition misses these nonzero-gamma gates; Chen-Liu EPR overlap at gamma=-alpha remains a subfamily overlap, not a full-field solution.",
    }


def two_qubit_pauli(word: str) -> list[list[F]]:
    one = {
        "I": [[F(1), F(0)], [F(0), F(1)]],
        "X": [[F(0), F(1)], [F(1), F(0)]],
        "Y": [[F(0), F(-1)], [F(1), F(0)]],
        "Z": [[F(1), F(0)], [F(0), F(-1)]],
    }
    result = [[F(1)]]
    for symbol in word:
        b = one[symbol]
        # Kronecker product, written explicitly to keep the check standalone.
        result = [[result[i][j] * b[k][l]
                   for j in range(len(result[0])) for l in range(2)]
                  for i in range(len(result)) for k in range(2)]
    # The real antisymmetric representative is iY, so its tensor square is
    # -YY in the standard Pauli convention.
    if word == "YY":
        result = [[-x for x in row] for row in result]
    return result


def matadd_scaled(terms):
    n = len(terms[0][1])
    return [[sum(scale * matrix[i][j] for scale, matrix in terms)
             for j in range(n)] for i in range(n)]


def exact_trace(a):
    return sum(a[i][i] for i in range(len(a)))


def exact_matrix_power(a, exponent: int):
    n = len(a)
    result = [[F(int(i == j)) for j in range(n)] for i in range(n)]
    for _ in range(exponent):
        result = matmul(result, a)
    return result


def mixed_field_trace_cube_checks() -> dict:
    rng = random.Random(604071)
    checks = []
    words = {name: two_qubit_pauli(name) for name in ("XX", "YY", "ZZ", "XI", "IX")}
    for _ in range(32):
        alpha = F(rng.randint(-4, 4), rng.randint(1, 7))
        gamma = F(rng.randint(-4, 4), rng.randint(1, 7))
        b1 = F(rng.randint(-4, 4), rng.randint(1, 7))
        b2 = F(rng.randint(-4, 4), rng.randint(1, 7))
        H = matadd_scaled(((alpha, words["XX"]), (alpha, words["YY"]),
                           (gamma, words["ZZ"]), (b1, words["XI"]),
                           (b2, words["IX"])))
        lhs = exact_trace(exact_matrix_power(H, 3))
        rhs = 24 * alpha * (b1 * b2 - alpha * gamma)
        assert lhs == rhs
        checks.append({"alpha": qstr(alpha), "gamma": qstr(gamma),
                       "b1": qstr(b1), "b2": qstr(b2), "trace_H3": qstr(lhs)})
    examples = []
    for b2 in (F(1), F(-1)):
        alpha, gamma, b1 = F(1), F(0), F(1)
        H = matadd_scaled(((alpha, words["XX"]), (alpha, words["YY"]),
                           (gamma, words["ZZ"]), (b1, words["XI"]),
                           (b2, words["IX"])))
        lhs = exact_trace(exact_matrix_power(H, 3))
        rhs = 24 * alpha * (b1 * b2 - alpha * gamma)
        assert lhs == rhs == (F(24) if b2 > 0 else F(-24))
        examples.append({"alpha": "1/1", "gamma": "0/1", "b1": "1/1",
                         "b2": qstr(b2), "trace_H3": qstr(lhs)})
    return {
        "exact_rational_matrix_cases": len(checks),
        "formula": "Tr(H^3)=24 alpha (b1*b2-alpha*gamma)",
        "mixed_sign_examples": examples,
        "interpretation": "The signed cubic moment is real and may change sign as field signs vary; this does not contradict positivity of Tr(exp(beta H)) or the shifted-gate coefficient representation.",
    }


def run() -> dict:
    soft = [exact_small_soft_law(False), exact_small_soft_law(True)]
    assert soft[0]["complement_balance_p0_equals_p2"]
    assert soft[0]["hard_probability_at_least_3_4"]
    assert not soft[1]["mu_complement_invariant"]
    return {
        "audits": {
            "c06_s03_complement_symmetry": first_order_complement_checks(),
            "c06_s03_exact_small_soft_law": soft,
            "c06_l03_and_c06_l08_second_order_local_gates": second_order_gate_checks(),
            "c06_s01_higher_spin_projector": projector_checks(),
            "c06_l05_easy_axis_boundary": local_boundary_checks(),
            "c06_l01_prior_art_scope": prior_art_scope_checks(),
            "c06_l04_mixed_field_cubic": mixed_field_trace_cube_checks(),
        },
        "peer_attribution": {
            "c06_s01": "higher-spin projector and compressed-layer transfer",
            "c06_s03": "c_v=0 complement symmetry and local exact-exchange route",
            "c06_l03": "rational P2 Taylor gates and second-order product bound",
            "c06_l08": "independent/refined P2 constants and charged total cost",
            "c06_l01": "prior-art scope: old squared-triangle exclusion, EPR endpoint overlap, other comparator boundaries",
            "c06_l04": "local anisotropy curvature and mixed-field trace-cube boundary diagnostics",
        },
        "status": "VERIFIED_INTERNAL finite audit only; imported gap/FPRAS, asymptotic claims, external correctness, and priority remain unverified",
    }


if __name__ == "__main__":
    output = run()
    path = Path(__file__).with_name("peer_audit.json")
    path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"saved": str(path), "status": output["status"],
                      "q_lorentzian_derivative_identities": output["audits"]["c06_s01_higher_spin_projector"]["exact_q_minus_2_derivative_signature_identities"]}, indent=2))
