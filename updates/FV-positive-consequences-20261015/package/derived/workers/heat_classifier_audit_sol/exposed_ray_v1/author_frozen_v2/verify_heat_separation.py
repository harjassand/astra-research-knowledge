#!/usr/bin/env python3
"""Standalone exact exposed-ray and corrected-heat obstruction verifier.

Requires SymPy only. Every mathematical constant is written below. It reads
no candidate, optimization output, certificate JSON, repo file or network.
The analytic averaging, cone and variational arguments are in PROOF.md.
"""
from pathlib import Path
from itertools import combinations_with_replacement,product
import json,time
import sympy as s
ROOT=Path(__file__).resolve().parent
tick=time.monotonic();checks=[]
def record(label):checks.append(label);print('PASS:',label,flush=True)
def zero(z):assert s.expand(z)==0
def same(A,B):assert A.shape==B.shape and all(s.expand(z)==0 for z in A-B)
x=s.symbols('a b c d');h=s.symbols('h0:6');k=s.symbols('k');a,b,c,d=x
u=a*a+c*c;v=b*b+d*d;w=a*b+c*d;q=a*d-b*c
fs=[u*u,v*v,u*v,w*w,u*w,v*w,q*u,q*v,q*w]
p=s.Matrix([1,1,s.Rational(166,3),-s.Rational(460,9),0,0,-s.Rational(52,9),s.Rational(52,9),0])
F=sum(pp*f for pp,f in zip(p,fs));HF=s.hessian(F,x)
zero(-c*s.diff(F,a)-d*s.diff(F,b)+a*s.diff(F,c)+b*s.diff(F,d))
zero(F.subs(dict(zip(x,(b,a,d,c))),simultaneous=True)-F)
zero(F.subs(dict(zip(x,(a,-b,-c,d))),simultaneous=True)-F)
normalization=s.Matrix([[16,16,8,4,0,0,0,0,0]])*p
assert normalization[0]==s.Rational(2432,9)
record('Integrand, left rotations, finite symmetries and exact normalization')

# Full acoustic Gram and a rational rank-four positive factor.
R=s.Matrix([1,k,0,0]);g=(R.T*HF*R)[0];M=s.hessian(g,x)/2
M11=M.subs(k,0);M12=M.diff(k).subs(k,0)/2;M22=M.diff(k,2)/2
K=s.zeros(4)
for (i,j),z in zip([(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)],
                  [s.Rational(8,9),s.Rational(8,9),0,0,-s.Rational(8,9),s.Rational(488,9)]):
    K[i,j]=z;K[j,i]=-z
Q=M11.row_join(M12+K).col_join((M12-K).row_join(M22))
B=s.zeros(8,4)
for col,positions,entries in [
 (0,[0,3,5,6],[2,-1,2,-1]),(1,[0,3,5,6],[1,-9,-1,9]),
 (2,[1,2,4,7],[3,2,3,2]),(3,[1,2,4,7],[1,1,-1,-1])]:
    for i,z in zip(positions,entries):B[i,col]=z
W=s.diag(s.Rational(8,3),s.Rational(4,3),s.Rational(8,9),s.Rational(4,9))
same(Q,B*W*B.T);assert B.rank()==4
y=s.Matrix(list(x)+[k*z for z in x]);zero((y.T*Q*y)[0]-g)
record('Universal acoustic identity and positive rank-four rational factor')

# Pointwise positivity is separate from quasiconvexity.
r=u-v;t0=2*w;d0=2*q
zero(F-(r-s.Rational(13,9)*d0)**2-s.Rational(14,9)*t0*t0-s.Rational(992,81)*d0*d0)
zero((u+v)**2-r*r-t0*t0-d0*d0)
Kcoerce=s.Matrix([[s.Rational(1,2),0,-s.Rational(13,9)],
 [0,s.Rational(19,18),0],[-s.Rational(13,9),0,s.Rational(83,6)]])
assert all(Kcoerce[:j,:j].det()>0 for j in range(1,4))
record('Pointwise lower bound F >= |A|^4/2, without a Jensen conclusion')

P=17*k**4-314*k*k+17
assert s.Poly(P,k).count_roots(-s.oo,s.oo)==4
AA=s.Matrix([203-17*k*k,k*(85*k*k-1551),2*k*(944-51*k*k),134])
assert all(s.rem(s.expand(z),P,k)==0 for z in M*AA)
zero(s.factor(M.det())-s.Rational(1024,729)*P*P)
detder=s.rem(s.expand(AA[3]-k*AA[2]),P,k)
assert detder==4*(8-k*k) and s.gcd(P,detder)==1
record('Four real acoustic contacts and nonzero determinant derivative')

# Complete closed-form parametrization, before imposing output invariance.
b1=s.Matrix([h[0],h[1],h[3],h[4]]);b2=s.Matrix([h[1],h[2],h[4],h[5]])
aps=list(combinations_with_replacement(range(4),2));hps=list(combinations_with_replacement(range(6),2))
def exp_pair(pair,n):
    e=[0]*n
    for i in pair:e[i]+=1
    return tuple(e)
indices={exp_pair(aa,4)+exp_pair(hh,6):i for i,(aa,hh) in enumerate(product(aps,hps))}
def vec(poly):
    out=s.zeros(210,1)
    for e,z in s.Poly(s.expand(poly),*(x+h)).terms():
        if z:out[indices[e]]=z
    return out
def curl_density(alpha):
    om=s.zeros(4)
    for i in range(4):
        for j in range(i+1,4):
            om[i,j]=s.diff(alpha[j],x[i])-s.diff(alpha[i],x[j]);om[j,i]=-om[i,j]
    return (b1.T*om*b2)[0]
allclosed=[]
for aa in combinations_with_replacement(range(4),3):
    pp=s.prod(x[i] for i in aa)
    for j in range(4):
        alpha=s.zeros(4,1);alpha[j]=pp;allclosed.append(curl_density(alpha))
N=s.Matrix.hstack(*[vec(z) for z in allclosed]);assert N.rank()==45
def rot(poly):
    return (-c*s.diff(poly,a)-d*s.diff(poly,b)+a*s.diff(poly,c)+b*s.diff(poly,d)
     -h[3]*s.diff(poly,h[0])-h[4]*s.diff(poly,h[1])-h[5]*s.diff(poly,h[2])
     +h[0]*s.diff(poly,h[3])+h[1]*s.diff(poly,h[4])+h[2]*s.diff(poly,h[5]))
LN=s.Matrix.hstack(*[vec(rot(z)) for z in allclosed]);assert LN.rank()==30
linear={
 'dv':s.Matrix([0,2*b,0,2*d]),'dw':s.Matrix([b,a,d,c]),'dq':s.Matrix([d,-c,-b,a]),
 'theta_u':s.Matrix([-c,0,a,0]),'theta_v':s.Matrix([0,-d,0,b]),
 'theta_cross':s.Matrix([-d,-c,b,a]),'zeta':s.Matrix([-b,a,-d,c])}
quads={'u':u,'v':v,'w':w}
names=['u * dv','u * dw','u * dq','u * theta_u','u * theta_v','u * theta_cross','u * zeta',
       'v * dw','v * dq','v * theta_u','v * theta_v','v * theta_cross','v * zeta','w * theta_cross','w * zeta']
densities=[]
for name in names:
    qn,ln=name.split(' * ');dd=curl_density(quads[qn]*linear[ln]);zero(rot(dd));densities.append(dd)
Ni=s.Matrix.hstack(*[vec(z) for z in densities]);assert Ni.rank()==15
record('All closed quadratic corrections: dimension45, invariant dimension15, complete explicit basis')

# Every constant strongly parabolic matrix diffusion averages to Δ+2βJ∂xy.
heat=(b1.T*HF*b1+b2.T*HF*b2)[0]
J=s.Matrix([[0,0,-1,0],[0,0,0,-1],[1,0,0,0],[0,1,0,0]])
rotating=(b1.T*HF*J*b2+b2.T*HF*J*b1)[0]
unknowns=s.symbols('c0:15')+(s.symbols('beta'),)
poly=heat+sum(cc*dd for cc,dd in zip(unknowns,densities+[rotating]))
hnull=dict(zip(h,(1,k,k*k,0,0,0)));asub=dict(zip(x,AA))
def coeff4(z):
    zz=s.Poly(s.rem(s.expand(z),P,k),k);return [zz.nth(i) for i in range(4)]
def contact_column(dd):
    return s.Matrix([z for hh in h for z in coeff4(s.diff(dd,hh).subs(hnull).subs(asub,simultaneous=True))])
C=s.Matrix.hstack(*[contact_column(dd) for dd in densities+[rotating]])
rhs=-contact_column(heat)
swap=dict(zip(x+h,(b,a,d,c,h[2],h[1],h[0],h[5],h[4],h[3])))
flip=dict(zip(x+h,(a,-b,-c,d,h[0],-h[1],h[2],-h[3],h[4],-h[5])))
eq=[]
for change in [swap,flip]:eq.extend(s.Poly(s.expand(poly-poly.subs(change,simultaneous=True)),*(x+h)).coeffs())
Ts,bs=s.linear_eq_to_matrix(eq,unknowns);T=C.col_join(Ts);rr=rhs.col_join(bs)
assert T.rank()==15 and T.row_join(rr).rank()==15
sol=list(s.linsolve((T,rr)))[0];param=sorted(set().union(*(z.free_symbols for z in sol)),key=str)
assert len(param)==1;tt=param[0]
expected=(0,-93*tt/59-s.Rational(5456,177),0,83*tt/177-s.Rational(9920,531),
 s.Rational(21328,531)-382*tt/177,0,tt,93*tt/59+s.Rational(5456,177),0,
 382*tt/177-s.Rational(21328,531),s.Rational(9920,531)-83*tt/177,0,tt,0,0,0)
assert all(s.factor(z-v0)==0 for z,v0 in zip(sol,expected))
assert sol[-1]==0
corrected=s.expand(poly.subs(dict(zip(unknowns,sol)),simultaneous=True))
record('Acoustic kernels and finite symmetries force beta=0 and exactly one correction parameter')

atoms=[([1,0,0,2],[0,1,0,0,0,-1]),([1,-1,0,2],[0,0,1,-1,0,0])]
values=[s.factor(corrected.subs(dict(zip(x+h,A0+H0)))) for A0,H0 in atoms]
assert s.expand(values[0]-(s.Rational(274,59)*tt-s.Rational(192260,531)))==0
assert s.expand(values[1]-(s.Rational(25120,177)-s.Rational(1172,177)*tt))==0
lower=s.Rational(96130,1233);upper=s.Rational(6280,293);assert lower>upper
zero(586*values[0]+411*values[1]+s.Rational(81691400,531))
record('Two rational jet tests contradict pointwise positivity, without an SOS restriction')

# Exposed extremality in the full nine-dimensional rank-one-convex cone.
Ms=[s.hessian((R.T*s.hessian(f,x)*R)[0],x)/2 for f in fs]
columns=[];ell=[]
for mm in Ms:
    col=[z for val in mm*AA for z in coeff4(val)]
    col.extend(coeff4((AA.T*mm.diff(k)*AA)[0]));columns.append(s.Matrix(col))
    ev=coeff4((AA.T*mm*AA)[0]);ell.append(4*ev[0]+s.Rational(628,17)*ev[2])
ext=s.Matrix.hstack(*columns);assert ext.rank()==8 and ext*p==s.zeros(20,1)
lc=s.ilcm(*(s.denom(z) for z in ell));ell=[z*lc for z in ell];gc=s.igcd(*(int(z) for z in ell));ell=[int(z/gc) for z in ell]
assert ell==[910741,1453621,324775,321232,0,0,244987,-432907,0]
assert sum(z*pp for z,pp in zip(ell,p))==0
record('Exact rank-eight contact criticality and rational exposed-ray functional')

result={'schema':'astra-exposed-ray-heat-separation/1','status':'EXACT_PASS','groups':len(checks),'checks':checks,
 'coefficient_order':['u^2','v^2','uv','w^2','uw','vw','qu','qv','qw'],'coefficients':[str(z) for z in p],
 'normalization_lambda':str(normalization[0]),'contact_polynomial':str(P),'contact_A':[str(z) for z in AA],
 'acoustic_factor_B':[[str(z) for z in row] for row in B.tolist()],'acoustic_factor_weights':[str(z) for z in W.diagonal()],
 'complete_invariant_correction_basis':names,'contact_symmetry_solution':[str(z) for z in sol],
 'pointwise_atoms':[{'A':A0,'H':H0,'evaluation':str(val)} for (A0,H0),val in zip(atoms,values)],
 'incompatible_parameter_bounds':[str(lower),str(upper)],'positive_combination_weights':[586,411],
 'positive_combination_value':'-81691400/531','exposing_functional':ell,
 'polyconvexity':'UNKNOWN','quasiconvexity':'UNKNOWN','full_heat_plus_polyconvex_cone':'UNKNOWN',
 'scope':'Pointwise closed-quadratic-form certificates for fixed strongly parabolic constant-coefficient linear diffusion; also nonnegative determinant-square supplement.',
 'not_a_gradient_law':True,'external_review':'UNKNOWN','historical_priority':'UNKNOWN','seconds':time.monotonic()-tick}
(ROOT/'HEAT_SEPARATION_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'EXACT_PASS','groups':len(checks),'seconds':result['seconds'],'PC':'UNKNOWN','QC':'UNKNOWN'},indent=2))
