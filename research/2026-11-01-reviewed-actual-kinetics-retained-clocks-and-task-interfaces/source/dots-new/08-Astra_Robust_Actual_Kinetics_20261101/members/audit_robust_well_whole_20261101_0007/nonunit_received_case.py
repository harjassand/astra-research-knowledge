from pathlib import Path
from fractions import Fraction as F
import importlib.util,json
H=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('robust_nonunit_received',H/'robust_well_kinetics_20261031/receive_robust.py');c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
r=c.fixture(64);r['energy_terms'][63]['coefficient']='1/7';r['mobility_program']={'kind':'constant_diagonal','entries':['64']*63+['32/11']};beta=F(2,3);k=F(7,3);e=F(1,700);dm=F(1,7);mu=F(32,11);alpha=16;ab=1+F(9,16)*k
t={'defect':e,'beta':beta,'kappa':k,'quad_relative':F(1,20),'full_ratio':F(10),'ks_error':F(99,100),'query_absolute_width':F(1),'times':[]};d=c.certify(r,**t);z=d['constants'];checks=[]
def ok(b,k):assert b,k;checks.append(k)
ok(d['acquisition']['pure_coefficient_min']=='1/7'and d['acquisition']['mobility_floor']=='32/11','complete last-axis coercivity and actual mobility minima')
ok(F(z['K_upper'])**2>=F(alpha*alpha,64)/(mu*mu*beta*dm),'non-square beta/dmin K root bound')
ok((F(z['source_S_nominal_factor_upper'])-1)**2>=k*k/(4*mu*mu*beta*dm*ab**3),'non-square beta/dmin S root bound')
ok(F(z['Dmax_upper'])**2>=16*alpha*alpha*k*k/(mu*mu*beta*dm),'non-square beta/dmin global norm root bound')
ok(F(z['density_price_factor_upper'])**2>=(1/(1-e/k))**(2*alpha+1),'nonunit exact H power and root price')
ok(c.verify(r,d,**t)['status']=='PASS','full nonunit literal original-task receiving')
(H/'nonunit_received_results.json').write_text(json.dumps({'status':'PASS','checks':len(checks),'tests':checks,'mean_ratio_display':float(F(d['total_mean_ratio'])),'KS_display':float(F(d['uniform_KS_error_upper']))},indent=2)+'\n');print(json.dumps({'status':'PASS','checks':len(checks)}))
