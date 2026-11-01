"""Phase-preserving observation of a continuously hot quantum mediator.

Finite smooth force/readout construction, exact Gaussian channel costs,
and comparisons with the strongest linear estimator at the SAME gate phase.
All values are model calculations, not experimental results.
"""
from pathlib import Path
import os
import argparse
import json
import numpy as np
from scipy.integrate import cumulative_trapezoid
from numpy.polynomial.legendre import leggauss


def inner(x, y, wt):
    return np.vdot(x, wt*y)


def fixture(T=2., kh=.3, kc=1., target=np.pi/8, turns=1, points=640):
    z, wt=leggauss(points)
    t=(z+1)*T/2; wt=wt*T/2
    omega=2*np.pi*turns/T; a=np.pi/T
    sn=np.sin(a*t); cs=np.cos(a*t)
    r=sn**4
    rp=4*a*sn**3*cs
    rpp=4*a*a*(3*sn**2*cs**2-sn**4)
    rppp=4*a**3*(6*sn*cs**3-10*sn**3*cs)
    amp=np.sqrt(target/(omega*T*35/128))
    wave=amp*np.exp(1j*omega*t)
    beta=wave*r
    bd=wave*(rp+1j*omega*r)
    bdd=wave*(rpp+2j*omega*rp-omega**2*r)
    bddd=wave*(rppp+3j*omega*rpp-3*omega**2*rp-1j*omega**3*r)
    kap=kh+kc
    g=1j*(bd+kap/2*beta)
    gd=1j*(bdd+kap/2*bd)
    gdd=1j*(bddd+kap/2*bdd)
    E=float(inner(g,g,wt).real)
    phase=float(-inner(beta,g,wt).real)
    return dict(T=T,kh=kh,kc=kc,kap=kap,target=target,omega=omega,t=t,wt=wt,
                beta=beta,g=g,gd=gd,gdd=gdd,E=E,phase=phase,
                force_peak=float(np.max(abs(g))),
                force_peak_upper_bound=float(amp*np.sqrt(omega**2+(kap/2+3*np.sqrt(3)*a/4)**2)))


def cost(q, qd, cfg, occupation, eta=.8, q_initial=0., electronics=0.,
         qdd=None, readout='homodyne', bandwidth=None):
    """J: coherence exp[-(s-s')^2 J]. Initial-bus variance n+1/2.
    Feedback is exp(+i S Y_f), with Y_f the physical cold-output quadrature.
    """
    g=cfg['g']; wt=cfg['wt']; kc=cfg['kc']; kh=cfg['kh']; kap=cfg['kap']
    Vh=occupation+.5
    f=(g-kap*q/2+qd)/np.sqrt(kc)
    hot=float(Vh*kh*inner(q,q,wt).real)
    initial=float(Vh*abs(q_initial)**2)
    cold=float(.5*inner(f+np.sqrt(kc)*q,f+np.sqrt(kc)*q,wt).real)
    nu=(1-eta)/(2*eta) if readout=='homodyne' else 1/eta-.5
    if qdd is None: qdd=np.gradient(qd,cfg['t'],edge_order=2)
    fd=(cfg['gd']-kap*qd/2+qdd)/np.sqrt(kc)
    applied=f if bandwidth is None else f-fd/bandwidth
    detector=float(nu*inner(f,f,wt).real+electronics*inner(applied,applied,wt).real)
    phase=float(inner(g,q,wt).imag)
    weight=float(inner(f,f,wt).real)
    rms=float(np.sqrt(max(0,inner(fd,fd,wt).real)/weight)) if weight>1e-25 else 0.
    return dict(J=initial+hot+cold+detector,phase=phase,hot=hot,
                cold=cold,detector=detector,initial=initial,
                readout_squared_weight=weight,
                readout_peak=float(np.max(abs(f))),readout_rms_frequency=rms,
                applied_squared_weight=float(inner(applied,applied,wt).real),
                applied_peak=float(np.max(abs(applied))))


def optimize(cfg, occupation, eta=.8, modes=10, readout='homodyne',
             bandwidth=None,electronics=0.):
    """Exact finite profile family: q=sin^2(pi t/T) sum c_m exp(i2pi mt/T).
    Hence q,q' vanish at both endpoints. No protected quantum memory is used.
    The optimizer is global within this declared finite readout family.
    """
    t=cfg['t']; wt=cfg['wt']; T=cfg['T']; g=cfg['g']
    kc=cfg['kc']; kh=cfg['kh']; kap=cfg['kap']
    Vh=occupation+.5; Vc=.5
    nu=(1-eta)/(2*eta) if readout=='homodyne' else 1/eta-.5
    m=np.arange(-modes,modes+1); om=2*np.pi*m/T
    rr=np.sin(np.pi*t/T)**2
    rd=(np.pi/T)*np.sin(2*np.pi*t/T)
    rdd=2*(np.pi/T)**2*np.cos(2*np.pi*t/T)
    exp=np.exp(1j*t[:,None]*om[None,:])
    B=rr[:,None]*exp
    D=(rd[:,None]+1j*rr[:,None]*om[None,:])*exp
    D2=(rdd[:,None]+2j*rd[:,None]*om[None,:]-rr[:,None]*om[None,:]**2)*exp
    Pc=(D+(kc-kh)/2*B)/np.sqrt(kc)
    Pd=(D-kap/2*B)/np.sqrt(kc)
    A=Vh*kh*(B.conj().T@(wt[:,None]*B))
    A+=Vc*(Pc.conj().T@(wt[:,None]*Pc))
    A+=nu*(Pd.conj().T@(wt[:,None]*Pd))
    h=(Vc*Pc.conj().T+nu*Pd.conj().T)@(wt*g/np.sqrt(kc))
    if electronics:
        Pe=Pd if bandwidth is None else (D-kap/2*B-(D2-kap/2*D)/bandwidth)/np.sqrt(kc)
        ge=g/np.sqrt(kc) if bandwidth is None else (g-cfg['gd']/bandwidth)/np.sqrt(kc)
        A+=electronics*(Pe.conj().T@(wt[:,None]*Pe))
        h+=electronics*(Pe.conj().T@(wt*ge))
    v=B.conj().T@(wt*1j*g)
    c0=-np.linalg.solve(A,h)
    z=np.linalg.solve(A,v)
    den=float(np.vdot(v,z).real)
    p0=float(np.vdot(c0,v).real)
    cstar=c0+(cfg['target']-p0)/den*z
    results={}
    def evaluate(c):
        return cost(B@c,D@c,cfg,occupation,eta,qdd=D2@c,readout=readout,
                    bandwidth=bandwidth,electronics=electronics)
    for key,c in [('variance_only',c0),('phase_preserving',cstar)]:
        results[key]=evaluate(c)
    a=cfg['target']/cfg['E']
    results['hot_bound_attainer']=cost(1j*a*g,1j*a*cfg['gd'],cfg,occupation,eta,
        qdd=1j*a*cfg['gdd'],readout=readout,bandwidth=bandwidth,electronics=electronics)
    results['hot_lower_bound']=Vh*kh*cfg['target']**2/cfg['E']
    results['frontier_denominator']=den
    results['basis_modes']=int(2*modes+1)
    results['target']=cfg['target']
    reps=cfg['target']+np.arange(-8,9)*np.pi/4
    results['best_equivalent_phase']=float(reps[np.argmin((reps-p0)**2)])
    results['occupation']=occupation
    results['readout']=readout;results['bandwidth']=bandwidth;results['electronics_noise']=electronics
    # Check constrained optimality against feasible perturbations.
    rng=np.random.default_rng(24119)
    perturb_min=1e100
    for _ in range(12):
        dc=rng.normal(size=cstar.size)+1j*rng.normal(size=cstar.size)
        dc-=np.vdot(dc,v).real/np.vdot(v,v).real*v
        dc*=.01/np.linalg.norm(dc)
        dJ=evaluate(cstar+dc)['J']-results['phase_preserving']['J']
        perturb_min=min(perturb_min,dJ)
    results['minimum_feasible_test_cost_increase']=float(perturb_min)
    assert abs(results['phase_preserving']['phase']-cfg['target'])<1e-10
    assert abs(results['hot_bound_attainer']['hot']-results['hot_lower_bound'])<1e-10*max(1,occupation)
    assert perturb_min>=-1e-10
    # Analytic quadratic frontier, independently compare several gains.
    j0=results['variance_only']['J']
    maxfront=0.
    for p in np.linspace(-cfg['target'],2*cfg['target'],9):
        c=c0+(p-p0)/den*z
        direct=evaluate(c)['J']
        maxfront=max(maxfront,abs(direct-(j0+(p-p0)**2/den)))
    results['frontier_check_max_error']=float(maxfront)
    return results


def no_feedback(cfg,occupation):
    # Independent fine-grid backward Volterra integration for ordinary hot gate.
    t=np.linspace(0,cfg['T'],20001); T=cfg['T']; a=np.pi/T
    omega=cfg['omega']; r=np.sin(a*t)**4; rp=4*a*np.sin(a*t)**3*np.cos(a*t)
    amp=np.sqrt(cfg['target']/(omega*T*35/128))
    beta=amp*r*np.exp(1j*omega*t)
    g=1j*amp*np.exp(1j*omega*t)*(rp+(1j*omega+cfg['kap']/2)*r)
    integ=cumulative_trapezoid(np.exp(-cfg['kap']*t/2)*g,t,initial=0)
    q=np.exp(cfg['kap']*t/2)*(integ[-1]-integ)
    P=float(np.trapezoid(np.conj(g)*q,t).imag)
    Vh=occupation+.5
    J=Vh*abs(q[0])**2+(Vh*cfg['kh']+.5*cfg['kc'])*float(np.trapezoid(abs(q)**2,t))
    return dict(J=float(J),phase=P,initial=float(Vh*abs(q[0])**2))


def metrics(J,phase,target,data_rate=0.,duration=0.):
    spins=np.array([[1,1],[1,-1],[-1,1],[-1,-1]])
    s=spins.sum(1)
    mismatches=(spins[:,None,:]!=spins[None,:,:]).sum(2)
    M=np.exp(1j*(phase-target)*(s[:,None]**2-s[None,:]**2)
             -J*(s[:,None]-s[None,:])**2-data_rate*duration*mismatches)
    Fe=float(M.sum().real/16)
    bound=float(np.max(abs(1-M))/2)
    return dict(entanglement_fidelity=Fe,average_gate_fidelity=(4*Fe+1)/5,
                half_diamond_error_lower_bound=bound)


def main(output):
    out=Path(output);out.mkdir(exist_ok=True,parents=True)
    os.environ.setdefault('MPLCONFIGDIR',str(out.resolve()/'mpl-cache'))
    cfg=fixture()
    rows=[]
    for n in (0,1,10,100,1000,10000):
        r=optimize(cfg,n)
        r['no_feedback']=no_feedback(cfg,n)
        for kind in ('no_feedback','variance_only','phase_preserving','hot_bound_attainer'):
            r[kind].update(metrics(r[kind]['J'],r[kind]['phase'],cfg['target']))
        rows.append(r)
    convergence=[]
    for m in (4,6,10,16,24):
        r=optimize(cfg,100,modes=m)
        convergence.append(dict(modes=2*m+1,J=r['phase_preserving']['J'],
                                phase=r['phase_preserving']['phase']))
    finite_bandwidth=[optimize(cfg,n,readout='heterodyne',bandwidth=10.,electronics=.01)
                      for n in (0,10,100,1000)]
    # Finite-response acquisition on an arbitrary smooth detector trajectory,
    # including nonzero initial/final detector states.
    ca=cfg['target']/cfg['E']; Bdet=10.; tt=cfg['t']; ww=cfg['wt']
    q=1j*ca*cfg['g']; qd=1j*ca*cfg['gd']; qdd=1j*ca*cfg['gdd']
    f=(cfg['g']-cfg['kap']*q/2+qd)/np.sqrt(cfg['kc'])
    fd=(cfg['gd']-cfg['kap']*qd/2+qdd)/np.sqrt(cfg['kc'])
    x=np.exp(7j*tt)+.3*np.sin(9*tt)+.2*tt/cfg['T']
    xd=7j*np.exp(7j*tt)+2.7*np.cos(9*tt)+.2/cfg['T']
    response_error=float(abs(np.sum(ww*f*(x+xd/Bdet))-np.sum(ww*(f-fd/Bdet)*x)))
    noise_weight_error=float(abs(inner(f-fd/Bdet,f-fd/Bdet,ww).real-
                  inner(f,f,ww).real-inner(fd,fd,ww).real/Bdet**2))
    assert max(response_error,noise_weight_error)<1e-10
    report=dict(model={k:cfg[k] for k in ('T','kh','kc','kap','target','omega','E','phase','force_peak','force_peak_upper_bound')},
                detector_efficiency=.8,rows=rows,finite_profile_convergence=convergence,
                finite_detector_bandwidth=finite_bandwidth,
                finite_response_identity_error=response_error,
                finite_response_noise_weight_error=noise_weight_error,
                conventions='J multiplies (s-sprime)^2; S=Z1+Z2; covariance vacuum=1/2; no data faults in quoted fidelities',
                scope='Exact Gaussian costs for finite smooth profiles. Numerical quadrature; independent collision and Fock checks accompany this file.')
    (out/'phase_frontier_results.json').write_text(json.dumps(report,indent=2))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,axs=plt.subplots(1,3,figsize=(14,4.2),layout='constrained')
    ns=np.array([r['occupation']+.5 for r in rows])
    colors={'no_feedback':'#657387','variance_only':'#df8f22','phase_preserving':'#176f8a'}
    labels={'no_feedback':'Ordinary closed loop','variance_only':'Minimize noise only','phase_preserving':'Retain the entangling gate'}
    for key in colors:
        axs[0].loglog(ns,[r[key]['J'] for r in rows],'o-',color=colors[key],label=labels[key])
        axs[1].semilogx(ns,[r[key]['phase']/cfg['target'] for r in rows],'o-',color=colors[key])
    axs[0].loglog(ns,[r['hot_lower_bound'] for r in rows],'--',color='#292929',label='Unavoidable hot contribution')
    axs[0].set(xlabel='Hot quadrature variance n + ½',ylabel='Dephasing coefficient J',title='Noise alone gives the wrong objective')
    axs[0].legend(fontsize=8)
    axs[1].set(xlabel='Hot quadrature variance n + ½',ylabel='Retained phase / required phase',ylim=(-.02,1.08),title='The quietest output loses its interaction')
    r=rows[2]; p=np.linspace(0,1.4*cfg['target'],250)
    j=r['variance_only']['J']+(p-r['variance_only']['phase'])**2/r['frontier_denominator']
    axs[2].plot(p/cfg['target'],j,color='#176f8a',lw=2)
    axs[2].plot([1],[r['phase_preserving']['J']],'o',color='#176f8a')
    axs[2].plot([r['variance_only']['phase']/cfg['target']],[r['variance_only']['J']],'o',color='#df8f22')
    axs[2].set(xlabel='Retained phase / required phase',ylabel='Minimum J in 21-mode readout family',title='Exact tradeoff at thermal occupation 10')
    fig.suptitle('Cold-output observation: preserving the interaction has a thermal cost',fontsize=14)
    fig.savefig(out/'phase_noise_frontier.png',dpi=180)
    plt.close(fig)
    print(json.dumps({'model':report['model'],'rows':[{'n':r['occupation'],'J_unobserved':r['no_feedback']['J'],
          'J_min_noise':r['variance_only']['J'],'phase_min_noise':r['variance_only']['phase'],
          'J_preserved':r['phase_preserving']['J'],'hot_bound':r['hot_lower_bound']} for r in rows],
          'convergence':convergence},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='warm_phase_results')
    main(p.parse_args().output)
