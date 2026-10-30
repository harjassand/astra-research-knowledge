"""Distinguish a protected source instrument from mere symmetric statistics."""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from star_subsystem import representation, hamiltonian, scalar_factor_residual


def reference_infidelity_rate(operators,W,gauge):
    # Initial |Phi>_RL tensor |g>_G; accept every final gauge but the same
    # logical Bell state. Population outside the E isotypic sector fails.
    g=len(gauge); value=0.
    for A in operators:
        a=W.conj().T@A@W
        avg=(a[:g,:g]+a[g:,g:])/2
        aa=W.conj().T@A.conj().T@A@W
        avg_square=(aa[:g,:g]+aa[g:,g:])/2
        value+=float(np.vdot(gauge,(avg_square-avg.conj().T@avg)@gauge).real)
    return value


def run():
    r=representation(); H=hamiltonian(t=.1,epsilon=.4)
    hg=scalar_factor_residual(H,r['W'])[0]
    e,v=eigh(hg); g=v[:,0]
    ns=r['m']['n']
    independent=reference_infidelity_rate(ns[1:],r['W'],g)
    central=reference_infidelity_rate([ns[0]],r['W'],g)
    collective=reference_infidelity_rate([sum(ns[1:])],r['W'],g)
    assert independent>1e-3
    assert abs(central)<1e-12 and abs(collective)<1e-12
    result=dict(t=.1,epsilon=.4,
        independent_equal_outer_number_dephasing_reference_infidelity_rate=independent,
        central_number_dephasing_rate=central,
        collective_outer_number_dephasing_rate=collective,
        convention='Unit coefficient of D[n] for each listed operator; initial logical Bell pair and low charge-gauge state.',
        implication='Equal independent bath spectra produce a permutation-covariant channel, not I_L tensor a gauge channel.',
        conditional_record_warning='I_L tensor K_r can steer L when L and G were already correlated. The trace-preserving sum preserves rho_LR; successful-record-only preservation is not claimed.')
    Path(__file__).with_name('instrument_checks_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__': run()
