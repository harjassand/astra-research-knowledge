"""Symbolic checks for the proposed NV-read pulse-order contrast.

Only checks the declared illustrative ODE and algebra. It is not experimental data.
Run: python3 verify_order_contrast.py
"""

import sympy as s

u, v, a, b, tau, r, k = s.symbols(
    "u v a b tau r k", positive=True, real=True
)
x, z = s.symbols("x z", real=True)


def field(amplitude):
    return s.Matrix([v * amplitude * (1 - z), a * amplitude**2 - b * z])


fp, fm = field(u), field(-u)
# AB means +u first, -u second: final-order bracket Df_- f_+ - Df_+ f_-.
bracket = s.simplify(fm.jacobian([x, z]) * fp - fp.jacobian([x, z]) * fm)
assert s.simplify(bracket.subs(z, 0)) == s.Matrix([2 * a * u**3 * v, 0])

# z(t) is the same in both orders, because u(t)^2 is the same.
t = s.symbols("t", nonnegative=True, real=True)
z_t = a * u**2 / b * (1 - s.exp(-b * t))
first = s.integrate(v * u * (1 - z_t), (t, 0, tau))
second = s.integrate(v * u * (1 - z_t), (t, tau, 2 * tau))
# x_+-=first-second, x_-+=-first+second.
contrast = s.simplify(k * 2 * (first - second))
expected = 2 * k * v * a * u**3 / b**2 * (1 - s.exp(-b * tau)) ** 2
assert s.simplify(contrast - expected) == 0
assert s.simplify(s.limit(contrast / tau**2, tau, 0) - 2 * k * v * a * u**3) == 0

K = s.simplify(contrast.subs(u, r * u) - r * contrast)
assert s.simplify(K - (r**3 - r) * contrast) == 0

# A purely linear relaxing local magnetic state has an order effect C~u,
# but the amplitude contrast cancels it for any a,b,tau.
c = s.symbols("c", real=True)
linear_C = -2 * c * u / b * (1 - s.exp(-b * tau)) ** 2
assert s.simplify(linear_C.subs(u, r * u) - r * linear_C) == 0

print("bracket =", bracket)
print("toy C(u,tau) =", contrast)
print("toy K(r,u,tau) =", K)
print("linear relaxing control K = 0")
