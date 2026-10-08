"""Finite three-state stochastic pump witness; only Python's standard library needed."""
from math import exp, ceil, log2

# Oriented ring edges 0->1, 1->2, 2->0. Energy units are k_B T and nu_e=1 s^-1.
EDGES = [(0, 1), (1, 2), (2, 0)]

def eye(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]

def matadd(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))]
            for i in range(len(A))]

def matscale(A, c):
    return [[c * x for x in row] for row in A]

def matvec(A, x):
    return [sum(A[i][j] * x[j] for j in range(len(x))) for i in range(len(A))]

def expm(A):
    """Scaling-and-squaring Taylor exponential for the small 3x3/6x6 matrices here."""
    n = len(A)
    norm = max(sum(abs(x) for x in row) for row in A)
    s = max(0, ceil(log2(norm / 0.25))) if norm > 0.25 else 0
    X = matscale(A, 2.0 ** (-s))
    out = term = eye(n)
    for k in range(1, 100):
        term = matscale(matmul(term, X), 1.0 / k)
        out = matadd(out, term)
        if max(abs(x) for row in term for x in row) < 1e-17:
            break
    for _ in range(s):
        out = matmul(out, out)
    return out

def generator(E, B):
    """Column generator for k_(i->j)=exp(-(B_e-E_i)) s^-1."""
    Q = [[0.0] * 3 for _ in range(3)]
    rates = []
    for e, (i, j) in enumerate(EDGES):
        kij = exp(-(B[e] - E[i]))
        kji = exp(-(B[e] - E[j]))
        Q[j][i] += kij
        Q[i][i] -= kij
        Q[i][j] += kji
        Q[j][j] -= kji
        rates.append((i, j, kij, kji))
    return Q, rates

def phase_transition_and_flux(E, B, p0, tau):
    Q, rates = generator(E, B)
    # Augmented ODE: p'=Qp, z'=p, so z(tau)=integral_0^tau p(t)dt.
    Aug = [[0.0] * 6 for _ in range(6)]
    for i in range(3):
        for j in range(3):
            Aug[i][j] = Q[i][j]
        Aug[i + 3][i] = 1.0
    M = expm(matscale(Aug, tau))
    p1 = matvec([row[:3] for row in M[:3]], p0)
    z = matvec([row[:3] for row in M[3:]], p0)
    flux = [kij * z[i] - kji * z[j] for i, j, kij, kji in rates]
    return p1, flux

def periodic_protocol(A, deltaB, tau, barrier_gate=True):
    """Rotate the low well 1->2->0; lower the forward edge's barrier to 0.

    With barrier_gate=False, keep every barrier at 0 while using the identical
    rotating well-depth waveform. State-energy work is sum_i p_i Delta E_i.
    """
    Es = [[0., -A, 0.], [0., 0., -A], [-A, 0., 0.]]
    if barrier_gate:
        Bs = [[0., deltaB, deltaB], [deltaB, 0., deltaB], [deltaB, deltaB, 0.]]
    else:
        Bs = [[0.] * 3 for _ in range(3)]
    P = eye(3)
    for E, B in zip(Es, Bs):
        Q, _ = generator(E, B)
        P = matmul(expm(matscale(Q, tau)), P)
    p = [1.0 / 3.0] * 3
    closure = float('inf')
    for _ in range(100000):
        pn = matvec(P, p)
        closure = sum(abs(pn[i] - p[i]) for i in range(3))
        p = pn
        if closure < 1e-14:
            break
    p = [max(0.0, x) for x in p]
    p = [x / sum(p) for x in p]
    allflux = [0.0] * 3
    Eprev = Es[-1]
    work = 0.0
    p_start = p.copy()
    for E, B in zip(Es, Bs):
        work += sum(p[i] * (E[i] - Eprev[i]) for i in range(3))
        p, fl = phase_transition_and_flux(E, B, p, tau)
        allflux = [allflux[i] + fl[i] for i in range(3)]
        Eprev = E
    return allflux, work, p_start, closure

if __name__ == '__main__':
    A, tau = 4.0, 1.0
    F0, W0, _, close0 = periodic_protocol(A, 0.0, tau, barrier_gate=False)
    print(f'fixed barriers: max |edge flux|={max(abs(x) for x in F0):.3g}, '
          f'well work={W0:.12g} kBT/cycle, closure={close0:.3g}')
    print('deltaB/kBT, J/cycle, W_E/kBT/cycle, W_E/J/kBT per product, '
          'bound J/cycle, J/T s^-1 per site')
    for deltaB in [0.001, 0.002, 0.005, 0.01, 0.05, 0.1, 0.25, 0.5, 1.0]:
        F, W, p0, closure = periodic_protocol(A, deltaB, tau, barrier_gate=True)
        J = sum(F) / 3.0
        eta = 1.0 - exp(-deltaB)  # c_e/c_e0 in [exp(-deltaB),1]
        # Triangle aggregate bound; c_e0=1 s^-1, gmax=1, T=3*tau.
        bound = 2.0 * eta * (3.0 * tau) / 3.0
        print(f'{deltaB:.3g}, {J:.12g}, {W:.12g}, {W/J:.8g}, '
              f'{bound:.8g}, {J/(3.0*tau):.12g}; closure={closure:.2g}')
