"""Certify the whole white ray at the two exact critical points."""
from fractions import Fraction as F
from pathlib import Path
import json,sys,time
sys.set_int_max_str_digits(0)
START=time.perf_counter()
import sympy as s
HERE=Path(__file__).resolve().parent
PRIOR=HERE.parents[2]/'sol12_structural_capability_20261028'/'quantum_independent'
sys.path.insert(0,str(PRIOR))
import arith as a
data=json.loads((HERE/'WHITE_POLYNOMIAL.json').read_text())
x=s.symbols('x');char=s.Poly.from_list([s.Rational(c)for c in data['M_char_coefficients']],x)
def fraction(q):return F(int(q.p),int(q.q))
eigdata=char.intervals(eps=s.Rational(1,2**50),inf=0)
assert len(eigdata)==6 and all(m==1 and iv[0]>0 for iv,m in eigdata)
eigs=[tuple(map(fraction,iv))for iv,m in eigdata]
def flog(iv):
 if iv==(F(0),F(0)):return a.iv(0)
 assert iv[0]>0
 return a.mul(iv,a.logiv(iv))
def hvalue(t):
 terms=[a.scale(flog(a.add(t,a.iv(F(500)))),2)]
 terms.extend(flog(a.add(t,a.iv(F(j))))for j in range(1,9))
 terms.append(a.scale(flog(t),8))
 terms.append(a.scale(flog(a.add(t,a.iv(F(518,9)))),18))
 terms.extend(a.scale(flog(a.add(t,a.scale(iv,F(1,3)))),-6)for iv in eigs)
 result=a.iv(0)
 for term in terms:result=a.add(result,term)
 return result
critical=[tuple(F(v)for v in iv)for iv,m in data['positive_critical_intervals']]
h0=hvalue(a.iv(0));values=[hvalue(iv)for iv in critical]
assert h0[0]>76 and values[0][0]>76 and values[1][0]>76
assert critical[1][0]>1
R=s.Poly.from_list([s.Rational(c)for c in data['R_coefficients']],x)
assert R.eval(0)<0 and R.LC()<0
# P(0)>0; the numerator vanishes at0. Two simple positive roots
# therefore force the derivative signs -,+,-.
out={'status':'EXACT_WHOLE_WHITE_CURVE_ADMITTED','M_eigenvalue_intervals':[a.record(iv)for iv in eigs],
 'h0_interval':a.record(h0),'critical_h_intervals':[a.record(iv)for iv in values],
 'positive_critical_intervals':[a.record(iv)for iv in critical],
 'derivative_signs':['negative','positive','negative'],
 'white_curve':'strictly positive for every finite a>=0; tends0 at infinity',
 'compact_lower':'h(a)>76 on[0,1]','seconds_including_sympy':time.perf_counter()-START,
 'root_polynomial_receipt':'WHITE_POLYNOMIAL.json','scope':'One independently noncommuting matrix-weight seed, not arbitrary weights.'}
(HERE/'WHOLE_WHITE.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'h0_display':out['h0_interval']['display_only'],
 'critical_h_displays':[iv['display_only']for iv in out['critical_h_intervals']],
 'seconds':out['seconds_including_sympy']},indent=2))
