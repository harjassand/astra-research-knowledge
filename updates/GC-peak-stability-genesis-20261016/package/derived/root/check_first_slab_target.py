"""Exact stopped-counting certificate for actual first-hit output, not full-state accuracy."""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import hashlib,json,sys
if hasattr(sys,"set_int_max_str_digits"):sys.set_int_max_str_digits(0)

def b(n):return F('2.676')*n*(n-1)+F('108.102')
def d(n):return F('.040')*n*(n-1)*(n-2)+F('37.881')*n
h=F(1,10000);D=F('8.2207')
# Taylor tail after degree18 is bounded geometrically: next term1/19!, later ratios<=1/20.
e_upper=sum((F(1,factorial(i)) for i in range(19)),F(0))+F(20,19*factorial(19))
assert e_upper<F(271828183,100000000)
def exp_lower(x):
 term=F(1);total=term
 for k in range(1,257):term*=x/k;total+=term
 return total

def tail(mu,k):
 assert 0<mu<k
 return e_upper**k*(mu/k)**k/exp_lower(mu)
rows=[]
for U in range(125,139):
 up=(b(U)+3*D*U)*h;death=8*d(U)*h;k=U+1-50
 p_upper=8*tail(up,k);p_death=tail(death,280);bound=p_upper+p_death
 rows.append((bound,U,p_upper,p_death,up,death,k))
bound,U,pu,pd,up,death,k=min(rows)
assert bound<F(1,10**65)
result={'scope':'Actual capped or unbounded eight-site target first-hit probability by h=1e-4 from all50; no full-state or T1 propagation guarantee.','h':str(h),'upper_stop_coordinate':U+1,'U':U,'up_count_threshold':k,'total_death_count_threshold':280,'up_poisson_mean':str(up),'total_death_poisson_mean':str(death),'up_exit_bound_exact':str(pu),'target_before_upper_exit_bound_exact':str(pd),'target_probability_bound_exact':str(bound),'target_probability_strict_upper':'1/10^65','descriptive_bound':float(bound),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'proof':'STOPPED_TARGET_FIRST_SLAB.md','physical_parameters_measured':False,'solver_advantage_established':False}
Path(__file__).with_name('FIRST_SLAB_TARGET_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if not k.endswith('_exact')},indent=2))
