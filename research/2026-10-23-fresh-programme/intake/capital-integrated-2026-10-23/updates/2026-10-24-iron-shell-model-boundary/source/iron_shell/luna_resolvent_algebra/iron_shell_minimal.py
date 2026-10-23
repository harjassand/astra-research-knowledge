"""Exact toy checks for Fe/FeO spherical eigenstrain and pressure-pulse bookkeeping.

Assumptions are documented in IRON_SHELL_MODEL.md. Numerical cases are
illustrative only, not fitted or measured iron/oxide material models.
"""
import sympy as sp

K, G, e, a, b, R, r = sp.symbols("K G e a b R r", positive=True)


def displacement(A, B, radius):
    return A * radius + B / radius**2


def sigma_radial(A, B, eigen, radius):
    return 3 * K * (A - eigen) - 4 * G * B / radius**3


def sigma_hoop(A, B, eigen, radius):
    return 3 * K * (A - eigen) + 2 * G * B / radius**3


# Two-layer outside-only oxidation: Fe core (zero eigenstrain) plus FeO skin.
Ac, Cc, Dc = sp.symbols("Ac Cc Dc")
two_layer_conditions = [
    sp.Eq(displacement(Ac, 0, a), displacement(Cc, Dc, a)),
    sp.Eq(sigma_radial(Ac, 0, 0, a), sigma_radial(Cc, Dc, e, a)),
    sp.Eq(sigma_radial(Cc, Dc, e, R), 0),
]
two_layer_solution = sp.solve(
    two_layer_conditions, [Ac, Cc, Dc], dict=True, simplify=True
)[0]
core_hydrostatic = sp.factor(3 * K * two_layer_solution[Ac])
expected_core = 12 * K * G * e * (R**3 - a**3) / (R**3 * (4 * G + 3 * K))
skin_hoop = sp.factor(sigma_hoop(Cc, Dc, e, r).subs(two_layer_solution))
expected_skin_hoop = (
    -6 * K * G * a**3 * e * (R**3 + 2 * r**3)
    / (R**3 * r**3 * (4 * G + 3 * K))
)
assert sp.simplify(core_hydrostatic - expected_core) == 0
assert sp.simplify(skin_hoop - expected_skin_hoop) == 0

# Equal-modulus, three-layer sphere: FeO core (eigenstrain e), Fe shell
# (zero eigenstrain), FeO outer skin (eigenstrain e), free outside surface.
A1, A2, B2, A3, B3 = sp.symbols("A1 A2 B2 A3 B3")
conditions = [
    sp.Eq(displacement(A1, 0, a), displacement(A2, B2, a)),
    sp.Eq(sigma_radial(A1, 0, e, a), sigma_radial(A2, B2, 0, a)),
    sp.Eq(displacement(A2, B2, b), displacement(A3, B3, b)),
    sp.Eq(sigma_radial(A2, B2, 0, b), sigma_radial(A3, B3, e, b)),
    sp.Eq(sigma_radial(A3, B3, e, R), 0),
]
solution = sp.solve(conditions, [A1, A2, B2, A3, B3], dict=True, simplify=True)[0]
fe_radial = sp.factor(sigma_radial(A2, B2, 0, r).subs(solution))
fe_hoop = sp.factor(sigma_hoop(A2, B2, 0, r).subs(solution))
expected_radial = (
    12 * K * G * e / (R**3 * (4 * G + 3 * K))
    * (R**3 + a**3 - b**3 - R**3 * a**3 / r**3)
)
expected_hoop = (
    6 * K * G * e / (R**3 * (4 * G + 3 * K))
    * (2 * (R**3 + a**3 - b**3) + R**3 * a**3 / r**3)
)
assert sp.simplify(fe_radial - expected_radial) == 0
assert sp.simplify(fe_hoop - expected_hoop) == 0

# Exact two-layer toy, normalized K=G=1, e=1%, oxidized skin starts at a/R=0.9.
two_fixture = {K: 1, G: 1, e: sp.Rational(1, 100), a: sp.Rational(9, 10), R: 1}
print("equal-modulus two-layer outside-only oxidation; normalized stress units")
print("Fe-core hydrostatic tension=", sp.factor(core_hydrostatic.subs(two_fixture)))
print("FeO-skin hoop stress at outside=", sp.factor(skin_hoop.subs({**two_fixture, r: 1})))

# Exact three-layer toy, normalized K=G=1, e=1%, a/R=1/2, b/R=9/10.
fixture = {K: 1, G: 1, e: sp.Rational(1, 100), a: sp.Rational(1, 2), b: sp.Rational(9, 10), R: 1}
print("equal-modulus three-layer toy; normalized stress units")
for radius in (sp.Rational(1, 2), sp.Rational(7, 10), sp.Rational(9, 10)):
    subs = {**solution, **fixture, r: radius}
    sr = sp.factor(sigma_radial(A2, B2, 0, r).subs(subs))
    sh = sp.factor(sigma_hoop(A2, B2, 0, r).subs(subs))
    print(f"Fe shell r={radius}: sigma_r={sr}; sigma_theta={sh}")
core_stress = sp.factor((3 * K * (solution[A1] - e)).subs(fixture))
print(f"FeO-core hydrostatic stress={core_stress}")

# Check stoichiometric gas accounting for FeO + H2 -> Fe + H2O.
xi, L, pw, ph, yw, yh, Pe, RT, V = sp.symbols(
    "xi L pw ph yw yh Pe RT V", real=True
)
dnw = xi - L * (pw - yw * Pe)
dnh = -xi - L * (ph - yh * Pe)
dP = sp.factor(RT / V * (dnw + dnh))
assert sp.simplify(dP + RT * L / V * (pw + ph - Pe * (yw + yh))) == 0
print("equal-permeance total-pressure balance:", dP)

# Step-down pulse at fixed external composition, fixed pore volume, equal species
# permeance, and zero independent net-gas/condensed-water source.
deltaP, pulse_time, tau = sp.symbols("deltaP pulse_time tau", positive=True)
delta_during = deltaP * sp.exp(-pulse_time / tau)
delta_just_after_return = delta_during - deltaP
print("downstep differential at pulse end:", delta_during)
print("differential immediately after return:", delta_just_after_return)
assert sp.limit(delta_during, pulse_time, 0, dir="+") == deltaP
assert sp.limit(delta_during, pulse_time, sp.oo) == 0
assert sp.limit(delta_just_after_return, pulse_time, 0, dir="+") == 0
assert sp.limit(delta_just_after_return, pulse_time, sp.oo) == -deltaP

# Thin spherical membrane criterion: sigma_theta = deltaP * R/(2 h).
deltaP, sig_eff, h, Rp = sp.symbols("deltaP sig_eff h Rp", positive=True)
threshold = sp.solve(sp.Eq(deltaP * Rp / (2 * h), sig_eff), deltaP)[0]
assert sp.simplify(threshold - 2 * sig_eff * h / Rp) == 0
print("ideal thin spherical-shell threshold deltaP =", threshold)
