from fractions import Fraction as Q
import json, sys
import numpy as np
sys.path.insert(0,'work/FO-continuous-calibration/source-copy/resonant')
from profile_algebra import averaged,poly_terms,edge_coeffs
z=json.load(open('work/FO-continuous-calibration/source-copy/resonant/profile_graph_certificate.json'))
V=[tuple(map(Q,v)) for v in z['vertices']]
G,N,_,_=averaged(1,-1,False);gt,nt=poly_terms(G),poly_terms(N)
eta=Q(1,4);K=10**9
mins=[];argmins=[]
for i,a in enumerate(V):
 row=[]; args=[]
 for j,b in enumerate(V):
  gc=edge_coeffs(gt,a,b);nc=edge_coeffs(nt,a,b);c=[gc[k]-eta*nc[k] for k in range(5)]
  # f(t)=sum c[k] t^(1-k); critical polynomial t^4 f'(t).
  poly=[float(c[0]),0.,-float(c[2]),-2*float(c[3]),-3*float(c[4])]
  roots=np.roots(poly) if any(poly) else []
  cand=[float(x.real) for x in roots if abs(x.imag)<1e-8 and x.real>0]
  vals=[sum(float(c[k])*t**(1-k) for k in range(5)) for t in cand]
  # Limits at the ends of (0,infinity).
  low=next((c[k] for k in (4,3,2) if c[k]),c[1])
  high=c[0] if c[0] else c[1]
  if low<0 or high<0: m=float('-inf'); t=0.
  else:
   m=min(vals+[float(low) if low<0 else (float('inf') if any(c[k] for k in (2,3,4)) else float(c[1])),
                     float(high) if high<0 else (float('inf') if c[0] else float(c[1]))])
   t=cand[vals.index(m)] if cand and m in vals else 0.
  row.append(m);args.append(t)
 mins.append(row);argmins.append(args)
# conservative rational edge lower bound. A 1e-7 margin dominates double-root error.
D=10**8
w=[[int(np.floor(mins[i][j]*D)) for j in range(len(V))] for i in range(len(V))]
# The zero profile has a structural zero self-edge, whose exact minimum is 0.
w[0][0]=0
# Bellman-Ford from virtual source with zero edge to every node.
d=[0]*len(V); pred=[None]*len(V)
for it in range(len(V)):
 nd=d.copy(); npred=pred.copy(); changed=False
 for i in range(len(V)):
  for j in range(len(V)):
   cand=d[i]+w[i][j]
   if cand<nd[j]: nd[j]=cand;npred[j]=i;changed=True
 if not changed: break
 d,pred=nd,npred
else: raise RuntimeError('negative cycle for conservative sampled edge minima')
# Shift to base=0 and save exact rational candidate.
base=d[0];pot=[Q(x-base,D) for x in d]
out={'status':'candidate from high-precision float edge minimization; exact all-width check follows',
     'scale_denominator':D,'conservative_floor_margin':1e-7,
     'potentials':[str(x) for x in pot],
     'min_edge_min':float(np.min(mins)),'max_edge_min_finite':float(np.max(np.array(mins)[np.isfinite(mins)])),
     'argmin_width_range':[float(np.min(np.array(argmins)[np.array(argmins)>0])),float(np.max(argmins))]}
open('work/FO-continuous-calibration/all_width_potential_candidate.json','w').write(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items() if k!='potentials'},indent=2))
