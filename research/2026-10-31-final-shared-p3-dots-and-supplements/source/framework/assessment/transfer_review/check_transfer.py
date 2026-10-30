"""Independent targeted checks of the post-comparison F0 transfer.

No imports from construction artifacts. Run with python3 -B.
"""
import sympy as s
from itertools import combinations_with_replacement

x,y,u,v=s.symbols('x y u v',real=True)
V=s.Matrix([x,y,u,v]);r=x*x+y*y;t=u*u+v*v
F=t*t+2*r*t;HF=s.hessian(F,V)
basis=[s.diff(F,z) for z in V]+[x*(u*u-v*v),2*x*u*v,y*(u*u-v*v),2*y*u*v]
quad=[a*b for a,b in combinations_with_replacement(V,2)]
R=[s.Matrix([1,0,1,0]),s.Matrix([1,0,-1,0]),s.Matrix([2,0,0,2])]
X=[s.Matrix([0,0,-s.Rational(1,4),0]),s.Matrix([0,0,s.Rational(1,4),0]),s.zeros(4,1)]
amp=s.symbols('a b d',nonzero=True,real=True)
kappa=s.symbols('kappa',real=True)
cs=s.symbols('c0:3',real=True)
G=sum((Ri*ai*ci for Ri,ai,ci in zip(R,amp,cs)),s.zeros(4,1))
wi=[ai*ai/2 for ai in amp]
Ai=[s.prod(amp)*kappa*Xi/w for Xi,w in zip(X,wi)]
M=s.Matrix(s.symbols('m0:4',real=True))

def average(poly):
    out=s.S.Zero
    for powers,coeff in s.Poly(s.expand(poly),*cs).terms():
        if sum(powers)==0: val=1
        elif sorted(powers)==[0,0,2]: val=s.Rational(1,2)
        elif powers==(1,1,1): val=kappa/4
        elif sorted(powers)==[0,0,4]: val=s.Rational(3,8)
        elif sorted(powers)==[0,2,2]: val=s.Rational(1,4)
        else: val=0
        out+=coeff*val
    return s.expand(out)

E=s.cancel(sum(w*(A.T*HF.subs(dict(zip(V,Ri)))*A)[0]/2 for Ri,w,A in zip(R,wi,Ai)))
f=average(F.subs(dict(zip(V,G)),simultaneous=True))
for j,p in enumerate([F]+basis+quad):
    gap=average(p.subs(dict(zip(V,M+G)),simultaneous=True))-p.subs(dict(zip(V,M)),simultaneous=True)
    HP=s.hessian(p,V)
    hsum=sum(w*(Ri.T*HP.subs(dict(zip(V,M+A)),simultaneous=True)*Ri)[0]/2 for Ri,w,A in zip(R,wi,Ai))
    rhs=hsum+(f-E if j==0 else 0)
    assert s.cancel(gap-rhs)==0
print('PASS: exact all-mean identity, symbolically in all amplitudes/relative phase, separately for F0, all eight actual cubic basis elements and all ten quadratic monomials.')

# Derive the ancillary fixed-P0 five-condition optimum independently.
A,B,D=s.symbols('A B D',positive=True)
weights=[A/2,B/2,D/2]
C0=basis[4]+basis[7]
g=s.Matrix([s.diff(C0,z) for z in V])
Hs=[HF.subs(dict(zip(V,Ri))) for Ri in R]
gs=[g.subs(dict(zip(V,Ri))) for Ri in R]
H=sum((w*Hi for w,Hi in zip(weights,Hs)),s.zeros(4))
wg=sum((w*gi for w,gi in zip(weights,gs)),s.zeros(4,1))
tau=sum(w*(gi.T*Hi.pinv()*gi)[0] for w,gi,Hi in zip(weights,gs,Hs))
K=H.row_join(wg).col_join(wg.T.row_join(s.Matrix([[tau]])))
b0=s.Matrix([-4,0,0,0,-1])
emin=s.factor(A*B*D*kappa*kappa*(b0.T*K.inv()*b0)[0]/2)
target=kappa*kappa*2*A*B*D*(A+B+2*D)/(2*A*B+D*(A+B))
assert s.cancel(emin-target)==0
assert s.factor(kappa*kappa*D*(A+B)-emin)==kappa*kappa*D*D*(A-B)**2/(A*D+2*A*B+B*D)
print('PASS: independent five-condition minimum-cost formula and its upper bound by the explicit all-eight-mode construction.')

# Derive cross-Hessian angular formula directly from F0, rather than its printed score.
ss,tt,zz,ww=s.symbols('s t z w',real=True)
RR=s.Matrix([1,0,1,0]);SS=s.Matrix([ss,zz,tt,ww])
score=s.expand((SS.T*HF.subs(dict(zip(V,RR)))*SS)[0])
score=score.subs({zz**2:1-ss**2,ww**2:1-tt**2}).expand()
assert s.expand(score-(12+8*tt*tt+16*ss*tt))==0
assert s.expand(score-(4+2*(ss+tt)**2)-6*(ss+tt)**2-8*(1-ss*ss))==0
print('PASS: cross-Hessian dominance independently derived using unit conformal components.')

# Exhaust the potentially dangerous mixed relations for two adjacent largest base blocks.
# The analytical integer-component argument, recorded in the review, covers every
# number of lower blocks. This is a finite implementation check of the worst base support.
freq=[(1,0),(0,1),(1,1),(2,1)]
signed=[(block,sgn*k[0]*scale,sgn*k[1]*scale)
        for block,scale in [(0,1),(1,9)] for k in freq for sgn in [-1,1]]
mixed=0
for length in [2,3,4]:
    for inds in combinations_with_replacement(range(len(signed)),length):
        entries=[signed[i] for i in inds]
        if len({e[0] for e in entries})<2: continue
        if sum(e[1] for e in entries) or sum(e[2] for e in entries): continue
        mixed+=1
        assert length==4
        for block in [0,1]:
            part=[e for e in entries if e[0]==block]
            assert len(part)==2 and sum(e[1] for e in part)==sum(e[2] for e in part)==0
print('PASS: all mixed zero sums of length <=4 for adjacent scale-9 four-wave supports are precisely opposite pairs in each block; count =',mixed)
