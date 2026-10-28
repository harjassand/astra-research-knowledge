"""Independent finite checks, not execution of the huge weighted design or source cap."""
import numpy as np, math, json, hashlib
from pathlib import Path
p=Path(__file__).parent
A=[]
for i in range(4):
 x=np.eye(4)[i]; A.append([*x*x,*[2*x[j]*x[l] for j in range(4) for l in range(j+1,4)]])
for i in range(4):
 for j in range(i+1,4):
  x=(np.eye(4)[i]+np.eye(4)[j])/math.sqrt(2); A.append([*x*x,*[2*x[j]*x[l] for j in range(4) for l in range(j+1,4)]])
A=np.array(A); ea=float(np.linalg.eigvalsh(A.T@A/10)[0]); assert ea>=1/4000
anchors=[]
for k in [1,2,3,5,10]:
 dc=3*k*k+1; D=10*dc
 # Decoder anchor covariance spectrum: dc-2 repeated eigenvalues and a 2x2 block.
 block=np.array([[1,math.sqrt(dc-1)/(4*dc)],[math.sqrt(dc-1)/(4*dc),1/(16*dc)]])
 eb=min(float(np.linalg.eigvalsh(block)[0]),1/(16*dc))
 lam=2**-22/D**2
 anchors.append(dict(k=k,D=D,decoder_eigenvalue=eb,weighted_initial_margin=ea*eb/19/lam))
 assert eb>=1/(33*dc**2) and ea*eb/19>=lam
min_det=10.; min_floor_logratio=1e9
for D in [2,3,10,40,130,1000,10000]:
 det=math.exp(D*math.log1p(-1/D))*(1+8*D/(D-1)); min_det=min(min_det,det); assert det>2
 for logQ in [1,10,100,1000]:
  T=math.ceil(D*logQ/math.log(2))+1
  ratio=T*math.log1p(-1/D)+4*logQ+math.log(4)
  min_floor_logratio=min(min_floor_logratio,ratio); assert ratio>=0
c=1/16; envelope=3*c*c+2*c*math.sqrt(32); assert envelope<.75
rng=np.random.default_rng(27519); worst=0.
for D in [2,7,20]:
 L=np.eye(D)+np.tril(rng.normal(size=(D,D))*.1,-1); ds=np.exp(rng.normal(size=D)); V=(L*ds)@L.T
 errphi=rng.uniform(-1,1,D)*4/np.sqrt(1234*ds); errtheta=np.linalg.solve(L.T,errphi)
 norm=float(errtheta@V@errtheta); assert norm<=16*D/1234*(1+1e-12)
 for _ in range(100):
  a=rng.normal(size=D); u=rng.uniform(.01,19); r=np.linalg.solve(L,a)
  lhs=float(a@np.linalg.solve(V,a)/u); rhs=float(np.sum(r*r/ds/u)); worst=max(worst,abs(lhs-rhs)/max(1,lhs)); assert np.isclose(lhs,rhs)
source=p/'ordinary_generic_fast_polynomial_design_baseline_20261028.md'
result=dict(status='PASS_FINITE_DIAGNOSTICS_ONLY',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),encoder_min_eigenvalue=ea,anchor_checks=anchors,min_update_determinant_ratio=min_det,min_log_floor_slack=min_floor_logratio,envelope_coefficient=envelope,max_LDL_relative_residual=worst,scope='Anchor eigenvalues, determinant/lower-conditioning inequalities, LDL decomposition and median norm algebra. No SDP solver, full design, source simulation, hardware or general proof by finite cases.')
(p/'ordinary_generic_fast_polynomial_design_baseline_20261028_independent_poly_check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
