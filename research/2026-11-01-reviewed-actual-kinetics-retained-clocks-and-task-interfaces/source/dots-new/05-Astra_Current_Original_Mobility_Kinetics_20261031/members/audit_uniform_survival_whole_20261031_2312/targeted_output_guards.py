from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import importlib.util,json
H=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('guard_survival',H/'uniform_survival_receiver_20261031/receive_survival.py');c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
r=c.fixture(64);t={'times':[F(0),F(1000),F(10000)],'ks_error':F(3,10),'query_absolute_width':F(3,5),'quad_relative':F(1,20),'full_ratio':F(6,5)};a=c.certify(r,**t);checks=[]
def ok(x,k):assert x,k;checks.append(k)
def unknown(fn,k):
 try:fn()
 except c.Unknown:ok(True,k)
 else:raise AssertionError(k)
L=max(a['work']['largest_extra_root_integer_bound_bits'],a['work']['largest_extra_guarded_product_bits'],a['mean_certificate']['work']['largest_root_integer_bound_bits'],a['mean_certificate']['work']['largest_guarded_product_bits'])
ok(c.certify(r,**dict(t,max_integer_bits=L))['queries']==a['queries'],'exact whole guarded integer bound passes')
unknown(lambda:c.certify(r,**dict(t,max_integer_bits=L-1)),'one-below whole guarded integer bound refuses')
b=c.certify(r,**dict(t,precision_bits=16));ok(F(b['initial_law_comparison_error_upper'])>=F(a['initial_law_comparison_error_upper']),'low-precision root contribution is not discarded')
rr=deepcopy(r);rr['energy_terms'].reverse();unknown(lambda:c.verify(rr,a,**t),'changed complete raw order binds even for same polynomial')
cc=deepcopy(a);cc['queries']=cc['queries']*2000;unknown(lambda:c.verify(r,cc,**t),'oversized output list fails exact original-query conjunction')
for k in ['work','seconds']:
 cc=deepcopy(a);del cc[k];ok(c.verify(r,cc,**t)['status']=='PASS','absent diagnostic '+k+' is intentionally not a proof failure')
for fn in [lambda:c.certify(r),lambda:c.certify(r,**dict(t,unrecognized_claim=True))]:
 try:fn()
 except TypeError:ok(True,'outside-Python-signature task is not admitted')
 else:raise AssertionError('unexpected API admission')
rep={'status':'PASS','checks':len(checks),'tests':checks,'exact_whole_guarded_integer_bound_bits':L,'scope':'Additional narrow guard checks; no source edits.'};(H/'targeted_output_guard_results.json').write_text(json.dumps(rep,indent=2)+'\n');print(json.dumps(rep,indent=2))
