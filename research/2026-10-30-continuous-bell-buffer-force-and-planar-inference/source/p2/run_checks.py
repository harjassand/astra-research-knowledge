"""Run the substantive checks and write a reproducible local results file."""
import json
from pathlib import Path
import numpy as np
from exact_measurement_certificate import certify
from teleportation_check import check
from force_transport import make_intervals,simulate,failure_examples

def within_parity_failure():
    # Even-parity |00> and |11> get two distinguishable positive kicks.
    p=np.arange(-5,5,.01)
    f=np.zeros(len(p)); f[np.abs(p)<.2]=1
    f=f/np.linalg.norm(f)
    # q=+1 on both states, but force strengths 1.3 and .7 for T=2.
    f00=np.roll(f,260); f11=np.roll(f,140)
    overlap=float(np.vdot(f00,f11))
    return {'parity_report_correct_probability':1.,
            'within_even_sector_pointer_overlap':overlap,
            'output_even_bell_fidelity':(1+overlap)/2,
            'positive_force_eigenvalues':[.7,1.3],
            'reason':'Force coefficient depends on a logical bit within the parity eigenspace.'}

def main():
    intervals=make_intervals()
    stress=[]
    for sign in [1,-1]:
        stress.append(simulate(intervals,sign))
    t,h,g=intervals[0]
    constant=[(2.,h,g)]
    stress.append(simulate(constant,1,substeps=128))
    results={'exact_cnot':certify(), 'gate_teleportation':check(),
             'positive_force_stress':stress,
             'operator_gap_failures':failure_examples(),
             'effect_without_instrument_failure':within_parity_failure(),
             'numerical_status':'Ordinary floating point, not certified rounding; analytic proofs carry the uniform claims.'}
    dest=Path(__file__).with_name('results.json')
    dest.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))

if __name__=='__main__': main()
