#!/usr/bin/env python3
"""Exact scalar compiler for the cold-preparation proof.

This does NOT execute a quantum Gibbs sampler, generate the native SW catalogue,
or qualify the additional lambda_cool gate. It compiles the flat-filter bounds,
the polynomial-window order and an ordinary finite error-budget schedule.
No Hamiltonian, model fixture, or random trajectories are read.
"""

from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import hashlib
import json
import time


def poly_add(a, b):
    out = dict(a)
    for j, c in b.items():
        out[j] = out.get(j, 0) + c
        if out[j] == 0:
            del out[j]
    return out


def poly_deriv(a):
    return {j - 1: j * c for j, c in a.items() if j}


def poly_shift(a, j, c=1):
    return {i + j: c * x for i, x in a.items()}


def poly_mul(a, b):
    out = {}
    for i, x in a.items():
        for j, y in b.items():
            out[i + j] = out.get(i + j, 0) + x * y
    return {j: x for j, x in out.items() if x}


def derivative_majorants(order):
    """Integer bounds I4--I5, derived without floating point or quadrature."""
    B, S, filt = [], [], []
    p = {0: 1}
    for k in range(order + 1):
        B.append(sum(abs(c) * factorial(j) for j, c in p.items()))
        if k == 0:
            S.append(1)
        else:
            S.append(8 * (B[k] + 2 * sum(
                comb(k, j) * B[j] * S[k-j] for j in range(1, k+1))))
        filt.append(4 ** k * sum(
            comb(k, j) * S[j] * S[k-j] for j in range(k+1)))
        p = poly_shift(poly_add(p, poly_shift(poly_deriv(p), 0, -1)), 2)

    # d^k tanh(x)/dx^k = T_k(tanh(x)), |T_k| <= coefficient l1 norm.
    tanh, p = [], {1: 1}
    for k in range(order + 1):
        tanh.append(sum(abs(x) for x in p.values()))
        p = poly_mul({0: 1, 2: -1}, poly_deriv(p))
    return B, S, filt, tanh


def ceil_fraction(x):
    x = F(x)
    return (x.numerator + x.denominator - 1) // x.denominator


def ceil_log2_fraction(x):
    x = F(x)
    if x <= 1:
        return 0
    k = max(0, x.numerator.bit_length() - x.denominator.bit_length())
    while F(1 << k) < x:
        k += 1
    return k


def schedule(n, L, t, epsilon, C_star, energy_bound):
    """I7--I14. Potentially huge exact integers; caller chooses its display.

    A caller still has to satisfy/qualify the theorem's native coupling and
    geometry promises. This function supplies no such qualification.
    """
    t, epsilon, energy_bound = map(F, (t, epsilon, energy_bound))
    assert n >= 1 and L >= 2 and t > 0 and 0 < epsilon < 1
    assert C_star >= 1 and energy_bound >= 0
    m = n * (L - 1)
    M0 = L * L - 1
    A = C_star * (1 + ceil_fraction(t)) ** 4
    alpha = 8 * A
    U = 4 * ceil_log2_fraction(F(32*n*M0) / epsilon)
    delta = epsilon / (1024 * U * m * alpha**2)
    T = ceil_fraction(8*A/delta)
    K = 2 + ceil_fraction(128*A*(1+energy_bound)*T*T/delta)
    Q = 16*m*alpha**3
    R = ceil_fraction(1024*U*U*Q*Q/epsilon) + ceil_fraction(U*Q)
    ds = F(U, R)
    # A closed error receiver: all exact inequalities; no dynamics asserted.
    errors = {
        'mixing_upper': F(4*n*M0, 1 << (U//4)),
        'generator_perturbation_upper': 14*m*alpha**2*delta*U,
        'reset_splitting_upper': F(3*U*U*Q*Q, R),
        'finite_simulation_upper': epsilon/64,
        'final_dressing_upper': epsilon/32,
    }
    assert ds*Q <= 1
    assert ds*alpha**2 <= 1
    assert sum(errors.values()) < epsilon
    return dict(A=A, alpha=alpha, U=U, delta=delta, T=T,
                K=K, Q=Q, R=R, ds=ds, errors=errors)


def main():
    start = time.perf_counter()
    D, L, a = 3, 8, F(8)
    m = 3*D + 4
    K_hot = 2*m + D + 14
    cold_loss = a + (m+2)*max(a-1, 0)
    p = cold_loss.numerator // cold_loss.denominator + 3
    assert F(p) > cold_loss + 2
    # All proof moments can be obtained by extending this finite recurrence;
    # this generous order covers the displayed Taylor and overlap moments.
    order = p + 2*m + D + 16
    B, S, filt, tanh = derivative_majorants(order)
    C_h = 2 * max(filt[:5])
    C_g = max(6*sum(comb(k,j)*tanh[j]*S[k-j]
                    for j in range(k+1)) for k in range(5))
    C_star = 64 * (1 + C_h + C_g)
    assert C_star >= 6*max(C_h, C_g)
    # Error-budget acceptance follows symbolically from I7--I13:
    # epsilon/8 +14/1024 epsilon +3/1024 epsilon +epsilon/64+epsilon/32.
    symbolic_error = F(1,8)+F(14,1024)+F(3,1024)+F(1,64)+F(1,32)
    assert symbolic_error < 1
    result = {
        'status': 'EXACT_SCALAR_COMPILER_ONLY',
        'native_geometry_dimension_bound': D,
        'native_clock_dimension': L,
        'cold_exponent_a': str(a),
        'local_row_moment_m': m,
        'heating_polynomial_exponent_K': K_hot,
        'normal_form_order_p': p,
        'cold_power_margin': str(F(p)-cold_loss),
        'oscillator_projection_norm_upper': 2,
        'number_nonconstant_modes': L*L-1,
        'oscillator_perturbation_multiplier': 3*(L*L-1),
        'sufficient_generator_row_bound': str(F(1,12*(L*L-1))),
        'computed_filter_derivative_order': order,
        'F0_to_F4_exact': list(map(str, filt[:5])),
        'C_star_exact': str(C_star),
        'C_star_bits': C_star.bit_length(),
        'last_filter_majorant_bits': filt[-1].bit_length(),
        'formal_total_error_over_epsilon_upper': str(symbolic_error),
        'coherent_cutoff_frequency': 6,
        'G_exact_Bohr_support_radius': 3,
        'temperature_work_exponents_suppressing_n_U_epsilon': {
            'derivative_envelope_A': 4,
            'LCU_normalization_alpha': 4,
            'operator_tolerance_inverse': 8,
            'time_cutoff_T': 12,
            'channel_step_count_R': 24,
            'time_grid_length_K': 36,
            'coefficient_frequency_quadrature_adds_further_polynomial': True,
        },
        'new_hamiltonian_fixtures': 0,
        'quantum_state_preparations_executed': 0,
        'native_SW_catalogue_generated': False,
        'lambda_cool_numerically_qualified': False,
        'previous_literal_lambda_T_qualified': False,
        'practical_or_physical_preparation_claim': False,
        'wall_seconds_after_imports': time.perf_counter()-start,
    }
    out = Path(__file__).with_name('COMPILER_RECEIPT.json')
    out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in (
        'status','normal_form_order_p','cold_power_margin','C_star_bits',
        'last_filter_majorant_bits','formal_total_error_over_epsilon_upper',
        'wall_seconds_after_imports')}, indent=2))


if __name__ == '__main__':
    main()
