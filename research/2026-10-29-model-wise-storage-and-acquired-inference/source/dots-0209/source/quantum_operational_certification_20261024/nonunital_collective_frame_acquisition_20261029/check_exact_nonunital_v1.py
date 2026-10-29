import numpy as np,json
from scipy.linalg import expm,svd,eigh
from scipy.spatial.transform import Rotation
from functools import reduce
rng=np.random.default_rng(2026102910)
P=np.array([np.eye(2),[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex);kron=lambda xs:reduce(np.kron,xs)
n=4;D=2**n;O=Rotation.random(n,random_state=rng).as_matrix()
def su(R):return expm(-.5j*np.einsum('a,aij->ij',Rotation.from_matrix(R).as_rotvec(),P[1:]))
V=kron([su(R) for R in O]);lower=np.array([[0,1],[0,0]],complex);L=V@sum(kron([lower if i==j else P[0] for i in range(n)]) for j in range(n))@V.conj().T;A=L.conj().T@L
G=np.kron(L,L.conj())-.5*(np.kron(A,np.eye(D))+np.kron(np.eye(D),A.T));Nt=expm(.65*G)
Jembed=np.zeros((16,9))
for a in range(1,4):
 for b in range(1,4):Jembed[4*a+b,3*(a-1)+b-1]=1
Ts=[];rows=[]
for i in range(1,n):
 inops=[kron([P[a] if j==i else P[b] if j==0 else P[0] for j in range(n)]) for a in range(4) for b in range(4)]
 outops=[inops[4*a+b] for a in range(1,4) for b in range(1,4)]
 T=np.array([[np.vdot(X.reshape(-1),Nt.conj().T@Y.reshape(-1)).real/D for Y in outops] for X in inops]);M=T-Jembed;_,s,vt=np.linalg.svd(M);v=vt[-1];C=O[i]@O[0].T;align=min(np.linalg.norm(v-C.reshape(-1)/np.sqrt(3)),np.linalg.norm(v+C.reshape(-1)/np.sqrt(3)))
 assert np.linalg.norm(M@C.reshape(-1))<1e-12 and align<1e-10
 rows.append({'pair':[i,0],'singular_values':s.tolist(),'one_dimensional_kernel':int(sum(s<1e-10))==1,'true_kernel_residual':float(np.linalg.norm(M@C.reshape(-1))),'recovered_normalized_frame_error':float(align),'lower_degree_mixing_frobenius':float(np.linalg.norm(T[[0,1,2,3,4,8,12],:]))})
 Ts.append(T)
nonunital=np.linalg.norm((Nt@np.eye(D).reshape(-1)).reshape(D,D)-np.eye(D))
print(json.dumps({'seed':2026102910,'n':n,'generator':'locally conjugated collective lowering Lindblad generator','time':.65,'global_nonunitality_F_norm':float(nonunital),'pair_results':rows},indent=2))
# Export compact arrays for the physical finite-probe check, not a claimed acquired environment model.
if __name__=='__main__':
 np.savez(__file__.replace('.py','.npz'),channel=Nt,Ts=np.array(Ts),O=O,Jembed=Jembed)
