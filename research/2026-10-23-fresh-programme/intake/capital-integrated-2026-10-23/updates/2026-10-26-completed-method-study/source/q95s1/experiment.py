#!/usr/local/bin/python3
"""Q95: bounded-probe discrimination of an elastic spring and a slow Maxwell mode.

All generated observations are simulations, not measurements of a material.
Run with /usr/local/bin/python3 experiment.py from this directory.
Only NumPy, SciPy and Matplotlib are required. No network calls.
"""
from pathlib import Path
import csv
import json
import math
import platform

import numpy as np
import scipy
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import ndtr, ndtri
from scipy.stats import ks_2samp

OUT = Path(__file__).resolve().parent
RNG = np.random.default_rng(951026)


def inner(a, b):
    return float(np.einsum('i,i->', a, b, optimize=False))


def mv(a, b):
    return np.einsum('ij,j->i', a, b, optimize=False)


def mm(a, b):
    return np.einsum('ik,kj->ij', a, b, optimize=False)


def factors(rate, dt):
    x = rate * dt
    a = math.exp(-x)
    r = -math.expm1(-x) / x
    if x < 1.e-3:
        c = x/2 - x*x/6 + x**3/24 - x**4/120 + x**5/720
    else:
        c = 1-r
    return a, r, c


def contrast_matrix(rate, dt, n, modulus=1.):
    """Bin-averaged stress contrast, elastic minus Maxwell, for each strain input."""
    a, r, c = factors(rate, dt)
    i, j = np.indices((n, n))
    k = np.zeros((n, n))
    prior = i > j
    k[prior] = r * (-math.expm1(-rate*dt)) * np.exp(-rate*dt*(i[prior]-j[prior]-1))
    np.fill_diagonal(k, c)
    return modulus*k


def step_contrast(rate, dt, n, modulus=1., amplitude=1.):
    a, r, c = factors(rate, dt)
    v = np.exp(-rate*dt*np.arange(n))
    return modulus*amplitude*(-np.expm1(-rate*dt*np.arange(n)) + c*v)


def lowpass_average(u, rate, dt):
    a, r, c = factors(rate, dt)
    v = 0.
    out = np.empty(len(u))
    for i, ui in enumerate(u):
        out[i] = c*ui+r*v
        v = a*v+(1-a)*ui
    return out


def continuous_energy(rate, duration):
    """Integral_0^T (1-exp(-rate*t))^2 dt; stable also at rate*T << 1."""
    x = rate*duration
    return duration*quad(lambda s: (-math.expm1(-x*s))**2, 0., 1.,
                         epsabs=1.e-25, epsrel=2.e-12)[0]


def duration_for_error(rate, alpha=.05, modulus=1., amplitude=1., noise=.02):
    target = (2*ndtri(1-alpha)*noise/(modulus*amplitude))**2
    hi = 1.
    while continuous_energy(rate, hi) < target:
        hi *= 2
    return brentq(lambda t: continuous_energy(rate, t)-target, 0., hi,
                  xtol=1.e-12, rtol=1.e-12)


def write_csv(name, rows):
    with (OUT/name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def mechanical_cost(u, rate, dt):
    """Exact jump work and hold dissipation; final unload/reset is not included."""
    a = math.exp(-rate*dt)
    z = old_u = net = gross = diss = 0.
    elastic_gross = 0.
    for ui in u:
        w = .5*((ui-z)**2-(old_u-z)**2)
        net += w
        gross += max(0., w)
        elastic_gross += max(0., .5*(ui*ui-old_u*old_u))
        diss += .5*(ui-z)**2*(1-a*a)
        z = a*z+(1-a)*ui
        old_u = ui
    return dict(Maxwell_net_work=net, Maxwell_gross_positive_work=gross,
                Maxwell_dissipation=diss, Maxwell_final_stored_energy=.5*(old_u-z)**2,
                elastic_gross_positive_work=elastic_gross,
                elastic_final_stored_energy=.5*old_u*old_u)


def simulate_feedback(rate=.2, duration=1., n=32, noise=.05, trials=30000, garbled=False):
    """The same causal policy is simulated directly and via the fixed-step experiment."""
    dt = duration/n
    a, r, c = factors(rate, dt)
    b = step_contrast(rate, dt, n)
    sd = noise/math.sqrt(dt)
    theta = np.where(np.arange(trials) < trials//2, 1., -1.)  # +1 elastic
    loglr = np.zeros(trials)
    state = np.zeros(trials)
    residual_sum = residual_sq = count = 0.
    max_ratio = 0.
    action_energy = np.zeros(trials)
    for i in range(n):
        # Parameter-free bounded feedback. It can reverse sign as evidence changes.
        u = np.tanh(1. + 3.*np.tanh(loglr))
        zbar = c*u+r*state
        mu0 = u
        mu1 = u-zbar
        mid = (mu0+mu1)/2
        delta = zbar
        ratio = delta/b[i]
        max_ratio = max(max_ratio, float(np.max(np.abs(ratio))))
        if garbled:
            x = theta*b[i]/2 + sd*RNG.standard_normal(trials)
            y = mid+ratio*x+sd*np.sqrt(np.maximum(0., 1-ratio*ratio))*RNG.standard_normal(trials)
        else:
            y = mid+theta*delta/2+sd*RNG.standard_normal(trials)
        residual = (y-mid-theta*delta/2)/sd
        residual_sum += float(residual.sum())
        residual_sq += inner(residual, residual)
        count += trials
        loglr += delta*(y-mid)/(sd*sd)
        state = a*state+(1-a)*u
        action_energy += u*u*dt
    errors = (np.where(loglr >= 0, 1., -1.) != theta)
    p = float(errors.mean())
    summary = dict(error=p, mc_95_halfwidth=1.96*math.sqrt(p*(1-p)/trials),
                   residual_mean=residual_sum/count, residual_second_moment=residual_sq/count,
                   maximum_envelope_ratio=max_ratio, mean_strain_squared_time=float(action_energy.mean()),
                   trials=trials, bins=n, rate=rate, noise_density=noise)
    return summary, loglr, theta


def main():
    n, duration, noise = 512, 1., .02
    dt = duration/n
    tm = (np.arange(n)+.5)*dt
    waveforms = {
        'step': np.ones(n),
        'linear_ramp': tm/duration,
        'sine_1_cycle': np.sin(2*np.pi*tm/duration),
        'chirp_1_to_20_cycles': np.sin(2*np.pi*(tm/duration+9.5*(tm/duration)**2)),
        'alternating_16_blocks': np.where((np.arange(n)*16//n)%2 == 0, 1., -1.),
    }
    rows = []
    checks = {}
    for rate in [1.e-5, 1.e-4, .001, .01, .1, 1., 10.]:
        k = contrast_matrix(rate, dt, n)
        b = step_contrast(rate, dt, n)
        assert np.min(k) >= 0
        np.testing.assert_allclose(mv(k, np.ones(n)), b, rtol=2.e-12, atol=2.e-15)
        for name, u in waveforms.items():
            d = mv(k, u)
            assert np.all(np.abs(d) <= b+1.e-13)
            d2 = inner(d, d)*dt/noise**2
            rows.append(dict(rate=rate, duration=duration, bins=n, noise_density=noise,
                             waveform=name, strain_squared_time=inner(u, u)*dt,
                             whitened_distance_squared=d2, KL=d2/2,
                             exact_equal_prior_error=float(ndtr(-math.sqrt(d2)/2)),
                             **mechanical_cost(u, rate, dt)))
        # Independent recurrence vs the explicit causal matrix.
        ucheck = RNG.uniform(-1., 1., n)
        np.testing.assert_allclose(mv(k, ucheck), lowpass_average(ucheck, rate, dt),
                                   rtol=1.e-10, atol=1.e-13)
    write_csv('waveform_comparison.csv', rows)

    # Exhaust every amplitude-saturating 16-bin waveform; 2^16 alternatives.
    enum_n, enum_rate = 16, .2
    k = contrast_matrix(enum_rate, 1/enum_n, enum_n)
    codes = np.arange(2**enum_n, dtype=np.uint32)
    inputs = 2*((codes[:, None] >> np.arange(enum_n)) & 1).astype(float)-1
    energies = np.sum(mm(inputs, k.T)**2, axis=1)/enum_n
    optimum = float(np.sum(mv(k, np.ones(enum_n))**2)/enum_n)
    np.testing.assert_allclose(energies.max(), optimum, rtol=1.e-13)
    checks['exhaustive_vertices'] = dict(count=len(codes), bins=enum_n, rate=enum_rate,
                                       maximum_contrast_energy=float(energies.max()),
                                       ordinary_step_contrast_energy=optimum,
                                       maximizers=int(np.sum(np.isclose(energies, optimum, atol=1.e-14, rtol=1.e-12))))

    # Exact passivity ledger for a spring of modulus A=1 in series with eta=1/rate.
    rate, z, old_u, work, diss = .2, 0., 0., 0., 0.
    a = math.exp(-rate*.01)
    for u in RNG.uniform(-1., 1., 1000):
        work += .5*((u-z)**2-(old_u-z)**2)
        energy_at_start = .5*(u-z)**2
        diss += energy_at_start*(1-a*a)
        z = a*z+(1-a)*u
        old_u = u
    final_energy = .5*(old_u-z)**2
    ledger_error = abs(work-diss-final_energy)
    assert ledger_error < 1.e-12 and diss >= 0
    checks['passivity_ledger'] = dict(work=work, dissipation=diss,
                                    final_energy=final_energy, balance_residual=ledger_error)

    # Exact least-favorable-spectrum test, plus nontrivial mixtures.
    least_rate = .1
    b = step_contrast(least_rate, dt, n)
    sd = noise/math.sqrt(dt)
    dmin = np.linalg.norm(b)/sd
    rates = np.geomspace(least_rate, 100., 64)
    spectrum_responses = np.stack([step_contrast(q, dt, n) for q in rates])
    weights = RNG.dirichlet(np.full(len(rates), .2), size=1000)
    deltas = mm(weights, spectrum_responses)
    standardized_projection = mv(deltas, b)/(sd*np.linalg.norm(b))
    type_two = ndtr(dmin/2-standardized_projection)
    bound = float(ndtr(-dmin/2))
    assert np.max(type_two) <= bound+1.e-13
    checks['composite_spectrum'] = dict(spectra=1000, rate_minimum=least_rate,
                                       rate_maximum=100., total_modulus=1.,
                                       minimax_error=bound, largest_random_mixture_type_II=float(type_two.max()),
                                       least_favorable_single_mode_error=bound)

    # Direct implementation of the parameter-independent causal Gaussian garbling.
    direct, direct_l, theta = simulate_feedback(garbled=False)
    garbled, garbled_l, theta2 = simulate_feedback(garbled=True)
    assert max(direct['maximum_envelope_ratio'], garbled['maximum_envelope_ratio']) <= 1+1.e-12
    oracle_b = step_contrast(.2, 1/32, 32)
    direct['step_oracle_error'] = float(ndtr(-math.sqrt(inner(oracle_b, oracle_b)/(32*.05**2))/2))
    checks['feedback_direct'] = direct
    checks['feedback_garbled_from_step'] = garbled
    checks['garbling_distribution_diagnostic'] = {
        'elastic_KS_statistic': float(ks_2samp(direct_l[theta == 1], garbled_l[theta2 == 1]).statistic),
        'Maxwell_KS_statistic': float(ks_2samp(direct_l[theta == -1], garbled_l[theta2 == -1]).statistic),
        'note': 'Finite Monte Carlo diagnostic; the exact conditional-law equality is proved in PROOF.md.'}

    duration_rows = []
    for rate in np.geomspace(1.e-6, 10., 29):
        exact = duration_for_error(rate, noise=noise)
        zcrit = ndtri(.95)
        approximation = (12*noise**2*zcrit**2/rate**2)**(1/3)
        duration_rows.append(dict(rate=float(rate), relaxation_time=float(1/rate), alpha=.05,
                                  noise_density=noise, exact_minimum_duration=exact,
                                  slow_mode_asymptotic_duration=float(approximation),
                                  rate_times_exact_duration=float(rate*exact)))
    write_csv('detection_duration.csv', duration_rows)

    # Boundary: passivity does not imply a one-sign impulse-response contrast.
    rc_dt, rc_T = .01, 60.
    rc_t = (np.arange(round(rc_T/rc_dt))+.5)*rc_dt
    rc_step = np.ones(len(rc_t))
    rc_sine = np.sin(math.sqrt(2)*rc_t)
    def rc_contrast(u):
        return lowpass_average(u, 1., rc_dt)-lowpass_average(u, 2., rc_dt)
    rc_dstep, rc_dsine = rc_contrast(rc_step), rc_contrast(rc_sine)
    step_e, sine_e = inner(rc_dstep, rc_dstep)*rc_dt, inner(rc_dsine, rc_dsine)*rc_dt
    assert sine_e > 10*step_e
    checks['sign_condition_counterexample'] = dict(
        systems='H0(s)=1/(s+1), H1(s)=2/(s+2); both ordinary passive RC voltage dividers',
        contrast_impulse='exp(-t)-2 exp(-2t), changes sign at log(2)',
        duration=rc_T, dt=rc_dt, step_energy=step_e, sine_energy=sine_e,
        sine_to_step_energy_ratio=sine_e/step_e, infinite_horizon_step_energy=1/12,
        steady_sine_contrast_amplitude=1/3)

    rate, epsilon = .001, .001
    checks['hidden_mode'] = dict(rate=rate, relaxation_time=1/rate,
        horizon=1., normalized_instantaneous_modulus=1., normalized_strain_bound=1.,
        maximum_stress_contrast_by_horizon=-math.expm1(-rate),
        continuous_white_noise_best_error=float(ndtr(-math.sqrt(continuous_energy(rate, 1.))/noise/2)),
        bounded_error_epsilon=epsilon,
        common_transcript_possible=bool(-math.expm1(-rate) <= 2*epsilon),
        minimum_duration_to_break_bounded_error_overlap=-math.log1p(-2*epsilon)/rate,
        minimum_duration_for_five_percent_white_noise_error=duration_for_error(rate, noise=noise),
        equilibrium_modulus_elastic=1., equilibrium_modulus_Maxwell=0.)

    metadata = dict(seed=951026, python=platform.python_version(), numpy=np.__version__,
                    scipy=scipy.__version__, observations='all synthetic',
                    noise_model='independent Gaussian bin averages with standard deviation sigma/sqrt(dt)',
                    resources='one specimen, reset initial state, same T, |strain|<=1, same readout bins and noise density')
    (OUT/'results.json').write_text(json.dumps(dict(metadata=metadata, checks=checks), indent=2)+'\n')
    lines = [json.dumps(metadata, indent=2), json.dumps(checks, indent=2)]
    (OUT/'RUN_OUTPUT.txt').write_text('\n\n'.join(lines)+'\n')

    # Standalone scientific figure: all curves are dimensionless theoretical/simulated models.
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False})
    fig, axs = plt.subplots(2, 2, figsize=(11, 7.4), constrained_layout=True)
    t_short = np.linspace(0, 1, 301)
    axs[0, 0].plot(t_short, np.ones_like(t_short), label='Permanent spring')
    axs[0, 0].plot(t_short, np.exp(-.001*t_short), '--', label='Maxwell, relaxation time 1000')
    axs[0, 0].set(xlabel='Time', ylabel='Stress / (A U)', title='Same short-time appearance')
    axs[0, 0].legend(fontsize=8)
    tl = np.geomspace(.001, 1.e5, 1000)
    axs[0, 1].semilogx(tl, np.ones_like(tl))
    axs[0, 1].semilogx(tl, np.exp(-.001*tl), '--')
    axs[0, 1].axvspan(.001, 1, color='0.8', alpha=.5, label='Observation horizon')
    axs[0, 1].set(xlabel='Time', ylabel='Stress / (A U)', title='Different equilibrium behavior')
    axs[0, 1].legend(fontsize=8)
    selected = [r for r in rows if r['rate'] == .1]
    labels = [r['waveform'].replace('_', ' ') for r in selected]
    axs[1, 0].barh(labels, [r['whitened_distance_squared'] for r in selected])
    axs[1, 0].set(xlabel='Squared whitened contrast (larger is better)', title='Matched amplitude, horizon and detector')
    axs[1, 1].loglog([r['relaxation_time'] for r in duration_rows],
                     [r['exact_minimum_duration'] for r in duration_rows], label='Exact optimum')
    axs[1, 1].loglog([r['relaxation_time'] for r in duration_rows],
                     [r['slow_mode_asymptotic_duration'] for r in duration_rows], '--', label='Slow-mode asymptotic')
    axs[1, 1].set(xlabel='Relaxation time', ylabel='Required observation duration', title='5% error, white noise density 0.02')
    axs[1, 1].legend(fontsize=8)
    fig.suptitle('Q95: a limit on detecting hidden relaxation — models and simulations only', fontsize=13)
    fig.savefig(OUT/'research_figure.png', dpi=180)
    fig.savefig(OUT/'research_figure.pdf')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
