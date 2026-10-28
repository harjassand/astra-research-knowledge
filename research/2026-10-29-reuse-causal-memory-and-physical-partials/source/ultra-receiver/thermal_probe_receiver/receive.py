"""Thin conditional statistical consumer; it never fabricates physical data.

An external source must warrant the model, timestamps, initialization,
calibration and independent-electronics contract. This function cannot
authenticate that scientific evidence from a Boolean or a source hash.
Its result is explicitly conditional on that externally warranted input.
"""
from fractions import Fraction as F
import json
from pathlib import Path

def receive(plan,*,score_sum_interval=None,blocks_observed=0,
            combined_score_mean_calibration_error=None,
            externally_warranted_scientific_access=False):
    required=int(plan.get('blocks_required',plan.get('raw_readouts_required','0')))
    if plan.get('status')=='THIS_VARIANCE_RULE_NOT_QUALIFIED':
        return {'status':'THIS_RULE_NOT_QUALIFIED','hypothesis':None}
    if score_sum_interval is None or combined_score_mean_calibration_error is None:
        return {'status':'NO_QUALIFIED_PHYSICAL_RECORD','hypothesis':None,
                'blocks_required':str(required),'blocks_observed':str(blocks_observed)}
    if not externally_warranted_scientific_access or blocks_observed<required:
        return {'status':'ACCESS_OR_RECORD_NOT_QUALIFIED','hypothesis':None}
    assert required>0 and blocks_observed>0
    sl=F(plan.get('signal_lower',plan.get('signal_interval',['0'])[0]))
    rlo,rhi=map(F,plan['reference_score_interval'])
    vlo,vhi=map(F,score_sum_interval)
    assert rlo<=rhi and vlo<=vhi
    vmean=(vlo+vhi)/(2*blocks_observed);rmean=(rlo+rhi)/2
    rounding=(vhi-vlo)/(2*blocks_observed)+(rhi-rlo)/2
    cal=F(combined_score_mean_calibration_error)
    if cal<0 or cal+rounding>sl/8:
        return {'status':'CALIBRATION_OR_DIGITIZATION_NOT_QUALIFIED','hypothesis':None}
    hypothesis='alpha_at_least_Delta' if rmean-vmean>=sl/2 else 'reference_alpha_zero'
    return {'status':'CONDITIONAL_STATISTICAL_DECISION','hypothesis':hypothesis,
            'each_hypothesis_risk_upper':plan.get('risk_bound_each','1/20'),
            'scope':'Only under the externally warranted model/read/timing/initialization contract and supplied aggregate/calibration bounds. This software does not authenticate device access or establish those premises.'}

if __name__=='__main__':
    packet=json.loads((Path(__file__).resolve().parent/'RECEIVER.json').read_text())
    print(json.dumps({'physical_data_supplied':False,
                     'results':[receive(c['passive_long']) for c in packet['cases']]},indent=2))
