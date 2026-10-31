#!/usr/bin/env python3
"""Unknown-strength selective rate gates expose the same hazard algebra."""
from fractions import Fraction as F
from pathlib import Path
import json
import sys
import time

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs/interventional_generator'
sys.path.insert(0,str(ROOT/'work'))
from interventional_tomography import (fixture4,ProbabilityOracle,scaled_crossings,resolvent,diagonal,mm,
    make_table,observable,recover,decode)


def oracle_for(q,pi,f,mp,mn):
    oracle=ProbabilityOracle(q,pi,f);B=resolvent(scaled_crossings(q,f,mp,mn),F(1))
    for k,bit in enumerate((-1,1)):oracle.T[2+k]=mm(B,diagonal([F(x==bit) for x in f]))
    return oracle


def main():
    start=time.perf_counter();q,pi,f=fixture4();out=[]
    for name,mp,mn in [('symmetric_kinetic_gate',F(3,2),F(3,2)),('asymmetric_unknown_gate',F(5,4),F(7,3))]:
        oracle=oracle_for(q,pi,f,mp,mn);table=make_table(oracle,4)
        table['actuation_model']='uniform_label_crossing_scaling';table.pop('field_multiplier')
        result=recover(table)
        assert F(result['identified_plus_crossing_multiplier'])==mp
        assert F(result['identified_minus_crossing_multiplier'])==mn
        hazards=[sum(q[i][j] for j in range(4) if f[i]!=f[j]) for i in range(4)]
        order=sorted(range(4),key=lambda i:(hazards[i],f[i]))
        assert decode(result['Q'])==[[q[i][j] for j in order] for i in order]
        path=OUT/(name+'_table.json');path.write_text(json.dumps(table,indent=2)+'\n')
        out.append({'name':name,'multipliers_recovered_from_probability_operators':[str(mp),str(mn)],
                    'source_generator_recovered_exactly':True,'entropy_rate_preview':result['entropy_rate_preview'],
                    'source_probability_queries':table['source_unique_probability_queries'],
                    'gate_strength_not_supplied_as_input':True})
    boundary=make_table(oracle_for(q,pi,f,F(1),F(2)),4);boundary['actuation_model']='uniform_label_crossing_scaling'
    try:observable(boundary)
    except RuntimeError:boundary_rejected=True
    else:raise AssertionError('zero hazard coefficient silently inverted')
    result={'status':'UNKNOWN_STRENGTH_SELECTIVE_GATE_CONTROLS_PASSED','fixtures':out,
            'one_unchanged_crossing_direction':{'hazard_formula_rejected':boundary_rejected,
                                              'not_a_general_identification_impossibility':True},
            'new_acquisitions':0,'physical_experiments':0,'elapsed_wall_seconds':time.perf_counter()-start,
            'unacquired':'physical uniform gate selectivity and within-label invariance, timing and controller costs'}
    (OUT/'selective_gate_receipt.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
