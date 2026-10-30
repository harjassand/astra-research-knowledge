"""Finite numerical diagnostics for the analytic randomized-channel theorem.

These tests are not a certificate for arbitrary baths. The proof is in
DERIVATION.md. No network, files outside this tranche, or installations used.
"""

from itertools import product
from math import pi
from fractions import Fraction
import numpy as np

from exact_word_check import PROFILE

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1.0, -1.0]).astype(complex)
PAULIS = {"A": X, "B": Y, "C": Z}
DATA = {"A": np.kron(X, I), "B": np.kron(I, X), "C": np.kron(Y, I)}
F_DATA = np.kron(Z, X)


def hermitian_unitary(h, t):
    values, vectors = np.linalg.eigh(h)
    return (vectors * np.exp(-1j * t * values)) @ vectors.conj().T


def spin_exp(v, t):
    """exp(-it v.sigma), using an exact two-dimensional formula."""
    norm = np.linalg.norm(v)
    if norm == 0:
        return I.copy()
    return np.cos(t * norm) * I - 1j * np.sin(t * norm) * sum(
        (v[k] / norm) * p for k, p in enumerate((X, Y, Z))
    )


def axes_function(kind, delta):
    if kind == "constant_Z_half":
        def axes(t):
            u = spin_exp((0, 0, 0.5), t)
            return {h: u.conj().T @ p @ u for h, p in PAULIS.items()}
        return axes, 2

    if kind == "rotating_axis_omega=3/delta":
        omega = 3.0 / delta
        def axes(t):
            r = spin_exp((0, omega / 2, 0), t)
            v = spin_exp((0, -omega / 2, 0.5), t)
            u = r @ v
            return {h: u.conj().T @ p @ u for h, p in PAULIS.items()}
        return axes, 2

    if kind == "spectator_shift_K=1e6":
        # H_M = 10^6 I x Z_s + (1/2) Z_M x Z_s. The spectator-only
        # summand commutes with everything involved in sigma_j(t), so it
        # cancels analytically from these axes. ||[H_M,sigma_j]|| <= 1.
        zz = np.kron(Z, Z)
        def axes(t):
            u = np.cos(t/2) * np.eye(4) - 1j * np.sin(t/2) * zz
            return {h: u.conj().T @ np.kron(p, I) @ u for h, p in PAULIS.items()}
        return axes, 4
    raise ValueError(kind)


def cycle(kind, delta, steps_per_segment=128):
    axes, m = axes_function(kind, delta)
    d = 4 * m
    signs = [{"A": a, "B": b, "C": a * b} for a, b in product((-1, 1), repeat=2)]
    unitary_size = 4 * d * d
    q_size = 3 * m * m
    state = np.concatenate([
        np.stack([np.eye(d, dtype=complex)] * 4).ravel(),
        np.zeros(q_size + m * m, dtype=complex),
    ])
    handles = ["A", "B", "C"]

    for pulse, (handle, orientation) in enumerate(PROFILE):
        active = handles.index(handle)
        def rhs(t, y):
            us = y[:unitary_size].reshape(4, d, d)
            qs = y[unitary_size:unitary_size + q_size].reshape(3, m, m)
            s = axes(t)[handle]
            native = np.kron(DATA[handle], s)
            du = np.stack([-1j * orientation * coin[handle] * native @ u
                           for coin, u in zip(signs, us)])
            dq = np.zeros_like(qs)
            dq[active] = orientation * s
            dg = -0.5 * orientation * (s @ qs[active] - qs[active] @ s)
            return np.concatenate([du.ravel(), dq.ravel(), dg.ravel()])
        step = delta / steps_per_segment
        for k in range(steps_per_segment):
            t = pulse * delta + k * step
            a = rhs(t, state)
            b = rhs(t + step/2, state + step*a/2)
            c = rhs(t + step/2, state + step*b/2)
            e = rhs(t + step, state + step*c)
            state = state + step*(a + 2*b + 2*c + e)/6

    us = state[:unitary_size].reshape(4, d, d)
    g = state[unitary_size + q_size:].reshape(m, m)
    g = (g - g.conj().T) / 2
    target = np.kron(hermitian_unitary(F_DATA, 4*delta**3),
                    hermitian_unitary(1j*g, 1))
    averaged = sum(np.kron(u.conj(), u) for u in us) / 4
    deterministic = np.kron(us[-1].conj(), us[-1])
    ideal = np.kron(target.conj(), target)

    def choi_trace_norm(s):
        j = s.reshape(d, d, d, d, order="F").transpose(0, 2, 1, 3)
        j = j.reshape(d*d, d*d, order="F") / d
        j = (j + j.conj().T) / 2
        return np.sum(np.abs(np.linalg.eigvalsh(j)))

    average_choi = choi_trace_norm(averaged - ideal)
    fixed_choi = choi_trace_norm(deterministic - ideal)
    # Analytic theorem gives (5/4)*(10 delta)^4; normalized Choi norm is
    # bounded by the diamond norm. This assertion is only a consistency test.
    theorem_bound = 1.25 * (10 * delta)**4
    assert average_choi <= theorem_bound + 2e-10
    unitarity = max(np.linalg.norm(u.conj().T @ u - np.eye(d), 2) for u in us)
    return average_choi, fixed_choi, unitarity


def resources(epsilon):
    eps = min(Fraction(str(epsilon)), Fraction(1))
    h = eps / 5000
    # Machin's formula and alternating-series rational brackets certify the
    # integer ceiling; only the displayed delta and duration are rounded.
    def atan_bracket(denominator):
        terms = 80  # even: the partial sum is a lower bound
        lower = sum(Fraction((-1)**k, (2*k + 1)*denominator**(2*k + 1))
                    for k in range(terms))
        upper = lower + Fraction(1, (2*terms + 1)*denominator**(2*terms + 1))
        return lower, upper
    a, aa = atan_bracket(5)
    b, bb = atan_bracket(239)
    low_pi, high_pi = 16*a - 4*bb, 16*aa - 4*b
    def ceiling(value):
        return (value.numerator + value.denominator - 1)//value.denominator
    n = ceiling(low_pi/(16*h**3))
    assert n == ceiling(high_pi/(16*h**3))
    delta = (pi / (16 * n))**(1/3)
    return n, delta, 10*n*delta, 10*n, 2*n


def main():
    print("Norm shown: trace norm of normalized Choi difference; a diamond-norm lower bound.")
    print("No numerical test below establishes the uniform theorem.")
    for kind in ("constant_Z_half", "rotating_axis_omega=3/delta"):
        print("\n", kind)
        print("delta   avg_choi    avg_choi/delta^4   fixed_choi/delta^2   unitarity")
        for delta in (0.08, 0.04, 0.02, 0.01, 0.005):
            avg, fixed, unitary = cycle(kind, delta)
            print(f"{delta:.5f} {avg:.9e} {avg/delta**4:.8f} "
                  f"{fixed/delta**2:.8f} {unitary:.2e}")
    print("\nspectator_shift_K=1e6 (K cancels analytically from local axes)")
    for delta in (0.04, 0.02):
        avg, fixed, unitary = cycle("spectator_shift_K=1e6", delta)
        print(f"delta={delta:g}: avg_choi={avg:.9e}; "
              f"avg/delta^4={avg/delta**4:.8f}; unitarity={unitary:.2e}")
    print("\nConservative resource examples: N certified by rational pi brackets; d,T rounded.")
    for eps in (0.1, 0.01):
        n, delta, duration, segments, bits = resources(eps)
        print(f"epsilon={eps:g}: N={n}, delta={delta:.12g}, "
              f"T={duration:.6e}, segments={segments}, private_coin_bits={bits}")


if __name__ == "__main__":
    main()
