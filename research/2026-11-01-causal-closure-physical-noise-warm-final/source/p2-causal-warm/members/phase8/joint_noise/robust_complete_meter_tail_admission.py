"""Authoritative all-history admission for the robust 10.984/g physical meter.

A reflected exponential-moment characteristic uses surplus damping during the
actual driven readouts to contract log M. Nominal oscillator dynamics are never
Fock truncated. Every actual meter interval appears below.
"""
from pathlib import Path
import math,json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import differential_evolution

HERE=Path(__file__).resolve().parent
CFG=dict(read_time=4.472,loop_time=1.84,conditional_X_time=.05,H_time=.05,feedforward_wait=.05,
         ramp=.1,force_cap=3.,read_force_relative_gain_bound=1e-6,force_error_cap=1e-7,
         thermal_nmax=.1,initial_nbar=.3,k0_lower=9e-5,k0_upper=1.1e-4,
         read_rate_lower=3.996,read_rate_upper=4.004)
SEGMENTS=[('read_prepare',CFG['read_time']),('conditional_X',.05),('H_prepare',.05),('loop',CFG['loop_time']),('H_final',.05),('read_final',CFG['read_time']),('feedforward',.05)]
TOTAL=sum(t for _,t in SEGMENTS)


def controls(t,dur,kind):
    w=0.
    if kind.startswith('read'):
        r=CFG['ramp'];w=1.
        if t<r:w=math.sin(math.pi*t/(2*r))**2
        elif t>dur-r:w=math.sin(math.pi*(dur-t)/(2*r))**2
    kl=CFG['k0_lower']+CFG['read_rate_lower']*w
    ku=CFG['k0_upper']+CFG['read_rate_upper']*w
    u=CFG['force_error_cap']
    if kind=='loop':u+=CFG['force_cap']
    if kind.startswith('read'):u+=CFG['force_cap']*(1+CFG['read_force_relative_gain_bound'])*w
    return kl,ku,u


def vb(t,theta,dur,kind,eps):
    kl,ku,u=controls(t,dur,kind);nb=CFG['thermal_nmax']
    d=(-math.expm1(-theta))*(1-nb*math.expm1(theta));sh=2*math.sinh(theta/2)
    return kl*d-u*eps*sh,ku*nb*math.expm1(theta)+u/eps*sh


def solve(theta_cap,eps_loop,eps_read,detail=False,rtol=2e-8,max_step=.05):
    if theta_cap>=math.log1p(1/CFG['initial_nbar']):return None
    # Readout/idle must push theta upwards throughout its allowed interval.
    if vb(CFG['read_time']/2,theta_cap,CFG['read_time'],'read_prepare',eps_read)[0]<=0:return None
    if vb(0,theta_cap,.05,'feedforward',1.)[0]<=0:return None
    y=np.array([theta_cap,1.,0.]);all_t=[];all_y=[];offset=0.
    for kind,dur in SEGMENTS:
        eps=eps_loop if kind=='loop' else eps_read if kind.startswith('read') else 1.
        def char_rhs(t,z):
            v,b=vb(t,z[0],dur,kind,eps)
            return [v,0.,b]
        def ceiling(t,z):return z[0]-theta_cap
        ceiling.terminal=True;ceiling.direction=1
        sample_start=0.
        if kind=='loop' or y[0]<theta_cap-1e-10:
            events=None if kind=='loop' else ceiling
            sol=solve_ivp(char_rhs,[0,dur],y,events=events,rtol=rtol,atol=rtol*.01,max_step=max_step,dense_output=True)
            if not sol.success:return None
            end=sol.t[-1];ts=np.linspace(0,end,max(31,int(end/.01)+1));vals=sol.sol(ts)
            all_t.extend((ts+offset).tolist());all_y.extend(vals.T.tolist());y=sol.y[:,-1];sample_start=end
        if sample_start<dur-1e-12:
            # At the exponent ceiling, residual negative number drift contracts log M.
            y[0]=theta_cap
            def fixed_rhs(t,z):
                v,b=vb(t,theta_cap,dur,kind,eps);lam=v/theta_cap
                if lam<0:raise ValueError('invalid reflected branch')
                return [0.,-lam*z[1],-lam*z[2]+b]
            sol=solve_ivp(fixed_rhs,[sample_start,dur],y,rtol=rtol,atol=rtol*.01,max_step=max_step,dense_output=True)
            if not sol.success:return None
            ts=np.linspace(sample_start,dur,max(31,int((dur-sample_start)/.01)+1));vals=sol.sol(ts)
            all_t.extend((ts+offset).tolist());all_y.extend(vals.T.tolist());y=sol.y[:,-1]
        offset+=dur
    if abs(y[0]-theta_cap)>1e-7 or not 0<y[1]<1:return None
    B0=-math.log1p(-CFG['initial_nbar']*math.expm1(theta_cap))
    B=max(B0,y[2]/(1-y[1]))
    yy=np.asarray(all_y);bt=yy[:,1]*B+yy[:,2];thmin=float(yy[:,0].min());E=float(np.max(bt/yy[:,0]))
    out=dict(theta_ceiling=theta_cap,epsilon_loop=eps_loop,epsilon_read=eps_read,
             cycle_moment_contraction=float(y[1]),cycle_moment_addition=float(y[2]),
             log_M_boundary=B,initial_log_M=B0,theta_peak=thmin,
             log_M_peak=thmin*E,mean_from_moment=E)
    if detail:out['trace']={'time':all_t,'theta':yy[:,0].tolist(),'log_moment_bound':bt.tolist()}
    return out


def compare(c,calls,delta,action,slots=None):
    th=math.floor(c['theta_peak']*1000)/1000;B=math.ceil(c['log_M_peak'])
    A=calls*action;L=max(1,int(1/th)+1)
    while math.log(2*A)+.5*math.log(L+1)+.5*(B-th*L)>math.log(delta):L+=1
    ans=dict(meter_calls=int(calls),theta_used=th,log_M_used=B,noise_operator_cap=L,
             force_difference_action_per_meter=action,total_force_difference_action=A,
             noise_cap_whole_history_half_trace=2*A*math.sqrt(L+1)*math.exp((B-th*L)/2),
             bounded_force_generator_norm_per_meter=4*action*math.sqrt(L),target_half_trace=delta)
    if slots is not None:
        Ls=1
        while True:
            q=math.exp(B-th*(Ls+1))
            if slots*(math.sqrt(q)+q)<=delta:break
            Ls+=1
        ans.update(compiled_slots=int(slots),input_sector_cap=Ls,
                   input_sector_whole_history_half_trace=slots*(math.sqrt(q)+q),input_sector_tail_per_slot=q)
        ans['fixed_input_sector_caps']=[]
        for cap in [192,320]:
            qc=math.exp(B-th*(cap+1))
            ans['fixed_input_sector_caps'].append(dict(cap=cap,tail_per_slot=qc,
                whole_history_half_trace=slots*(math.sqrt(qc)+qc)))
    return ans


def optimize(calls,delta,action,slots):
    def obj(v):
        c=solve(*v)
        if c is None:return 1e9
        # Optimize the general input-sector cap, since readout robustness needs it too.
        return c['mean_from_moment']+2*math.log(slots/delta)/c['theta_peak']
    r=differential_evolution(obj,[(.15,1.43),(.03,.4),(.05,.8)],seed=20261103,popsize=7,maxiter=80,tol=3e-5,polish=True)
    pars=[round(float(x),5) for x in r.x]
    c=solve(*pars,rtol=1e-10,max_step=.01)
    c['proof_parameters']=pars;c['comparison']=compare(c,calls,delta,action,slots)
    c['optimization_success']=bool(r.success)
    return c


def main():
    # Preserve the already constructed proof parameters. Only the physical
    # readout duration and complete compiled-slot ledger changed.
    cases=[]
    for calls,delta,slots,pars in [(10**6,1e-6,10**7,[1.26892,.09638,.25253]),
                                   (10**12,1e-9,10**13,[1.39396,.08273,.2211])]:
        c=solve(*pars,rtol=1e-10,max_step=.01)
        c['proof_parameters']=pars
        c['comparison']=compare(c,calls,delta,CFG['force_error_cap']*TOTAL,slots)
        c['optimization_status']='Previously optimized proof parameters retained; physical final readout and slot ledger updated.'
        cases.append(c)
    c=cases[0];th=c['comparison']['theta_used'];v,b=vb(0,th,.05,'feedforward',1.)
    out=dict(model=CFG,segments=[dict(operation=k,duration=t) for k,t in SEGMENTS],complete_meter_time=TOTAL,
             cases=cases,extra_idle_moment_contract=dict(theta=th,negative_number_coefficient=v,
             constant_coefficient=b,stationary_log_moment_upper=th*b/v,
             admitted_log_moment=c['comparison']['log_M_used']),
             source_scope='Implemented robust p2 receiver, readout duration4.472,512 ADC bins,16-bit ADC over+/-16,40-bit weights,72-bit accumulator; all nominal readout forcing and finite ramps included.',
             limitations=['This is the declared directly damped effective-mode model, not a finite-converter elimination theorem.',
               'Moment bounds allow arbitrary data/ancilla faults and measurement histories that respect force and damping envelopes.',
               'Readout pole/force-gain intervals enter the energy bounds; the receiver robustness is separately proved in physical_mechanisms.',
               'Initial exponential moment requires actual physical admission or a separately charged finite preparation from a known initial energy family.',
               'Additional waits preserve the shown moment envelope but their force, data, control and thermal exposure remain in the operation ledger.',
               'Numbers are high-accuracy ODE evaluations with conservative exponent/log-moment rounding, not formal interval arithmetic.'])
    # Residual apparatus coupling persists during actual consumer waiting.
    # The caller supplies all extra control/classical latency beyond these
    # explicit examples; this is not a zero-latency assumption.
    idle_rows=[]
    for wait in [8*TOTAL,88.]:
        for cap in [192,320]:
            action=CFG['force_error_cap']*wait
            idle_rows.append(dict(wait_time=wait,cap=cap,residual_force_action=action,
                 residual_generator_norm_for_wait=4*action*math.sqrt(cap)))
    out['extra_idle_residual_exposure_examples']=idle_rows
    out['caller_obligations']='Count every compiled apparatus-interface slot, including local control and idle interfaces, within M; add every physical waiting duration to integrated residual-force and data/control exposure. The10^7 slot budget is a declared caller budget, not an assertion that arbitrary extra scheduling fits it.'
    (HERE/'robust_complete_meter_tail_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
