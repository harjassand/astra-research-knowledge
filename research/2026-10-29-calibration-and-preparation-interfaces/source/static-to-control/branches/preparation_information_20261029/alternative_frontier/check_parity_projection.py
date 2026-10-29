"""Independent rational/prime-log checks for root parity projection.

General proof is reviewed in PARITY_PROJECTION_INDEPENDENT_REVIEW.md.
No Monte Carlo. No symbolic-algebra package required.
"""
import json, math
from pathlib import Path
from collections import defaultdict
from fractions import Fraction as F

BASE=Path(__file__).resolve().parent
n=4
theta=[1,0,3,2]
rho=list(map(F,[1,2,3,4]));rho=[x/10 for x in rho]
f=[list(map(F,row)) for row in [[0,1,2,3],[1,0,4,5],[2,4,0,6],[3,5,6,0]]]
for i,j in [(0,1),(1,2),(2,0)]:f[i][j]+=1
q=[rho[theta[i]] for i in range(n)]
mu=[(rho[i]+q[i])/2 for i in range(n)]
g=[[f[theta[j]][theta[i]] for j in range(n)] for i in range(n)]
fluxbar=[[(f[i][j]+g[i][j])/2 for j in range(n)] for i in range(n)]
G=[list(map(F,row)) for row in [[0,1,2,3],[1,0,3,2],[2,3,0,5],[3,2,5,0]]]
nu=[F(1,6),F(1,6),F(1,3),F(1,3)]
def gen(flux,p):
    M=[[flux[i][j]/p[i] for j in range(n)] for i in range(n)]
    for i in range(n):M[i][i]=-sum(M[i][j] for j in range(n) if i!=j)
    return M
L=gen(f,rho);R=gen(g,q);B=gen(fluxbar,mu);H=gen(G,nu)
def stationary(M,p):
    return all(sum(p[i]*M[i][j] for i in range(n))==0 for j in range(n))
for M,p in [(L,rho),(R,q),(B,mu),(H,nu)]:assert stationary(M,p)
assert all(B[i][j]*mu[i]==B[theta[j]][theta[i]]*mu[theta[j]] for i in range(n) for j in range(n) if i!=j)
assert all(B[i][i]==B[theta[i]][theta[i]] for i in range(n))
def primes(num):
    o={};d=2
    while d*d<=num:
        while num%d==0:o[d]=o.get(d,0)+1;num//=d
        d+=1
    if num>1:o[num]=o.get(num,0)+1
    return o
def form():return defaultdict(F)
def addlog(o,c,x):
    for p,e in primes(x.numerator).items():o[p]+=c*e
    for p,e in primes(x.denominator).items():o[p]-=c*e
def plus(*terms):
    o=form()
    for factor,v in terms:
        for k,c in v.items():o[k]+=factor*c
    return {k:c for k,c in o.items() if c}
def divlaw(p,z):
    o=form()
    for a,b in zip(p,z):addlog(o,a,a/b)
    return o
def rate(M,p,N):
    o=form()
    for i in range(n):
      for j in range(n):
        if i==j:continue
        addlog(o,p[i]*M[i][j],M[i][j]/N[i][j])
        o[0]+=p[i]*(N[i][j]-M[i][j])
    return o
checks={
 'initial_pythagoras':plus((1,divlaw(rho,nu)),(-1,divlaw(rho,mu)),(-1,divlaw(mu,nu))),
 'rate_pythagoras':plus((1,rate(L,rho,H)),(-1,rate(L,rho,B)),(-1,rate(B,mu,H))),
 'reversal_rate_symmetry':plus((1,rate(L,rho,R)),(-1,rate(R,q,L))),
 'projection_rate_symmetry':plus((1,rate(L,rho,B)),(-1,rate(R,q,B))),
}
assert all(v=={} for v in checks.values())
# The scalar inequality is checked as an ordinary proof in the review;
# the executable is confined to the nontrivial finite-state identities.
def val(o):return math.fsum(float(v)*(1 if k==0 else math.log(k)) for k,v in o.items())
sigma=val(rate(L,rho,R));I=val(rate(L,rho,B))
assert 4*I<sigma
out={
 'status':'all rational/prime-log identities passed',
 'rho':list(map(str,rho)),'q':list(map(str,q)),'mu':list(map(str,mu)),
 'sigma_approximate':sigma,'projection_rate_I_approximate':I,
 'I_over_sigma_approximate':I/sigma,
 'prime_log_residuals':checks,
 'scalar_derivative':'ordinary algebra checked in review; no executable symbolic-derivative claim',
 'scope':'one exact finite example; general proof reviewed separately; displayed floats are not interval certificates'
}
(BASE/'PARITY_PROJECTION_EXACT_CHECKS.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))

