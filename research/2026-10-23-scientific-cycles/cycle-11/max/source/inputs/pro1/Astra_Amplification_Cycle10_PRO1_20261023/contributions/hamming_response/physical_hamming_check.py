#!/usr/bin/env python3
"""Bounded diagnostic of the NEW all-distance response interface.

Physical amplitudes are (6 U + i I)/sqrt(37); each whole-path amplitude
has a Gaussian-integer numerator. No bath cutoff or classical mixture is used.
All exact integer identities below are checked before numerical eigenvalues.
The analytic proof, not these finite checks, supplies the all-length theorem.
"""
from itertools import product
from math import comb, exp, sqrt
from pathlib import Path
import json, resource, time
import numpy as np

ROOT = Path(__file__).resolve().parent
START = time.perf_counter()

def histories(word, prefix):
    states = {((), prefix): 1+0j}
    for c in word:
        nxt = {}
        for (out, stack), amplitude in states.items():
            key = (out+(c,), stack)
            nxt[key] = nxt.get(key, 0j) + 1j*amplitude
            if c:
                key = (out+(0,), (c,)+stack)
            else:
                assert stack, 'A bulk history unexpectedly reached the root early.'
                key = (out+(stack[0],), stack[1:])
            nxt[key] = nxt.get(key, 0j) + 6*amplitude
        states = nxt
    return states

def build(k, selected_patterns=None):
    words = [w for w in product(range(3), repeat=k)
             if selected_patterns is None or tuple(int(c!=0) for c in w) in selected_patterns]
    prefixes = list(product((1,2), repeat=k))
    basis = [(w,p) for w in words for p in prefixes]
    output = {}
    for column,(word,prefix) in enumerate(basis):
        for (out,stack),amp in histories(word,prefix).items():
            output.setdefault((out,stack),[]).append((column,amp))
    n = len(basis)
    gram = np.zeros((n,n), dtype=np.complex128)
    qgram = np.zeros_like(gram)
    for (out,stack),entries in output.items():
        idx = np.array([j for j,_ in entries])
        amps = np.array([v for _,v in entries])
        block = np.outer(amps.conj(),amps)
        gram[np.ix_(idx,idx)] += block
        qgram[np.ix_(idx,idx)] += sum(c!=0 for c in out)*block
    denom = 37**k
    # Every Gaussian-integer partial sum is bounded in magnitude by k*37**k
    # using the absolute-amplitude Cauchy--Schwarz bound. This is below the
    # exact integer range of the binary64 components in these bounded cases.
    assert k*denom < 2**53
    assert np.array_equal(gram, denom*np.eye(n))
    charges = np.array([sum(c!=0 for c in w) for w,p in basis])
    patterns = [tuple(int(c!=0) for c in w) for w,p in basis]
    gnum = denom*np.diag(charges)-qgram
    gnum[charges[:,None]!=charges[None,:]]=0
    assert np.array_equal(gnum,gnum.conj().T)
    groups = {x:np.array([i for i,y in enumerate(patterns) if y==x]) for x in set(patterns)}
    for x,idx in groups.items():
        expected=36*37**(k-1)*(2*sum(x)-k)*np.eye(len(idx))
        assert np.array_equal(gnum[np.ix_(idx,idx)],expected)
    return words,prefixes,patterns,groups,gnum/denom

observations=[]
for k,selected in [(2,None),(3,None),(4,{(0,1,0,1),(1,0,1,0)})]:
    words,prefixes,patterns,groups,g=build(k,selected)
    a,b=36/37,1/37
    flip_sets={tuple(i for i in range(k) if x[i]!=y[i])
               for x in groups for y in groups if sum(x)==sum(y) and x!=y}
    level=[]
    for T in sorted(flip_sets):
        z=np.zeros_like(g)
        for x,ix in groups.items():
            y=tuple(1-v if j in T else v for j,v in enumerate(x))
            if y in groups and sum(x)==sum(y):
                iy=groups[y]
                z[np.ix_(ix,iy)]=g[np.ix_(ix,iy)]
        m=len(T)//2
        bound=m*comb(2*m,m)*(a*b)**m
        norm=float(np.max(np.abs(np.linalg.eigvalsh(z))))
        assert norm<=bound+1e-12
        level.append({'endpoints':T,'m':m,'norm_numeric':norm,'analytic_bound':bound})
    record={'k':k,'selected_charge_patterns':None if selected is None else sorted(selected),
            'joint_input_prefix_dimension':len(g),'exact_isometry_gram':'PASS',
            'exact_complete_pattern_diagonal':'PASS','flip_set_bounds':level}
    if selected is None:
        z=g.copy()
        for ix in groups.values():z[np.ix_(ix,ix)]=0
        z2=z@z
        observed=max(float(np.linalg.eigvalsh(z2[np.ix_(ix,ix)])[-1]) for ix in groups.values())
        r=b*k
        bound=r*r*exp(4*r*r)
        assert observed<=bound+1e-12
        record['row_square']={'max_numeric':observed,'analytic_bound':bound}
        rng=np.random.default_rng(20261023+k)
        ni,nf=len(words),len(prefixes)
        y=rng.normal(size=(ni,ni)); y=(y+y.T)/2
        for i,x in enumerate(words):
            for j,w in enumerate(words):
                if sum(c!=0 for c in x)!=sum(c!=0 for c in w) or tuple(c!=0 for c in x)==tuple(c!=0 for c in w):y[i,j]=0
        weights=np.array([2.0**(-k-sum(c!=0 for c in w)) for w in words])
        norm2=sqrt(float(np.sum(weights[:,None]*y*y)))
        response=np.einsum('ab,buav->uv',weights[:,None]*y,g.reshape(ni,nf,ni,nf))
        norm=float(np.max(np.abs(np.linalg.eigvalsh(response))))
        bound=r*exp(2*r*r)*norm2
        assert norm<=bound+1e-12
        record['weighted_response']={'random_seed':20261023+k,'weighted_L2':norm2,
                                     'operator_norm_numeric':norm,'analytic_bound':bound}
    observations.append(record)

out={'device':'(6 U+i I)/sqrt(37), actual bulk histories, same evolving bath',
     'beta_squared':'1/37','prefix_depth':'k, no root hit before last call',
     'observations':observations,'all_checks':'PASS',
     'wall_seconds':time.perf_counter()-START,
     'peak_rss_kib_linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
     'scope':'Bounded exact integer identity checks and numerical norm diagnostics of new formulas. No all-length certification or capacity computation. Discovery/inference costs unknown.'}
(ROOT/'physical_hamming_check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
