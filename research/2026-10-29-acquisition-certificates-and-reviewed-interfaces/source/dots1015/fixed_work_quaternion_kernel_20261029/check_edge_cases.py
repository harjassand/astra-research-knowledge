import json,time
from pathlib import Path
from fractions import Fraction as F
import bounded_sos_oracle as bs
import fixed_work_oracle as fw
r=Path(__file__).parent;cases=[('zero',{}),('Choi-Lam',{(2,2,0,0):1,(0,2,2,0):1,(2,0,2,0):1,(0,0,0,4):1,(1,1,1,1):-4}),('negative_constant',{tuple(2*(int(i==a)+int(i==b)) for i in range(4)):-F(1 if a==b else 2) for a in range(4) for b in range(a,4)})];rows=[]
for name,f in cases:
 st=time.time();c=bs.solve(f);assert bs.verify(f,c);rows.append(dict(name=name,seconds=time.time()-st,certificate=c));print(name,float(F(c['gap'])),flush=True)
 if name=='zero':assert F(c['gap'])==0
 if name=='negative_constant':assert F(c['lower'])<=-1 and F(c['upper'])==-1
# Deliberately singular basis must fall back to identity and remain sound.
G=[[F(-int(i==j)) for j in range(10)] for i in range(10)];V=[[F(0) for j in range(10)] for i in range(10)];delta,V=bs.repair(G,V);assert delta==1 and V==[[F(int(i==j)) for j in range(10)] for i in range(10)]
(r/'edge_case_results.json').write_text(json.dumps(dict(cases=rows,singular_basis_fallback=True,scope='Exact special-case and bad-basis checks; no proof of tight SOS gap on all quartics.'),indent=2)+'\n')
