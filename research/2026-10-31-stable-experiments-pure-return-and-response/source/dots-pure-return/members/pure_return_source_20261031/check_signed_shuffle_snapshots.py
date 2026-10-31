"""Small dense source-snapshot diagnostic; not the succinct quantum compiler."""
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
 Eq1=expm(tc*gen);Eq2=expm((Tend-tc)*gen)
 comms=[-1j*np.sqrt(lam)*(np.kron(np.eye(2),B)-np.kron(B.T,np.eye(2))) for B in Hlabels]
 gc=np.kron(lam*(R.T-np.eye(ds)),np.eye(4))+block_diag(*comms)
 Ec1=expm(tc*gc);Ec2=expm((Tend-tc)*gc)
 for initial in ['stationary','fixed_label_0']:
  source=Proj if initial=='stationary' else np.diag(np.eye(ds)[0])
  weights=np.ones(ds)/ds if initial=='stationary' else np.eye(ds)[0]
  rho=(Eq1@np.kron(rho0,source).reshape(-1,order='F')).reshape(dim,dim,order='F')
  cv=Ec1@np.concatenate([w*rho0.reshape(-1,order='F') for w in weights])
  error=0.;total=0.
  for label in range(ds):
   U=Uc if label%2 else X
   proj=np.diag(np.eye(ds)[label]);instrument=np.kron(U,proj)
   branch=instrument@rho@instrument.conj().T
   qout=(Eq2@branch.reshape(-1,order='F')).reshape(dim,dim,order='F').reshape(2,ds,2,ds)
   cin=np.zeros_like(cv);local=cv.reshape(ds,4)[label].reshape(2,2,order='F')
   cin.reshape(ds,4)[label]=(U@local@U.conj().T).reshape(-1,order='F')
   cout=(Ec2@cin).reshape(ds,4)
   for final_label in range(ds):
    qc=qout[:,final_label,:,final_label];cc=cout[final_label].reshape(2,2,order='F');diff=qc-cc
    error+=float(np.sum(np.abs(eigvalsh((diff+diff.conj().T)/2))))
    total+=float(np.trace(qc).real)
  assert error<1e-10 and abs(total-1)<1e-10
  rows.append({'lambda':lam,'initial_source':initial,'joint_snapshot_feedback_final_label_trace_error':error,'total_probability':total})
result={'scope':'dense diagnostic of classical label measurements/feedback only','n':n,'source_dimension':ds,'snapshot_time':tc,'final_time':Tend,'rows':rows}
print(json.dumps(result,indent=2));Path(__file__).with_name('signed_shuffle_snapshot_checks.json').write_text(json.dumps(result,indent=2)+'\n')
