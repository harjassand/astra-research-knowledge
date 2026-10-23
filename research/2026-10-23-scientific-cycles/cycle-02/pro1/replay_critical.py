#!/usr/bin/env python3
"""Exact finite checks for the new critical-depth construction.

The bath consists of actual infinite-tree coordinates (side, finite word).
All states have finite support because a fixed finite number of interactions is
expanded. No artificial boundary, reflecting truncation or bath reset is used.
These checks test representations and a concrete continuation input. They do
not replace the all-horizon compression and coding proofs.

Run from this directory: python replay_critical.py --output replay/critical.json
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as F
from itertools import product
import json
from math import comb, isqrt
from pathlib import Path
import platform
import resource
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent / 'representation'))
from exact_representation import G, I_G


def add(out, key, value):
    out[key] = out.get(key, G()) + value


def clean(out):
    return {k: v for k, v in out.items() if v}


def edge(x, vertex):
    side, w = vertex
    if x:
        return 0, (side, (x,) + w)
    if w:
        return w[0], (side, w[1:])
    return 0, (1-side, ())


def entry(y, x, vertex, alpha, beta):
    out = {}
    if y == x and beta:
        add(out, vertex, I_G * beta)
    ym, vm = edge(x, vertex)
    if ym == y and alpha:
        add(out, vm, G(alpha))
    return clean(out)


def step(tau, rho, alpha, beta):
    """Trace the physical output after a fully coherent V interaction."""
    out = {}
    action_cache = {}
    for (v, w), tvw in tau.items():
        for (x, xp), rxx in rho.items():
            for y in range(3):
                key1, key2 = (y,x,v), (y,xp,w)
                if key1 not in action_cache:
                    action_cache[key1] = entry(y,x,v,alpha,beta)
                if key2 not in action_cache:
                    action_cache[key2] = entry(y,xp,w,alpha,beta)
                for ov, a in action_cache[key1].items():
                    for ow, b in action_cache[key2].items():
                        add(out, (ov,ow), tvw * rxx * a * b.conjugate())
    return clean(out)


def pure_density(psi):
    return {(v,w): a*b.conjugate() for v,a in psi.items()
            for w,b in psi.items()}


def depth(tau):
    out = defaultdict(F)
    trace = G()
    for (v,w), x in tau.items():
        if v == w:
            assert x.im == 0 and x.re >= 0
            out[len(v[1])] += x.re
            trace += x
    assert trace == G(F(1))
    return dict(out)


def classical_step(dist, q, alpha, beta):
    out = defaultdict(F)
    for h, p in dist.items():
        out[h+1] += p*alpha*alpha*(1-q)
        out[max(0,h-1)] += p*alpha*alpha*q
        out[h] += p*beta*beta
    return {k:v for k,v in out.items() if v}


def diagonal(q):
    return {(0,0):G(q),(1,1):G((1-q)/2),(2,2):G((1-q)/2)}


def sqrt_interval(x, bits=140):
    scale = 1 << bits
    k = isqrt((x.numerator << (2*bits)) // x.denominator)
    lo, hi = F(k,scale), F(k+1,scale)
    assert lo*lo <= x <= hi*hi
    return lo, hi


def ln_interval(x, terms=90):
    assert x > 0
    t = (x-1)/(x+1)
    t2, power = t*t, t
    s = F(0)
    for k in range(terms):
        s += power/F(2*k+1)
        power *= t2
    rem = 2*abs(t)**(2*terms+1)/F(2*terms+1)/(1-t2)
    return 2*s-rem, 2*s+rem


def outward_decimal(x, rounding):
    with localcontext() as ctx:
        ctx.prec = 42
        ctx.rounding = rounding
        return str(Decimal(x.numerator)/Decimal(x.denominator))


def entropy_seed_certificate():
    beta = F(1,512)
    q = F(1,2)-3*beta*beta/32
    g = beta/8
    a = (1-q)/2
    assert q > 0 and a > 0 and q*a-g*g > 0
    sl, su = sqrt_interval((q-a)**2+4*g*g)
    intervals = [(a,a),((q+a+sl)/2,(q+a+su)/2),
                 ((q+a-su)/2,(q+a-sl)/2)]
    ll2, lu2 = ln_interval(F(2))
    lower, upper = F(0), F(0)
    for lo, hi in intervals:
        assert 0 < lo <= hi < 1
        lnlo, _ = ln_interval(lo)
        _, lnhi = ln_interval(hi)
        lower += -lo*lnhi/lu2
        upper += -hi*lnlo/ll2
    assert lower > F(3,2)
    assert upper-lower < F(1,10**30)
    return {
        'beta':str(beta), 'rho00':str(q), 'rho01_over_i':str(g),
        'rho11_rho22':str(a), 'positive_principal_minor':str(q*a-g*g),
        'entropy_bits_lower':outward_decimal(lower,ROUND_FLOOR),
        'entropy_bits_upper':outward_decimal(upper,ROUND_CEILING),
        'gain_lower':outward_decimal(lower-F(3,2),ROUND_FLOOR),
        'sqrt_binary_bits':140,'log_atanh_terms':90,
        'certificate':'All interval endpoints and assertions use exact rational arithmetic.',
        'scope':'Port entropy only. No stationary bath, tight-tail estimate, or capacity gain is established.'}


def run():
    wall, cpu = time.perf_counter(), time.process_time()
    psi = {(0,()):G(F(3,5)),(1,(1,)):G(F(0),F(4,5))}
    tau0 = pure_density(psi)
    cases = []
    params = [(F(3,5),F(4,5)),
              (F(1048575,1048577),F(2048,1048577)),
              (F(1),F(0)),(F(0),F(1))]
    for alpha,beta in params:
        assert alpha*alpha+beta*beta == 1
        for q in [F(1,2),F(2,5)]:
            tau, dist = tau0, depth(tau0)
            max_entries = len(tau)
            for n in range(1,5):
                tau = step(tau,diagonal(q),alpha,beta)
                dist = classical_step(dist,q,alpha,beta)
                assert depth(tau) == dist, (alpha,beta,q,n)
                max_entries = max(max_entries,len(tau))
            cases.append({'alpha':str(alpha),'beta':str(beta),'q':str(q),
                          'horizons':[1,2,3,4],
                          'max_density_entries':max_entries,'exact_depth_identity':True})

    # Verify type domination through an independently expanded coherent process.
    alpha,beta = F(3,5),F(4,5)
    n = 4
    words = [w for w in product(range(3),repeat=n) if w.count(0)==n//2]
    D = comb(n,n//2)*2**(n//2)
    assert len(words)==D
    tau_type = {}
    for word in words:
        t = tau0
        for x in word:
            t = step(t,{(x,x):G(F(1))},alpha,beta)
        for key,val in t.items():
            add(tau_type,key,val*F(1,D))
    type_dist = depth(clean(tau_type))
    t = tau0
    for _ in range(n):
        t = step(t,diagonal(F(1,2)),alpha,beta)
    product_dist = depth(t)
    p_n = F(comb(n,n//2),2**n)
    type_checks=[]
    for h in range(7):
        tt=sum(v for k,v in type_dist.items() if k>h)
        tp=sum(v for k,v in product_dist.items() if k>h)
        assert tt <= tp/p_n
        type_checks.append({'cutoff':h,'type_overflow':str(tt),
                            'product_overflow_div_type_probability':str(tp/p_n)})

    # Input-coherent drift, evaluated by explicit density evolution.
    q,g=F(2,5),F(1,10)
    rho=diagonal(q)
    rho[(0,1)],rho[(1,0)]=I_G*g,-I_G*g
    psi2={(0,()):G(F(3,5)),(0,(1,)):G(F(4,5))}
    t0=pure_density(psi2)
    t1=step(t0,rho,alpha,beta)
    d0,d1=depth(t0),depth(t1)
    observed=sum(k*v for k,v in d1.items())-sum(k*v for k,v in d0.items())
    p=F(9,25)
    z1=F(12,25)
    predicted=alpha*alpha*(1-2*q+q*p)-2*alpha*beta*g*z1
    assert observed==predicted

    certificate=entropy_seed_certificate()
    return {'status':'PASS','claims_not_established_by_replay':[
        'No numerical experiment certifies the asymptotic capacity floor.',
        'No capacity gain, normal coherent stationary bath, or plateau is proved.'],
        'exact_depth_cases':cases,'type_dimension':D,'type_probability':str(p_n),
        'type_checks':type_checks,
        'coherent_drift':{'observed':str(observed),'predicted':str(predicted)},
        'next_input_entropy_certificate':certificate,
        'resources':{'wall_seconds':time.perf_counter()-wall,
                     'cpu_seconds':time.process_time()-cpu,
                     'max_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                     'python':platform.python_version(),
                     'platform':platform.platform()},
        'resources_scope':'Process-body replay costs, not discovery or model-inference costs.'}


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--output',type=Path,default=Path('replay/critical.json'))
    args=p.parse_args()
    result=run()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'resources':result['resources'],
                      'entropy_seed':result['next_input_entropy_certificate']},indent=2))
