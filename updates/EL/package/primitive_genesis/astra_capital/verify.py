#!/usr/bin/env python3
"""Independent finite diagnostics. Exact algebra != a universal proof or an assay.

Writes only next to this script. Uses the installed mpmath for explicitly marked
high-precision, non-interval-certified numerical diagnostics.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import math
import random
import subprocess
import sys

import mpmath as mp

OUT = Path(__file__).resolve().parent
ASTRA = Path('/Users/harjas/Documents/ChatGPT/quant/research_wave_2026-10-12/astra')
PIN = '5fc72a144d77c31b400efc0768afd7833c702362'
COUNTS = {'exact_assertions': 0, 'numerical_assertions': 0}


def check(value, exact=True):
    assert value
    COUNTS['exact_assertions' if exact else 'numerical_assertions'] += 1


def zero(n, m=None):
    return [[F(0) for _ in range(n if m is None else m)] for _ in range(n)]


def mm(a, b):
    return [[sum((a[i][h] * b[h][j] for h in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def mv(a, v):
    return [sum((aij * vj for aij, vj in zip(row, v)), F(0)) for row in a]


def dot(u, v):
    return sum((x * y for x, y in zip(u, v)), F(0))


def generator(off):
    a = [row[:] for row in off]
    for i in range(len(a)):
        a[i][i] = -sum((a[i][j] for j in range(len(a)) if i != j), F(0))
    return a


def scale_gain(q, g):
    return generator([[q[i][j] * g[i][j] if i != j else F(0)
                       for j in range(len(q))] for i in range(len(q))])


def target_v(q, labels, a):
    e = [F(l == a) for l in labels]
    qe = mv(q, e)
    v = [[(q[i][j] * (e[j] - e[i]) - (qe[i] if i == j else 0)) / 2
          for j in range(len(q))] for i in range(len(q))]
    check(all(sum(row) == 0 for row in v))
    return v


def source_identity_checks():
    rng = random.Random(640182)
    for rep in range(24):
        n, k, s = 5, 3, 2
        labels = [0, 0, 1, 1, 2]
        raw_mass = [rng.randrange(1, 13) for _ in range(s * n * 2)]
        denom = sum(raw_mass)
        joint = [[[F(raw_mass[(j * n + i) * 2 + c], denom)
                   for c in range(2)] for i in range(n)] for j in range(s)]
        omega = [[sum(joint[j][i]) for i in range(n)] for j in range(s)]
        check(sum(map(sum, omega)) == 1)
        actual_g, inferred_g, bpred, cpred, direct = F(0), F(0), F(0), F(0), F(0)
        for j in range(s):
            off = [[F(rng.randrange(1, 9), 8 * (n-1)) if i != l else F(0)
                    for l in range(n)] for i in range(n)]
            q = generator(off)
            check(max(-q[i][i] for i in range(n)) <= 1)
            e = [[F(labels[i] == a) for a in range(k)] for i in range(n)]
            qe = mm(q, e)
            q2e = mm(q, qe)
            for a in range(k):
                ea = [row[a] for row in e]
                qea = [row[a] for row in qe]
                v = target_v(q, labels, a)
                gains = [[[F(2) ** ((1 if u == 0 else -1) * (ea[l] - ea[i]))
                           for l in range(n)] for i in range(n)] for u in range(2)]
                controls = [scale_gain(q, g) for g in gains]
                w = [F(1, 3), -F(1, 3)]
                synth = [[sum(w[u] * controls[u][i][l] for u in range(2))
                          for l in range(n)] for i in range(n)]
                check(synth == v)
                h = [[sum(omega[j][i] * q[i][l] * gains[u][i][l] * gains[z][i][l]
                          for i in range(n) for l in range(n)
                          if i != l and labels[i] != labels[l])
                      for z in range(2)] for u in range(2)]
                ba = [sum(omega[j][i] * q[i][l] * gains[u][i][l] * (ea[l]-ea[i])/2
                          for i in range(n) for l in range(n) if i != l)
                      for u in range(2)]
                ca = sum(omega[j][i] * q[i][l] * ((ea[l]-ea[i])/2)**2
                         for i in range(n) for l in range(n) if i != l)
                err = dot(w, mv(h, w)) - 2 * dot(ba, w) + ca
                check(err == 0)
                # A deliberately imperfect synthesis verifies the squared
                # Cauchy-Schwarz envelope independently from the exact fit.
                wp = [F(1, 4), -F(1, 4)]
                ep = dot(wp, mv(h, wp)) - 2 * dot(ba, wp) + ca
                delta = [[sum(wp[u]*controls[u][i][l] for u in range(2))-v[i][l]
                          for l in range(n)] for i in range(n)]
                rerr = dot(omega[j], mv(delta, qea))
                check(rerr**2 <= 4 * sum(omega[j]) * ep)
                c2 = dot(omega[j], [ea[i]*q2e[i][a] for i in range(n)])
                t = dot(omega[j], mv(q, [ea[i]*qea[i] for i in range(n)]))
                response = dot(omega[j], mv(v, qea))
                gram = dot(omega[j], [x*x for x in qea])
                check(gram == t-c2-2*response)
                actual_g += gram
                inferred_g += t-c2-2*sum(w[u]*dot(omega[j], mv(controls[u], qea))
                                         for u in range(2))
            for i in range(n):
                for c in range(2):
                    # Different observed histories can give different frozen
                    # prediction vectors at the same hidden state.
                    a = labels[i]
                    vv = [F(0)] * k
                    for b in range(k):
                        if b != a:
                            vv[b] = F(rng.randrange(0, 6), 12)
                    vv[a] = -sum(vv)
                    mass = joint[j][i][c]
                    bpred += mass * dot(vv, qe[i])
                    cpred += mass * dot(vv, vv)
                    direct += mass * sum((qe[i][b]-vv[b])**2 for b in range(k))
        check(actual_g == inferred_g)
        check(direct == inferred_g - 2*bpred + cpred)
        check(direct >= 0)


def counterexample_checks():
    delta = F(1, 1000)
    nu = [(1-delta)/2, delta, (1-delta)/2]
    q = [[F(-1), F(1), F(0)], [F(0), F(-1), F(1)], [F(0)]*3]
    labels = [0, 0, 1]
    e = [[F(l == a) for a in range(2)] for l in labels]
    qe = mm(q, e)
    rate = 2*delta/(1+delta)
    l = [[-rate, rate], [F(0), F(0)]]
    d = sum(nu[i]*sum((qe[i][b]-l[labels[i]][b])**2 for b in range(2))
            for i in range(3))
    check(d == 2*delta*(1-delta)/(1+delta))
    check(min(nu[0]+nu[1], nu[2]) > F(49, 100))
    mp.mp.dps = 80
    t = mp.mpf(4)
    dd = mp.mpf(delta.numerator)/delta.denominator
    true_b = 1-mp.exp(-t)*(dd+(1-dd)*(1+t)/2)
    reduced_b = 1-(1+dd)*mp.exp(-2*dd*t/(1+dd))/2
    check(true_b-reduced_b > mp.mpf('0.45'), exact=False)

    # Stationary observed Markov law with a nonzero hidden-rate residual.
    n = 4
    h, f = [1,-1,0,0], [1,1,-1,-1]
    eps = F(1, 16)
    qv = [[F(1,n)-(1 if i == j else 0)+eps*h[i]*f[j]
           for j in range(n)] for i in range(n)]
    check(all(sum(row) == 0 for row in qv))
    check(all(sum(qv[i][j] for i in range(n)) == 0 for j in range(n)))
    check(all(qv[i][j] > 0 for i in range(n) for j in range(n) if i != j))
    labels = [0,0,1,1]
    e = [[F(l == a) for a in range(2)] for l in labels]
    qe = mm(qv, e)
    l = [[F(-1,2), F(1,2)], [F(1,2), F(-1,2)]]
    residual = sum(F(1,4)*sum((qe[i][b]-l[labels[i]][b])**2 for b in range(2))
                   for i in range(n))
    check(residual == F(1,64))
    qt = list(map(list, zip(*qv)))
    check(mm(qt, e) == [l[a] for a in labels])
    return {'delta': str(delta), 'training_residual': str(d),
            'endpoint_probability_gap_T4': mp.nstr(true_b-reduced_b, 35),
            'perfect_observed_predictor_hidden_residual': str(residual)}


def stirling(n, k):
    if n == k == 0:
        return 1
    if n == 0 or k == 0:
        return 0
    return k*stirling(n-1,k)+stirling(n-1,k-1)


def falling(n, d):
    return math.prod(range(n-d+1,n+1)) if d <= n else 0


def collision_checks():
    records = []
    for n in [8,16,32,256]:
        for r in range(1,6):
            tv = F(0)
            for d in range(1,min(r,n)+1):
                tuples = stirling(r,d)*falling(n,d)
                alt = F(falling(n//2,d), falling(n,d))*F(2,n)**r
                null = F(1,n)**r
                tv += tuples*abs(alt-null)/2
            check(tv <= F(3*r*(r-1),2*n))
            records.append({'support':n,'trials':r,'mixture_TV':str(tv)})
    return records


def prefix_model(m, subset):
    prefixes = [tuple(v) for depth in range(m) for v in product([0,1], repeat=depth)]
    tails = [('tail',p,b) for p in range(2) for b in range(2)]
    states = prefixes+tails
    idx = {v:i for i,v in enumerate(states)}
    labels = [(len(v)%2, v[-1] if v else 0) if v in prefixes else (v[1],v[2])
              for v in states]
    labelnum = [2*p+b for p,b in labels]
    q = zero(len(states))
    for prefix in prefixes:
        i = idx[prefix]
        mass = sum(tuple(v[:len(prefix)]) == prefix for v in subset)
        for bit in [0,1]:
            child = prefix+(bit,)
            childmass = sum(tuple(v[:len(child)]) == child for v in subset)
            prob = F(childmass,mass) if mass else F(1,2)
            dest = child if len(child)<m else ('tail',m%2,bit)
            q[i][idx[dest]] += prob
    for tail in tails:
        i = idx[tail]
        for bit in [0,1]:
            q[i][idx[('tail',1-tail[1],bit)]] = F(1,2)
    return generator(q), labelnum


def mpmatrix(a):
    return mp.matrix([[mp.mpf(v.numerator)/v.denominator for v in row] for row in a])


def prefix_checks():
    m = 3
    strings = list(product([0,1], repeat=m))
    subset = [strings[i] for i in [0,2,3,5]]
    q0, labels0 = prefix_model(m, strings)
    q, labels = prefix_model(m, subset)
    l = [[F(1,2) if a//2 != b//2 else F(0) for b in range(4)] for a in range(4)]
    for a in range(4):
        l[a][a] = -1
    e = [[F(a == b) for b in range(4)] for a in labels]
    e0 = [[F(a == b) for b in range(4)] for a in labels0]
    check(mm(q0,e0) == [l[a] for a in labels0])
    check(all(-q[i][i] == 1 for i in range(len(q))))
    n, t = len(q), mp.mpf(4*m)
    aug = mp.zeros(n+1,n+1)
    qm = mpmatrix(q)
    for i in range(n):
        for j in range(n):
            aug[i,j] = qm[j,i]
    aug[0,n] = 1
    expaug = mp.expm(t*aug)
    occ = [expaug[i,n]/t for i in range(n)]
    check(abs(sum(occ)-1)<mp.mpf('1e-70'), exact=False)
    qe = mm(q,e)
    d = sum(occ[i]*sum((mp.mpf((qe[i][b]-l[labels[i]][b]).numerator)
                       /(qe[i][b]-l[labels[i]][b]).denominator)**2
                      for b in range(4)) for i in range(n))
    enough = 1-mp.exp(-t)*sum(t**r/mp.factorial(r) for r in range(m))
    lower = enough/2
    check(lower>mp.mpf('0.4'), exact=False)
    check(lower <= t*mp.sqrt(3*d), exact=False)
    check(d > lower**2/(3*t*t), exact=False)
    return {'m':m,'hidden_states':n,'horizon':str(t),
            'occupation_squared_error':mp.nstr(d,35),
            'path_TV_lower_bound':mp.nstr(lower,35),
            'coupling_upper_bound_unclipped':mp.nstr(t*mp.sqrt(3*d),35)}


def cheb_weights(n, order):
    nodes = [(1-mp.cos(mp.pi*j/n))/2 for j in range(n+1)]
    result = []
    for j in range(n+1):
        cj = mp.mpf('0.5') if j in [0,n] else mp.mpf(1)
        terms = []
        for k in range(n+1):
            ck = mp.mpf('0.5') if k in [0,n] else mp.mpf(1)
            deriv = -2*k*k if order == 1 else mp.mpf(4)*k*k*(k*k-1)/3
            terms.append(ck*deriv*mp.cos(mp.pi*k*j/n))
        result.append(2*cj*sum(terms)/n)
    return nodes, result


def spectral_checks():
    records=[]
    for n in [4,8,12,20,32]:
        nodes,w1=cheb_weights(n,1)
        _,w2=cheb_weights(n,2)
        l1,l2=sum(map(abs,w1)),sum(map(abs,w2))
        check(abs(l1-2*n*n)<mp.mpf('1e-65'), exact=False)
        check(abs(l2-mp.mpf(4)*n*n*(n*n-1)/3)<mp.mpf('1e-65'), exact=False)
        for degree in range(n+1):
            check(abs(sum(w1[j]*nodes[j]**degree for j in range(n+1))
                      -(1 if degree == 1 else 0))<mp.mpf('1e-65'), exact=False)
            check(abs(sum(w2[j]*nodes[j]**degree for j in range(n+1))
                      -(2 if degree == 2 else 0))<mp.mpf('1e-65'), exact=False)
        first = sum(w1[j]*mp.exp(-nodes[j]) for j in range(n+1))
        second = sum(w2[j]*mp.exp(-nodes[j]) for j in range(n+1))
        mixed = sum(w1[j]*w1[h]*mp.exp(-nodes[j]-2*nodes[h])
                    for j in range(n+1) for h in range(n+1))
        bound = 8*mp.exp(4)*n**4*2**(n+1)/mp.factorial(n+1)
        errors = [abs(first+1),abs(second-1),abs(mixed-2)]
        check(max(errors) <= bound, exact=False)
        # Deterministic adversarial nodal errors, not a Monte Carlo assay.
        beta = mp.mpf('1e-15')
        noise_amplification = sum(w1[j]*(beta if w1[j]>=0 else -beta)
                                  for j in range(n+1))
        check(abs(noise_amplification-beta*l1)<mp.mpf('1e-65'), exact=False)
        records.append({'degree':n,'first_weight_l1':mp.nstr(l1,20),
                        'second_weight_l1':mp.nstr(l2,20),
                        'errors':[mp.nstr(v,20) for v in errors],
                        'common_bias_envelope':mp.nstr(bound,20)})
    return records


def receipts():
    head = subprocess.check_output(['git','-C',str(ASTRA),'rev-parse','HEAD'],text=True).strip()
    check(head == PIN)
    specs = [
        ('00_START_HERE.txt',[[1,8]],'authoritative task-first entry, read in full'),
        ('AGENTS.md',[[1,7]],'applicable source access instructions, read in full'),
        ('updates/EE/package/genesis_intervention_products/astra_intervention_products/proof_note.md',
         [[1,428]],'full original N718 proof read; main mathematical capital, independently reconstructed'),
        ('updates/EC/package/active_closure/recovered/astra_active_closure/proof_note.md',
         [[1,240]],'original N713 response, controlled path proof and passive-equivalence argument read'),
        ('frontier/dossiers/N718.txt',None,'current status/gate navigation'),
        ('frontier/gates/G-EE-N718-INDEPENDENT-REVIEW.json',None,'open independent review and acquisition gate'),
        ('frontier/dossiers/N709.txt',None,'overlap check only; no theorem imported'),
    ]
    sources=[]
    for rel,ranges,use in specs:
        data=(ASTRA/rel).read_bytes()
        sources.append({'repository_path':rel,'local_path':str(ASTRA/rel),
                        'raw_url':f'https://raw.githubusercontent.com/harjassand/astra-research-knowledge/{PIN}/{rel}',
                        'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),
                        'read_inclusive_lines':ranges,'use':use,
                        'status':'source research unreviewed; receipt is preservation/access evidence only'})
    obj={'repository':'harjassand/astra-research-knowledge','revision':head,
         'sources':sources,'external_primary_sources':[
             {'url':'https://arxiv.org/abs/2201.10256','scope':'abstract-level prior quantitative coarse-graining comparison; no theorem imported'},
             {'url':'https://arxiv.org/abs/1109.5509','scope':'prior analytic spectral differentiation; needed elementary bound independently given'},
             {'url':'https://www.columbia.edu/cu/neurotheory/pdfs/Paninski_2008.pdf','scope':'prior square-root-support uniformity testing; needed half-support bound independently proved'}],
         'source_rule':'Original bytes not edited. All writes confined to astra_capital.'}
    (OUT/'SOURCE_RECEIPTS.json').write_text(json.dumps(obj,indent=2)+'\n')


def main():
    source_identity_checks()
    output={'status':'finite diagnostics only; no formal, external, statistical-assay or physical certification',
            'counterexamples':counterexample_checks(),
            'uniformity_mixture_exact':collision_checks(),
            'prefix_tree_numerical':prefix_checks(),
            'spectral_numerical':spectral_checks()}
    receipts()
    output['counts']=COUNTS
    output['runtime']={'python':sys.version.split()[0], 'mpmath':mp.__version__,
                       'mpmath_digits':mp.mp.dps,'numerical_interval_certified':False}
    (OUT/'VERIFICATION_RESULTS.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'status':'passed','counts':COUNTS,'outputs':[str(OUT/'VERIFICATION_RESULTS.json'),str(OUT/'SOURCE_RECEIPTS.json')]}))


if __name__ == '__main__':
    main()
