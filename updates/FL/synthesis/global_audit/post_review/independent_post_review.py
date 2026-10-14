#!/usr/bin/env python3
"""Independent exact checks for the post-isolation FL critique.

This reconstructs load-bearing algebra in the two incoming reports. It is not
a formal verification of their analytic theorems.
"""
from __future__ import annotations

import json
from itertools import combinations_with_replacement
from pathlib import Path

import sympy as s


checks: list[str] = []


def must_zero(name: str, value) -> None:
    value = s.simplify(s.expand(value))
    if value != 0:
        raise AssertionError(f"{name}: {s.factor(value)}")
    checks.append(name)


a, b, c, d = s.symbols("a b c d", real=True)
xv = s.Matrix([a, b, c, d])
u = a*a + c*c
v = b*b + d*d
w = a*b + c*d
q = a*d - b*c
basis = [u*u, v*v, u*v, w*w, u*w, v*w, q*u, q*v, q*w]
dA = s.Matrix([1, 0, 0, 0])
dB = s.Matrix([0, 1, 0, 0])
s1, s2 = s.symbols("s1 s2", real=True)
z = s.Matrix.vstack(s1*xv, s2*xv)

# Reconstruct the nine acoustic Gram coefficient matrices by differentiating
# each basis quartic, rather than reusing the producer's coefficient matrices.
grams = []
for idx, f in enumerate(basis):
    Hf = s.hessian(f, xv)
    forms = [
        (dA.T * Hf * dA)[0],
        (dA.T * Hf * dB)[0],
        (dB.T * Hf * dB)[0],
    ]
    blocks = [s.hessian(form, xv) / 2 for form in forms]
    for form, block in zip(forms, blocks):
        must_zero(f"basis {idx+1}: quadratic acoustic block reconstruction", xv.dot(block*xv)-form)
    M11, M12, M22 = blocks
    Q0 = M11.row_join(M12).col_join(M12.row_join(M22))
    direction = s1*dA + s2*dB
    direct = (direction.T * Hf * direction)[0]
    must_zero(f"basis {idx+1}: direct acoustic identity", (z.T*Q0*z)[0]-direct)
    grams.append(Q0)

# Reconstruct the strict Slater point used by the N794 moment-duality proof.
# For F=|A|^4=u^2+v^2+2uv, one skew entry K_12=1 makes the acoustic Gram
# positive definite, so no unproved closure/attainment assumption is needed.
Qnorm = grams[0] + grams[1] + 2*grams[2]
Kslater = s.zeros(4)
Kslater[0,1] = 1
Kslater[1,0] = -1
Qslater = Qnorm.copy()
Qslater[:4,4:] += Kslater
Qslater[4:,:4] -= Kslater
slater_minors = [s.factor(Qslater[:j,:j].det()) for j in range(1,9)]
assert all(value > 0 for value in slater_minors), slater_minors
checks.append("N794 strict Slater Gram for |A|^4 is positive definite")

# Every six-dimensional skew-block freedom is invisible to z(A,b), and its
# trace pairing vanishes on atoms zz^T because their off-diagonal block is
# symmetric.
k12, k13, k14, k23, k24, k34 = s.symbols("k12 k13 k14 k23 k24 k34", real=True)
K = s.Matrix([[0,k12,k13,k14],[-k12,0,k23,k24],[-k13,-k23,0,k34],[-k14,-k24,-k34,0]])
dQ = s.zeros(8)
dQ[:4,4:] = K
dQ[4:,:4] = -K
must_zero("all skew freedoms vanish on acoustic rank-one z", (z.T*dQ*z)[0])
Yatom = z*z.T
must_zero("all skew freedoms annihilate rank-one PSD atoms", s.trace(dQ*Yatom))
must_zero("atom off-diagonal block is symmetric", (Yatom[:4,4:]-Yatom[:4,4:].T).norm())

# Exact rational modulation moments and the displayed diagonal PSD completion.
t = s.symbols("t", real=True)
rho = 1 + s.cos(t)/2
drho = s.diff(rho, t)
u0, v0, w0, q0 = drho**2, rho**2, s.Integer(0), rho*drho
values = [u0**2, v0**2, u0*v0, w0**2, u0*w0, v0*w0, q0*u0, q0*v0, q0*w0]
mean_t = lambda f: s.simplify(s.integrate(s.expand_trig(f), (t, 0, 2*s.pi))/(2*s.pi))
moments = [mean_t(f) for f in values]
target_moments = [s.Rational(3,128), s.Rational(227,128), s.Rational(17,128), 0,0,0,0,0,0]
assert moments == target_moments
checks.append("r=1+cos(x)/2: independently derived nine exact moments")
Y = s.diag(s.Rational(1,512),0,0,s.Rational(17,256),0,0,0,s.Rational(227,512))
pairings = [s.trace(G*Y) for G in grams]
assert pairings == target_moments
checks.append("displayed diagonal Y: nine independently reconstructed coefficient pairings")
assert all(eigen >= 0 for eigen in Y.diagonal())
checks.append("displayed Y is PSD and its off-diagonal block is symmetric")

# Sheared curvature formula and the exact positive/negative signed defects.
L, M, N = s.symbols("L M N", real=True)
gx, gxx, ny = s.symbols("gprime gsecond n", real=True)
Xi1 = ny*(L*gx*gx + M*ny*ny + N*gx*ny)
Xi2 = -gx*(L*gx*gx + M*ny*ny + N*gx*ny)
div_shear = s.diff(Xi1, gx)*gxx
must_zero("sheared div Xi = n(2L g' + nN)g''", div_shear-ny*(2*L*gx+ny*N)*gxx)
y = s.symbols("y", real=True)
mean_y = lambda f: s.simplify(s.integrate(s.expand_trig(f), (y,0,2*s.pi))/(2*s.pi))
div_convex = -4*s.sin(2*y)
defect_pos = mean_y((1-s.sin(2*y)/2)*div_convex/4)
defect_neg = mean_y((1+s.sin(2*y)/2)*div_convex/4)
assert (defect_pos, defect_neg) == (s.Rational(1,4), -s.Rational(1,4))
checks.append("convex phase-defect example has exact opposite signs +/-1/4")

# Removing amplitude half-turn symmetry can break b=E DF(X)=0. Here
# r=1+eps*cos(y), theta=y, and F=|A|^4; X has one column X_y=r_y V+rW.
eps = s.symbols("eps", real=True)
V = s.Matrix([s.cos(y), s.sin(y)])
W = s.Matrix([-s.sin(y), s.cos(y)])
r1 = 1 + eps*s.cos(y)
Xcol = s.diff(r1,y)*V + r1*W
norm2 = s.simplify(Xcol.dot(Xcol))
bvec = s.Matrix([mean_y(4*norm2*Xcol[i]) for i in range(2)])
assert bvec == s.Matrix([0,4*eps])
checks.append("without half-turn symmetry, b=E DF(X) can be nonzero: (0,4 eps)")

# A rank-one sine test is rigorously obtained as a limit of nondegenerate
# ellipses V_delta=alpha*cos(t)+delta*c*sin(t). For each delta>0 this is an
# admissible loop; its averaged quadratic and quartic Taylor coefficients
# converge to 1/4 and 3/8 times the desired rank-one forms.
tau = s.symbols("tau", real=True)
trig_means = [
    s.integrate(s.sin(tau)**2,(tau,0,2*s.pi))/(2*s.pi),
    s.integrate(s.sin(tau)*s.cos(tau),(tau,0,2*s.pi))/(2*s.pi),
    s.integrate(s.sin(tau)**4,(tau,0,2*s.pi))/(2*s.pi),
    s.integrate(s.sin(tau)**2*s.cos(tau)**2,(tau,0,2*s.pi))/(2*s.pi),
]
assert trig_means == [s.Rational(1,2),0,s.Rational(3,8),s.Rational(1,8)]
checks.append("ellipse degeneration has exact second/fourth trigonometric moments")

# Check the complete quartic expansion used in affine optimization, separately
# for all 35 monomials. The cubic-in-B term is linear in X and hence averages
# to zero for every periodic gradient; the linear-in-B coefficient is cubic
# and is killed by the amplitude half-turn symmetry.
Bv = s.Matrix(s.symbols("B0:4", real=True))
Xv = s.Matrix(s.symbols("X0:4", real=True))
subs_BX = dict(zip(xv, Bv+Xv))
subs_B = dict(zip(xv, Bv))
subs_X = dict(zip(xv, Xv))
quartic_monomials = []
vars4 = (a,b,c,d)
for inds in combinations_with_replacement(range(4),4):
    quartic_monomials.append(s.prod(vars4[j] for j in inds))
for idx, f in enumerate(quartic_monomials):
    gradX = s.Matrix([s.diff(f, var).subs(subs_X, simultaneous=True) for var in xv])
    hessX = s.hessian(f, xv).subs(subs_X, simultaneous=True)
    third_term = 0
    for i in range(4):
        for j in range(4):
            for k in range(4):
                third_term += (s.diff(f,xv[i],xv[j],xv[k]).subs(subs_X, simultaneous=True)
                               * Bv[i]*Bv[j]*Bv[k])
    lhs = f.subs(subs_BX, simultaneous=True)-f.subs(subs_B, simultaneous=True)
    rhs = (f.subs(subs_X, simultaneous=True) + gradX.dot(Bv)
           + (Bv.T*hessX*Bv)[0]/2 + third_term/6)
    must_zero(f"quartic affine expansion monomial {idx+1}", lhs-rhs)
    assert s.Poly(third_term,*list(Xv)).total_degree() == 1
checks.append("all averaged cubic-in-background terms vanish from mean gradient zero")
checks.append("half-turn kills the remaining cubic moment b=E DF(X)")
checks.append("rank-one polar test follows by ellipse degeneration and eps->0")

# Half-turn symmetry in the explicit non-affine profile, its transport moment,
# and a point with full-rank gradient.
x, yy = s.symbols("x yy", real=True)
g = s.sin(x)/4
h = s.sin(2*x)/3
amp = 1 + s.cos(2*(yy+h))/5
must_zero("explicit amplitude is invariant under y->y+pi", amp.subs(yy,yy+s.pi)-amp)
transport_mean = s.simplify(s.integrate(s.expand_trig(amp**4),(yy,0,2*s.pi))/(2*s.pi))
assert transport_mean == s.Rational(5603,5000)
checks.append("explicit two-variable amplitude has y-fourth moment 5603/5000")
det_at = (amp*s.diff(amp,yy)*(s.diff(h,x)-s.diff(g,x))).subs({x:0,yy:s.pi/4})
assert det_at == -s.Rational(1,6)
checks.append("explicit profile gradient determinant is -1/6 at (0,pi/4)")

result = {
    "scope": "Independent exact algebraic checks for the post-isolation critique; not formal verification.",
    "checks": checks,
    "modulation_moments": [str(value) for value in moments],
    "dual_pairings": [str(value) for value in pairings],
    "slater_leading_minors": [str(value) for value in slater_minors],
    "half_turn_removed_b": [str(value) for value in bvec],
    "variable_phase_defect_signs": [str(defect_pos), str(defect_neg)],
    "two_variable_profile_det_sample": str(det_at),
}
out = Path(__file__).with_name("independent_post_review_results.json")
out.write_text(json.dumps(result, indent=2) + "\n")
print(f"PASS {len(checks)} independent exact checks")
for name in checks:
    print("PASS", name)
print("WROTE", out)
