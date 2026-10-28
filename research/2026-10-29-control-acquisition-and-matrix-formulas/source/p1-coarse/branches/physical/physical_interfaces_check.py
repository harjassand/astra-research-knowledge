"""Exact rational common-metric counterexample and qubit echo identities.

Also checks the analytically derived entropy-tail witness numerically.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import numpy as np


def mat(rows):
    return [[F(x) for x in row] for row in rows]


def mul(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def adj(a):
    return list(map(list, zip(*a)))


def eq(a, b):
    return a == b


def dump(a):
    return [[str(x) for x in row] for row in a]


def echo_checks():
    b = mat([[1, 0], [0, 0]])
    us = {"z": mat([[1, 0], [0, -1]]),
          "n": [[F(4, 5), F(3, 5)], [F(3, 5), F(-4, 5)]]}
    def phi(x, name):
        uxu = mul(mul(us[name], x), us[name])
        return [[(x[i][j] + uxu[i][j]) / 2 for j in range(2)] for i in range(2)]
    def act(w):
        x = b
        for c in reversed(w):
            x = phi(x, c)
        return x
    def f(w):
        return trace(mul(b, act(w)))
    words = [w for k in range(5) for w in product("zn", repeat=k)]
    count = 0
    for v in words:
        for w in words:
            assert f(tuple(reversed(v)) + w) == trace(mul(act(v), act(w)))
            count += 1
    assert act(("z", "n")) != act(("n", "z"))
    return {"exact_echo_pairs": count,
            "Phi_z_Phi_n_b": dump(act(("z", "n"))),
            "Phi_n_Phi_z_b": dump(act(("n", "z"))),
            "f_znz": str(f(("z", "n", "z"))),
            "f_nzn": str(f(("n", "z", "n")))}


def metric_failure():
    a1 = [[F(3, 4), F(1, 4)], [F(3, 4), F(1, 4)]]
    a2 = [[F(1, 4), F(3, 4)], [F(1, 4), F(3, 4)]]
    for a, pi in [(a1, [F(3, 4), F(1, 4)]), (a2, [F(1, 4), F(3, 4)])]:
        d = [[pi[0], F(0)], [F(0), pi[1]]]
        assert mul(d, a) == mul(adj(a), d)
        assert mul(a, a) == a
    g = [[mul(ai, aj)[0][0] for aj in [a1, a2]] for ai in [a1, a2]]
    sym = [[(g[i][j] + g[j][i]) / 2 for j in range(2)] for i in range(2)]
    det = sym[0][0] * sym[1][1] - sym[0][1] * sym[1][0]
    assert det == -F(1, 16)
    return {"echo_matrix": dump(g), "symmetrized": dump(sym), "determinant": str(det)}


def rel_entropy(a, b):
    av, au = np.linalg.eigh(a)
    bv, bu = np.linalg.eigh(b)
    logb = (bu * np.log(np.maximum(bv, 1e-300))) @ bu.conj().T
    pos = av > 1e-14
    return float(np.sum(av[pos] * np.log(av[pos])) - np.trace(a @ logb).real)


def measured_blocks(rho, effects, dr=3):
    t = rho.reshape(2, dr, 2, dr)
    return [np.einsum("ab,brat->rt", e, t) for e in effects]


def entropy_failure():
    s, e = 0.5, 1.0
    ident, x = np.eye(2), np.array([[0., 1.], [1., 0.]])
    pe = [ident / 2, ident / 2]
    qe = [(ident + s * x) / 2, (ident - s * x) / 2]
    aa = np.zeros((6, 6)); aa[1, 1] = 1
    phi = np.zeros(6); phi[1] = phi[5] = 1 / np.sqrt(2)
    ground = np.zeros((6, 6)); ground[0, 0] = ground[3, 3] = 0.5
    def defect(a, b):
        p = sum(rel_entropy(r, q) for r, q in zip(measured_blocks(a, pe), measured_blocks(b, pe)))
        q = sum(rel_entropy(r, q) for r, q in zip(measured_blocks(a, qe), measured_blocks(b, qe)))
        return q - p
    def reset_high(rho):
        t = rho.reshape(2, 3, 2, 3)
        y = t[:, :2, :, :2].copy()
        y[:, 0, :, 0] += t[:, 2, :, 2]
        out = np.zeros_like(t)
        out[:, :2, :, :2] = y
        return out.reshape(6, 6)
    rows = []
    expected = -0.5 * np.log(1 - s * s)
    for level in [10, 100, 1000, 10000]:
        p = 2 * e / (level + 1)
        bb = (1 - p) * ground + p * np.outer(phi, phi)
        before, after = defect(aa, bb), defect(aa, reset_high(bb))
        assert abs(before - expected) < 2e-12
        assert abs(after) < 2e-12
        rows.append({"excited_energy": level, "mean_beta_energy": e,
                     "omitted_probability": p / 2, "defect_before": before,
                     "defect_after": after})
    return rows


if __name__ == "__main__":
    result = {"common_metric_failure": metric_failure(),
              "quantum_echo": echo_checks(),
              "entropy_tail_failure": entropy_failure(),
              "scope": "Rational metric/echo checks are exact; entropy checks are floating diagnostics of the ordinary proof."}
    Path(__file__).with_name("physical_interface_checks.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
