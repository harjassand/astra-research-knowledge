"""Finite algebra checks for the N-ring rapid-drive formulas in CYCLE2_REPORT.md."""
from math import exp, log, sinh, tanh, cosh, isclose


def analytic(N, A, d, B0, nu):
    q = exp(-A)
    c = nu * exp(-B0)
    u = c / N * (exp(d) + q * (exp(-d) + N - 2))
    w = c / N * (q * exp(d) + exp(-d) + (N - 2) * q)
    J = (u - w) / N
    T = u + w
    affinity = N * log(u / w)
    Wdot = 2 * A * c * (1 - q) * cosh(d) / N
    return u, w, J, T, affinity, Wdot


def phase_average(N, A, d, B0, nu):
    """Directly average each Arrhenius edge rate over the N protocol phases."""
    forward = [0.0] * N
    reverse = [0.0] * N
    for r in range(N):
        E = [0.0 if i == r else -A for i in range(N)]
        B = [B0 - d if i == r else B0 + d if i == (r - 1) % N else B0
             for i in range(N)]
        for i in range(N):
            j = (i + 1) % N
            forward[i] += nu * exp(-(B[i] - E[i])) / N
            reverse[i] += nu * exp(-(B[i] - E[j])) / N
    return forward, reverse


def check():
    for N in (3, 4, 5, 8):
        for A, d, B0, nu in ((4.0, 0.1, 0.5, 1.0),
                             (1.7, 0.35, 0.6, 2.3),
                             (7.0, 0.0, 0.4, 0.8)):
            u, w, J, T, affinity, Wdot = analytic(N, A, d, B0, nu)
            fwd, rev = phase_average(N, A, d, B0, nu)
            assert all(isclose(x, u, rel_tol=2e-14, abs_tol=2e-14) for x in fwd)
            assert all(isclose(x, w, rel_tol=2e-14, abs_tol=2e-14) for x in rev)
            assert isclose(J, 2 * nu * exp(-B0) * (1 - exp(-A))
                           * sinh(d) / N**2, rel_tol=2e-14, abs_tol=2e-14)
            assert isclose(J, (T / N) * tanh(affinity / (2 * N)),
                           rel_tol=2e-14, abs_tol=2e-14)
            if d > 0:
                assert isclose(Wdot, N * A * J / tanh(d),
                               rel_tol=2e-14, abs_tol=2e-14)
                K = 2 * nu * exp(-B0) * (1 - exp(-A)) / N**2
                assert isclose(Wdot, N * A * (J * J + K * K)**0.5,
                               rel_tol=2e-14, abs_tol=2e-14)
            print(f"PASS N={N} A={A} d={d}: J={J:.12g}, traffic={T:.12g}, "
                  f"affinity={affinity:.12g}, Wwell={Wdot:.12g}")


if __name__ == "__main__":
    check()
