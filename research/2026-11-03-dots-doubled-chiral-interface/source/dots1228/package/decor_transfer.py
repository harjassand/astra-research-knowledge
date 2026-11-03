import numpy as np
from functools import reduce
D='producer-workspace/chiral_hamiltonian_interface_20261102'
z=np.load(D+'matching.npz',allow_pickle=True);sg={tuple(e):s for e,s in zip(z['edges'],z['signs'])}
verts=[8,9,11,12,13,14,16,17];idx={v:i for i,v in enumerate(verts)}
pa=[(8,17),(9,11),(12,16),(13,14)];pb=[(8,11),(9,13),(12,14),(16,17)]
I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);kron=lambda a:reduce(np.kron,a)
gam=[kron([Z]*(j//2)+([X] if j%2==0 else [Y])+[I]*(3-j//2)) for j in range(8)]
def terms(p):return [1j*sg[e]*gam[idx[e[0]]]@gam[idx[e[1]]] for e in p]
def proj(p):return reduce(np.matmul,[(np.eye(16)+b)/2 for b in terms(p)])
P,Q=proj(pa),proj(pb);ea,va=np.linalg.eigh(-sum(terms(pa)));eb,vb=np.linalg.eigh(-sum(terms(pb)));a=va[:,0];b=vb[:,0]
print('decoration full spectra',ea,eb)
for i,v in enumerate(verts):
 t=Q@gam[i]@P
 print(v,'amplitude',np.vdot(b,t@a),'rank',np.linalg.matrix_rank(t),'norm',np.linalg.norm(t,2))
print('P Q overlap',np.linalg.norm(P@Q));print('projector eig',np.linalg.eigvalsh(P))
np.savez(D+'decor_transfer.npz',P=P,Q=Q,gamma=gam,ea=ea,eb=eb)
