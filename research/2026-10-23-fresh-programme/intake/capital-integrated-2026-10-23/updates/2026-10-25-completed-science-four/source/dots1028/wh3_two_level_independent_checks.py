"""Independent exact transport identities plus bounded physical two-level diagnostics."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import sympy as s,numpy as np,json,time
from pathlib import Path
start=time.perf_counter();z=s.symbols('z',positive=True);u=(9*z*z-1)/(1-z*z);v=4*u/3;t=(12*z-4)/(1-z)
exact={}
exact['cutoff_order_factor']=s.factor(t-v-8*(3*z-1)/(3*(1-z*z)))==0
exact['matched_tail_ratio']=s.factor((t+4)/(t+12)-z)==0
exact['interval_payment_exponential']=s.factor(((t+4)/(t+12)*(v+12)/(v+4))**2-(u+1)*(u+9)/(u+3)**2)==0
q=s.symbols('q',positive=True)
exact['integral_antiderivative']=s.simplify(s.diff(2*s.log((q+4)/(q+12)),q)-16/((q+4)*(q+12)))==0
assert all(exact.values())
rng=np.random.default_rng(202610250900)
def log(X):
 w,U=np.linalg.eigh((X+X.conj().T)/2);assert min(w)>0;return (U*np.log(w))@U.conj().T
cases=[]
for n,m in [(2,2),(3,4),(4,5)]:
 size=3*n;Q=np.linalg.qr(rng.normal(size=(size,m))+1j*rng.normal(size=(size,m)))[0];P=Q@Q.conj().T;I=np.eye(size)
 def E(X):return np.kron(np.eye(3)/3,np.trace(X.reshape(3,n,3,n),axis1=0,axis2=2))
 def N(X):return (3*E(X)-X.reshape(3,n,3,n).transpose(2,1,0,3).reshape(size,size))/2
 B=E(P);C=(P+3*B)/4;NP=N(P)
 for r in [.03,1.,20.]:
  A=I+r*P;EA=I+r*B;NA=I+r*NP
  gap=np.trace(A@log(A)+EA@log(EA)-2*NA@log(NA)).real
  derivative=m*np.log1p(r)+np.trace(B@log(EA)-2*NP@log(NA)).real
  lower_matrix=np.log1p(r)*np.eye(m)+Q.conj().T@(log(EA)-2*log(I+r*C))@Q
  lower=np.linalg.eigvalsh(lower_matrix)[0]
  bound=np.trace(lower_matrix).real
  assert gap>-1e-9 and derivative>-1e-9 and lower>-1e-9 and derivative-bound>-1e-8
  cases.append({'reference_dim':n,'projection_rank':m,'r':r,'homogeneous_gap':float(gap),'derivative':float(derivative),'compressed_derivative_bound_min_eigenvalue':float(lower),'jensen_trace_margin':float(derivative-bound)})
out={'scope':'Four exact transport identities and nine reproducible physical tests; universal proof is independently audited separately','exact_checks':exact,'seed':202610250900,'cases':cases,'seconds':time.perf_counter()-start}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
