"""Failed explicit-extension attempt; this file is not a legal witness.

The projective representation and first marginal pass, but the second
marginal check fails by order one. Do not use this formula as a channel
extension. The d=5 compatibility fact used in the report comes only from the
separate exact compatibility-kernel certificate in D5_AUDIT.md.
Run from the repository root with Python 3 and NumPy installed to reproduce
the failed check.
"""
from __future__ import annotations

import numpy as np


D = 5
OMEGA = np.exp(2j * np.pi / D)
INV2 = 3  # inverse of 2 in F_5
X = np.roll(np.eye(D, dtype=complex), 1, axis=1)
Z = np.diag(OMEGA ** np.arange(D))
I_D = np.eye(D, dtype=complex)


def symplectic(g, h):
    return (g[0] * h[1] - g[1] * h[0]) % D


def add(g, h):
    return ((g[0] + h[0]) % D, (g[1] + h[1]) % D)


def phase(t):
    return OMEGA ** (t % D)


def weyl(g):
    """Symmetrized Weyl W_(a,b)=omega^(ab/2) X^a Z^b."""
    a, b = g
    return phase((a * b * INV2) % D) * np.linalg.matrix_power(X, a) @ np.linalg.matrix_power(Z, b)


def exact_v_as_float():
    r = np.sqrt(5.0)
    vals = {
        (0, 0): (23 - 2 * r) / 25,
        "b1": (75 - 16 * r) / 500,
        "b2": 3 / 20,
        "a1": 9 / 100,
        "a2": 1 / 4,
    }
    v = {}
    for a in range(D):
        for b in range(D):
            if a == b == 0:
                v[a, b] = vals[(0, 0)]
            elif b % D in (1, 4):
                v[a, b] = vals["b1"]
            elif b % D in (2, 3):
                v[a, b] = vals["b2"]
            elif a % D in (1, 4):
                v[a, b] = vals["a1"]
            else:
                v[a, b] = vals["a2"]
    return v


def main():
    vdict = exact_v_as_float()
    points = [(a, b) for a in range(D) for b in range(D)]
    v = np.array([vdict[p] for p in points])
    norm2 = float(v @ v)
    q = v * v / norm2
    index = {p: i for i, p in enumerate(points)}

    # Explicit regular projective representation on E=C^(Z_5^2).
    def R(g):
        out = np.zeros((D * D, D * D), complex)
        for h in points:
            k = ((h[0] - g[0]) % D, (h[1] - g[1]) % D)
            out[index[k], index[h]] = phase(symplectic(g, h) * INV2)
        return out

    max_rep_error = 0.0
    for g in points:
        Rg = R(g)
        max_rep_error = max(max_rep_error, np.linalg.norm(Rg.conj().T @ Rg - np.eye(D * D)))
        for h in points:
            lhs = Rg @ R(h)
            rhs = phase(-symplectic(g, h) * INV2) * R(((g[0] + h[0]) % D, (g[1] + h[1]) % D))
            max_rep_error = max(max_rep_error, np.linalg.norm(lhs - rhs))

    # V: C^5 -> C^5 tensor E, V|xi> = sum_h sqrt(q_h) W_h|xi> tensor |h>.
    V = np.zeros((D * D * D, D), complex)
    for h in points:
        Wh = weyl(h)
        for i in range(D):
            V[i * D * D + index[h], :] = np.sqrt(q[index[h]]) * Wh[i, :]
    isometry_error = np.linalg.norm(V.conj().T @ V - I_D)

    # Compute channel and compression eigenvalues on the Weyl basis.
    lam_errors = []
    corr_errors = []
    for g in points:
        Wg = weyl(g)
        lam = sum(q[index[h]] * phase(symplectic(h, g)) for h in points)
        corr = sum(np.sqrt(q[index[h]] * q[index[add(h, g)]]) for h in points)
        first = sum(q[index[h]] * weyl(h).conj().T @ Wg @ weyl(h) for h in points)
        second = V.conj().T @ np.kron(I_D, R(g)) @ V
        lam_errors.append(np.linalg.norm(first - lam * Wg))
        corr_errors.append(np.linalg.norm(second - corr * Wg))

    # Fourier-fixedness means q is self-compatible; check the exact-script
    # defining identity here at floating precision.
    f_v = np.array([
        sum(phase(symplectic(m, r)) * vdict[m] for m in points) / D
        for r in points
    ])
    print("norm2", norm2)
    print("max |Fv-v|", np.max(np.abs(f_v - v)))
    print("max projective-representation error", max_rep_error)
    print("Stinespring isometry error", isometry_error)
    print("max first-marginal Weyl-action error", max(lam_errors))
    print("max second-marginal Weyl-action/correlation error", max(corr_errors))
    print("max |lambda-correlation|", max(
        abs(
            sum(q[index[h]] * phase(symplectic(h, g)) for h in points)
            - sum(np.sqrt(q[index[h]] * q[index[add(h, g)]]) for h in points)
        )
        for g in points
    ))


if __name__ == "__main__":
    main()
