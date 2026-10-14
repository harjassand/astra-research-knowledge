from fractions import Fraction as Q
import json, sys
from math import isclose
import numpy as np
sys.path.insert(0, 'work/FO-continuous-calibration/source-copy/resonant')
from profile_algebra import averaged, poly_terms, edge_coeffs
z=json.load(open('work/FO-continuous-calibration/source-copy/resonant/profile_graph_certificate.json'))
verts=[tuple(map(Q,v)) for v in z['vertices']]
P=[Q(int(v),int(z['common_denominator'])) for v in z['potential_numerators']]
G,N,_,_=averaged(1,-1,False); gt,nt=poly_terms(G),poly_terms(N); eta=Q(1,4)
worst=(0,None)
for i,a in enumerate(verts):
 for j,b in enumerate(verts):
  gc=edge_coeffs(gt,a,b); nc=edge_coeffs(nt,a,b)
  cs=[gc[k]-eta*nc[k] for k in range(5)]
  cs[1]-=P[j]-P[i]
  # derivative polynomial after multiplying tau^4
  poly=[float(-3*cs[4]),float(-2*cs[3]),float(-cs[2]),0.,float(cs[0])]
  roots=np.roots(poly)
  cand=[float(x.real) for x in roots if abs(x.imag)<1e-8 and x.real>0]
  for t in cand:
   val=sum(float(cs[k])*t**(1-k) for k in range(5))
   if val<worst[0]:worst=(val,(i,j,t,cs))
print('worst',worst[0],worst[1][:3] if worst[1] else None)
if worst[1]:
 i,j,t,cs=worst[1]
 print('endpoints',verts[i],verts[j],'nearwidth',t,'coeffs',cs)
 for tt in [Q(1,100),Q(1,10),Q(1,4),Q(1,2),Q(1),Q(2),Q(4),Q(10),Q(100)]:
  val=sum(cs[k]*tt**(1-k) for k in range(5))
  print(tt,val)
