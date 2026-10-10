"""Exact rational checks of the factor-sensitive normalization identities.
A qutrit PPT nonEB signal is embedded in a four-dimensional absorbing flag.
The normalized rare sector remains the signal map although raw maps tend EB.
This is a boundary mechanism check, not a proof of the general theorem.
"""
from pathlib import Path
import json
import sympy as s
r=s.Rational
d=4

def unit(n,a,b):
    M=s.zeros(n);M[a,b]=1;return M

# Horodecki rho at parameter t=1/2, as in the preserved exactness barrier.
v=s.zeros(9,1)
for a in range(3):v[3*a+a]=1
P=v*v.T/3
sp=sum((unit(9,3*a+(a+1)%3,3*a+(a+1)%3) for a in range(3)),s.zeros(9))/3
sm=sum((unit(9,3*a+(a-1)%3,3*a+(a-1)%3) for a in range(3)),s.zeros(9))/3
rho=(2*P+r(7,2)*sp+r(3,2)*sm)/7
J=3*rho # input-first convention; both marginals are identity.
def psi(X):
    Y=s.zeros(3)
    for a in range(3):
        for b in range(3):Y+=X[a,b]*J[3*a:3*a+3,3*b:3*b+3]
    return Y
assert psi(s.eye(3))==s.eye(3)
for a in range(3):
    for b in range(3):assert s.trace(psi(unit(3,a,b)))==int(a==b)

def raw(X,e):
    Y=s.zeros(4);Y[:3,:3]=e*psi(X[:3,:3]);Y[3,3]=X[3,3]+(1-e)*s.trace(X[:3,:3]);return Y

def state(e,i):return s.diag(e**i,e**i,e**i,4-3*e**i)
def normmap(X,e,i):
    Y=s.zeros(4);Y[:3,:3]=psi(X[:3,:3])
    Y[3,3]=((1-e)*e**(i-1)*s.trace(X[:3,:3])+(4-3*e**(i-1))*X[3,3])/(4-3*e**i)
    return Y

def filt(X,S):
    roots=[s.sqrt(S[i,i]) for i in range(4)]
    return s.Matrix(4,4,lambda a,b:s.simplify(roots[a]*X[a,b]*roots[b]))

cases=identities=0
for e in [r(1,2),r(1,100),r(1,10000)]:
    for i in range(1,5):
        prev,now=state(e,i-1),state(e,i)
        assert raw(prev,e)==now
        assert normmap(s.eye(4),e,i)==s.eye(4)
        for a in range(4):
            for b in range(4):
                X=unit(4,a,b);B=normmap(X,e,i)
                assert filt(B,now)==raw(filt(X,prev),e)
                assert s.trace(now*B)==s.trace(prev*X)
                identities+=2
        cases+=1
# For every later normalized factor the limiting kernel block is exactly psi.
e=s.symbols('e',positive=True)
P4=s.diag(1,1,1,0)
for i in [2,3,4]:
    lim=normmap(P4,e,i).applyfunc(lambda x:s.limit(x,e,0))
    assert lim==P4
# A one-factor normalized limit can remain nonEB: its P corner is psi.
s0=sum((unit(9,3*a+a,3*a+a) for a in range(3)),s.zeros(9))/3
W=3*s0+3*sm-sum((unit(9,3*a+a,3*b+b) for a in range(3) for b in range(3) if a!=b),s.zeros(9))
assert s.trace(W*rho)==-r(1,14)
result={'status':'PASS','arithmetic':'Exact SymPy rational and symbolic limits','dimension':4,'trajectory_cases':cases,'matrix_unit_intertwining_and_dual_identities':identities,'moving_kernel_limits':3,'rare_sector_witness_expectation':'-1/14','scope':'Checks normalization and rare-kernel exposure, not universal EB membership or the universal exact exponent.'}
Path(__file__).with_name('normalized_kernel_boundary_verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
