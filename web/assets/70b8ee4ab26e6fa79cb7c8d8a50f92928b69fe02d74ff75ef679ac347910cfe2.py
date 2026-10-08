#!/usr/bin/env python3
"""Finite chi-square recurrence audit for the fixed pair.

Computes chi2(P1||P0)=sum P0*(P1/P0-1)^2 on a finite prefix in log
arithmetic. This is diagnostic only; analytic large-m bounds are described
in FINAL_REPORT.md and omitted mass is not interval-certified.
"""
from __future__ import annotations
import json, math
from pathlib import Path

RATES=((1,1,4,0),(0,4,1,1))

def logsumexp(xs):
    a=max(xs)
    if not math.isfinite(a): return a
    return a+math.log(math.fsum(math.exp(x-a) for x in xs))

def logq(mu, rates, nmax):
    q=[-math.inf]*(nmax+1); q[0]=0.0
    for m in range(1,nmax+1):
        ts=[math.log(j*rates[j-1])+q[m-j]
            for j in range(1,min(4,m)+1)
            if rates[j-1] and q[m-j]>-math.inf]
        if ts: q[m]=math.log(mu/m)+logsumexp(ts)
    return q

def log_abs_expm1(x):
    if x==0: return -math.inf
    if x>40: return x+math.log1p(-math.exp(-x))
    if x<-40: return math.log1p(-math.exp(x))
    return math.log(abs(math.expm1(x)))

def calc(mu):
    nmax=math.ceil(15*mu+22*math.sqrt(41*mu)+100)
    a,b=(logq(mu,r,nmax) for r in RATES)
    logs=[]
    for m in range(nmax+1):
        if a[m]==-math.inf: continue
        d=b[m]-a[m]
        if d==-math.inf: # m=1 support hole
            logdiff=0.0
        else:
            logdiff=log_abs_expm1(d)
        logs.append(-6*mu+a[m]+2*logdiff)
    lchi=logsumexp(logs)
    chi=math.exp(lchi) if lchi<709 else math.inf
    return {'mu':mu,'cutoff':nmax,'chi2_truncated':chi,
            'mu_chi2_truncated':mu*chi,
            'target':6/(41**3),
            'support_hole_term':mu*math.exp(-6*mu)}

def main():
    data={'method':'log-domain Panjer coefficient recurrence; truncated at mean + 22 SD + 100',
          'target_mu_chi2':6/(41**3),
          'rows':[calc(mu) for mu in (8,16,32,56,100,250,1000)],
          'scope':'finite floating-point diagnostic, not interval-certified and not by itself a global tail proof'}
    p=Path(__file__).with_name('chi_square_tail_results.json')
    p.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))
if __name__=='__main__': main()
