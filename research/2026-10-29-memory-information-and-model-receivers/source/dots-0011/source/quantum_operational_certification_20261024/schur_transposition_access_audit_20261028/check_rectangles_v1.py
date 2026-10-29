#!/usr/bin/env python3
"""Independent Young orthogonal matrices and exact predicted transposition Gram."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
from pathlib import Path
import json,itertools,numpy as np
HERE=Path(__file__).parent

def tableaux(m):
 out=[]
 def rec(w,a,b):
  if a==b==m:out.append(tuple(w));return
  if a<m:rec(w+[0],a+1,b)
  if b<a:rec(w+[1],a,b+1)
 rec([],0,0);return out

def reps(m):
 tabs=tableaux(m);index={t:i for i,t in enumerate(tabs)};d=len(tabs);k=2*m;S=[]
 for a in range(k-1):
  A=np.zeros((d,d))
  for j,t in enumerate(tabs):
   cols=[sum(t[z]==t[p] for z in range(p+1))-1 for p in [a,a+1]]
   axial=(cols[1]-t[a+1])-(cols[0]-t[a]);A[j,j]=1/axial
   sw=list(t);sw[a],sw[a+1]=sw[a+1],sw[a];sw=tuple(sw)
   if sw in index and sw!=t:A[index[sw],j]=np.sqrt(1-1/axial**2)
  assert np.max(abs(A@A-np.eye(d)))<1e-12;S.append(A)
 return tabs,S

def main():
 rows=[]
 for m in range(2,7):
  k=2*m;tabs,S=reps(m);d=len(tabs);edges=list(itertools.combinations(range(k),2));ops=[]
  for a,b in edges:
   indices=list(range(a,b))+list(range(b-2,a-1,-1));U=np.eye(d)
   for z in indices:U=S[z]@U
   ops.append(U)
  N=len(edges);c=k*(k-4)/4;t=c/N;g=3*(k*k-4)/(4*(k-1)*(k-3));dim=k*(k-3)//2
  A=np.array(ops);center=A-t*np.eye(d)[None,:,:];flat=center.reshape(N,-1);G=flat@flat.T/d
  incidence=np.array([[int(v in e) for e in edges] for v in range(k)]);P=np.eye(N)-incidence.T@np.linalg.inv(incidence@incidence.T)@incidence
  err=np.max(abs(G-g*P));eigs=np.linalg.eigvalsh(G);rank=int(np.sum(eigs>1e-8));assert rank==dim and err<1e-10
  stars=max(np.max(abs(sum(A[q] for q,e in enumerate(edges) if v in e)-(k-4)/2*np.eye(d))) for v in range(k));assert stars<1e-10
  ortherr=max(np.max(abs(S[a]@S[a+1]@S[a]-S[a+1]@S[a]@S[a+1])) for a in range(k-2));assert ortherr<1e-10
  rows.append({'m':m,'k':k,'irrep_dimension':d,'edge_count':N,'transverse_dimension':dim,'Gram_eigenvalue':g,'rank':rank,'Gram_projector_error':float(err),'star_identity_error':float(stars),'Coxeter_braid_error':float(ortherr),'trivial_transposition_component':t,'smallest_positive_numerical_eigenvalue':float(min(eigs[eigs>1e-8]))})
  print(rows[-1],flush=True)
 (HERE/'check_rectangles_v1.json').write_text(json.dumps(rows,indent=2)+'\n')
if __name__=='__main__':main()
