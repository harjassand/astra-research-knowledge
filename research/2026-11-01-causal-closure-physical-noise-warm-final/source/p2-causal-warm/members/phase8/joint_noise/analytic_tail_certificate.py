"""Closed-form conservative tail bound for every retained measurement history.

Uses only a peak force envelope, a thermal-occupation bound and the complete
physical interval ledger. The force is allowed to be any bounded, data-controlled
operator; no Gaussian apparatus-state or data-error-count assumption is made.
"""
from pathlib import Path
import math,json
import numpy as np
from scipy.optimize import differential_evolution

HERE=Path(__file__).resolve().parent

def force_step(theta,U,eps):
    after=4*math.atanh(math.tanh(theta/4)*math.exp(-eps*U))
    return after,(theta-after)/(eps*eps)

def thermal_flow(theta,rate,time,nb):
    w=math.expm1(theta);e=math.exp(rate*time)
    return math.log1p(w*e/(1+nb*w*(e-1)))

def certificate(theta0,eps_loop,eps_idle,cfg):
    nb=cfg['thermal_nmax'];T=cfg['loop_time'];s=cfg['switch_time'];R=cfg['readout_hold_time'];kr=cfg['readout_damping'];kl=cfg['loop_damping'];uf=cfg['total_force_cap'];ue=cfg['off_force_cap']
    if not 0<theta0<min(math.log1p(1/nb),math.log1p(1/cfg['initial_nbar'])):return None
    # During loop and switches discard damping's negative drift but retain all
    # upward thermal injection in the scalar cost. Both switches take the upper
    # rate kr; their actual continuous shape lies below that envelope.
    theta_a,c_loop=force_step(theta0,uf*T,eps_loop)
    c_loop+=kl*nb*math.expm1(theta0)*T
    theta_b,c_up=force_step(theta_a,ue*s,eps_idle)
    c_up+=kr*nb*math.expm1(theta_a)*s
    theta_hi=thermal_flow(theta_b,kr,R,nb)
    ratio=math.exp(theta_hi/2)/(1-nb*math.expm1(theta_hi))
    keff=kr-ue*eps_idle*ratio
    if keff<=0:return None
    theta_lo=thermal_flow(theta_b,keff,R,nb)
    # Thermal cost upper bound follows the faster zero-force characteristic.
    c_hold=math.log1p(nb*math.expm1(theta_b)*math.expm1(kr*R))
    c_hold+=2*ue/eps_idle*math.sinh(theta_hi/2)*R
    # Closing switch: endpoint lower bound from theta_lo, cost upper bound from theta_hi.
    theta_end,_=force_step(theta_lo,ue*s,eps_idle)
    _,c_down=force_step(theta_hi,ue*s,eps_idle)
    c_down+=kr*nb*math.expm1(theta_hi)*s
    C=c_loop+c_up+c_hold+c_down
    if theta_end<=theta0:return None
    B0=-math.log1p(-cfg['initial_nbar']*math.expm1(theta0))
    B=max(B0,theta0*C/(theta_end-theta0))
    thmin=min(theta_b,theta_end)
    # Safe common all-time exponent and moment; rounding increases the bound.
    thsafe=math.floor(thmin*1000)/1000
    Bpeak=math.ceil(B+C)
    return dict(theta_start=theta0,epsilon_loop=eps_loop,epsilon_idle=eps_idle,
                theta_min_unrounded=thmin,theta_end_lower=theta_end,cost_upper=C,
                log_M_boundary_upper=B,theta_uniform=thsafe,log_M_uniform_upper=Bpeak,
                initial_log_moment=B0,mean_bound_from_certificate=Bpeak/thsafe)

def cap_bound(c,cycles,action,delta):
    th=c['theta_uniform'];B=c['log_M_uniform_upper'];A=cycles*action
    L=max(1,int(1/th)+1)
    while math.log(2*A)+.5*math.log(L+1)+.5*(B-th*L)>math.log(delta):L+=1
    return dict(module_cycles=int(cycles),force_difference_action_per_cycle=action,
                cutoff=L,whole_history_half_trace_bound=2*A*math.sqrt(L+1)*math.exp((B-th*L)/2),
                bounded_force_generator_norm_per_cycle=4*action*math.sqrt(L),
                target_whole_history_half_trace=delta)

def optimize(cfg,cycles,action,delta):
    tm=min(math.log1p(1/cfg['thermal_nmax']),math.log1p(1/cfg['initial_nbar']))*.999
    def obj(v):
        c=certificate(*v,cfg)
        if c is None or c['theta_uniform']<=0:return 1e9
        L=c['mean_bound_from_certificate']+2*math.log(2*cycles*action/delta)/c['theta_uniform']
        return L+math.log(max(L,1))/c['theta_uniform']
    r=differential_evolution(obj,[(.05,tm),(.03,.5),(.05,3)],seed=20261102,maxiter=80,popsize=8,tol=1e-5,polish=False)
    # Round free proof parameters, then recompute the analytical certificate.
    v=[round(float(x),4) for x in r.x]
    c=certificate(*v,cfg);c['comparison']=cap_bound(c,cycles,action,delta)
    return c

def main():
    cfg=dict(loop_time=1.84,loop_damping=1e-4,total_force_cap=3.000001,
             switch_time=.1,readout_hold_time=3.,readout_damping=1.,
             off_force_cap=1e-6,thermal_nmax=.1,initial_nbar=.3)
    cycle=cfg['loop_time']+2*cfg['switch_time']+cfg['readout_hold_time']
    cases=[optimize(cfg,10**6,1e-6*cycle,1e-6),optimize(cfg,10**12,1e-6*cycle,1e-9),optimize(cfg,10**6,1e-9,1e-6)]
    out=dict(model=cfg,cycle_time=cycle,cases=cases,
             meaning='Closed-form envelope certificate; caps only perturbing operators, leaving nominal bosonic controls/damping unchanged.',
             limitation='The declared rate and force envelopes must hold through the actual control and measurement schedule; omitted damping intervals or stronger heating are outside this physical model.')
    (HERE/'analytic_tail_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
