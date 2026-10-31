"""Small exhaustive validators for decision-core counterexamples.

This file tests explicit finite examples. It does not experimentally
establish the complexity or information lower bounds in the proof note.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import product
from pathlib import Path
import json
import math


def energy(x, edges, fields):
    return sum(w*x[i]*x[j] for i,j,w in edges)+sum(h*y for h,y in zip(fields,x))


def minimizers(n, edges, fields):
    values=[(energy(x,edges,fields),x) for x in product((-1,1), repeat=n)]
    v=min(e for e,x in values)
    return v,[x for e,x in values if e==v]


def dominance_core(n,edges,fields):
    active=set(range(n)); pins={}; h=list(fields)
    changed=True
    while changed:
        changed=False
        for i in sorted(active):
            radius=sum(abs(w) for a,b,w in edges if (a==i and b in active) or (b==i and a in active))
            if abs(h[i])>radius:
                x=-1 if h[i]>0 else 1
                pins[i]=x;active.remove(i)
                for a,b,w in edges:
                    if a==i and b in active:h[b]+=w*x
                    elif b==i and a in active:h[a]+=w*x
                changed=True
                break
    return sorted(active),pins


def main():
    checks=[]
    n=8
    edges=[(i,(i+1)%n,Fraction(-1)) for i in range(n)]
    for label,fields in [
        ("zero_field_ferromagnet",[Fraction(0)]*n),
        ("unique_optimum_small_field_ferromagnet",[Fraction(1,100)]*n),
        ("large_fields_pin_all",[Fraction(3)]*n),
    ]:
        v,opts=minimizers(n,edges,fields)
        core,pins=dominance_core(n,edges,fields)
        if label=="zero_field_ferromagnet":
            assert len(core)==n and len(opts)==2
        elif label=="unique_optimum_small_field_ferromagnet":
            assert len(core)==n and opts==[(-1,)*n]
        else:
            assert not core and opts==[(-1,)*n]
        checks.append(dict(name=label,core_size=len(core),optimum_count=len(opts),minimum=str(v)))

    interval_examples=[]
    for n in (2,4,6,8):
        rho=Fraction(1,1000)
        candidate=tuple(1 if i%3 else -1 for i in range(n))
        edges=[(i,j,rho*candidate[i]*candidate[j]) for i in range(n) for j in range(i+1,n)]
        v,opts=minimizers(n,edges,[Fraction(0)]*n)
        regret=energy(candidate,edges,[Fraction(0)]*n)-v
        assert regret==rho*n*n/2
        interval_examples.append(dict(n=n,rho=str(rho),candidate_regret=str(regret),formula=str(rho*n*n/2)))

    # Threshold responses distinguish arbitrarily close unknown coefficients
    # once an external field is chosen between their switching thresholds.
    a=Fraction(1,1000000)
    _,plus=minimizers(1,[],[a])
    _,minus=minimizers(1,[],[-a])
    assert plus==[(-1,)] and minus==[(1,)]

    # Validate the Bernoulli information-radius inequality used in the proof.
    ratios=[]
    for j in range(1,501):
        a_over_b=j/1000
        q=.5+a_over_b/2
        kl=q*math.log(2*q)+(1-q)*math.log(2*(1-q))
        bound=a_over_b*a_over_b
        assert kl<=bound+1e-14
        ratios.append(kl/bound)
    result={
        "verdict":"All explicit decision-core counterexamples passed.",
        "dominance_fixtures":checks,
        "interval_box_fixtures":interval_examples,
        "arbitrarily_small_signal":str(a),
        "opposite_optima": [list(plus[0]),list(minus[0])],
        "bernoulli_information_bound_checks":len(ratios),
        "largest_information_to_upper_bound_ratio":max(ratios),
        "scope":"No sample-optimality, runtime-hardness, or new positive capability claim is inferred from enumeration."
    }
    Path(__file__).with_name("decision_obstruction_results.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__":main()
