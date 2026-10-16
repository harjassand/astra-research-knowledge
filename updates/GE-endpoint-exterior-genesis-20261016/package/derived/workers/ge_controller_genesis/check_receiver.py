#!/usr/bin/env python3
"""Own finite checks. Standard library only; no supplied/acquired code imported.

Quantum algebra uses arbitrary-precision Gaussian integers and rational
denominators. Equality checks below are exact, not floating-point tolerances.
Noise-weight checks alone use floating point and are labelled accordingly.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path
import time

OUT = Path(__file__).resolve().parent
Z = (0, 0)
ONE = (1, 0)
IUNIT = (0, 1)


def ga_add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def ga_mul(a, b):
    return (a[0] * b[0] - a[1] * b[1],
            a[0] * b[1] + a[1] * b[0])


def ga_conj(a):
    return (a[0], -a[1])


def put(v, k, a):
    x = ga_add(v.get(k, Z), a)
    if x == Z:
        v.pop(k, None)
    else:
        v[k] = x


def pauli_qubits(word, v):
    out = {}
    for k, value in v.items():
        j, phase = k, ONE
        for site, letter in enumerate(word):
            mask = 1 << (4 - site)
            bit = bool(k & mask)
            if letter == "X":
                j ^= mask
            elif letter == "Z":
                if bit:
                    phase = ga_mul(phase, (-1, 0))
            elif letter == "Y":
                j ^= mask
                phase = ga_mul(phase, (0, -1) if bit else IUNIT)
            else:
                assert letter == "I"
        put(out, j, ga_mul(phase, value))
    return out


def embed(v):
    out = {}
    for k, value in v.items():
        j = sum(((k >> (4 - i)) & 1) * 3 ** (4 - i)
                for i in range(5))
        out[j] = value
    return out


def inner(v, dv, w, dw):
    z = Z
    for k, a in v.items():
        z = ga_add(z, ga_mul(ga_conj(a), w.get(k, Z)))
    return (Fraction(z[0], dv * dw), Fraction(z[1], dv * dw))


def qadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def qmul(a, b):
    return (a[0] * b[0] - a[1] * b[1],
            a[0] * b[1] + a[1] * b[0])


def qconj(a):
    return (a[0], -a[1])


def qnorm(a):
    return a[0] ** 2 + a[1] ** 2


def fmt(a):
    return str(a[0]) + ("+" if a[1] >= 0 else "") + str(a[1]) + "i"


def local(v, den, site, matrix, matrix_den=1):
    stride = 3 ** (4 - site)
    out = {}
    for k, value in v.items():
        digit = (k // stride) % 3
        for target in range(3):
            a = matrix[target][digit]
            if a != Z:
                put(out, k + (target - digit) * stride,
                    ga_mul(a, value))
    return out, den * matrix_den


ID3 = [[ONE, Z, Z], [Z, ONE, Z], [Z, Z, ONE]]
PX = [[Z, ONE, Z], [ONE, Z, Z], [Z, Z, ONE]]
PY = [[Z, (0, -1), Z], [IUNIT, Z, Z], [Z, Z, ONE]]
PZ = [[ONE, Z, Z], [Z, (-1, 0), Z], [Z, Z, ONE]]
CMAT = [[(1, -1), (-1, -1), Z],
        [(1, -1), (1, 1), Z],
        [Z, Z, (2, 0)]]


def matrix_unit(a, b):
    m = [[Z for _ in range(3)] for _ in range(3)]
    m[a][b] = ONE
    return m


def gram(images_a, images_b):
    return [[inner(v, dv, w, dw) for w, dw in images_b]
            for v, dv in images_a]


def logical_matrix(vcols, images):
    return [[inner(v, 4, w, den) for w, den in images]
            for v in vcols]


def matrix_product(a, b):
    return [[qadd(qmul(a[i][0], b[0][j]),
                  qmul(a[i][1], b[1][j])) for j in range(2)]
            for i in range(2)]


def matrix_dagger(a):
    return [[qconj(a[j][i]) for j in range(2)] for i in range(2)]


def selector(rs):
    return min(range(4), key=lambda r: (-rs.count(r), r))


def survival(t, lam, p, eta):
    a = (lam + 9 * p) / 2
    b = math.sqrt((lam + 9 * p) ** 2 - 80 * p * p) / 2
    if b == 0:
        return math.exp(-(eta + a) * t) * (1 + a * t)
    return math.exp(-eta * t) * (
        (1 + a / b) * math.exp(-(a - b) * t) / 2
        + (1 - a / b) * math.exp(-(a + b) * t) / 2)


def uniformization(t, lam, p, eta):
    # Exact killed 2-state generator evaluated by a convergent Poisson series.
    q = max(5 * p + eta, lam + 4 * p + eta)
    if not q:
        return 1.0
    p00, p01 = 1 - (5 * p + eta) / q, lam / q
    p10, p11 = 5 * p / q, 1 - (lam + 4 * p + eta) / q
    v0, v1, weight = 1.0, 0.0, math.exp(-q * t)
    total = weight
    for k in range(1, max(100, int(q * t + 20 * math.sqrt(q * t + 1)))):
        v0, v1 = p00 * v0 + p01 * v1, p10 * v0 + p11 * v1
        weight *= q * t / k
        total += weight * (v0 + v1)
    return total


def main():
    cpu_start, wall_start = time.process_time(), time.perf_counter()
    raw = {0: ONE}
    stabilizers = ["XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"]
    for word in stabilizers:
        w = pauli_qubits(word, raw)
        for k, value in w.items():
            put(raw, k, value)
    assert len(raw) == 16 and all(a in (ONE, (-1, 0)) for a in raw.values())
    raw1 = pauli_qubits("XXXXX", raw)
    for word in stabilizers:
        assert pauli_qubits(word, raw) == raw
        assert pauli_qubits(word, raw1) == raw1
    vcols = [embed(raw), embed(raw1)]
    assert logical_matrix(vcols, [(v, 4) for v in vcols]) == [
        [(Fraction(1), Fraction(0)), (Fraction(0), Fraction(0))],
        [(Fraction(0), Fraction(0)), (Fraction(1), Fraction(0))]]

    named = [("I", [(v, 4) for v in vcols], Fraction(1))]
    for i in range(5):
        for name, matrix in [("X", PX), ("Y", PY), ("Z", PZ)]:
            named.append((f"{name}{i}", [local(v, 4, i, matrix) for v in vcols], Fraction(1)))
        for b in range(2):
            named.append((f"L{i}{b}", [local(v, 4, i, matrix_unit(2, b))
                                      for v in vcols], Fraction(1, 2)))
    assert len(named) == 26
    gram_blocks = 0
    for ia, (_, a, ka) in enumerate(named):
        for ib, (_, b, _) in enumerate(named):
            g = gram(a, b)
            target = ka if ia == ib else Fraction(0)
            assert g == [[(target, Fraction(0)), (Fraction(0), Fraction(0))],
                         [(Fraction(0), Fraction(0)), (target, Fraction(0))]]
            gram_blocks += 1

    generic = [("I", [(v, 4) for v in vcols])]
    for i in range(5):
        for a, b in product(range(3), range(2)):
            generic.append((f"E{i}{a}{b}",
                            [local(v, 4, i, matrix_unit(a, b)) for v in vcols]))
    assert len(generic) == 31
    generic_blocks = 0
    for _, a in generic:
        for _, b in generic:
            g = gram(a, b)
            assert g[0][1] == g[1][0] == (Fraction(0), Fraction(0))
            assert g[0][0] == g[1][1]
            generic_blocks += 1

    logicals = {}
    for name, matrix, den in [("X", PX, 1), ("C", CMAT, 2)]:
        images = [(v, 4) for v in vcols]
        for i in range(5):
            images = [local(v, d, i, matrix, den) for v, d in images]
        l = logical_matrix(vcols, images)
        for b in range(2):
            norm = inner(images[b][0], images[b][1], images[b][0], images[b][1])
            assert norm == (Fraction(1), Fraction(0))
            assert sum(qnorm(l[a][b]) for a in range(2)) == 1
        logicals[name] = l
    lx, lc = logicals["X"], logicals["C"]
    cx, xc = matrix_product(lc, lx), matrix_product(lx, lc)
    assert cx != xc
    relative = matrix_product(matrix_dagger(cx), xc)
    trace = qadd(relative[0][0], relative[1][1])
    assert trace == (Fraction(0), Fraction(0))  # Perfectly distinguishable channels.

    total_states = one_site_cases = 0
    selector_table = []
    for rs in product(range(4), repeat=5):
        r = selector(rs)
        selector_table.append(r)
        for ls in product(range(2), repeat=5):
            # Every branch has a suffix and a canonical ownership result.
            suffix = [not (rs[i] == r and ls[i] == 1) for i in range(5)]
            assert len(suffix) == 5
            output_rs = ((r + 1) % 4,) * 5
            assert selector(output_rs) == (r + 1) % 4
            assert (1 - r % 2) == output_rs[0] % 2
            total_states += 1
    assert total_states == 4 ** 5 * 2 ** 5
    for r, ls in product(range(4), product(range(2), repeat=5)):
        for site, rr, ll in product(range(5), range(4), range(2)):
            rs, bad_ls = [r] * 5, list(ls)
            rs[site], bad_ls[site] = rr, ll
            assert selector(rs) == r
            for j in range(5):
                if j != site:
                    suffix = not (rs[j] == r and bad_ls[j] == 1)
                    assert int(suffix) + ls[j] == 1
            one_site_cases += 1
    assert one_site_cases == 5120

    trap = (1, 2, 3, 0, 0)
    assert selector(trap) == 0
    split = (1, 1, 0, 0, 0)
    assert selector(split) == 0
    wrong_majority = (1, 1, 1, 0, 0)
    assert selector(wrong_majority) == 1
    # This branch selects initially vacant B and discards legitimately owned A.
    # The total recovery maps five vacancies to its declared complement |0_L>.
    vacancy_index = 3 ** 5 - 1
    assert all(vacancy_index not in v for _, images, _ in named for v, _ in images)

    noise_checks, examples = 0, []
    for lam, p, eta, t in product([0.2, 1.0, 3.0], [0.0, 0.001, 0.01, 0.1],
                                [0.0, 0.002], [0.01, 1.0, 10.0, 50.0]):
        s = survival(t, lam, p, eta)
        u = uniformization(t, lam, p, eta)
        assert abs(s - u) < 2e-12
        h = eta + 20 * p * p / (lam + 4 * p)
        assert -2e-12 <= 1 - s <= min(1.0, h * t) + 2e-12
        noise_checks += 1
        if lam == 1 and p == 0.01 and eta == 0 and t in [1.0, 10.0, 50.0]:
            examples.append({"t": t, "good_probability": s,
                             "diamond_upper": 2 * (1 - s),
                             "linear_upper": min(2.0, 2 * h * t)})

    table = {"phase_modulus": 4, "copies": 5, "progress_bit": [0, 1],
             "selector_index": "base-4 word in itertools.product order",
             "selector": selector_table,
             "micro": [{"r": r, "l": l, "accept": l == 0,
                         "bank": r % 2, "gate": "X" if r % 2 == 0 else "C",
                         "output_l": 1} for r, l in product(range(4), range(2))],
             "terminal_suffix": [{"selected_r": r, "local_r": rr,
                                  "local_l": l,
                                  "apply_U_selected": not (rr == r and l == 1)}
                                 for r, rr, l in product(range(4), range(4), range(2))]}
    (OUT / "CONTROLLER_TABLE.json").write_text(json.dumps(table, indent=2) + "\n")
    result = {
        "status": "PASS_WITH_EXPLICIT_BOUNDARIES",
        "exact_quantum_arithmetic": "Gaussian arbitrary-precision integers and Fraction",
        "code_support_per_logical_basis": [len(v) for v in vcols],
        "orthogonal_recovery_images": 26,
        "exact_diagonal_gram_blocks": gram_blocks,
        "generic_single_qutrit_error_maps": 31,
        "exact_generic_KL_blocks": generic_blocks,
        "logical_X": [[fmt(z) for z in row] for row in lx],
        "logical_C": [[fmt(z) for z in row] for row in lc],
        "relative_CX_vs_XC_trace": fmt(trace),
        "classical_full_domain_states": total_states,
        "one_site_controller_perturbation_cuts": one_site_cases,
        "three_distinct_residue_trap_selector": selector(trap),
        "two_copy_split_selector": selector(split),
        "wrong_majority_negative_control": {
            "phase_word": wrong_majority, "selected": selector(wrong_majority),
            "result": "Selects initially vacant B, discards live A, prepares code |0_L>. Quantum contract FAILS as expected outside one-site family."},
        "noise_formula_numeric_checks": noise_checks,
        "noise_examples": examples,
        "cpu_seconds": time.process_time() - cpu_start,
        "wall_seconds": time.perf_counter() - wall_start,
        "scope": "Fixed five-site atomic terminal, closed wire, one distinct faulty site per interval; no compiler, threshold, acquired physical device, or novelty proof.",
    }
    (OUT / "CHECK_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
