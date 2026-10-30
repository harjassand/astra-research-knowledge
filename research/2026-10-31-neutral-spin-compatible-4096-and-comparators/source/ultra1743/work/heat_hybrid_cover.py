"""Stable numerical guide for a hybrid 6/7-dimensional heat certificate.

Six-dimensional physical Schur matrices away from the root; a seven-
dimensional blow-up at the root. All coordinates are centered exactly
at the acoustic value before conversion to floating point. Subdivision
uses convex de Casteljau averaging. This is not an exact receiver.
"""
from pathlib import Path
from fractions import Fraction as R
from math import comb
import time,json
import numpy as np, scipy.linalg as la
root=Path(__file__).resolve().parents[1];start=time.perf_counter();src=json.loads((root/'outputs/hopf_structure/certificate.json').read_text());e0,f0=map(lambda x:float(R(x)),src['ray']['canonical_zero']);data=np.load(root/'work/heat_centered_float.npz');LP=data['charts'][:,:,:,:7,:7,:];PP=data['physical_charts']
def weights(a,b,n):return np.array([[sum(comb(k,j)*a**(k-j)*(b-a)**j*comb(i,j)/comb(n,j) for j in range(min(i,k)+1)) for k in range(n+1)] for i in range(n+1)])
def coefficients(P,box):
 ds=tuple(x-1 for x in P.shape[2:]);shift=[e0,f0,0.];W=[weights(float(box[2*k])-shift[k],float(box[2*k+1])-shift[k],ds[k]) for k in range(3)]
 return np.einsum('xa,yb,zc,ijabc->xyzij',*W,P,optimize=True)
def midpoint(B):
 ds=[s-1 for s in B.shape[:3]];W=[np.array([comb(n,k)/2**n for k in range(n+1)]) for n in ds]
 return np.einsum('a,b,c,abcij->ij',*W,B,optimize=True)
def divide(B,k):
 C=np.moveaxis(B,k,0);n=len(C)-1;left=np.empty_like(C);right=np.empty_like(C);left[0]=C[0];right[n]=C[n]
 for j in range(1,n+1):C=(C[:-1]+C[1:])/2;left[j]=C[0];right[n-j]=C[-1]
 return np.moveaxis(left,0,k),np.moveaxis(right,0,k)
queue=[];eexact,fexact=map(R,src['ray']['canonical_zero']);dd=2**26;er=R((eexact*dd).__floor__(),dd);fr=R((fexact*dd).__floor__(),dd);small=(er-R(1,dd),er+R(2,dd),fr-R(1,dd),fr+R(2,dd))
for ch in range(4):
 for leaf in src['cover']['leaves']:
  raw=tuple(map(R,leaf['box']));subboxes=[(raw,6)]
  if leaf['proof']=='M':
   subboxes=[];xx=(raw[0],small[0],small[1],raw[1]);yy=(raw[2],small[2],small[3],raw[3])
   for i in range(3):
    for j in range(3):subboxes.append(((xx[i],xx[i+1],yy[j],yy[j+1]),7 if i==j==1 else 6))
  for bb,kind in subboxes:
   box=bb+(R(-1),R(1));P=LP[ch] if kind==7 else PP[ch];queue.append((ch,kind,box,coefficients(P,box),0))
leaves=[];splits=0;last=start;depthmax=0;bychart=[0]*4;minev=1.
while queue:
 ch,kind,box,B,depth=queue.pop();A=midpoint(B);A=(A+A.T)/2
 try:C=la.cholesky(A,lower=True)
 except la.LinAlgError:raise RuntimeError(('nonpositive physical centre',ch,kind,list(map(str,box)),la.eigvalsh(A).tolist()))
 W=la.solve_triangular(C,np.eye(kind),lower=True);PB=W@B@W.T;PB=(PB+PB.swapaxes(-1,-2))/2;mn=float(np.min(np.linalg.eigvalsh(PB)));depthmax=max(depthmax,depth)
 if mn>.001:
  leaves.append({'chart':ch,'dimension':kind,'box':list(map(str,box))});bychart[ch]+=1;minev=min(minev,mn)
 else:
  change=[float(np.max(np.linalg.norm(np.diff(PB,axis=k),axis=(-2,-1)))) for k in range(3)];k=int(np.argmax(change));b1=list(box);b2=list(box);mid=(box[2*k]+box[2*k+1])/2;b1[2*k+1]=mid;b2[2*k]=mid;B1,B2=divide(B,k);queue.extend(((ch,kind,tuple(b1),B1,depth+1),(ch,kind,tuple(b2),B2,depth+1)));splits+=1
  if depth>50:raise RuntimeError(('subdivision stalled',ch,kind,list(map(str,box)),mn,change))
 if time.perf_counter()-last>15:
  print(json.dumps({'leaves':len(leaves),'pending':len(queue),'by_chart':bychart,'max_added_depth':depthmax,'min_normalized_coefficient':minev,'seconds':time.perf_counter()-start}),flush=True);last=time.perf_counter()
 if len(leaves)>100000:raise RuntimeError('cover size limit; no positivity claim')
out={'scope':'NUMERICAL COVER PROPOSAL ONLY. All coefficient signs require rigorous reception.','leaves':leaves,'splits':splits,'minimum_numerical_normalized_coefficient':minev,'maximum_added_depth':depthmax,'seconds':time.perf_counter()-start};(root/'work/heat_hybrid_cover_proposal.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='leaves'}|{'leaf_count':len(leaves),'by_chart':bychart}),flush=True)
