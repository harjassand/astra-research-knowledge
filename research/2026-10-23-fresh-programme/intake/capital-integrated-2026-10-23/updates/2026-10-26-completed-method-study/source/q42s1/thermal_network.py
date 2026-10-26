"""Exact periodic DC response of reciprocal lumped thermal networks.

Only NumPy/SciPy; no fitted parameters or external datasets.  Heat currents are
positive from a fixed-temperature terminal into the network.  Temperatures can
be offsets about any common positive background.  Conductances are W/K, heat
capacities J/K, and durations s.  The ideal model omits actuator work and heat.
"""
from dataclasses import dataclass
import numpy as np
from scipy.linalg import expm
from numpy.polynomial.legendre import leggauss


@dataclass
class Phase:
    duration: float
    laplacian: np.ndarray


def laplacian(nodes, edges):
    """Undirected nonnegative (i, j, conductance) contacts."""
    out = np.zeros((nodes, nodes))
    for i, j, g in edges:
        if g < 0 or i == j:
            raise ValueError("Expected nonnegative conductances between nodes")
        out[i, i] += g
        out[j, j] += g
        out[i, j] -= g
        out[j, i] -= g
    return out


def blocks(L, ports):
    D = L[:ports, :ports]
    B = -L[ports:, :ports]
    A = L[ports:, ports:]
    return A, B, D


def segment_matrix(phase, capacity, ports):
    """Generator on [internal temperatures, constant terminal T, integral q]."""
    m = len(capacity)
    A, B, D = blocks(phase.laplacian, ports)
    F = np.zeros((m + 2*ports, m + 2*ports))
    F[:m, :m] = -np.linalg.solve(capacity, A)
    F[:m, m:m+ports] = np.linalg.solve(capacity, B)
    F[m+ports:, :m] = -B.T
    F[m+ports:, m:m+ports] = D
    return F


def response(phases, capacity, ports, gap_quadrature=0):
    """No burn-in: solve the periodic fixed point of exact segment exponentials.

    Requires stable periodic internal dynamics, so I-monodromy is invertible.
    Optional quadrature independently evaluates the proposed dissipation gap.
    """
    capacity = np.asarray(capacity, dtype=float)
    if capacity.ndim == 1:
        capacity = np.diag(capacity)
    m = capacity.shape[0]
    period = sum(p.duration for p in phases)
    total = np.eye(m + 2*ports)
    gens, maps = [], []
    for phase in phases:
        F = segment_matrix(phase, capacity, ports)
        E = expm(F * phase.duration)
        if not np.all(np.isfinite(E)):
            raise FloatingPointError('Nonfinite phase exponential')
        total = E @ total
        if not np.all(np.isfinite(total)):
            raise FloatingPointError('Nonfinite composed period map')
        gens.append(F)
        maps.append(E)
    M = total[:m, :m]
    X0 = np.linalg.solve(np.eye(m)-M, total[:m, m:m+ports])
    initial = np.vstack([X0, np.eye(ports), np.zeros((ports, ports))])
    final = total @ initial
    Y = final[m+ports:, :] / period
    if not np.all(np.isfinite(Y)):
        raise FloatingPointError('Nonfinite port response')
    Lbar = sum(p.duration * p.laplacian for p in phases) / period
    Abar, Bbar, Dbar = blocks(Lbar, ports)
    Xbar = np.linalg.solve(Abar, Bbar)
    Ybar = Dbar - Bbar.T @ Xbar
    result = dict(Y=Y, Ybar=Ybar, monodromy=M, X0=X0,
                  Xbar=Xbar, period=period,
                  periodic_residual=np.linalg.norm(final[:m]-X0))
    if gap_quadrature:
        points, weights = leggauss(gap_quadrature)
        integral = np.zeros((ports, ports))
        state = initial.copy()
        for phase, F, E in zip(phases, gens, maps):
            A = blocks(phase.laplacian, ports)[0]
            for v, w in zip(points, weights):
                t = (v+1)*phase.duration/2
                Z = (expm(F*t) @ state)[:m] - Xbar
                integral += (w*phase.duration/2) * Z.T @ A @ Z
            state = E @ state
        result['gap_integral'] = integral / period
    return result


def shuttle_phases(ports=3, on=1., off=0., period=3.):
    phases = []
    for active in range(ports):
        edges = [(j, ports, on if j == active else off)
                 for j in range(ports)]
        phases.append(Phase(period/ports, laplacian(ports+1, edges)))
    return phases


def ideal_shuttle(ports, conductance, capacity, period):
    """Closed-form terminal matrix for one exclusively contacted heat capacity."""
    z = conductance*period/(ports*capacity)
    r = np.exp(-z)
    a = capacity*(-np.expm1(-z))**2/(period*(-np.expm1(-ports*z)))
    Y = np.zeros((ports, ports))
    for j in range(ports):
        for i in range(ports):
            d = (j-i) % ports
            if d:
                Y[j, i] = -a*r**(d-1)
        Y[j, j] = -Y[j].sum()
    return Y


def leaky_shuttle(ports, on, off, capacity, period):
    """Exact finite leakage formula, equal durations and identical contacts."""
    G = on+(ports-1)*off
    alpha = (on-off)/G
    Y0 = ideal_shuttle(ports, G, capacity, period)
    Ybar = G/ports*(np.eye(ports)-np.ones((ports, ports))/ports)
    return alpha**2*Y0 + (1-alpha**2)*Ybar


def nonuniform_exclusive_shuttle(conductances, durations, capacity):
    """Exact arbitrary positive contact strengths and contact durations."""
    g, tau = np.asarray(conductances), np.asarray(durations)
    n = len(g)
    r = np.exp(-g*tau/capacity)
    denominator = -np.expm1(-np.sum(g*tau/capacity))
    Y = np.zeros((n, n))
    for j in range(n):
        for i in range(n):
            if i == j:
                continue
            indices = [(i+d) % n for d in range(1, (j-i) % n)]
            intermediate = np.prod(r[indices]) if indices else 1.
            Y[j, i] = -(capacity/tau.sum())*(1-r[j])*(1-r[i])*intermediate/denominator
        Y[j, j] = -Y[j].sum()
    return Y


def symmetric(X):
    return (X+X.T)/2


def contrast_basis(ports):
    from scipy.linalg import null_space
    return null_space(np.ones((1, ports)))


def min_contrast_eigenvalue(X):
    U = contrast_basis(len(X))
    return np.linalg.eigvalsh(U.T @ symmetric(X) @ U)[0]
