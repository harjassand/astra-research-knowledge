"""Learner: finite port-pulse experiment, no private-source import."""
from fractions import Fraction as Q
from exact import exp_minus, encode, require

def acquire(port):
    p=3;m=4;h=Q(2);lead=Q(1,4096);W=Q(30);R=Q(5,2)
    eta=Q(1,1<<30);zeta=Q(1,1<<32);scale=1<<40
    records=[];G=[[[Q(0) for _ in range(p)] for _ in range(p)] for _ in range(m)]
    for col in range(p):
        port.advance((0,0,0),W)
        for lag in range(m):
            cmd=tuple(int(lag==0 and j==col) for j in range(p))
            port.advance(cmd,h-lead)
            raw=port.read()
            port.advance(cmd,lead)
            for row in range(p):G[lag][row][col]=Q(raw[row],scale)
            records.append({'column':col,'lag':lag,'reported_integers':raw,'fractional_bits':40})
    _,ew,cw=exp_minus(W,96)
    _,et,ct=exp_minus(m*h-lead,96)
    coefficient_error=R*ew+zeta+eta
    initial_error=R*ew
    tail_error=2*et
    coefficient_total=m*p*coefficient_error
    epsilon=initial_error+tail_error+coefficient_total+zeta
    require(epsilon<Q(1,1000))
    return {'record':records,'G':G,'epsilon':epsilon,'p':p,'m':m,'h':h,'lead':lead,'W':W,
            'certificate':{'coefficient_entry_error':coefficient_error,'coefficient_convolution_error':coefficient_total,
             'initial_error':initial_error,'tail_error':tail_error,'deployment_actuation_error':zeta,
             'epsilon':epsilon,'read_error':eta,'actuator_error':zeta,
             'command_L2_cap':Q(1),'command_coordinate_cap':Q(1),'a':Q(1),'tau':Q(1,8),
             'uniform_source_norm_cap':Q(2),'uniform_actuator_norm_cap':Q(2),
             'initial_augmented_output_residue_cap':R,
             'acquisition_trials':p,'vector_reads':p*m,'scalar_reads':p*p*m,
             'acquisition_time':p*(W+m*h),'source_input_active_time':p*h,
             'pulse_command_changes_upper':2*p,'coefficient_scalars':p*p*m,
             'planner_exponential_enclosures':2,'planner_taylor_terms':cw['taylor_terms']+ct['taylor_terms'],
             'clock_jitter_executed':Q(0),'operation_start_relaxation':W,
             'positive_read_to_command_window':lead,'uniform_output_derivative_bound':Q(7),
             'per_interval_source_supply_absolute_bound':Q(4)*h,
             'force_L2_cap':Q(2),'force_slew_L2_cap':Q(32),
             'physical_units':'calibrated source-time and power-conjugate port units; no watts/joules calibration supplied'}}
