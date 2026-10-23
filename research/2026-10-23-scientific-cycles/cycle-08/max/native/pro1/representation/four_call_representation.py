#!/usr/bin/env python3
"""Exact, root-retaining finite-path algebra for correlated four-call inputs.

No bath truncation or long-time simulation. Each path uses the infinite Fock
coordinate rules, including vacuum seed exchange. The bulk coefficient matrix
acts on a four-letter prefix and is tensor the identity on the untouched tail.
Coefficients are integers in alpha^(8-r) beta^r; charge-preserving bulk blocks
have only even r. Standard library only.
"""
from collections import defaultdict
from itertools import product
from fractions import Fraction as F
from math import comb
import argparse, json, platform, resource, time


def charge(x): return sum(a != 0 for a in x)

def history(x, seed, word, mask):
    """mask bit 1 = stay, otherwise the actual U edge reversal."""
    out=[]; stays=0; word=tuple(word)
    for j,a in enumerate(x):
        if (mask>>j)&1:
            out.append(a); stays+=1
        elif a:
            word=(a,)+word; out.append(0)
        elif word:
            out.append(word[0]); word=word[1:]
        else:
            seed=1-seed; out.append(0)
    return tuple(out),seed,word,stays


def drift_coefficients(n=4, depth=4):
    """Return D_r[(i,u,j,v)] for total stay count r; complex coeff as int pair.

    Matrix orientation <input_i,prefix_u| D |input_j,prefix_v>. The overall
    monomial is alpha^(2*n-r) beta^r. Only equal input-charge sectors retained.
    Also return the charge-compressed unitarity Gram coefficients.
    """
    words=list(product((0,1,2), repeat=n)); baths=list(product((1,2), repeat=depth))
    grouped=defaultdict(list)
    for i,x in enumerate(words):
        for u,w in enumerate(baths):
            for mask in range(1<<n):
                y,seed,v,r=history(x,0,w,mask)
                grouped[(charge(x),y,seed,v)].append((i,u,r))
    drift=[defaultdict(complex) for _ in range(2*n+1)]
    gram=[defaultdict(complex) for _ in range(2*n+1)]
    for (q,y,seed,v),paths in grouped.items():
        delta=len(v)-depth
        for i,u,r in paths:
            for j,w,s in paths:
                c=(1j)**((s-r)%4)
                key=(i,u,j,w)
                gram[r+s][key]+=c
                drift[r+s][key]+=delta*c
    drift=[{k:(int(v.real),int(v.imag)) for k,v in d.items() if v} for d in drift]
    gram=[{k:(int(v.real),int(v.imag)) for k,v in d.items() if v} for d in gram]
    return words,baths,drift,gram


def b_polynomial(drift,n):
    """Substitute alpha^2=1-b, beta^2=b in charge-preserving bulk matrix."""
    assert all(not drift[r] for r in range(1,2*n+1,2))
    out=[defaultdict(int) for _ in range(n+1)]
    for k in range(n+1):
        for key,(re,im) in drift[2*k].items():
            assert im==0
            for j in range(n-k+1):out[k+j][key]+=re*comb(n-k,j)*((-1)**j)
    return [{k:v for k,v in d.items() if v} for d in out]


def entry(poly,key):return [d.get(key,0) for d in poly]


def run():
    started=time.perf_counter();words,baths,drift,gram=drift_coefficients()
    poly=b_polynomial(drift,4);gpoly=b_polynomial(gram,4)
    nwords,nbaths=len(words),len(baths)
    identity={(i,u,i,u):1 for i in range(nwords) for u in range(nbaths)}
    assert gpoly[0]==identity and all(not d for d in gpoly[1:])
    # At beta=0, exact drift is 2N-4; for diagonal inputs, all beta dependence
    # is exactly (1-b)(2N-4), independent of the bath prefix.
    d0={(i,u,i,u):2*charge(x)-4 for i,x in enumerate(words) for u in range(nbaths) if 2*charge(x)-4}
    assert poly[0]==d0
    for i,x in enumerate(words):
        for u in range(nbaths):
            expected=[2*charge(x)-4,4-2*charge(x),0,0,0]
            assert entry(poly,(i,u,i,u))==expected
    # Concrete failure of scalar depth closure, valid for every beta.
    i=words.index((1,0,0,0));j=words.index((0,1,0,0))
    for u,w in enumerate(baths):
        for v,z in enumerate(baths):
            expected=[0,1,-1,0,0] if u==v and w[0]==2 else [0]*5
            assert entry(poly,(i,u,j,v))==expected
            assert entry(poly,(j,u,i,v))==expected
    # Localized root effect: |0000> makes zero moves in depth at vacuum,
    # and full paths include vacuum seed exchange. No reflecting rule used.
    assert history((0,0,0,0),0,(),0)==((0,0,0,0),0,(),0)
    assert history((0,),0,(),0)==((0,),1,(),0)
    # Complete first nontrivial drift matrix exported sparsely for reuse.
    sparse={str(k):[[*key,value] for key,value in sorted(d.items())] for k,d in enumerate(poly)}
    return {
      'scope':'Exact four-call bulk drift on charge-preserving input sectors; root-retaining path algorithm; no asymptotic claim',
      'input_words':[list(w) for w in words], 'bath_prefix_words':[list(w) for w in baths],
      'coefficient_convention':'D(b)=sum b^k D_k, entries [input_i,prefix_u,input_j,prefix_v,value]; each D_k is tensor I on seed and untouched tail for initial depth>=4',
      'input_dimension':81,'prefix_dimension':16,
      'nonzero_monomials_by_total_stays':[len(d) for d in drift],
      'nonzero_b_polynomial_entries':[len(d) for d in poly],
      'odd_bulk_powers_vanish':True,'full_gram_identity_checked':True,
      'diagonal_drift_exact':'(1-b)(2 charge(input)-4) I',
      'closure_counterexample':{'rho':'rho_c^tensor4 + epsilon (|1000><0100|+h.c.)','range':'0<epsilon<=1/32','exact_bulk_drift':'2 epsilon b(1-b)(I-S1S1*)','top_color_1':0,'top_color_2':'2 epsilon b(1-b)'},
      'bulk_drift_coefficients':sparse,
      'wall_seconds':time.perf_counter()-started,'max_rss_kib_linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'python':platform.python_version()
    }

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',default='four_call_representation.json');args=ap.parse_args()
    result=run();open(args.output,'w').write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('bulk_drift_coefficients','input_words','bath_prefix_words')},indent=2))
