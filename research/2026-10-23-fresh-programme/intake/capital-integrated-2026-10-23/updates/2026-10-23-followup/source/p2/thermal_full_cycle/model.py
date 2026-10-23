"""Private Astra P2 two-mode thermal model. No acquired device data.

This file evaluates a stated linear quantum-Langevin model, its steady
heat/work balances, exact normalized feasibility gates, and a deliberately
optimistic hot-side overlap construction. All example numbers are synthetic.
Run: python thermal_full_cycle/model.py
"""
from pathlib import Path
import json
import platform
import time
import numpy as np
from scipy.linalg import solve_continuous_lyapunov
from scipy.optimize import minimize_scalar, brentq

OUT = Path(__file__).resolve().parent
HBAR = 1.054571817e-34
KB = 1.380649e-23


def bose(omega, temperature):
    return 1.0 / np.expm1(HBAR * omega / (KB * temperature))


def two_mode(w, temperatures, rates, g, detuning=0.0):
    """rates[j,r], r=0 cold, r=1 hot; heat positive out of reservoir.

    detuning is the rotating-frame mismatch. Work uses wp=w2-w1
    for the resonant calculation. Off resonance the rates are an approximate
    local model; no exact thermodynamic detuned-work claim is made here.
    """
    w = np.asarray(w, float)
    rates = np.asarray(rates, float)
    occ = bose(w[:, None], np.asarray(temperatures)[None, :])
    k = rates.sum(axis=1)
    f = rates[:, 0] / k
    nbar = (rates * occ).sum(axis=1) / k
    ceff = (4 * g*g / np.prod(k)) / (1 + (2*detuning / sum(k))**2)
    current = np.prod(k) / sum(k) * ceff / (1 + ceff) * (nbar[0]-nbar[1])
    populations = nbar + np.array([-current/k[0], current/k[1]])
    heat_by_mode_bath = HBAR * w[:, None] * rates * (occ-populations[:, None])
    heat = heat_by_mode_bath.sum(axis=0)
    leak = np.sum(HBAR*w*k*f*(1-f)*(occ[:, 1]-occ[:, 0]))
    qstar = HBAR*(w[0]*f[0]-w[1]*f[1])*np.prod(k)/sum(k)*(nbar[0]-nbar[1])
    work = HBAR*(w[1]-w[0])*current
    return dict(occupations=occ, k=k, f=f, nbar=nbar, C=ceff,
                current=current, populations=populations, heat=heat,
                leak=leak, Qstar=qstar, conversion_work=work,
                entropy_production=-sum(heat/np.asarray(temperatures)))


def numeric_covariance(w, temperatures, rates, g, detuning=0.0):
    """Direct complex covariance solution, independent of eliminated flow."""
    rates=np.asarray(rates, float)
    occ=bose(np.asarray(w)[:,None], np.asarray(temperatures)[None,:])
    k=rates.sum(axis=1)
    drift=np.array([[-k[0]/2-1j*detuning/2, -1j*g],
                    [-1j*g, -k[1]/2+1j*detuning/2]])
    diffusion=np.diag((rates*occ).sum(axis=1))
    covariance=solve_continuous_lyapunov(drift, -diffusion)
    pops=np.diag(covariance).real
    heat=(HBAR*np.asarray(w)[:,None]*rates*(occ-pops[:,None])).sum(axis=0)
    return covariance, heat


def threshold(leakage, power, cmax=np.inf):
    """Supremum b for positive C/(1+C)-b*C**power-leakage.

    Strict b < threshold is required; equality gives at best zero heat.
    0<power<=1. Unlimited C permitted only as a mathematical envelope.
    """
    p=float(power); ell=float(leakage)
    if not (0 < p <= 1) or ell < 0:
        raise ValueError('0<p<=1 and ell>=0 required')
    if ell >= 1 or cmax <= ell/(1-ell):
        return 0.0, None
    if p == 1 and ell == 0:
        return 1.0, 0.0
    s=(1-p+np.sqrt((1-p)**2+4*p*ell))/2
    s=min(s, cmax/(1+cmax)) if np.isfinite(cmax) else s
    c=s/(1-s)
    return float((s-ell)*((1-s)/s)**p), float(c)


def remote_cooling(x, z, a, d):
    """Qc/Q0 with A=a B, x=hot low-mode loss/B, 4 Xi=z B.

    g^2=x_loss*Xi is the SATURATED Cauchy envelope, not an acquired material.
    d=(n(w1,Th)-n(w1,Tc))/(n(w1,Tc)-n(w2,Th)); both positive.
    """
    return ((a+1)*x*(z*(1-d*x)-d*(a+x+1)) /
            ((a+x+1)*(a+x+z*x)))


def remote_coefficient(x, a, d):
    """Max b for remote_cooling(x,z)-b*z>0 at some z."""
    if x <= 0 or x >= 1/d:
        return 0.0
    gain=(a+1)/(a+x+1)*(1+d*x/(a+x))
    leak=d*(a+1)*x/(a+x)
    return float(x/(a+x)*(np.sqrt(gain)-np.sqrt(leak))**2)


def best_remote(a, d, cold_loss_per_z, xmax=None, zmax=np.inf):
    """Exact inner elimination and numerical outer optimization of an envelope.

    No global-optimum certification of the outer numerical search is claimed.
    """
    if cold_loss_per_z < 0:
        raise ValueError('cold loss must be nonnegative')
    if cold_loss_per_z == 0 and not np.isfinite(zmax):
        raise ValueError('zero cold loss requires a finite physical zmax; the unlimited-drive limit is only a supremum')
    xmax=min(1/d, xmax) if xmax is not None else 1/d
    def at_x(x):
        gain=(a+1)/(a+x+1)*(1+d*x/(a+x))
        leak=d*(a+1)*x/(a+x)
        alpha=cold_loss_per_z*(a+x)/(x*gain)
        if alpha >= 1:
            return -leak, 0.0
        c=(1/np.sqrt(alpha)-1) if alpha > 0 else np.inf
        z=min((a+x)/x*c, zmax)
        q=remote_cooling(x,z,a,d)-cold_loss_per_z*z
        return float(q),float(z)
    opt=minimize_scalar(lambda x:-at_x(x)[0], bounds=(1e-10,xmax*(1-1e-10)),
                        method='bounded',options={'xatol':1e-13})
    q,z=at_x(opt.x)
    if q <= 0:
        return dict(x=None,z=None,net_Q_over_Q0=0.,operating=False)
    return dict(x=float(opt.x),z=z,net_Q_over_Q0=q,operating=True)


def all_contact_loss_threshold(d):
    """Analytic maximization over a=A/B>0 and X=x/B>0.

    Returned Hcrit bounds R=f*(Omega/w1)*kp/(4*xi*Delta0), assuming
    the overlap envelope g^2=x*xi*N can saturate and linewidths are tunable
    independently of xi. At threshold cooling is zero.
    """
    if not np.isfinite(d) or d <= 0:
        raise ValueError('finite d>0 required; d=0 is a separate limiting case')
    # Scale the polynomial root before solving: a fixed absolute bracket/tolerance
    # on s fails for d << 1. This formulation has a root of order one for all d.
    smax=(d/(1+d))**(1/3)
    u=brentq(lambda u:1-smax*smax*u*u-u**3*(2+smax*u),0.,1.,
             xtol=5e-15)
    s=smax*u
    r=u**3/(1+d*(1-u**3))
    t=1/s-1
    a=(1-r)*t
    x=r*t
    z=d*(1+s+s*s)/(s*s)
    # Algebraically equal to the cube-root difference, without cancellation.
    h=r*(1-r)*(1-s)**2/(1+s+s*s)
    return dict(Hcrit=float(h),s=float(s),low_mode_hot_fraction=float(r),
                A_over_B=float(a),x_over_B=float(x),z=float(z))


def main():
    started=time.perf_counter()
    rng=np.random.default_rng(20261023)
    residuals=[]; entropy=[]
    for _ in range(500):
        w=2*np.pi*np.array([rng.uniform(10,30),rng.uniform(35,60)])*1e12
        temperatures=np.array([rng.uniform(200,350),rng.uniform(360,500)])
        rates=10**rng.uniform(9,12,size=(2,2))
        g=np.sqrt(np.prod(rates.sum(axis=1)))/2*10**rng.uniform(-1,1)
        exact=two_mode(w,temperatures,rates,g)
        cov,heat=numeric_covariance(w,temperatures,rates,g)
        scale=max(abs(exact['heat']).max(),abs(exact['Qstar']),exact['leak'],1e-30)
        residuals.append(float(max(abs(heat-exact['heat']))/scale))
        residuals.append(float(abs(sum(exact['heat'])+exact['conversion_work'])/scale))
        residuals.append(float(abs(exact['heat'][0]-(exact['Qstar']*exact['C']/(1+exact['C'])-exact['leak']))/scale))
        entropy.append(float(exact['entropy_production']))
        # Detuned covariance check: heat formula alone, no exact detuned work assertion.
        delta=rng.normal()*rates.sum()
        exact_d=two_mode(w,temperatures,rates,g,delta)
        _,heat_d=numeric_covariance(w,temperatures,rates,g,delta)
        residuals.append(float(max(abs(heat_d-exact_d['heat']))/scale))
    assert max(residuals)<1e-10
    assert min(entropy)>-1e-22

    gate_checks=[]
    for p in [1.,.5,1/3,1/4,.7]:
        for ell in [0.,.01,.1,.4,.8,.99]:
            b,c=threshold(ell,p)
            cs=np.geomspace(1e-9,1e7,100001)
            test=(cs/(1+cs)-ell)/(cs**p)
            grid_max=max(0.,float(test.max()))
            assert abs(grid_max-b)<2e-7
            gate_checks.append(dict(power=p,leakage=ell,b_critical=b,C_at_tangency=c))

    # Fully declared synthetic thermal example. No material response is supplied.
    tc,th=300.,330.
    w=2*np.pi*np.array([20.,24.])*1e12
    kappa=2*np.pi*.1e12
    delta0=bose(w[0],tc)-bose(w[1],th)
    deltaa=bose(w[0],th)-bose(w[0],tc)
    d=float(deltaa/delta0)
    q0=HBAR*w[0]*kappa/2*delta0
    contact_rows=[]
    for eps in [0.,.005,.01,.02,.05,.1,.15,.2,.3,.4]:
        rates=kappa*np.array([[1-eps,eps],[eps,1-eps]])
        r=two_mode(w,[tc,th],rates,kappa/2)
        ell=r['leak']/r['Qstar'] if r['Qstar']>0 else np.inf
        bnorm,_=threshold(ell,1) if np.isfinite(ell) else (0,None)
        contact_rows.append(dict(cross_fraction=eps,Qstar_over_Q0=float(r['Qstar']/q0),
                         bath_leak_over_Q0=float(r['leak']/q0),normalized_leak=float(ell),
                         max_cold_pump_loss_per_C_over_Q0=float(max(0.,r['Qstar']/q0*bnorm))))

    # Remote hot-side sheet: exact independent covariance checks of overlap formula.
    remote_res=[]
    for _ in range(200):
        a=10**rng.uniform(-1,1);x=10**rng.uniform(-4,1);z=10**rng.uniform(-1,3)
        rates=kappa*np.array([[a,x],[0,1.]])
        g=kappa*np.sqrt(x*z)/2
        r=two_mode(w,[tc,th],rates,g)
        base=HBAR*w[0]*kappa*a/(a+1)*delta0
        remote_res.append(abs(r['heat'][0]/base-remote_cooling(x,z,a,d)))
    assert max(remote_res)<1e-10
    a=1.
    boundary=minimize_scalar(lambda x:-remote_coefficient(x,a,d),
                            bounds=(1e-12,1/d*(1-1e-10)),method='bounded',
                            options={'xatol':1e-14})
    bmax=float(-boundary.fun)
    all_contact=all_contact_loss_threshold(d)
    check=remote_coefficient(all_contact['x_over_B'],all_contact['A_over_B'],d)
    check*=all_contact['A_over_B']/(all_contact['A_over_B']+1)
    assert abs(check-all_contact['Hcrit'])<1e-12
    # An independent audit exposed a fixed-tolerance small-d failure. The
    # normalized solve must recover Hcrit -> 1/4 as the hot noise penalty vanishes.
    tiny_d=all_contact_loss_threshold(1e-36)
    assert abs(tiny_d['Hcrit']-.25)<1e-10
    try:
        best_remote(1.,d,0.)
    except ValueError:
        pass
    else:
        raise AssertionError('unbounded zero-loss edge must be explicit')
    remote_rows=[]
    for fraction in [.01,.05,.1,.25,.5,.75,.9,1.,1.1]:
        result=best_remote(a,d,bmax*fraction)
        result.update(loss_fraction_of_max=fraction,cold_loss_per_z=bmax*fraction)
        if result['operating']:
            x,z=result['x'],result['z']
            rates=kappa*np.array([[a,x],[0,1.]])
            g=kappa*np.sqrt(x*z)/2
            r=two_mode(w,[tc,th],rates,g)
            # Assumed cold deposition fraction 0.1 only for this synthetic wall balance.
            absorption=(bmax*fraction*z*q0)/.1
            wall=r['conversion_work']+absorption
            result.update(C=float(z*x/(a+x)),
                          gross_cold_heat_W_per_pair=float(r['heat'][0]),
                          net_cold_heat_W_per_pair=float(result['net_Q_over_Q0']*q0),
                          conversion_work_W_per_pair=float(r['conversion_work']),
                          total_pump_absorption_W_per_pair=float(absorption),
                          wall_COP_before_other_losses=float(result['net_Q_over_Q0']*q0/wall),
                          g_over_omega1=float(g/w[0]),
                          cold_pump_heat_W_per_pair=float(.1*absorption))
            assert result['wall_COP_before_other_losses']<=tc/(th-tc)+1e-10
        remote_rows.append(result)

    output=dict(status='ANALYTIC_MODEL_AND_NUMERICAL_DIAGNOSTICS_ONLY',
        source_revision='e606bfc587c76bdcae8b8fa3ec33e721efa2fbac',
        source_data_used_for_synthetic_examples=False,
        checks=dict(cross_bath_random_cases=500,detuned_cases=500,
                    maximum_scaled_covariance_or_energy_residual=max(residuals),
                    min_resonant_entropy_production_W_per_K=min(entropy),
                    scalar_gate_cases=len(gate_checks),remote_overlap_cases=200,
                    max_remote_normalized_error=max(remote_res)),
        generalized_gate=gate_checks,
        synthetic=dict(Tc_K=tc,Th_K=th,f1_THz=20.,f2_THz=24.,
            linewidth_over_2pi_THz=.1,delta0=float(delta0),deltaa=float(deltaa),
            d=d,Q0_W_per_pair=float(q0),ideal_COP=5.,Carnot_COP=10.,
            symmetric_cross_contact=contact_rows,
            remote_hot_converter=dict(A_over_B=a,b_max=bmax,x_at_loss_tangency=float(boundary.x),
                                      assumed_cold_fraction_for_wall_COP=.1,cases=remote_rows,
                                      all_contact_threshold=all_contact)),
        receipts=dict(python=platform.python_version(),numpy=np.__version__,
                      wall_seconds=time.perf_counter()-started,
                      provider_model_id='UNKNOWN',token_usage='UNKNOWN',billing='UNKNOWN'))
    (OUT/'results.json').write_text(json.dumps(output,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'checks':output['checks'],'synthetic':output['synthetic'],
                      'receipts':output['receipts']},indent=2,allow_nan=False))


if __name__=='__main__':
    main()
