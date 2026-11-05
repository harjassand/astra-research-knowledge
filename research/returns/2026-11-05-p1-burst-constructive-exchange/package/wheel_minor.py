from bdl_matroid_probe import rank_and_relations,relation_columns
from bdl_cmr_probe import fundamental
from find_fano_submatrix import search
from itertools import combinations
import json
edges=[('A','B'),('A','C'),('B','C'),('A','D'),('B','E'),('C','D'),('C','E'),('D','E')]
v={x:i for i,x in enumerate('ABCDE')}
_,cyc=rank_and_relations([(1<<v[a])^(1<<v[b]) for a,b in edges])
F=relation_columns(cyc,len(edges))
# w=bit0 and u=bit1 in old dependency space.
D=[0,1,0,1,0,3,2,2]
labels=[];cols=[]
for d in [1,2,3]:cols.append(d);labels.append(('D',d))
for i,e in enumerate(edges):
 for t in [0,1]:cols.append((F[i]<<2)^(D[i] if t else 0));labels.append(('F',e,t))
chosen,rest,cs=fundamental(cols)
rows=[sum(1<<j for j,c in enumerate(cs) if (c>>i)&1) for i in range(len(chosen))]
w=search(rows,cs)
print('rank',len(chosen),'F',F,'witness',w)
# Exhaust all rank-3 contractions. 19 elements tiny.
r=len(chosen)
for ids in combinations(range(len(cols)),r-3):
 bv={}
 for ii in ids:
  x=cols[ii]
  while x:
   p=x.bit_length()-1
   if p not in bv:bv[p]=x;break
   x^=bv[p]
 if len(bv)!=r-3:continue
 reps={}
 for i,x in enumerate(cols):
  for p in sorted(bv,reverse=True):
   if (x>>p)&1:x^=bv[p]
  if x:reps.setdefault(x,i)
 if len(reps)==7:
  out={'contract':[labels[i] for i in ids],'keep':[labels[i] for i in reps.values()],'quotient_vectors':list(reps),'edges':edges,'F':F,'D':D}
  print(json.dumps(out,indent=2));open('exchange_20261105/matroid_certificates/wheel_Fano.json','w').write(json.dumps(out,indent=2)+'\n');break
else:print('NO FANO MINOR')
