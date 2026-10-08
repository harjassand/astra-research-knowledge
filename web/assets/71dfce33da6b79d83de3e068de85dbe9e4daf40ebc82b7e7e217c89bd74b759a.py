"""Finite diagnostics, not proof validation. Uses bundled Python/numpy/scipy."""
from pathlib import Path
import json
import numpy as np
from itertools import product

OUT = Path(__file__).resolve().parents[1] / "results"
OUT.mkdir(exist_ok=True)

def F(x):
    return 2*x*np.arctanh(x)

def Fprime(x):
    return 2*np.arctanh(x)+2*x/(1-x*x)

def inv_Fprime(h):
    lo, hi = 0., np.nextafter(1., 0.)
    for _ in range(80):
        mid = (lo+hi)/2
        if Fprime(mid)<h:
            lo=mid
        else:
            hi=mid
    return (lo+hi)/2

def ep(Q, pi):
    n = len(pi)
    return sum(pi[i]*Q[i,j]*np.log(pi[i]*Q[i,j]/(pi[j]*Q[j,i]))
               for i in range(n) for j in range(n)
               if i != j and Q[i,j] > 0)

def ring(u, v):
    Q=np.zeros((4,4))
    for i in range(4):
        Q[i,(i+1)%4]=u
        Q[i,(i-1)%4]=v
        Q[i,i]=-u-v
    return Q

def wordlaw(Q, pi, T=.5):
    labels = [0,1,2,2]
    words=list(product(range(3), repeat=3))
    lookup={w:i for i,w in enumerate(words)}
    rev=np.array([lookup[w[::-1]] for w in words])
    probs=np.zeros(len(words))
    eigvals,eigvecs=np.linalg.eig(Q)
    P=np.real_if_close(eigvecs@np.diag(np.exp(eigvals*T/2))@np.linalg.inv(eigvecs)).real
    assert np.min(P)>=-1e-14 and np.max(np.abs(P.sum(axis=1)-1))<1e-12
    for x,y,z in product(range(4),repeat=3):
        probs[lookup[(labels[x],labels[y],labels[z])]] += pi[x]*P[x,y]*P[y,z]
    assert np.isclose(probs.sum(),1)
    D=np.sum(probs*np.log(probs/probs[rev]))
    return probs, rev, D

def adaptive_trials(probs, rev, D, T, seed, trials=1000, nmax=10000, H=4., alpha=.05):
    rng=np.random.default_rng(seed)
    counts=np.zeros((trials,len(probs)),dtype=np.int64)
    totals=np.zeros(trials)
    clipped=inv_Fprime(H)
    failed=np.zeros(trials,dtype=bool)
    plugin_failed=np.zeros(trials,dtype=bool)
    checkpoints={}
    rows=np.arange(trials)
    cdf=np.cumsum(probs)
    for n in range(1,nmax+1):
        w=np.searchsorted(cdf,rng.random(trials))
        reverse=rev[w]
        # The critic uses counts from observations 1,...,n-1 only.
        cp,cm=counts[rows,w],counts[rows,reverse]
        x=np.clip((cp-cm)/(cp+cm+2.),-clipped,clipped)
        h=Fprime(x)
        fstar=h*x-F(x)
        totals += h-fstar
        counts[rows,w]+=1
        boundary=H*np.sqrt(2*n*np.log(n*(n+1)/alpha))
        lower=np.maximum(0.,(totals-boundary)/(n*T))
        failed |= lower > D/T + 1e-12
        if n in [100,1000,10000]:
            # Jeffreys/KL plug-in with unit pseudocount avoids infinities.
            empirical=(counts+1)/(n+len(probs))
            plugin=np.sum(empirical*np.log(empirical/empirical[:,rev]),axis=1)/T
            plugin_failed |= plugin > D/T + 1e-12
            checkpoints[str(n)]={
                "mean_lower":float(lower.mean()),
                "positive_fraction":float(np.mean(lower>0)),
                "mean_smoothed_plugin":float(plugin.mean()),
                "plugin_exceedance_fraction":float(np.mean(plugin>D/T+1e-12)),
            }
    return {"trials":trials,"nmax":nmax,"H":H,"alpha":alpha,
            "word_KL_rate":float(D/T),"confidence_anytime_exceedance_fraction":float(failed.mean()),
            "plugin_ever_exceedance_at_checkpoints":float(plugin_failed.mean()),"checkpoints":checkpoints}

def betting_trials(probs, rev, D, T, seed, trials=200, nmax=10000, H=1., alpha=.05):
    rng=np.random.default_rng(seed)
    counts=np.zeros((trials,len(probs)),dtype=np.int64)
    clipped=inv_Fprime(H)
    fstarH=H*clipped-F(clipped)
    lower_score=-H-fstarH
    grid=np.arange(0.,.51,.05)
    # The extra population-KL point is used for diagnostic coverage only.
    hypotheses=np.r_[grid,D/T]
    eta=np.array([.02,.1,.3,.5])
    denominator=T*hypotheses-lower_score
    logproducts=np.zeros((trials,len(hypotheses),len(eta)))
    failed=np.zeros(trials,dtype=bool)
    grid_failed=np.zeros(trials,dtype=bool)
    checkpoints={}
    rows=np.arange(trials)
    cdf=np.cumsum(probs)
    for n in range(1,nmax+1):
        w=np.searchsorted(cdf,rng.random(trials))
        cp,cm=counts[rows,w],counts[rows,rev[w]]
        x=np.clip((cp-cm)/(cp+cm+2.),-clipped,clipped)
        h=Fprime(x)
        score=h-(h*x-F(x))
        numerator=score-lower_score
        factors=1-eta[None,None,:]+eta[None,None,:]*numerator[:,None,None]/denominator[None,:,None]
        assert factors.min()>0
        logproducts+=np.log(factors)
        counts[rows,w]+=1
        mx=logproducts.max(axis=2)
        logwealth=mx+np.log(np.exp(logproducts-mx[:,:,None]).mean(axis=2))
        accepted=logwealth[:,:len(grid)]>=np.log(1/alpha)
        lower=np.max(np.where(accepted,grid[None,:],0),axis=1)
        failed |= logwealth[:,-1]>=np.log(1/alpha)
        grid_failed |= lower>D/T+1e-12
        if n in [100,1000,10000]:
            checkpoints[str(n)]={"mean_grid_lower":float(lower.mean()),
                "positive_fraction":float(np.mean(lower>0)),
                "fraction_rejecting_zero":float(np.mean(accepted[:,0]))}
    return {"trials":trials,"nmax":nmax,"H":H,"alpha":alpha,
            "eta_mixture":eta.tolist(),"grid":grid.tolist(),
            "word_KL_rate":float(D/T),"score_lower":float(lower_score),
            "anytime_wealth_crossing_at_true_word_KL":float(failed.mean()),
            "anytime_grid_lower_exceedance_fraction":float(grid_failed.mean()),
            "checkpoints":checkpoints}

pi=np.ones(4)/4
Q=ring(3.,1.)
sigma=ep(Q,pi)
w,q=.4,1e-7
Qext=np.zeros((5,5));Qext[:4,:4]=Q
Qext[0,4]=q;Qext[0,0]-=q
Qext[4,0]=w*pi[0]*q/(1-w);Qext[4,4]=-Qext[4,0]
piext=np.r_[w*pi,1-w]
bridge={"stationarity_residual":float(np.max(np.abs(piext@Qext))),
        "base_sigma":float(sigma),"bridge_sigma":float(ep(Qext,piext)),
        "expected_bridge_sigma":float(w*sigma),"w":w,"q":q,
        "survival_probability_floor_at_T_1000000":float(w*np.exp(-q*1e6))}

# Check the Fenchel identity and bounded score on random finite involution laws.
rng=np.random.default_rng(42)
max_gap_error=0.
minimum_fenchel_gap=float("inf")
for _ in range(1000):
    p=rng.dirichlet(np.ones(10))
    rev=np.arange(9,-1,-1)
    s=(p+p[rev])/2
    x=(p-p[rev])/(p+p[rev])
    D=np.sum(p*np.log(p/p[rev]))
    max_gap_error=max(max_gap_error,abs(D-np.dot(s,F(x))))
    z=rng.uniform(-.95,.95,5);z=np.r_[z,-z[::-1]]
    h=Fprime(z);fstar=h*z-F(z)
    minimum_fenchel_gap=min(minimum_fenchel_gap,D-np.dot(p,h-fstar))

results={"bridge":bridge,"fenchel":{"maximum_identity_error":max_gap_error,
          "minimum_random_fenchel_gap":minimum_fenchel_gap},"experiments":{}}
for u,v,name,seed in [(3.,1.,"driven",7),(1.,1.,"equilibrium",8)]:
    probs,rev,D=wordlaw(ring(u,v),pi)
    r=adaptive_trials(probs,rev,D,.5,seed)
    r["true_CTMC_sigma"]=ep(ring(u,v),pi)
    results["experiments"][name]=r
    results["experiments"][name+"_betting"]=betting_trials(probs,rev,D,.5,seed+20)
(OUT/"checks.json").write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
