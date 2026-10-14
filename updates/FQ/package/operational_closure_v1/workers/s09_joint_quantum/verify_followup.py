"""Symbolic checks for the S09 follow-up countermodels.

These identities concern toy models only; they are not experimental validation.
"""

import sympy as s

U, r, tau, t = s.symbols("U r tau t", positive=True)
a, b, v, alpha, k = s.symbols("a b v alpha k", positive=True)
lam, gamma, beta, Bs, d = s.symbols(
    "lam gamma beta Bs d", positive=True
)

# An even-in-current thermal state has the same trajectory in both pulse orders.
theta = a * U**2 / b * (1 - s.exp(-b * t))
early = s.integrate(theta, (t, 0, tau))
late = s.integrate(theta, (t, tau, 2 * tau))
c_thermal = s.simplify(2 * k * v * alpha * U * (late - early))
target_thermal = (
    2 * k * v * alpha * a * U**3
    * (1 - s.exp(-b * tau)) ** 2 / b**2
)
assert s.simplify(c_thermal - target_thermal) == 0
assert s.simplify(
    target_thermal.subs(U, r * U) - r * target_thermal
    - (r**3 - r) * target_thermal
) == 0

# A purely linear polarization changes a local ohmic heating coefficient.
q_early = U * (1 - s.exp(-lam * t)) / lam
q_at_tau = q_early.subs(t, tau)
q_late = (
    q_at_tau * s.exp(-lam * (t - tau))
    - U * (1 - s.exp(-lam * (t - tau))) / lam
)
q_integral = s.simplify(
    s.integrate(q_early, (t, 0, tau))
    + s.integrate(q_late, (t, tau, 2 * tau))
)
target_q_integral = U * (1 - s.exp(-lam * tau)) ** 2 / lam**2
assert s.simplify(q_integral - target_q_integral) == 0
c_ohmic = 2 * beta * a * gamma * U**2 * q_integral
assert s.simplify(
    c_ohmic
    - 2 * beta * a * gamma * U**3
    * (1 - s.exp(-lam * tau)) ** 2 / lam**2
) == 0

# A saturating sensor reports a cubic contrast from a linear field.
F = lambda x: x / (1 + (x / Bs) ** 2)
k_sensor = s.series(
    (F(r * d * U) - F(-r * d * U))
    - r * (F(d * U) - F(-d * U)),
    U,
    0,
    5,
).removeO()
assert s.simplify(
    k_sensor + 2 * (r**3 - r) * d**3 * U**3 / Bs**2
) == 0

print("thermal gating: exact formula and cubic amplitude contrast PASS")
print("ohmic heating: exact pulse integral and cubic contrast PASS")
print("sensor saturation: cubic false positive PASS")
