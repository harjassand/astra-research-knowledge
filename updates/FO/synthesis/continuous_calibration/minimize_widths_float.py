from fractions import Fraction as Q
import json, sys
import numpy as np
sys.path.insert(0,'work/FO-continuous-calibration/source-copy/resonant')
from profile_algebra import averaged,poly_terms,edge_coeffs
z=json.load(open('work/FO-continuous-calibration/source-copy/resonant/profile_graph_certificate.json'))
V=[tuple(map(Q,v)) for v in z['vertices']]
G,N,_,_=averaged(1,-1,False);gt,nt=poly_terms(G),poly_terms(N)
M=np.zeros((len(V),len(V))); arg=np.zeros_like(M)
for i,a in enumerate(V):
 for j,b in enumerate(V):
  gc=edge_coeffs(gt,a,b);nc=edge_coeffs(nt,a,b);c=[gc[k]-Q(1,4)*nc[k] for k in range(5)]
  poly=[float(c[0]),0.,-float(c[2]),-2*float(c[3]),-3*float(c[4])]
  roots=np.roots(poly); ts=[float(z.real) for z in roots if abs(z.imag)<1e-8 and z.real>0]
  vals=[sum(float(c[k])*t**(1-k) for k in range(5)) for t in ts]
  # Include asymptotic infima only when finite (constant profile endpoint degeneracies).
  if not ts: vals.append(float('inf'))
  ix=int(np.argmin(vals));M[i,j]=vals[ix];arg[i,j]=ts[ix] if ts else 0.
# Floyd-Warshall all-pairs, with approximate min edge weights.
d=M.copy(); nxt=np.tile(np.arange(len(V)),(len(V),1))
for k in range(len(V)):
 d=np.minimum(d,d[:,k,None]+d[None,k,:])
neg=[(i,d[i,i]) for i in range(len(V)) if d[i,i]<-1e-8]
print('negative cycles?',neg[:5], 'n=',len(neg))
print('edge min range',M.min(),M.max())
if not neg:
 dist=d[0]
 print('finite potential range',dist.min(),dist.max())
 # verify each edge inequality with inf weights
 sl=M+dist[:,None]-dist[None,:]
 print('min reduced edge slack',sl.min(),'negative edges',int(np.sum(sl<-1e-8)))
 ij=np.unravel_index(np.argmin(sl),sl.shape);print('worst',ij,V[ij[0]],V[ij[1]],'minTau',arg[ij])
