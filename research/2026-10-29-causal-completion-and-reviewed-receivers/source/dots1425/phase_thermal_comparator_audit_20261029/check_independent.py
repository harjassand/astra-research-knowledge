import sympy as s,numpy as np,json,hashlib
from scipy.integrate import quad
from pathlib import Path
p=Path(__file__).parent;src=p.parent/'qubit_entropy_comparator_20261029'
for mn in ['PHASE_FREEZE.json','THERMAL_FREEZE.json']:
 for f,h in json.loads((src/mn).read_text()).items():assert hashlib.sha256((src/f).read_bytes()).hexdigest()==h
assert hashlib.sha256((src/'PRIMARY_PRIOR_ART_SCOPE.md').read_bytes()).hexdigest()=='ce463488f1ba04734e997d44ad852ed10e744e2b6476cb842e8fcb016f177975'
g,q=s.symbols('gamma q',positive=True);A=1-g*(1-q);B=1-g*q;eta=1-g
assert s.expand(A*B-eta-g*g*q*(1-q))==0
c=s.sqrt(eta/(A*B));block=s.Matrix([[c*A,s.sqrt(eta)],[s.sqrt(eta),c*B]])
assert s.simplify(block.det())==0
# Independent scalar-series/resolvent diagnostic, including noncommuting reference blocks.
rng=np.random.default_rng(1319);Z=np.diag([1,1,-1,-1]);rows=[];maxres=0
S=lambda a:-sum(v*np.log(v) for v in np.linalg.eigvalsh((a+a.conj().T)/2) if v>1e-14)
for trial in range(15):
 X=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));rho=X@X.conj().T;rho/=np.trace(rho);r0=(rho+Z@rho@Z)/2;off=rho-r0
 def integrand(t,a):
  # Integrate paired expression, not cancellation-prone Tr[X inverse].
  eig,U=np.linalg.eigh(r0+t*np.eye(4));inv=(U*(1/np.sqrt(eig)))@U.conj().T;ev=np.linalg.eigvalsh(inv@off@inv)
  return float(sum(a*v*v/(1-a*a*v*v) for v in ev))
 for a in [.1,.5,.9]:
  integ=quad(lambda t:integrand(t,a),0,np.inf,epsabs=1e-10)[0]
  h=1e-5;deriv=(S(r0-(a-h)*(-off))-S(r0-(a+h)*(-off)))/(2*h)
  # g(a)=S(r0)-S(r0+a off), so the derivative is negative derivative of S.
  maxres=max(maxres,abs(integ-deriv));assert abs(integ-deriv)<1e-7
  ga=S(r0)-S(r0+a*off);g1=S(r0)-S(rho);assert ga<=a*a*g1+1e-12
 rows.append({'trial':trial,'coherence':float(S(r0)-S(rho))})
out={'manifests_and_prior_companion_verified':True,'symbolic_AB_identity_and_CP_block_determinant':'pass','noncommuting_resolvent_cases':45,'max_resolvent_derivative_residual':maxres,'scope':'Exact CP algebra plus finite floating resolvent diagnostics; established prior mechanisms, not novelty or hardware.'}
(p/'INDEPENDENT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
