#!/usr/bin/env python3
"""Exact finite checks accompanying ASTRA_POSITIVE_DEFINITE_BARRIER.md.

Run with Python 3 and SymPy. No optimizer, pickle, prior artifact, or network
access is used. These checks do not formalize the analytic proofs in the note.
Output: positive_definite_verification.json beside this script.
"""
from __future__ import annotations
import json
from pathlib import Path
import sympy as s

OUT: dict[str, object] = {}
PASSED: list[str] = []

def zero(expr: s.Expr | s.MatrixBase, label: str = "identity") -> None:
    entries = list(expr) if isinstance(expr, s.MatrixBase) else [expr]
    if any(s.cancel(s.expand(e)) != 0 for e in entries):
        raise AssertionError(label)

def done(label: str) -> None:
    PASSED.append(label)
    print(f"PASS {len(PASSED):02d}: {label}", flush=True)

def strings(matrix: s.MatrixBase) -> list[list[str]]:
    return [[str(e) for e in row] for row in matrix.tolist()]

a,b,c,d = s.symbols('a b c d', real=True)
coords = (a,b,c,d)
X = s.Matrix(coords)
u, v, w, q = a*a+c*c, b*b+d*d, a*b+c*d, a*d-b*c
Jdet = s.hessian(q, coords)/2
I = s.Matrix([1,0,0,1])
A0 = s.Matrix(s.symbols('A0:4', real=True))
R0 = s.Matrix(s.symbols('R0:4', real=True))
# All homogeneous quartic monomials, not a sample.
monomials = []
for e0 in range(5):
    for e1 in range(5-e0):
        for e2 in range(5-e0-e1):
            e3 = 4-e0-e1-e2
            monomials.append(a**e0*b**e1*c**e2*d**e3)
for mon in monomials:
    hm = s.hessian(mon,coords)
    df = s.Matrix([s.diff(mon,z) for z in coords])
    atA = dict(zip(coords,A0))
    atR = dict(zip(coords,R0))
    zero((R0.T*hm.subs(atA)*R0)[0]-(A0.T*hm.subs(atR)*A0)[0], 'reciprocity')
    expanded = mon.subs(dict(zip(coords,A0+R0)))
    reconstructed = mon.subs(atA)+df.subs(atA).dot(R0)+(A0.T*hm.subs(atR)*A0)[0]/2+df.subs(atR).dot(A0)+mon.subs(atR)
    zero(expanded-reconstructed, 'quartic polarization')
assert len(monomials)==35
done('reciprocity and background polarization for all 35 monomials')

Ac,Bc,Cc,Ec,Gc,Hc,Lc,Mc,Nc=s.symbols('Ac Bc Cc Ec Gc Hc Lc Mc Nc', real=True)
Finv=Ac*u*u+Bc*v*v+Cc*u*v+Ec*w*w+Gc*u*w+Hc*v*w+Lc*q*u+Mc*q*v+Nc*q*w
Hinv=s.hessian(Finv,coords)
# Infinitesimal left SO(2) generator on the row-major entries.
rot=lambda F:s.expand(-c*s.diff(F,a)-d*s.diff(F,b)+a*s.diff(F,c)+b*s.diff(F,d))
images=[rot(mon) for mon in monomials]
rotmat=s.Matrix([[s.Poly(im,*coords).coeff_monomial(mon) for im in images] for mon in monomials])
assert 35-rotmat.rank()==9
zero(rot(Finv))
H11=Hinv.subs({a:1,b:0,c:0,d:0})
expected=s.Matrix([[12*Ac,3*Gc,0,3*Lc],[3*Gc,2*Cc+2*Ec,-Lc,Nc],[0,-Lc,4*Ac,Gc],[3*Lc,Nc,Gc,2*Cc]])
zero(H11-expected)
D=H11.extract([0,2],[0,2]);B=H11.extract([0,2],[1,3])
kern=-D.inv()*B*s.Matrix([b,d])
zero(kern-s.Matrix([-(Gc*b+Lc*d)/(4*Ac),(Lc*b-Gc*d)/(4*Ac)]))
zero(q.subs({a:kern[0],c:kern[1]})+Lc*(b*b+d*d)/(4*Ac))
Sch=H11.extract([1,3],[1,3])-B.T*D.inv()*B
zero(Sch.subs({Lc:0,Cc:Gc**2/(8*Ac),Ec:Gc**2/(4*Ac),Nc:0}))
done('complete invariant dimension and rank-one-background rank-two remainder')

# Complex coordinates relative to I,J,K,L.
f,eps,lam,gg,etaR,etaI=s.symbols('f eps lam gg etaR etaI', real=True)
i,j,k,l=s.symbols('i j k l', real=True)
zsq=i*i+j*j; wsq=k*k+l*l; zr=i*k+j*l; zi=j*k-i*l
p=12*f-lam; rr=4*f-lam
beta=(9*eps**2/p+eps**2/rr-2*lam)/4
delta=(9*eps**2/p-eps**2/rr)/4
Fgen=f*zsq**2+beta*zsq*wsq+gg*wsq**2+delta*(zr**2-zi**2)+eps*zsq*zr+wsq*(etaR*zr-etaI*zi)
CI=s.diff(Fgen,i)
CU=s.expand(CI.subs({i:-3*eps*k/p,j:-eps*l/rr}))
Pk=s.Poly(CU,k,l)
zero(Pk.coeff_monomial(k**3)-Pk.coeff_monomial(k*l**2)+4*lam**3*eps**3/(rr**2*p**3))
zero(Pk.coeff_monomial(l**3)-etaI)
zero(Pk.coeff_monomial(k*k*l)-etaI)
# The totally rank-one kernel gives precisely a convex sum.
Fnull=Fgen.subs({lam:0,eps:4*f,etaR:4*f,etaI:0}, simultaneous=True)
zero(Fnull-(f*((i+k)**2+(j+l)**2)**2+(gg-f)*wsq**2))
done('rank-two indefinite-kernel contradiction identity and totally-null reconstruction')

# Remaining upper-block boundary case: its acoustic test forces both mixed terms out.
tau,h,g0,ff,Z,W,t=s.symbols('tau h g0 ff Z W t', real=True)
Fb=ff*(zsq-wsq)**2+tau*zr**2+g0*wsq**2+h*wsq*zr
for sigma in (-1,1):
    test=Fb.subs({i:sigma*t,j:Z,k:t,l:W})
    second=s.diff(test,t,2).subs(t,0)
    zero(second-2*((2*tau*sigma+h)*Z*W+(2*g0+h*sigma)*W*W))
done('singular upper-block acoustic identities')

# Joint second-order contact eliminates the nonshear tangency.
P,R,V=s.symbols('P R V', positive=True)
fj=(P-R)/8; lambdaj=(P-3*R)/2; ej=P/3; gj=V-(P-9*R)/24
bj=P**2/(36*R)+3*R/4; dj=(P-P**2/(9*R))/4
Fjoint=fj*zsq**2+bj*zsq*wsq+gj*wsq**2+dj*(zr*zr-zi*zi)+ej*zsq*zr+R*wsq*zr
subphysical={i:(a+d)/2,j:(c-b)/2,k:(a-d)/2,l:(c+b)/2}
Fjphys=s.expand(Fjoint.subs(subphysical));Hj=s.hessian(Fjphys,coords)
M0=s.hessian(Hj[1,1],coords)/2
M1=s.hessian(2*Hj[0,1],coords)/2
M2=s.hessian(Hj[0,0],coords)/2
n=s.Matrix([0,-1,1,0]);U=s.Matrix([[1,0,0],[0,0,1],[0,0,1],[0,1,0]])
Cj=s.simplify(U.T*M0*U);bj0=s.simplify(U.T*M1*n);cj=(n.T*M2*n)[0]
zero(M0*n)
zero((n.T*M1*n)[0])
zero(Cj-s.Matrix([[(P-3*R)**2/(36*R)+V/4,-V/4,0],[-V/4,V/4,0],[0,0,3*V]]))
zero(Cj.det()-V**2*(P-3*R)**2/(48*R))
zero(cj-(bj0.T*Cj.inv()*bj0)[0]+(P-3*R)**4/(324*R**2*V))
# Surviving shear branch eps=rr: the cubic is independent of its radical.
hr=(48*f*f-40*f*lam+7*lam*lam)/p
CUshear=s.factor(CU.subs({eps:rr,etaR:hr,etaI:0}))
zero(CUshear+4*k**3*lam**3*rr/p**3)
zero(s.diff(CUshear,l))
bb1,bb2,zz,tt0=s.symbols('bb1 bb2 zz tt0',real=True)
vv=s.Matrix([-bb2*zz,bb1*zz]);bb0=s.Matrix([[bb1,bb2]]);NN=vv*bb0
zero(NN*NN);zero((s.eye(2)+tt0*NN)*(s.eye(2)-tt0*NN)-s.eye(2))
zero((s.eye(2)+tt0*NN).det()-1);zero(bb0*NN)
OUT['joint_contact_schur']='-(P-3*R)^4/(324*R^2*V)'
OUT['shear_kernel_cubic']='-4*k^3*lambda^3*(4*f-lambda)/(12*f-lambda)^3'
done('joint acoustic negative-curvature certificate and shear cubic invariance')

# Explicit tangent quartic G, independently differentiated and Gram-certified.
G=s.expand(3*(u+v-2*q)**2+s.Rational(35,24)*u*u+q*q-s.Rational(5,2)*q*u)
DG=s.Matrix([s.diff(G,z) for z in coords]);HG=s.hessian(G,coords)
coef={Ac:s.Rational(107,24),Bc:3,Cc:19,Ec:-13,Gc:0,Hc:0,Lc:-s.Rational(29,2),Mc:-12,Nc:0}
zero(G-Finv.subs(coef))
M11=s.hessian(HG[0,0],coords)/2;M12=s.hessian(HG[0,1],coords)/2;M22=s.hessian(HG[1,1],coords)/2
K=s.zeros(4);vals=[s.Integer(11),s.Rational(91,6),0,0,s.Integer(11),s.Rational(41,3)];nidx=0
for ii in range(4):
    for jj in range(ii+1,4):
        K[ii,jj]=vals[nidx];K[jj,ii]=-vals[nidx];nidx+=1
Q=M11.row_join(M12+K).col_join((M12-K).row_join(M22))
x1,x2=s.symbols('x1 x2',real=True)
rankdir=s.Matrix([x1,x2,0,0]);bil=s.Matrix.vstack(x1*X,x2*X)
zero((bil.T*Q*bil)[0]-(rankdir.T*HG*rankdir)[0])
null1=s.Matrix([-s.Rational(2,3),0,0,-s.Rational(2,3),0,-1,1,0])
null2=s.Matrix([0,0,0,0,1,0,0,1])
zero(Q*null1);zero(Q*null2)
mins=[s.factor(Q[:j0,:j0].det()) for j0 in range(1,7)]
assert mins==[s.Rational(107,2),642,s.Rational(1605,8),s.Rational(8445,16),s.Rational(2815,8),s.Rational(26865,4)]
assert Q.rank()==6
OUT['G_acoustic']={'coefficients':{str(kk):str(vv) for kk,vv in coef.items()},'K':strings(K),'Q':strings(Q),'leading_six_minors':list(map(str,mins)),'rank':6}
done('exact rank-six acoustic certificate for the unequal-orientation quartic G')

GI=G.subs(dict(zip(coords,I)));J=s.Matrix([1,0,0,-1]);GJ=G.subs(dict(zip(coords,J)))
assert GI==-s.Rational(1,24) and GJ==s.Rational(1271,24)
tscale=s.Integer(36)
polyconvex_gap=s.factor(tscale**2/(1+tscale**2)*(tscale**2*GI+GJ))
assert polyconvex_gap==-s.Rational(1350,1297)
contact=(I.T*HG*I)[0]+q
zero(contact-(3*a-2*d)**2/2-s.Rational(5,6)*c*c)
zero(DG.dot(I).subs({c:0,d:s.Rational(3,2)*a})+s.Rational(5,12)*a**3)
shearvar=s.symbols('shearvar',real=True)
zero(G.subs({a:1,b:shearvar,c:0,d:1})+s.Rational(1,24)-3*shearvar**4)
OUT['G_nonpolyconvex_gap']=str(polyconvex_gap)
done('negative polyconvex witness and semidefinite contact plane for G')

# Exact integration of the actual full-rank concentrating gradient profile.
sx,sy,rho=s.symbols('sx sy rho',positive=True)
ky=sy*(1-sy);j2=sx*(1-sx)
pieces=[(2*sx,0,s.Rational(1,3)),(1-sx,s.Rational(1,3),1)]
cache:dict[str,s.Expr]={}
def integrate_profile(expr:s.Expr, second_output:bool=True)->s.Expr:
    key=f'{second_output}:{expr}'
    if key in cache:return cache[key]
    total=s.Integer(0)
    for f1,lo,hi in pieces:
        subs={a:s.diff(f1,sx)*ky,b:f1*s.diff(ky,sy),c:s.diff(j2,sx)*ky if second_output else 0,d:j2*s.diff(ky,sy) if second_output else 0}
        pol=s.expand(expr.subs(subs))
        total+=s.integrate(s.integrate(pol,(sx,lo,hi)),(sy,0,1))
    total=s.factor(total);cache[key]=total;return total
HP=s.Matrix(4,4,lambda ii,jj:integrate_profile(HG[ii,jj]))
BP=s.Matrix([integrate_profile(z) for z in DG]);CP=integrate_profile(G)
CovP=s.Matrix(4,4,lambda ii,jj:integrate_profile(X[ii]*X[jj]));M4=integrate_profile((u+v)**2)
assert HP==s.Matrix([[s.Rational(2581,540),s.Rational(41,405),s.Rational(248,1215),-s.Rational(2189,540)],
 [s.Rational(41,405),s.Rational(47,15),s.Rational(121,36),-s.Rational(14,405)],
 [s.Rational(248,1215),s.Rational(121,36),s.Rational(1229,324),-s.Rational(41,405)],
 [-s.Rational(2189,540),-s.Rational(14,405),-s.Rational(41,405),s.Rational(494,135)]])
assert BP==s.Matrix([s.Rational(191,756),s.Rational(1231,11340),s.Rational(1439,11340),-s.Rational(2299,11340)])
assert CP==s.Rational(5951,58800) and M4==s.Rational(29023,1071630)
assert all(HP[:jj,:jj].det()>0 for jj in range(1,5))
assert CovP.rank()==4 and all(CovP[:jj,:jj].det()>0 for jj in range(1,5))
zero(s.Matrix([integrate_profile(z) for z in X]))
assert integrate_profile(q)==0
OUT['full_rank_profile']={'H':strings(HP),'b':strings(BP),'c':str(CP),'C':strings(CovP),'M4':str(M4),'covariance_rank':4}
done('all moments of an actual zero-boundary full-rank gradient profile')

Hbase=HG.subs({a:0,b:1,c:0,d:0})/2
assert Hbase==s.Matrix([[6,0,0,-6],[0,18,18,0],[0,18,19,0],[-6,0,0,6]])
assert Hbase.rank()==3;zero(Hbase*I)
Hr=Hbase+rho*HP;br=s.sqrt(rho)*BP;cr=s.Rational(3,2)+CP
minors=[s.factor(Hr[:jj,:jj].det()) for jj in range(1,5)]
for minor in minors:
    num,den=s.fraction(minor)
    assert den>0 and all(coef0>=0 for coef0 in s.Poly(num,rho).all_coeffs()) and minor.subs(rho,1)>0
loss=s.factor((br.T*Hr.inv()*br)[0]/2)
losslim=s.limit(loss,rho,0)
assert losslim==s.Rational(80089,21313530)
assert BP.dot(I)==s.Rational(283,5670) and (I.T*HP*I)[0]==s.Rational(179,540)
background=-Hr.inv()*br
zero(s.Matrix([s.limit(s.sqrt(rho)*z,rho,0) for z in background])+s.Rational(566,3759)*I)
gap=s.factor(cr-loss);gn,gd=s.fraction(gap)
assert all(cc>0 for cc in s.Poly(gn,rho).all_coeffs()) and all(cc>0 for cc in s.Poly(gd,rho).all_coeffs())
OUT['actual_nonpolyconvex_concentration']={'H0':strings(Hbase),'H_positive_minors':list(map(str,minors)),'loss':str(loss),'loss_limit':str(losslim),'gap':str(gap),'scaled_background_limit':strings(-s.Rational(566,3759)*I),'constant_M4':str(s.Rational(1,2)+M4)}
done('positive-definite H, positive covariance, nonzero limiting loss, and positive actual gaps')

# Simpler entirely convex version, independently using the same first profile.
Fconv=u*u+v*v;DC=s.Matrix([s.diff(Fconv,z) for z in coords]);HC=s.hessian(Fconv,coords)
Hpc=s.Matrix(4,4,lambda ii,jj:integrate_profile(HC[ii,jj],False));Bpc=s.Matrix([integrate_profile(z,False) for z in DC])
assert Hpc==s.diag(s.Rational(4,5),s.Rational(16,27),s.Rational(4,15),s.Rational(16,81))
assert Bpc==s.Matrix([s.Rational(2,35),0,0,0])
Hrc=s.diag(0,6,0,2)+rho*Hpc
assert s.factor((s.sqrt(rho)*Bpc).dot(Hrc.inv()*(s.sqrt(rho)*Bpc))/2)==s.Rational(1,490)
OUT['convex_concentration_loss']='1/490'
done('independent convex concentration example with loss exactly 1/490')

# A deliberately NONCOMPATIBLE bounded matrix law: not a QC counterexample.
weight=s.Rational(1,10**6);m=s.Integer(9);tt=s.Rational(9,2)*m*m*weight/(1-s.Rational(3,2)*weight)
Smat=s.Matrix([1,0,0,s.Rational(3,2)]);Rmat=s.Matrix([0,1,tt,0])
atoms=[Rmat,-Rmat,m*Smat,-2*m*Smat]
weights=[(1-s.Rational(3,2)*weight)/2]*2+[weight,weight/2]
def ev(expr,atom):return expr.subs(dict(zip(coords,atom)))
zero(sum((pp*atom for pp,atom in zip(weights,atoms)),s.zeros(4,1)))
assert sum(pp*ev(q,atom) for pp,atom in zip(weights,atoms))==0
Claw=sum((pp*atom*atom.T for pp,atom in zip(weights,atoms)),s.zeros(4))
Hlaw=sum((pp*ev(HG,atom) for pp,atom in zip(weights,atoms)),s.zeros(4))
blaw=sum((pp*ev(DG,atom) for pp,atom in zip(weights,atoms)),s.zeros(4,1))
claw=sum(pp*ev(G,atom) for pp,atom in zip(weights,atoms))
assert Claw.rank()==2
assert all(Hlaw[:jj,:jj].det()>0 for jj in range(1,5))
hh=(I.T*Hlaw*I)[0];bb=blaw.dot(I);badgap=s.factor(claw-bb*bb/(2*hh))
assert badgap==-s.Rational(11792123534471829388849317,15999928000107999946000000)
OUT['nongradient_law']={'warning':'NOT an actual gradient law; not a quasiconvexity counterexample','atoms':[strings(z) for z in atoms],'weights':list(map(str,weights)),'H_positive_minors':[str(s.factor(Hlaw[:jj,:jj].det())) for jj in range(1,5)],'directional_background':str(-bb/hh),'negative_directional_gap':str(badgap)}
done('bounded determinant-balanced law with negative gap, explicitly NOT compatible')

# A scalar-block illustration of the analytically proved matrix gluing law.
h0,k0,a0,j0,d0,e0,eps0=s.symbols('h0 k0 a0 j0 d0 e0 eps0', positive=True)
HH=s.Matrix([[eps0*k0,eps0*a0],[eps0*a0,h0+eps0*j0]])
bbvec=s.sqrt(eps0)*s.Matrix([d0,e0])
scalar_loss=s.factor((bbvec.T*HH.inv()*bbvec)[0]/2)
assert s.limit(scalar_loss,eps0,0)==d0*d0/(2*k0)
done('block-inverse concentration limit identity (analytic theorem handles all block sizes)')

OUT['checks_passed']=PASSED
OUT['scope']='Exact finite algebra only. Analytic theorems and limitations are proved in the accompanying note. No full quasiconvexity theorem or compatible negative-gap example is claimed.'
path=Path(__file__).with_name('positive_definite_verification.json')
path.write_text(json.dumps(OUT,indent=2)+'\n')
print(f'WROTE {path.name}; {len(PASSED)} groups passed.',flush=True)
