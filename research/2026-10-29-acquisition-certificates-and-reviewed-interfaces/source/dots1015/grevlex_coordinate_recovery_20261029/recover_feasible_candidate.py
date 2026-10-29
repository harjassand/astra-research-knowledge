"""Untrusted modular-coordinate finder; exact unit/upper/lower verification is decisive."""
from pathlib import Path
from fractions import Fraction as F
import sympy as s,json,sys,time
P=Path(__file__).parent;SRC=Path('producer-workspace/grevlex_value_oracle_20261029');sys.path.insert(0,str(SRC/'received'));from quartic_sos_oracle import rational_candidate,exact_eval
st=time.time();nums=[[F(x) for x in row] for row in json.loads((P/'coordinate_candidates.json').read_text())['coefficients']];c=[F(x) for x in json.loads((SRC/'candidate.json').read_text())['monic_coefficients_low_to_high']];t=s.Symbol('t');poly=s.Poly.from_list([s.Rational(x.numerator,x.denominator) for x in c[::-1]],t)
iv=s.intervals(poly,eps=s.Rational(1,2**100),fast=True)[0][0];lb,ub=map(lambda x:F(str(x)),iv);mid=(lb+ub)/2
def ev(cs):
 a=F(0)
 for x in cs[::-1]:a=a*mid+x
 return a
der=ev([i*c[i] for i in range(1,41)]);coords=[ev(cs)/der for cs in nums];q=rational_candidate([1]+[float(x) for x in coords],bits=36);assert sum(x*x for x in q)==1
inp=json.loads((SRC/'received/input.json').read_text());f={tuple(e):F(v) for e,v in zip(inp['exponents'],inp['original'])};upper=exact_eval(f,q);lower=lb-F(inp['objective_bias_bound']);gap=upper-lower;assert gap<F(inp['target_gap'])
out={'status':'EXACT_FEASIBLE_GLOBAL_GAP_CERTIFICATE_USING_UNTRUSTED_COORDINATE_FINDER','seconds':time.time()-st,'coordinate_midpoint_approximations':[float(x) for x in coords],'rational_unit_quaternion':list(map(str,q)),'least_value_interval':[str(lb),str(ub)],'exact_original_upper':str(upper),'exact_original_lower':str(lower),'exact_gap':str(gap),'gap_float':float(gap),'scope':'No local optimizer used. Coordinate candidate identities remain modular only; exact feasibility and original objective upper independently verify their useful output. Global lower depends on received exact grevlex value polynomial proof.'};(P/'feasible_candidate_certificate.json').write_text(json.dumps(out,indent=2)+'\n');print('coords',out['coordinate_midpoint_approximations'],'gap',float(gap),'seconds',out['seconds'])
