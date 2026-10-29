"""Independent adaptive classical-history stress tests and exact primitive checks."""
from pathlib import Path
import numpy as np,sympy as s,json,hashlib
D=Path(__file__).parent.parent
I=np.eye(2);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);YY=np.kron(Y,Y);v=np.array([1,0,0,1])/np.sqrt(2);phi=np.outer(v,v)
def con(r):
 vals=np.linalg.eigvals(r@YY@r.conjugate()@YY);a=np.sort(np.sqrt(np.maximum(vals.real,0)))[::-1]
 return max(0.,float(a[0]-sum(a[1:])))
def one(r,k):
 q=np.kron(I,k);return q@r@q.conj().T
rng=np.random.default_rng(29062026)
def unitary():return np.linalg.qr(rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)))[0]
def instrument():
 # Weak, history-dependent measurement with independently chosen outcome control.
 p,q=rng.uniform(.15,.85,2);u=unitary()
 return [unitary()@np.diag(np.sqrt([p,q]))@u,unitary()@np.diag(np.sqrt([1-p,1-q]))@u]
c=.93;q=.82;AD=[np.diag([1,c]),np.array([[0,np.sqrt(1-c*c)],[0,0]])]
max_excess=-1.;trials=[]
for trial in range(80):
 branches=[phi];capacity=1.
 for t in range(4):
  before=sum(con(r) for r in branches);new=[]
  for r in branches:new.extend(one(r,k) for k in instrument())
  assert sum(con(r) for r in new)<=before+2e-7
  branches=[]
  for r in new:
   # Noise environment is summed, never supplied as a free classical record.
   r=sum(one(r,k) for k in AD);r=(1+q)/2*r+(1-q)/2*one(r,Z);branches.append(r)
  capacity*=c*q
  assert sum(con(r) for r in branches)<=capacity+2e-7
 fe=sum(np.trace(phi@r).real for r in branches);ex=fe-(1+capacity)/2;max_excess=max(max_excess,ex);assert ex<2e-7
 # Correct probability-weighted heralding bound on an arbitrary declared subset.
 selected=branches[::2];prob=sum(np.trace(r).real for r in selected);joint=sum(np.trace(phi@r).real for r in selected)
 assert joint<=(prob+capacity)/2+2e-7
 trials.append(fe)
# Exact Bell-preserving counterexample if the dephasing environment is monitored.
assert np.max(abs((1+q)/2*phi+(1-q)/2*one(one(phi,Z),Z)-phi))<1e-15
# Exact spinflip characteristic polynomials; independent symbol construction.
x,z=s.symbols('x z',real=True);sy=s.Matrix([[0,-s.I],[s.I,0]]);flip=s.kronecker_product(sy,sy)
j=s.Matrix([[1,0,0,x],[0,0,0,0],[0,0,1-x*x,0],[x,0,0,x*x]])/2
assert s.simplify((z*s.eye(4)-j*flip*j.conjugate()*flip).det()-z**3*(z-x*x))==0
jd=s.Matrix([[1,0,0,x],[0,0,0,0],[0,0,0,0],[x,0,0,1]])/2
assert s.simplify((z*s.eye(4)-jd*flip*jd.conjugate()*flip).det()-z*z*(z-(1+x)**2/4)*(z-(1-x)**2/4))==0
comparisons=[]
for strength in [.01,.03,.1]:
 data=json.loads((D/f'rate_{strength}_v1.json').read_text());fe=1-data['encoded'][-1]['entanglement_infidelity'];upper=(1+(399/401)**32*np.exp(-32*strength))/2
 comparisons.append({'integrated':strength,'encoded_Fe':fe,'all_controls_single_carrier_upper':upper,'margin':fe-upper})
files=[D/'adaptive_single_carrier_bound_v1.md',D/'adaptive_single_carrier_bound_check_v1.py',D/'adaptive_single_carrier_bound_check_v1.json',D/'AUTHOR_MANIFEST_ADAPTIVE_COMPARATOR_v1.json',Path(__file__)]
out={'status':'PASS_ADAPTIVE_RECORD_PROOF_AND_INDEPENDENT_STRESS','trials':80,'compulsory_rounds':4,'terminal_classical_histories_per_trial':16,'max_final_fidelity_bound_excess':max_excess,'comparisons':comparisons,'source_draws':0,'sha256':{str(p.relative_to(D)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
