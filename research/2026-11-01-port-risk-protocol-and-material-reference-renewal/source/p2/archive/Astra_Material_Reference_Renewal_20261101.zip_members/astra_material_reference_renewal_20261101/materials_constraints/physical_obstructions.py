"""Executable counterexamples for local geometric protection of repairing solids.

All numerical parameters are dimensionless model choices, not material data.
No external simulator or fitted force field is supplied. The checks concern
exact finite Markov chains, linear elasticity, and a reaction--diffusion slab.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
from scipy.linalg import null_space


def stationary(Q):
    A = Q.T.copy()
    b = np.zeros(len(Q))
    A[-1] = 1.0
    b[-1] = 1.0
    p = np.linalg.solve(A, b)
    assert np.min(p) > -1e-12
    assert np.linalg.norm(p @ Q) < 1e-10
    return p


def fueled_gate(affinity, bath_correct=0.3, selectivity=1.0):
    # States V, C_open, C_protected, W_open, W_protected.
    # O<->P has passive and fueled channels, each with local detailed balance.
    # Dimensionless protected/open energy gap is delta=-2.
    delta = -2.0
    pf = 0.1 * np.exp((affinity - delta) / 2)
    uf = 0.1 * np.exp(-(affinity - delta) / 2)
    p0 = np.exp(-delta / 2)
    u0 = np.exp(delta / 2)
    protect, unprotect = p0 + pf, u0 + uf
    dC, dW = 0.8, 0.8 * selectivity
    Q = np.zeros((5, 5))
    Q[0, 1], Q[0, 3] = 3 * bath_correct, 3 * (1 - bath_correct)
    Q[1, 0], Q[3, 0] = dC, dW
    Q[1, 2] = Q[3, 4] = protect
    Q[2, 1] = Q[4, 3] = unprotect
    Q -= np.diag(Q.sum(axis=1))
    pi = stationary(Q)
    occupied = 1 - pi[0]
    correctness = (pi[1] + pi[2]) / occupied
    expected_correctness = bath_correct * selectivity / (
        bath_correct * selectivity + 1 - bath_correct
    )
    assert abs(correctness - expected_correctness) < 1e-12
    fuel_current = pf * (pi[1] + pi[3]) - uf * (pi[2] + pi[4])
    assert affinity * fuel_current >= -1e-12

    # Absorbing first-passage times from O/P until departure.
    def mean_residence(d):
        transient = np.array([[-d-protect, protect], [unprotect, -unprotect]])
        times = np.linalg.solve(-transient, np.ones(2))
        exact = (d + protect + unprotect) / (unprotect * d)
        assert abs(times[1] - exact) / exact < 1e-12
        return float(times[1])

    return dict(affinity=affinity, bath_correct=bath_correct,
                selectivity=selectivity, correctness=float(correctness),
                entropy_production_rate=float(affinity*fuel_current),
                protected_C_residence=mean_residence(dC),
                protected_W_residence=mean_residence(dW),
                stationarity_residual=float(np.linalg.norm(pi @ Q)))


def spring_network():
    # Four vertices and six bars: a planar square with both diagonals.
    xy = np.array([[0., 0.], [1., 0.], [1., 1.], [0., 1.]])
    edges = [(0,1),(1,2),(2,3),(3,0),(0,2),(1,3)]
    B = np.zeros((len(edges), 2*len(xy)))
    lengths = []
    for k, (i,j) in enumerate(edges):
        e = xy[j]-xy[i]
        lengths.append(np.linalg.norm(e))
        e /= np.linalg.norm(e)
        B[k,2*i:2*i+2] = -e
        B[k,2*j:2*j+2] = e
    U, s, Vh = np.linalg.svd(B)
    rank = np.sum(s > 1e-10)
    S = null_space(B.T)
    P = S @ S.T
    assert rank == 5 and S.shape == (6,1)
    assert np.linalg.norm(P @ B) < 1e-12
    rng = np.random.default_rng(30)
    d = rng.normal(size=6)
    u, *_ = np.linalg.lstsq(B, d, rcond=None)
    E = np.sum((B@u-d)**2)/2
    assert abs(E-np.sum((P@d)**2)/2) < 1e-12

    # A compatible error changes the desired shape with zero internal stress.
    shape_change = np.zeros_like(xy)
    shape_change[:,0] = 0.05*xy[:,0]
    dc = B @ shape_change.ravel()
    assert np.linalg.norm(P@dc) < 1e-12
    # Exact nonlinear counterpart: replace rest lengths by a rectangle's lengths.
    rectangle = xy + shape_change
    exact_rest = np.array([np.linalg.norm(rectangle[j]-rectangle[i]) for i,j in edges])
    exact_energy = sum((np.linalg.norm(rectangle[j]-rectangle[i])-exact_rest[k])**2/2
                       for k,(i,j) in enumerate(edges))
    assert exact_energy == 0.0

    # Arbitrary compatible imposed displacement does not alter this differential
    # syndrome in the linear model. A physical force readout is still required.
    imposed = rng.normal(size=8)
    syndrome_before = P @ d
    syndrome_after = P @ (d + B @ imposed)
    return dict(rank=int(rank), self_stress_dimension=S.shape[1],
                self_stress_vector=S[:,0].tolist(),
                residual_energy=float(E),
                projection_error=float(abs(E - np.dot(P@d,P@d)/2)),
                compatible_error_norm=float(np.linalg.norm(dc)),
                compatible_error_syndrome=float(np.linalg.norm(P@dc)),
                exact_rectangle_rest_lengths=exact_rest.tolist(),
                exact_rectangle_energy=float(exact_energy),
                imposed_displacement_syndrome_error=float(np.linalg.norm(syndrome_after-syndrome_before)))


def transport():
    # Slab -L<x<L, D c''-k c=0, c(+-L)=c0.
    # This is an explicit model, not a universal lower bound on all delivery.
    D,k,c0 = 1.0,1.0,1.0
    lam = np.sqrt(D/k)
    result = []
    for L in [0.1,1.0,3.0,10.0]:
        # finite differences independently validate the analytic center value
        n=4000
        h=2*L/n
        diag=np.full(n-1,2*D/h**2+k)
        rhs=np.zeros(n-1)
        rhs[0] += D*c0/h**2
        rhs[-1] += D*c0/h**2
        # tridiagonal solve
        from scipy.linalg import solve_banded
        ab=np.zeros((3,n-1)); ab[1]=diag
        ab[0,1:]=-D/h**2; ab[2,:-1]=-D/h**2
        numerical=solve_banded((1,1),ab,rhs)
        center_exact=c0/np.cosh(L/lam)
        center_numerical=numerical[n//2-1]
        assert abs(center_numerical-center_exact) < 2e-7
        result.append(dict(half_thickness=L,center_fuel=float(center_exact),
                           numerical_center_fuel=float(center_numerical),
                           mean_fuel=float(c0*lam/L*np.tanh(L/lam))))
    return result


def main():
    out = dict(
        label_blind=[fueled_gate(A) for A in [0,2,5,10]],
        physically_selective=[fueled_gate(A,selectivity=10) for A in [0,2,5,10]],
        spring_network=spring_network(),
        surface_fueled_slab=transport(),
        scope='Model counterexamples and identities; not measurements or universal chemistry no-go.'
    )
    path=Path(__file__).with_name('physical_obstructions_results.json')
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    main()
