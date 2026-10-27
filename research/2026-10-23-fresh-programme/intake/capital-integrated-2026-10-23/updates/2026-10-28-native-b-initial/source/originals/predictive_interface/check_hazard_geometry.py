#!/usr/bin/env python3
"""Exact-law diagnostics for OBSERVABLE_HAZARD_GEOMETRY.txt.
No Astra originals are imported or changed. All acquisition data are synthetic.
The proof certifies full TV; finite tests here check formulas/implementation.
"""
from __future__ import annotations
import math
from pathlib import Path
import numpy as np
from scipy.stats import beta, binom

OUT = Path(__file__).resolve().parent
RNG = np.random.default_rng(20261027)

def survival(p: float, k: int) -> float:
    if k == 0: return 1.0
    if p == 1: return 0.0
    return math.exp(k * math.log1p(-p))

def gap(p: float, q: float, k: int) -> float:
    p, q = sorted((p, q))
    if k == 0 or p == q: return 0.0
    if q == 1: return survival(p, k)
    lp, lq = math.log1p(-p), math.log1p(-q)
    return math.exp(k*lp) * (-math.expm1(k*(lq-lp)))

def law_distance(p: float, q: float, horizon: int | None = None):
    p, q = sorted((p,q))
    assert 0 <= p <= q <= 1
    if p == q or horizon == 0: return 0.0, 0
    if p == 0:
        return (1.0, None) if horizon is None else (gap(p,q,horizon), horizon)
    if q == 1: return gap(p,q,1), 1
    lp, lq = math.log1p(-p), math.log1p(-q)
    real_optimum = math.log(lq/lp)/(lp-lq)
    candidates = {0,1, max(0,math.floor(real_optimum)), math.ceil(real_optimum)}
    if horizon is not None:
        candidates = {min(horizon,k) for k in candidates} | {horizon}
    return max((gap(p,q,k),k) for k in candidates)

def geometric_censored(p: float, horizon: int):
    if p == 0:
        return np.r_[np.zeros(horizon),1.0]
    if p == 1:
        return np.r_[1.0,np.zeros(horizon)]
    indices=np.arange(horizon)
    return np.r_[p*np.exp(indices*math.log1p(-p)),survival(p,horizon)]

def binomial_interval(x: int, n: int, alpha: float):
    lo=0.0 if x==0 else float(beta.ppf(alpha/2,x,n-x+1))
    hi=1.0 if x==n else float(beta.ppf(1-alpha/2,x+1,n-x))
    return lo,hi

def inverse_block(q: float, h: int):
    if q==1: return 1.0
    return -math.expm1(math.log1p(-q)/h)

def center_interval(lo: float,hi: float,horizon: int | None=None):
    if horizon is None and lo==0<hi:
        return lo,1.0
    left,right=lo,hi
    for _ in range(80):
        mid=(left+right)/2
        dl,_=law_distance(lo,mid,horizon)
        dr,_=law_distance(mid,hi,horizon)
        if dl<dr: left=mid
        else: right=mid
    mid=(left+right)/2
    return mid,max(law_distance(lo,mid,horizon)[0],
                   law_distance(mid,hi,horizon)[0])

def binary_kl(p,q):
    if p==0: return -math.log1p(-q)
    if p==1: return -math.log(q)
    return p*math.log(p/q)+(1-p)*(math.log1p(-p)-math.log1p(-q))

def random_policy_transcript(w: int, table: dict, max_charges: int, depth: int):
    """Same deterministic policy for every hidden W; policies use only history."""
    count=0
    hist=()
    for t in range(depth):
        if count == max_charges:
            return hist+(('R',int(count>=w)),)
        if hist not in table:
            table[hist]=int(RNG.integers(0,3))
        action=table[hist]
        if action==2:
            return hist+(('R',int(count>=w)),('stop',))
        if action==0:
            count+=1
            hist+=(('C',0),)
        else:
            hist+=(('R',int(count>=w)),)
    return hist+(('R',int(count>=w)),)

def policy_tv(p,q,H,depth):
    table={}
    leaves={}
    for w,(a,b) in enumerate(zip(geometric_censored(p,H),
                                 geometric_censored(q,H)),start=1):
        key=random_policy_transcript(w,table,H,depth)
        if key not in leaves: leaves[key]=[0.0,0.0]
        leaves[key][0]+=a
        leaves[key][1]+=b
    return sum(abs(a-b) for a,b in leaves.values())/2

def main():
    lines=[]
    def record(s):
        lines.append(s)
        print(s)
    record("OBSERVABLE HAZARD GEOMETRY: numerical law and acquisition checks")
    record("These are synthetic-data/formula checks, not new physical measurements.")
    record("The full-law result is the analytic proof, not a moment or KS test.")

    max_tv_residual=0.0
    cases=0
    for _ in range(1000):
        p,q=sorted(RNG.uniform(1e-5,.95,2))
        H=int(RNG.integers(1,300))
        closed,k=law_distance(p,q,H)
        finite=float(np.abs(geometric_censored(p,H)-geometric_censored(q,H)).sum()/2)
        brute=max(gap(p,q,j) for j in range(H+1))
        max_tv_residual=max(max_tv_residual,abs(closed-finite),abs(closed-brute))
        assert abs(closed-finite)<3e-14
        assert abs(closed-brute)<3e-14
        cases+=1
    record(f"Complete censored-law checks: {cases}; maximum residual {max_tv_residual:.3g}.")

    violations=0
    max_policy_residual=0.0
    for _ in range(1000):
        p,q=sorted(RNG.uniform(.001,.9,2))
        H=int(RNG.integers(1,10))
        tv=policy_tv(p,q,H,20)
        exact,k=law_distance(p,q,H)
        max_policy_residual=max(max_policy_residual,tv-exact)
        violations+=int(tv>exact+5e-14)
        # The attaining experiment has a Bernoulli law.
        assert abs(gap(p,q,k)-exact)<1e-14
    assert violations==0
    record(f"Random adaptive policy full-transcript checks: 1000; violations {violations}; max excess {max_policy_residual:.3g}.")

    c0=81/256*(-math.expm1(-1))
    minimum_ratio=math.inf
    maximum_kl_ratio=0.0
    for p in np.geomspace(1e-7,.25,30):
        for eta in np.geomspace(1e-3,1,30):
            q=(1+eta)*p
            H=math.floor(1/p)
            observed_gap=gap(p,q,H)
            minimum_ratio=min(minimum_ratio,observed_gap/eta)
            assert observed_gap>=c0*eta-1e-13
            kl=binary_kl(p,q)
            maximum_kl_ratio=max(maximum_kl_ratio,kl/(p*eta*eta))
            assert kl<=2*p*eta*eta+1e-14
    record(f"Lower-bound constants: c0={c0:.12f}; min checked d_H/eta={minimum_ratio:.12f}; max checked KL/(p eta^2)={maximum_kl_ratio:.12f}.")

    alpha=.01
    coverage_min=1.0
    for n in (10,30,100):
        intervals=[binomial_interval(x,n,alpha) for x in range(n+1)]
        for p in np.linspace(.001,.999,61):
            total=sum(float(binom.pmf(x,n,p)) for x,(l,u) in enumerate(intervals)
                      if l-2e-15<=p<=u+2e-15)
            coverage_min=min(coverage_min,total)
            assert total>=1-alpha-1e-12
    record(f"Exact finite-sum coverage check over 183 (N,p) pairs: minimum coverage={coverage_min:.12f} (target .99).")

    record("")
    record("Matched charge-budget examples (p=.01, 200000 charge calls, alpha=.01):")
    rows=["h,N,x,q_lower,q_upper,p_lower,p_upper,p_center,whole_law_radius,confidence_diameter,k_star,charges,reads,resets"]
    for h,n in ((1,200000),(100,2000)):
        true_p=.01
        true_q=-math.expm1(h*math.log1p(-true_p))
        x=int(RNG.binomial(n,true_q))  # generation only; learner sees x,n,h,alpha.
        qlo,qhi=binomial_interval(x,n,alpha)
        lo,hi=inverse_block(qlo,h),inverse_block(qhi,h)
        center,radius=center_interval(lo,hi)
        diameter,k=law_distance(lo,hi)
        assert lo<=true_p<=hi  # diagnostic on this recorded seed, not the proof.
        # Tail residuals of floating interval calculations.
        r1=abs(float(binom.sf(x-1,n,qlo))-alpha/2) if x>0 else 0
        r2=abs(float(binom.cdf(x,n,qhi))-alpha/2) if x<n else 0
        assert max(r1,r2)<2e-9
        record(f"h={h}, N={n}, successes={x}; p interval=[{lo:.10f},{hi:.10f}], center={center:.10f}, full unbounded-reuse TV radius={radius:.8f}, diameter={diameter:.8f}, optimal discriminator charges={k}; interval-tail residual={max(r1,r2):.3g}.")
        rows.append(",".join(map(str,(h,n,x,qlo,qhi,lo,hi,center,radius,diameter,k,h*n,n,n))))
    (OUT/"SYNTHETIC_COUNTS.csv").write_text("\n".join(rows)+"\n")

    # Zero counts cannot identify an unbounded lifetime law.
    _,u=binomial_interval(0,1000,.01)
    infinite,_=law_distance(0,u)
    finite,_=law_distance(0,u,10)
    assert infinite==1
    record(f"Zero-success example (N=1000): upper p={u:.10f}; unbounded diameter=1, ten-charge diameter={finite:.10f}.")

    record("")
    record("PASS. All checks completed. No raw counts of the original rank-four fixture were used.")
    (OUT/"CHECK_RESULTS.txt").write_text("\n".join(lines)+"\n")

if __name__=="__main__":
    main()

