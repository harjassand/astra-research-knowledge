"""Exact finite corroboration of rank-two prediction/control separation.
The all-horizon proofs are in RESEARCH_NOTE.txt. No external data or oracle.
"""
from itertools import product
from fractions import Fraction as F
from math import log
import json
from pathlib import Path
import sympy as sp

def words(d): return list(product((0,1), repeat=d))
def probability(a,r,w):
    p=F(3,4) if a==w else F(1,4)
    return (p if r else 1-p)/2**len(w)

rows=[]
for d in range(1,9):
    w=tuple(i%2 for i in range(d))
    ranks=[]
    for t in range(1,d+1):
        H=sp.Matrix([[probability(p+s,r,w) for s in words(d-t) for r in (0,1)] for p in words(t)])
        ranks.append(H.rank())
    assert ranks==[2]*d
    tv=sum(abs(probability(a,r,w)-(F(1,4) if r else F(3,4))/2**d) for a in words(d) for r in (0,1))/2
    assert tv==F(1,2**(d+1))
    # Noiseless minimax construction: query q distinct words, then guess
    # one remaining word. For uniform hidden word exactly q+1 successes.
    N=2**d
    for q in sorted(set((0,1,N//2,N-1))):
        tested=words(d)[:q]; guess=words(d)[q]
        successes=sum(w0 in tested or w0==guess for w0 in words(d))
        assert successes==q+1
    delta=.05
    p=1/N
    kl=p*log(p/(1-delta))+(1-p)*log((1-p)/delta)
    rows.append(dict(horizon=d,cut_ranks=ranks,trajectory_TV=str(tv),noisy_episodes_lower_bound=N*kl/(.5*log(3))))

# Revealing progress sensor, deterministic fixture: one revelation per test
# recovers every password with d tests, independent of hidden state access.
for d in range(1,10):
    for w in words(d):
        recovered=[]
        for t in range(d):
            proposal=tuple(recovered+[0])
            progress=(proposal==w[:t+1])
            recovered.append(0 if progress else 1)
        assert tuple(recovered)==w

out={'status':'ALL_EXACT_FIXTURES_PASSED','rows':rows,'reveal_passwords_checked':sum(2**d for d in range(1,10))}
Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
