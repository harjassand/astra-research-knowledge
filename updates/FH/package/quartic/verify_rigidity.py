#!/usr/bin/env python3
"""Exact algebra checks for ASTRA full-cone quartic rigidity.

Requires Python 3 and SymPy. No SDP, floating-point optimization, pickle, or
external data is used. These checks support the accompanying analytic proof;
they do not formally verify its measure-theoretic/variational steps or priority.
"""
from __future__ import annotations
import itertools
import json
import math
from pathlib import Path
import sympy as s

RESULTS: dict[str, object] = {}
def zero(expr: s.Expr) -> None:
    assert s.expand(expr) == 0, s.factor(expr)
def matrix_zero(M: s.Matrix) -> None:
    for e in M:
        zero(e)
def record(name: str, data: object = True) -> None:
    RESULTS[name] = data
    print('PASS:', name, flush=True)
def monomials(vs: tuple[s.Symbol, ...], degree: int) -> list[s.Expr]:
    return [s.prod(vs[i] for i in inds)
            for inds in itertools.combinations_with_replacement(range(len(vs)), degree)]

# All 35 quartic monomials: no rotational restriction in this first block.
x = s.symbols('x0:4'); a = s.symbols('a0:4'); y = s.symbols('y0:4')
X, A, Y = s.Matrix(x), s.Matrix(a), s.Matrix(y)
mons = monomials(x, 4)
assert len(mons) == 35
for f in mons:
    h = s.hessian(f, x)
    fa = f.xreplace(dict(zip(x, a)))
    ha = h.xreplace(dict(zip(x, a)))
    dfxa = sum(s.diff(f, xi)*ai for xi, ai in zip(x, a))
    dfax = sum(s.diff(fa, ai)*xi for xi, ai in zip(x, a))
    zero((A.T*h*A)[0] - (X.T*ha*X)[0])
    shift = f.xreplace({xi: xi+ai for xi, ai in zip(x, a)})
    zero(shift-fa-dfax-(A.T*h*A)[0]/2-dfxa-f)
    lhs = (X.T*s.hessian(dfxa, x).xreplace(dict(zip(x, y)))*X)[0]
    q_a = (X.T*ha*X)[0]
    rhs = sum(s.diff(q_a, ai)*yi for ai, yi in zip(a, y))
    zero(lhs-rhs)
record('35-monomial quartic reciprocity, Taylor formula, and cubic-derivative identity')

# The algebraic cubic closure statement, checked in all signatures relevant to
# subspaces of R^4. The general-dimensional proof is in the note.
closure_checks = []
for diag in [(1,-1), (1,-1,0), (1,1,-1), (1,-1,0,0),
             (1,1,-1,0), (1,1,-1,-1), (1,1,1,-1)]:
    n = len(diag); z = s.symbols(f'z0:{n}')
    cm = monomials(z,3); cs = s.symbols(f'c0:{len(cm)}'); ls = s.symbols(f'l0:{n}')
    cubic = sum(ci*mi for ci,mi in zip(cs,cm)); lin = sum(li*zi for li,zi in zip(ls,z))
    eq = []
    HH = s.hessian(cubic,z)
    for i in range(n):
        for j in range(n):
            e = s.expand(HH[i,j]-(diag[i]*lin if i==j else 0))
            eq.extend(s.Poly(e,*z).coeffs())
    mat,_ = s.linear_eq_to_matrix(eq,cs+ls)
    assert mat.rank() == len(cs)+len(ls)
    closure_checks.append({'signature_diagonal':list(diag),'unknowns':len(cs)+len(ls),'rank':mat.rank()})
record('cubic Hessian proportionality forces zero, including indefinite forms with a radical',closure_checks)

# Complete left-SO(2) invariant quartic coordinates.
i,j,k,l = s.symbols('i j k l',real=True)
v = (i,j,k,l); V=s.Matrix(v)
z2=i*i+j*j; w2=k*k+l*l; rr=i*k+j*l; ss=j*k-i*l
alpha,beta,gamma,dr,di,er,ei,hr,hi=s.symbols('alpha beta gamma dr di er ei hr hi',real=True)
pars=(alpha,beta,gamma,dr,di,er,ei,hr,hi)
F=alpha*z2*z2+beta*z2*w2+gamma*w2*w2+dr*(rr*rr-ss*ss)-2*di*rr*ss+(er*rr-ei*ss)*z2+(hr*rr-hi*ss)*w2
rot=(-j,i,-l,k)
zero(sum(s.diff(F,vi)*ri for vi,ri in zip(v,rot)))
quartics=monomials(v,4)
rotmat=s.zeros(35)
for col,f in enumerate(quartics):
    pp=s.Poly(s.expand(sum(s.diff(f,vi)*ri for vi,ri in zip(v,rot))),*v)
    for row,m in enumerate(quartics):rotmat[row,col]=pp.coeff_monomial(m)
assert 35-rotmat.rank()==9
basis=s.Matrix([[s.Poly(s.diff(F,p),*v).coeff_monomial(m) for p in pars] for m in quartics])
assert basis.rank()==9
record('complete nine-dimensional invariant basis, not a symmetry subfamily')

H=s.hessian(F,v).subs({i:1,j:0,k:0,l:0})
expected=s.Matrix([[12*alpha,0,3*er,3*ei],[0,4*alpha,-ei,er],
                   [3*er,-ei,2*(beta+dr),2*di],[3*ei,er,2*di,2*(beta-dr)]])
matrix_zero(H-expected)
record('exact Hessian at I forced by homogeneity and left rotations',str(H))

# Positive-value branch: rank-one PSD remainder implies the determinant square
# plus |w|^4, except for a cubic term which closure kills.
f,g=s.symbols('f g',real=True); q=z2-w2
Fp=s.expand(F.subs({alpha:f,beta:-2*f,gamma:f+g,dr:0,di:0,er:0,ei:0}))
zero(Fp-(f*q*q+g*w2*w2+(hr*rr-hi*ss)*w2))
zero(s.diff(Fp,i).subs(i,0)-w2*(hr*k+hi*l))
Hp=s.hessian(Fp,v).subs({i:1,j:0,k:0,l:0})
matrix_zero(Hp-(s.diag(8*f,0,0,0)+4*f*s.diag(1,1,-1,-1)))
record('positive-value low-rank branch and the cubic term eliminated by closure')

# Zero-value branch: normalized phase, then exact rank-one second derivative.
Z,W,t,sigma,h=s.symbols('Z W t sigma h',real=True)
Fzero=2*beta*rr**2+gamma*w2**2+h*w2*rr
line=s.expand(Fzero.subs({i:sigma*t,j:Z,k:t,l:W}))
second=s.diff(line,t,2).subs(t,0)
expected_second=2*((4*beta*sigma+h)*Z*W+(2*gamma+h*sigma)*W*W)
zero(second-expected_second)
for sg in [-1,1]:
    # Direction (z,w)=(sg,1) lies on det=0.
    assert sg*sg-1==0
    zero(second.subs(sigma,sg)-expected_second.subs(sigma,sg))
assert s.solve([4*beta+h,-4*beta+h],[beta,h])=={beta:0,h:0}
record('zero-value branch: two exact rank-one tests force beta=h=0',str(second))

# Degenerate rank-one restriction, reconstructed in matrix-entry coordinates.
aa,bb,cc,dd=s.symbols('a b c d'); vs=(aa,bb,cc,dd)
u=aa*aa+cc*cc; vv=bb*bb+dd*dd; w=aa*bb+cc*dd; det=aa*dd-bb*cc
c0,lam,L,M,N=s.symbols('c0 lam L M N')
Fd=c0*u*u+lam*det*det+det*(L*u+M*vv+N*w)
HD=s.hessian(Fd,vs)
e12=HD.subs({aa:0,bb:1,cc:0,dd:0})
expected12=s.Matrix([[0,0,-N,M],[0,0,-3*M,0],[-N,-3*M,2*lam,0],[M,0,0,0]])
matrix_zero(e12-expected12)
e11=HD.subs({aa:1,bb:0,cc:0,dd:0,M:0,N:0})
expected11=s.Matrix([[12*c0,0,0,3*L],[0,0,-L,0],[0,-L,4*c0,0],[3*L,0,0,2*lam]])
matrix_zero(e11-expected11)
record('rank-one-background degenerate classification, including all odd coefficients',{'e12':str(e12),'e11_after_M_N_zero':str(e11)})

# Sharpness of the exceptional class: actual three-wave compatible gradient.
R1=s.Matrix([[0,1],[0,0]]); R2=s.Matrix([[0,0],[1,0]]); R3=s.Matrix([[1,1],[-1,-1]])
rs=[s.Matrix([R[0,0],R[0,1],R[1,0],R[1,1]]) for R in [R1,R2,R3]]
assert all(R.det()==0 and s.trace(R)==0 for R in [R1,R2,R3])
C=sum((r*r.T/2 for r in rs),s.zeros(4));assert C.rank()==3
QJ=s.Matrix([[0,0,0,s.Rational(1,2)],[0,0,-s.Rational(1,2),0],[0,-s.Rational(1,2),0,0],[s.Rational(1,2),0,0,0]])
assert s.trace(QJ*C)==0
anti=((aa-dd)**2+(cc+bb)**2)/4
Fe=det**2+anti**2
HE=s.hessian(Fe,vs)
Havg=sum((HE.subs(dict(zip(vs,r)))/2 for r in rs),s.zeros(4))
Id=s.Matrix([1,0,0,1]);matrix_zero(Havg*Id)
assert Havg.rank()==3
record('exceptional class has a genuine three-direction resonant gradient with singular averaged Hessian',{'C':str(C),'H':str(Havg)})

# General affine-background minimum: symbolic square-completion identity.
# Range inclusion is analytic, not asserted by this finite check.
B0=s.Matrix(s.symbols('B0:4')); rhsvec=s.Matrix(s.symbols('b0:4'))
for diagH in [(1,2,3,4),(1,2,3,0),(1,2,0,0)]:
    HH=s.diag(*diagH); pinv=s.diag(*[s.Rational(1,hv) if hv else 0 for hv in diagH])
    bvec=s.Matrix([bi if hv else 0 for bi,hv in zip(rhsvec,diagH)])
    zero((B0.T*HH*B0)[0]/2+(bvec.T*B0)[0] + (bvec.T*pinv*bvec)[0]/2
         -((B0+pinv*bvec).T*HH*(B0+pinv*bvec))[0]/2)
record('background deflation square completion, with singular cases')

# Exact all-flow obstruction, actual compatible Fourier potential.
sx,cx,sy,cy,a0,b0,c0=s.symbols('sx cx sy cy a0 b0 c0')
def avg1(p:int,r:int)->s.Rational:
    if p%2 or r%2:return s.S.Zero
    m,n=p//2,r//2
    return s.Rational(math.factorial(2*m)*math.factorial(2*n),4**(m+n)*math.factorial(m)*math.factorial(n)*math.factorial(m+n))
def mean(poly:s.Expr)->s.Expr:
    return s.expand(sum(co*avg1(ex[0],ex[1])*avg1(ex[2],ex[3])
                        for ex,co in s.Poly(s.expand(poly),sx,cx,sy,cy).terms()))
AG=s.Matrix([[-a0*sx,-a0*sy],[-2*sx*(b0*cx+c0*cy),-2*sy*(b0*cy+c0*cx)]])
qmean=mean(AG.det()**2);nmean=mean(sum(e*e for e in AG)**2)
zero(qmean-a0*a0*(c0-b0)**2/2)
zero(nmean-(s.Rational(5,4)*a0**4+2*a0*a0*b0*b0+4*a0*a0*c0*c0+s.Rational(5,4)*b0**4+10*b0*b0*c0*c0+5*c0**4))
def heat_derivative(poly:s.Expr)->s.Expr:
    return s.factor((-a0*s.diff(poly,a0)-4*b0*s.diff(poly,b0)-2*c0*s.diff(poly,c0)).subs({a0:1,b0:1,c0:s.Rational(4,3)}))
qd=heat_derivative(qmean);nd=heat_derivative(nmean);eta=s.Rational(1,10000);ed=qd+eta*nd
assert qd==s.Rational(1,3) and nd==-s.Rational(34621,81)
assert ed==s.Rational(235379,810000)>0
record('exact compatible heat increase for a uniformly quasiconvex quartic',{'mean_det2':str(qmean),'mean_norm4':str(nmean),'det2_derivative':str(qd),'norm4_derivative':str(nd),'eta':str(eta),'total_derivative':str(ed)})

# D4 averaging acts on ANY output matrix, including its skew part.
rot=s.Matrix([[0,-1],[1,0]]);ref=s.diag(1,-1)
D4=[rot**j for j in range(4)]+[ref*rot**j for j in range(4)]
c=s.Matrix(2,2,s.symbols('c0:4'))
avg=sum((R*c*R.T for R in D4),s.zeros(2))/8
matrix_zero(avg-s.trace(c)*s.eye(2)/2)
record('D4 averaging removes anisotropy and output skew, without an SOS ansatz')

# Why the one-quadric hypothesis matters: known 3x2 three-axis geometry.
xx,yy,zz=s.symbols('xx yy zz')
GG=s.Matrix([[xx,0],[0,yy],[zz,zz]])
minors=[s.det(GG[list(pair),:]) for pair in itertools.combinations(range(3),2)]
assert minors==[xx*yy,xx*zz,-yy*zz]
cubic=xx*yy*zz;HC=s.hessian(cubic,(xx,yy,zz))
assert all(HC[j,j]==0 for j in range(3))
# cos(x+y)=cos x cos y - sin x sin y
assert mean(cx*cy)==0
assert mean(cx*(cx*cy-sx*sy))==0
assert mean(cy*(cx*cy-sx*sy))==0
resonance=mean(cx*cy*(cx*cy-sx*sy));assert resonance==s.Rational(1,4)
record('multiple-quadric limitation: three-axis cubic and an actual resonant gradient',{'minors':list(map(str,minors)),'cubic_mean':str(resonance)})

out=Path(__file__).with_name('exact_checks.json')
out.write_text(json.dumps(RESULTS,indent=2,default=str)+'\n')
print(f'ALL {len(RESULTS)} GROUPED EXACT CHECKS PASSED. Analytic proofs remain in the note.',flush=True)
