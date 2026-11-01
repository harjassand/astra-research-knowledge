"""Tail admission for the ACTUAL Phase8 two-readout retained-bus meter.

This replaces the earlier force-off hold illustration. Preparation readout,
conditional X, H, parity loop, H, final readout and feedforward waiting are all
included. Readout continues to drive the retained bus; it is not cooling to vacuum.
"""
from pathlib import Path
import math,json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import differential_evolution

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
READ=[x for x in json.loads((ROOT/'phase8/root/finite_longitudinal_readout_results.json').read_text())['rows'] if x['readout_rate_cap']==4 and x['target']==1e-6][0]
PULSE=json.loads((ROOT/'phase8/physical_mechanisms/one_bus_parity_results.json').read_text())['optimized_safe']
CFG=dict(read_time=READ['T'],loop_time=PULSE['T'],conditional_X_time=.05,H_time=.05,feedforward_wait=.05,
         ramp=.1,force_cap=3.,force_error_cap=1e-7,thermal_nmax=.1,initial_nbar=.3,
         k0_lower=9e-5,k0_upper=1.1e-4,read_rate_lower=3.996,read_rate_upper=4.004)
SEGMENTS=[('read_prepare',CFG['read_time']),('conditional_X',.05),('H_prepare',.05),('loop',CFG['loop_time']),('H_final',.05),('read_final',CFG['read_time']),('feedforward',.05)]
TOTAL=sum(t for _,t in SEGMENTS)


def envelope(t,T):
    r=CFG['ramp']
    if t<r:return math.sin(math.pi*t/(2*r))**2
    if t>T-r:return math.sin(math.pi*(T-t)/(2*r))**2
    return 1.


def solve(theta0,eps_loop,eps_read,detail=False,rtol=2e-8,max_step=.04):
    nb=CFG['thermal_nmax'];uerr=CFG['force_error_cap'];y=np.array([theta0,0.]);tt=[];yy=[];offset=0.
    for kind,dur in SEGMENTS:
        isread=kind.startswith('read');isloop=kind=='loop'
        eps=eps_read if isread else eps_loop if isloop else 1.
        def rhs(t,v):
            th=v[0]
            w=envelope(t,dur) if isread else 0.
            kl=CFG['k0_lower']+CFG['read_rate_lower']*w
            ku=CFG['k0_upper']+CFG['read_rate_upper']*w
            # Loop uses the physical peak envelope rather than a favorable nominal waveform.
            u=CFG['force_cap']*(w if isread else 1. if isloop else 0.)+uerr
            d=(-math.expm1(-th))*(1-nb*math.expm1(th));sh=2*math.sinh(th/2)
            return [kl*d-u*eps*sh,ku*nb*math.expm1(th)+u/eps*sh]
        sol=solve_ivp(rhs,[0,dur],y,rtol=rtol,atol=rtol*.01,max_step=max_step,dense_output=True)
        if not sol.success:return None
        ts=np.linspace(0,dur,max(51,int(dur/.005)+1));vals=sol.sol(ts)
        tt.extend((ts+offset).tolist());yy.extend(vals.T.tolist());y=sol.y[:,-1];offset+=dur
    theta1,C=y
    if theta1<=theta0 or theta0>=math.log1p(1/CFG['initial_nbar']):return None
    B0=-math.log1p(-CFG['initial_nbar']*math.expm1(theta0))
    B=max(B0,theta0*C/(theta1-theta0))
    yy=np.asarray(yy);thmin=float(yy[:,0].min());E=float(np.max((B+yy[:,1])/yy[:,0]))
    ans=dict(theta_initial=theta0,theta_final=float(theta1),epsilon_loop=eps_loop,epsilon_read=eps_read,
             log_M_boundary=B,initial_log_M=B0,theta_peak=thmin,log_M_peak=thmin*E,
             mean_from_moment=E,cost=C)
    if detail:ans['trace']={'time':tt,'theta':yy[:,0].tolist(),'cost':yy[:,1].tolist()}
    return ans


def comparison(c,calls,delta,force_action):
    # Round exponent down, log moment up for a margin exceeding numerical precision.
    th=math.floor(c['theta_peak']*1000)/1000;B=math.ceil(c['log_M_peak'])
    # Reducing theta reduces M, so the old B is a safe upper bound.
    A=calls*force_action;L=max(1,int(1/th)+1)
    while math.log(2*A)+.5*math.log(L+1)+.5*(B-th*L)>math.log(delta):L+=1
    return dict(meter_calls=int(calls),theta_used=th,log_M_used=B,cutoff=L,
                total_force_difference_action=A,force_difference_action_per_meter=force_action,
                whole_history_half_trace_bound=2*A*math.sqrt(L+1)*math.exp((B-th*L)/2),
                bounded_force_generator_norm_per_meter=4*force_action*math.sqrt(L),target_half_trace=delta)


def optimize(calls,delta,action):
    def obj(v):
        c=solve(*v)
        if c is None:return 1e9
        L=c['mean_from_moment']+2*math.log(2*calls*action/delta)/c['theta_peak']
        return L+math.log(max(L,1))/c['theta_peak']
    r=differential_evolution(obj,[(.1,1.44),(.03,.4),(.05,1.0)],seed=20261102,popsize=7,maxiter=70,tol=3e-5,polish=True)
    # The displayed proof parameters are rounded, then the ODE is recomputed accurately.
    pars=[round(float(x),5) for x in r.x]
    c=solve(*pars,rtol=1e-10,max_step=.01)
    c['proof_parameters']=pars;c['comparison']=comparison(c,calls,delta,action)
    c['optimization_success']=bool(r.success)
    return c


def main():
    cases=[]
    for calls,delta,action in [(10**6,1e-6,CFG['force_error_cap']*TOTAL),(10**12,1e-9,CFG['force_error_cap']*TOTAL),(10**6,1e-6,1e-9)]:
        cases.append(optimize(calls,delta,action))
    out=dict(model=CFG,segments=[dict(operation=x,duration=t) for x,t in SEGMENTS],complete_meter_time=TOTAL,
             cases=cases,
             scope=['The actual two driven QND readouts are included; no force-off cooldown or vacuum reset was substituted.',
                    'The damping bounds include an illustrative +/-0.1% readout-port and +/-10% intrinsic-rate envelope, for energy admission only.',
                    'Every waiting, conditional pulse, basis pulse and finite readout ramp in the declared meter is included.',
                    'The initial marginal exponential-moment family is thermal n=.3; data/memory correlations are unrestricted subject to that moment.',
                    'Force clipping and damping envelopes must hold on the physical histories admitted by this theorem.',
                    'Whole-history trace comparison caps only residual force operators. It does not truncate the nominal oscillator or replace its exact fresh-noise channel.',
                    'The scalar ODE theorem is analytic. Displayed numbers are ordinary high-accuracy numerical evaluations with generous rounding, not formal interval arithmetic.'])
    th=cases[0]['comparison']['theta_used'];sh=2*math.sinh(th/2)
    d=(1-math.exp(-th))*(1-CFG['thermal_nmax']*math.expm1(th))
    a=CFG['k0_lower']*d-CFG['force_error_cap']*sh
    b=CFG['k0_upper']*CFG['thermal_nmax']*math.expm1(th)+CFG['force_error_cap']*sh
    out['extra_idle_moment_contract']=dict(theta=th,negative_number_coefficient=a,
        constant_coefficient=b,stationary_log_moment_upper=th*b/a,
        already_admitted_log_moment=cases[0]['comparison']['log_M_used'],
        meaning='Any extra force-capped weakly damped idle interval cannot increase the stated exponential moment; its residual-force, data and control exposure must still be added to the total time/action ledger.')
    (HERE/'complete_meter_tail_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
