"""No-Kato-denominator charged Gaussian surgery, including exact +/-1 modes.
Algebra/local truncation test only, NOT a simulation of the enormous certified Wilson slab.
"""
import numpy as np,json
from scipy.linalg import eigh,expm
n=20;patch=12;rank=6
Pa=np.diag([1.]*rank+[0.]*(n-rank)).astype(complex)
angles=[np.pi/2,np.pi/2-1e-12,.7,.05,.0001]
Vb=np.zeros((n,5),complex)
for j,t in enumerate(angles):Vb[j,j]=np.cos(t);Vb[j+6,j]=np.sin(t)
Pb=Vb@Vb.conj().T
rng=np.random.default_rng(20261103)
# Generic basis change INSIDE the physical patch; no exterior dependency.
A=rng.normal(size=(patch,patch))+1j*rng.normal(size=(patch,patch));R,_=np.linalg.qr(A)
RR=np.eye(n,dtype=complex);RR[:patch,:patch]=R
Pa=RR@Pa@RR.conj().T;Pb=RR@Pb@RR.conj().T

def surgery(P,Q):
 M=(P-Q)[:patch,:patch];ev,evc=eigh(M);t=.01
 inside=sorted([float(abs(x)) for x in ev if t<abs(x)<2*t]);cuts=[t]+inside+[2*t]
 k=int(np.argmax(np.diff(cuts)));threshold=(cuts[k]+cuts[k+1])/2
 S=np.zeros((n,np.count_nonzero(abs(ev)>=threshold)),complex);S[:patch]=evc[:,abs(ev)>=threshold]
 a,Ua=eigh(S.conj().T@P@S);b,Ub=eigh(S.conj().T@Q@S)
 # Sorted occupied first; ties inside the occupied subspace do not affect the prepared Slater ray.
 Ua=Ua[:,np.r_[np.where(a>.5)[0],np.where(a<=.5)[0]]];Ub=Ub[:,np.r_[np.where(b>.5)[0],np.where(b<=.5)[0]]]
 ra=int(sum(a>.5));rb=int(sum(b>.5));assert ra-rb==1
 W=np.eye(n)+S@(Ub@Ua.conj().T-np.eye(len(a)))@S.conj().T
 d=S@Ua[:,ra-1]
 occ=float(np.real(d.conj()@P@d));u=P@d/np.sqrt(occ)
 Pout=W@(P-np.outer(u,u.conj()))@W.conj().T
 vals,vec=eigh(Q);B=vec[:,vals>.5]
 mat=B.conj().T@Pout@B
 amp=np.sqrt(occ)*np.sqrt(max(0,float(np.real(np.linalg.det(mat)))))
 return dict(retained_modes=S.shape[1],retained_occupancy_a=ra,retained_occupancy_b=rb,threshold=threshold,cut_empty_interval=cuts[k+1]-cuts[k],amplitude=amp,unitarity_error=float(np.linalg.norm(W@W.conj().T-np.eye(n))),annihilated_occupation=occ,min_abs_direct_rotation_denominator=float(min(abs(eigh(np.eye(n)-(P-Q)@(P-Q),eigvals_only=True)))))
out=[]
for leakage in [0.,1e-6,1e-3,.01]:
 G=np.zeros((n,n),complex)
 for j in range(8):G[j,j+12]=leakage;G[j+12,j]=-leakage
 V=expm(G);P=V@Pa@V.conj().T;Q=V@Pb@V.conj().T
 row=surgery(P,Q);row['leakage_rotation']=leakage;row['difference_tail_trace_norm']=float(np.linalg.svd((P-Q)-np.pad((P-Q)[:patch,:patch],((0,n-patch),(0,n-patch))),compute_uv=False).sum());out.append(row)
assert out[0]['amplitude']>.9999999
assert out[2]['amplitude']>.99999
open('producer-workspace/principal_surgery_results.json','w').write(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
