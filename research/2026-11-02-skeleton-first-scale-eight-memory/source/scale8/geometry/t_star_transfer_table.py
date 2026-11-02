"""All relative coset costs, including unmatched boundary charges.
Tropical/min-cost table intended for gluing; does not assume unmatched traces vanish.
"""
import json
out={}
for name,F in [('blue',[0,7]),('red',[0,3,5,6])]:
 def rep(x):return min((x^f for f in F),key=lambda y:(y.bit_count(),y))
 table={}
 for x in range(32768):
  a,p,b,q,c=[(x>>(3*j))&7 for j in range(5)]
  key=(rep(a^p),rep(b^q),rep(p^q^c))
  value=(x.bit_count(),x)
  if key not in table or value<table[key]:table[key]=value
 out[name]=[dict(U=k[0],V=k[1],W=k[2],min_input_weight=v[0],representative=v[1],matched=(k[0]==k[1] and k[2]==0)) for k,v in sorted(table.items())]
print(json.dumps(out,indent=2))
