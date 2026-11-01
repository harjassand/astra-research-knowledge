from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import importlib.util,json
H=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('robust_parameter_check',H/'robust_well_kinetics_20261031/receive_robust.py');c=importlib.util.module_from_spec(s);s.loader.exec_module(c);checks=[]
def ok(x,k):assert x,k;checks.append(k)
raw=c.fixture(64);task={'defect':F(1,1000),'quad_relative':F(1,20),'full_ratio':F(2),'ks_error':F(3,4),'query_absolute_width':F(1),'times':[F(0),F(1000),F(10000)]};a=c.certify(raw,**task)
rr=deepcopy(raw);rr['mobility_program']['value']='1/3';b=c.certify(rr,**dict(task,beta=F(9),times=[9*t for t in task['times']]))
ok(all(F(b['mean_hitting_time'][side])==9*F(a['mean_hitting_time'][side])for side in ['lower','upper']),'actual beta mobility scaling multiplies mean time by nine')
ok(F(b['reference_exponential_rate'])==F(a['reference_exponential_rate'])/9 and b['uniform_KS_error_upper']==a['uniform_KS_error_upper'],'actual beta mobility scaling preserves KS but changes reference clock')
ok([q['cdf']for q in a['queries']]==[q['cdf']for q in b['queries']],'absolute query times must scale with physical parameters')
# Last-axis minima, non-square beta/dmin and rational nonunit defect/profile.
rr=c.fixture(64);rr['energy_terms'][63]['coefficient']='1/7';rr['mobility_program']={'kind':'constant_diagonal','entries':['64']*63+['32/11']};tt=dict(task,beta=F(2,3),kappa=F(3,7),defect=F(1,700),full_ratio=F(10),ks_error=F(99,100),times=[])
# A broad external request still cannot override the finite structural KS gate.
try:d=c.certify(rr,**tt)
except c.Unknown as exc:
 ok(str(exc)=='actual robust all-time KS bound misses original tolerance','nonunit full source case remains honest if structural KS fails');d=None
if d is not None:
 ok(d['acquisition']['pure_coefficient_min']=='1/7'and d['acquisition']['mobility_floor']=='32/11','full nonfirst-axis minima under uncertain family')
 z=d['constants'];beta=F(2,3);kap=F(3,7);mu=F(32,11);dm=F(1,7);alpha=16;ab=1+F(9,16)*kap
 ok(F(z['K_upper'])**2>=F(alpha*alpha,64)/(mu*mu*beta*dm),'nonsquare K root under nonunit actual parameters')
 ok((F(z['source_S_nominal_factor_upper'])-1)**2>=kap*kap/(4*mu*mu*beta*dm*ab**3),'nonsquare S correction root under nonunit parameters')
 ok(F(z['Dmax_upper'])**2>=16*alpha*alpha*max(kap,F(1))**2/(mu*mu*beta*dm),'nonsquare global transport root under nonunit parameters')
 ok(c.verify(rr,d,**tt)['status']=='PASS','full nonunit literal task receiver')
# Exact-exp reference order is sufficient for the actual max precision.
from math import factorial
ok((1<<321)*factorial(321)>1<<2500,'degree321 alternating adjacent gap below 2^-2500 on reduced half interval')
rep={'status':'PASS','checks':len(checks),'tests':checks,'nonunit_case_received':d is not None};(H/'targeted_parameter_results.json').write_text(json.dumps(rep,indent=2)+'\n');print(json.dumps(rep,indent=2))
