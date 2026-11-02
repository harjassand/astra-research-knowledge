#!/usr/bin/env python3
"""Counterexample to extrapolating the two-mode sign theorem to three hidden modes."""
import json
from fractions import Fraction as F

# Each molecule retains one of three modes throughout the whole sequence.
# One-stage action effects may switch signs twice as a function of p.
p = [F(1,10), F(1,2), F(9,10)]
a = [F(1,10), F(85,100), F(4,10)]
b = [F(9,10), F(15,100), F(5,10)]
w = [F(1,3)]*3

def delta(n):
    return sum(wj * (pj**n) * (aj-bj) for wj,pj,aj,bj in zip(w,p,a,b))

d0 = delta(0); d1=delta(1); d74=delta(74)
assert d0 < 0 < d1 and d74 < 0
# finite horizon sign changes
sign = lambda x: 1 if x>0 else -1 if x<0 else 0
seq = [delta(n) for n in range(100)]
switches = [(n,str(seq[n]), float(seq[n])) for n in range(1,100) if sign(seq[n])!=sign(seq[n-1])]
res={'three_modes': [{'p':str(pi),'A':str(ai),'B':str(bi),'weight':str(wi)} for pi,ai,bi,wi in zip(p,a,b,w)],
     'd0_exact':str(d0),'d0':float(d0),'d1_exact':str(d1),'d1':float(d1),
     'd74_exact':str(d74),'d74':float(d74),'sign_changes':switches,
     'conclusion':'Two short contrast signs do not imply long-horizon preference with three modes.'}
with open('producer-workspace/three_mode_falsifier_results.json','w') as f:json.dump(res,f,indent=2)
print(json.dumps(res,indent=2)[:1600])
