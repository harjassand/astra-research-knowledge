import numpy as np,json,itertools
p=5; m=4; alpha=np.arange(1,5)
def rankmod(A):
 A=np.array(A,dtype=int).copy()%p;r=0
 for j in range(A.shape[1]):
  ids=[i for i in range(r,len(A)) if A[i,j]%p]
  if not ids:continue
  i=ids[0];A[[i,r]]=A[[r,i]];A[r]=A[r]*pow(int(A[r,j]),-1,p)%p
  for k in range(len(A)):
   if k!=r:A[k]=(A[k]-A[k,j]*A[r])%p
  r+=1
 return r
cols=[np.ones(m,dtype=int),alpha]
for e in np.eye(m,dtype=int):
 if rankmod(np.stack(cols+[e],axis=1))>len(cols):cols.append(e)
 if len(cols)==m:break
L=np.stack(cols,axis=1);N=p**m
idx=lambda v:sum(int(v[i])*p**i for i in range(m))
E=np.zeros((N,N),complex);omega=np.exp(2j*np.pi/p)
for x in itertools.product(range(p),repeat=m):
 for b in range(p):
  y=list(x);y[1]=b
  E[idx(L@np.array(y)%p),idx(x)]+=omega**(b*x[1])/np.sqrt(p)
V=np.zeros((N,p),complex)
for a in range(p):
 for b in range(p):V[idx((a+b*alpha)%p),a]+=1/np.sqrt(p)
want=np.zeros((N,p),complex)
for a in range(p):want[a,a]=1
res=float(np.linalg.norm(E.conj().T@V-want,2))
# Physical W basis index 2*qudit+qubit.
W=np.eye(2*p);W[[2,1]]=W[[1,2]]
v=np.zeros((p,2,2),complex);v[0,0,0]=v[1,0,1]=1/np.sqrt(2)
out=(W@v.reshape(2*p,2)).reshape(p,2,2)
target=np.zeros_like(out);target[0,0,0]=target[0,1,1]=1/np.sqrt(2)
port=float(np.linalg.norm(out-target))
assert res<1e-12 and port<1e-12
print(json.dumps(dict(result='PASS',prime=p,degree=1,block_length=m,Vandermonde_rank=rankmod(L),inverse_quantum_encoder_residual=res,entangled_physical_qubit_transfer_residual=port,scope='exact finite encoder/port algebra, not noisy native factory'),indent=2))
