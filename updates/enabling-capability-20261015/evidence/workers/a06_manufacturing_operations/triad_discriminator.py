"""A specified next experiment, not a synthetic optimization or hardware result.

Use the one measured 0.46 N/cm spring calibration for every spring in an
otherwise source-scale three-rotor assembly. Replication needs actual individual
spring calibrations; using one fitted spring for all is a hypothesis.
"""
import itertools
import json
import math
import time
from audit import BASE, pair_torque, drive_torque, root


def length_coupling(w,li,lj,ti,tj):
    return math.hypot(w+lj*math.sin(tj)-li*math.sin(ti),
                      lj*math.cos(tj)-li*math.cos(ti))


def main():
    t0=time.perf_counter()
    measured=json.loads((BASE/'RESULTS.json').read_text())['spring_fits']['0.46']
    k=measured['k_N_per_m']/100
    rest=measured['rest_length_m']*100
    own_angle,neighbour_angle=map(math.radians,[18.3,38.8])
    results={}
    lengths=[]
    for drive_rest in [rest,0.0]:
        key='measured_spring_fit' if drive_rest else 'zero_rest_drive_control'
        results[key]={}
        for own in [-1,1]:
            vals={}
            for left,right in itertools.product([-1,1],repeat=2):
                ti=own*own_angle
                torque=0
                for w,sign in [(-15.24,left),(15.24,right)]:
                    tj=sign*neighbour_angle
                    torque+=pair_torque(k,rest,w,4.731,-4.731,ti,tj)
                    if drive_rest:
                        for a in [-1,1]:
                            lengths.append(length_coupling(w,a*4.731,-a*4.731,ti,tj))
                g=root(lambda g:drive_torque(k,drive_rest,9.4,-8.1,6.31,ti,g)+torque)
                vals[f'{left},{right}']=g
                if drive_rest:
                    lengths.append(math.hypot(g-8.1-6.31*math.sin(ti),9.4+6.31*math.cos(ti)))
            contrast=vals['1,1']-vals['1,-1']-vals['-1,1']+vals['-1,-1']
            results[key]['up' if own==-1 else 'down']=dict(thresholds_cm=vals,mixed_contrast_cm=contrast)
    low,high=[100*x for x in measured['measured_length_range_m']]
    result=dict(status='UNEXECUTED_PHYSICAL_DISCRIMINATOR',
        predicted=results,
        assumptions=dict(spring_k_N_per_cm=k,spring_rest_length_cm=rest,
            spring_source='Fig. 1B A3:B31; one specimen fitted to all springs, not acquired matched parts',
            own_stop_angles_deg=[-18.3,18.3],neighbour_stop_angles_deg=[-38.8,38.8],
            neighbour_spacing_cm=15.24,coupling_arm_cm=4.731,drive_arm_cm=6.31,
            rod_distance_cm=9.4,drive_offset_cm=-8.1,
            neighbours_held_at_stops=True,quasistatic=True,frictionless=True),
        predicted_spring_lengths_at_eight_thresholds_cm=[min(lengths),max(lengths)],
        observed_calibration_length_range_cm=[low,high],
        all_endpoint_lengths_within_source_calibration=all(low<=x<=high for x in lengths),
        midpoint_motion_and_collision_clearance_verified=False,
        contrast_error_if_each_threshold_error_at_most_0_1_cm=0.4,
        caveats=['Component family and dimensions are jointly plausible, not acquired assembled hardware.',
                 'Finite calibration residuals are not a uniform constitutive-law bound.',
                 'Predicted contrast is a diagnostic of the known full model, not new functionality.',
                 'A different local monotone drive coordinate can remove apparent many-body terms for one rotor.'],
        execution_seconds=time.perf_counter()-t0)
    (BASE/'TRIAD_DISCRIMINATOR.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
