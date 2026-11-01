"""Closed-form tail barrier for the FINAL finite-readout physical schedule.

No ODE optimizer or Fock truncation is used. All inequalities use physical peak
envelopes and deliberately loose round constants. This certifies an alternative
M_.4 <= exp(64) barrier, adequate at input cap320 for10^7 actual interfaces.
The sharper collaborator characteristic bounds are preserved separately.
"""
from pathlib import Path
import json, math

HERE=Path(__file__).resolve().parent

def force(theta,action,eps):
    end=4*math.atanh(math.tanh(theta/4)*math.exp(-eps*action))
    return end,(theta-end)/(eps*eps)

def main():
    u=3.0000031; nb=.1; kl_hi=.00011; kl_lo=.00009
    kr_hi=4.00411;kr_lo=3.99609
    tgate=1.84; tr=.1; thold=4.472-.2
    tb=.8; B0=20.; eps_force=.1; eps_read=.2; ceiling=.85
    d=lambda th:(1-math.exp(-th))*(1-nb*math.expm1(th))
    s=lambda th:2*math.sinh(th/2)
    tg,cg=force(tb,u*tgate,eps_force)
    cg+=kl_hi*nb*math.expm1(tb)*tgate
    tu,cu=force(tg,u*tr,eps_force)
    cu+=kr_hi*nb*math.expm1(tg)*tr
    # d is increasing throughout this small interval (checked below analytically).
    speed=kr_lo*d(tu)-u*eps_read*s(ceiling)
    time_up=(ceiling-tu)/speed
    bmax=kr_hi*nb*math.expm1(ceiling)+u*s(ceiling)/eps_read
    cr=bmax*time_up
    peak=B0+cg+cu+cr
    a=kr_lo*d(ceiling)-u*eps_read*s(ceiling)
    decay=a/ceiling; stationary=bmax/decay
    remaining=thold-time_up
    hold_end=stationary+(peak-stationary)*math.exp(-decay*remaining)
    td,cd=force(ceiling,u*tr,eps_force)
    cd+=kr_hi*nb*math.expm1(ceiling)*tr
    Bout=(hold_end+cd)*tb/td
    # During arbitrary additional idles (also data/control pulses), F<=1e-7.
    # Choose epsilon so half of the passive negative number drift remains.
    idle=[]
    for th in [.4,tu,tb,ceiling]:
        u0=1.e-7; eps=kl_lo*d(th)/(2*u0*s(th))
        aa=kl_lo*d(th)/2
        bb=kl_hi*nb*math.expm1(th)+u0*s(th)/eps
        idle.append(dict(theta=th,stationary_log_moment=bb*th/aa))
    # d'(theta)=(1+nb)e^-theta - nb e^theta >0 iftheta<.5log((1+nb)/nb).
    monotonic_limit=.5*math.log((1+nb)/nb)
    checks=dict(theta_min_above_point4=tu>.4,peak_below64=peak<64,
       outgoing_theta_at_least_point8=td>.8,boundary_logM_below20=Bout<20,
       readout_reaches_ceiling=time_up<thold,d_increasing=ceiling<monotonic_limit,
       idle_preserves_bounds=max(x['stationary_log_moment'] for x in idle)<20)
    if not all(checks.values()):raise AssertionError(checks)
    L=320;M=10**7;logq=64-.4*(L+1);q=math.exp(logq)
    full=M*(math.sqrt(q)+q)
    out=dict(model=dict(force_envelope=u,thermal_occupation_max=nb,intrinsic_rate=[kl_lo,kl_hi],
       readout_rate=[kr_lo,kr_hi],gate_time=tgate,readout_time=4.472,ramp_time=tr,
       complete_meter_time=10.984,initial_boundary_theta=.8,initial_boundary_logM=20),
       proof_parameters=dict(epsilon_force=eps_force,epsilon_read=eps_read,theta_ceiling=ceiling),
       gate_end_theta=tg,gate_cost=cg,ramp_up_end_theta=tu,ramp_up_cost=cu,
       hold_minimum_exponent_speed=speed,time_to_ceiling_upper=time_up,
       hold_cost_rate_upper=bmax,peak_logM_upper=peak,hold_decay_rate_lower=decay,
       hold_stationary_logM_upper=stationary,hold_remaining_time_lower=remaining,
       hold_end_logM_upper=hold_end,ramp_down_end_theta=td,ramp_down_cost=cd,
       outgoing_boundary_logM_upper=Bout,idle_bounds=idle,checks=checks,
       rounded_uniform_barrier=dict(theta=.4,log_M=64),
       input_sector_replacement=dict(interface_slots=M,number_cap=L,
          individual_tail_upper=q,whole_history_half_trace_bound=full),
       meaning='Analytic comparison inequalities with large margins. Elementary evaluations are double precision; no sampled trajectory maximum or ODE envelope is used.',
       initial_admission='M_.8<=exp(20) at first cycle boundary. The separate finite conditioning proof from initial n<=100 supplies it; an arbitrary unbounded initial state does not.')
    (HERE/'analytic_all_interval_barrier_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
