"""Stationary physical-memory guard evaluator; no file/global source dependencies."""
import numpy as np,math
from fractions import Fraction

def nb_tail(t,b,R):
 R=Fraction(R);r,q=R.numerator,R.denominator;N=t+b+1
 return Fraction(sum(math.comb(N,j)*q**j*r**(N-j) for j in range(b+1)),(q+r)**N)
def fault_radius(b,R):
 t=0
 while nb_tail(t,b,R)>Fraction(1,128):t+=1
 return t

def evaluate(tp,tf,service,sigma,s,J,b):
 """Column-vector row-major bath maps, sigma2x2. No logical-fault counter needed for yield."""
 tr=np.array([1,0,0,1]);G=np.linalg.inv(np.eye(4)-(1-s)*tp);S=s*service@G;F=(1-s)*tf@G
 state=np.zeros((J+1,b+1,4),complex);state[0,0]=sigma.reshape(-1);acc=np.zeros(4,complex);abort=np.zeros(4,complex);calls=0.
 for j in range(J):
  for f in range(b+1):
   v=state[j,f];calls+=float((tr@G@v).real);sv=S@v;fv=F@v
   if j+1==J:acc+=sv
   else:state[j+1,f]+=sv
   if f==b:abort+=fv
   else:state[j,f+1]+=fv
 A=float((tr@acc).real);Ab=float((tr@abort).real)
 if abs(A+Ab-1)>2e-8:raise ValueError('Probability conservation failed')
 return {'uncapped_acceptance':A,'uncapped_expected_calls':calls,'test_failure_abort_probability':Ab}

def finite_bounds(A,E,s,J,payload):
 sf=Fraction(s);s=float(sf);cap=math.ceil(Fraction(2*J+256)/sf);err=math.exp(max(-float(cap*sf)/8,-700.));tail=err/(-math.expm1(-s/8))
 return {'cap_native_calls':cap,'finite_cap_loss_upper_bound':err,'expected_calls_truncation_upper_bound':tail,'finite_guard_payload_per_call_lower':payload*max(0,A-err)/E,'finite_guard_payload_per_call_upper':payload*A/(E-tail)}

def evaluate_fast(tp,tf,service,sigma,s,J,b):
 """Service-epoch block transfer, matrix exponentiation in O(log J).
Failure count is retained. Aborts are lost trace, not accepted arrivals.
"""
 tr=np.array([1,0,0,1]);G=np.linalg.inv(np.eye(4)-(1-s)*tp);S=s*service@G;F=(1-s)*tf@G
 powers=[np.eye(4,dtype=complex)]
 for k in range(b):powers.append(F@powers[-1])
 n=4*(b+1);A=np.zeros((n,n),complex);c=np.zeros(n,complex)
 for fin in range(b+1):
  for fout in range(fin,b+1):A[4*fout:4*fout+4,4*fin:4*fin+4]=S@powers[fout-fin]
  c[4*fin:4*fin+4]=tr@G@sum(powers[:b-fin+1])
 aug=np.zeros((n+1,n+1),complex);aug[:n,:n]=A;aug[n,:n]=c;aug[n,n]=1
 v=np.zeros(n+1,complex);v[:4]=sigma.reshape(-1);v=np.linalg.matrix_power(aug,J)@v
 acceptance=float(sum(tr@v[4*k:4*k+4] for k in range(b+1)).real)
 return {'uncapped_acceptance':acceptance,'uncapped_expected_calls':float(v[-1].real),'test_failure_abort_probability':1-acceptance}
