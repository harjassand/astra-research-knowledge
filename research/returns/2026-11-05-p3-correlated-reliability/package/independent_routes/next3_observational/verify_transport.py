"""Reproduce the passive finite-observation Green--Kubo counterexample.

No simulation is used as evidence for the theorem. The program checks independent
matrix identities, Gaussian finite-sample KL, and the conditional tail bound.
Run: python next3_observational/verify_transport.py
"""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm, toeplitz, cho_factor, cho_solve
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent


def model(rho, lam):
    u = rho*rho
    sigma = np.array([[1., rho], [rho, 1.]])
    Q = np.diag([1., lam])
    A = Q @ np.linalg.inv(sigma)
    discr = np.sqrt((1.-lam)**2 + 4.*lam*u)
    fast = (1.+lam+discr)/(2.*(1.-u))
    slow = lam/((1.-u)*fast)  # stable form; no cancellation
    wslow = (fast-1.)/(fast-slow)
    wfast = 1.-wslow
    return sigma, Q, A, np.array([fast, slow]), np.array([wfast, wslow])


def corr(t, rates, weights):
    return np.exp(-np.multiply.outer(np.asarray(t), rates)) @ weights


def cumulative(t, rates, weights):
    return (-np.expm1(-np.multiply.outer(np.asarray(t), rates))) @ (weights/rates)


def full_path_kl(rho, lam, duration, replicas=1):
    u = rho*rho
    return -.5*replicas*np.log1p(-u) + duration*(1.+lam)*u/(4.*(1.-u))


def discrete_scalar_kl(times, rates, weights, noise_sd=0.):
    """KL of the scalar stationary Gaussian vector relative to unit OU.

    Equally spaced sampling is checked. Independent measurement noise is added
    to both models. This is an exact finite Gaussian calculation, not an
    asymptotic periodogram approximation.
    """
    assert np.allclose(np.diff(times), np.diff(times)[0])
    C1 = toeplitz(corr(times-times[0], rates, weights))
    C0 = toeplitz(np.exp(-(times-times[0])))
    C1 += noise_sd**2*np.eye(len(times))
    C0 += noise_sd**2*np.eye(len(times))
    L0 = cho_factor(C0, lower=True)
    L1 = cho_factor(C1, lower=True)
    tr = np.trace(cho_solve(L0, C1))
    logdet0 = 2.*np.log(np.diag(L0[0])).sum()
    logdet1 = 2.*np.log(np.diag(L1[0])).sum()
    return .5*(tr-len(times)+logdet0-logdet1)


def main():
    rho = .01
    target_K = 1000.
    lam = rho*rho/(target_K-1.)
    T = 100.
    sigma, Q, A, rates, weights = model(rho, lam)
    eye = np.eye(2)
    K_matrix = np.linalg.solve(A, sigma)[0, 0]
    K_spectral = np.sum(weights/rates)
    K_formula = 1.+rho*rho/lam
    assert np.allclose(A@sigma, Q, rtol=1e-12, atol=1e-14)
    assert np.allclose(A@sigma+sigma@A.T, 2.*Q, rtol=1e-12, atol=1e-14)
    assert np.all(rates > 0.) and np.all(weights > 0.)
    assert np.allclose(weights.sum(), 1.)
    assert np.allclose(weights@rates, 1.)
    assert np.isclose(K_matrix, K_formula, rtol=1e-12)
    assert np.isclose(K_spectral, K_formula, rtol=2e-11)
    dense_t = np.linspace(0., T, 2001)
    c1 = corr(dense_t, rates, weights)
    c0 = np.exp(-dense_t)
    for t in [0., .1, 1., 10., 100.]:
        assert np.isclose(corr(t, rates, weights).item(), (expm(-A*t)@sigma)[0,0], rtol=1e-11)
    # A separate direct formula for the Girsanov drift expectation.
    Sinv = np.linalg.inv(sigma)
    expectation = np.trace((Sinv-eye)@Q@(Sinv-eye)@sigma)
    expectation_formula = (1.+lam)*rho*rho/(1.-rho*rho)
    assert np.isclose(expectation, expectation_formula, rtol=1e-10)
    kl = full_path_kl(rho, lam, T)
    tv_upper = min(1., np.sqrt(kl/2.))
    sampled_kl = discrete_scalar_kl(np.arange(101.), rates, weights)
    noisy_sampled_kl = discrete_scalar_kl(np.arange(101.), rates, weights, noise_sd=.1)
    assert 0. <= noisy_sampled_kl <= sampled_kl <= kl
    R = cumulative(T, rates, weights).item()
    cT = corr(T, rates, weights).item()
    derivative_negative = np.sum(weights*rates*np.exp(-rates*T))
    tail_lower = cT*cT/derivative_negative
    tail_upper = cT/min(rates)
    true_tail = K_formula-R
    assert tail_lower <= true_tail*(1.+1e-9)
    assert true_tail <= tail_upper*(1.+1e-9)
    # A finite-time integral cannot silently omit the unresolved tail.
    assert R < 1.1 and true_tail > 998.
    out = {
        'rho':rho, 'lambda':lam, 'observation_duration':T,
        'reference_transport':1., 'alternative_transport':K_formula,
        'stationary_current_variance':float(sigma[0,0]),
        'current_quadratic_variation_rate':float(2.*Q[0,0]),
        'rates_fast_slow':rates.tolist(), 'weights_fast_slow':weights.tolist(),
        'slow_relaxation_time':float(1./min(rates)),
        'full_two_coordinate_path_KL':float(kl),
        'scalar_continuous_path_TV_upper':float(tv_upper),
        'worst_case_testing_error_lower':float((1.-tv_upper)/2.),
        'scalar_101_sample_KL':float(sampled_kl),
        'scalar_101_sample_with_noise_sd_0_1_KL':float(noisy_sampled_kl),
        'max_covariance_difference_on_observed_interval':float(np.max(c1-c0)),
        'observed_integral_R_T':float(R),
        'true_unobserved_tail':float(true_tail),
        'conditional_tail_lower_if_exact_derivative_known':float(tail_lower),
        'conditional_tail_upper_if_true_gap_known':float(tail_upper),
        'verification':'All matrix, spectral, Gaussian-KL, and tail-bound checks passed.'
    }
    (OUT/'verification_results.json').write_text(json.dumps(out, indent=2)+'\n')
    # Export exact, standalone research figure: full-scale correlation hides
    # the weak tail, while cumulative transport shows its eventual consequence.
    fig, ax = plt.subplots(1,3,figsize=(14,4.2),constrained_layout=True)
    ax[0].plot(dense_t,c0,label='Reference: K=1',lw=2)
    ax[0].plot(dense_t,c1,label='Alternative: K=1000',lw=1.5,ls='--')
    ax[0].set(xlabel='Time (fast relaxation units)',ylabel='Equilibrium current correlation',xlim=(0,12),title='Observed correlations nearly coincide')
    ax[0].legend(fontsize=8)
    ax[1].plot(dense_t,c1-c0,color='#b64620')
    ax[1].set(xlabel='Time',ylabel='Alternative minus reference',title='Small unresolved correlation tail')
    all_t = np.geomspace(.01,1e9,1200)
    ax[2].semilogx(all_t,-np.expm1(-all_t),label='Reference',lw=2)
    ax[2].semilogx(all_t,cumulative(all_t,rates,weights),label='Alternative',lw=2)
    ax[2].axvspan(.01,T,alpha=.1,color='black',label='Observation window')
    ax[2].set(xlabel='Integration horizon',ylabel='Cumulative Green–Kubo integral',title='Macroscopic transport differs 1000-fold')
    ax[2].legend(fontsize=8)
    fig.suptitle('Exact passive equilibrium counterexample; no fitted or simulated data',fontsize=12)
    fig.savefig(OUT/'transport_counterexample.png',dpi=180)
    fig.savefig(OUT/'transport_counterexample.pdf')
    print(json.dumps(out,indent=2))

if __name__ == '__main__':
    main()
