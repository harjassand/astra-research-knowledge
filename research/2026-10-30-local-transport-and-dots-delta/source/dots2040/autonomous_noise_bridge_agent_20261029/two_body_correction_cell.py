"""Exact 3-bit recovery: two-body hub/data Hamiltonian, hub-only resets."""
import numpy as np
from functools import reduce
kron=lambda xs:reduce(np.kron,xs)
I=np.eye(2);X=np.array([[0,1],[1,0]]);Z=np.diag([1,-1])
# Logical register order: data d1,d2,d3, syndrome s1,s2. Clock is final factor.
U=[]
for data,synd in [(0,3),(1,3),(1,4),(2,4)]:
    op=np.zeros((32,32))
    for j in range(32):
        bits=[(j>>(4-k))&1 for k in range(5)];out=bits.copy()
        out[synd]^=bits[data]
        k=sum(b<<(4-p) for p,b in enumerate(out));op[k,j]=1
    U.append(op)
for data,syn in [(0,(1,0)),(1,(1,1)),(2,(0,1))]:
    op=np.zeros((32,32))
    for j in range(32):
        bits=[(j>>(4-k))&1 for k in range(5)];out=bits.copy()
        if tuple(bits[3:])==syn:out[data]^=1
        k=sum(b<<(4-p) for p,b in enumerate(out));op[k,j]=1
    U.append(op)
# Each U affects hub syndrome and only one data qubit: explicit construction above.
E=np.kron(np.eye(8),np.array([[1],[0],[0],[0]]));Vs=[E]
for op in U:Vs.append(op@Vs[-1])
W=np.zeros((256,64))
for d in range(8):
 for t in range(8):W[:,d*8+t]=np.kron(Vs[t][:,d],np.eye(8)[:,t])
H=np.zeros((256,256));Hc=np.zeros((8,8))
for t,op in enumerate(U):
    b=np.zeros((8,8));b[t+1,t]=1
    H+=np.kron(op,b)+np.kron(op.T,b.T)
    Hc+=b+b.T
res={'isometry':float(np.linalg.norm(W.T@W-np.eye(64))),
     'H_intertwiner':float(np.linalg.norm(H@W-W@np.kron(np.eye(8),Hc)))}
Ks=[]
for s in range(4):
    K=Vs[-1].reshape(8,4,8)[:,s,:];Ks.append(K)
    jump_hub=np.zeros((32,32));jump_hub[0,s*8+7]=1
    L=np.kron(np.eye(8),jump_hub)
    bc=np.zeros((8,8));bc[0,7]=1
    res[f'jump_{s}']=float(np.linalg.norm(L@W-W@np.kron(K,bc)))
res['TP']=float(np.linalg.norm(sum(K.T@K for K in Ks)-np.eye(8)))
enc=np.zeros((8,2));enc[0,0]=1;enc[7,1]=1
rho=np.array([[.4,.2+.1j],[.2-.1j,.6]])
ideal=enc@rho@enc.T
for j in [-1,0,1,2]:
    err=kron([X if k==j else I for k in range(3)])
    recovered=sum(K@err@ideal@err.T@K.T for K in Ks)
    res[f'correction_X{j}']=float(np.linalg.norm(recovered-ideal))
assert max(res.values())<1e-12
print(res)
