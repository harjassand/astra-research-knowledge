"""Independent Fock-space check of the warm-output correction multiplier.

Runs only NumPy/SciPy. The numeric side computes the operator product directly;
it does not feed the analytic conditional variance into a second implementation.
The vacuum/thermal detector-loss quadrature is integrated analytically as an
independent characteristic function. Increasing Fock cutoff checks truncation.
"""
import json
import numpy as np
from scipy.linalg import expm


def thermal(cutoff, occupation):
    if occupation == 0:
        p = np.zeros(cutoff)
        p[0] = 1
    else:
        ratio = occupation / (occupation + 1)
        p = (1 - ratio) * ratio ** np.arange(cutoff)
        p /= p.sum()
    return p


def numeric(cutoff, occupation, eta, angle, gain, a, s, sprime, added_variance):
    ladder = np.diag(np.sqrt(np.arange(1, cutoff)), 1)
    x = (ladder + ladder.T) / np.sqrt(2)
    p = (ladder - ladder.T) / (1j * np.sqrt(2))
    d = s - sprime
    u = expm(-1j * a * s * p)
    up = expm(-1j * a * sprime * p)
    y = np.sqrt(eta) * (p * np.cos(angle) + x * np.sin(angle))
    product = up.conj().T @ expm(1j * gain * d * y) @ u
    value = np.dot(np.diag(product), thermal(cutoff, occupation))
    return value * np.exp(-0.5 * gain**2 * d**2 * (1 - eta) * added_variance)


def analytic(occupation, eta, angle, gain, a, s, sprime, added_variance):
    v = occupation + 0.5
    d = s - sprime
    residual = (a*a*v - 2*a*gain*np.sqrt(eta)*v*np.cos(angle)
                + gain*gain*(eta*v + (1-eta)*added_variance))
    phase = a*gain*np.sqrt(eta)*np.sin(angle)*(s*s-sprime*sprime)/2
    return np.exp(1j*phase - d*d*residual/2)


def run():
    cases = []
    # s+s' nonzero is essential to check the often missed deterministic S^2 phase.
    a, s, sprime, w = 0.37, 2.0, -0.5, 0.5
    for n, eta, angle, gain_error in [
        (0.0, 1.0, 0.0, 0.0),
        (1.0, 0.7, 0.0, 0.0),
        (1.0, 0.7, 0.2, 0.0),
        (5.0, 0.2, 0.2, 0.03),
        (5.0, 1.0, -0.15, 0.0),
    ]:
        v = n + 0.5
        gain = a*np.sqrt(eta)*v*np.cos(angle)/(eta*v+(1-eta)*w)+gain_error
        target = analytic(n, eta, angle, gain, a, s, sprime, w)
        errors = {}
        for cutoff in (64, 112):
            value = numeric(cutoff, n, eta, angle, gain, a, s, sprime, w)
            errors[str(cutoff)] = float(abs(value-target))
        cases.append(dict(n=n, eta=eta, angle=angle, gain_error=gain_error,
                          analytic_real=float(target.real),
                          analytic_imag=float(target.imag), errors=errors))
    worst = max(c['errors']['112'] for c in cases)
    assert worst < 1e-7, worst
    print(json.dumps(dict(worst_error_at_cutoff_112=worst, cases=cases), indent=2))


if __name__ == '__main__':
    run()
