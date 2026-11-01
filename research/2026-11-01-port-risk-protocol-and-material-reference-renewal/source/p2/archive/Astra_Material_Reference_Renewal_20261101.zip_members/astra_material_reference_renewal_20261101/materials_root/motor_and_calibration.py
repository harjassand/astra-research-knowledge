"""Thermodynamic and calibration closure tests for renewable rest geometry.

No hardware performance is inferred.  Finite sensors and motor rates are explicit.
"""
from pathlib import Path
import json
import math
import numpy as np
from scipy.optimize import minimize_scalar
from reference_turnover import FiniteOUReadout

HERE=Path(__file__).resolve().parent
OUT=HERE/'results'
OUT.mkdir(exist_ok=True)


def motor_channels(x, affinity, work, coupling=1.0, attempt=1.0):
    """Rates on ONE mechanical edge at fixed x; energies in kBT.

    A forward consumes fuel, A reverse synthesizes it.
    B reverse consumes fuel, B forward synthesizes it.
    Barrier prefactors are the SAME on each edge and its time reversal.
    """
    ap=attempt*math.exp(coupling*x+(affinity-work)/2)
    am=attempt*math.exp(coupling*x-(affinity-work)/2)
    bp=attempt*math.exp(-coupling*x+(-affinity-work)/2)
    bm=attempt*math.exp(-coupling*x-(-affinity-work)/2)
    return ap,am,bp,bm


def motor_test():
    rows=[];err=0.
    for x in [-3,-1,0,1,3]:
        for work in [-4,0,4]:
            A=8.
            ap,am,bp,bm=motor_channels(x,A,work)
            err=max(err,abs(math.log(ap/am)-(A-work)),
                    abs(math.log(bp/bm)-(-A-work)))
            aggregate=math.log((ap+bp)/(am+bm))
            effective=math.log(math.cosh(x+A/2)/math.cosh(x-A/2))
            assert abs(aggregate-(effective-work))<1e-12
            assert abs(effective)<=A+1e-12
            rows.append(dict(x=x,step_work_kBT=work,effective_affinity=effective,
                             forward_reverse_log_ratio=aggregate))
    # At x=0, the motor is not an ideal zero-error holder: load wins.
    zero=motor_channels(0,8,4)
    assert abs(math.log((zero[0]+zero[2])/(zero[1]+zero[3]))+4)<1e-12
    # Energy/fuel feasibility of a desired forward reverse-event contrast.
    A,work,p=12.,4.,0.01
    required=work+math.log((1-p)/p)
    threshold=math.atanh(math.tanh(required/2)/math.tanh(A/2))
    ap,am,bp,bm=motor_channels(threshold,A,work)
    contrast_error=(am+bm)/(ap+bp+am+bm)
    assert abs(contrast_error-p)<1e-10
    # Equal adjacent-state populations are assumed for this local edge contrast;
    # this is NOT the full finite-path repair probability.
    return dict(local_detailed_balance_max_error=err,rows=rows,
                no_latch_zero_signal_log_ratio=-4.,
                finite_contrast_example=dict(affinity_kBT=A,step_work_kBT=work,
                    desired_reverse_edge_contrast=p,required_gate_coordinate=threshold,
                    attained_reverse_edge_contrast=contrast_error),
                caveat='Local edge rate comparison only; actual pathway occupation, latch, and first-passage error remain separate.')


def reciprocal_meter_test(seed=81):
    """Unknown-offset readout plus finite common-mode null calibration.

    A real polarity reversal changes mechanical coupling, not just a digital sign.
    The simulation grants this operation with explicit state-equilibration and
    finite-readout premises; it does not claim a fabricated reversing latch.
    """
    rng=np.random.default_rng(seed)
    k1,k2,kap=0.7,0.9,0.4
    r1,r2=10e-6,10e-6+2e-9
    offset=8e-9; read_gain=1.17; single_sd=0.02e-9
    tau=.001; observation_window=.5; settling_time=.01
    readout=FiniteOUReadout(single_sd,tau,rng,channels=1)
    signal_state=0.0
    L0,L1=10.1e-6,10.6e-6
    def mean_x(L,beta):
        h=k1+k2*beta*beta+kap
        return (k1*(L-r1)-beta*k2*(L-r2))/h
    def read(L,beta,polarity):
        nonlocal signal_state
        target=read_gain*polarity*mean_x(L,beta)
        signal_state=target+(signal_state-target)*math.exp(-settling_time/tau)
        readout.average_noise(settling_time)
        z=math.exp(-observation_window/tau)
        signal_average=target+(signal_state-target)*tau/observation_window*(1-z)
        signal_state=target+(signal_state-target)*z
        return offset+signal_average+readout.average_noise(observation_window)[0]
    def differential(L,beta):
        return (read(L,beta,1)-read(L,beta,-1))/2
    # Finite 18-step nulling search; no stiffness or gap values enter this loop.
    lo,hi=.2,2.0
    for _ in range(18):
        mid=(lo+hi)/2
        measured_change=differential(L1,mid)-differential(L0,mid)
        if measured_change>0:lo=mid
        else:hi=mid
    estimate=(lo+hi)/2
    truth=k1/k2
    levels=np.linspace(9.8e-6,10.9e-6,50)
    noiseless=np.array([read_gain*mean_x(L,estimate) for L in levels])
    observations=np.array([differential(L,estimate) for L in levels])
    h=k1+k2*estimate*estimate+kap
    nominal_signal=read_gain*k1*(r2-r1)/h
    return dict(unknown_offset_m=offset,unknown_read_gain=read_gain,
                observation_windows=4*18+2*len(levels),
                observation_window_s=observation_window,
                settling_time_per_window_s=settling_time,
                noise_correlation_time_s=tau,
                calibration_time_s=4*18*(observation_window+settling_time),
                calibration_and_validation_time_s=readout.elapsed,
                mechanical_ratio_bits=18,
                acquired_arm_ratio=estimate,true_balanced_ratio_for_scoring_only=truth,
                arm_ratio_error=estimate-truth,
                residual_common_length_coefficient=k1-estimate*k2,
                tested_common_length_span_m=levels[-1]-levels[0],
                noiseless_output_span_m=float(np.ptp(noiseless)),
                output_error_including_noise_max_m=float(np.max(abs(observations-nominal_signal))),
                read_noise_sd_per_snapshot_m=single_sd,
                remaining_costs=['finite common deformation probe','18-bit effective lever-ratio setting',
                   'physical polarity reversal and settling','drift between reciprocal records',
                   'actuator/latch/sensor power','endplate rigidity and temperature matching'])


def nonlinear_copy_test():
    G=lambda z:z+2*z**3
    errors=[]; max_sign_errors=0
    for L in np.linspace(-2,2,17):
        for d in [-.1,-.02,0,.03,.1]:
            r1,r2=.25,.25+d
            # Convex branch energy V'=G.  The finite rocker observes a real
            # mechanical coordinate; no input labelled good or bad is supplied.
            V=lambda z: .5*z*z+.5*z**4
            kap=.4
            U=lambda x:V(L-r1-x)+V(L-r2+x)+.5*kap*x*x
            opt=minimize_scalar(U,bounds=(-.2,.2),method='bounded',
                                options={'xatol':1e-13})
            x=opt.x
            if d:
                assert x*d>0
                assert abs(x)<abs(d)/2+1e-10
            else:assert abs(x)<2e-8
            errors.append(abs(x) if d==0 else 0.)
    # Analytic contraction, checked by a finite-time nonautonomous integration.
    from scipy.integrate import solve_ivp
    target=.25;gamma=.7;initial=.1
    def ode(t,e):
        L=1.3*math.sin(5*t)+.2*math.sin(17*t)
        return [gamma*(G(L-target-e[0])-G(L-target))]
    sol=solve_ivp(ode,[0,5],[initial],rtol=1e-10,atol=1e-12,max_step=.01)
    bound=initial*np.exp(-gamma*sol.t)  # G'>=1 everywhere
    assert np.max(abs(sol.y[0])-bound)<1e-9
    return dict(maximum_zero_reference_rocker_displacement=max(errors),
                initial_rest_error=initial,final_rest_error=float(sol.y[0,-1]),
                analytic_final_contraction_bound=float(bound[-1]),
                external_load_or_length_not_an_input_to_comparison=True,
                warning='Matched memoryless force laws and quasistatic branch response; not arbitrary hysteretic materials.')


def main():
    result=dict(motor=motor_test(),reciprocal_calibration=reciprocal_meter_test(),
                nonlinear_copy=nonlinear_copy_test())
    (OUT/'motor_and_calibration_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
