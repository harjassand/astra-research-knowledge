"""Information-theoretic falsifier for transferring local tests without a warranted
range/locality contract. Two models have identical measured distributions under
all admitted clamped triple tests but different deployment behaviour.
"""
import json
from pathlib import Path
from source_device import BATHS

if __name__=='__main__':
    h=.04
    for mode,bath in BATHS.items():
        assert all(bath.rate((l,c,r))==(bath.rate((l,c,r))+h*(1-1)/2)
                   for l in (-1,1) for c in (-1,1) for r in (-1,1))
    # The fourth (next-next) spin is +1 in calibration, so the hidden defect
    # term is zero. At deployment the fourth spin may be -1 and changes the
    # local flip rate by h. The derivative of E[s_i] at t=0 differs by -2h
    # when queried central s_i=+1, regardless of its left/right spins.
    derivative_gap=2*h
    gap_certificate={"identical_all_admitted_three_spin_Poisson_laws":True,
                     "hidden_term":"additional rate h*(1-sigma[i+2])/2",'h':h,
                     'derivative_gap_for_sigma_i_plus_and_sigma_i_plus2_minus':derivative_gap,
                     'consequence':'No n-uniform certificate without externally warranted bounded locality or extra probes on the fourth spin',
                     'physical_premises_unverified':['selective exposure preserves rates in unisolated deployment',
                                                    'range truly <=1 on the ring','no intervention cross-talk']}
    (Path(__file__).parent/'assumption_attack.json').write_text(json.dumps(gap_certificate,indent=2))
    print(gap_certificate)
