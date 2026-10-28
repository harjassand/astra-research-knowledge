"""Author finite matrix checks, no sampled calibration outcomes."""
import numpy as np,json
from pathlib import Path
from hashlib import sha256
rng=np.random.default_rng(281045);I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);P=[X,Y,Z]
V=np.vstack([I,np.zeros((2,2))]);res=[]
for c in range(64):
 u=rng.normal(size=4);u/=np.linalg.norm(u);W=u[0]*I-1j*sum((u[k+1]*P[k] for k in range(3)),np.zeros_like(I));H=np.block([[np.zeros_like(I),W.conj().T],[W,np.zeros_like(I)]])
 mom=max(np.max(np.abs(V.conj().T@np.linalg.matrix_power(H,k)@V-(I if k%2==0 else np.zeros_like(I)))) for k in range(13));assert mom<2e-14
 R=np.array([[np.trace(P[a]@W@P[j]@W.conj().T).real/2 for j in range(3)] for a in range(3)])
 p=float(rng.uniform());mean=np.zeros((3,3));second=0.
 for j in range(3):
  for s in [-1,1]:
   rho=(I+s*P[j])/2
   for a in range(3):
    for b in [-1,1]:
     probability=p*np.trace((I+b*P[a])/2@W@rho@W.conj().T).real/18
     F=np.zeros((3,3));F[a,j]=9*s*b
     mean+=probability*F;second+=probability*np.sum(F*F)
 assert np.max(abs(mean-p*R))<2e-14 and abs(second-81*p)<2e-13
 res.append({'moment_residual':float(mom),'mean_residual':float(np.max(abs(mean-p*R))),'second_residual':float(abs(second-81*p))})
# Weyl average leakage becomes depolarizing, qubit fidelity 1/4.
phi=np.array([1,0,0,1],complex)/np.sqrt(2);bell=np.outer(phi,phi.conj())
avg=sum(np.kron(I,A)@bell@np.kron(I,A).conj().T for A in [I]+P)/4
assert np.max(abs(avg-np.eye(4)/4))<2e-15
# Distinct I/X recovery choice gives average fidelity 1/2.
avg2=(bell+np.kron(I,X)@bell@np.kron(I,X))/2
assert abs(np.trace(avg2@bell).real-.5)<2e-15
root=Path(__file__).resolve().parent
out={'status':'PASS_AUTHOR_MATRIX_AND_BORN_EXPECTATION_FIXTURES','cases':64,'source_calls':0,'sampled_calibration_outcomes':0,'source_sha256':sha256((root/'compressed_moments_hidden_orientation_bridge_20261028.md').read_bytes()).hexdigest(),'max_moment_residual':max(x['moment_residual'] for x in res),'max_mean_residual':max(x['mean_residual'] for x in res),'max_second_residual':max(x['second_residual'] for x in res),'weyl_minimax_leakage_loss':.75,'two_world_no_information_leakage_loss':.5}
(root/'compressed_moments_hidden_orientation_check_20261028.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
