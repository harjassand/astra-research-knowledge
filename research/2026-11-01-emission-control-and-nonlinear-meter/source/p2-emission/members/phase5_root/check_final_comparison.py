"""Reproduce the deliberately generous calibrated baseline from saved data."""
from pathlib import Path
import json
import sys

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'phase5_autonomous'))
from joint_postprocess import dec,phase_oracle
from joint_gaussian_instrument import gate_choi

out={}
for label in ('nonlinear_mean_unmod','nonlinear_mean_mod'):
    x=json.loads((BASE/'phase5_autonomous'/f'joint_{label}_results.json').read_text())
    w=[dec(x['reported_plus_instrument']),dec(x['reported_minus_instrument'])]
    J,e,b=gate_choi(w,return_branches=True)
    ep,ph=phase_oracle(b)
    Js,es,bs=gate_choi(w,qx=.001,qprep=.001,return_branches=True)
    eps,_=phase_oracle(bs)
    out[label]={
        'raw_entanglement_infidelity':e,
        'phase_oracle_entanglement_infidelity':ep,
        'raw_with_0p1percent_preparation_and_X_readout':es,
        'phase_oracle_with_same_preparation_and_X_readout':eps,
        'storage_loss_probability_bound_at_ratio_1e4':x['storage_loss_probability_bound_for_kappa1_over_kappa2_1e_minus4'],
        'max_assignment_error':x['max_parity_assignment_error']}
(Path(__file__).with_name('final_corrected_gate_comparison.json')).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
