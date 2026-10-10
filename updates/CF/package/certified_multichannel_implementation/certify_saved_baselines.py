"""Reference-dependent certificates for saved CF4 endpoints.
Not a certified CF4 integrator and not an independent validation algorithm.
"""
from pathlib import Path
from fractions import Fraction as F
import json,time
BASE=Path(__file__).parent
rows=json.loads((BASE/'exploratory_manifest_results.json').read_text())['rows'];out=[]
for rowid in ['B4_f0_s20','B6_f0_s20','B3_f0_s36']:
 start=time.perf_counter();reference=json.loads((BASE/f'certified_expression_{rowid}.json').read_text());q=2**reference['endpoint_denominator_power_of_two']
 if rowid=='B6_f0_s20':base=json.loads((BASE/'cf4_B6_f0_s20_safety1.json').read_text())
 else:base=next(x for x in rows if x['id']==rowid)['baseline']
 distance=F(0)
 for i in range(3):
  for j in range(3):
   for k in range(2):distance+=abs(F(base['endpoint'][i][j][k])-F(int(reference['endpoint_exact_dyadic_integer_pairs'][i][j][k]),q))
 err=F(int(reference['global_operator_error_upper_integer']),2**reference['global_error_fraction_bits'])+distance
 target=F(reference['requested_operator_error'])
 out.append({'row_id':rowid,'certificate_type':'reference-dependent exact endpoint distance bound','independent_certified_cf4_implementation':False,'raw_cf4_solver_seconds':base['seconds'],'reference_construction_seconds':reference['total_charged_seconds'],'distance_validation_seconds':time.perf_counter()-start,'exact_entrywise_l1_distance':str(distance),'cf4_operator_error_upper':str(err),'cf4_operator_error_upper_approximate':float(err),'target_met_exactly':err<=target,'timing_interpretation':'Raw CF4 time is reported separately. Its endpoint certification depends on constructing or reusing the supplied certified reference; this is not a fair production-cost ranking.'})
(BASE/'CF4_REFERENCE_DEPENDENT_CERTIFICATES.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
