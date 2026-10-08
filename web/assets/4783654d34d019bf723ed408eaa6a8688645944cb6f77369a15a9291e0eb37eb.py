#!/usr/bin/env python3
"""Exact Pauli-word certificates for Clifford-vector star energies.

For m=2n+1, use the irreducible Hermitian Clifford generators on n qubits and
H=Sum_i Gamma_i^T (x) Gamma_i (x) I + Gamma_i^T (x) I (x) Gamma_i.
The script proves p(H)=0 by exact Pauli multiplication. Since H is Hermitian,
the real roots of p bound its spectrum, giving an exact full-star upper bound.
"""

import sympy as sp


PAULI_PRODUCT = {
    ("I", "I"): (0, "I"), ("I", "X"): (0, "X"),
    ("I", "Y"): (0, "Y"), ("I", "Z"): (0, "Z"),
    ("X", "I"): (0, "X"), ("Y", "I"): (0, "Y"),
    ("Z", "I"): (0, "Z"), ("X", "X"): (0, "I"),
    ("Y", "Y"): (0, "I"), ("Z", "Z"): (0, "I"),
    ("X", "Y"): (1, "Z"), ("Y", "X"): (3, "Z"),
    ("Y", "Z"): (1, "X"), ("Z", "Y"): (3, "X"),
    ("Z", "X"): (1, "Y"), ("X", "Z"): (3, "Y"),
}


def multiply_words(left, right):
    phase = 0
    out = []
    for a, b in zip(left, right):
        local_phase, symbol = PAULI_PRODUCT[a, b]
        phase = (phase + local_phase) % 4
        out.append(symbol)
    return phase, tuple(out)


def gaussian_product(a, b):
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def phase_product(a, phase):
    if phase == 0:
        return a
    if phase == 1:
        return -a[1], a[0]
    if phase == 2:
        return -a[0], -a[1]
    return a[1], -a[0]


def add_term(poly, word, coefficient):
    old = poly.get(word, (0, 0))
    new_value = old[0] + coefficient[0], old[1] + coefficient[1]
    if new_value == (0, 0):
        poly.pop(word, None)
    else:
        poly[word] = new_value


def multiply_pauli_sums(left, right):
    out = {}
    for a, ca in left.items():
        for b, cb in right.items():
            phase, word = multiply_words(a, b)
            add_term(out, word, phase_product(gaussian_product(ca, cb), phase))
    return out


def gamma_words(n):
    """Return m=2n+1 Hermitian Jordan-Wigner gamma words and signs."""
    words = []
    for k in range(n):
        prefix = ("Z",) * k
        suffix = ("I",) * (n - k - 1)
        words.append((1, prefix + ("X",) + suffix))
        words.append((1, prefix + ("Y",) + suffix))
    words.append((1, ("Z",) * n))
    return words


def star_hamiltonian(n):
    """Pauli-word expansion on reference and two output spinors."""
    m = 2 * n + 1
    out = {}
    for sign, gamma in gamma_words(n):
        transpose_sign = (-1) ** gamma.count("Y")
        reference = gamma
        output = gamma
        a_word = reference + output + ("I",) * n
        b_word = reference + ("I",) * n + output
        coefficient = (sign * transpose_sign, 0)
        add_term(out, a_word, coefficient)
        add_term(out, b_word, coefficient)
    assert len(out) == 2 * m
    return out


def polynomial_for_m(m):
    x = sp.Symbol("x")
    if m == 3:
        return sp.Poly(x * (x - 4) * (x + 2), x)
    if m == 5:
        return sp.Poly(x * (x - 6) * (x - 2) * (x + 4) * (x**2 - 20), x)
    if m == 7:
        return sp.Poly(
            x
            * (x - 8)
            * (x - 4)
            * (x + 2)
            * (x**2 - 36)
            * (x**2 - 48)
            * (x**2 - 20),
            x,
        )
    if m == 9:
        return sp.Poly(
            x
            * (x - 10)
            * (x - 6)
            * (x - 2)
            * (x + 4)
            * (x + 6)
            * (x + 8)
            * (x**2 - 84)
            * (x**2 - 48)
            * (x**2 - 20),
            x,
        )
    raise ValueError("certificate is provided for m=3,5,7,9")


def annihilator_certificate(m):
    n = (m - 1) // 2
    h = star_hamiltonian(n)
    p = polynomial_for_m(m)
    powers = [{("I",) * (3 * n): (1, 0)}]
    accumulator = {}
    for degree in range(p.degree() + 1):
        if degree:
            powers.append(multiply_pauli_sums(powers[-1], h))
        coefficient = p.nth(degree)
        if coefficient:
            assert coefficient.is_Integer
            coefficient = int(coefficient)
            for word, value in powers[-1].items():
                add_term(
                    accumulator,
                    word,
                    (coefficient * value[0], coefficient * value[1]),
                )
        print(f"m={m}: computed H^{degree}, Pauli support={len(powers[-1])}")
    assert accumulator == {}, f"nonzero residual Pauli terms: {len(accumulator)}"
    # The explicit factorization below has only real roots and largest root
    # m+1, so Hermiticity gives lambda_max(H) <= m+1 exactly.
    roots = sp.solve(p.as_expr(), p.gen)
    assert all(sp.im(root).simplify() == 0 for root in roots)
    assert max(roots) == m + 1
    assert sp.gcd(p, p.diff()).degree() == 0
    x = p.gen
    quotient = p.exquo(sp.Poly(x - (m + 1), x))
    projector_poly = sp.Poly(quotient.as_expr() / quotient.eval(m + 1), x)
    identity = ("I",) * (3 * n)
    projector_identity = sum(
        projector_poly.nth(degree) * powers[degree].get(identity, (0, 0))[0]
        for degree in range(projector_poly.degree() + 1)
    )
    multiplicity = sp.Integer(2 ** (3 * n)) * projector_identity
    assert multiplicity.is_Integer and multiplicity > 0
    print(f"m={m}: exact identity p(H)=0; real-root spectral upper bound={m+1}")
    print(f"  exact multiplicity of top eigenvalue {m+1}: {multiplicity}")
    print("  annihilator:", sp.factor(p.as_expr()))


def main():
    for m in (3, 5, 7, 9):
        annihilator_certificate(m)


if __name__ == "__main__":
    main()
