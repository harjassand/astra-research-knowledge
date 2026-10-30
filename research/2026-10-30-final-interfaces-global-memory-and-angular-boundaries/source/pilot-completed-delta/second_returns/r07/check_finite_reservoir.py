#!/usr/bin/env python3
"""Finite-energy version of the saturation obstruction; no continuing supply."""
from pathlib import Path
import json
import math
import numpy as np

OUT=Path(__file__).resolve().parent


def main():
    T=4096; W=2.2; M=1.; R=.7; K=128; lam=.5; b=.4
    a=math.sqrt(lam); c=math.sqrt(1-lam)
    rng=np.random.default_rng(7201034)
    initial_wavepacket=W*rng.choice(np.array([-1.,1.]),size=T)
    E0=float(np.dot(initial_wavepacket,initial_wavepacket))
    remaining=E0
    q=np.zeros((2,T+1)); y=np.zeros_like(q); dump=np.zeros_like(q)
    adaptive_history=0.; max_energy_residual=0.
    for t in range(T+1):
        # Same adaptive controller can be coupled on identical prefix records.
        x=R*math.tanh(adaptive_history/(t+1)+.3*math.sin(t)) if t<T else R
        w=initial_wavepacket[t] if t<T else 0.
        # Compute the norm of the actual remaining packet state directly;
        # do not let repeated energy subtraction create a negative remainder.
        remaining=float(np.sum(initial_wavepacket[t:]**2)) if t<T else 0.
        nxt=float(np.sum(initial_wavepacket[t+1:]**2)) if t<T else 0.
        signs=np.array([a,-a])
        y[:,t]=signs*x+c*w
        dump[:,t]=c*x-signs*w
        z=np.clip(y[:,t],-M,M)
        mag=np.abs(z)*K
        lo=np.floor(mag)
        fresh=(int(rng.integers(0,65536))+.5)/65536
        q[:,t]=np.sign(z)*(lo+(fresh<mag-lo))/K
        residual=nxt+y[:,t]**2+dump[:,t]**2-remaining-x*x
        max_energy_residual=max(max_energy_residual,float(np.max(np.abs(residual))))
        if t<T:
            assert q[0,t]==q[1,t]
            assert abs(q[0,t])==M
            adaptive_history+=q[0,t]
        remaining=nxt
    assert abs(remaining)<1e-8
    assert q[0,T]!=q[1,T]
    # Small explicit realization: state shift, no input-to-state injection,
    # output row [c,0,...,0,a]. Its omitted dump row completes passivity.
    dimension=8
    S=np.zeros((dimension+1,dimension+1))
    S[:dimension-1,1:dimension]=np.eye(dimension-1)
    S[dimension,0]=c; S[dimension,dimension]=a
    norm=float(np.linalg.norm(S,2))
    assert norm<=1+1e-14
    threshold=(M+a*R)**2/(1-lam)
    result=dict(
        reservoir_coordinates=T,initial_energy=E0,continuing_supply_energy=0,
        background_packet_energy=W*W,all_packet_amplitudes=W,
        exact_generic_sufficient_energy_per_masked_window=threshold,
        indistinguishable_prefix_windows=T,
        first_different_ADC_window=T+1,
        prefix_transcript_disagreements=int(np.sum(q[0,:T]!=q[1,:T])),
        terminal_reservoir_energy=remaining,
        maximum_local_energy_identity_residual=max_energy_residual,
        explicit_small_colligation_operator_norm=norm,
        optimal_commands=[b/(2*math.sqrt(lam)),-b/(2*math.sqrt(lam))],
        minimax_radius_until_prefix_ends=b/(2*math.sqrt(lam)),
        gain_access='same fixed-range ADC, bounded scalar forward/adjoint queries',
        hidden_export_port='dump=c*x-a*w; its energy is charged but not observed',
        state_preparation_and_dimension_are_not_free=True,
        first_tranche_E0_16_masks_at_least_windows=int(16//(W*W)),
        does_not_contradict_first_tranche_65536_window_guarantee=True)
    (OUT/'FINITE_RESERVOIR_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    np.savez_compressed(OUT/'FINITE_RESERVOIR_RECORD.npz',
        initial_wavepacket=initial_wavepacket,ADC=q,analogue_output=y,
        inaccessible_export=dump)
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
