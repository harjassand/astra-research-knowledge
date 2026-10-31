#!/usr/bin/env python3
"""Two control levels predict the qualified field family, not an unknown actuator."""
from fractions import Fraction as F
from pathlib import Path
import json
import sys
import time

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs/interventional_generator'
sys.path.insert(0,str(ROOT/'work'))
from interventional_tomography import ProbabilityOracle,make_table,observable,predict_generator,controlled,resolvent,mm,mv,rmv,scale
from interventional_quotient_controls import stationary


def main():
    start=time.perf_counter()
    # Rank four with a repeated within-label hazard: entropy-basis theorem
    # does not apply, while control completeness still does.
    q=[[F(0),F(1),F(2),F(3)],[F(1),F(0),F(4),F(1)],
       [F(1),F(1),F(0),F(1)],[F(2),F(4),F(2),F(0)]]
    for i in range(4):q[i][i]=-sum(q[i])
    f=[1,1,-1,-1];pi=stationary(q);oracle=ProbabilityOracle(q,pi,f)
    table=make_table(oracle,4);o=observable(table)
    # Validation uses the source suffix vectors; the prediction procedure
    # sees only the exact probability table and calibrated rate law.
    columns=[]
    for word in table['suffixes']:
        v=[F(1)]*4
        for c in reversed(word):v=mv(oracle.T[c],v)
        columns.append(v)
    V=[list(row) for row in zip(*columns)];checks=[]
    for s in (F(1,3),F(3,2),F(5)):
        predicted=predict_generator(o,s);actual=controlled(q,f,s)
        assert mm(actual,V)==mm(V,predicted)
        clock_checks=0
        for nu in (F(2,3),F(7,3)):
            assert mm(resolvent(actual,nu),V)==mm(V,resolvent(predicted,nu));clock_checks+=1
        checks.append({'unmeasured_field_multiplier':str(s),'generator_intertwining_exact':True,
                       'unmeasured_clock_resolvent_identities':clock_checks,
                       'all_deterministic_time_semigroups':'follows for every duration from exact generator intertwining'})
    # An alternative symmetric barrier response is EXACTLY identical at
    # training levels1,2 and differs at3. Energy-dependent rate ratios
    # alone, and finite calibration points, cannot exclude it.
    def barrier(s):return 1+F(1,10)*(s-1)**2*(s-2)**2
    assert barrier(F(1))==barrier(F(2))==1
    s=F(3);honest=controlled(q,f,s);wrong=scale(barrier(s),honest)
    for i in range(4):
        for j in range(4):
            if i!=j:assert wrong[i][j]/wrong[j][i]==honest[i][j]/honest[j][i]
    p1=sum(x for x,label in zip(rmv(pi,resolvent(honest,F(1))),f) if label==1)
    p2=sum(x for x,label in zip(rmv(pi,resolvent(wrong,F(1))),f) if label==1)
    assert p1!=p2
    data={'status':'TWO_SETTING_CONTROL_COMPLETENESS_EXACT_CONTROLS_PASSED',
          'fixture':'rank-four, repeated within-label hazards; joint simplicity not used',
          'training_field_multipliers':['1','2'],'training_clock':'1','held_out_controls':checks,
          'alternative_barrier_response':{'formula':'1+(s-1)^2(s-2)^2/10',
               'identical_at_training_levels':True,'all_local_detailed_balance_ratios_unchanged':True,
               'unmeasured_multiplier':'3','first_output_probability_difference_exact':str(p2-p1),
               'first_output_probability_difference_preview':float(p2-p1),
               'conclusion':'global finite-field rate law is a qualified premise, not acquired by fitting two control levels'},
          'new_acquisitions':0,'physical_experiments':0,'elapsed_wall_seconds':time.perf_counter()-start,
          'input_contract':'exact controlled word probabilities plus rank promise; calibrated finite-field law for prediction range'}
    (OUT/'control_closure_receipt.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))


if __name__=='__main__':main()
