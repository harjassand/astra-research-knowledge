#!/usr/bin/env python3
"""Exact algebra for the full finite-H ROC completion range criterion.

The classical semidefinite biform factorization and the written Schur
complement argument are proof premises, not conclusions of this script.
No source checkout or input is modified.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
W = Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-sharp-ion-20261015')
PIN = 'b32943eeb62d0d79929a9e572a344219a785ebf9'
checks = []


def check(name, expression):
    if isinstance(expression, sp.MatrixBase):
        assert expression.applyfunc(sp.simplify) == sp.zeros(*expression.shape), name
    else:
        assert sp.simplify(expression) == 0, (name, sp.simplify(expression))
    checks.append(name)


def export(matrix):
    return [[str(sp.factor(v)) for v in row] for row in matrix.tolist()]


a, b, c, d, p, q, h, k, s, t = sp.symbols('a b c d p q h k s t', real=True)
x = sp.Matrix([a, b, c, d])
f = sp.symbols('f0:9', real=True)
u, v, w, j = a*a+c*c, b*b+d*d, a*b+c*d, a*d-b*c
basis = [u*u, v*v, u*v, w*w, u*w, v*w, u*j, v*j, w*j]
F = sum(fi*bi for fi, bi in zip(f, basis))
H = (u+v-2*j)**2
hf = [1, 1, 6, -4, 0, 0, -4, -4, 0]
acoustic = sp.expand((p*p*sp.diff(F, a, 2)
                     + 2*p*q*sp.diff(F, a, b)
                     + q*q*sp.diff(F, b, 2))/2)
M11 = sp.hessian(acoustic.coeff(p, 2), x)/2
M12 = sp.hessian(acoustic.coeff(p, 1).coeff(q, 1)/2, x)/2
M22 = sp.hessian(acoustic.coeff(q, 2), x)/2
M11_explicit = sp.Matrix([
    [6*f[0], 3*f[4]/2, 0, 3*f[6]/2],
    [3*f[4]/2, f[2]+f[3], -f[6]/2, f[8]/2],
    [0, -f[6]/2, 2*f[0], f[4]/2],
    [3*f[6]/2, f[8]/2, f[4]/2, f[2]],
])
M12_explicit = sp.Matrix([
    [3*f[4]/2, f[2]+f[3], -f[6]/2, f[8]/2],
    [f[2]+f[3], 3*f[5]/2, -f[8]/2, f[7]/2],
    [-f[6]/2, -f[8]/2, f[4]/2, f[3]/2],
    [f[8]/2, f[7]/2, f[3]/2, f[5]/2],
])
M22_explicit = sp.Matrix([
    [f[2]+f[3], 3*f[5]/2, -f[8]/2, f[7]/2],
    [3*f[5]/2, 6*f[1], -3*f[7]/2, 0],
    [-f[8]/2, -3*f[7]/2, f[2], f[5]/2],
    [f[7]/2, 0, f[5]/2, 2*f[1]],
])
for name, actual, expected in [('M11', M11, M11_explicit),
                                ('M12', M12, M12_explicit),
                                ('M22', M22, M22_explicit)]:
    check(name+' explicit coefficient matrix', actual-expected)

z, r, ss, tt, uu, vv = sp.symbols('z r s_aux t_aux u_aux v_aux', real=True)
S = sp.Matrix([[0, z, r, ss], [-z, 0, tt, uu],
               [-r, -tt, 0, vv], [-ss, -uu, -vv, 0]])
T = sp.Matrix([[1, 0, 1, 0], [0, -1, 0, 1],
               [0, 1, 0, 1], [1, 0, -1, 0]])
check('conformal-anticonformal coordinate matrix', T*sp.Matrix([h,k,s,t])
      - sp.Matrix([h+s,t-k,t+k,h-s]))
check('orthogonal unnormalized coordinates', T.T*T-2*sp.eye(4))
M11b, M12b, M22b = [sp.simplify(T.T*M*T) for M in (M11,M12,M22)]
G0 = M11b.row_join(M12b+S).col_join((M12b-S).row_join(M22b))
order = [0,1,4,5,2,3,6,7]
Gram = G0.extract(order, order)
C, B, D = Gram[:4,:4], Gram[:4,4:], Gram[4:,4:]
U = sp.Matrix([p*h,p*k,q*h,q*k])
V = sp.Matrix([p*s,p*t,q*s,q*t])
check('full eight-dimensional Gram identity', ((U.col_join(V)).T*Gram
      *(U.col_join(V)))[0]-acoustic.subs(dict(zip(x,T*sp.Matrix([h,k,s,t]))), simultaneous=True))

Baux = B-B.subs({r:0,ss:0,tt:0,uu:0})
M = sp.Matrix([[r,ss],[tt,uu]])
check('mixed four-variable pattern', Baux-sp.zeros(2).row_join(M).col_join((-M).row_join(sp.zeros(2))))
J = sp.diff(C,z)
check('conformal skew pencil involution', J*J-sp.eye(4))
n0,n1,n2,n3 = sp.symbols('n0 n1 n2 n3', real=True)
n = sp.Matrix([n0,n1,n2,n3])
Xn = sp.Matrix([[n0,n2],[-n1,-n3]])
check('skew pencil isotropy means rank-one increment', (n.T*J*n)[0]+2*Xn.det())
mixed_map = sp.Matrix([sp.diff(vv1, var) for vv1 in list(n.T*Baux)
                       for var in (r,tt,ss,uu)]).reshape(4,4)
check('mixed map invertible for nonrankone kernel vector', mixed_map.det()+Xn.det()**2)

hsubs = dict(zip(f,hf))
check('H has no conformal block', C.subs(hsubs).subs(z,0))
check('H has no mixed block', B.subs(hsubs).subs({r:0,ss:0,tt:0,uu:0}))
DH = D.subs(hsubs).subs(vv,8)
DH_explicit = sp.Matrix([[24,0,0,16],[0,8,0,0],[0,0,8,0],[16,0,0,24]])
check('positive definite H Gram', DH-DH_explicit)
assert sorted(DH.eigenvals().items()) == [(sp.Integer(8),3),(sp.Integer(40),1)]
checks.append('H Gram eigenvalues 8,8,8,40')

# The unique boundary Gram and contradictory cross equations for w^2.
wsubs = {fi:0 for fi in f}; wsubs[f[3]]=1
Cw = C.subs(wsubs).subs(z,sp.Rational(1,2))
Bw = B.subs(wsubs)
assert Cw.rank()==1
Kw = sp.Matrix.hstack(sp.eye(4)[:,0],sp.eye(4)[:,3],sp.Matrix([0,1,1,0]))
check('w2 kernel', Cw*Kw)
eqw = Kw.T*Bw
assert sp.linsolve(list(eqw),(r,ss,tt,uu)) is sp.EmptySet
checks.append('w2 finite-completion cross system inconsistent')
forced_w = {r:0,ss:-sp.Rational(3,2),tt:-sp.Rational(3,2),uu:0}
check('w2 exact residual after first two kernel vectors',
      eqw.subs(forced_w)-sp.Matrix([[0,0,0,0],[0,0,0,0],[0,2,-2,0]]))

# Positive w2+epsilon v2 approaches the excluded boundary. An exact Gram
# completion is built for epsilon=1/2, without numerical eigenvalues.
eps=sp.symbols('epsilon',positive=True)
esubs=dict(wsubs);esubs[f[1]]=eps
Ce=C.subs(esubs).subs(z,sp.Rational(1,2))
check('nonshear local rank-three determinant', Ce[1:,1:].det()-12*eps**2)
assert Ce[0,:]==sp.zeros(1,4)
checks.append('nonshear epsilon branch unique kernel e0')
Be=B.subs(esubs).subs({r:0,ss:-sp.Rational(3,2),tt:sp.Rational(3,2),uu:0})
De=D.subs(esubs).subs(vv,0)
E = sp.simplify(Be[1:,:].T*Ce[1:,1:].inv()*Be[1:,:]-De)
En=E.subs(eps,sp.Rational(1,2))
alpha=sum(abs(vv1) for vv1 in En)/8
Schur=alpha*DH-En
assert all(Schur.extract(ids,ids).det()>=0
           for size in range(1,5)
           for ids in __import__('itertools').combinations(range(4),size))
checks.append('exact finite ROC completion for w2+v2/2')

# The already known sharp shear family has a rank-two conformal Gram.
rho=sp.symbols('rho',real=True)
jsubs={fi:0 for fi in f}
jsubs.update({f[0]:rho*(rho-1)/6,f[2]:1,f[3]:-1,f[6]:rho})
Cj=sp.simplify(C.subs(jsubs).subs(z,-(rho+1)/2))
Kj=sp.Matrix.hstack(sp.Matrix([0,0,1,0]),sp.Matrix([1,0,0,rho+1]))
check('sharp shear rank-two conformal kernel', Cj*Kj)
Bj=sp.simplify(B.subs(jsubs))
solj=sp.solve(list(Kj.T*Bj),(r,ss,tt,uu),dict=True)
assert len(solj)==1
check('sharp shear mixed range solution', (Kj.T*Bj).subs(solj[0]))

# Rank-zero local data can complete only in the zero projected class.
allvars=[*f,z,r,ss,tt,uu]
zero_map=sp.linear_eq_to_matrix(list(C)+list(B),allvars)[0]
assert zero_map.rank()==13 and len(zero_map.nullspace())==1
zero_generator=zero_map.nullspace()[0]
assert sp.Matrix.hstack(zero_generator[:9,0],sp.Matrix(hf)).rank()==1
assert zero_generator[9:,0]==sp.zeros(5,1)
checks.append('rank-zero conformal Gram finite completion forces span H')

# The range predicate genuinely goes beyond the prior cubic-flat compiler:
# det^2 has a valid range solution but a nonflat, nonrankone support kernel.
j2subs={fi:0 for fi in f};j2subs.update({f[2]:1,f[3]:-1})
Cj2=C.subs(j2subs).subs(z,-sp.Rational(1,2))
Kj2=sp.Matrix.hstack(*Cj2.nullspace())
solj2={r:0,ss:-sp.Rational(1,2),tt:-sp.Rational(1,2),uu:0}
check('det2 full kernel cross range condition', Kj2.T*B.subs(j2subs).subs(solj2))
tau=sp.symbols('tau',real=True)
I=sp.Matrix([[1,0],[0,1]])
XX=sp.Matrix([[a,b],[c,d]])
cubic=sp.expand((I+tau*XX).det()**2).coeff(tau,3)
check('det2 cubic Taylor coefficient',cubic-2*(a+d)*(a*d-b*c))
check('det2 cubic-flat failure at trace-zero nonrankone Z',
      (sp.diff(cubic,a)+sp.diff(cubic,d)).subs({a:1,b:0,c:0,d:-1})+4)

# A rank-one null vector gives exactly two transverse stationarity tests.
eta1,eta2,xi1,xi2=sp.symbols('eta1 eta2 xi1 xi2',real=True)
nr=sp.Matrix([eta1*xi1,eta2*xi1,eta1*xi2,eta2*xi2])
row=sp.Matrix([[eta1,eta2]])*M
check('rank-one null mixed-map image', nr.T*Baux
      -sp.Matrix.hstack(-xi2*row,xi1*row))
q1,q2,q3,q4=sp.symbols('q1 q2 q3 q4',real=True)
testrow=sp.Matrix([[q1,q2,q3,q4]])
check('two transverse acoustic stationarity equations',
      2*(testrow*sp.Matrix([xi1*s,xi1*t,xi2*s,xi2*t]))[0]
      -2*s*(xi1*q1+xi2*q3)-2*t*(xi1*q2+xi2*q4))

out={
 'coefficient_order':[str(fi) for fi in f],
 'invariant_basis':['u^2','v^2','uv','w^2','uw','vw','uj','vj','wj'],
 'acoustic_normalization':'one half D2 F(A)[e1 tensor (p,q), e1 tensor (p,q)]',
 'M11':export(M11),'M12':export(M12),'M22':export(M22),
 'coordinate_T':export(T),'C':export(C),'B':export(B),'D':export(D),
 'H_positive_Gram':export(DH),
 'w2_obstruction_residual':export(eqw.subs(forced_w)),
 'epsilon_half_ROC_completion_alpha':str(alpha),
 'epsilon_half_Schur_complement':export(Schur),
 'sharp_shear_C':export(Cj),
 'sharp_shear_range_solution':{str(var):str(sp.factor(value)) for var,value in solj[0].items()},
 'det2_range_solution':{str(var):str(value) for var,value in solj2.items()},
 'checks':checks,
 'interpretation':'Exact identities and finite PSD checks only; written proof supplies quantified range equivalence.',
 'historical_novelty':'UNKNOWN',
}
(ROOT/'EXACT_ALGEBRA.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','exact_check_groups':len(checks),
                  'epsilon_half_alpha':str(alpha),
                  'sharp_shear_range_solution':out['sharp_shear_range_solution']},indent=2))
