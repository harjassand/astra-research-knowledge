"""Conditional finite-state constructions; no fit to an acquired generator.
Run: python catalytic_cycle_response.py
All irreversible examples are explicitly labeled. Full reverse reactions
are retained in the ring+trap example. Bias/Poisson identity is standard.
"""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import expi

KB=8.617333262145e-5
T=298.0


def generator(rates):
    Q=np.array(rates,float).copy()
    np.fill_diagonal(Q,0)
    Q[np.diag_indices(len(Q))]=-Q.sum(1)
    return Q


def stationary(Q):
    A=Q.T.copy()
    b=np.zeros(len(Q))
    A[-1]=1
    b[-1]=1
    return np.linalg.solve(A,b)


def poisson(Q,reward):
    pi=stationary(Q)
    g=(Q*reward).sum(1)
    J=pi@g
    # Rank-one regularization removes additive gauge.
    h=np.linalg.solve(Q+np.ones((len(Q),1))*pi[None,:],J-g)
    w=reward+h[None,:]-h[:,None]
    return pi,g,J,h,w


def ring(forward,backward=None,trap=None):
    n=len(forward)
    m=n+(trap is not None)
    q=np.zeros((m,m)); r=np.zeros((m,m))
    if backward is None: backward=np.zeros(n)
    for i,(k,krev) in enumerate(zip(forward,backward)):
        j=(i+1)%n
        q[i,j]+=k; q[j,i]+=krev
        if i==n-1: r[i,j]=1; r[j,i]=-1
    if trap is not None:
        alpha,delta=trap
        q[0,n]=alpha; q[n,0]=delta
    return generator(q),r


def pulse_response(Q,r,edge,c,tau,end_tau=25.,symmetric=False):
    pi,g,J,h,w=poisson(Q,r)
    i,j=edge
    n=len(Q)
    def diff(t):
        out=np.zeros_like(Q)
        out[i,j]=Q[i,j]*np.expm1(c*np.exp(-t/tau))
        if symmetric: out[j,i]=Q[j,i]*np.expm1(c*np.exp(-t/tau))
        out[np.diag_indices(n)]=-out.sum(1)
        return out
    # Integrate only the pulse; analytically account for complete relaxation
    # using the baseline reward bias h after the pulse has ended.
    def rhs(t,y):
        p=y[:n]; dq=diff(t); qt=Q+dq
        return np.r_[p@qt,p@(qt*r).sum(1)-J,p@(dq*w).sum(1)]
    y0=np.r_[pi,0.,0.]
    z=solve_ivp(rhs,(0,end_tau*tau),y0,method='DOP853',rtol=3e-12,
                atol=1e-14,max_step=tau/20.)
    y=z.y[:,-1]
    # Residual envelope at end_tau is explicitly truncated in both routes.
    direct=y[n]+(y[:n]-pi)@h
    reward_identity=y[n+1]
    return {'baseline_current':float(J),'pi':pi.tolist(),
            'edge_value':float(w[i,j]),'reverse_edge_value':float(w[j,i]),
            'direct_excess_with_relaxation':float(direct),
            'poisson_excess':float(reward_identity),
            'identity_abs_residual':float(abs(direct-reward_identity)),
            'tail_envelope_fraction':float(np.exp(-end_tau)),
            'normalization_error':float(abs(y[:n].sum()-1))}


def depletion_example():
    G=3.3; theta=.3
    theta0=1-(1-theta)/G
    c=1/theta-1/(G*theta0)
    C=np.log(10)*KB*T*1000
    alpha0=C/66.1; alpha1=C/60.2
    mat=np.array([[1-theta0,theta0],
                  [(1-theta)/(1-c*theta**2),theta/(1-c*theta**2)]])
    aa,ab=np.linalg.solve(mat,np.array([alpha0,alpha1]))
    a0=theta0/(1-theta0)
    def solve(x):
        a=a0*np.exp(aa*x);b=np.exp(ab*x);cc=c*np.exp(ab*x)
        th=brentq(lambda z:a*(1-z)-b*z-cc*a*(1-z)*z,0.,1.)
        return a*(1-th)
    dx=1e-5
    derivative=(np.log(solve(dx))-np.log(solve(-dx)))/(2*dx)
    return {'G':G,'theta':theta,'theta0':theta0,'c':c,
            'alpha_refill':float(aa),'alpha_release':float(ab),
            'alpha_new':float(alpha1),'alpha_finite_difference':float(derivative),
            'warning':'Local constructed parameters; not a fit across the U-shaped gain curve.'}


def gate_resource(E,J,eta=.28):
    q=np.exp(-E/(KB*T)); peq=q/(1+q)
    gamma=1/(41e-9); affinity=4*eta/(KB*T)
    def cost(p):
        return gamma*(p-q*(1-p))*np.log(p/(q*(1-p)))
    pmax=brentq(lambda p:cost(p)-affinity*J,peq,1-1e-14,xtol=1e-15)
    return {'assumed_gate_free_energy_eV':E,'total_net_O2_turnovers_s':J,
            'assumed_eta_V':eta,'affinity':float(affinity),
            'thermal_p':float(peq),'max_p_from_entropy_budget':float(pmax),
            'max_population_ratio':float(pmax/peq),
            'warning':'Necessary bound, not sufficient attainable gate or current gain; E is not acquired.'}


def main():
    c=.192/(KB*T);tau=41e-9
    action_time=tau*(expi(c)-np.euler_gamma-np.log(c))
    kOH=2.3e9*np.exp(-.375/(KB*T))
    Q,r=ring([50,200,100,80,kOH,120])
    serial=pulse_response(Q,r,(4,5),c,tau)
    pi,g,J,h,w=poisson(Q,r)
    serial['short_pulse_formula']=float(pi[4]**2*(-np.expm1(-kOH*action_time)))
    serial['action_time_s']=float(action_time)
    serial['bound_J_times_action']=float(J*action_time)
    A=4*.28/(KB*T)
    rates=np.full(6,50.)
    Qt,rt=ring(rates,rates*np.exp(-A/6),trap=(.01,.0001))
    trap_oneway=pulse_response(Qt,rt,(6,0),c,tau)
    trap_sym=pulse_response(Qt,rt,(6,0),c,tau,symmetric=True)
    pt,gt,Jt,ht,wt=poisson(Qt,rt)
    trap_oneway['w_times_cold_rate']=float(wt[6,0]*Qt[6,0])
    trap_oneway['bound_J_times_action']=float(Jt*action_time)
    trap_oneway['thermodynamic_status']='Forward-only pulse uses an external transient affinity; autonomous realization must consume a charged mode and include reverse pumping.'
    trap_sym['thermodynamic_status']='Symmetric barrier lowering preserves detailed balance of the dead-end edge; exactly zero net reward from stationary initial distribution.'
    result={'scope':'Conditional constructed CTMCs, not inferred catalytic parameters.',
      'kOH_s':float(kOH),'pulse_action_time_s':float(action_time),
      'serial_cycle':serial,'reversible_ring_trap_oneway_pulse':trap_oneway,
      'reversible_ring_trap_symmetric_pulse':trap_sym,
      'depletion_local_Tafel':depletion_example(),
      'net_pump_targets_required_if_one_pulse_per_net_turnover':[
        {'baseline_TOF_s':j,'G':3.3,'z_lower':float((1-1/3.3)/(j*action_time))}
        for j in [.2,1.,4.]],
      'entropy_gate_bounds':[gate_resource(e,j) for e in [.126,.197] for j in [2.,20.,200.]]}
    p=Path(__file__).with_name('catalytic_cycle_response_results.json')
    p.write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
