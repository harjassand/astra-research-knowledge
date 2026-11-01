"""Photon exponential-moment and virtual-cutoff bounds; no conditional coin.

The sharp scheduled calculation applies to certified passive pre/post windows
with vacuum fields and bounded forces in the mapping window. A separate global
bound admits bounded forces at all times and unequal thermal baths, but is much
looser. Numbers are analytic certificates evaluated in double precision, not
interval-arithmetic-certified hardware limits.
"""
from pathlib import Path
import json
import math
import numpy as np
from scipy.optimize import differential_evolution, minimize

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
ROW=json.loads((ROOT/'phase7/root/repeated_operation_results.json').read_text())['repeated_report_candidate']
p=ROW['read_pre_operator_norm']; q=ROW['read_post_operator_norm']
U=ROW['integrated_absolute_mapping_force']; tau=ROW['total_time']; tmap=ROW['mapping_time']

def f(r,theta):
    return math.log1p(r*r*math.expm1(theta))

def finv(r,theta):
    return math.log1p(math.expm1(theta)/(r*r))

def backdrive(theta,U,eps):
    z=math.tanh(theta/4)*math.exp(eps*U)
    if z>=1: return None
    ti=4*math.atanh(z)
    return ti,(ti-theta)/(eps*eps)

def certificate(theta_b,eps_c,theta_peak,nbar0=.3,modes=2):
    if theta_b<=0 or theta_peak<=0 or math.expm1(theta_b)*nbar0>=1: return None
    x=backdrive(f(q,theta_b),U,eps_c)
    if x is None: return None
    ti,c=x; F=f(p,ti); rho=F/theta_b
    if rho>=1 or rho<=0: return None
    B0=-modes*math.log1p(-nbar0*math.expm1(theta_b))
    B=max(B0,c/(1-rho))
    ti_peak=finv(p,theta_b)
    if ti_peak<=theta_peak:return None
    eps_peak=math.log(math.tanh(ti_peak/4)/math.tanh(theta_peak/4))/U
    if eps_peak<=0:return None
    c_peak=(ti_peak-theta_peak)/(eps_peak*eps_peak)
    # Before pre-observation, the boundary bound also matters if theta_peak>theta_b.
    # Enforce common theta_peak<=theta_b, so all windows have the same peak bound.
    if theta_peak>theta_b:return None
    Bpeak=B+c_peak
    return dict(theta_boundary=theta_b,epsilon_cycle=eps_c,theta_peak=theta_peak,
                F_boundary=F,rho=rho,log_M_initial=B0,log_M_boundary=B,
                log_M_peak=Bpeak,epsilon_peak=eps_peak)

def find_cutoff(c,uses,delta):
    # Half trace-distance bound from deleting only the N=L <-> L+1 drive edges.
    totalaction=uses*U
    th=c['theta_peak']; B=c['log_M_peak']
    L=max(1,int((B+2*math.log(max(totalaction,1)/delta))/th))
    while math.log(totalaction)+.5*math.log(L+1)+.5*(B-th*L)>math.log(delta):L+=1
    return L

def optimize(uses,delta,nbar0=.3):
    # Optimize smooth proxy to the integer cutoff, then evaluate exact displayed inequality.
    def fun(v):
        tb,eps,frac=v; c=certificate(tb,eps,tb*frac,nbar0)
        if c is None:return 1e10
        L=(c['log_M_peak']+2*math.log(uses*U/delta))/c['theta_peak']
        return L+math.log(max(L,1))/c['theta_peak']
    res=differential_evolution(fun,[(.01,math.log1p(1/nbar0)*.999),(.005,.65),(.01,1)],seed=20261101,tol=1e-8,popsize=14,maxiter=400,polish=True)
    tb,eps,frac=res.x;c=certificate(tb,eps,tb*frac,nbar0)
    L=find_cutoff(c,uses,delta)
    c.update(uses=int(uses),target_half_trace_error=delta,cutoff=L,
        actual_half_trace_error_bound=uses*U*math.sqrt(L+1)*math.exp((c['log_M_peak']-c['theta_peak']*L)/2),
        initial_single_module_tail=math.exp(c['log_M_initial']-c['theta_boundary']*(L+1)),
        intrinsic_loss_diamond_per_map=2*ROW['model']['ka']*L*tmap,
        intrinsic_loss_diamond_full_meter=2*ROW['model']['ka']*L*tau,
        relative_area_error_diamond_coefficient=2*math.pi*L,
        optimizer_success=bool(res.success))
    return c

def global_bound(theta,u_max,kappa_min,rates,nbar):
    z=math.expm1(theta); nmax=max(nbar)
    if nmax*z>=1:raise ValueError('outside thermal exponential-moment domain')
    a0=kappa_min*(-math.expm1(-theta))*(1-nmax*z)
    bthermal=sum(k*n for k,n in zip(rates,nbar))*z
    bdrive=2*u_max*u_max*z/(kappa_min*(1-nmax*z))
    B=2*theta*(bthermal+bdrive)/a0
    return dict(theta=theta,log_stationary_moment_bound=B,
                implied_Jensen_mean_bound=B/theta,
                decay_rate_for_log_moment=a0/(2*theta),
                force_cap=u_max,rate_min=kappa_min,thermal_occupations=nbar)

def main():
    rows=[optimize(n,d) for n,d in [(120,1e-6),(1000000,1e-6),(1000000000000,1e-9)]]
    result=dict(model_source='phase7/root/repeated_operation_results.json',p=p,q=q,U=U,
                nominal_scheduled_scope='Certified passive observation windows, vacuum fields, bounded arbitrary data-controlled forces during mapping; unconditional history moment.',
                scheduled_certificates=rows,
                broad_all_interval_bound=[global_bound(th,3.001,1e-4,[1e-4,4],[.001,.001]) for th in [.01,.1,.5]],
                disclaimers=['No conditional energy cap or independent loss coin is asserted.',
                  'The virtual cutoff is mathematical, not a physical measurement or reset.',
                  'All interval residual forcing is covered by the broad bound; the sharper nominal schedule numbers do not certify that case.',
                  'Integrated bounded-generator norms are amplitudes/channel-norm budgets, not physical probabilities.',
                  'All actual waiting/switching/readout time must be included in the bounded-noise ledger.'])
    (HERE/'exponential_tail_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
