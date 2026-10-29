#!/usr/bin/env python3
import numpy as np, math,json,pathlib,itertools
from fractions import Fraction
from scipy.linalg import expm,eigh
R=pathlib.Path(__file__).resolve().parent
rng=np.random.default_rng(202610290440)
def kronn(a,n):
 x=np.ones((1,1),complex)
 for _ in range(n):x=np.kron(x,a)
 return x
H=np.array([[1,1],[1,-1]],complex)/np.sqrt(2);S=np.diag([1,1j]);X=np.array([[0,1],[1,0]],complex)
def membership(n):
 D=2**n;Pz=np.diag([float(x.bit_count()==n//2) for x in range(D)])
 Ux=kronn(H,n);Uy=kronn(S@H,n)
 return (Pz+Ux@Pz@Ux.conj().T+Uy@Pz@Uy.conj().T)/3
out={'spin_checks':[],'physical_checks':[],'transfer_checks':[]}
for j in range(1,51):
 ms=np.arange(-j,j+1,dtype=float);Jp=np.zeros((2*j+1,2*j+1),complex)
 for k,m in enumerate(ms[:-1]):Jp[k+1,k]=np.sqrt(j*(j+1)-m*(m+1))
 Jx=(Jp+Jp.conj().T)/2;Jy=(Jp-Jp.conj().T)/(2j)
 _,vx=eigh(Jx);_,vy=eigh(Jy);vz=np.eye(2*j+1)[:,j]
 A=np.column_stack([vx[:,j],vy[:,j],vz]);ev=eigh(A.conj().T@A/3,eigvals_only=True)
 c=Fraction(0) if j%2 else Fraction((-1)**(j//2)*math.comb(j,j//2),2**j)
 expected=np.sort([float((1+2*c)/3),float((1-c)/3),float((1-c)/3)])
 err=float(np.max(abs(ev-expected)));assert err<1e-11 and ev[-1]<=7/12+1e-12
 out['spin_checks'].append({'j':j,'legendre_zero':str(c),'max_pass_eigenvalue':float(ev[-1]),'spectrum_residual':err})
for n in (2,4,6,8):
 T=membership(n);ev,U=eigh(T);d=math.comb(n,n//2)//(n//2+1)
 beta=1/3 if n==2 else .5 if n<8 else 7/12
 assert np.max(abs(ev[-d:]-1))<1e-11 and abs(ev[-d-1]-beta)<1e-11
 P=U[:,-d:]@U[:,-d:].conj().T
 gap_res=float(np.min(eigh(P+beta*(np.eye(2**n)-P)-T,eigvals_only=True)))
 assert gap_res>-1e-11
 out['physical_checks'].append({'n':n,'singlet_rank':d,'second_sector_eigenvalue':float(ev[-d-1]),'claimed_beta':beta,'operator_inequality_min_eigenvalue':gap_res})
# Exact wrong-code counterexample using a genuine collective rotation.
n=4;D=16;T=membership(n);vals,U=eigh(T);V=U[:,-2:];P=V@V.conj().T
Ebad=np.eye(D)[:,[0,15]]
phases=np.array([np.exp(1j*np.pi*(n-2*x.bit_count())/8) for x in range(D)])
N=np.diag(phases)
logical=Ebad.conj().T@N@Ebad
out['wrong_code_counterexample']={'roundtrip_fidelity':1.,'service_fidelity':float(abs(np.trace(logical)/2)**2),
 'source_on_singlet_residual':float(np.linalg.norm(N@V-V)),
 'membership_failure':float(1-np.trace(T@Ebad@Ebad.conj().T/2).real)}
assert out['wrong_code_counterexample']['service_fidelity']<1e-20
assert out['wrong_code_counterexample']['source_on_singlet_residual']<1e-11
# Stable actual E,D map transfer tests; no use of their matrices as an
# acquisition interface is asserted by these simulator checks.
def iso(a,b):return np.linalg.qr(rng.normal(size=(a,b))+1j*rng.normal(size=(a,b)))[0]
def decoder(Vd):
 u,s,v=np.linalg.svd(Vd.conj().T,full_matrices=True);comp=v.conj().T[:,2:]
 ks=[Vd.conj().T]
 for a in range(2):
  for r in range(D-2):ks.append(np.outer(np.eye(2)[:,a],comp[:,r].conj())/np.sqrt(2))
 return np.array(ks)
perms=[]
for p in itertools.permutations(range(n)):
 ix=[sum(((x>>i)&1)<<p[i] for i in range(n)) for x in range(D)]
 perms.append(np.eye(D)[ix,:])
Vperp=np.linalg.svd(V.conj().T,full_matrices=True)[2].conj().T[:,2:4]
for case in range(36):
 theta=(0.,.001,.02,.1)[case%4];rot=(0.,.005,.05)[case%3]
 E0=np.cos(theta)*V+np.sin(theta)*Vperp
 E1=E0@expm(1j*rot*X)
 Es=np.array([np.sqrt(.7)*E0,np.sqrt(.3)*E1])
 Vd=E0@expm(1j*(rot/2)*np.diag([1.,-1.]))
 Ds=decoder(Vd)
 eta=float(sum(np.trace(e.conj().T@(np.eye(D)-P)@e).real for e in Es)/2)
 rttr=np.einsum('bki,aik->ab',Ds,Es)
 delta=float(1-np.sum(abs(rttr)**2)/4)
 randomKs=iso(D*3,D).reshape(3,D,D)
 amp=(.0001,.01,.2)[case%3]
 Ns=[np.sqrt(1-amp)*np.eye(D)]+[np.sqrt(amp)*a for a in randomKs]
 pbad=float(1-sum(abs(np.trace(V.conj().T@a@V)/2)**2 for a in Ns))
 fe=0.
 for W in perms:
  for a in Ns:
   A=W.T@a@W
   ne=np.einsum('ij,ajk->aik',A,Es)
   tr=np.einsum('bki,aik->ab',Ds,ne)
   fe+=np.sum(abs(tr)**2)/(4*24)
 loss=float(1-fe)
 bound=(np.sqrt(max(0,delta))+np.sqrt(max(0,pbad))+2*np.sqrt(max(0,eta)))**2
 lin=3*delta+3*pbad+12*eta
 assert loss<=bound+1e-10 and bound<=lin+1e-10
 if theta==0:assert loss<=delta+pbad-delta*pbad+1e-10
 out['transfer_checks'].append({'case':case,'encoder_leakage':eta,'roundtrip_loss':delta,'raw_orbit_bad_mass':pbad,'actual_service_loss':loss,'triangle_bound':float(bound),'linear_bound':float(lin)})
out['all_checks_passed']=True
(R/'check_calibration_boundary_v1.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'all_checks_passed':True,'spin_checks':50,'physical_sizes':[2,4,6,8],'transfer_cases':36,'wrong_code':out['wrong_code_counterexample']},indent=2))
