"""Finite passive/active conductance-response comparison, without path resets.

Each trial is one contiguous trajectory. Independent Monte Carlo repetitions
only verify the finite-data estimator. They are not acquisition resets supplied
to a single estimator. Units are dimensionless; no material/device is claimed.
"""
from pathlib import Path
import json
import numpy as np
from scipy.fft import dst
from scipy.optimize import minimize_scalar


def spectrum(n, h, theta, K, read_var):
    lam = 2 - 2 * np.cos(np.pi * np.arange(1, n + 1) / (n + 1))
    return 2 * theta * K * h + read_var * lam, lam


def drift_basis(n, h, order=1):
    t = (np.arange(n) + .5) * h
    t -= np.mean(t)
    return np.column_stack([t**j for j in range(order + 1)]) * h


def information(n, h, theta, K, read_var, c, kappa=1., drift_order=1):
    s, lam = spectrum(n, h, theta, K, read_var)
    a = 2 * theta * h
    cov_known = .5 * np.sum((a / s)**2)
    rr = .5 * np.sum((lam / s)**2)
    kr = .5 * np.sum(a * lam / s**2)
    cov_unknown = cov_known - kr**2 / rr
    B = dst(drift_basis(n, h, drift_order), type=1, norm='ortho', axis=0)
    v = dst(kappa * h * c, type=1, norm='ortho')
    gram = B.T @ (B / s[:, None])
    cross = B.T @ (v / s)
    mean = float(np.sum(v*v/s) - cross @ np.linalg.solve(gram, cross))
    mean = max(mean, 0.)
    duration = n * h
    integral_c = float(np.sum(c) * h)
    integral_c2 = float(np.sum(c*c) * h)
    # The work and mean-FI identity below applies with constant unknown drift,
    # noiseless complete records and b=0 for the added mechanical work.
    work = kappa*kappa * K * integral_c2
    ideal_mean_info_relative = kappa*kappa * K / (2*theta) * (
        integral_c2 - integral_c**2/duration) if theta > 0 else None
    return dict(covariance_FI_readnoise_known=float(cov_known),
                covariance_FI_readnoise_unknown=float(max(cov_unknown, 0.)),
                active_mean_FI=mean,
                relative_CRLB_passive=float(1/(K*np.sqrt(cov_known))) if cov_known > 0 else None,
                relative_CRLB_combined=float(1/(K*np.sqrt(cov_known+mean))) if cov_known+mean > 0 else None,
                mean_control_displacement=kappa*K*integral_c,
                induced_viscous_work=work,
                ideal_active_mean_FI_relative=ideal_mean_info_relative,
                thermal_endpoint_rms=float(np.sqrt(2*theta*K*duration)),
                samples=n+1, duration=duration,
                scope='Finite Gaussian experiment. CRLB concerns regular locally unbiased estimators, not a finite confidence guarantee. Work excludes electrode Joule loss and detector cost.')


def abba(n, maximum):
    assert n % 4 == 0
    return np.r_[np.zeros(n//4), np.full(n//2, maximum), np.zeros(n//4)]


def fit_K(d, c, h, theta, read_var, kappa=1., drift_order=1, restricted=False):
    n = len(d)
    data = dst(d, type=1, norm='ortho')
    cv = dst(kappa * h * c, type=1, norm='ortho')
    B = dst(drift_basis(n, h, drift_order), type=1, norm='ortho', axis=0)
    lam = 2 - 2 * np.cos(np.pi*np.arange(1, n+1)/(n+1))

    def profile(logK):
        K = np.exp(logK)
        s = 2*theta*K*h + read_var*lam
        r = data - K*cv
        gram = B.T @ (B/s[:, None])
        beta = np.linalg.solve(gram, B.T @ (r/s))
        r -= B @ beta
        correction = np.linalg.slogdet(gram)[1] if restricted else 0.
        return .5*(np.sum(np.log(s)) + np.sum(r*r/s) + correction)

    res = minimize_scalar(profile, bounds=(np.log(1e-4), np.log(20.)),
                          method='bounded', options={'xatol': 1e-7})
    if not res.success:
        raise RuntimeError(res)
    return float(np.exp(res.x))


def verify_finite_estimators(seed=219503, replicates=600):
    rng = np.random.default_rng(seed)
    n, h, theta, K, read_var = 256, .02, .002, 1., .01
    kappa, b = 1., .03
    out = {}
    for name, c in [('passive', np.zeros(n)), ('positive_abba', abba(n, .5))]:
        vals, restricted_vals, ranges = [], [], []
        for _ in range(replicates):
            # A single unreset latent trajectory, including all traversed states.
            dx = (b + kappa*K*c)*h + np.sqrt(2*theta*K*h)*rng.normal(size=n)
            x = np.r_[0., np.cumsum(dx)]
            y = x + np.sqrt(read_var)*rng.normal(size=n+1)
            vals.append(fit_K(np.diff(y), c, h, theta, read_var))
            restricted_vals.append(fit_K(np.diff(y), c, h, theta, read_var, restricted=True))
            ranges.append(float(np.ptp(x)))
        a = np.asarray(vals)
        ar = np.asarray(restricted_vals)
        out[name] = dict(estimate_mean=float(a.mean()),
                         estimate_sd=float(a.std(ddof=1)),
                         estimate_rmse=float(np.sqrt(np.mean((a-K)**2))),
                         lower_boundary_fraction=float(np.mean(a < 1.001e-4)),
                         restricted_likelihood_mean=float(ar.mean()),
                         restricted_likelihood_sd=float(ar.std(ddof=1)),
                         restricted_likelihood_rmse=float(np.sqrt(np.mean((ar-K)**2))),
                         latent_range_median=float(np.median(ranges)),
                         latent_range_95pct=float(np.quantile(ranges, .95)),
                         information=information(n,h,theta,K,read_var,c))
    out['conditions'] = dict(n=n,h=h,theta=theta,K=K,read_var=read_var,
                             autonomous_drift=b,unknown_drift_polynomial_order=1,
                             replicates=replicates,seed=seed,
                             no_reset='Every fitted dataset is one contiguous latent trajectory. Replications test estimator distribution only.')
    return out


def detector_resource_limit():
    # Point-read model with read variance S/h. This earns a fixed noise spectral
    # resource instead of assuming infinitely many equally precise free reads.
    theta, K, S, T = .01, 1., .003, 10.
    rows = []
    for n in [40, 160, 640, 2560, 10240]:
        h = T/n
        s, _ = spectrum(n,h,theta,K,S/h)
        fi = .5*np.sum((2*theta*h/s)**2)
        rows.append(dict(n=n, h=h, read_variance=S/h, relative_FI=K*K*float(fi)))
    j=np.arange(1,200000)
    limiting = 2*theta*theta*np.sum(1/(2*theta*K+S*(np.pi*j/T)**2)**2)
    return dict(parameters=dict(theta=theta,K=K,noise_spectral_resource=S,T=T),
                finite_rows=rows, limiting_FI=float(limiting),
                caveat='Point read model; finite exposure/motion blur require their observation kernel. The finite-resource saturation, not this kernel, is the conclusion.')


def four_read_abba(seed=4908):
    # Four noisy reads are needed: 0, T/4, 3T/4, T. A midpoint is generated
    # below for simple bookkeeping but its coefficient in the estimator is zero.
    rng=np.random.default_rng(seed)
    T,theta,K,cmax,kappa,R=5.12,.002,1.,.5,1.,.01
    reps=100000
    times=(np.arange(4)+.5)*T/4
    c=np.array([0.,cmax,cmax,0.])
    b0,b1=.03,.012
    dx=(b0+b1*times+kappa*K*c)*T/4+np.sqrt(2*theta*K*T/4)*rng.normal(size=(reps,4))
    x=np.column_stack([np.zeros(reps),np.cumsum(dx,axis=1)])
    y=x+np.sqrt(R)*rng.normal(size=x.shape)
    estimates=2*(y[:,0]-2*y[:,1]+2*y[:,3]-y[:,4])/(kappa*cmax*T)
    var=8*theta*K/(kappa*kappa*cmax*cmax*T)+40*R/(kappa*kappa*cmax*cmax*T*T)
    return dict(mean=float(np.mean(estimates)),sd=float(np.std(estimates,ddof=1)),
                exact_sd=float(np.sqrt(var)),reads_used=4,
                control_schedule='0 on [0,T/4), cmax on [T/4,3T/4), 0 on [3T/4,T]',
                drift='Unknown affine drift b0+b1*t canceled exactly; simulation b0=.03,b1=.012.',
                curvature_bias_bound='If |b_second_derivative|<=B2, |bias|<=B2*T^2/(16*kappa*cmax).',
                mean_control_displacement=kappa*K*cmax*T/2,
                induced_viscous_work=kappa*kappa*K*cmax*cmax*T/2,
                scope='Finite unbiased estimator in exact affine response model, four noisy reads, no reset. Electrode power and reading backaction remain separate physical costs.')


def passive_oracle():
    # Give the passive comparator exact initial state and autonomous drift,
    # calibrated R, and every raw observation, not only the increment invariant.
    n,h,theta,K,R=256,.02,.002,1.,.01
    lam=2-2*np.cos((2*np.arange(1,n+1)-1)*np.pi/(2*n+1))
    a=2*theta*h
    information=.5*np.sum((a/(a*K+R*lam))**2)
    return dict(FI=float(information),relative_CRLB=float(1/(K*np.sqrt(information))),
                scope='More favorable passive oracle: initial state, autonomous drift and R exactly known; all uniformly sampled raw positions available. Regular locally unbiased bound for this finite observation schedule, not all possible biased estimators or all possible observer designs.')


def cone_counterexample():
    # Physical two-electrode conductance G(q)=q [[1,-1],[-1,1]], q>0.
    # dG/dq=L; every admissible C gives force kappa tr(LC)>=0.
    L = np.array([[1., -1.],[-1.,1.]])
    rng=np.random.default_rng(4005)
    forces=[]
    for _ in range(1000):
        v=rng.normal(size=(2,2));C=v@v.T
        forces.append(float(np.trace(L@C)))
    return dict(G_derivative=L.tolist(),sampled_min_force=float(min(forces)),
                proof='tr(L C)=E[(V1-V2)^2]>=0 for every voltage covariance C PSD. Thus controlled mean q velocity cannot be negative in the zero-autonomous-drift affine model. The boundary kernel is exactly known and nonzero; covariance knowledge does not resolve the cone obstruction.',
                scope='Mean/local controllability. Thermal excursions can visit lower q; no deterministic reverse actuator or free stabilizing/reset operation is supplied.')


def main():
    n,h,K,cmax=256,.02,1.,.5
    grid=[]
    for theta in [1., .01, .0001]:
        for noise in [0., .01, 1.]:
            grid.append(dict(theta=theta,read_var=noise,
                result=information(n,h,theta,K,noise,abba(n,cmax))))
    comparison=verify_finite_estimators()
    assert comparison['positive_abba']['estimate_rmse'] < comparison['passive']['estimate_rmse']*.5
    assert comparison['positive_abba']['information']['mean_control_displacement'] > 0
    # With constant positive control and unknown constant drift, no mean-response
    # information remains, although force/work/displacement are expended.
    constant=information(n,h,.002,K,.01,np.full(n,.25),drift_order=0)
    assert constant['active_mean_FI'] < 1e-8
    out=dict(model='dg=(b(t)+kappa K c(t))dt+sqrt(2 theta K)dW, y_i=g_i+independent N(0,read_var), c>=0',
             grid=grid,finite_estimators=comparison,constant_bias=constant,
             four_read_active=four_read_abba(),
             passive_oracle=passive_oracle(),
             detector_budget=detector_resource_limit(),
             PSD_cone=cone_counterexample())
    path=Path(__file__).with_name('finite_response_results.json')
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'finite_estimators':comparison,'constant_bias':constant,
                      'detector_budget':out['detector_budget'],'PSD_cone':out['PSD_cone']},indent=2))


if __name__ == '__main__':
    main()
