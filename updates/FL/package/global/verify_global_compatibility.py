#!/usr/bin/env python3
"""Exact algebra supporting GLOBAL_COMPATIBILITY.md.
Requires SymPy. No optimiser or saved search output is used.
Finite checks do not certify the analytic arguments or historical novelty.
"""
from __future__ import annotations
import json
from itertools import combinations_with_replacement, product
from pathlib import Path
import sympy as S
from sympy import QQ_I

ROOT=Path(__file__).resolve().parent
checks=[]; details={}
def passed(name):
    checks.append(name); print(f'PASS {len(checks):02d}: {name}',flush=True)
def zero(p):
    assert S.expand(p)==0

# Polynomial ingredients.
a,b,c,d=S.symbols('a b c d',real=True); xx=(a,b,c,d)
u=a*a+c*c; v=b*b+d*d; q=a*d-b*c
N=(u+v)**2
G=3*(u+v-2*q)**2+S.Rational(35,24)*u*u+q*q-S.Rational(5,2)*q*u
basis=[u*u,v*v,u*v,(a*b+c*d)**2,u*(a*b+c*d),v*(a*b+c*d),q*u,q*v,q*(a*b+c*d)]
monoms=[S.prod(xx[j] for j in inds) for inds in combinations_with_replacement(range(4),4)]
assert len(monoms)==35

# Exact flux identity for every quartic monomial and arbitrary B,k,r,grad r.
# At theta=0 the circular carrier has V=e1,W=e2,V'=W,W'=-V.
# Differentiation of the primitive includes BOTH its base and its direction.
B=S.Matrix(S.symbols('B0:4')); k1,k2,r,t,h1,h2=S.symbols('k1 k2 r t h1 h2',real=True)
Vk=S.Matrix([k1,k2,0,0]); Wk=S.Matrix([0,0,k1,k2]); Q=S.Matrix([h1,h2,0,0])
base=B+t*Wk
for f in monoms:
    df=S.Matrix([S.diff(f,z) for z in xx]); hf=S.hessian(f,xx)
    sub=dict(zip(xx,base)); dfs=df.subs(sub,simultaneous=True); hfs=hf.subs(sub,simultaneous=True)
    pr=[]; dtheta=[]
    for i in range(2):
        ve=S.eye(4)[:,i]; we=S.eye(4)[:,i+2]
        pr.append(S.integrate(S.expand(dfs.dot(ve)),(t,0,r)))
        dtheta.append(S.integrate(S.expand(-t*(Vk.T*hfs*ve)[0]+dfs.dot(we)),(t,0,r)))
    div=S.diff(pr[0],r)*h1+S.diff(pr[1],r)*h2+k1*dtheta[0]+k2*dtheta[1]
    acoustic=S.integrate(S.expand(t*(Vk.T*hfs*Vk)[0]),(t,0,r))
    fbase=f.subs(dict(zip(xx,B+r*Wk)),simultaneous=True)
    fB=f.subs(dict(zip(xx,B)),simultaneous=True)
    dfbase=df.subs(dict(zip(xx,B+r*Wk)),simultaneous=True)
    zero(div-(dfbase.dot(Q)+fbase-fB-acoustic))
passed('circular flux/divergence identity: all 35 monomials, symbolic B,k,r and gradient')

# Two exact scalar completions used for all-background coercivity.
A,L,C,z=S.symbols('A L C z',nonzero=True)
zero(A+L+C-A/3-(3*(L+4*A/3)**2/(8*A)+C-3*L**2/(8*A)))
I=A*z**4/4+L*z**3/3+C*z**2/2
zero(I-A*z**4/36-(z**2*(L+4*A*z/3)**2/(8*A)+z**2*(C-L**2/(4*A))/2))
x,y=S.symbols('x y')
zero(12*(x*x/3+y*y/9)-(x+y)**2-(3*x-y)**2/3)
# Invariance supplies the leading acoustic coefficient 4F(e2 tensor k).
for f in basis:
    hf=S.hessian(f,xx).subs(dict(zip(xx,Wk)),simultaneous=True)
    zero((Vk.T*hf*Vk)[0]-4*f.subs(dict(zip(xx,Wk)),simultaneous=True))
passed('quartic rank-one Bregman margin, weighted acoustic margin, and mu/12 constant')

# Reconstruct G's global rank-one convexity certificate.
M11=S.hessian(S.diff(G,a,2),xx)/2
M12=S.hessian(S.diff(G,a,b),xx)/2
M22=S.hessian(S.diff(G,b,2),xx)/2
K=S.zeros(4)
pairs=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
for (i,j),val in zip(pairs,[11,S.Rational(91,6),0,0,11,S.Rational(41,3)]): K[i,j]=val;K[j,i]=-val
Gram=M11.row_join(M12+K).col_join((M12-K).row_join(M22))
minors=[Gram[:i,:i].det() for i in range(1,7)]
assert minors==[S.Rational(107,2),642,S.Rational(1605,8),S.Rational(8445,16),S.Rational(2815,8),S.Rational(26865,4)]
T=Gram[:6,:6];U=Gram[:6,6:]
assert Gram[6:,6:]-U.T*T.inv()*U==S.zeros(2)
witness=(36**4*G.subs({a:1,b:0,c:0,d:1})+36**2*G.subs({a:1,b:0,c:0,d:-1}))/(1+36**2)
assert witness==-S.Rational(1350,1297)
zero(G-3*N-S.Rational(35,24)*u*u -q*(-12*(u+v)+13*q-S.Rational(5,2)*u))
details['G_acoustic_leading_minors']=[str(z) for z in minors]
passed('G: exact PSD acoustic Gram, rank-one lower bound mu=3, non-polyconvex witness')

# Exact two-dimensional Fourier algebra over Q(i).
class Fourier:
    def __init__(self,coeff=None):
        self.c={tuple(k):QQ_I.convert(v) for k,v in (coeff or {}).items() if v!=0}
    def __add__(self,o):
        if not isinstance(o,Fourier): o=Fourier({(0,0):o})
        d=self.c.copy()
        for k,v in o.c.items(): d[k]=d.get(k,QQ_I.zero)+v
        return Fourier({k:v for k,v in d.items() if v})
    __radd__=__add__
    def __neg__(self):return Fourier({k:-v for k,v in self.c.items()})
    def __sub__(self,o):return self+-o
    def __rsub__(self,o):return -self+o
    def __mul__(self,o):
        if not isinstance(o,Fourier):return Fourier({k:v*QQ_I.convert(o) for k,v in self.c.items()})
        d={}
        for k,v in self.c.items():
            for l,w in o.c.items():
                m=(k[0]+l[0],k[1]+l[1]);d[m]=d.get(m,QQ_I.zero)+v*w
        return Fourier({k:v for k,v in d.items() if v})
    __rmul__=__mul__
    def __pow__(self,n):
        out=Fourier({(0,0):1})
        for _ in range(n):out=out*self
        return out
    def diff(self,j):return Fourier({k:v*QQ_I.convert(S.I*k[j]) for k,v in self.c.items()})
    def mean(self):
        out=QQ_I.to_sympy(self.c.get((0,0),QQ_I.zero));assert S.im(out)==0;return S.re(out)
    def dilate(self,n):return Fourier({(n*k[0],n*k[1]):v for k,v in self.c.items()})

def cos(k):return Fourier({k:S.Rational(1,2),(-k[0],-k[1]):S.Rational(1,2)})
def sin(k):return Fourier({k:1/(2*S.I),(-k[0],-k[1]):-1/(2*S.I)})
def derivative(pot):return [pot[0].diff(0),pot[0].diff(1),pot[1].diff(0),pot[1].diff(1)]
def evaluate(poly,X):
    out=Fourier()
    for powers,coef in S.Poly(poly,*xx).terms():
        term=Fourier({(0,0):coef})
        for t,n in zip(X,powers):
            if n:term=term*t**n
        out=out+term
    return out

def moments(f,X):
    C=S.Matrix(4,4,lambda i,j:(X[i]*X[j]).mean())
    H=S.Matrix(4,4,lambda i,j:evaluate(S.diff(f,xx[i],xx[j]),X).mean())
    b=S.Matrix([evaluate(S.diff(f,z),X).mean() for z in xx])
    c=evaluate(f,X).mean();n4=evaluate(N,X).mean()
    assert [z.mean() for z in X]==[0]*4
    assert evaluate(q,X).mean()==0
    return C,H,b,c,n4

def summary(f,X):
    C,H,b,c,n4=moments(f,X)
    assert all(H[:i,:i].det()>0 for i in range(1,5))
    B=-H.inv()*b;delta=c+(b.dot(B))/2
    return {'C':C,'H':H,'b':b,'c':c,'n4':n4,'B':B,'delta':delta}
def record(z):
    return {k:([str(x) for x in v] if isinstance(v,S.MatrixBase) else str(v)) for k,v in z.items()}

# A full-rank field far from every rank-one line.
r0=1+S.Rational(1,2)*cos((1,0))
X0=derivative([r0*cos((0,1)),r0*sin((0,1))])
z0=summary(G,X0)
assert z0['C']==S.diag(S.Rational(1,16),S.Rational(9,16),S.Rational(1,16),S.Rational(9,16))
assert z0['b']==S.zeros(4,1)
assert z0['n4']==S.Rational(33,16)
assert z0['delta']>=z0['n4']/4
details['far_from_any_line']=record(z0)
passed('compatible circular modulation: full covariance, captured fraction 9/20, exact positive gap')

# Real two-dimensional amplitude: internally resonant and nonzero cubic.
rr=1+S.Rational(1,3)*cos((1,0))+S.Rational(1,4)*cos((0,1))+S.Rational(1,5)*cos((1,1))
pot=[rr*cos((0,1)),rr*sin((0,1))]
X=derivative(pot);z=summary(G,X)
assert z['b']!=S.zeros(4,1)
assert z['delta']>=z['n4']/4
assert z['C'].det()>0
details['two_dimensional_amplitude']=record(z)
# Verify that this is one connected primitive-resonance component, not separated waves.
def canon(k):
    return k if (k[0]>0 or (k[0]==0 and k[1]>0)) else (-k[0],-k[1])
freq=sorted(set().union(*(set(t.c) for t in X))-{(0,0)})
vertices=sorted({canon(k) for k in freq});parent={k:k for k in vertices}
def root(k):
    while parent[k]!=k:k=parent[k]
    return k
edge_count={3:0,4:0}
for degree in (3,4):
    for ks in combinations_with_replacement(freq,degree):
        if tuple(map(sum,zip(*ks)))!=(0,0):continue
        if any(ks[i][0]+ks[j][0]==0 and ks[i][1]+ks[j][1]==0 for i in range(degree) for j in range(i+1,degree)):continue
        edge_count[degree]+=1
        targets=[canon(k) for k in ks]
        for k in targets[1:]:parent[root(k)]=root(targets[0])
assert len({root(k) for k in vertices})==1
assert edge_count[3]>0 and edge_count[4]>0
details['two_dimensional_amplitude']['frequency_classes']=vertices
details['two_dimensional_amplitude']['primitive_resonance_counts']=edge_count
passed('two-dimensional resonant amplitude: nonzero b, complete affine minimization, connected triad/quartet graph')

# Exact degree-four independent dilation and optimized gluing.
# Base support max infinity norm 2; a dilation by 17 separates all short cross relations.
Y=[f.dilate(17) for f in X0]
zY=summary(G,Y)
zsum=summary(G,[p+q for p,q in zip(X,Y)])
assert zsum['H']==z['H']+zY['H'] and zsum['b']==z['b']+zY['b']
cross=(z['H']*zY['C']).trace()/2
assert zsum['c']==z['c']+zY['c']+cross
penalty=((z['B']-zsum['B']).T*z['H']*(z['B']-zsum['B']))[0]/2
penalty+=((zY['B']-zsum['B']).T*zY['H']*(zY['B']-zsum['B']))[0]/2
assert S.cancel(zsum['delta']-z['delta']-zY['delta']-cross-penalty)==0
assert cross>=0 and penalty>=0
details['dilated_packet_sum']={'cross_energy':str(cross),'background_disagreement':str(penalty),'delta':str(zsum['delta']),'n4':str(zsum['n4'])}
passed('actual Fourier packet gluing: covariance interaction and all-background disagreement identity')

# A compatible resonant obstruction to extending that gluing without hypotheses.
rr=1+S.Rational(1,2)*cos((1,0));ss=1-S.Rational(1,2)*cos((1,0))
X1=derivative([rr*cos((0,1)),rr*sin((0,1))])
X2=derivative([ss*cos((0,2)),ss*sin((0,2))])
xsum=[p+q for p,q in zip(X1,X2)]
c1=evaluate(q*q,X1).mean();c2=evaluate(q*q,X2).mean();ct=evaluate(q*q,xsum).mean()
assert c1==S.Rational(17,128) and c2==S.Rational(17,32)
assert ct==S.Rational(75,256) and ct-c1-c2==-S.Rational(95,256)
assert moments(q*q,X1)[2]==S.zeros(4,1) and moments(q*q,X2)[2]==S.zeros(4,1)
details['resonant_gluing_obstruction']={'c1':str(c1),'c2':str(c2),'c_sum':str(ct),'difference':str(ct-c1-c2)}
passed('compatible two-carrier resonance: exact negative interaction -95/256, not a negative QC gap')

# General variable-phase defect: Hessian(theta) appears with the asserted sign.
# Fix theta=0 as above and allow an arbitrary symmetric phase Hessian.
h11,h12,h22=S.symbols('h11 h12 h22');KH=S.Matrix([[h11,h12],[h12,h22]])
for f in monoms:
    df=S.Matrix([S.diff(f,z) for z in xx]); hf=S.hessian(f,xx)
    sub=dict(zip(xx,B+t*Wk));dfs=df.subs(sub,simultaneous=True);hfs=hf.subs(sub,simultaneous=True)
    pr=[S.integrate(S.expand(dfs[i]),(t,0,r)) for i in range(2)]
    extra=sum(S.diff(pr[i],kj)*KH[j,i] for i in range(2) for j,kj in enumerate((k1,k2)))
    target=0
    for i in range(2):
        Wki=S.Matrix([0,0,KH[0,i],KH[1,i]])
        target+=S.integrate(S.expand(t*(Wki.T*hfs*S.eye(4)[:,i])[0]),(t,0,r))
    zero(extra-target)
passed('all 35 monomials: exact variable-phase curvature defect (no sign assertion)')

# At B=0 in the left-SO(2) cone, phase curvature depends only on q-odd coefficients.
Lc,Mc,Nc=S.symbols('Lc Mc Nc')
FO=Lc*q*u+Mc*q*v+Nc*q*(a*b+c*d)
# The derivative in the orthogonal output direction is Xi=M(k)*(k2,-k1).
Xi=S.Matrix([(S.diff(FO,z).subs(dict(zip(xx,Wk)),simultaneous=True)) for z in (a,b)])
Mk=Lc*k1*k1+Mc*k2*k2+Nc*k1*k2
assert S.simplify(Xi-Mk*S.Matrix([k2,-k1]))==S.zeros(2,1)
for f in basis[:6]:
 assert S.Matrix([S.diff(f,z).subs(dict(zip(xx,Wk)),simultaneous=True) for z in (a,b)])==S.zeros(2,1)
# theta=x+eps sin(y), r^4=1+beta sin(2y): average defect = Mc eps^2 beta/8.
eps,bet,yy=S.symbols('eps bet yy',real=True)
divXi=sum(S.diff(Xi[i],kj)*KH[j,i] for i in range(2) for j,kj in enumerate((k1,k2)))
phase_sub={k1:1,k2:eps*S.cos(yy),h11:0,h12:0,h22:-eps*S.sin(yy),Nc:0}
defect=S.expand_trig(divXi.subs(phase_sub))* (1+bet*S.sin(2*yy))/4
avg=S.integrate(S.expand_trig(defect),(yy,0,2*S.pi))/(2*S.pi)
zero(avg-Mc*eps**2*bet/8)
# Convex Fc=(u+v-2q)^2 has Mc=-4. eps=1,beta=-1/2 gives positive signed defect 1/4.
assert avg.subs({Mc:-4,eps:1,bet:-S.Rational(1,2)})==S.Rational(1,4)
details['phase_curvature_example']={'F':'(u+v-2q)^2, convex','theta':'x+sin(y)',
 'amplitude_fourth_power':'1-sin(2y)/2','mean_signed_defect':'1/4'}
passed('variable phase in the invariant cone: exact signed defect, positive even for a convex quartic')

out={'scope':'Exact finite checks; analytic theorems are proved in GLOBAL_COMPATIBILITY.md. No novelty or formal-proof certification.',
     'checks':checks,'details':details}
(ROOT/'global_verification.json').write_text(json.dumps(out,indent=2))
print('WROTE global_verification.json;',len(checks),'groups passed.',flush=True)
