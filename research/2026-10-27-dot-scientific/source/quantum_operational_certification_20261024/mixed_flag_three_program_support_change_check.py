"""S4 Schur-block test of label difference and conditional (program-average) baseline."""
import itertools,numpy as np
n=3;m=n+1;perms=list(itertools.permutations(range(m)));idx={p:i for i,p in enumerate(perms)};N=len(perms)
def comp(p,q):return tuple(p[q[i]] for i in range(m))
def inverse(p):return tuple(np.argsort(p))
def lengths(p):
 seen=set();out=[]
 for i in range(m):
  if i not in seen:
   j=i;k=0
   while j not in seen:seen.add(j);k+=1;j=p[j]
   out.append(k)
 return tuple(sorted(out,reverse=True))
classes=[(1,1,1,1),(2,1,1),(2,2),(3,1),(4,)]
characters=[[1,1,1,1,1],[3,1,-1,0,-1],[2,0,2,-1,0],[3,-1,-1,0,1],[1,-1,1,1,-1]]
regs=[]
for p in perms:
 R=np.zeros((N,N))
 for j,q in enumerate(perms):R[idx[comp(p,q)],j]=1
 regs.append(R)
reps=[];fdims=[]
for ch in characters:
 f=ch[0];central=sum(ch[classes.index(lengths(p))]*R for p,R in zip(perms,regs))*f/N
 ev,U=np.linalg.eigh(central);basis=U[:,ev>.5];assert basis.shape[1]==f*f
 reps.append([basis.T@R@basis for R in regs]);fdims.append(f)
base={}
for a in range(3):
 xs=[]
 for p in perms:
  X=np.zeros((3**n,3**n))
  for row in itertools.product(range(3),repeat=n):
   full=row+(a,);cols=tuple(full[p[i]] for i in range(m))
   if cols[-1]!=a:continue
   ii=sum(row[i]*3**(n-1-i) for i in range(n));jj=sum(cols[i]*3**(n-1-i) for i in range(n))
   X[ii,jj]=1/3**n
  xs.append(X)
 base[a]=xs
for r in [1]:
 d=3*r;G=np.array([[float(d)**len(lengths(comp(inverse(p),q))) for q in perms] for p in perms])
 coeff={}
 for a in range(3):
  xs=np.array([base[a][i]*float(r)**(len(lengths(p))-m) for i,p in enumerate(perms)])
  coeff[a]=(np.linalg.pinv(G,hermitian=True,rcond=1e-10)@xs.reshape(N,-1)).reshape(N,3**n,3**n)
 mults=[d*(d+1)*(d+2)*(d+3)/24,d*(d-1)*(d+1)*(d+2)/8,d*d*(d*d-1)/12,d*(d-1)*(d-2)*(d+1)/8,d*(d-1)*(d-2)*(d-3)/24]
 td=0;chi=0;tr=0
 for rep,f,mult in zip(reps,fdims,mults):
  blocks=[sum(np.kron(coeff[a][i],rep[i]) for i in range(N)) for a in range(3)]
  for block in blocks:assert np.linalg.norm(block-block.T)<1e-10
  diff=blocks[0]-blocks[1];baseline=sum(blocks)/3
  vals=np.linalg.eigvalsh(baseline);assert vals.min()>-1e-12
  weight=mult/f;tr+=weight*np.trace(blocks[0]);td+=weight*np.abs(np.linalg.eigvalsh(diff)).sum()/2
  chi+=weight*np.trace(diff@np.linalg.pinv(baseline,hermitian=True,rcond=1e-10)@diff)
 assert abs(tr-1)<1e-9
 print(f'r={r:3d} half_distance={td:.12g} r_times_distance={r*td:.12g} conditional_chi={chi:.12g} chi_r2={chi*r*r:.12g} linear_candidate={6*n/(9*r*r-1):.12g}',flush=True)
