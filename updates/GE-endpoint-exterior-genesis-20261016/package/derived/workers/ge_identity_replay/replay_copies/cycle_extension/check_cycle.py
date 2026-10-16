import itertools,json
from pathlib import Path
import numpy as np
from scipy.linalg import expm

def pair_matrix(n,edges,weights):
 pairs=list(itertools.combinations(range(n),2));ix={p:i for i,p in enumerate(pairs)}
 W=np.zeros((n,n),dtype=np.int64)
 for (x,y),w in zip(edges,weights):W[x,y]=W[y,x]=w
 H=np.zeros((len(pairs),len(pairs)),dtype=np.int64)
 for j,(x,y) in enumerate(pairs):
  H[j,j]=2*W[x,y]
  for a,b in [(x,y),(y,x)]:
   for z in range(n):
    if z not in (a,b):H[j,j]+=W[a,z];H[j,ix[tuple(sorted((z,b)))]]-=W[a,z]
 return H,pairs

def wedge_generator(A,pairs):
 ix={p:i for i,p in enumerate(pairs)};B=np.zeros((len(pairs),len(pairs)),dtype=np.int64)
 for j,(x,y) in enumerate(pairs):
  for z in range(len(A)):
   if z!=y:
    k=tuple(sorted((z,y)));B[ix[k],j]+=int(A[z,x])*(1 if z<y else -1)
   if z!=x:
    k=tuple(sorted((x,z)));B[ix[k],j]+=int(A[z,y])*(1 if x<z else -1)
 return B

def lap(n,edges,weights,twist=None):
 L=np.zeros((n,n),dtype=np.int64)
 for e,((x,y),w) in enumerate(zip(edges,weights)):
  L[x,x]+=w;L[y,y]+=w;v=w if e==twist else -w;L[x,y]=L[y,x]=v
 return L

rows=[]
for n in range(3,13):
 w=[1+((7*i+3*n)%13) for i in range(n)];ed=[(i,(i+1)%n) for i in range(n)]
 H,ps=pair_matrix(n,ed,w);A=lap(n,ed,w,n-1)
 assert np.array_equal(H,wedge_generator(A,ps))
 cover=lap(2*n,[(i,(i+1)%(2*n)) for i in range(2*n)],w+w)
 # Exact integer intertwiner, no square roots needed.
 T=np.vstack((np.eye(n,dtype=np.int64),-np.eye(n,dtype=np.int64)))
 assert np.array_equal(cover@T,T@A)
 for t in [.001,.07,.5]:
  P=expm(-t*A);C=expm(-t*cover);S=expm(-t*H).sum(axis=1)
  err=np.max(abs(P-(C[:n,:n]-C[:n,n:])))
  K=np.sign(np.arange(n)[None,:]-np.arange(n)[:,None])
  pred=np.array([P[x]@K@P[y] for x,y in ps]);er=float(np.max(abs(pred-S)))
  assert max(err,er)<2e-12
  rows.append({'n':n,'t':t,'cover_error':float(err),'survival_error':er})
# A six-step physical-pair loop on the branching star exchanges the two walkers.
# Every one-particle edge is traversed twice, so any tree edge gauge cancels;
# exterior reordering signs have product -1.
loop=[(1,2),(0,2),(2,3),(0,3),(1,3),(0,1),(1,2)]
A=lap(4,[(0,1),(0,2),(0,3)],[1,1,1]);H,ps=pair_matrix(4,[(0,1),(0,2),(0,3)],[1,1,1]);B=wedge_generator(A,ps);ix={p:i for i,p in enumerate(ps)}
prod=1
for p,q in zip(loop,loop[1:]):
 assert H[ix[p],ix[q]]==-1
 prod*=int(B[ix[p],ix[q]]/H[ix[p],ix[q]])
assert prod==-1
out={'integer_wedge_and_cover_identities':'PASS for cycles n3..12','heat_checks':rows,'star_loop':loop,'relative_sign_product':prod,'scope':'cycle identity proved by ordered-basis signs; finite checks diagnostic; branching loop defeats fixed one-particle edge gauge on this tree, not every possible algorithm'}
p=Path(__file__).parent/'checks.json';p.write_text(json.dumps(out,indent=2));print('PASS',len(rows),'heat checks; exact star sign product',prod)
