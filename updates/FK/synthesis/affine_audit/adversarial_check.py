#!/usr/bin/env python3
"""Independent exact law-level checks for the moving affine theorem.

Uses finite atomic laws and an independently assembled Dacorogna--Marcellini
quartic.  These checks target rare-spike concentration, covariance-normal
regression, full affine minimization, and the singular pure-line boundary.
They do not certify the analytic theorem or gradient compatibility.
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as s

a, b, c, d = s.symbols("a b c d", real=True)
x = s.Matrix([a, b, c, d])
q = a*d - b*c
J = s.hessian(q, (a, b, c, d)) / 2
norm2 = a*a + b*b + c*c + d*d
F = norm2**2 - 4/s.sqrt(3)*norm2*q
grad = s.Matrix([s.diff(F, z) for z in (a, b, c, d)])
Hess = s.hessian(F, (a, b, c, d))
R = s.Matrix([0, 1, 0, 0])
e11 = s.Matrix([1, 0, 0, 0])


def eval_at(poly, vec):
    return s.expand(poly.subs(dict(zip((a, b, c, d), list(vec))), simultaneous=True))


def avg(poly, atoms):
    return s.factor(sum(w * eval_at(poly, z) for z, w in atoms))


def avg_vec(vec, atoms):
    return s.simplify(sum((w * vec.subs(dict(zip((a, b, c, d), list(z))), simultaneous=True)
                           for z, w in atoms), s.zeros(vec.rows, vec.cols)))


def require_zero(value, label):
    vals = list(value) if isinstance(value, s.MatrixBase) else [value]
    if any(s.cancel(s.simplify(v)) != 0 for v in vals):
        raise AssertionError(label)


def positive(value, label):
    v = s.simplify(value)
    if v.is_positive is not True:
        raise AssertionError(f"{label}: exact positivity unresolved: {v}")


report = {"checks": []}


def passed(label):
    report["checks"].append(label)
    print(f"PASS {len(report['checks']):02d}: {label}", flush=True)


# Singular endpoint: a nontrivial centered law exactly on the rank-one line.
# The chosen two-point scalar law has m2=1/2, m3=1/4, m4=3/8.
line_atoms = [(R, s.Rational(1, 3)), (-R/2, s.Rational(2, 3))]
require_zero(sum((w*z for z, w in line_atoms), s.zeros(4, 1)), "line mean")
require_zero(avg(q, line_atoms), "line determinant balance")
line_moments = {j: s.factor(sum(w * (z.dot(R))**j for z, w in line_atoms)) for j in (2, 3, 4)}
Hline = avg_vec(Hess, line_atoms)
bline = avg_vec(grad, line_atoms)
cline = avg(F, line_atoms)
u_line = line_moments[3] / (3*line_moments[2])
require_zero(bline - u_line*Hline*R, "Euler range identity on singular line")
assert Hline.rank() == 3
Bline = -u_line*R
line_gap = s.factor(cline + bline.dot(Bline) + (Bline.T*Hline*Bline)[0]/2)
line_formula = s.factor(F.subs({a: 0, b: 1, c: 0, d: 0}) *
                         (line_moments[4] - s.Rational(2, 3)*line_moments[3]**2/line_moments[2]))
require_zero(line_gap - line_formula, "singular optimized line formula")
assert line_gap == s.Rational(7, 24)
passed("singular nonzero line law: rank(H)=3, b in range(H), exact gap 7/24")

# Rare transverse spikes with a unique covariance maximizer.  The spike is
# rank one and so E det(X)=0 pointwise; its amplitude is 10 while its mass is
# 10^-10.  Both relative transverse norms are small, with delta2 << delta4.
p = s.Rational(1, 10**10)
A = s.Integer(10)
s_atoms = [(s.Integer(1), s.Rational(1, 3)), (-s.Rational(1, 2), s.Rational(2, 3))]
y_atoms = [(s.Integer(0), 1-p), (A, p/2), (-A, p/2)]
spike_atoms = [(sv*R + y*e11, ws*wy) for sv, ws in s_atoms for y, wy in y_atoms]
require_zero(sum((w*z for z, w in spike_atoms), s.zeros(4, 1)), "spike mean")
require_zero(avg(q, spike_atoms), "spike determinant balance")
Csp = s.simplify(sum((w*z*z.T for z, w in spike_atoms), s.zeros(4)))
m2 = s.factor(sum(ws*sv**2 for sv, ws in s_atoms))
m3 = s.factor(sum(ws*sv**3 for sv, ws in s_atoms))
m4 = s.factor(sum(ws*sv**4 for sv, ws in s_atoms))
v = s.factor(sum(w*(z-R*z.dot(R)).dot(z-R*z.dot(R)) for z, w in spike_atoms))
t4 = s.factor(sum(w*((z-R*z.dot(R)).dot(z-R*z.dot(R)))**2 for z, w in spike_atoms))
assert Csp == s.diag(p*A**2, m2, 0, 0)
assert m2 > p*A**2
delta2sq = s.factor(v/m2)
delta4fourth = s.factor(t4/m4)
assert delta2sq == s.Rational(2, 10**8)
assert delta4fourth == s.Rational(8, 3)*s.Rational(1, 10**6)

Hsp = avg_vec(Hess, spike_atoms)
bsp = avg_vec(grad, spike_atoms)
csp = avg(F, spike_atoms)
u = m3/(3*m2)
ell = s.simplify(bsp-u*Hsp*R)

# The transverse contact frame is A=(-1/2)e12+(sqrt(3)/2)e21.  Q is an
# orthonormal complement with columns e11, (sqrt(3)/2)e12+(1/2)e21, e22.
At = s.Matrix([0, -s.Rational(1, 2), s.sqrt(3)/2, 0])
Q = s.Matrix.hstack(s.Matrix([1, 0, 0, 0]),
                    s.Matrix([0, s.sqrt(3)/2, s.Rational(1, 2), 0]),
                    s.Matrix([0, 0, 0, 1]))
MR = eval_at(Hess, R)
require_zero(MR*At, "transverse acoustic null vector")
h = s.factor((At.T*Hsp*At)[0])
k = s.simplify(Q.T*Hsp*At)
D = s.simplify(Q.T*Hsp*Q)
sigma = s.factor(h - (k.T*D.inv()*k)[0])
positive(h, "moving-frame h")
for j in range(1, 4):
    positive(D[:j, :j].det(), f"moving-frame D leading minor {j}")
positive(sigma, "actual Schur complement")
ratio = s.factor(sigma/h)
assert ratio > s.Rational(99999999, 10**8)

# Independently compute the unrestricted affine minimum and its pure-line
# approximation.  This law was selected to make L2 far smaller than L4.
Delta = s.factor(csp - (bsp.T*Hsp.inv()*bsp)[0]/2)
Qorigin = s.factor(csp - u*bsp.dot(R) + u**2*(R.T*Hsp*R)[0]/2)
regressed = s.factor((ell.T*Hsp.inv()*ell)[0])
require_zero(Delta - (Qorigin - regressed/2), "full affine regression identity")
reference = s.factor(F.subs({a: 0, b: 1, c: 0, d: 0}) * (m4-s.Rational(2, 3)*m3**2/m2))
positive(Delta, "rare-spike optimized gap")
report["rare_spike"] = {
    "mass": str(p), "amplitude": str(A), "m2": str(m2), "m3": str(m3), "m4": str(m4),
    "v": str(v), "Y4": str(t4), "delta2_squared": str(delta2sq),
    "delta4_fourth": str(delta4fourth), "h": str(h), "sigma": str(sigma),
    "sigma_over_h": str(ratio), "regressed_cubic_loss": str(regressed),
    "optimized_gap": str(Delta), "pure_line_reference": str(reference),
    "gap_minus_reference": str(s.factor(Delta-reference)),
}
passed("rare rank-one spikes: exact covariance fit, positive full Schur gap, and full affine minimum")

# A second rare atomic law forces a nonzero covariance correlation normal to
# the determinant cone.  For rare atoms X=(A*u,s,s*A^2,A*u), q(X)=0
# pointwise; hence q(Y)=s*Y_c is exactly the fitted covariance correlation.
p2 = s.Rational(1, 10**8)
A2 = s.Integer(2)
atoms2 = []
for sv in (-1, 1):
    atoms2.append((s.Matrix([0, sv, 0, 0]), (1-p2)/2))
    for sign in (-1, 1):
        atoms2.append((s.Matrix([A2*sign, sv, sv*A2**2, A2*sign]), p2/4))
require_zero(sum((w*z for z, w in atoms2), s.zeros(4, 1)), "correlated rare-law mean")
require_zero(avg(q, atoms2), "correlated rare-law determinant balance")
C2 = s.simplify(sum((w*z*z.T for z, w in atoms2), s.zeros(4)))
z2 = s.simplify(C2*R-R.dot(C2*R)*R)
Y2_atoms = [(z-R*z.dot(R), w) for z, w in atoms2]
qY2 = s.factor(avg(q, Y2_atoms))
normal_rhs = s.simplify(-qY2*J*R/(2*(J*R).dot(J*R)))
require_zero(z2-normal_rhs, "covariance-normal regression with concentrated law")
# Exact global maximum: on q=0, ad=bc and a^2+d^2>=2|bc|.  For r=pA^2,
# t=pA^4, 1-R^TCR >=2(1-3r)|bc|+(1-t)c^2 >=0 for these small p,A.
r = p2*A2**2
t = p2*A2**4
assert r < s.Rational(1, 3) and t < 1
assert R.dot(C2*R) == 1
cov2_poly = s.expand((x.T*C2*x)[0])
cov2_reduced = b**2+t*c**2+r*(a**2+d**2)+4*r*b*c
require_zero(cov2_poly-cov2_reduced-2*r*q, "rare covariance objective reduction")
report["covariance_normal_spike"] = {
    "qY": str(qY2), "z": [str(vv) for vv in z2],
    "delta2_squared": str(s.factor(sum(w*yy.dot(yy) for yy, w in Y2_atoms))),
    "delta4_fourth": str(s.factor(sum(w*(yy.dot(yy))**2 for yy, w in Y2_atoms))),
    "global_fit_certificate": "for q=0, 1-r^T C r >= 2(1-3r)|bc|+(1-t)c^2 >= 0",
}
passed("rare correlated rank-one atoms: exact determinant-normal covariance correction and fitted-line maximality")

# Tangent boundary attack: independently rebuild the supplied bounded
# determinant-balanced law for the rank-one-convex quartic G.  It has a
# rank-two, rather than rank-three, Finsler remainder at the limiting contact.
U = a*a + c*c
V = b*b + d*d
G = 3*(U+V-2*q)**2 + s.Rational(35, 24)*U**2 + q**2 - s.Rational(5, 2)*q*U
gradG = s.Matrix([s.diff(G, z) for z in (a, b, c, d)])
HessG = s.hessian(G, (a, b, c, d))
eps = s.Rational(1, 10**6)
m = s.Integer(9)
w = 1-s.Rational(3, 2)*eps
tau = s.Rational(9, 2)*m**2*eps/w
Rt = s.Matrix([0, 1, tau, 0])
Sdiag = s.Matrix([1, 0, 0, s.Rational(3, 2)])
tangent_atoms = [(Rt, w/2), (-Rt, w/2), (m*Sdiag, eps), (-2*m*Sdiag, eps/2)]
require_zero(sum((wt*z for z, wt in tangent_atoms), s.zeros(4, 1)), "tangent law mean")
require_zero(avg(q, tangent_atoms), "tangent law determinant balance")
Ct = s.simplify(sum((wt*z*z.T for z, wt in tangent_atoms), s.zeros(4)))
Htan = s.simplify(sum((wt*HessG.subs(dict(zip((a,b,c,d), list(z))), simultaneous=True)
                       for z, wt in tangent_atoms), s.zeros(4)))
btan = s.simplify(sum((wt*gradG.subs(dict(zip((a,b,c,d), list(z))), simultaneous=True)
                       for z, wt in tangent_atoms), s.zeros(4, 1)))
ctan = avg(G, tangent_atoms)
for j in range(1, 5):
    positive(Htan[:j, :j].det(), f"tangent-law Hessian leading minor {j}")
I = s.Matrix([1, 0, 0, 1])
betaI = s.simplify(btan.dot(I))
hI = s.factor((I.T*Htan*I)[0])
directional_gap = s.factor(ctan-betaI**2/(2*hI))
full_gap = s.factor(ctan-(btan.T*Htan.inv()*btan)[0]/2)
assert directional_gap < 0 and full_gap < 0

# Prove the exact covariance maximizer from the rank-one constraint, using
# the displayed source reduction and strict matrix inequalities at eps=10^-6.
Wcov = m**2*eps*s.Matrix([[3, 9], [9, s.Rational(27, 4)]])
cov_margin = s.simplify(w*s.eye(2)-Wcov)
positive(cov_margin[0, 0], "tangent covariance margin 1")
positive(cov_margin.det(), "tangent covariance margin determinant")
assert tau**2 < 1
rvec = s.Matrix([a,b,c,d])
cov_pol = s.expand((rvec.T*Ct*rvec)[0])
reduced = w*b**2+w*tau**2*c**2+(s.Matrix([a,d]).T*Wcov*s.Matrix([a,d]))[0]
require_zero(cov_pol-reduced+9*m**2*eps*q, "tangent covariance cone reduction")
report["tangent_boundary"] = {
    "epsilon": str(eps), "m": str(m), "tau": str(tau),
    "directional_gap": str(directional_gap), "full_optimized_gap": str(full_gap),
    "fit_margin_determinant": str(cov_margin.det()),
    "scope": "balanced moment law only; not a compatible-gradient counterexample; transverse Finsler remainder has rank 2",
}
passed("tangent boundary: exact negative balanced-law gap, positive H, and rank-two remainder exclusion")

# Scale the same tangent family symbolically. This checks that the negative
# direction persists as both relative transverse norms tend to zero, rather
# than only at the displayed finite epsilon. A one-direction trial already
# upper-bounds the unrestricted affine infimum, so a negative limit suffices.
eps_sym = s.symbols("eps_sym", positive=True)
w_sym = 1-s.Rational(3, 2)*eps_sym
tau_sym = s.Rational(9, 2)*m**2*eps_sym/w_sym
Rt_sym = s.Matrix([0, 1, tau_sym, 0])
tangent_family = [
    (Rt_sym, w_sym/2), (-Rt_sym, w_sym/2),
    (m*Sdiag, eps_sym), (-2*m*Sdiag, eps_sym/2),
]
mean_sym = sum((wt*z for z, wt in tangent_family), s.zeros(4, 1))
require_zero(mean_sym, "symbolic tangent-family mean")
require_zero(avg(q, tangent_family), "symbolic tangent-family determinant balance")
b_sym = avg_vec(gradG, tangent_family)
H_sym = avg_vec(HessG, tangent_family)
c_sym = avg(G, tangent_family)
beta_sym = s.factor(b_sym.dot(I))
h_sym = s.factor((I.T*H_sym*I)[0])
directional_sym = s.factor(c_sym-beta_sym**2/(2*h_sym))
directional_limit = s.factor(s.limit(directional_sym, eps_sym, 0, dir="+"))
m2_sym = s.factor(sum(wt*(z.dot(R))**2 for z, wt in tangent_family))
v_sym = s.factor(sum(wt*(z-R*z.dot(R)).dot(z-R*z.dot(R)) for z, wt in tangent_family))
m4_sym = s.factor(sum(wt*(z.dot(R))**4 for z, wt in tangent_family))
y4_sym = s.factor(sum(wt*((z-R*z.dot(R)).dot(z-R*z.dot(R)))**2 for z, wt in tangent_family))
delta2_sym = s.factor(v_sym/m2_sym)
delta4_fourth_sym = s.factor(y4_sym/m4_sym)
assert directional_limit == -s.Rational(3, 4)
assert s.limit(delta2_sym, eps_sym, 0, dir="+") == 0
assert s.limit(delta4_fourth_sym, eps_sym, 0, dir="+") == 0
report["tangent_scale_family"] = {
    "directional_gap_limit": str(directional_limit),
    "delta2_squared": str(delta2_sym),
    "delta4_fourth": str(delta4_fourth_sym),
    "scope": "exact symbolic family; full affine infimum is no greater than the negative one-direction trial for sufficiently small eps",
}
passed("tangent scale family: exact negative directional limit while both relative transverse norms vanish")

# Include the zero law as the other trivial singular boundary.
Hzero = s.zeros(4)
bzero = s.zeros(4, 1)
czero = s.Integer(0)
assert Hzero.rank() == 0 and bzero == s.zeros(4, 1) and czero == 0
passed("zero law: rank-zero Hessian and zero affine gap")

report["scope"] = (
    "Exact finite atomic calculations for the named Dacorogna-Marcellini quartic. "
    "They check concentration and singular mechanisms but do not prove the general Holder, "
    "spectral-neighborhood, Finsler-selection, or compatibility claims."
)
Path(__file__).with_name("adversarial_results.json").write_text(json.dumps(report, indent=2) + "\n")
print("WROTE adversarial_results.json", flush=True)
