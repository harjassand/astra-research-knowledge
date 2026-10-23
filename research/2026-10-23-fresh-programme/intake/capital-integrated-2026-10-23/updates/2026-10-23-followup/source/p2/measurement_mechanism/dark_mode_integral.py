"""Exact passive-chain covariance and integrated dark-mode noise check.

MODEL CALCULATION ONLY. No measured coupling, loss, or noise spectrum.
Three resonantly converted modes [a,m,b], with equal real couplings g,
terminal linewidths kappa, intermediate linewidth gamma. White Markov
occupations are assumed over the whole resolved triplet. Noise-source
contributions are separated by linearity, not interpreted as a complete
refrigerator performance model.
"""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import quad
from scipy.linalg import solve_continuous_lyapunov


def model(kappa, gamma, g, source=1):
    rates = np.array([kappa, gamma, kappa], dtype=float)
    h = np.array([[0., g, 0.], [g, 0., g], [0., g, 0.]])
    drift = -np.diag(rates/2)-1j*h
    occupancy = np.zeros(3)
    occupancy[source] = 1.
    diffusion = np.diag(rates*occupancy)
    N = solve_continuous_lyapunov(drift, -diffusion)
    root = np.diag(np.sqrt(rates))

    def scattering(nu):
        return np.eye(3)-root@np.linalg.solve(-1j*nu*np.eye(3)-drift, root)

    def density(nu):
        return abs(scattering(nu)[0, source])**2

    # The chosen real, resonant chain has an even intensity spectrum.
    # Integrate around each resolved bright resonance and include the tail.
    bright = np.sqrt(2)*g
    width = max(kappa, gamma)
    edges = sorted(set([0., max(0., bright-3*width), bright,
                        bright+3*width, bright+30*width]))
    integ = 0.
    errors = 0.
    for left, right in zip(edges[:-1], edges[1:]):
        val, err = quad(density, left, right, epsabs=1e-12, epsrel=2e-11,
                        limit=300)
        integ += val
        errors += err
    val, err = quad(density, edges[-1], np.inf, epsabs=1e-12,
                    epsrel=2e-11, limit=300)
    integ = (integ+val)/np.pi
    errors = (errors+err)/np.pi
    center = scattering(0.)
    return dict(kappa=kappa, gamma=gamma, g=float(g), source=source,
                central_terminal_conversion=float(abs(center[2, 0])**2),
                central_intermediate_to_a_noise=float(abs(center[0, 1])**2),
                integrated_source_to_a=float(integ),
                quadrature_error_estimate=float(errors),
                covariance_outgoing_source_flux=float(kappa*N[0, 0].real),
                covariance_integral_disagreement=float(abs(integ-kappa*N[0, 0].real)),
                number_balance_residual=float(abs(np.sum(rates*(occupancy-N.diagonal().real)))),
                covariance_residual=float(np.max(abs(drift@N+N@drift.conj().T+diffusion))),
                minimum_covariance_eigenvalue=float(np.linalg.eigvalsh(N).min()),
                maximum_drift_real_eigenvalue=float(np.linalg.eigvals(drift).real.max()),
                reciprocity_disagreement=float(np.max(abs(center-center.T))))


def main():
    kappa = 1.
    gamma = .1
    rows = []
    for C in [.1, 1., 10., 100., 1000.]:
        g = np.sqrt(C*kappa*gamma/8)
        row = model(kappa, gamma, g)
        row.update(cooperativity=C,
                   formula_central_conversion=C*C/(1+C)**2,
                   formula_central_intermediate_noise=2*C/(1+C)**2,
                   formula_integrated_noise=kappa*gamma/(2*(kappa+gamma))*C/(1+C))
        rows.append(row)
    lossless_rows = []
    for g in [.1, 1., 10.]:
        row = model(1., 0., g, source=2)
        row.update(formula_integrated_reverse_hot_flux=2*g*g/(1+4*g*g))
        lossless_rows.append(row)
    result = dict(status='EXACT_LINEAR_MARKOV_MODEL_ONLY_NO_MEASUREMENT',
                  source_occupancy=1.,
                  intermediate_noise=rows,
                  lossless_intermediate_reverse_terminal_noise=lossless_rows,
                  limits={
                      'C_to_infinity_central_conversion': 1.,
                      'C_to_infinity_central_intermediate_noise': 0.,
                      'C_to_infinity_integrated_intermediate_noise': kappa*gamma/(2*(kappa+gamma)),
                      'gamma_to_zero_intermediate_noise_at_fixed_g': 0.,
                      'g_to_infinity_lossless_intermediate_reverse_noise': kappa/2})
    Path(__file__).with_name('dark_mode_results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
