"""Independent record diamond/premium checks and exact noncommuting POVM fixture."""
from pathlib import Path
import numpy as np,sympy as s,itertools,json,hashlib
D=Path(__file__).parent;A=D.parent;Q=A.parent
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);P=[I,X,Y,Z];pn=[np.array(p,complex) for p in P]
# Exact noncommuting six-effect POVM, each direction has rational radius.
weights=[s.Rational(1,2),s.Rational(1,3),s.Rational(1,6)];radii=[s.Rational(3,5),s.Rational(4,5),s.Rational(1,2)]
Fs=[w*(I+sg*r*P[j+1])/2 for j,(w,r) in enumerate(zip(weights,radii)) for sg in [-1,1]]
assert sum(Fs,s.zeros(2))==I
L=sum(w*r for w,r in zip(weights,radii));assert L==s.Rational(13,20)
Ms=[]
for F in Fs:
 M=s.zeros(4)
 for j in range(4):M[0,j]=s.trace(F*P[j])/2
 Ms.append(M)
# Exact moment proof by exhaustive settings/outcomes; output is erased mixed qubit.
est=[s.zeros(4) for _ in Ms];mass=0
for j,u,k,v,h in itertools.product(range(1,4),[-1,1],range(1,4),[-1,1],range(6)):
 M=Ms[h];prob=(M[0,0]+u*M[0,j]+v*M[k,0]+u*v*M[k,j])/36;assert prob>=0;mass+=prob
 est[h][0,0]+=prob;est[h][0,j]+=3*u*prob;est[h][k,0]+=3*v*prob;est[h][k,j]+=9*u*v*prob
assert mass==1 and est==Ms
full=sum((M[0,0]+s.sqrt(sum(M[0,j]**2 for j in range(1,4))))/4 for M in Ms);unitary=sum(M[0,0]/4 for M in Ms)
assert full-unitary==L/4==s.Rational(13,80)
# Bell blocks give exact norm L. Each traceless qubit matrix has eigenvalues ±||b||.
bellnorm=0
for F in Fs:
 B=F-s.trace(F)*I/2;ev=list((B.T/2).eigenvals().items());bellnorm+=sum(abs(e)*m for e,m in ev)
assert bellnorm==L
# Independently generate arbitrary instruments and CPTP conditional receivers.
rng=np.random.default_rng(18002026);max_excess=-1.;bell_error=0.;input_excess=-1.;spin_error=0.;checks=0

def random_kraus(count):
 z=rng.normal(size=(2*count,2))+1j*rng.normal(size=(2*count,2));q=np.linalg.qr(z)[0];return [q[2*i:2*i+2] for i in range(count)]
def ptm(ks):return np.array([[sum(np.trace(p@k@q@k.conj().T).real/2 for k in ks) for q in pn] for p in pn])
def trnorm(z):return float(np.linalg.svd(z,compute_uv=False).sum())
for S in [2,3,6,16]:
 for trial in range(30):
  ks=random_kraus(2*S);maps=[ptm(ks[2*h:2*h+2]) for h in range(S)];bs=[M[0,1:] for M in maps];leak=sum(np.linalg.norm(x) for x in bs);assert leak<=1+1e-12
  uni=0
  for M in maps:
   u,sv,vh=np.linalg.svd(M[1:,1:]);opt=sum(sv[:2])+np.linalg.det(u@vh)*sv[2];uni+=(M[0,0]+opt)/4
  score=0
  for M in maps:
   ds=random_kraus(4);R=ptm(ds);flip=ptm([pn[2]@k.conj()@pn[2] for k in ds]);spin_error=max(spin_error,float(np.max(abs(flip[1:,1:]-R[1:,1:]))),float(np.max(abs(flip[1:,0]+R[1:,0]))))
   score+=np.trace(R@M)/4
  max_excess=max(max_excess,float(score-uni-leak/4));assert score<=uni+leak/4+1e-12
  Bs=[sum(x[j]*pn[j+1] for j in range(3)) for x in bs];bell=sum(trnorm(B.T/2) for B in Bs);bell_error=max(bell_error,abs(bell-leak))
  # General (including nonpositive/non-Hermitian) trace-class test with reference4.
  C=rng.normal(size=(8,8))+1j*rng.normal(size=(8,8));C/=trnorm(C);tensor=C.reshape(2,4,2,4);norm=0
  for B in Bs:out=np.einsum('ij,jria->ra',B,tensor);norm+=trnorm(out)
  input_excess=max(input_excess,norm-leak);assert norm<=leak+1e-12;checks+=1
# Read-only actual source diagnostics: objective orientation and saved primal feasibility.
source=Q/'continuous_inverse_control_20261028/endpoint_instrument_v1.json';src=json.loads(source.read_text());models=np.load(A/'oracle_models_v1.npz');oracle=json.loads((A/'oracle_results_v1.json').read_text());errors=[];actualL=0
for row in oracle['rows']:
 key=row['branch'];M=np.array(src['branch_PTMs'][key]);J=models['CPTP_J_'+key];R=models['CPTP_M_'+key]
 C=sum(M[j,i]*np.kron(pn[i],pn[j].T)/8 for i in range(4) for j in range(4));errors.append(abs(np.trace(C@J).real-np.trace(R@M).real/4))
 assert np.max(abs(J[:2,:2]+J[2:,2:]-np.eye(2)))<1e-10 and np.linalg.eigvalsh(J).min()>-1e-10
 actualL+=np.linalg.norm(M[0,1:])
assert max(errors)<1e-12
files=[A/'GOVERNING_BRANCH_RECOVERY_v1.md',A/'AUTHOR_MANIFEST_v1.json',A/'oracle_models_v1.npz',A/'oracle_results_v1.json',source,Path(__file__)]
out={'status':'PASS_EXACT_FIXED_RECORD_FIXTURE_AND_INDEPENDENT_BRANCH_STRESS','exact_noncommuting_POVM_L':str(L),'exact_attained_premium':str(full-unitary),'exact_moment_entries':96,'random_instruments':checks,'maximum_premium_bound_excess':max_excess,'Bell_identity_max_error':bell_error,'general_traceclass_reference4_max_excess':input_excess,'spin_flip_affine_max_error':spin_error,'actual_L_over_4':actualL/4,'actual_objective_identity_max_error':max(errors),'new_acquisition_draws':0,'sha256':{str(p.relative_to(Q)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(D/'check_branch_theorem_v1.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
