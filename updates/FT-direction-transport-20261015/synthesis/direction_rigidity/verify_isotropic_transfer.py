#!/usr/bin/env python3
"""Exact algebra supporting ISOTROPIC_TRANSFER_OBSTRUCTION.md.

The analytic face classification and coefficient-closure argument are proved in
the report. These checks are symbolic identities, exact Gram positivity, and one
finite lifted Jensen functional; they do not assert a negative gradient law.
"""
import json
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parent
a, b, c, d, tau, sx, sy = s.symbols("a b c d tau sx sy", real=True)
X = s.Matrix([a, b, c, d])
u = a*a + c*c
v = b*b + d*d
w = a*b + c*d
q = a*d - b*c
norm = u+v
checks = {}

def acoustic_matrices(coef):
    A, B, C, E, G, H, L, M, N = coef
    m11 = s.Matrix([[12*A, 3*G, 0, 3*L],
                    [3*G, 2*C+2*E, -L, N],
                    [0, -L, 4*A, G],
                    [3*L, N, G, 2*C]])
    m12 = s.Matrix([[3*G, 2*C+2*E, -L, N],
                    [2*C+2*E, 3*H, -N, M],
                    [-L, -N, G, E],
                    [N, M, E, H]])
    m22 = s.Matrix([[2*C+2*E, 3*H, -N, M],
                    [3*H, 12*B, -3*M, 0],
                    [-N, -3*M, 2*C, H],
                    [M, 0, H, 4*B]])
    return m11, m12, m22

def polynomial(coef):
    basis = [u*u, v*v, u*v, w*w, u*w, v*w, u*q, v*q, w*q]
    return s.expand(sum(z*t for z, t in zip(coef, basis)))

def gram_with_skew(coef, entries):
    m11, m12, m22 = acoustic_matrices(coef)
    skew = s.zeros(4)
    for (i, j), z in zip([(0, 1), (0, 2), (0, 3),
                          (1, 2), (1, 3), (2, 3)], entries):
        skew[i, j] = z
        skew[j, i] = -z
    return m11.row_join(m12+skew).col_join((m12-skew).row_join(m22))

def ell(p):
    return s.diff(p.subs({a:1, b:tau, c:0, d:1},
                        simultaneous=True), tau, 2).subs(tau, 0)

# General invariant basis, acoustic identity, positive trace and coefficient
# recovery. The report derives compactness from PSD, rather than sampling.
coef = s.symbols("A B C E G H L M N", real=True)
p = polynomial(coef)
m11, m12, m22 = acoustic_matrices(coef)
direction = s.Matrix([sx, sy, 0, 0])
hessian = s.hessian(p, X)
assert s.expand((direction.T*hessian*direction)[0] -
                (X.T*(sx*sx*m11+2*sx*sy*m12+sy*sy*m22)*X)[0]) == 0
recovered = [m11[0,0]/12, m22[1,1]/12, m11[3,3]/2,
             m11[1,1]/2-m11[3,3]/2, m11[0,1]/3,
             m22[0,1]/3, m11[0,3]/3, m22[0,3], m11[1,3]]
assert all(s.expand(z-t) == 0 for z,t in zip(recovered,coef))
lam = s.trace(m11)+s.trace(m22)
assert s.expand(lam - (16*(coef[0]+coef[1])+8*coef[2]+4*coef[3])) == 0
basis = [s.Poly(z, a,b,c,d) for z in
         [u*u,v*v,u*v,w*w,u*w,v*w,u*q,v*q,w*q]]
monomials = sorted(set().union(*(set(z.monoms()) for z in basis)))
basis_matrix = s.Matrix([[z.coeff_monomial(mon) for z in basis]
                         for mon in monomials])
assert basis_matrix.rank() == 9
checks["compact_acoustic_normalization"] = {
    "basis_rank":9, "trace":"16(A+B)+8C+4E",
    "coefficient_recovery":"all nine symbolic identities pass",
    "scope":"The PSD-to-compactness inference is analytic in the report"}

# All right-transformed isotropic atoms obey the necessary beta bound,
# including the alpha=0 degeneracy.
alpha, beta0, gamma0 = s.symbols("alpha beta0 gamma0", real=True)
iso = alpha*norm**2+beta0*q*norm+gamma0*q*q
probe_plus = s.diff(iso.subs({a:1,b:tau,c:0,d:1},
                           simultaneous=True),tau,2).subs(tau,0)
probe_minus = s.diff(iso.subs({a:1,b:tau,c:0,d:-1},
                            simultaneous=True),tau,2).subs(tau,0)
assert probe_plus == 8*alpha+2*beta0
assert probe_minus == 8*alpha-2*beta0
pure_q_probe = s.diff((gamma0*q*q).subs({a:tau,b:0,c:0,d:1},
                                     simultaneous=True),tau,2).subs(tau,0)
assert pure_q_probe == 2*gamma0
checks["isotropic_necessary_probes"] = {
    "I_shear":str(probe_plus),"J_shear":str(probe_minus),
    "alpha_zero_det_probe":str(pure_q_probe),
    "deduction":"alpha>=0; |beta0|<=4alpha; alpha=0 implies beta0=0,gamma0>=0"}

# Parameter representation and all nine expansion identities.
U11,U12,U22,beta,gamma = s.symbols("U11 U12 U22 beta gamma",real=True)
sigma = U11*u+2*U12*w+U22*v
h = sigma**2+beta*q*sigma+gamma*q*q
param_coef = [U11**2, U22**2, 2*U11*U22+gamma, 4*U12**2-gamma,
              4*U11*U12, 4*U12*U22, beta*U11, beta*U22, 2*beta*U12]
assert s.expand(h-polynomial(param_coef)) == 0
face = s.factor(ell(h))
assert s.expand(face-(8*U12**2+(4*(U11+U22)+2*beta)*U22)) == 0
checks["transformed_isotropic_parametrization"] = {
    "all_nine_coefficients":"symbolic identity passes",
    "acoustic_face":str(face),
    "scope":"Closed parameter bound and AM-GM face equality are proved analytically"}

# Exact identities in both null-face cases and their remaining acoustic tests.
case1 = h.subs({U12:0,U22:0,beta:0})
assert s.expand(case1-U11**2*u*u-gamma*q*q) == 0
case1probe = s.diff(case1.subs({a:tau,b:0,c:0,d:1},
                             simultaneous=True),tau,2).subs(tau,0)
assert case1probe == 2*gamma
tt = s.symbols("tt", positive=True)
case2 = h.subs({U11:tt,U12:0,U22:tt,beta:-4*tt})
assert s.expand(case2-tt**2*(norm-2*q)**2-(gamma-4*tt**2)*q*q) == 0
case2probe = s.diff(case2.subs({a:1+tau,b:0,c:0,d:1},
                             simultaneous=True),tau,2).subs(tau,0)
assert case2probe == 2*(gamma-4*tt**2)
assert s.expand(norm-2*q-(a-d)**2-(b+c)**2) == 0
checks["acoustic_null_atoms_are_polyconvex"] = {
    "rank_one_U_probe":str(case1probe),"scalar_U_probe":str(case2probe),
    "convex_fourth_power":"(|A|^2-2det A)^2=((a-d)^2+(b+c)^2)^2",
    "scope":"Complete case split is analytic, not a finite test of arbitrary parameters"}

# Prior Fstar strict global acoustic certificate, independently reconstructed.
fstar_coef = [1,1,s.Rational(7,2),s.Rational(1,2),0,0,
              -s.Rational(29,10),-s.Rational(29,10),0]
Fstar = u*u+v*v+4*w*w+s.Rational(7,2)*q*q-s.Rational(29,10)*q*norm
assert s.expand(Fstar-polynomial(fstar_coef)) == 0
Qstar = gram_with_skew(fstar_coef,
    [s.Rational(1,2),s.Rational(17,10),0,0,s.Rational(17,10),s.Rational(23,10)])
bilin = s.Matrix([sx*a,sx*b,sx*c,sx*d,sy*a,sy*b,sy*c,sy*d])
fstar_ac = (direction.T*s.hessian(Fstar,X)*direction)[0]
assert s.expand(fstar_ac-(bilin.T*Qstar*bilin)[0]) == 0
shift = Qstar-s.eye(8)/16
shift_minors = [s.factor(shift[:k,:k].det()) for k in range(1,9)]
assert all(z>0 for z in shift_minors)
ss,st = s.symbols("ss st",real=True)
boundary = Fstar.subs({b:st*a,d:st*c,a:ss*a,c:ss*c},simultaneous=True)
assert s.expand(boundary-(ss**4+4*ss**2*st**2+st**4)*(a*a+c*c)**2) == 0
checks["prior_Fstar_exact_acoustic_input"] = {
    "shifted_leading_minors":list(map(str,shift_minors)),
    "bound":"D2Fstar(B)[a tensor b,a tensor b] >= |B|^2 |a|^2 |b|^2 /16",
    "singular_null_face":"(ss^4+4ss^2st^2+st^4)|Ae1|^4",
    "provenance":"Existing pinned N794/FO certificate; independently replayed"}

# Target global ROC (for context), exact acoustic zero and positive trace.
G = 3*(norm-2*q)**2+s.Rational(35,24)*u*u+q*q-s.Rational(5,2)*q*u
gcoef = [s.Rational(107,24),3,19,-13,0,0,-s.Rational(29,2),-12,0]
assert s.expand(G-polynomial(gcoef)) == 0
Qg = gram_with_skew(gcoef,[11,s.Rational(91,6),0,0,11,s.Rational(41,3)])
assert s.expand((direction.T*s.hessian(G,X)*direction)[0]-
                (bilin.T*Qg*bilin)[0]) == 0
gminors = [s.factor(Qg[:k,:k].det()) for k in range(1,7)]
assert all(z>0 for z in gminors)
assert Qg[6:,6:]-Qg[6:,:6]*Qg[:6,:6].inv()*Qg[:6,6:] == s.zeros(2)
gline = s.expand(G.subs({a:1,b:tau,c:0,d:1},simultaneous=True))
assert gline == -s.Rational(1,24)+3*tau**4
assert ell(G) == 0
gm11,_,gm22 = acoustic_matrices(gcoef)
assert s.trace(gm11)+s.trace(gm22) == s.Rational(658,3)
checks["target_global_acoustic_and_null_face"] = {
    "rank":Qg.rank(),"positive_six_minors":list(map(str,gminors)),
    "last_schur_block":"zero","shear_line":str(gline),"Lambda":"658/3"}

# The finite law separates polyconvex atoms; it is not a gradient construction.
gI = s.factor(G.subs({a:1,b:0,c:0,d:1}))
gJ = s.factor(G.subs({a:1,b:0,c:0,d:-1}))
mean_det = s.Rational(36**2,1297)-s.Rational(1296,1297)
jG = s.factor((36**4*gI+1296*gJ)/1297)
assert gI == -s.Rational(1,24) and gJ == s.Rational(1271,24)
assert mean_det == 0 and jG == -s.Rational(1350,1297)
checks["finite_lifted_Jensen_witness"] = {
    "G(I)":str(gI),"G(J)":str(gJ),"mean_matrix":"zero by opposite signs",
    "mean_determinant":str(mean_det),"J_mu(G)":str(jG),
    "scope":"Polyconvex separator only; no compatible gradient law"}

# The single-transform rank-one square obstruction.
ss,tt = s.symbols("ss tt",real=True)
rankone_G = s.expand(G.subs({a:ss,b:tt,c:0,d:0},simultaneous=True))
assert rankone_G == s.Rational(107,24)*ss**4+6*ss**2*tt**2+3*tt**4
assert 6**2 != 4*s.Rational(107,24)*3
checks["single_transform_square_obstruction"] = {
    "rank_one_binary":str(rankone_G),
    "mixed_square_required":"36=107/2 (false)"}

out = {"status":"PASS","groups":len(checks),"checks":checks,
       "scope":"Exact supporting algebra. Analytic compact-face concentration proves "
               "the coefficient-closed positive-transfer exclusion in the report. "
               "No quasiconvexity conclusion or negative compatible field."}
(ROOT/"exact_isotropic_transfer_checks.json").write_text(
    json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
