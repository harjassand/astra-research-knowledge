import numpy as np,json,itertools
p=7;m=4;d=1
# Full degree<m Vandermonde is an explicit invertible extension.
A=np.array([[pow(i+1,j,p) for j in range(m)] for i in range(m)],dtype=int)
R=A.copy();rank=0
for c in range(m):
 piv=next((j for j in range(rank,m) if R[j,c]%p),None)
 if piv is None:continue
 R[[rank,piv]]=R[[piv,rank]];R[rank]=(R[rank]*pow(int(R[rank,c]),-1,p))%p
 for j in range(m):
  if j!=rank:R[j]=(R[j]-R[j,c]*R[rank])%p
 rank+=1
assert rank==m
seen=set()
for coeff in itertools.product(range(p),repeat=m):
 y=tuple((A@coeff)%p);assert y not in seen;seen.add(y)
# Equal superposition over degree-one coefficient is orthonormal over logical a.
enc=np.zeros((p**m,p),complex)
for a in range(p):
 for b in range(p):
  y=(A@np.array([a,b,0,0]))%p;idx=sum(int(y[j])*p**j for j in range(m));enc[idx,a]=p**-.5
res=np.linalg.norm(enc.conj().T@enc-np.eye(p))
# Entangled embedded qubit transfer; order reference,Q,b.
v=np.zeros((2,p,2),complex);v[0,0,0]=2**-.5;v[1,1,0]=2**-.5
w=v.copy();w[:,1,0]=v[:,0,1];w[:,0,1]=v[:,1,0]
t=np.zeros_like(v);t[0,0,0]=2**-.5;t[1,0,1]=2**-.5
transfer=np.linalg.norm(w-t)
assert res<1e-12 and transfer==0
print(json.dumps(dict(result='PASS',field=p,length=m,degree=d,vandermonde_rank=rank,permutation_cases=len(seen),encoding_isometry_residual=float(res),entangled_transfer_residual=float(transfer),scope='exact finite algebra; no noisy gadget/synthesis theorem'),indent=2))
