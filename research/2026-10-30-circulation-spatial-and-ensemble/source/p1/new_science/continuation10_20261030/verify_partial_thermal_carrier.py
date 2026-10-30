#!/usr/bin/env python3
"""Check the untuned actual interacting cell and its stable zero-response failure."""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp


def coefficients(theta, r, g, b):
    c, s = np.cos(theta), np.sin(theta)
    M = np.array([[c, -s], [r*s, r*c]])
    d = np.array([s/g+b, r*(1-c)/g])
    ell = np.array([s/g+b*c, -(1-c)/g-b*s])
    d0 = (1-c)/g**2+b*s/g+b*b/2
    noise = np.array([0., np.sqrt(1-r*r)])
    k = np.linalg.solve((np.eye(2)-M).T, ell)
    mu = d0+k@d
    formula = (2/g+b*s/(1-c))**2*(1-r)/(2*(1+r))
    return M, d, ell, d0, noise, k, mu, formula


def check(theta, r, g, b, strength, seed):
    rng = np.random.default_rng(seed)
    R, N, h = 5, 13., theta/g
    M, d, ell, d0, noise, k, mu, formula = coefficients(theta, r, g, b)
    coupling = rng.uniform(.1, 2., (R, R))
    coupling = (coupling+coupling.T)/2
    np.fill_diagonal(coupling, 0.)
    X = rng.uniform(0, N, R)
    V, Y = rng.normal(size=R), rng.normal(size=R)
    current = delayed = work = corrected_work = correction = 0.
    errors = np.zeros(3)
    for j in range(18):
        F = 0. if j < 2 else -.13*np.sign(delayed)
        old_current, X0 = current, X.copy()
        z0 = np.array([V.sum(), Y.sum()])

        def grad(x):
            phase = 2*np.pi*(x[:, None]-x[None, :])/N
            return strength*2*np.pi/N*(coupling*np.sin(phase)).sum(axis=1)

        def transport(_t, state):
            x, v, y = np.split(state, 3)
            return np.concatenate((v, -grad(x)-g*y+F, g*v))

        sol = solve_ivp(transport, (0, h), np.concatenate((X, V, Y)), rtol=2e-11, atol=1e-12)
        assert sol.success
        X, V, Y = np.split(sol.y[:, -1], 3)
        incoming = rng.normal(size=R)

        def bath(_t, state):
            x, v = np.split(state, 2)
            return np.concatenate((v, -grad(x)+F))

        sol = solve_ivp(bath, (0, b), np.concatenate((X, V)), rtol=2e-11, atol=1e-12)
        assert sol.success
        X, V = np.split(sol.y[:, -1], 2)
        # Exact finite-frequency partial rotation; all particle bath motion counted.
        Y = r*Y+np.sqrt(1-r*r)*incoming
        z1, dA = np.array([V.sum(), Y.sum()]), (X-X0).sum()
        predicted = R*mu*F+(k@noise)*incoming.sum()
        errors = np.maximum(errors, [np.max(abs(z1-M@z0-R*d*F-noise*incoming.sum())),
                                     abs(dA-ell@z0-R*d0*F),
                                     abs(dA+k@(z1-z0)-predicted)])
        work += F*dA
        corrected_work += F*predicted
        correction += F*(k@(z1-z0))
        current += dA
        delayed = old_current
    fdt = abs((k@noise)**2-2*mu)
    covariance = np.linalg.norm(M@M.T+np.outer(noise, noise)-np.eye(2))
    work_error = abs(work-corrected_work+correction)
    assert max(*errors, work_error) < 3e-8
    assert max(fdt, covariance, abs(mu-formula)) < 2e-12 and mu > 0
    return dict(theta=theta, refresh_cosine=r, g=g, bath_duration=b,
                unknown_relative_interaction_strength=strength,
                spectral_radius=float(max(abs(np.linalg.eigvals(M)))),
                mobility_per_cycle=float(mu), closed_formula=float(formula),
                FDT_identity_error=float(fdt), invariant_covariance_error=float(covariance),
                max_actual_state_error=float(errors[0]), max_true_current_error=float(errors[1]),
                max_corrected_current_error=float(errors[2]), actual_work_identity_error=float(work_error),
                nonzero_corrector_work_that_must_be_retained=float(correction))


def main():
    cases = [check(.4, .8, 1.2, .3, .1, 910101),
             check(1.5, -.7, .9, .4, 2., 910102),
             check(2.7, .2, 1.1, .7, 17., 910103)]
    M, d, ell, d0, noise, k, mu, formula = coefficients(3*np.pi/2, 0., 1., 2.)
    failure = dict(theta=3*np.pi/2, r=0., g=1., bath_duration=2.,
                   spectral_radius=float(max(abs(np.linalg.eigvals(M)))),
                   mobility=float(mu), formula=float(formula), corrector=k.tolist(),
                   noise_coefficient=float(k@noise),
                   true_current_equals_momentum_change_error=float(max(np.max(abs(ell-(M[0]-[1, 0]))), abs(d0-d[0]))))
    assert abs(mu) < 1e-12 and failure['true_current_equals_momentum_change_error'] < 1e-12
    result = dict(schema='astra_p1.untuned_carrier_checks.v1', actual_interacting_cases=cases,
                  preserved_stable_zero_response_failure=failure,
                  scope='Population ODE/algebra verification; no acquired calibration or apparatus error budget.')
    output = Path(__file__).with_name('UNTUNED_CARRIER_CHECK_RESULTS.json')
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
