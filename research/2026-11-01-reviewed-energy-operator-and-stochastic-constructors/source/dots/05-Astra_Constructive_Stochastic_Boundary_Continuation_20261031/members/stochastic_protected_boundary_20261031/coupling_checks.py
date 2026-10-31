"""Exact local generator marginal/dominance challenges; not a proof substitute."""
from fractions import Fraction as F
from itertools import product
from math import prod
from collections import defaultdict
import json
import protected_boundary as p

def ff(x,u):return prod(prod(range(a-b+1,a+1)) for a,b in zip(x,u))
def audit(sp,rs):
    rec=p.recognize(sp,rs);assert rec['accepted'];S=rec['service'];m=len(S)
    linear={(u,v) for u,v,k in rec['linear_core']};cases=0;events=0
    for x in product(range(3),repeat=len(sp)):
      y=tuple(x[i] for i in S)
      for b in product([0,1],repeat=m):
        if any(a>z for a,z in zip(b,y)):continue
        xm=defaultdict(F);bm=defaultdict(F);target=defaultdict(F)
        for u,v,k in rec['reactions']:
            if any(z<a for z,a in zip(x,u)):continue
            rate=k*ff(x,u);xp=tuple(z-a+c for z,a,c in zip(x,u,v))
            localu=tuple(u[i] for i in S);localv=tuple(v[i] for i in S)
            islinear=all(u[j]==v[j]==0 for j in rec['satellites']) and (localu,localv) in linear
            channels=[]
            if not islinear:channels=[(b,rate)]
            elif sum(localu)==0:
                bp=tuple(min(1,a+c) for a,c in zip(b,localv));channels=[(bp,rate)]
            else:
                i=localu.index(1);protected=k*b[i]
                if protected:
                    bp=tuple(min(1,z-a+c) for z,a,c in zip(b,localu,localv));channels.append((bp,protected))
                if rate>protected:channels.append((b,rate-protected))
            assert sum(r for bp,r in channels)==rate
            for bp,r in channels:
                assert r>=0 and all(bp[i]<=xp[S[i]] for i in range(m))
                xm[xp]+=r
                if bp!=b:bm[bp]+=r
                events+=1
            target[xp]+=rate
        assert xm==target
        expected=defaultdict(F)
        for u,v,k in rec['linear_core']:
            rate=k if sum(u)==0 else k*b[u.index(1)]
            if rate:
                bp=tuple(min(1,z-a+c) for z,a,c in zip(b,u,v))
                if bp!=b:expected[bp]+=rate
        assert bm==expected,(x,b,dict(bm),dict(expected))
        cases+=1
    return {'joint_states':cases,'coupled_event_terms':events,'X_marginals_exact':True,
            'binary_marginal_autonomous':True,'coordinate_dominance_preserved':True}

if __name__=='__main__':
    sp,rs=p.demo_network();out=audit(sp,rs)
    print(json.dumps(out,indent=2,sort_keys=True))
