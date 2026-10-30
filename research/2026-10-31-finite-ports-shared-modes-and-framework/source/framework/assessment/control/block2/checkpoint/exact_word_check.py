"""Exact cubic certificate for the ten-segment randomized native loop.

Uses Gaussian integers and exponential *derivatives*, rather than floating
point Taylor coefficients. No third-party packages are needed.
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

# Chronological order. Each entry is a unit-strength pulse of duration delta.
PROFILE = [
    ("B", -1), ("C", -1), ("B", 1), ("C", 1), ("A", -1),
    ("C", -1), ("B", -1), ("C", 1), ("B", 1), ("A", 1),
]


def main():
    degree = 4
    for a in (-1, 1):
        for b in (-1, 1):
            signs = {"A": a, "B": b, "C": a * b}
            word = [{"III": (1, 0)}] + [{} for _ in range(degree)]
            for handle, orientation in PROFILE:
                pulse = pulse_series(HANDLES[handle], signs[handle] * orientation, degree)
                word = series_mul(pulse, word, degree)
            assert word[0] == {"III": (1, 0)}
            assert word[1] == {}
            assert word[2] == {}
            assert word[3] == {"ZXI": (0, -24)}
            print(f"sA={a:+d} sB={b:+d} sC={a*b:+d}: "
                  "W(0)=I; W'(0)=W''(0)=0; W'''(0)=-24i ZXI")
            print("  exact fourth derivative:", word[4])
    print("Therefore W(delta)=I-4i delta^3 Z1X2+O(delta^4), for all four coins.")
    print("Gaussian-integer arithmetic only; derivatives divided by k! give coefficients.")


if __name__ == "__main__":
    main()
