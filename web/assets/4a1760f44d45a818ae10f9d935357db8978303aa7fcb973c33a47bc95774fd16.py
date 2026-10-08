#!/usr/bin/env python3
"""Memory-lean exact Pauli-word certificate for the m=11 Clifford star."""

import sympy as sp


def gamma_strings(n):
    strings = []
    for k in range(n):
        strings.append("Z" * k + "X" + "I" * (n - k - 1))
        strings.append("Z" * k + "Y" + "I" * (n - k - 1))
    strings.append("Z" * n)
    return strings


def word_data(word):
    """Encode tensor Pauli word as X^x Z^z and its Gaussian-integer phase."""
    length = len(word)
    xmask = zmask = ny = 0
    for axis, symbol in enumerate(word):
        bit = 1 << (length - axis - 1)
        if symbol in "XY":
            xmask |= bit
        if symbol in "YZ":
            zmask |= bit
        ny += symbol == "Y"
    phase = ((1, 0), (0, 1), (-1, 0), (0, -1))[ny % 4]
    return xmask | (zmask << length), phase


def add_term(target, key, value):
    old = target.get(key, (0, 0))
    new = old[0] + value[0], old[1] + value[1]
    if new == (0, 0):
        target.pop(key, None)
    else:
        target[key] = new


def star_terms(n):
    length = 3 * n
    terms = {}
    for gamma in gamma_strings(n):
        transpose_sign = (-1) ** gamma.count("Y")
        for word in (gamma + gamma + "I" * n, gamma + "I" * n + gamma):
            key, phase = word_data(word)
            add_term(terms, key, (transpose_sign * phase[0], transpose_sign * phase[1]))
    assert len(terms) == 2 * (2 * n + 1)
    assert all(imag == 0 for _, imag in terms.values())
    return terms, length


def multiply(left, right, length):
    low_mask = (1 << length) - 1
    out = {}
    for key_a, coeff_a in left.items():
        x_a = key_a & low_mask
        z_a = key_a >> length
        for key_b, coeff_b in right.items():
            x_b = key_b & low_mask
            z_b = key_b >> length
            sign = -1 if ((z_a & x_b).bit_count() & 1) else 1
            key = (x_a ^ x_b) | ((z_a ^ z_b) << length)
            re = coeff_a[0] * coeff_b[0] - coeff_a[1] * coeff_b[1]
            im = coeff_a[0] * coeff_b[1] + coeff_a[1] * coeff_b[0]
            add_term(out, key, (sign * re, sign * im))
    return out


def main():
    m, n = 11, 5
    dimension = 2 ** n
    h, length = star_terms(n)
    x = sp.Symbol("x")
    p = sp.Poly(
        x
        * (x - 12)
        * (x - 8)
        * (x - 6)
        * (x - 4)
        * (x + 2)
        * (x + 6)
        * (x + 10)
        * (x**2 - 128)
        * (x**2 - 84)
        * (x**2 - 80)
        * (x**2 - 48)
        * (x**2 - 20),
        x,
    )
    roots = sp.solve(p.as_expr(), x)
    assert all(sp.im(root).simplify() == 0 for root in roots)
    assert max(roots) == 12
    assert sp.gcd(p, p.diff()).degree() == 0
    quotient = p.exquo(sp.Poly(x - 12, x))
    q = sp.Poly(quotient.as_expr() / quotient.eval(12), x)

    power = {0: (1, 0)}
    p_residual = {}
    q_identity_coefficient = sp.Rational(0)
    for degree in range(p.degree() + 1):
        p_coefficient = int(p.nth(degree))
        q_coefficient = q.nth(degree)
        if p_coefficient:
            for key, coeff in power.items():
                add_term(
                    p_residual,
                    key,
                    (p_coefficient * coeff[0], p_coefficient * coeff[1]),
                )
        q_identity_coefficient += q_coefficient * power.get(0, (0, 0))[0]
        print(f"degree {degree}: Pauli support {len(power)}")
        if degree < p.degree():
            power = multiply(power, h, length)

    assert p_residual == {}, f"p(H) has {len(p_residual)} residual Pauli words"
    top_multiplicity = sp.Integer(2 ** (3 * n)) * q_identity_coefficient
    assert top_multiplicity.is_Integer and top_multiplicity > 0
    print("exact p_11(H_11)=0; all roots real and at most 12")
    print("exact multiplicity of eigenvalue 12:", top_multiplicity)
    print("three-factor Choi dimension:", dimension**3)


if __name__ == "__main__":
    main()
