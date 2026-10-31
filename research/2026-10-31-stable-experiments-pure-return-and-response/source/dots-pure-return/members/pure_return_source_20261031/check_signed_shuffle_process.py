"""Small dense diagnostic, not the succinct quantum compiler."""
from pathlib import Path
from itertools import permutations
import json,numpy as np
from scipy.linalg import expm,block_diag,eigvalsh
n=3;perms=list(permutations(range(n)));ix={p:i for i,p in enumerate(perms)};d=len(perms)
Ts=[]
for c in range(n):
 T=np.zeros((d,d),complex)
 for y,p in enumerate(perms):T[y,ix[(c,)+tuple(v for v in p if v!=c)]]=1
 Ts.append(T)
P=sum(Ts)/n;plus=np.ones(2)/np.sqrt(2);Ksign=[np.outer(plus,np.eye(2)[z]) for z in range(2)]
Ks=[np.kron(k,T/np.sqrt(n)) for k in Ksign for T in Ts];ds=2*d
psi=np.ones(ds)/np.sqrt(ds);Proj=np.outer(psi,psi);Q=np.eye(ds)-Proj
Wret=Q.copy();m=int(np.ceil(n*np.log(16*n)))
for _ in range(m):Wret=sum(k.conj().T@Wret@k for k in Ks)
A=sum(Ks)/np.sqrt(2*n)
cert={'m':m,'return_norm':float(np.linalg.norm(Wret,2)),'power_norm':float(np.linalg.norm(np.linalg.matrix_power(A,m)@Q,2)),'TP_error':float(np.linalg.norm(sum(k.conj().T@k for k in Ks)-np.eye(ds),2))}
assert cert['return_norm']<=1/16+1e-12 and cert['power_norm']<=.25+1e-12
X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1.,-1.]);gates=[expm(-.37j*X),expm(-.51j*Y),expm(-.29j*Z)];b=.4
Bs=[]
for p in perms:
 U=np.eye(2,dtype=complex)
 for k in p:U=gates[k]@U
 Bs.append(b*U.conj().T@Z@U)
Hlabels=[sgn*Bs[j] for sgn in [1.,-1.] for j in range(d)]
Kcoupling=sum(np.kron(B,np.diag(np.eye(ds)[j])) for j,B in enumerate(Hlabels));rho0=np.outer(plus,plus);Tend=.4;tc=.17;Uc=expm(-.31j*X);Ufull=np.kron(Uc,np.eye(ds));dim=2*ds
R=np.kron(np.ones((2,2))/2,P.T.real);rows=[]
for lam in [3.,30.]:
 H=np.sqrt(lam)*Kcoupling;I=np.eye(dim)
 gen=-1j*(np.kron(I,H)-np.kron(H.T,I))-lam*np.eye(dim*dim,dtype=complex)
 for k in Ks:
  kk=np.kron(np.eye(2),k);gen+=lam*np.kron(kk.conj(),kk)
 rho=np.kron(rho0,Proj)
 rho=(expm(tc*gen)@rho.reshape(-1,order='F')).reshape(dim,dim,order='F');rho=Ufull@rho@Ufull.conj().T
 rho=(expm((Tend-tc)*gen)@rho.reshape(-1,order='F')).reshape(dim,dim,order='F')
 red=np.einsum('iaja->ij',rho.reshape(2,ds,2,ds))
 comms=[-1j*np.sqrt(lam)*(np.kron(np.eye(2),B)-np.kron(B.T,np.eye(2))) for B in Hlabels]
 gc=np.kron(lam*(R.T-np.eye(ds)),np.eye(4))+block_diag(*comms)
 rhos=np.tile(rho0.reshape(-1,order='F')/ds,ds)
 rhos=expm(tc*gc)@rhos
 blocks=[Uc@v.reshape(2,2,order='F')@Uc.conj().T for v in rhos.reshape(ds,4)]
 rhos=np.concatenate([v.reshape(-1,order='F') for v in blocks]);rhos=expm((Tend-tc)*gc)@rhos
 classical=sum(v.reshape(2,2,order='F') for v in rhos.reshape(ds,4))
 error=float(np.sum(np.abs(eigvalsh(red-classical))))
 assert error<1e-10
 rows.append({'lambda':lam,'controlled_final_trace_norm_difference':error,'quantum_trace':float(np.trace(rho).real)})
result={'scope':'small dense controlled-process diagnostic only','n':n,'source_dimension':ds,'certificate':cert,'T':Tend,'control_time':tc,'rows':rows}
print(json.dumps(result,indent=2));Path(__file__).with_name('signed_shuffle_process_checks.json').write_text(json.dumps(result,indent=2)+'\n')
