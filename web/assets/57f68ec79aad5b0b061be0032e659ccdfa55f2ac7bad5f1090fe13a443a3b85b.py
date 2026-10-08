"""Finite exact jump recursion. Diagnostic, not part of the proof."""
from collections import defaultdict
from math import fsum
import json

def moments(n, r, steps=30):
    active={(n,1):1.0}
    terminal=defaultdict(float)
    for _ in range(steps):
        nxt=defaultdict(float)
        for (a,b),p in active.items():
            rates=[(a,b+1,r),(a+1,b-1,r*b)]
            if a>0 and b>=2:
                rates.append((a-1,b-2,a*b*(b-1)))
            q=fsum(v for _,_,v in rates)
            for aa,bb,v in rates:
                pp=p*v/q
                if bb==0:
                    terminal[aa-n]+=pp
                else:
                    nxt[aa,bb]+=pp
        active=nxt
    return {'n':n,'r':r,'remaining_mass':fsum(active.values()),
            'mean':fsum(d*p for d,p in terminal.items()),
            'second':fsum(d*d*p for d,p in terminal.items()),
            'scaled_mean':n*fsum(d*p for d,p in terminal.items()),
            'scaled_second_correction':n*(fsum(d*d*p for d,p in terminal.items())-1)}

rows=[moments(n,r) for r in [.1,.5,1.] for n in [50,100,200,500,1000]]
with open('work/agents/critical_crn_blind/moment_diagnostic.json','w') as f:
    json.dump(rows,f,indent=2)
for x in rows:
    print(x)
