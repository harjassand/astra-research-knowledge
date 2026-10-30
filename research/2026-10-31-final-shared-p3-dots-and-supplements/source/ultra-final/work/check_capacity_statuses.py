from pathlib import Path
from fractions import Fraction as R
import sys,json,copy,time
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'outputs/shared_mode_gluing'));import verify_field as v
start=time.perf_counter();checks=[]
# A degenerate field has a singular translation block and zero quotient
# capacity. The generalized Schur form must still certify it exactly.
one={'modes':[{'frequency':[1,0],'sine':['1','0']}],'catalogue':[{'weight':'1/2','rank_one_direction':['1','0','0','0']}],'requested_L4_gap':'1/32'}
x=v.verify(one);assert x['status']=='CERTIFIED_FIELD' and x['nine_by_nine_capacity_LMI_verified'];checks.append('singular_translation_block_and_zero_quotient_capacity')
# A genuine catalogue obstruction must be distinguished from QC failure.
triad={'modes':[{'frequency':[1,0],'sine':['1','0']},{'frequency':[0,1],'sine':['0','1']},{'frequency':[1,1],'sine':['1','1']}],'catalogue':[{'weight':'1/2','rank_one_direction':r} for r in (['1','0','0','0'],['0','0','0','1'],['1']*4)]}
x=v.verify(triad);assert x['status']=='FIXED_CATALOGUE_RANGE_OBSTRUCTION';checks.append('fixed_catalogue_range_obstruction')
x=copy.deepcopy(one);x['catalogue'][0]['weight']='1';x=v.verify(x);assert x['status']=='FIXED_CATALOGUE_COVARIANCE_MISMATCH';checks.append('covariance_mismatch')
x=copy.deepcopy(one);x['requested_L4_gap']='2';x=v.verify(x);assert x['status']=='FIXED_CATALOGUE_BUDGET_INSUFFICIENT' and not x['nine_by_nine_capacity_LMI_verified'];checks.append('insufficient_requested_budget')
# Arbitrary-phase Laurent arithmetic is independently compared with the
# all-amplitude construction, with a proper output rotation and signs.
x=v.verify(json.loads((v.HERE/'field_input.json').read_text()));assert x['status']=='CERTIFIED_FIELD' and x['nine_by_nine_capacity_LMI_verified'];checks.append('arbitrary_phase_rational_Gaussian_actual_field')
print(json.dumps({'operation_guards_checked':checks,'seconds':time.perf_counter()-start},indent=2))
