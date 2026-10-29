import sympy as s,json,time,sys,hashlib
from fractions import Fraction as F
from pathlib import Path
P=Path(__file__).parent;SRC=P/'received';sys.set_int_max_str_digits(0)
c=json.loads((P/'candidate_value_polynomial.json').read_text());x=s.symbols('lambda');cs=[int(z) for z in c['integer_coefficients_low_to_high']];p=s.Poly.from_list(cs[::-1],x);assert p.degree()==40 and s.gcd(p,p.diff()).degree()==0
st=time.time();ivs=s.intervals(p,eps=s.Rational(1,2**45),fast=True);isosecs=time.time()-st
assert len(ivs)==28 and all(m==1 for _,m in ivs);lb=F(str(ivs[0][0][0]));ub=F(str(ivs[0][0][1]))
sys.path.insert(0,str(P/'received'));from quartic_sos_oracle import find_candidate
inp=json.loads((SRC/'input.json').read_text());orig={tuple(e):F(v) for e,v in zip(inp['exponents'],inp['original'])};st=time.time();q,value=find_candidate(orig,seed=117,starts=20);optsecs=time.time()-st;bias=F(inp['objective_bias_bound']);lower=lb-bias;gap=value-lower
out={'status':'EXACT_POLYNOMIAL_ROOT_BOUNDS_PENDING_QUOTIENT_IDENTITY','least_real_value_interval':[str(lb),str(ub)],'real_root_count':len(ivs),'all_real_value_intervals':[[str(a),str(b)] for (a,b),m in ivs],'root_isolation_seconds':isosecs,'ordinary_candidate_seconds':optsecs,'ordinary_candidate_quaternion':[str(v) for v in q],'original_exact_candidate_upper':str(value),'original_lower_if_value_polynomial_verified':str(lower),'original_gap_if_verified':str(gap),'gap_float':float(gap),'target':inp['target_gap'],'original_perturbation_bias':str(bias),'scope':'Exact univariate rational isolation plus ordinary candidate evaluated exactly; global interpretation waits for exact quotient verification and accepted shape/primitive/boundary prerequisites.'}
assert gap<=F(inp['target_gap']);(P/'root_candidate_certificate.json').write_text(json.dumps(out,indent=2)+'\n');print('isolation',isosecs,'candidate',optsecs,'gap',float(gap),flush=True)
