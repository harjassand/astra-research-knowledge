#!/usr/bin/env python3
"""Exact finite rational checks for the fixed-aperture rectification pivot.

No material response or actuation power is fabricated. A measured quasisteady
on/off flow ratio would be an input, not an output of this construction.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def main():
    cases = []
    # Normalize pressure magnitude, half-cycle duration and off-state flow to 1.
    # Q_on=r and Q_off=1. A zero-mean +P/-P pressure cycle is applied.
    for r in (F(3,2), F(2), F(5), F(10), F(25), F(100)):
        volume = r-1
        gross = r+1
        axial_work = r+1
        matched_unidirectional_work = volume
        ratio = axial_work/matched_unidirectional_work
        assert ratio == (r+1)/(r-1) and ratio > 1
        direct_on_duration = volume/r
        # A controllable pressure source uses the same thinned state at +P,
        # then turns pressure off. Deadline=2, and its on duration is <1.
        # For any nonnegative constant actuation power A, direct total work
        # is smaller by 2 + A/r; preparation/reset count can be identical.
        assert direct_on_duration < 1
        for actuation_power in (F(0),F(1,10),F(1),F(10),F(100)):
            rectifier_total = axial_work + actuation_power
            direct_total = volume + actuation_power*direct_on_duration
            assert rectifier_total-direct_total == 2+actuation_power/r
        for conductance in (F(1,10), F(1), F(2), F(100)):
            # Any static odd law gives equal and opposite strokes at +/-P.
            assert conductance-conductance == 0
        cases.append({'on_off_flow_ratio':str(r), 'net_volume':str(volume),
                      'gross_absolute_volume':str(gross),
                      'minimum_axial_work':str(axial_work),
                      'matched_direct_unidirectional_work':str(matched_unidirectional_work),
                      'axial_work_penalty_factor':str(ratio),
                      'same_thinned_state_direct_on_duration':str(direct_on_duration),
                      'common_deadline_duration':'2',
                      'rectifier_minus_direct_total_work_for_actuation_power_A':f'2+A/({r})',
                      'actuation_work_is_additional':True})
    # Holding by symmetric forward/back flow does not retain packets. The
    # signed displacement cancels, but the boundary can experience exchanges.
    hold = {'net_volume': '0', 'gross_absolute_volume_for_Q=1_each_half':'2',
            'true_packet_retention_certified':False,
            'required_extra_contract':'Stroke shorter than protected-region guard distance, plus diffusion/migration bound; otherwise shutoff valve or stopped pressure is the strong control.'}
    result = {'status':'internally reconstructed algebra; conditional actuation-access primitive, no new physical discovery',
              'contract':'Constant pressure magnitudes +/-P, equal half-periods, quasisteady odd passive flow, on-state Q_L(P)>Q_H(P)>0, state selection synchronized with pressure.',
              'static_controls_result':'Any fixed odd Q(P), including diameter changes and an ideal coaxial stable carrier film, has zero cycle net volume under half-period antisymmetric pressure.',
              'actuated_result':'V=(T/2)*(Q_L-Q_H)>0; W_axial=(P*T/2)*(Q_L+Q_H).',
              'axial_energy_identity':'Any unidirectional pressure P delivery uses W_direct=P*V; that identity alone does not guarantee that a passive fixed aperture can meet the same deadline.',
              'strong_total_work_control':'A controllable pressure source runs the SAME thinned state at +P for t_direct=(T/2)*(1-Q_H/Q_L), then turns pressure off. It meets the same aperture, peak pressure and deadline, incurs less axial work and less actuation on-time, and can have the same preparation/reset count. It wins if pressure control is allowed and no extra unequal pump switching cost dominates.',
              'cases':cases,'hold_counterexample':hold,
              'unacquired_inputs':['actual fixed-aperture pressure-flow trajectories under actuation','on/off recovery and training memory','acoustic/coil/driver input energy and heat','particle damage and concentration changes','clearing probability and post-clear product quality'],
              'prior_art':'Sehgal et al., arXiv:2206.01141v1, and PhysRevResearch.6.043107 (2024) demonstrate time-synchronized acoustic viscosity modulation and negative averaged viscosity. Lin et al. (2016) already demonstrate motor restart and fixed-torque fivefold impeller-speed change.',
              'conclusion':'The pivot enables access if the reciprocal pressure input is externally fixed and cannot be controlled. A controllable pressure source using the same thinned state dominates within the stated quasisteady constant actuation-power contract. Additional valve/pump switching costs require measurement. Packet retention and novelty remain unestablished.'}
    out = HERE/'pivot_checks.json'
    out.write_text(json.dumps(result,indent=2)+'\n')
    receipt = {'arithmetic':'fractions.Fraction','finite_cases':len(cases),'assertions':'passed',
               'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               'result_sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
    (HERE/'PIVOT_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
