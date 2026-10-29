"""Explicit 29-gate autonomous full quantum recovery circuit for [[5,1,3]].
Hub=4 syndrome bits x 30 clock positions=480 levels; every gate touches hub
alone or hub + one external data qubit. Dense full Hamiltonian not needed.
"""
import numpy as np
from functools import reduce
kron=lambda xs:reduce(np.kron,xs)
I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);H=(X+Z)/np.sqrt(2)
paulis={'I':I,'X':X,'Y':Y,'Z':Z}
strings=['XZZXI','IXZZX','XIXZZ','ZXIXZ'];Gs=[kron([paulis[x] for x in s]) for s in strings]
proj=reduce(lambda a,g:a@(np.eye(32)+g)/2,Gs,np.eye(32))
eig,vec=np.linalg.eigh(proj);enc=vec[:,eig>.5]
assert enc.shape==(32,2)
errors=[np.eye(32)];syndromes=[0];recover={0:np.eye(32)}
for q in range(5):
 for P in [X,Y,Z]:
    E=kron([P if j==q else I for j in range(5)])
    bits=[int(np.linalg.norm(E@G-G@E)>1e-8) for G in Gs]
    s=sum(b<<(3-j) for j,b in enumerate(bits))
    assert s not in recover
    recover[s]=E;errors.append(E);syndromes.append(s)
V=np.kron(np.eye(32),np.eye(16)[:,0:1]);Vhist=[V];gates=[]
for j,string in enumerate(strings):
    Hj=kron([H if k==j else I for k in range(4)])
    op=np.kron(np.eye(32),Hj);V=op@V;Vhist.append(V);gates.append(('hub_H',j))
    ctrl=kron([np.diag([0,1]) if k==j else I for k in range(4)])
    for q,p in enumerate(string):
        if p=='I':continue
        Pd=kron([paulis[p] if k==q else I for k in range(5)])
        op=np.kron(np.eye(32),np.eye(16)-ctrl)+np.kron(Pd,ctrl)
        V=op@V;Vhist.append(V);gates.append(('controlled_'+p,q,j))
    op=np.kron(np.eye(32),Hj);V=op@V;Vhist.append(V);gates.append(('hub_H',j))
# One controller-conditioned Pauli update per external data qubit.
for q in range(5):
    op=np.zeros((512,512),complex)
    for s,E in recover.items():
        # Recover matrix is a single-qubit Pauli or I; select its factor on q
        Pq=I
        if s:
            for P in [X,Y,Z]:
                candidate=kron([P if j==q else I for j in range(5)])
                if np.linalg.norm(E-candidate)<1e-8:Pq=P
        Ed=kron([Pq if j==q else I for j in range(5)])
        diag=np.zeros((16,16));diag[s,s]=1
        op+=np.kron(Ed,diag)
    V=op@V;Vhist.append(V);gates.append(('syndrome_conditioned_Pauli',q))
Ks=[V.reshape(32,16,32)[:,s,:] for s in range(16)]
res={'stages':len(gates),'hub_dimension':16*len(Vhist),
     'max_history_isometry_error':max(float(np.linalg.norm(W.conj().T@W-np.eye(32))) for W in Vhist),
     'TP_error':float(np.linalg.norm(sum(K.conj().T@K for K in Ks)-np.eye(32)))}
errs=[]
for E,s in zip(errors,syndromes):
 for t,K in enumerate(Ks):
    errs.append(np.linalg.norm(K@E@enc-(enc if s==t else 0)))
res['max_single_Pauli_correction_error']=float(max(errs))
assert len(gates)==29 and max(res[k] for k in res if 'error' in k)<1e-12
print(res)
