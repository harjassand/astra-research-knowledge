"""Dimensionless local Fisher audit for a two-state loss-echo assay.

Every setting is a Bernoulli survival measurement. Parameter coordinates are
log(a), log(r), log(d1), log(d2), and all data are model-generated.
"""

import numpy as np


def expm2(M, t):
    values, vectors = np.linalg.eig(M)
    return np.real_if_close(vectors @ np.diag(np.exp(values * t))
                            @ np.linalg.inv(vectors)).real


def survival(logpars, pulse):
    a, r, d1, d2 = np.exp(logpars)
    A = np.array([[-a, r], [a, -r]])
    M = A - np.diag([d1, d2])
    x = np.array([1.0, 0.0])
    for is_on, duration in pulse:
        x = expm2(M if is_on else A, duration) @ x
    return float(x.sum())


def fisher(logpars, settings):
    h = 1e-5
    J = np.empty((len(settings), len(logpars)))
    y = np.empty(len(settings))
    for row, setting in enumerate(settings):
        y[row] = survival(logpars, setting)
        for col in range(len(logpars)):
            step = np.zeros(len(logpars))
            step[col] = h
            J[row, col] = (survival(logpars + step, setting)
                           - survival(logpars - step, setting)) / (2 * h)
    assert np.all((y > 0) & (y < 1))
    WJ = J / np.sqrt(y * (1 - y))[:, None]
    return WJ.T @ WJ, np.linalg.svd(WJ, compute_uv=False)


def main():
    logpars = np.log(np.array([2., 1., 2., 3.]))
    one_times = np.linspace(0.05, 2.0, 20)
    one = [[(True, float(t))] for t in one_times]
    # A conservative fixed-amplitude design with several on and dark times.
    on_times = (0.05, 0.15, 0.35, 0.7)
    dark_times = (0.05, 0.2, 0.6, 1.2)
    echo = [[(True, t1), (False, tau), (True, t2)]
            for t1 in on_times for tau in dark_times for t2 in on_times]
    # A competent same-information estimator fits all 64 outcomes jointly;
    # the CRLB is a best-case local noise benchmark for any such estimator.
    for label, settings in (("one pulse", one), ("echo only", echo),
                            ("one pulse plus echo", one + echo)):
        F, sigma = fisher(logpars, settings)
        print(label, "settings", len(settings))
        print("  weighted sensitivity singular values:", sigma)
        print("  condition:", sigma[0] / sigma[-1])
        if sigma[-1] > 1e-8:
            cov = np.linalg.inv(F * 10000)
            print("  local CRLB fractional 1-sigma at N=10000 each:",
                  np.sqrt(np.diag(cov)))
        else:
            print("  structurally rank deficient at this design")


if __name__ == "__main__":
    main()
