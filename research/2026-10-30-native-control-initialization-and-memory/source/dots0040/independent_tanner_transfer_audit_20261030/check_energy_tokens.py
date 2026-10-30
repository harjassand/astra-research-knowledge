from itertools import combinations
from pathlib import Path
import json
counts=dict(pair_checks=0,orbit_checks=0)
for edges,n,kind in [([(i,(i+1)%6) for i in range(6)],6,'rep'),(list(combinations(range(4),2)),4,'even')]:
 stars=[sum(1<<j for j,e in enumerate(edges) if v in e) for v in range(n)]
 def subs(x):
  y=x
  while True:
   yield y
   if not y:break
   y=(y-1)&x
 codes=[[0,s] if kind=='rep' else [c for c in subs(s) if c.bit_count()%2==0] for s in stars]
 energies=[];tokens=[]
 for e in range(1<<len(edges)):
  uv=[min(((e&s)^c).bit_count() for c in code) for s,code in zip(stars,codes)]
  energies.append(uv);bits=0;off=0
  for u,s in zip(uv,stars):bits|=((1<<u)-1)<<off;off+=s.bit_count()
  tokens.append(bits)
  assert bits.bit_count()==sum(uv)<=2*e.bit_count()
 for e in range(1<<len(edges)):
  for f in range(1<<len(edges)):
   du=sum(abs(a-b) for a,b in zip(energies[e],energies[e^f]))
   assert (tokens[e]^tokens[e^f]).bit_count()==du<=2*f.bit_count()
   counts['pair_checks']+=1
  for Z in range(1<<len(edges)):
   orbit=[tokens[e^f] for f in subs(Z)];AND=orbit[0];OR=orbit[0]
   for t in orbit:AND&=t;OR|=t
   assert (OR^AND).bit_count()<=2*Z.bit_count()
   counts['orbit_checks']+=1
# Preserved counterexample to persistence based only on unary energy.
e=1;ep=2;f=1
assert e.bit_count()==ep.bit_count()==1
assert (e^f).bit_count()<1 and (ep^f).bit_count()>1
out=dict(status='pass',**counts,energy_only_persistence_counterexample_preserved=True,scope='Toy exact energy/token/Lipschitz/orbit algebra, not Tanner expansion or memory simulation')
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
