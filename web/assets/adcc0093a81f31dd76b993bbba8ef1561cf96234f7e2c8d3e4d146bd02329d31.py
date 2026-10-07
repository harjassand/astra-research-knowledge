"""Exact finite stress tests of Q modular repair with paired shared keys.

These audit only finite shift distributions, representative domination,
and the failed deterministic norm-band-colour alternative; not asymptotics.
"""
from collections import defaultdict
from fractions import Fraction
from itertools import product
from math import comb, exp, sqrt
from pathlib import Path
import json

checks = 0
shift_cases = 0
worst_slack = Fraction(1)
for Q in range(2, 6):
    for s in range(1, 4):
        for p in (Fraction(1,8),Fraction(1,2)):
            a=p/(Q-1)
            assert 1-p >= a
            denom=p.denominator*(Q-1)
            weights=[(p.denominator-p.numerator)*(Q-1)]+[p.numerator]*(Q-1)
            shifts=[]
            for E in product(range(Q),repeat=s):
                w=1
                for e in E: w*=weights[e]
                shifts.append((E,w))
            for c0 in product(range(Q),repeat=s):
                # The second occurrence of key i can have a DIFFERENT outer colour.
                for offset in range(Q):
                    reps=defaultdict(int); full=defaultdict(int)
                    for E,w in shifts:
                        x=sum((c0[i]+E[i])%Q==0 for i in range(s))
                        y=x+sum((c0[i]+offset+E[i])%Q==0 for i in range(s))
                        assert y>=x
                        reps[x]+=w;full[y]+=w
                        shift_cases+=1
                    for threshold in range(1,s+1):
                        p_rep=Fraction(sum(w for x,w in reps.items() if x<threshold),denom**s)
                        p_full=Fraction(sum(w for x,w in full.items() if x<threshold),denom**s)
                        p_bin=sum(Fraction(comb(s,x))*a**x*(1-a)**(s-x) for x in range(threshold))
                        assert p_full<=p_rep<=p_bin,(Q,s,p,c0,offset,threshold,p_full,p_rep,p_bin)
                        worst_slack=min(worst_slack,p_bin-p_rep)
                        checks+=1

# Rich-target representatives are Bernoulli(1-p) regardless of Q.
rich_checks=0
for p in (Fraction(1,100),Fraction(1,16),Fraction(1,8)):
    for s in range(1,31):
        prob=sum(Fraction(comb(s,x))*(1-p)**x*p**(s-x) for x in range(s+1) if x<Fraction(s,2))
        assert float(prob)<=(2*sqrt(float(p)))**s+1e-14
        rich_checks+=1

# A deterministic attempt C=floor(||q y||^2) mod Q can be constant
# on a real cyclic AP: with y_j=jQ/q, q>2kQ, the band is j^2 Q^2.
counterexamples=[]
for Q in range(2,9):
    k=12; lattice_q=1009 # Prime exceeds 2*k*Q in these cases.
    ys=[Fraction(j*Q,lattice_q) for j in range(k)]
    assert all(y<Fraction(1,2) for y in ys)
    bands=[(lattice_q*y)**2 for y in ys]
    assert all(z.denominator==1 and z.numerator%Q==0 for z in bands)
    counterexamples.append({'Q':Q,'k':k,'q':lattice_q,'bands':[int(z) for z in bands]})

out={'exact_cdf_checks':checks,'enumerated_shared_key_shift_cases':shift_cases,
     'rich_tail_checks':rich_checks,'worst_domination_slack':str(worst_slack),
     'deterministic_band_mod_Q_counterexamples':counterexamples,
     'asymptotic_theorem_verified_by_computation':False}
Path(__file__).with_name('FINITE_CHECKS.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items() if k!='deterministic_band_mod_Q_counterexamples'},indent=2))
