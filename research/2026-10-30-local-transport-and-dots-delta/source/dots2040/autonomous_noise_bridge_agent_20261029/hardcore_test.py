"""Checks the root's exact hard-core intertwining on overlap path x-y-z."""
import numpy as np
from functools import reduce
kron=lambda xs:reduce(np.kron,xs)
I2=np.eye(2);I3=np.eye(3);P0=np.diag([1,0,0]);X=np.array([[0,1],[1,0]])
K=[np.diag([1,np.sqrt(.7)]),np.array([[0,np.sqrt(.3)],[0,0]])]
U=np.array([[1,1],[1,-1]])/np.sqrt(2)
Kz=[U@a@U for a in K]
CNOT=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
Ks=[[np.kron(a,I2) for a in K],[CNOT,np.zeros((4,4))],[np.kron(I2,a) for a in Kz]]
neigh=[[1],[0,2],[1]]
sets=[(),(0,),(1,),(2,),(0,2)];nc=len(sets);dim=4*3**3
V=[]
for x in range(3):
    vx=np.zeros((dim,dim),complex)
    for s,a in enumerate(Ks[x],1):
        b=np.zeros((3,3));b[s,0]=1
        vx+=kron([a]+[b if j==x else I3 for j in range(3)])
    V.append(vx)
W=np.zeros((dim,4*nc),complex)
for i in range(4):
 for j,S in enumerate(sets):
    v=kron([np.eye(4)[:,i]]+[np.array([1,0,0])]*3)
    for x in S:v=V[x]@v
    W[:,i*nc+j]=v
H=np.zeros((dim,dim),complex);Hc=np.zeros((nc,nc))
for x in range(3):
    proj=kron([np.eye(4)]+[P0 if j in neigh[x] else I3 for j in range(3)])
    H+=(V[x]+V[x].conj().T)@proj
    for j,S in enumerate(sets):
        Snew=tuple(sorted(set(S)^{x}))
        if Snew in sets:Hc[sets.index(Snew),j]+=1
res={'isometry':np.linalg.norm(W.conj().T@W-np.eye(4*nc)),
     'H_intertwiner':np.linalg.norm(H@W-W@np.kron(np.eye(4),Hc))}
for x in range(3):
    b=np.zeros((nc,nc))
    for j,S in enumerate(sets):
        if x in S:b[sets.index(tuple(y for y in S if y!=x)),j]=1
    for s,a in enumerate(Ks[x],1):
        aa=np.zeros((3,3));aa[0,s]=1
        L=kron([np.eye(4)]+[aa if j==x else I3 for j in range(3)])
        res[f'jump_{x}_{s}']=np.linalg.norm(L@W-W@np.kron(a,b))
for v in res.values():assert v<1e-12
print(res)
