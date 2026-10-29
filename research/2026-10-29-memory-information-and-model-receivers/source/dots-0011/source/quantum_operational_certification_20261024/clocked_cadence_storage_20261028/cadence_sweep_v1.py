#!/usr/bin/env python3
"""Finite source-informed diagnostic cadence grid; no learning/holdout claim.
Carries actual physical encoded state across r native uses and each real EC.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
from pathlib import Path
import sys,json,hashlib,numpy as np
HERE=Path(__file__).parent;Q=HERE.parent
sys.path.insert(0,str(Q/'clocked_flagged_storage_20261028'));import clocked_channel_v1 as m
sys.path.insert(0,str(Q/'endpoint_oracle_acquisition_20261028'));from oracle_and_endpoint_fit_v1 import oracle
CLOCK={'one':1.,'two':2.,'prep':2.,'measure':4.,'feedback':1.}
PLAN={'eta':.001,'background_integral_per_EC_window':[.03,.1,.3],'mandatory_native_uses':[32,64],'cadences':[1,2,4,8,16,32],'native_inverse_phase_time_per_use':2.,'scope':'Source-informed diagnostic grid, not acquired cadence selection; actual physical reuse and same-elapsed matching per policy.'}

def main():
 (HERE/'PLAN_v1.json').write_text(json.dumps(PLAN,indent=2)+'\n');mts=m.native();initial,D=m.code_coordinates();rows=[]
 for integrated in PLAN['background_integral_per_EC_window']:
  F,timing=m.build_ec(PLAN['eta'],integrated/201,CLOCK)
  idle=np.diag([1,np.exp(-integrated),np.exp(-integrated),1])
  for T in PLAN['mandatory_native_uses']:
   for r in PLAN['cadences']:
    assert T%r==0;count=T//r;local=[np.linalg.matrix_power(M,r) for M in mts];A=initial.copy()
    for _ in range(count):
     for q,M in enumerate(local):A=m.local(A,M,[q],5)
     A=F@A
    score=m.old.metrics(D@A);base=[]
    for site,M in enumerate(local):
     E=np.linalg.matrix_power(idle@M,count);_,fe=oracle(E)
     base.append({'site':site,**m.old.metrics(E),'full_CPTP_terminal_oracle_entanglement_fidelity':fe})
    # External known comparator theorem: best native amplitude-damping
    # concurrence multiplier399/401, dephasing multiplier exp(-integrated).
    adaptive_ceiling=(1+(399/401)**T*np.exp(-count*integrated))/2
    row={'background_integral_per_EC_window':integrated,'native_uses':T,'cadence_r':r,'EC_windows':count,'encoded_native_carrier_exposures':5*T,'unencoded_native_carrier_exposures_per_site':T,'elapsed_reference_time':2*T+count*timing['total_EC_time'],'encoded':score,'same_elapsed_unencoded':base,'source_informed_all_adaptive_single_carrier_Fe_upper':adaptive_ceiling,'feasible_classical_measure_store_reprepare_Fe':.5,'encoded_Fe_exceeds_all_adaptive_single_carrier_ceiling':1-score['entanglement_infidelity']>adaptive_ceiling}
    rows.append(row)
   print('done integral',integrated,'T',T,flush=True)
 out={'status':'AUTHOR_DETERMINISTIC_ACTUAL_CADENCE_GRID_PENDING_REVIEW','plan':PLAN,'clock':CLOCK,'sources':{str(p.relative_to(Q)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Q/'clocked_flagged_storage_20261028/clocked_channel_v1.py',Q/'clocked_flagged_storage_20261028/GOVERNING_CLOCK_MODEL_v1.md',Q/'five_qubit_acquired_frame_pilot_20261028/models.npz',Q/'clocked_flagged_storage_20261028/adaptive_single_carrier_bound_v1.md']},'rows':rows}
 (HERE/'results_v1.json').write_text(json.dumps(out,indent=2)+'\n')
 print('DONE',len(rows),flush=True)
if __name__=='__main__':main()
