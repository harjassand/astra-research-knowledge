import numpy as np
from scipy.linalg import eigh
P=np.array([[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex)
I=np.eye(2)
v=np.array([0,1,-1,0])/np.sqrt(2)
S=np.outer(v,v)
rng=np.random.default_rng(89203)
def pt(x): return x.reshape(2,2,2,2).transpose(0,3,2,1).reshape(4,4)
examples=[]
for i in range(3000):
    z=rng.normal(size=(8,2))+1j*rng.normal(size=(8,2)); q=np.linalg.qr(z)[0]; kraus=q.reshape(4,2,2)
    def ch(x): return sum(a@x@a.conj().T for a in kraus)
    c=np.array([np.trace(p@ch(I/2)).real for p in P]); T=np.array([[np.trace(p@ch(q)).real/2 for q in P] for p in P])
    tau=sum(np.kron(a,b)@S@np.kron(a,b).conj().T for a in kraus for b in kraus)
    e=np.linalg.eigvalsh(pt(tau)).min(); score=np.sum(c*c)+np.sum(T*T)
    if e < -1e-8 and score<=1: examples.append((score,e,c.tolist(),T.tolist()))
print('missed_entangled_count',len(examples))
print(examples[:2])
