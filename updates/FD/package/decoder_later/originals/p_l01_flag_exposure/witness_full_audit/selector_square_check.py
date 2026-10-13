#!/usr/bin/env python3
"""Independent two-bit check of the exact-on-completion tournament."""
from __future__ import annotations
import json, random, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
COMPILER=ROOT/'p_s01c_witness_compiler'
sys.path.insert(0,str(COMPILER))
import witness_compiler as wc
ac=wc.ac

def rank(x):
    return (((x>>0)&1)<<1) | ((x>>1)&1)

def cmp(x,y):
    return int(rank(x)<rank(y))

results=[]
for basis in ([1,2],[2,1]):
    for seed in range(16):
        source=ac.Source(cmp)
        meter=ac.Meter()
        cfg=wc.parameters(2,0,2,.5,prefix_length=2,mode='witness')
        winner,trials,reason=ac._select_certified_zero(list(basis),0,source,random.Random(seed),cfg,meter,dict(attempts=0,matches=0))
        results.append(dict(basis=list(basis),seed=seed,winner=winner,reason=reason,
                            trials=trials,comparisons=source.calls))
        assert reason is None,(basis,seed,reason)
        assert winner==1,(basis,seed,winner)
        assert len(trials)==1
out=dict(scope='finite deterministic helper check only; not the proof',
         source='identity lex order Q(x0,x1)=(x0,x1)',true_q0='x0',
         flag_vectors=[1,2],selected_vector=1,results=results,
         conclusion='for both basis orders and all 16 tested PRNG seeds the exact helper returns e0; pairwise lex-order argument is given in AUDIT.txt')
Path(__file__).with_name('selector_square_check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(status='PASS',cases=len(results),selected_direction=1)))
