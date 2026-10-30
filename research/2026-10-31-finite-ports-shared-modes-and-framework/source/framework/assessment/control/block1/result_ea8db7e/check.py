#!/usr/bin/env python3
"""Exact cycle-noise certificate plus diagnostics for the proved scalar law.

Uses local SymPy; no network, installation, or physical access. The grid is
only a diagnostic. The continuum and bath guarantees are analytic in PROOF.md.
"""
import cmath
import json
import math
from fractions import Fraction

import sympy as sp

import schedule


def exact_cycle_certificate():
    eye = sp.eye(2)
    x = sp.Matrix([[0, 1], [1, 0]])
    y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    z = sp.diag(1, -1)
    kron = sp.kronecker_product
    ident = sp.eye(8)
    zero = sp.zeros(8)
    handles = {'A': kron(x, eye, x), 'B': kron(eye, x, y),
               'C': kron(y, eye, z)}
    drift = kron(eye, eye, y)/2
    f = kron(z, x, eye)

    def multiply(a, b):
        return [sum((a[j]*b[n-j] for j in range(n+1)), zero)
                for n in range(5)]

    def trace_data(mat):
        return sum((mat[2*j:2*j+2, 2*j:2*j+2] for j in range(4)),
                   sp.zeros(2))

    fidelity_series = [sp.S(0)]*5
    second_order = []
    for sa in (-1, 1):
        for sb in (-1, 1):
            signs = {'A': sa, 'B': sb, 'C': sa*sb}
            series = [ident, zero, zero, zero, zero]
            for handle, orientation in schedule.ORIENTED_CYCLE:
                h = drift+orientation*signs[handle]*handles[handle]
                generator = -sp.I*h
                pulse = [generator**n/sp.factorial(n) for n in range(5)]
                series = multiply(pulse, series)
            # Correct by exp(+4i*delta^3*F), the intended cycle gate inverse.
            target_inverse = [ident, zero, zero, 4*sp.I*f, zero]
            corrected = multiply(target_inverse, series)
            traced = [trace_data(u) for u in corrected]
            for n in range(5):
                value = sum(sp.trace(traced[j]*traced[n-j].conjugate().T)
                            for j in range(n+1))/32
                fidelity_series[n] += value/4
            pa = kron(x, eye, z)
            pc = kron(y, eye, x)
            second_order.append({
                'sa': sa, 'sb': sb,
                'X1_sigma_z_coefficient': str(sp.trace(pa*series[2])/8),
                'Y1_sigma_x_coefficient': str(sp.trace(pc*series[2])/8),
            })
    fidelity_series = [sp.simplify(value) for value in fidelity_series]
    assert fidelity_series == [1, 0, 0, 0, -41], fidelity_series
    return {'averaged_entanglement_fidelity_coefficients_delta_0_to_4':
            list(map(str, fidelity_series)),
            'per_sign_second_order_nonmemory_terms': second_order}


def scalar_diagnostics():
    n = 9
    theta = math.pi/n
    v = [cmath.exp(1j*j*theta)/math.sqrt(n) for j in range(n)]
    target_moment_matrix = [[1 if j == k else (-1j if j > k else 1j)
                             for k in range(n)] for j in range(n)]
    eigenvalue = 1-1/math.tan(math.pi/(2*n))
    residual = max(abs(sum(target_moment_matrix[j][k]*v[k]
                           for k in range(n))-eigenvalue*v[j])
                   for j in range(n))
    assert residual < 1e-12
    barrier = -eigenvalue/8
    r = 1-1/schedule.M
    step = float(schedule.ANGLE_STEP)
    maximum = (-1.0, None)
    for j in range(20001):
        c = 1+7*j/20000
        z = cmath.exp(-2j*c*step)
        rz = r*z
        characteristic = (1-r)/(1-rz)*(1-rz**schedule.K)+rz**schedule.K
        distance = abs(characteristic+1j)
        if distance > maximum[0]:
            maximum = (distance, c)
    analytic_scalar_bound = math.sqrt(26/37)+6/schedule.M+2*math.exp(-16)
    full_bound = analytic_scalar_bound+float(schedule.SYNTHESIS_ERROR)
    assert maximum[0] <= analytic_scalar_bound
    assert full_bound < 0.84
    assert schedule.cycle_count(schedule.K) == schedule.MAX_CYCLES
    assert 4*Fraction(schedule.cycle_count(123), schedule.Q**3) == 123*schedule.ANGLE_STEP
    # Exercise a finite prefix, never the astronomical full native word.
    prefix = schedule.native_segments_for_index(1, iter([0, 1]*10))
    first_ten = [next(prefix) for _ in range(10)]
    assert all(t == schedule.DELTA and abs(u) == 1 for _, u, t in first_ten)
    assert schedule.sample_capped_geometric(iter([0]*13)) == 0
    return {
        'restricted_scalar_error_lower_bound': barrier,
        'moment_matrix_eigenvector_residual': residual,
        'continuous_exponential_scalar_bound': math.sqrt(26/37),
        'finite_scalar_analytic_bound': analytic_scalar_bound,
        'full_analytic_bound_including_native_synthesis_and_timing': full_bound,
        'grid_only_maximum_finite_scalar_distance': maximum[0],
        'grid_only_maximizing_gain_product': maximum[1],
        'grid_points': 20001,
    }


if __name__ == '__main__':
    output = {'exact_cycle': exact_cycle_certificate(),
              'scalar_diagnostics': scalar_diagnostics(),
              'resources': schedule.resources()}
    print(json.dumps(output, indent=2))
