#!/usr/bin/env python3
"""Exact reconstruction of the r=1 acoustic/shear-elimination identities.

This is a symbolic identity checker, not a quasiconvexity decision procedure.
It uses only SymPy and the Python standard library. No inherited verifier is
imported. Run from any directory; its receipt is written alongside this file.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as S

ROOT = Path(__file__).resolve().parent
checks = []


def check(name, expression):
    if isinstance(expression, S.MatrixBase):
        residual = expression.applyfunc(lambda e: S.factor(S.expand(e)))
        assert residual == S.zeros(*residual.shape), (name, residual)
    else:
        residual = S.factor(S.expand(expression))
        assert residual == 0, (name, residual)
    checks.append({"name": name, "status": "PASS", "method": "exact symbolic identity"})


def avg_z(expression, variable):
    return S.factor(S.expand(expression).coeff(variable, 0))


a, b, c, d, h, s, jvar = S.symbols("a b c d h s jvar", real=True)
V = S.Matrix([a, b, c, d])
j = a*d-b*c
J = ((a-d)**2+(b+c)**2)**2/S.Integer(8)+j*j+(a*a+c*c)*j
Cv = a**3+5*a*a*d-4*a*b*c+a*c*c+2*a*d*d-2*b*c*d+c*c*d
e = 2*a+d
Qv = e*e+c*c
Pv = S.Rational(3, 2)*(b+c)**2+S.Rational(1, 2)*(a-d)**2+2*c*c
Nv = S.diff(J, b)
Mv = c*e

shift = J.subs({a: a+s, d: d+s}, simultaneous=True)-2*s**4
check("conformal Taylor expansion with determinant and linear terms",
      shift-J-s*Cv-s*s*(Qv+3*j)-s**3*(5*a+3*d))
check("cubic invariant expression", Cv-((a*a+c*c)*(a+d)+2*e*j))
check("shear quartic expansion before horizontal averaging",
      J.subs(b, b+h)-J-h*Nv-h*h*Pv/2-h**3*(b+c)/2-h**4/8)
check("shear change of cubic source", Cv.subs(b, b+h)-Cv+2*h*Mv)
check("shear independence of conformal quadratic form", Qv.subs(b, b+h)-Qv)
check("positive joint shear-background quadratic completion",
      Qv*s*s-2*s*h*Mv+Pv*h*h/2
      -((s*e-h*c)**2+s*s*c*c+S.Rational(3, 4)*h*h*(b+c)**2
        +S.Rational(1, 4)*h*h*(a-d)**2))
check("explicit cubic shear source",
      Nv-((b+c)**3/2+(a-d)**2*(b+c)/2+2*c*c*(b+c)
          -c*(2*a*d+a*a+3*c*c)))

# Pointwise coercivity is reconstructed from the Gram variables, with the
# physical constraint x^2+y^2 <= 1 stated and proved in REPORT.md.
u, v, w, jj = S.symbols("u v w jj", real=True)
Jgram = (u+v)**2/8+S.Rational(3, 2)*jj*jj+(u-v)*jj/2
check("Gram expression of the unchanged integrand",
      J-Jgram.subs({u: a*a+c*c, v: b*b+d*d, jj: j}, simultaneous=True))
check("Gram determinant identity", (a*a+c*c)*(b*b+d*d)-(a*b+c*d)**2-j*j)
lam = (3-S.sqrt(13))/2
check("coercivity eigenvalue", lam*lam-3*lam-1)

# Independent rank-one convexity proof, not imported from the source package.
z, P0, Q0, X0, Y0 = S.symbols("z P0 Q0 X0 Y0", real=True)
direction = S.Matrix([1, z, 0, 0])
acoustic = S.expand((direction.T*S.hessian(J, V)*direction)[0])
acoustic = acoustic.subs({a: (P0+X0)/2, b: (Y0-Q0)/2,
                         c: (Y0+Q0)/2, d: (P0-X0)/2}, simultaneous=True)
G = S.simplify(S.hessian(acoustic, (P0, Q0, X0, Y0))/2)
Ac = S.Matrix([[2, -z], [-z, (z*z+1)/2]])
Schur = S.Matrix([[S.Rational(3, 8)*(z*z+1), S.Rational(3, 4)*z],
                  [S.Rational(3, 4)*z, S.Rational(3, 2)*z*z]])
check("rank-one acoustic conformal block", G[:2, :2]-Ac)
check("rank-one acoustic conformal block determinant", Ac.det()-1)
check("rank-one acoustic Schur complement",
      G[2:4, 2:4]-G[2:4, :2]*Ac.inv()*G[:2, 2:4]-Schur)
check("rank-one acoustic Schur determinant", Schur.det()-S.Rational(9, 16)*z**4)
check("rank-one acoustic full determinant", G.det()-S.Rational(9, 16)*z**4)

# The scalar conjugate is evaluated at a root rather than manipulating a
# potentially branch-sensitive Cardano formula.
pp, zz, hh = S.symbols("pp zz hh", real=True)
gp = hh**4/8+pp*hh*hh/2
root_value = hh**3/2+pp*hh
check("scalar convex conjugate at its unique root",
      root_value*hh-gp-(S.Rational(3, 8)*hh**4+pp*hh*hh/2))
check("scalar root derivative", S.diff(gp, hh)-root_value)

# Complex-variable chart: xi=f_x, q=f_x+i f_y=2 f_bar-z.
qr, qi = a-d, b+c
rho = a*a+c*c
ell = a*qr+c*qi
check("complex derivative polynomial",
      J-(2*rho*rho-3*rho*ell+ell*ell+(qr*qr+qi*qi)**2/8))

# An infinite-dimensional separable divergence-free potential family:
# psi=(-G' F/2, G F'), with arbitrary smooth periodic F and G.
F, F1, F2, G0, G1, G2 = S.symbols("F F1 F2 G0 G1 G2", real=True)
potential_sub = {a: -G1*F1/2, b: -G2*F/2, c: G0*F2, d: G1*F1}
check("potential family has e identically zero", e.subs(potential_sub, simultaneous=True))
check("potential family cubic before averaging",
      Cv.subs(potential_sub, simultaneous=True)-G1**3*F1**3/8-G1*G0**2*F1*F2**2/2)
Npot = (-G2**3*F**3/16+3*G2**2*G0*F**2*F2/8
        -7*G2*G0**2*F*F2**2/4-G0**3*F2**3/2
        -9*G1**2*G2*F*F1**2/16+15*G1**2*G0*F1**2*F2/8)
check("potential family cubic shear source", Nv.subs(potential_sub, simultaneous=True)-Npot)

# A non-half-period-symmetric, phase-resolved exact profile. Its quartic
# moments are phase-blind but its two cubic sources have distinct phases.
Z = S.symbols("Z", nonzero=True)
t, rphase, beta = S.symbols("t rphase beta", real=True)
sin1 = (Z-Z**-1)/(2*S.I)
cos1 = (Z+Z**-1)/2
sin2 = (Z**2-Z**-2)/(2*S.I)
cos2 = (Z**2+Z**-2)/2
Fz = sin1+t*sin2+rphase*cos2
F1z = cos1+2*t*cos2-2*rphase*sin2
F2z = -sin1-4*t*sin2-4*rphase*cos2
profile_sub = {F: Fz, F1: F1z, F2: F2z}
nu = t*t+rphase*rphase
moment_formulas = {
    "F2": ((1+nu)/2, Fz**2),
    "F1_2": ((1+4*nu)/2, F1z**2),
    "F2_2": ((1+16*nu)/2, F2z**2),
    "F3": (-3*rphase/4, Fz**3),
    "F_F1_2": (-3*rphase/4, Fz*F1z**2),
    "F_F2_2": (-9*rphase/4, Fz*F2z**2),
    "F2_3": (3*rphase, F2z**3),
    "F1_3": (3*t/2, F1z**3),
    "F1_F2_2": (3*t/2, F1z*F2z**2),
    "F1_2_F2": (0, F1z**2*F2z),
}
for name, (answer, expression) in moment_formulas.items():
    check("phase profile moment "+name, avg_z(expression, Z)-answer)
Nanswer = rphase*(3*G2**3/64+9*G2**2*G0/16+27*G1**2*G2/64
                 +63*G2*G0**2/16-3*G0**3/2)
Nactual = avg_z(Npot.subs(profile_sub, simultaneous=True), Z)
check("non-half-period profile shear source", Nactual-Nanswer)
Panswer = (7*(1+16*nu)*G0**2/4+3*(1+4*nu)*G0*G2/4
           +3*(1+nu)*G2**2/16+9*(1+4*nu)*G1**2/16)
Pactual = avg_z(Pv.subs(potential_sub, simultaneous=True)
                .subs(profile_sub, simultaneous=True), Z)
check("non-half-period profile positive quadratic weight", Pactual-Panswer)

Jx = avg_z(J.subs(potential_sub, simultaneous=True)
           .subs(profile_sub, simultaneous=True), Z)
W = S.symbols("W", nonzero=True)
gs = (W-W**-1)/(2*S.I)+beta*(W**2-W**-2)/(2*S.I)
gp1 = (W+W**-1)/2+beta*(W**2+W**-2)
gp2 = -(W-W**-1)/(2*S.I)-2*beta*(W**2-W**-2)/S.I
Aprofile = avg_z(Jx.subs({G0: gs, G1: gp1, G2: gp2}, simultaneous=True), W)
B2 = beta*beta
Aanswer = (422912*nu**2*B2**2+699008*nu**2*B2+75713*nu**2
           +401408*nu*B2**2+572672*nu*B2+43688*nu
           +20288*B2**2+25088*B2+1652)/8192
check("non-half-period profile exact quartic energy", Aprofile-Aanswer)
Cprofile = avg_z(avg_z(Cv.subs(potential_sub, simultaneous=True)
                 .subs(profile_sub, simultaneous=True), Z)
                 .subs({G0: gs, G1: gp1, G2: gp2}, simultaneous=True), W)
check("non-half-period profile conformal cubic source", Cprofile-9*t*beta/32)
Qprofile = avg_z(avg_z(Qv.subs(potential_sub, simultaneous=True)
                 .subs(profile_sub, simultaneous=True), Z)
                 .subs({G0: gs, G1: gp1, G2: gp2}, simultaneous=True), W)
check("non-half-period profile exact quadratic energy",
      Qprofile-(1+B2)*(1+16*nu)/4)
check("profile weight even in vertical coordinate", Panswer.subs({G0: -G0, G2: -G2})-Panswer)
check("profile shear source odd in vertical coordinate", Nanswer.subs({G0: -G0, G2: -G2})+Nanswer)

# Opposite determinant-sign conformal contact and its independent acoustic
# shear. This does not import a transformation-equivalence premise.
CD = S.diff(J, a)-S.diff(J, d)
fD = a-2*d
QD = fD*fD+b*b
PD = (a+d)**2/2+S.Rational(3, 2)*(c-b)**2+2*b*b
ND = S.diff(J, c)
MD = -b*fD
shiftD = J.subs({a: a+s, d: d-s}, simultaneous=True)-2*s**4
check("opposite-sign conformal expansion",
      shiftD-J-s*CD-s*s*(QD-3*j)-s**3*(3*a-5*d))
check("opposite-sign shear quartic expansion before vertical averaging",
      J.subs(c, c+h)-J-h*ND-h*h*PD/2-h**3*(c-b)/2-h**4/8)
check("opposite-sign shear change of cubic source", CD.subs(c, c+h)-CD+2*h*MD)
check("opposite-sign shear independence of quadratic form", QD.subs(c, c+h)-QD)
check("opposite-sign positive joint quadratic completion",
      QD*s*s-2*s*h*MD+PD*h*h/2
      -((s*fD+h*b)**2+s*s*b*b+S.Rational(3, 4)*h*h*(c-b)**2
        +S.Rational(1, 4)*h*h*(a+d)**2))

# Two-axis attempted extension: exact compatible positive-energy countermodel
# to joint convexity in both independent acoustic shear amplitudes.
Hamp, Kamp = S.symbols("Hamp Kamp", real=True)
two_shear_energy = S.Rational(3, 64)*(Hamp**4+Kamp**4)+S.Rational(7, 16)*Hamp**2*Kamp**2
two_shear_direct = avg_z(avg_z(J.subs({a: 0, b: Hamp*(W+W**-1)/2,
                                                     c: Kamp*(Z+Z**-1)/2, d: 0}, simultaneous=True), Z), W)
check("compatible two-shear exact energy", two_shear_direct-two_shear_energy)
two_shear_Hess = S.hessian(two_shear_energy, (Hamp, Kamp)).subs({Hamp: 1, Kamp: 1})
check("two-shear Hessian", two_shear_Hess-S.Matrix([[S.Rational(23, 16), S.Rational(7, 4)],
                                                                  [S.Rational(7, 4), S.Rational(23, 16)]]))
check("two-shear negative Hessian eigenvalue",
      two_shear_Hess*S.Matrix([1, -1])+S.Rational(5, 16)*S.Matrix([1, -1]))

# The entire separable divergence-free architecture is excluded by an
# analytic integration identity and this exact pointwise SOS. The global
# integration-by-parts steps are spelled out in REPORT.md, not assumed from
# checking finitely many profiles.
J_e0 = J.subs(d, -2*a)
separable_sos = (97*(a*a+S.Rational(30, 97)*b*c)**2+2*a*a*c*c
                 +(b*b+2*b*c-c*c)**2+S.Rational(264, 97)*b*b*c*c)
check("divergence-free quartic SOS controlling separable cubic",
      8*(J_e0-S.Rational(9, 4)*a*a*b*b)-separable_sos)
check("separable cubic integration-by-parts coefficient",
      S.Rational(1, 8)-2*S.Rational(1, 4)*S.Rational(1, 2)*S.Rational(1, 2))

# Nonseparable scalar-Hessian fixture. All its coefficients are reconstructed
# from its actual compatible potential, including the remaining mean-zero
# shear source, not from an arbitrary probability distribution of matrices.
Uamp, Vamp, Tamp = S.symbols("Uamp Vamp Tamp", real=True)
cx = (Z+Z**-1)/2
cxy = (Z*W+(Z*W)**-1)/2
c2xy = (Z**2*W+(Z**2*W)**-1)/2
nonsep = {a: Vamp*cxy/2+Tamp*c2xy,
          b: Vamp*cxy/2+Tamp*c2xy/2,
          c: -Uamp*cx-Vamp*cxy-4*Tamp*c2xy,
          d: -Vamp*cxy-2*Tamp*c2xy}
nonsep_mean = lambda expression: avg_z(avg_z(expression.subs(nonsep, simultaneous=True), Z), W)
check("nonseparable potential has e=0", e.subs(nonsep, simultaneous=True))
check("nonseparable conformal cubic source", nonsep_mean(Cv)+S.Rational(3, 2)*Tamp*Uamp*Vamp)
check("nonseparable failure of separable cubic cancellation",
      nonsep_mean(Cv-8*a*b*c))
check("nonseparable exact quadratic energy",
      nonsep_mean(Qv)-(16*Tamp*Tamp+Uamp*Uamp+Vamp*Vamp)/2)
An = (21675*Tamp**4+4016*Tamp*Tamp*Uamp*Uamp+9616*Tamp*Tamp*Vamp*Vamp
      +48*Uamp**4+512*Uamp*Uamp*Vamp*Vamp+300*Vamp**4)/1024
check("nonseparable exact quartic energy", nonsep_mean(J)-An)
P0n = (439*Tamp*Tamp+28*(Uamp*Uamp+Vamp*Vamp))/16
P1n = S.Rational(11, 4)*Uamp*Vamp
N0n = S.Rational(85, 16)*Tamp*Uamp*Vamp
N1n = Tamp*(31*Uamp*Uamp+30*Vamp*Vamp)/16
check("nonseparable exact variable quadratic weight",
      avg_z(Pv.subs(nonsep, simultaneous=True), Z)-P0n-P1n*(W+W**-1)/2)
check("nonseparable exact variable cubic shear source",
      avg_z(Nv.subs(nonsep, simultaneous=True), Z)-N0n-N1n*(W+W**-1)/2)
xx, yy, zz3 = S.symbols("xx yy zz3", nonnegative=True)
Bn = xx/2+S.Rational(9, 8)*yy+S.Rational(21, 2)*zz3
bound_poly = S.Poly(S.expand((16*zz3+xx+yy)*Bn*Bn), xx, yy, zz3)
check("nonseparable positive bound xyz coefficient",
      bound_poly.coeff_monomial(xx*yy*zz3)-S.Rational(417, 8))
assert all(coef >= 0 for coef in bound_poly.coeffs())
checks.append({"name": "nonseparable bound has no negative coefficients",
               "status": "PASS", "method": "exact rational coefficient signs"})
check("nonseparable affine loss bound coefficient",
      S.Rational(9, 8)/S.Rational(417, 8)-S.Rational(3, 139))
check("nonseparable positive margin elementary comparison",
      S.Rational(1, 16)-S.Rational(3, 139)-S.Rational(91, 2224))

receipt = {
    "schema": "fz-positive-shear-reduction-check-v1",
    "status": "ALL_EXACT_IDENTITY_GROUPS_PASS",
    "integrand": "J_1, unchanged alpha=1/8",
    "group_count": len(checks),
    "checks": checks,
    "scope": "Symbolic algebra plus analytic proof in REPORT.md; no all-gradient source inequality is certified.",
    "quasiconvexity_at_I": "UNRESOLVED",
    "compatible_counterexample": "NOT_FOUND",
    "historical_originality": "UNKNOWN",
    "sympy_version": S.__version__,
}
receipt["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(ROOT/"VERIFICATION_RECEIPT.json").write_text(json.dumps(receipt, indent=2)+"\n")
print(json.dumps({"status": receipt["status"], "groups": len(checks),
                  "receipt": str(ROOT/"VERIFICATION_RECEIPT.json")}, indent=2))
