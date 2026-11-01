"""All-history exponential Lyapunov admission for a retained directly damped bus.

Every cycle contains a finite loop, a finite opening ramp, readout/hold, and a
finite closing ramp. Bounded residual force acts throughout. The stated warm
Markov bath and clipped force envelope are physical model assumptions; neither
conditional states nor independent error coins are assumed.
"""
from pathlib import Path
import json, math, sys
import numpy as np
from scipy.integrate import solve_ivp, simpson
from scipy.optimize import differential_evolution

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'phase8/physical_mechanisms'))
from double_closed_hot_bus import loop

PULSE=json.loads((ROOT/'phase8/physical_mechanisms/one_bus_parity_results.json').read_text())['optimized_safe']


def force_profile(points=4001):
    T=PULSE['T']; k=PULSE['kappa']; A,B,c=PULSE['coefficients']
    t=np.linspace(0,T,points);q=np.pi*t/T;dq=np.pi/T;s=np.sin(q);co=np.cos(q)
    X=s*s*np.sin(2*q); Xp=dq*(2*s*co*np.sin(2*q)+2*s*s*np.cos(2*q))
    Y=s*s*(np.cos(2*q)+.5); Yp=dq*(2*s*co*(np.cos(2*q)+.5)-2*s*s*np.sin(2*q))
    ef=np.exp(k*t/2);x=ef*X;xp=ef*(Xp+k*X/2);y=ef*Y;yp=ef*(Yp+k*Y/2)
    y=y-c*x;yp=yp-c*xp;x*=A;xp*=A;y*=B;yp*=B
    f1=1j*(xp+k*x/2);f2=-(yp+k*y/2)
    bound=np.sqrt(4*abs(f1)**2+abs(f2)**2)
    return t,bound,float(simpson(bound,x=t))

FT,FU,LOOP_ACTION=force_profile()


def model_values(t,cfg):
    T=PULSE['T']; ramp=cfg['switch_time']; hold=cfg['readout_hold_time']; k0=PULSE['kappa'];kR=cfg['readout_damping']
    if t<=T:
        return k0,float(np.interp(t,FT,FU))+cfg['force_error_cap'],True
    t-=T
    if t<ramp:k=k0+(kR-k0)*math.sin(math.pi*t/(2*ramp))**2
    elif t<ramp+hold:k=kR
    else:k=k0+(kR-k0)*math.cos(math.pi*(t-ramp-hold)/(2*ramp))**2
    return k,cfg['force_error_cap'],False


def integrate_characteristic(theta0,eps_loop,eps_idle,cfg,dense=False):
    Tcycle=PULSE['T']+2*cfg['switch_time']+cfg['readout_hold_time'];nb=cfg['thermal_nmax']
    def rhs(t,y):
        th=y[0]
        if th>20: return [0,1e30]
        k,u,isloop=model_values(t,cfg);eps=eps_loop if isloop else eps_idle
        d=(-math.expm1(-th))*(1-nb*math.expm1(th))
        sh=2*math.sinh(th/2)
        return [k*d-u*eps*sh,k*nb*math.expm1(th)+u/eps*sh]
    sol=solve_ivp(rhs,[0,Tcycle],[theta0,0.],rtol=1e-8,atol=1e-10,max_step=.04,dense_output=True)
    if not sol.success:return None
    theta1=sol.y[0,-1];c=sol.y[1,-1]
    if theta1<=theta0 or theta0>=math.log1p(1/cfg['initial_nbar']):return None
    B0=-math.log1p(-cfg['initial_nbar']*math.expm1(theta0))
    B=max(B0,theta0*c/(theta1-theta0))
    tt=np.unique(np.r_[np.linspace(0,Tcycle,601),FT])
    yy=sol.sol(tt);th=yy[0];co=yy[1];thp=float(th.min())
    if thp<=0:return None
    Emax=float(np.max((B+co)/th))
    out=dict(theta_boundary=theta0,theta_cycle_end=float(theta1),epsilon_loop=eps_loop,
             epsilon_idle=eps_idle,log_M_boundary=B,log_M_initial=B0,
             theta_peak=thp,log_M_peak=thp*Emax,mean_bound_from_moment=Emax,
             cycle_time=Tcycle,loop_time=PULSE['T'],loop_force_action=LOOP_ACTION,
             all_interval_force_action=LOOP_ACTION+cfg['force_error_cap']*Tcycle)
    if dense:out['trace']={'t':tt.tolist(),'theta':th.tolist(),'cost':co.tolist()}
    return out


def force_cap_comparison(c,cycles,delta,force_difference_action_per_cycle):
    # D = F(a+a^dag) - P F(a+a^dag) P satisfies
    # ||D psi|| <= 2 ||F|| sqrt(<(N+1) 1_{N>=L}>).
    # Half trace distance <= 2 action sqrt(L+1) exp[(B-theta L)/2].
    action=cycles*force_difference_action_per_cycle
    B=c['log_M_peak'];th=c['theta_peak']
    if action==0:return dict(cutoff=0,half_trace_bound=0.)
    L=max(1,int((B+2*math.log(max(2*action/delta,1)))/th))
    L=max(L,int(1/th)+1)
    while math.log(2*action)+.5*math.log(L+1)+.5*(B-th*L)>math.log(delta):L+=1
    val=2*action*math.sqrt(L+1)*math.exp((B-th*L)/2)
    eta=4*force_difference_action_per_cycle*math.sqrt(L) # full diamond integrated perturbation
    return dict(cycles=int(cycles),target_half_trace=delta,force_difference_action_per_cycle=force_difference_action_per_cycle,
                cutoff=L,half_trace_bound=val,bounded_force_generator_norm_per_cycle=eta)


def optimize(cfg,cycles,delta,da):
    thmax=min(math.log1p(1/cfg['thermal_nmax']),math.log1p(1/cfg['initial_nbar']))*.999
    def obj(v):
        c=integrate_characteristic(v[0],v[1],v[2],cfg)
        if c is None:return 1e9
        th=c['theta_peak'];L=c['mean_bound_from_moment']+2*math.log(2*cycles*da/delta)/th
        return L+math.log(max(L,1))/th
    opt=differential_evolution(obj,[(.05,thmax),(.02,.8),(.02,5)],seed=20261102,maxiter=80,popsize=8,tol=2e-5,polish=True)
    c=integrate_characteristic(*opt.x,cfg,dense=False)
    c['optimization_success']=bool(opt.success)
    c['comparison']=force_cap_comparison(c,cycles,delta,da)
    return c


def main():
    cfg=dict(switch_time=.1,readout_hold_time=3.,readout_damping=1.,thermal_nmax=.1,initial_nbar=.3,force_error_cap=1e-6)
    # First scenario caps all residual force with a deliberately much larger budget
    # than the closure-only pole-projection error. Second uses a small projection budget.
    cases=[]
    for cycles,delta,da in [(10**6,1e-6,1e-6*(PULSE['T']+3.2)),(10**12,1e-9,1e-6*(PULSE['T']+3.2)),(10**6,1e-6,1e-9)]:
        cases.append(optimize(cfg,cycles,delta,da))
    ans=dict(physical_model=cfg,pulse_source='phase8/physical_mechanisms/one_bus_parity_results.json',
             physical_damping_action=PULSE['kappa']*PULSE['T']+cfg['readout_damping']*cfg['readout_hold_time']+(PULSE['kappa']+cfg['readout_damping'])*cfg['switch_time'],
             cases=cases,
             scope=['Single directly damped effective mode; this is not an adiabatic elimination certificate for a finite converter.',
                    'The thermal bath may have occupation at most thermal_nmax at every time; all field inputs must be fresh Markov inputs.',
                    'The force error cap is a physical bounded actuator envelope, including the nominally off intervals.',
                    'Arbitrary data operations and measurement histories are included because the generator inequality is operator valued.',
                    'Initial exponential moment is a physical admission family, not earned from unrestricted input by finite cooling.',
                    'No conditional photon cap, observed flag, independent fault coin, or actual oscillator truncation is introduced.',
                    'Full physical readout/control/data fault rates are separate ledger entries; the displayed result controls bosonic rare-history amplification only.'])
    (HERE/'retained_bus_all_interval_results.json').write_text(json.dumps(ans,indent=2)+'\n')
    print(json.dumps(ans,indent=2))

if __name__=='__main__':main()
