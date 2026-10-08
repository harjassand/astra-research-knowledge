#!/usr/bin/env python3
"""Finite exact checks of derived identities; not theorem certification."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def chi(s,x): return 1 if (s & x).bit_count()%2 == 0 else -1

def moments(bank,L):
    size=1<<L
    mu=[sum(g[x][w] for x in range(size) for w in (0,1))/F(2*size) for g in bank]
    hs=[[F(g[x][0]-g[x][1],2) for x in range(size)] for g in bank]
    beta=[[sum(h[x]*chi(s,x) for x in range(size))/size for h in hs] for s in range(size)]
    return mu,hs,beta

def sigma2_at_least(mu,row,kappa):
    a=sum(v*v for v in mu)-kappa*kappa
    d=sum(v*v for v in row)-kappa*kappa
    c=sum(u*v for u,v in zip(mu,row))
    return a>=0 and d>=0 and a*d>=c*c

counts={'hankel_entries':0,'parseval_rows':0,'coverage_bounds':0,'prefix_energy':0,'fourier_tree':0,'bhattacharyya':0,'sharp_attainment':0}
fixtures=[]
for L in range(1,6):
    size=1<<L
    selected=list(range(min(4,size)))
    bank=[[[F(1),F(1)] for x in range(size)]]
    bank += [[[F(chi(s,x)),F(-chi(s,x))] for x in range(size)] for s in selected]
    # Arbitrary bounded dyadic evaluator, not a supplied parity test.
    bank += [[[F(((13*x+7*w+5)%17)-8,8) for w in (0,1)] for x in range(size)]]
    mu,hs,beta=moments(bank,L)
    M=len(bank)
    for j,h in enumerate(hs):
        assert sum(beta[s][j]**2 for s in range(size)) == sum(z*z for z in h)/size
        assert mu[j]**2+sum(z*z for z in h)/size <= 1
        counts['parseval_rows']+=1
    for lam in [F(1),F(1,2),F(3,4)]:
        for s in range(size):
            for j,g in enumerate(bank):
                direct=[F(0),F(0)]
                for u,x,w in product((0,1),range(size),(0,1)):
                    p=F(1,4*size)*(1+lam*chi(s,x)*(1 if (u+w)%2==0 else -1))
                    direct[0]+=p*g[x][w]
                    direct[1]+=p*(1 if u==0 else -1)*g[x][w]
                assert direct==[mu[j],lam*beta[s][j]]
                counts['hankel_entries']+=2
        for kappa in [lam,lam/2,lam/4]:
            covered=[s for s in range(size) if sigma2_at_least(mu,[lam*b for b in beta[s]],kappa)]
            bound=lam*lam*(M-sum(m*m for m in mu))/(kappa*kappa)
            assert len(covered)<=bound
            if covered:
                sharp_general=lam*lam*(M-kappa*kappa)/(kappa*kappa)
                assert len(covered)<=sharp_general
            counts['coverage_bounds']+=1
            fixtures.append({'L':L,'lambda':str(lam),'kappa':str(kappa),'covered':len(covered),'bound':str(bound)})
    # Exact prefix energy identity for an arbitrary bounded real function.
    h=hs[-1]
    coeff=[sum(h[x]*chi(s,x) for x in range(size))/size for s in range(size)]
    for k in range(L+1):
        for a in range(1<<k):
            mass=sum(coeff[s]**2 for s in range(size) if s & ((1<<k)-1)==a)
            total=F(0)
            for u,up,v in product(range(1<<k),range(1<<k),range(1<<(L-k))):
                total += h[u | (v<<k)]*h[up | (v<<k)]*chi(a,u ^ up)
            total/=F(1<<(L+k))
            assert total==mass
            counts['prefix_energy']+=1
    gamma=F(1,8)
    surviving=[0]
    for k in range(1,L+1):
        nxt=[]
        for prev in surviving:
            for bit in (0,1):
                a=prev | (bit<<(k-1))
                mass=sum(coeff[s]**2 for s in range(size) if s & ((1<<k)-1)==a)
                if mass>=3*gamma*gamma/4: nxt.append(a)
        surviving=nxt
        assert len(surviving)<=F(2,gamma*gamma)
    assert all(s in surviving for s in range(size) if abs(coeff[s])>=gamma)
    counts['fourier_tree']+=1

# Sharp M-1 coverage at the natural margin is attained, not only bounded.
for L in range(1,6):
    size=1<<L
    for count in range(1,min(4,size)+1):
        selected=list(range(count))
        bank=[[[F(1),F(1)] for x in range(size)]]
        bank += [[[F(chi(s,x)),F(-chi(s,x))] for x in range(size)] for s in selected]
        mu,hs,beta=moments(bank,L)
        for lam in [F(1),F(1,2),F(3,4)]:
            covered=[s for s in range(size) if sigma2_at_least(mu,[lam*b for b in beta[s]],lam)]
            assert covered==selected
            assert len(covered)==len(bank)-1
            counts['sharp_attainment']+=1

# Squared Gaussian-mixture-free affinity identity, exact at rational square roots.
for L in range(1,6):
    size=1<<L
    # lambda=3/5 gives sqrt(1-lambda^2)=4/5.
    lam=F(3,5); rho=F(9,10)
    for s,t in product(range(size),repeat=2):
        if s==t: continue
        # x half-agreement, half-disagreement => affinity rho.
        same=sum(chi(s,x)==chi(t,x) for x in range(size))
        affinity=F(same,size)+F(size-same,size)*F(4,5)
        assert affinity==rho
        counts['bhattacharyya']+=1

out={'status':'PASS','scope':'Finite exact algebra fixtures, not universal proof or external review','counts':counts,'coverage_fixtures':fixtures}
Path(__file__).with_name('check_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'counts':counts}))
