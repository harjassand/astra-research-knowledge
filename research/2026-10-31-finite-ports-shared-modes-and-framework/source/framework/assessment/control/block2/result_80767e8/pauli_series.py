"""Sparse exact Pauli-series arithmetic retained from this worker's first tranche.

Gaussian-integer exponential derivatives avoid all floating-point coefficients.
"""

from math import comb, factorial


def gauss_add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def gauss_mul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def gauss_scale(a, n):
    return (n * a[0], n * a[1])


PAULI = {
    ("X", "Y"): ("Z", (0, 1)),
    ("Y", "Z"): ("X", (0, 1)),
    ("Z", "X"): ("Y", (0, 1)),
    ("Y", "X"): ("Z", (0, -1)),
    ("Z", "Y"): ("X", (0, -1)),
    ("X", "Z"): ("Y", (0, -1)),
}


def pauli_mul(p, q):
    result, phase = [], (1, 0)
    for a, b in zip(p, q):
        if a == "I":
            c, z = b, (1, 0)
        elif b == "I":
            c, z = a, (1, 0)
        elif a == b:
            c, z = "I", (1, 0)
        else:
            c, z = PAULI[a, b]
        result.append(c)
        phase = gauss_mul(phase, z)
    return "".join(result), phase


def polynomial_mul(p, q):
    out = {}
    for a, x in p.items():
        for b, y in q.items():
            c, phase = pauli_mul(a, b)
            z = gauss_mul(gauss_mul(x, y), phase)
            out[c] = gauss_add(out.get(c, (0, 0)), z)
    return {key: val for key, val in out.items() if val != (0, 0)}


def series_mul(p, q, degree):
    out = []
    for k in range(degree + 1):
        term = {}
        for j in range(k + 1):
            for key, value in polynomial_mul(p[j], q[k - j]).items():
                value = gauss_scale(value, comb(k, j))
                term[key] = gauss_add(term.get(key, (0, 0)), value)
        out.append({key: value for key, value in term.items() if value != (0, 0)})
    return out


def pulse_series(pauli, sign, degree):
    phase = (1, 0)
    out = []
    for k in range(degree + 1):
        out.append({pauli if k % 2 else "III": phase})
        phase = gauss_mul(phase, (0, -sign))
    return out


HANDLES = {"A": "XIX", "B": "IXY", "C": "YIZ"}

