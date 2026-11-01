"""Exact finite-duration feedback sensor: deterministic transfer matrices.

Model: one sensing qubit S, protected qubit A and a fresh meter M per cycle.
H_signal=omega Z_S/2, L=sqrt(gamma_j) sigma_theta^S.
During tau: H_meter=g_s Z_S X_M+g_a Z_A X_M, g_a*tau=pi/4.
A finite coherent CZ(A,M) erases the meter's logical phase before noisy
classical readout. All correction/readout/reset delay d is charged at the
old noise rate. The report selects gamma_low or gamma_high next cycle.

The tilted 4x4 matrix integrates ALL sensor jumps and all meter outcomes.
No Monte Carlo, truncated fault count, infinitesimal readout, or learned
noise-angle value is used in this main calculation.
"""
from pathlib import Path
import json
import math
import os
import numpy as np
from scipy.linalg import expm, expm_frechet

Z=np.diag([1.,-1.])

def propagator(gamma, omega, t):
    Q=np.array([[-gamma,gamma],[gamma,-gamma]],complex)
    return expm((Q-1j*omega*Z)*t)

def prop_derivative(gamma, omega, t):
    Q=np.array([[-gamma,gamma],[gamma,-gamma]],complex)
    return expm_frechet((Q-1j*omega*Z)*t,-1j*Z*t,compute_expm=False)

def transfer(omega, rates=(1.,4.), tau=.1, dead=.1, eta=.8, angle=np.pi/2):
    lam=angle/tau
    K=np.zeros((4,4),complex)
    for j,gamma in enumerate(rates):
        E=propagator(gamma,omega,tau)
        sine=(propagator(gamma,omega-lam,tau)-propagator(gamma,omega+lam,tau))/(2j)
        G=propagator(gamma,omega,dead)
        for jp,u in enumerate([1.,-1.]):
            K[2*jp:2*jp+2,2*j:2*j+2]=G@(E+u*eta*sine)/2
    return K

def transfer_derivative(omega=0.,rates=(1.,4.),tau=.1,dead=.1,eta=.8,angle=np.pi/2):
    lam=angle/tau
    K=np.zeros((4,4),complex)
    for j,gamma in enumerate(rates):
        E=propagator(gamma,omega,tau)
        dE=prop_derivative(gamma,omega,tau)
        sine=(propagator(gamma,omega-lam,tau)-propagator(gamma,omega+lam,tau))/(2j)
        dsine=(prop_derivative(gamma,omega-lam,tau)-prop_derivative(gamma,omega+lam,tau))/(2j)
        G=propagator(gamma,omega,dead)
        dG=prop_derivative(gamma,omega,dead)
        for jp,u in enumerate([1.,-1.]):
            K[2*jp:2*jp+2,2*j:2*j+2]=(dG@(E+u*eta*sine)+G@(dE+u*eta*dsine))/2
    return K

def stationary_formula(rates=(1.,4.),tau=.1,dead=.1,eta=.8,angle=np.pi/2):
    dt=tau+dead
    g=np.array(rates)
    lam=angle/tau
    q=-np.expm1(-2*g*dt)/2
    b=np.exp(-2*g*dead)
    # Expression analytic also for gamma=lambda; evaluate sine moment directly.
    s=np.array([(1j*propagator(x,lam,tau)[0,0]).real for x in g])
    Q=q.sum()
    D=eta*np.sum(s*b)/(2-eta**2*(s[0]*b[0]-s[1]*b[1])*(s[0]*q[1]-s[1]*q[0])/Q)
    m=np.array([q[1],-q[0]])*D/Q
    xl=.5+eta*D*(s[0]*q[1]-s[1]*q[0])/(2*Q)
    mass=np.array([xl,1-xl])
    pi=np.array([(mass[0]+m[0])/2,(mass[0]-m[0])/2,
                 (mass[1]+m[1])/2,(mass[1]-m[1])/2])
    velocity=D*q[0]*q[1]*(1/g[0]-1/g[1])/(dt*Q)
    pe=(1+D*(q[1]-q[0])/Q)/2
    return dict(pi=pi,velocity=float(velocity),even_probability=float(pe),D=float(D),
                q=q,s=s,asymptotic_F_over_T2=float((pe*velocity)**2))

def finite_information(n,**kwargs):
    K=transfer(0.,**kwargs)
    dK=transfer_derivative(0.,**kwargs)
    # Block power gives exact derivative of the matrix power without differencing.
    block=np.block([[K,dK],[np.zeros_like(K),K]])
    power=np.linalg.matrix_power(block,int(n))
    start=np.array([1.,0.,0.,0.])
    end=np.array([1.,0.,1.,0.])
    pe=float((end@power[:4,:4]@start).real)
    moment=float((1j*end@power[:4,4:]@start).real)
    T=n*(kwargs.get('tau',.1)+kwargs.get('dead',.1))
    return dict(cycles=int(n),time=T,even_probability=pe,signed_even_exposure=moment,
                achieved_F=moment**2,F_over_T2=(moment/T)**2,
                ideal_herald_F=moment**2/pe)

def final_mean(omega,n,**kwargs):
    start=np.array([1.,0.,0.,0.])
    end=np.array([1.,0.,1.,0.])
    return float(-(end@np.linalg.matrix_power(transfer(omega,**kwargs),int(n))@start).imag)

def run_checks():
    rng=np.random.default_rng(718244)
    residual=0.
    minimum=1.
    derivative_error=0.
    for _ in range(100):
        rates=tuple(np.sort(np.exp(rng.uniform(-2,2,2))))
        tau=float(np.exp(rng.uniform(-3,0)))
        dead=float(np.exp(rng.uniform(-4,0)))
        eta=float(rng.uniform(.05,1))
        angle=float(rng.uniform(.05,np.pi/2))
        kw=dict(rates=rates,tau=tau,dead=dead,eta=eta,angle=angle)
        K=transfer(0.,**kw)
        f=stationary_formula(**kw)
        residual=max(residual,float(np.max(abs(K@f['pi']-f['pi']))),float(np.max(abs(K.sum(0)-1))))
        minimum=min(minimum,float(K.real.min()))
        v=float((1j*np.ones(4)@transfer_derivative(0.,**kw)@f['pi']).real/(tau+dead))
        residual=max(residual,abs(v-f['velocity']))
        h=1e-5
        diff=(transfer(h,**kw)-transfer(-h,**kw))/(2*h)
        derivative_error=max(derivative_error,float(np.max(abs(diff-transfer_derivative(0.,**kw)))))
        assert f['velocity']>0
    assert residual<1e-10
    assert minimum>-1e-12
    assert derivative_error<1e-8
    # Loss of either rate contrast or usable record removes the linear drift.
    for kw in [dict(rates=(2.,2.)),dict(eta=0.)]:
        assert abs(stationary_formula(**kw)['velocity'])<1e-12
    return dict(cases=100,stationary_and_velocity_max_residual=residual,
                minimum_transition_probability=minimum,derivative_max_residual=derivative_error)

def generate_outputs(directory):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    kw=dict(rates=(1.,4.),tau=.1,dead=.1,eta=.8,angle=np.pi/2)
    formula=stationary_formula(**kw)
    table=[finite_information(n,**kw) for n in [10,30,100,300,1000,3000,10000]]
    check=run_checks()
    report={'model':'exact finite-duration meter and feedback with all sensor exposure',
            'parameters':{k:list(v) if isinstance(v,tuple) else float(v) for k,v in kw.items()},
            'stationary':{k:v.tolist() if isinstance(v,np.ndarray) else v for k,v in formula.items()},
            'finite_information':table,'checks':check}
    # Show local window directly, not a claim of globally identifiable long fringes.
    report['local_fringes']=[{'cycles':n,'scaled_residual':h,'mean':final_mean(h/(.2*n),n,**kw)}
                            for n in [100,1000,10000] for h in [-2,-1,0,1,2]]
    C=formula['asymptotic_F_over_T2'];delta=kw['tau']+kw['dead']
    report['phase_fault_examples']=[]
    for p in [1e-5,1e-4,1e-3]:
        G=-math.log1p(-2*p)/delta
        report['phase_fault_examples'].append(dict(p_gate=p,coherence_decay_rate=G,
            max_single_rate_F_ratio=C/(2*math.e*G),optimal_comparison_time=1/(2*G)))
    report['phase_fault_threshold_vs_fixed_rate_bound']=.5*(1-math.exp(-delta*C/(2*math.e)))
    report['p1e5_F_at_T2000']=table[-1]['achieved_F']*(1-2e-5)**20000
    readout_repeats=math.ceil(2/.8**2*math.log(10000/.01))
    readout_repeats+=1-readout_repeats%2
    report['deferred_frame_example']=dict(meter_uses=10000,readout_error=.1,
        total_frame_failure_budget=.01,reads_per_meter=readout_repeats,
        total_reads=10000*readout_repeats,read_duration=.1,
        parallel_meter_bound=1+math.ceil(readout_repeats*.1/delta))
    (directory/'finite_controller_results.json').write_text(json.dumps(report,indent=2)+'\n')
    os.environ.setdefault('MPLCONFIGDIR','producer-workspace/astra_sensing_matplotlib')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
    fig,axs=plt.subplots(1,2,figsize=(11,4.2),layout='constrained')
    ns=np.unique(np.logspace(1,4,65).astype(int))
    vals=[finite_information(n,**kw) for n in ns]
    ts=np.array([x['time'] for x in vals]);fs=np.array([x['achieved_F'] for x in vals])
    axs[0].loglog(ts,fs,label='Finite meter + scalar rate feedback',color='#087e8b',lw=2.2)
    axs[0].loglog(ts,formula['asymptotic_F_over_T2']*ts**2,'--',color='#b35a24',label='Proved asymptotic coefficient × T²')
    axs[0].loglog(ts,ts,':',color='#555555',label='Fixed-rate bound; no rate-control resource')
    axs[0].set(xlabel='Total time T (units of 1/γ low)',ylabel='Achieved local classical Fisher information')
    axs[0].legend(fontsize=8);axs[0].grid(alpha=.2,which='both')
    hs=np.linspace(-4,4,121)
    for n,c in [(100,'#9a6700'),(1000,'#087e8b'),(10000,'#6534ac')]:
        axs[1].plot(hs,[final_mean(h/(.2*n),n,**kw) for h in hs],color=c,label=f'T={.2*n:g}')
    axs[1].plot(hs,formula['even_probability']*np.sin(formula['velocity']*hs),'k--',lw=1,label='Local limit')
    axs[1].set(xlabel='Residual frequency × total time',ylabel='Mean final binary readout',ylim=(-1,1))
    axs[1].legend(fontsize=8);axs[1].grid(alpha=.2)
    fig.suptitle('Mathematical model: finite measurement, continuing noise, 10% report errors\nProtected ancilla and exact coherent erasure gate assumed; no hardware data',fontsize=11)
    fig.savefig(directory/'finite_controller_scaling.png',dpi=180)
    plt.close(fig)
    print(json.dumps({'checks':check,'stationary':report['stationary'],'finite_information':table},indent=2))

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',default='astra_sensing_20261101')
    generate_outputs(parser.parse_args().output)
