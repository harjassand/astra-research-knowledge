"""Exact Rep4/Par4 tree-resolution cochain projection and packet-norm contract.
No stochastic/admissibility assumption: all32 fine syndrome vectors checked.
"""
import json
from sheaf_incidence_compiler import echelon,solve
reports=[]
for color in ['blue','red']:
 old=[15] if color=='blue' else [3,5,9]
 # two3-face junctions on(0,1,aux4) and(2,3,aux4)
 new=[19,28] if color=='blue' else [3,17,12,20]
 auximage=3 if color=='blue' else 1
 def p2(s):return (s&15)^(auximage if s>>4&1 else 0)
 p1=[solve(echelon(old),p2(g)) for g in new]
 i1=[solve(echelon(new),g) for g in old]
 h2=solve(echelon(new),(1<<4)|auximage)
 def apply(cols,s):
  out=0
  for j,c in enumerate(cols):
   if s>>j&1:out^=c
  return out
 for j in range(len(new)):
  # 1+IP = h d in degree1 (no degree0 in transverse cancellation)
  assert (1<<j)^apply(i1,p1[j])==(h2 if new[j]>>4&1 else 0)
 for s in range(32):
  image=p2(s);mu=(image.bit_count()+1)//2 if color=='blue' else image.bit_count()
  assert mu<=s.bit_count()
  assert s^p2(s)==apply(new,h2 if s>>4&1 else 0)
 reports.append(dict(color=color,old_generators=old,new_generators=new,P2_aux=auximage,P1=p1,I1=i1,h2_aux=h2,all_syndromes=32,packet_contraction_verified=True))
print(json.dumps(reports,indent=2))
