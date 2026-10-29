import numpy as np,json,itertools
from pathlib import Path
from functools import reduce
from scipy.linalg import expm
from scipy.spatial.transform import Rotation
rng=np.random.default_rng(2026102913);base=np.load(Path(__file__).with_name('check_exact_nonunital_v1.npz'));O=base['O'];Jembed=base['Jembed'];n=4;D=16
P=np.array([np.eye(2),[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex);kron=lambda xs:reduce(np.kron,xs)
def su(R):return expm(-.5j*np.einsum('a,aij->ij',Rotation.from_matrix(R).as_rotvec(),P[1:]))
V=kron([su(R) for R in O]);Js=[V@sum(kron([P[a] if i==j else P[0] for i in range(n)]) for j in range(n))@V.conj().T/2 for a in [1,2,3]]
H=sum(np.kron(Js[a],P[a+1]) for a in range(3));Us=[expm(-1j*(.45*H+np.kron(np.eye(D),.2*P[1]))),expm(-1j*(.9*H+np.kron(np.eye(D),.35*P[3])))]
coeff=np.zeros((2,3,4,16,9))
for v,U in enumerate(Us):
 for i in range(1,n):
  ops=[kron([P[a] if j==i else P[b] if j==0 else P[0] for j in range(n)]) for a in range(4) for b in range(4)]
  ys=[U.conj().T@np.kron(ops[4*a+b],np.eye(2))@U for a in [1,2,3] for b in [1,2,3]]
  for z in range(4):
   coeff[v,i-1,z]=np.array([[np.trace(np.kron(X,P[z]/2)@Y).real/D for Y in ys] for X in ops])
# Product-Pauli pure states and actual simultaneous local measurement bases.
kets=[]
for a in [1,2,3]:
 _,U=np.linalg.eigh(P[a]);kets.extend([U[:,1],U[:,0]])
configs=np.array(list(itertools.product(range(6),repeat=n)),int);invec=np.stack([kron([kets[x] for x in c]) for c in configs]);axes=np.array(list(itertools.product(range(3),repeat=n)),int);bits=np.array(list(itertools.product(range(2),repeat=n)),int);measurement=np.stack([np.stack([kron([kets[2*a+b] for a,b in zip(ax,bit)]) for bit in bits],axis=1) for ax in axes])
bath=np.array([1,0],complex);lastparity=0;sums=np.zeros((3,16,9));moments=np.zeros((2,4));rows=[]
def polar(A):
 u,s,v=np.linalg.svd(A);return u@np.diag([1,1,np.linalg.det(u@v)])@v
def rounding(v):
 A=np.sqrt(3)*v.reshape(3,3);R1=polar(A);R2=polar(-A);return R1 if np.linalg.norm(R1-A)<=np.linalg.norm(R2+A) else R2
for step in range(1,200001):
 variant=lastparity;bloch=np.array([np.vdot(bath,Q@bath).real for Q in P]);moments[variant]+=bloch
 ii=rng.integers(len(configs));zz=rng.integers(len(axes));wave=(Us[variant]@np.kron(invec[ii],bath)).reshape(D,2);amp=measurement[zz].conj().T@wave;prob=(abs(amp)**2).sum(axis=1);prob/=prob.sum();out=rng.choice(D,p=prob);bath=amp[out]/np.linalg.norm(amp[out]);lastparity=int(bits[out].sum()%2)
 ci=configs[ii]//2+1;si=1-2*(configs[ii]%2);zi=axes[zz];yi=1-2*bits[out]
 for i in range(1,n):
  col=3*zi[i]+zi[0];b=9*yi[i]*yi[0]
  sums[i-1,0,col]+=b;sums[i-1,4*ci[i],col]+=3*si[i]*b;sums[i-1,ci[0],col]+=3*si[0]*b;sums[i-1,4*ci[i]+ci[0],col]+=9*si[i]*si[0]*b
 if step in [10000,100000,200000]:
  Tbar=np.einsum('vz,vizab->iab',moments,coeff)/step;results=[]
  for i in range(1,n):
   true=O[i]@O[0].T;Mbar=Tbar[i-1]-Jembed;That=sums[i-1]/step;_,sv,vt=np.linalg.svd(That-Jembed);Chat=rounding(vt[-1])
   assert np.linalg.norm(Mbar@true.reshape(-1))<1e-11
   results.append({'pair':[i,0],'occupation_common_kernel_residual':float(np.linalg.norm(Mbar@true.reshape(-1))),'occupation_second_singular_value':float(np.linalg.svd(Mbar,compute_uv=False)[-2]),'operator_error_vs_actual_occupation_average':float(np.linalg.norm(That-Tbar[i-1],2)),'relative_frame_F_error':float(np.linalg.norm(Chat-true))})
  rows.append({'full_array_calls':step,'conditional_source_variant_counts':moments[:,0].tolist(),'predictable_bath_Bloch_sums':moments[:,1:].tolist(),'pair_results':results})
print(json.dumps({'seed':2026102913,'scope':'Actual fresh product-Pauli probes, simultaneous output measurement, conditional bath-state updates and past-output-dependent source variant. The bath is NEVER reset. The learner uses only classical probe records; exact occupation matrices are simulator checks, not physical access.','results':rows,'confidence_note':'Small finite executable mechanism checks; no claim that conservative stopping confidence target is reached.'},indent=2))
