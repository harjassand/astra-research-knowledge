import os
os.environ['OPENBLAS_NUM_THREADS']='2'
import numpy as np,itertools,scipy.linalg as la,json
D='producer-workspace/chiral_hamiltonian_interface_20261102'
N=3; coords=list(itertools.product(range(N),repeat=3));ix={x:i for i,x in enumerate(coords)}
def site(x):return ix[tuple(t%N for t in x)]
T=[]
for x in coords:
 for perm in itertools.permutations(range(3)):
  vs=[site(x)];y=list(x)
  for k in perm:y[k]+=1;vs.append(site(y))
  s=(-1)**sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))
  s*=(-1)**sum(vs[i]>vs[j] for i in range(4) for j in range(i+1,4))
  T.append((tuple(sorted(vs)),s))
edges=sorted({e for t,s in T for e in itertools.combinations(t,2)});faces=sorted({f for t,s in T for f in itertools.combinations(t,3)})
def data(phi):
 m={e:int(np.floor(phi[e[1]]-phi[e[0]]+.5)) for e in edges}
 n={(a,b,c):m[b,c]-m[a,c]+m[a,b] for a,b,c in faces}
 q=sum(s*m[a,b]*n[b,c,d] for (a,b,c,d),s in T)
 return q,m,n
rng=np.random.default_rng(18)
for attempt in range(10000):
 p=rng.random(27);v=0;neighbors=[b if a==v else a for a,b in edges if v in (a,b)]
 for nb in neighbors:
  threshold=(p[nb]+.5)%1
  pa=p.copy();pb=p.copy();pa[v]=threshold-1e-5;pb[v]=threshold+1e-5
  if not (0<pa[v]<pb[v]<1):continue
  qa,ma,na=data(pa);qb,mb,nbb=data(pb)
  if abs(qb-qa)==1:break
 else:continue
 break
print('move',qa,qb,'changed m',[(e,ma[e],mb[e]) for e in edges if ma[e]!=mb[e]],flush=True)
np.savez(D+'cubic_move.npz',phi_a=pa,phi_b=pb,q_a=qa,q_b=qb,T=np.array(T,dtype=object))
I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);G=[np.kron(X,X),np.kron(X,Y),np.kron(X,Z),np.kron(Y,I),np.kron(Z,I)]
def slab(L,m=-1):
 n=27*L*4;h=np.zeros((n,n),complex)
 for w in range(L):
  for x in coords:
   j=(w*27+site(x))*4;h[j:j+4,j:j+4]=(m+4)*G[4]
   for d in range(4):
    if d==3:
     if w+1==L:continue
     k=((w+1)*27+site(x))*4
    else:
     y=list(x);y[d]+=1;k=(w*27+site(y))*4
    hop=-.5*G[4]+G[d]/(2j)
    h[j:j+4,k:k+4]+=hop;h[k:k+4,j:j+4]+=hop.conj().T
 return h

def full(h,L,phi,M,lam):
 n=len(h);H=la.block_diag(h,h,-h,-h);z=np.exp(2j*np.pi*phi)
 for x in coords:
  i=site(x);y=list(x);y[0]+=1;ym=list(x);ym[0]-=1;u=list(x);u[1]+=1;um=list(x);um[1]-=1
  b=lam*(z[site(y)]-z[site(ym)]+1j*(z[site(u)]-z[site(um)]))
  U=np.array([[z[i],b],[-b.conjugate(),z[i].conjugate()]])/np.sqrt(1+abs(b)**2)
  j=i*4
  for a in range(2):
   for b in range(2):
    sl=slice(a*n+j,a*n+j+4);sr=slice((b+2)*n+j,(b+2)*n+j+4)
    H[sl,sr]=M*U[a,b]*np.eye(4);H[sr,sl]=M*U[a,b].conjugate()*np.eye(4)
 return H
out=[]
for L in [3,5]:
 h=slab(L)
 for M in [.5,2,8]:
  for lam in [0,.4]:
   vals=[]
   for p in [pa,pb]:
    H=full(h,L,p,M,lam);e=la.eigvalsh(H,driver='evr');vals.append((int(sum(e<0)),float(min(abs(e)))))
   r={'L':L,'M':M,'lambda':lam,'A_occupancy_a':vals[0][0],'A_occupancy_b':vals[1][0],'min_abs_e_a':vals[0][1],'min_abs_e_b':vals[1][1]};out.append(r);print(r,flush=True)
json.dump(out,open(D+'wilson_endpoint_results.json','w'),indent=2)
