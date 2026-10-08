"""Exact finite-POVM lower bound and reproducible optimizer diagnostic for d=5.

The exact rational seed certifies S_5(Q) >= (5+sqrt(5))/2 > 3 for the six
selected Weyl-mode pairs. The optional NumPy multistart is only a local-search
diagnostic; its value near (13+sqrt(5))/4 is not certified as the global max.

Run from the repository root with Python 3, SymPy 1.14, and NumPy.
"""
from __future__ import annotations

import sympy as sp
from sympy import Poly


D = 5
z = sp.symbols("z")
cyclotomic = Poly(z**4 + z**3 + z**2 + z + 1, z, domain=sp.QQ)

# Two representatives (g and 2g) per projective line, slopes 0,...,4,
# followed by the vertical line. The chosen six contain one pair per line.
reps: list[tuple[int, int]] = []
for slope in range(D):
    reps.extend([(1, slope), (2, (2 * slope) % D)])
reps.extend([(0, 1), (0, 2)])
selected = (0, 2, 5, 7, 8, 10)
selected_modes = tuple(reps[i] for i in selected)


def reduce_cyclotomic(expr):
    return Poly(sp.expand(expr), z, domain=sp.QQ).rem(cyclotomic).as_expr()


def exact_certificate() -> sp.Expr:
    # |psi>=(1,-1,0,1,-1)/2, a normalized vector with rational entries.
    psi = [sp.Rational(1, 2), sp.Rational(-1, 2), 0,
           sp.Rational(1, 2), sp.Rational(-1, 2)]
    norm2 = sum(x * x for x in psi)
    assert norm2 == 1

    pair_scores = []
    for a, b in selected_modes:
        # W_(a,b)=X^a Z^b, so <psi|W|psi>=sum_j psi[j+a] psi[j] z^(b j).
        amp = sum(psi[(j + a) % D] * psi[j] * z ** (b * j)
                  for j in range(D))
        amp_conj = amp.subs(z, z**4)
        pair_scores.append(reduce_cyclotomic(sp.expand(amp * amp_conj)))

    # A_g=(W_g+W_g^*)/sqrt(2), B_g=(W_g-W_g^*)/(i sqrt(2)); hence
    # Tr(P A_g)^2+Tr(P B_g)^2=2|Tr(P W_g)|^2.
    f = reduce_cyclotomic(2 * sum(pair_scores))
    sqrt5_in_field = 1 + 2 * (z + z**4)
    target = (5 + sqrt5_in_field) / 2
    assert reduce_cyclotomic(f - target) == 0
    assert reduce_cyclotomic(target - 3) != 0
    print("selected_modes", selected_modes)
    print("rational_seed", psi)
    print("per_mode_abs2", pair_scores)
    print("exact_f_in_Q(zeta)", f)
    print("exact_f_radical", "(5+sqrt(5))/2")
    print("exact_f_gt_3", True)
    print("25_outcome_Weyl_orbit_POVM_score", "(5+sqrt(5))/2")
    return f


def numerical_optimizer_diagnostic() -> None:
    import numpy as np

    omega = np.exp(2j * np.pi / D)
    X = np.roll(np.eye(D, dtype=complex), 1, axis=1)
    Z = np.diag(omega ** np.arange(D))
    Ws = [np.linalg.matrix_power(X, a) @ np.linalg.matrix_power(Z, b)
          for a, b in selected_modes]

    def score(v):
        return float(2 * sum(abs(np.vdot(v, W @ v)) ** 2 for W in Ws))

    def riemannian_gradient(v):
        grad = np.zeros_like(v)
        for W in Ws:
            amp = np.vdot(v, W @ v)
            grad += 2 * (np.conjugate(amp) * (W @ v)
                         + amp * (W.conj().T @ v))
        grad -= v * np.vdot(v, grad).real
        return grad

    rng = np.random.default_rng(20261008)
    best_value, best_v = -1.0, None
    for _ in range(64):
        v = rng.normal(size=D) + 1j * rng.normal(size=D)
        v /= np.linalg.norm(v)
        value, step = score(v), 0.05
        for _ in range(5000):
            grad = riemannian_gradient(v)
            if np.linalg.norm(grad) < 1e-11:
                break
            rate = step
            while rate > 1e-12:
                candidate = v + rate * grad
                candidate /= np.linalg.norm(candidate)
                candidate_value = score(candidate)
                if candidate_value > value + 1e-14:
                    break
                rate *= 0.5
            if rate <= 1e-12:
                break
            v, value = candidate, candidate_value
            step = min(1.2 * rate, 0.2)
        if value > best_value:
            best_value, best_v = value, v.copy()

    assert best_v is not None
    pivot = int(np.argmax(np.abs(best_v)))
    best_v *= np.exp(-1j * np.angle(best_v[pivot]))
    print("optimizer_status", "64 seeded local-search starts; not a global certificate")
    print("approx_local_best_score", format(best_value, ".15f"))
    print("approx_local_optimizer_vector", [
        [float(x.real), float(x.imag)] for x in best_v
    ])
    print("conjectured_value_only", "(13+sqrt(5))/4")


if __name__ == "__main__":
    exact_certificate()
    numerical_optimizer_diagnostic()
