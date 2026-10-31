#!/usr/bin/env python3
"""Independent physical conventions: equilibrium, constant field and time units."""
from fractions import Fraction as F
from pathlib import Path
import json
import sys
import time
import numpy as np

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs/interventional_generator'
sys.path.insert(0,str(ROOT/'work'))
from interventional_opening import cycle
from interventional_work_receiver import certify,controlled


def main():
    start=time.perf_counter();data=json.loads((OUT/'retuned_receipt.json').read_text())
    q=[[F(x) for x in row] for row in data['Q']];f=data['labels'];n=len(q)
    ratios=list(map(F,data['field_multipliers']));dt=F(data['step_duration']);candidate=data['source']['periodic_initial']
    equilibrium=[[(q[i][j]+q[j][i])/2 if i!=j else F(0) for j in range(n)] for i in range(n)]
    for i in range(n):equilibrium[i][i]=-sum(equilibrium[i])
    proposal=cycle(equilibrium,np.array([1/n]*n),np.array(f),ratios,dt)
    eq=certify(equilibrium,f,ratios,dt,proposal['periodic_initial'])
    assert F(eq['cyclic_work_on_interval'][0])>0
    assert eq['chemical_fuel_input_interval']==['0','0']
    constant=certify(q,f,[F(1)]*16,dt,[1/n]*n)
    assert constant['cyclic_work_on_interval']==['0','0']
    base=certify(q,f,ratios,dt,candidate);factor=F(7,3)
    scaled=[[factor*x for x in row] for row in q]
    for t in ratios:assert [[x*dt/factor for x in row] for row in controlled(scaled,f,t)]==[
        [x*dt for x in row] for row in controlled(q,f,t)]
    timed=certify(scaled,f,ratios,dt/factor,candidate)
    lo=max(F(base['cyclic_work_on_interval'][0]),F(timed['cyclic_work_on_interval'][0]))
    hi=min(F(base['cyclic_work_on_interval'][1]),F(timed['cyclic_work_on_interval'][1]))
    assert lo<=hi and base['chemical_fuel_input_interval']==timed['chemical_fuel_input_interval']
    assert F(timed['period'])*factor==F(base['period'])
    result={'status':'INTERVENTIONAL_WORK_PHYSICAL_CONVENTION_CONTROLS_PASSED',
            'equilibrium_same_protocol':{'detailed_balance_exact':True,'chemical_fuel':'0',
                                         'work_on_preview':eq['cyclic_work_on_preview'],'strictly_positive':True},
            'constant_field_zero_work_exact':True,
            'physical_time_unit_change':{'rate_factor':str(factor),'duration_factor':str(1/factor),
                                         'all_held_generator_times_exactly_equal':True,
                                         'work_intervals_overlap':True,'chemical_fuel_intervals_identical':True},
            'new_acquisitions':0,'physical_experiments':0,'elapsed_wall_seconds':time.perf_counter()-start,
            'scope':'model consistency and receiver checks; no empirical device validation'}
    (OUT/'work_controls_receipt.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
