#!/usr/bin/env python3
import itertools, json, math, pathlib, hashlib
import numpy as np
from scipy.linalg import eigh
ROOT=pathlib.Path(__file__).resolve().parent
rng=np.random.default_rng(202610290433)
def matchings(v):
 if not v:yield ();return
 for j in range(1,len(v)):
  for t in matchings(v[1:j]+v[j+1:]):yield ((v[0],v[j]),)+t
def state(n,M):
 v=np.zeros(2**n)
 for x in range(2**n):
  bits=[(x>>(n-1-j))&1 for j in range(n)]
  if all(bits[a]!=bits[b] for a,b in M):v[x]=np.prod([1 if bits[a]==0 else -1 for a,b in M])/np.sqrt(2**len(M))
 return v
out={'seed':202610290433,'orbit_fixtures':[],'rank_one_rate_comparison':[]}
for n in (4,6):
 states=np.array([state(n,M) for M in matchings(tuple(range(n)))]).T
 d=math.comb(n,n//2)//(n//2+1)
 vals,V=eigh(states@states.T);V=V[:,-d:]
 e0=V.T@state(n,tuple((j,j+1) for j in range(0,n,2)))
 x=V.T@state(n,((0,2),(1,3))+tuple((j,j+1) for j in range(4,n,2)))
 e1=x-e0*np.vdot(e0,x);e1/=np.linalg.norm(e1);E=np.column_stack([e0,e1])
 reps=[]
 for p in itertools.permutations(range(n)):
  ids=[]
  for x in range(2**n):
   bits=[(x>>(n-1-j))&1 for j in range(n)]
   ids.append(sum(bits[p[j]]<<(n-1-j) for j in range(n)))
  reps.append(V.T@V[ids])
 for orientation in ('adversarial_code_vector','random'):
  v=e0.astype(complex) if orientation=='adversarial_code_vector' else rng.normal(size=d)+1j*rng.normal(size=d)
  v/=np.linalg.norm(v);U=np.eye(d)-2*np.outer(v,v.conj());a=1-2/d;pbad=1-a*a
  J=np.zeros((4,4),complex);avg=np.zeros((d,d),complex)
  for R in reps:
   B=R.T@U@R;avg+=B/len(reps);A=E.conj().T@B@E
   L=np.eye(2)-A.conj().T@A
   avec=A.reshape(-1,order='F')
   J+=(np.outer(avec,avec.conj())+np.kron(L.T,np.diag([1.,0.])))/(2*len(reps))
  bell=np.eye(2).reshape(-1,order='F')/np.sqrt(2);Jid=np.outer(bell,bell)
  residual=J-a*a*Jid
  min_cp=float(np.min(np.linalg.eigvalsh(residual)))
  assert min_cp>-1e-11
  assert np.linalg.norm(avg-a*np.eye(d))<1e-11
  assert abs(np.trace(residual)-pbad)<1e-11
  fixed=E.conj().T@U@E
  fixedfe=abs(np.trace(fixed)/2)**2
  if orientation=='adversarial_code_vector':assert fixedfe<1e-24
  out['orbit_fixtures'].append({'n':n,'d':d,'orientation':orientation,'permutations':len(reps),'fixed_raw_entanglement_fidelity':float(fixedfe),'orbit_entanglement_fidelity':float(np.vdot(bell,J@bell).real),'orbit_halfdiamond_upper_bound':pbad,'bad_CP_min_eigenvalue':min_cp,'mean_unitary_residual':float(np.linalg.norm(avg-a*np.eye(d)))})
for n in range(4,101,4):
 d=math.comb(n,n//2)//(n//2+1);D0=2**(n//4)
 out['rank_one_rate_comparison'].append({'n':n,'full_singlet_d':d,'four_spin_payload_qubits':n//4,'four_spin_D0':D0,'permutation_halfdiamond_upper_bound':4*(d-1)/d**2,'four_spin_logical_Pauli_halfdiamond_upper_bound':4*(D0-1)/D0**2,'fixed_one_payload_mixed_ancilla_product_defect_exact_halfdiamond':2/D0})
out['all_checks_passed']=True
out['script_sha256']=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
(ROOT/'check_defect.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'all_checks_passed':True,'orbit_fixtures':out['orbit_fixtures'],'sample_rates':[r for r in out['rank_one_rate_comparison'] if r['n'] in (8,12,20,40)]},indent=2))
