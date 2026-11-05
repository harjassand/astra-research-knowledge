"""Retained passive source, finite position-box acquisition, fresh readiness.

This is a floating physical-source illustration and an exact rational report
encoder.  It is not an interval-validated ODE or a laboratory experiment.
The learner receives only finite reports and public bounds.  No source matrix,
mode frequency, hidden state, or exact step response is passed to learn_table.
"""
from __future__ import annotations
import hashlib
import json
import math
from fractions import Fraction as Q
from pathlib import Path
from time import perf_counter

import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm

ROOT = Path(__file__).resolve().parent
SOURCE_SEED = 2026110501
CLOCK_CAL_SEED = 2026110502
CLOCK_DEP_SEED = 2026110503
NOISE_CAL_SEED = 2026110504
NOISE_DEP_SEED = 2026110505
T = Q(1)
A = Q(1)
H = Q(1,50)
B = Q(1,200)
DELTA = Q(1,100)
CLEAR = Q(1,5000)
TAU_SENSOR = Q(1,100000)
CLOCK = Q(1,1000000)
PROGRAM_CLOCK = Q(1,100000000)
LATENCY = Q(1,100)
E_INITIAL = Q(1,5)
E_DEP = Q(1,2)
E_DEP_DURING = Q(7,10)
ALPHA_Q = Q(1,50)
DELTA_CAL = Q(1,50)
DELTA_DEP = Q(1,25)
V_X = Q(1,10000000000)
METER_BIAS = Q(1,10000)
NOISE_CAL = Q(1,1000)
NOISE_DEP = Q(3,5000)
FORCE_ERROR = Q(1,100000)
BACKACTION = Q(1,1000000)
ADC_BITS = 20
ADC_HALF_RANGE = Q(2)
ADC_STEP = 2*ADC_HALF_RANGE / 2**ADC_BITS
D_CAL = CLEAR+2*B+T+H+2*CLOCK
D_DEP = CLEAR+B+LATENCY+T+2*CLOCK


def fq(x):
    return str(x if isinstance(x,Q) else Q(x))


def next_power_two(q):
    n=(q.numerator+q.denominator-1)//q.denominator
    return 1 << max(0,(n-1).bit_length())


def smooth(s):
    if s<=0: return 0.
    if s>=1: return 1.
    return s*s*s*(10+s*(-15+6*s))


def make_source():
    """Physical generator only: energy is half the squared state norm."""
    omega=np.array([.003,.019,.11,.7,1.3,3.1,7.,13.,29.,61.,113.,5.7])
    damp=np.array([0.,0.,0.,0.,.0001,.0002,.0001,0.,.00005,0.,0.,0.])
    gain=np.array([.04,.07,.12,.18,.23,.31,.29,.20,.15,.10,.04,0.])
    theta=np.array([.2,.7,1.1,1.4,.3,2.,.9,1.8,2.4,.5,1.6,0.])
    n=2+2*len(omega)
    mat=np.zeros((n,n))
    mat[0,1]=1.
    mat[1,0]=-1.
    mat[1,1]=-1.
    for j,(om,da,ga,th) in enumerate(zip(omega,damp,gain,theta)):
        ix=2+2*j
        c=ga*np.array([math.cos(th),math.sin(th)])
        mat[1,ix:ix+2]=-c
        mat[ix:ix+2,1]=c
        mat[ix:ix+2,ix:ix+2]=np.array([[-da,-om],[om,-da]])
    inp=np.zeros(n); inp[1]=1.
    rng=np.random.default_rng(SOURCE_SEED)
    initial=rng.normal(size=n)
    initial *= math.sqrt(2*float(E_INITIAL)/(initial@initial))
    # This fixture is generated before either private-clock emulation draw.
    return mat,inp,initial,dict(omega=omega.tolist(),damping=damp.tolist(),
                                gain=gain.tolist(),angle=theta.tolist())


def energy(state):
    return float(state@state/2)


def sensor_segment(mat,inp,start,stop,force,breakpoints):
    """Retain physical state; initialize only the finite sensor/integrator."""
    n=len(start)
    aug=np.zeros(n+2)
    aug[:n]=start
    tau=float(TAU_SENSOR)
    jac=np.zeros((n+2,n+2))
    jac[:n,:n]=mat
    jac[n,0]=1/tau
    jac[n,n]=-1/tau
    jac[n+1,n]=1.
    def rhs(t,y):
        out=jac@y
        out[:n]+=inp*force(t)
        return out
    pieces=[]
    last=0.
    count={"nfev":0,"njev":0,"nlu":0}
    for end in sorted(set([float(stop)]+[float(z) for z in breakpoints if 0<float(z)<float(stop)])):
        sol=solve_ivp(rhs,(last,end),aug,method="Radau",jac=jac,
                      rtol=2e-10,atol=2e-12,dense_output=True,
                      max_step=.002)
        if not sol.success: raise RuntimeError(sol.message)
        pieces.append((last,end,sol.sol))
        aug=sol.y[:,-1]
        last=end
        for k in count: count[k]+=getattr(sol,k)
    def value(t):
        t=float(t)
        for lo,hi,fn in pieces:
            if lo-1e-12<=t<=hi+1e-12:
                return fn(min(max(t,lo),hi))
        raise ValueError(("time outside segment",t))
    def mean(lo,hi):
        return float((value(hi)[n+1]-value(lo)[n+1])/(float(hi)-float(lo)))
    return value,mean,aug[:n].copy(),count


def adc(value):
    """Actual finite quantization; throw on overflow rather than clipping."""
    z=int(round(value/float(ADC_STEP)))
    if z < -(2**(ADC_BITS-1)) or z > 2**(ADC_BITS-1)-1:
        raise RuntimeError("finite ADC overflow")
    return Q(z)*ADC_STEP


def learn_table(times,raw_baseline,raw_reports,public):
    """No physical source arguments enter this operation."""
    amp=Q(public["amplitude_exact"])
    upper=Q(public["step_range_upper_exact"])
    values=[Q(0)]
    for r in raw_reports:
        values.append(min(upper,max(Q(0),(Q(r)-Q(raw_baseline))/amp)))
    assert len(times)==len(values)
    return values


def write_json(path,data):
    path.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n")


def main():
    started=perf_counter()
    mat,inp,state,hidden=make_source()
    initial_energy=energy(state)
    initial_state=state.copy()
    n_cal=next_power_two(E_INITIAL*D_CAL/(ALPHA_Q*DELTA_CAL**2))
    n_dep=next_power_two(E_DEP*D_DEP/(ALPHA_Q*DELTA_DEP**2))
    j_cal=int(np.random.default_rng(CLOCK_CAL_SEED).integers(n_cal))
    wait_cal=Q(j_cal)*D_CAL
    state=expm(mat*float(wait_cal))@state
    cal_selected_state=state.copy()
    cal_free_energy=energy(state)
    clear_start=CLOCK
    baseline_start=CLOCK+CLEAR
    force_start=baseline_start+B
    off_start=force_start+T+B
    off_end=off_start+H
    def cal_force(t):
        s=t-float(force_start)
        if s<0:return 0.
        if s<float(H):return smooth(s/float(H))
        if t<float(off_start):return 1.
        if t<float(off_end):return 1.-smooth((t-float(off_start))/float(H))
        return 0.
    cal_val,cal_mean,state,cal_counts=sensor_segment(
        mat,inp,state,D_CAL,cal_force,
        [clear_start,baseline_start,force_start,force_start+H,off_start,off_end])
    noise_cal_rng=np.random.default_rng(NOISE_CAL_SEED)
    sigma=math.sqrt(float(V_X/B))
    # Declared deterministic sensor allowance is much larger than this fixture's
    # fixed calibration offset; actual filter lag and finite ADC are simulated.
    actual_meter_offset=2e-6
    baseline_ideal=cal_mean(baseline_start,force_start)
    baseline_noise=float(noise_cal_rng.normal(0,sigma))
    baseline_report=adc(baseline_ideal+actual_meter_offset+baseline_noise)
    times=[Q(j,100) for j in range(101)]
    means=[]; noises=[]; reports=[]
    for t in times[1:]:
        mean=cal_mean(force_start+t,force_start+t+B)
        noise=float(noise_cal_rng.normal(0,sigma))
        means.append(mean); noises.append(noise)
        reports.append(adc(mean+actual_meter_offset+noise))
    public=dict(amplitude_exact="1",step_range_upper_exact="2")
    values=learn_table(times,fq(baseline_report),list(map(fq,reports)),public)
    cal_terms={
      "quiet":DELTA_CAL/A,
      "finite_positive_ramp":Q(2)*H/2,
      "finite_position_box":Q(2)*B/2,
      "linear_interpolation":Q(2)*DELTA/2,
      "deterministic_meter_difference":2*METER_BIAS/A,
      "simultaneous_meter_noise":NOISE_CAL/A,
      "finite_clock":2*CLOCK,
      "force_and_backaction":Q(33,2000000),
    }
    response_error=sum(cal_terms.values(),Q(0))
    cal_energy_after=energy(state)
    cal_end_state=state.copy()
    # Conservative physical energy ledger including the permitted force error.
    # The complete ramp/hold/off nominal force-square integral is exact.
    ramp_square=Q(181,462)
    nominal_probe_energy=(T+B-H)+2*H*ramp_square
    actual_probe_energy_bound=(math.sqrt(float(nominal_probe_energy))
        +(float(FORCE_ERROR)+float(BACKACTION))*math.sqrt(float(D_CAL)))**2
    cal_energy_bound=float(E_INITIAL)+actual_probe_energy_bound/4
    assert cal_energy_bound<float(E_DEP)

    # New independent random index, same physical state.  No source reset.
    j_dep=int(np.random.default_rng(CLOCK_DEP_SEED).integers(n_dep))
    wait_dep=Q(j_dep)*D_DEP
    state=expm(mat*float(wait_dep))@state
    dep_selected_state=state.copy()
    dep_energy_before=energy(state)
    dep_baseline_start=CLOCK+CLEAR
    dep_baseline_end=dep_baseline_start+B
    dep_force_start=dep_baseline_end+LATENCY
    query_ramp=Q(1,20)
    query_amplitude=Q(4,5)
    dep_off_start=dep_force_start+T
    dep_off_end=dep_off_start+H
    dep_stop=D_DEP+H
    def dep_force(t):
        s=t-float(dep_force_start)
        if s<0:return 0.
        if s<float(query_ramp):
            return float(query_amplitude)*smooth(s/float(query_ramp))
        if t<float(dep_off_start):return float(query_amplitude)
        if t<float(dep_off_end):
            return float(query_amplitude)*(1.-smooth((t-float(dep_off_start))/float(H)))
        return 0.
    dep_val,dep_mean,state,dep_counts=sensor_segment(
        mat,inp,state,dep_stop,dep_force,
        [CLOCK,dep_baseline_start,dep_baseline_end,dep_force_start,
         dep_force_start+query_ramp,dep_off_start,dep_off_end])
    noise_dep_rng=np.random.default_rng(NOISE_DEP_SEED)
    dep_baseline_true=dep_mean(dep_baseline_start,dep_baseline_end)
    dep_baseline_noise=float(noise_dep_rng.normal(0,sigma))
    dep_baseline=adc(dep_baseline_true+actual_meter_offset+dep_baseline_noise)

    # Round sound square-root bounds upward to convenient exact rationals.
    baseline_backaction_bound=Q(11,100000000)
    actual_baseline_bound=2*float(BACKACTION)*math.sqrt(float(CLEAR+B))/math.sqrt(2)
    assert actual_baseline_bound<float(baseline_backaction_bound)
    delivery_bound=Q(1,125000) # 8e-6
    actual_delivery_bound=(float(FORCE_ERROR)+float(BACKACTION))*math.sqrt(float(T)/2)
    assert actual_delivery_bound<float(delivery_bound)
    readiness_terms={
       "quiet":DELTA_DEP,
       "deterministic_baseline_meter":METER_BIAS,
       "baseline_noise":NOISE_DEP,
       "baseline_only_backaction":baseline_backaction_bound,
    }
    readiness=sum(readiness_terms.values(),Q(0))
    diagnostic_t=np.linspace(0,1,2001)
    physical=np.array([dep_val(dep_force_start+Q(str(t)))[:len(state)]
                       for t in diagnostic_t])
    free=np.array([expm(mat*float(dep_force_start+Q(str(t))))@dep_selected_state
                   for t in diagnostic_t])
    zero_source=np.zeros(len(state))
    zero_response_matrix=np.zeros((len(state)+1,len(state)+1))
    zero_response_matrix[:len(state),:len(state)]=mat
    zero_response_matrix[:len(state),-1]=inp
    zero_initial=np.zeros(len(state)+1);zero_initial[-1]=1.
    true_step=np.array([(expm(zero_response_matrix*float(t))@zero_initial)[0]
                        for t in times])
    sampled_table_error=float(np.max(np.abs(np.array(list(map(float,values)))-true_step)))
    free_baseline=float(np.mean([
        (expm(mat*float(z))@dep_selected_state)[0]
        for z in np.linspace(float(dep_baseline_start),float(dep_baseline_end),101)]))

    # A total confidence ledger uses rounded-up meter tail allowances.
    alpha_noise_cal=Q(1,250)
    alpha_noise_dep=Q(1,250)
    alpha_overflow=Q(1,1000000)
    joint_success=1-2*ALPHA_Q-alpha_noise_cal-alpha_noise_dep-2*alpha_overflow
    assert 200*math.exp(-12.5)<float(alpha_noise_cal)
    assert 2*math.exp(-9)<float(alpha_noise_dep)
    force_backaction_actual=(2*float(BACKACTION)
        +float(FORCE_ERROR)+float(BACKACTION))*math.sqrt(float(D_CAL)/2)
    assert force_backaction_actual<float(cal_terms["force_and_backaction"])

    resources={
      "physical_horizon_exact":"1","calibration_amplitude_exact":"1",
      "calibration_ramp_exact":fq(H),"readout_box_exact":fq(B),
      "sample_mesh_exact":fq(DELTA),"sensor_clearing_exact":fq(CLEAR),
      "sensor_time_constant_exact":fq(TAU_SENSOR),
      "clock_tolerance_exact":fq(CLOCK),
      "within_program_time_tolerance_exact":fq(PROGRAM_CLOCK),
      "postread_latency_exact":fq(LATENCY),
      "calibration_slot_exact":fq(D_CAL),"deployment_slot_exact":fq(D_DEP),
      "calibration_slots":n_cal,"deployment_slots":n_dep,
      "calibration_private_bits":int(math.log2(n_cal)),
      "deployment_private_bits":int(math.log2(n_dep)),
      "calibration_selected_index":j_cal,"deployment_selected_index":j_dep,
      "calibration_actual_wait_exact":fq(wait_cal),
      "deployment_actual_wait_exact":fq(wait_dep),
      "worst_total_protocol_time_exact":fq(n_cal*D_CAL+n_dep*D_DEP+H),
      "actual_protocol_time_exact":fq(wait_cal+D_CAL+wait_dep+D_DEP+H),
      "raw_position_boxes":102,"adc_bits":ADC_BITS,"adc_half_range_exact":"2",
      "adc_step_exact":fq(ADC_STEP),
      "raw_adc_payload_bits":102*ADC_BITS,
      "sensor_resets":2,"source_resets":0,
      "initial_energy_bound_exact":fq(E_INITIAL),
      "deployment_start_energy_bound_exact":fq(E_DEP),
      "deployment_during_energy_bound_exact":fq(E_DEP_DURING),
      "nominal_probe_force_squared_integral_exact":fq(nominal_probe_energy),
      "probe_energy_upper_bound_including_allowances":cal_energy_bound,
      "calibration_center_range":1.,
      "calibration_center_speed_cap":15/(8*float(H)),
      "calibration_center_acceleration_cap":10*math.sqrt(3)/(3*float(H)**2),
      "calibration_reaction_force_cap":2.,
      "calibration_center_travel":2.,
      "calibration_absolute_work_cap":4.,
      "query_center_range":float(query_amplitude),
      "query_center_speed_cap":15*float(query_amplitude)/(8*float(query_ramp)),
      "query_center_acceleration_cap":10*math.sqrt(3)*float(query_amplitude)/(3*float(query_ramp)**2),
      "query_reaction_force_cap":float(query_amplitude)+math.sqrt(2*float(E_DEP_DURING)),
      "source_step_lipschitz_bound_used_exact":"2",
      "on_force_discrepancy_allowance_exact":fq(FORCE_ERROR),
      "meter_backaction_allowance_exact":fq(BACKACTION),
      "off_mode":"exact fixed center in primary illustration",
      "off_mode_extension":"Nonzero common off error must meet the separate floor and energy ledger in universal_physical_closure.md.",
      "calibration_noise_probability_bound":200*math.exp(-12.5),
      "deployment_noise_probability_bound":2*math.exp(-9),
      "joint_valid_event_probability_exact":fq(joint_success),
      "joint_valid_event_probability_at_least":float(joint_success),
      "readiness_scope":"Includes only quiet drift, baseline metrology/noise and baseline-only backaction. Forecast force/backaction is separate in delivery_error_exact.",
      "relative_program_timing_scope":"Within-program error <=1e-8 and command tracking/gain/rounding together must fit the 1e-5 force error. Absolute slot/report timestamp tolerance is separately 1e-6.",
      "hardware_scope":"Permanent spring; its reaction is bounded by energy. Known mass also bounds the local damper reaction. Bare law and hidden modes are not supplied to the learner."
    }
    output={
      "schema":"acquired_step_response_v1",
      "times_exact":list(map(fq,times)),
      "values_exact":list(map(fq,values)),
      "response_error_exact":fq(response_error),
      "deployment_baseline_exact":fq(dep_baseline),
      "readiness_error_exact":fq(readiness),
      "delivery_error_exact":fq(delivery_bound),
      "horizon_exact":"1","gamma_exact":"1","stiffness_exact":"1","mass_exact":"1",
      "calibration_error_terms_exact":{k:fq(v) for k,v in cal_terms.items()},
      "readiness_error_terms_exact":{k:fq(v) for k,v in readiness_terms.items()},
      "resources":resources,
      "evidence_scope":{
        "source":"Floating finite passive-oscillator simulation, not interval-validated or laboratory data.",
        "reports":"Actual finite-box sensor output, simulated white readout noise, finite 20-bit ADC; stored as exact rational reports.",
        "clock":"Distinct reproducible PRNG seeds emulate independent private choices; this is not execution of a physical entropy source.",
        "initial_state":"Generated once before the clock draws; retained continuously through calibration, turnoff, second random wait, deployment and turnoff.",
        "robust_errors":"Nonzero force/backaction, hardware timing and systematic allowances are charged but their worst-case perturbations are not all physically simulated.",
        "microscopic_access":"Only the source simulator and diagnostic routine receive its matrix, state and modes. The learner receives only raw finite reports, node times and declared public bounds.",
      }
    }
    output_path=ROOT/"acquired_step_response.json"
    write_json(output_path,output)
    traces={
      "query":{"amplitude_exact":"4/5","start_exact":"0","ramp_exact":"1/20",
               "force":"quintic positive rise then hold through horizon"},
      "times":diagnostic_t.tolist(),
      "physical_x":physical[:,0].tolist(),
      "counterfactual_free_x":free[:,0].tolist(),
      "nominal_force":[float(query_amplitude)*smooth(float(t)/float(query_ramp)) for t in diagnostic_t],
      "scope":"Sampled floating source traces for diagnostic comparison, not proof of the uniform acquired certificate."
    }
    write_json(ROOT/"source_trace_diagnostic.json",traces)
    diagnostic={
      "source_parameters":hidden,
      "source_dimension":len(state),"hidden_mode_pairs":12,
      "initial_state":initial_state.tolist(),
      "initial_energy":initial_energy,
      "energy_at_calibration_selected_slot":cal_free_energy,
      "energy_after_complete_calibration":cal_energy_after,
      "energy_before_deployment_selected_slot":dep_energy_before,
      "energy_after_deployment_and_turnoff":energy(state),
      "hidden_energy_after_calibration":float(cal_end_state[2:]@cal_end_state[2:]/2),
      "hidden_energy_before_deployment":float(dep_selected_state[2:]@dep_selected_state[2:]/2),
      "dark_pair_energy_initial":float(initial_state[-2:]@initial_state[-2:]/2),
      "dark_pair_energy_final":float(state[-2:]@state[-2:]/2),
      "calibration_raw_baseline_exact":fq(baseline_report),
      "calibration_raw_reports_exact":list(map(fq,reports)),
      "calibration_sensor_means":means,"calibration_noise_draws":noises,
      "calibration_baseline_sensor_mean":baseline_ideal,
      "calibration_baseline_noise_draw":baseline_noise,
      "deployment_baseline_sensor_mean":dep_baseline_true,
      "deployment_baseline_noise_draw":dep_baseline_noise,
      "sampled_acquired_table_error":sampled_table_error,
      "source_only_true_step_at_nodes":true_step.tolist(),
      "sampled_deployment_free_motion_from_free_baseline":float(np.max(np.abs(free[:,0]-free_baseline))),
      "radau_calibration_counts":cal_counts,"radau_deployment_counts":dep_counts,
      "seeds":{"source":SOURCE_SEED,"calibration_clock":CLOCK_CAL_SEED,
               "deployment_clock":CLOCK_DEP_SEED,"calibration_noise":NOISE_CAL_SEED,
               "deployment_noise":NOISE_DEP_SEED},
      "elapsed_seconds":perf_counter()-started,
      "table_sha256":hashlib.sha256(output_path.read_bytes()).hexdigest(),
      "all_recorded_ADC_readings_inside_range":True,
      "scope":"Microscopic source diagnostics only; not passed to the learner or predictor."
    }
    write_json(ROOT/"retained_source_diagnostics.json",diagnostic)
    print(json.dumps({
      "output":str(output_path),"table_sha256":diagnostic["table_sha256"],
      "response_error":float(response_error),"readiness_error":float(readiness),
      "delivery_error":float(delivery_bound),
      "deployment_baseline":float(dep_baseline),
      "sampled_table_error":sampled_table_error,
      "source_resets":0,"physical_clock_slots":[n_cal,n_dep],
      "selected_clock_indices":[j_cal,j_dep],
      "energies":[initial_energy,cal_energy_after,dep_energy_before,energy(state)],
      "elapsed_seconds":diagnostic["elapsed_seconds"],
    },indent=2))


if __name__=="__main__":
    main()
