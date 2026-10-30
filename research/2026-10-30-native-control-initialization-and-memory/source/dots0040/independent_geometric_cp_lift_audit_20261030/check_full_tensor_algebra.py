import numpy as np,json
from scipy.linalg import sqrtm
n=3;edges=[(0,1),(0,2)];dim=2**n;dc=3
I2=np.eye(2);a=np.array([[0,1],[0,0]],complex);nn=a.conj().T@a
embed=lambda A,j: np.kron(np.kron(np.eye(2**j),A),np.eye(2**(n-j-1)))
aa=[embed(a,j) for j in range(n)];ns=[embed(nn,j) for j in range(n)];Ic=np.eye(dim,dtype=complex);Id=np.eye(dc);I=np.eye(dim*dc)
neigh=[[] for _ in range(n)]
for i,j in edges:neigh[i].append(j);neigh[j].append(i)
G=[];ms=[]
for h in range(n):
 g=Ic.copy();m=np.zeros_like(Ic)
 for j in neigh[h]:g=g@(Ic-ns[j]);m+=ns[j]
 G.append(g);ms.append(m)
Y=[1j*(aa[h]-aa[h].conj().T) for h in range(n)]
nu=.01;t=.0001;f0=5.;r=.1
fms=[np.diag(f0*r**np.diag(m)) for m in ms]
Bs=[ns[h]+2*nu*G[h]@Y[h]+nu**2*fms[h] for h in range(n)]
roots=[np.asarray(sqrtm(B),dtype=complex) for B in Bs]
H0=sum(G[h]@(aa[h]+aa[h].conj().T) for h in range(n));H=nu*np.kron(H0,Id)
# Three fully CPTP idempotent classical maps; h:2->1, j:1->0, third dephasing.
maps=[[0,1,1],[0,0,2],[0,1,2]];Ks=[]
for mp in maps:
 ks=[]
 for s,u in enumerate(mp):
  K=np.zeros((dc,dc),complex);K[u,s]=1;ks.append(K)
 Ks.append(ks)
Phi=lambda h,O:sum(K.conj().T@O@K for K in Ks[h])
Vd=np.diag([1.,2.,3.]);V=np.kron(Ic,Vd);ds=[Vd-Phi(h,Vd) for h in range(n)]
jumps=[[np.kron(aa[h],K) for K in Ks[h]] for h in range(n)]
def dis(J,O):
 Q=J.conj().T@J
 return J.conj().T@O@J-(Q@O+O@Q)/2
def LC(B):return 1j*nu*(H0@B-B@H0)+sum(dis(x,B) for x in aa)
def LL(O):return 1j*(H@O-O@H)+sum(dis(J,O) for jj in jumps for J in jj)
def ZZ(h,O):return sum(dis(np.kron(roots[h],K),O) for K in Ks[h])
err=[];comms=[]
for h in range(n):
 comm=LL(ZZ(h,V))-ZZ(h,LL(V));comms.append(comm)
 rhs=-np.kron(LC(Bs[h]),ds[h])
 for j in range(n):
  rhs-=np.kron(aa[j].conj().T@Bs[h]@aa[j],Phi(j,ds[h])-ds[h])
  rhs+=np.kron(roots[h]@ns[j]@roots[h],Phi(h,ds[j])-ds[j])
  rhs+=np.kron(dis(roots[h],ns[j]),ds[j])
 err.append(float(np.linalg.norm(comm-rhs,2)))
first=LL(V)+t*sum(comms);baseline=sum(np.kron(ns[h],ds[h]) for h in range(n));D=sum(np.kron(Ic,d) for d in ds)
qmin=.45;c=qmin/16
res=first+.5*baseline+c*t*nu**2*D
# zero-drift data level0 yields exact zero eigenvalues; check maximum.
out={'commutator_identity_norm_errors':err,'B_min_eigenvalues':[float(np.linalg.eigvalsh(B).min()) for B in Bs],'first_order_drift_upper_residual_maxeig':float(np.linalg.eigvalsh((res+res.conj().T)/2).max()),'nu':nu,'t':t,'c_test':c,'model':'full three-clock star tensor product; direct fresh idempotent CPTP reset maps'}
assert max(err)<1e-10
assert min(out['B_min_eigenvalues'])>0
assert out['first_order_drift_upper_residual_maxeig']<1e-10
print(json.dumps(out,indent=2))
