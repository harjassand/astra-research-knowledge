"""Exact S3-Weingarten reduction of the two-Choi-program Haar experiment; finite-matrix diagnostic."""
import itertools,numpy as np
perms=list(itertools.permutations(range(3)))
def pmatrix(p,d):
 out=np.zeros((d**3,d**3))
 for x in itertools.product(range(d),repeat=3):
  y=[0]*3
  for i in range(3):y[p[i]]=x[i]
  a=sum(x[i]*d**(2-i) for i in range(3));b=sum(y[i]*d**(2-i) for i in range(3));out[b,a]=1
 return out
def cyc(p):
 seen=set();c=0
 for i in range(3):
  if i not in seen:
   c+=1;j=i
   while j not in seen:seen.add(j);j=p[j]
 return c
Ps=[pmatrix(p,3) for p in perms]
R3=[]
for p in perms:
 R=np.zeros((3,3))
 for i in range(3):R[p[i],i]=1
 R3.append(R)
B=np.column_stack([np.array([1,-1,0])/np.sqrt(2),np.array([1,1,-2])/np.sqrt(6)])
reps=[[np.ones((1,1)) for p in perms],[np.array([[round(np.linalg.det(R))]]) for R in R3],[B.T@R@B for R in R3]]
base={}
for a in [0,1,2]:
 P=np.zeros((3,3));P[a,a]=1;xs=[]
 for pp in Ps:
  X=np.zeros((9,9))
  for i,j,k,l in itertools.product(range(3),repeat=4):
   M=np.zeros((3,3));M[i,j]=1;N=np.zeros((3,3));N[k,l]=1
   X[3*i+k,3*j+l]=np.trace(np.kron(np.kron(M,N),P)@pp.T)/9
  xs.append(X)
 base[a]=xs
for r in [2,3,5,10,30,100]:
 d=3*r;G=np.zeros((6,6))
 for i,p in enumerate(perms):
  inv=np.argsort(p)
  for j,q in enumerate(perms):G[i,j]=float(d)**cyc(tuple(inv[q[k]] for k in range(3)))
 coeff={}
 for a in [0,1,2]:
  xs=np.array([base[a][i]*float(r)**(cyc(p)-3) for i,p in enumerate(perms)])
  coeff[a]=np.linalg.solve(G,xs.reshape(6,-1)).reshape(6,9,9)
 mults=[d*(d+1)*(d+2)/6,d*(d-1)*(d-2)/6,d*(d*d-1)/3]
 td=0;tr=0;chi=0
 for rep,mult in zip(reps,mults):
  blocks=[sum(np.kron(coeff[a][i],rep[i]) for i in range(6)) for a in [0,1,2]]
  for block in blocks:assert np.linalg.eigvalsh((block+block.T)/2).min()>-1e-12
  tr+=mult*np.trace(blocks[0]);diff=blocks[0]-blocks[1];td+=mult*np.abs(np.linalg.eigvalsh(diff)).sum()/2
  baseline=sum(blocks)/3; chi+=mult*np.trace(diff@np.linalg.pinv(baseline,hermitian=True)@diff)
 assert abs(tr-1)<1e-10
 assert td<=1-(1-1/r)**2+1e-10
 print(f'r={r:3d} two_program_half_distance={td:.12g} r_times_distance={r*td:.12g} conditional_chi_r2={chi*r*r:.12g}')
