"""Exact finite-data spectral tails in the complete Morse Jacobi space.

lambda=8, D=1, F=exp(-a q). Sources F|n> and F^2|n>, n=2,4,6.
All polynomial actions use every finite-support coefficient. There is no
finite-box continuum approximation. Rational spectral Markov bounds are
optimized over ALL nonnegative integer powers: moment log-convexity proves
that the first nondecreasing ratio identifies a global minimum.

Run with Python's standard library only. JSON rational bounds are the
mathematical results; floats are display approximations.
"""
from fractions import Fraction
from math import comb, factorial, isqrt, sqrt
from pathlib import Path
import json

N = 8
H_SCALE = 256
F_SCALE = 16


def native_integer_vector(n):
    """Integer multiple of the exact normalized native Morse eigenvector."""
    x = []
    for j in range(N):
        value = 0
        for ell in range(n + 1):
            power = N - n - 1 + ell
            if power < j:
                continue
            coeff = ((-1)**ell * comb(2*N-n-1, n-ell)
                     * factorial(power) // factorial(ell))
            value += coeff * comb(power, j)
        x.append((-1)**j * value)
    return x


def norm2(x):
    return sum(z*z for z in x)


def integer_F_action(x):
    """16 F; the returned extra coefficient is retained, never discarded."""
    out = [0] * (len(x) + 1)
    for j, z in enumerate(x):
        out[j] += (2*j+1)*z
        if j:
            out[j-1] -= j*z
        out[j+1] -= (j+1)*z
    return out


def integer_H_action(x):
    """256 H_M; exact full Jacobi action on a finite-support vector."""
    out = [0] * (len(x) + 1)
    for j, z in enumerate(x):
        out[j] += (8*j*j-56*j+227)*z
        if j:
            out[j-1] -= 4*(j-8)*j*z
        out[j+1] -= 4*(j-7)*(j+1)*z
    return out


def sqrt_upper_decimal(q, places=120):
    """An exact upward decimal upper bound on sqrt(nonnegative Fraction)."""
    scale = 10**places
    scaled_numerator = q.numerator * scale * scale
    k = isqrt(scaled_numerator // q.denominator)
    if k*k*q.denominator < scaled_numerator:
        k += 1
    digits = str(k).zfill(places+1)
    return digits[:-places] + '.' + digits[-places:]


def one_source(n, power, thresholds=(50, 100)):
    x = native_integer_vector(n)
    source_normalization = norm2(x) * F_SCALE**(2*power)
    eigenvalue_numerator = 256 - (15-2*n)**2
    hx = integer_H_action(x)
    assert hx == [eigenvalue_numerator*z for z in x] + [0]
    y = x
    for _ in range(power):
        y = integer_F_action(y)
    source_norm2 = Fraction(norm2(y), source_normalization)
    current = y
    previous_moment_numerator = norm2(current)
    unfinished = set(thresholds)
    results = {}
    moment = 0
    while unfinished:
        next_vector = integer_H_action(current)
        next_moment_numerator = norm2(next_vector)
        for threshold in sorted(unfinished.copy()):
            comparison_rhs = previous_moment_numerator * (H_SCALE*threshold)**2
            if next_moment_numerator >= comparison_rhs:
                # b_(m+1)/b_m >=1, and all future ratios are >= this one.
                bound = Fraction(previous_moment_numerator,
                    source_normalization * (H_SCALE*threshold)**(2*moment))
                results[str(threshold)] = {
                    'threshold_over_D': threshold,
                    'optimal_integer_moment': moment,
                    'source_support_max_index': max(j for j,z in enumerate(y) if z),
                    'moment_support_max_index': max(j for j,z in enumerate(current) if z),
                    'spectral_weight_bound_exact': str(bound),
                    'spectral_weight_bound_float': float(bound),
                    'spectral_amplitude_bound_float': sqrt(float(bound)),
                    'spectral_amplitude_exact_upper_decimal': sqrt_upper_decimal(bound),
                    'next_bound_ratio_exact': str(Fraction(next_moment_numerator, comparison_rhs)),
                    'global_integer_optimum_by_log_convexity': True,
                }
                unfinished.remove(threshold)
        current = next_vector
        previous_moment_numerator = next_moment_numerator
        moment += 1
    return {
        'native_level': n,
        'native_energy_over_D_exact': str(Fraction(eigenvalue_numerator, 256)),
        'source': f'F^{power}|{n}>',
        'source_norm_squared_exact': str(source_norm2),
        'source_norm_float': sqrt(float(source_norm2)),
        'thresholds': results,
    }


def main():
    cases = [one_source(n,k) for n in (2,4,6) for k in (1,2)]
    code_bounds = {}
    for threshold in (50,100):
        # Frobenius bound uniform on the coherent three-dimensional input code.
        by_power = {}
        for power in (1,2):
            q = sum((Fraction(r['thresholds'][str(threshold)]['spectral_weight_bound_exact'])
                     for r in cases if r['source'].startswith(f'F^{power}')), Fraction(0))
            by_power[str(power)] = {
                'uniform_code_weight_bound_exact': str(q),
                'uniform_code_weight_bound_float': float(q),
                'uniform_code_amplitude_bound_float': sqrt(float(q)),
                'uniform_code_amplitude_exact_upper_decimal': sqrt_upper_decimal(q),
            }
        code_bounds[str(threshold)] = by_power
    # Additional source-level completion for a centered harmonic lateral
    # ground state. sin(kX)|0> has odd oscillator levels only, with exact
    # squared coefficients exp(-mu)*mu^l/l!, mu=(k sigma)^2. At a sigma=.1,
    # l<=31 leaves the intra-F absorption window (halfwidth D) above50D.
    # For l>=33 use an exact rational geometric majorant, dropping exp(-mu).
    transverse = {}
    for power in (1, 2):
        mu = Fraction(power*power, 100)
        first = 33
        odd_tail = (mu**first / factorial(first)
                    / (1-mu*mu/Fraction((first+1)*(first+2))))
        source_frob2 = sum((Fraction(r['source_norm_squared_exact'])
                           for r in cases
                           if r['source'].startswith(f'F^{power}')), Fraction(0))
        low_nuclear = Fraction(code_bounds['50'][str(power)]
                               ['uniform_code_weight_bound_exact'])
        # ||sin(kX)|0>|| <= k sigma. Triangle separates low/high lateral l.
        low_squared = Fraction(power*power, 100)*low_nuclear
        high_squared = odd_tail*source_frob2
        transverse[str(power)] = {
            'source': f'F^{power} sin({power} a X)|n,0_perp>',
            'odd_oscillator_tail_start': first,
            'odd_oscillator_tail_weight_bound_exact': str(odd_tail),
            'odd_oscillator_tail_weight_bound_float': float(odd_tail),
            'coherent_code_source_frobenius_norm_squared_exact': str(source_frob2),
            'low_transverse_window_residual_squared_bound_exact': str(low_squared),
            'high_transverse_window_residual_squared_bound_exact': str(high_squared),
            'window_residual_amplitude_bound_float':
                sqrt(float(low_squared))+sqrt(float(high_squared)),
            'window_residual_bound_formula':
                'sqrt(low_squared_exact)+sqrt(high_squared_exact)',
        }
    # Actual compensated profile: A_r=a_r exp(r^2 s^2/2), a_1=1,a_2=-1/3.
    # Its oscillator coefficient is a_r (i r s)^l/sqrt(l!), with no Gaussian
    # exponential. Use the requested halfwidth5D window, keeping odd l<=29
    # in the high-nuclear-energy sector and bounding ALL l>=30 by a
    # geometric majorant. This is conservative for the odd sine source.
    compensated = {}
    source_upper_rational = {}
    for power in (1, 2):
        mu = Fraction(power*power, 100)
        poisson_tail = mu**30 / factorial(30) / (1-mu/31)
        # sinh(mu) <= mu/(1-mu^2/6), by ratios of successive odd terms.
        sine_norm2_bound = mu / (1-mu*mu/6)
        source_frob2 = sum((Fraction(r['source_norm_squared_exact'])
                           for r in cases
                           if r['source'].startswith(f'F^{power}')), Fraction(0))
        nuclear_weight = Fraction(code_bounds['50'][str(power)]
                                  ['uniform_code_weight_bound_exact'])
        low_squared = sine_norm2_bound*nuclear_weight
        high_squared = poisson_tail*source_frob2
        upper = (Fraction(sqrt_upper_decimal(low_squared))
                 + Fraction(sqrt_upper_decimal(high_squared)))
        source_upper_rational[power] = upper
        compensated[str(power)] = {
            'compensated_source': f'exp({power**2}/200) F^{power} sin({power} a X)|n,0_perp>',
            'all_oscillator_tail_start': 30,
            'oscillator_tail_weight_bound_exact': str(poisson_tail),
            'oscillator_tail_weight_bound_float': float(poisson_tail),
            'compensated_sine_norm_squared_bound_exact': str(sine_norm2_bound),
            'low_transverse_window_residual_squared_bound_exact': str(low_squared),
            'high_transverse_window_residual_squared_bound_exact': str(high_squared),
            'window_residual_amplitude_upper_rational': str(upper),
            'window_residual_amplitude_upper_float': float(upper),
        }
    # 2/sqrt(3)<6/5, two axes by triangle; no Fourier1/2 improvement used.
    full_longitudinal_upper = (Fraction(6,5)
        * (source_upper_rational[1]+source_upper_rational[2]/3))
    assert full_longitudinal_upper < Fraction(1,10**24)
    report = {
        'scope': __doc__,
        'lambda': 8, 'D': 1, 'native_levels': [2,4,6],
        'cases': cases, 'uniform_coherent_code_bounds': code_bounds,
        'harmonic_transverse_source_extension': {
            'a_sigma_exact': '1/10',
            'hbar_omega_perp_over_D_exact': '25/16',
            'drive_hbar_omega_over_D_exact': '201/2',
            'excluded_window_halfwidth_over_D': 1,
            'lowest_window_endpoint_for_odd_l_at_most31_exact': '13207/256',
            'hyperfine_assisted_odd_channel_gap_over_D_exact': '7/32',
            'sources': transverse,
            'scope': 'First-order source and spectral window only, under the declared independent harmonic ground state and quasistatic spatial harmonics; no higher-order Floquet or full gate assertion.',
        },
        'compensated_five_D_window_extension': {
            'a_sigma_exact': '1/10',
            'excluded_window_halfwidth_over_D': 5,
            'lowest_window_endpoint_for_odd_l_at_most29_exact': '12983/256',
            'sources': compensated,
            'profile_coefficients_before_Debye_Waller_compensation': ['1','-1/3'],
            'spin_diagonal_Dz_over_d_abs': '1/sqrt(3)',
            'axes': 2,
            'full_longitudinal_window_amplitude_upper_exact': str(full_longitudinal_upper),
            'full_longitudinal_window_amplitude_upper_float': float(full_longitudinal_upper),
            'full_longitudinal_window_amplitude_below_1e_minus24_exactly': True,
            'scope': 'Uniform source-column/Frobenius bound for the intra-F longitudinal absorption window. Two axes are charged by triangle without Fourier amplitude gain; all lateral oscillator levels included. This does not bound the full driven gate.',
        },
        'normalization': 'F=Y/16; H_M=A/256; native source x/sqrt(sum x_j^2).',
        'proof': 'Spectral Markov inequality and log-convex exact squared moments; no continuum cutoff.',
    }
    target = Path(__file__).with_suffix('.json')
    target.write_text(json.dumps(report, indent=2)+'\n')
    print('n power A m spectral_weight_bound spectral_amplitude_bound')
    for case in cases:
        power = int(case['source'][2])
        for A in (50,100):
            q = case['thresholds'][str(A)]
            print(case['native_level'],power,A,q['optimal_integer_moment'],
                  f"{q['spectral_weight_bound_float']:.12e}",
                  f"{q['spectral_amplitude_bound_float']:.12e}")
    print('coherent-code Frobenius upper bounds')
    for A, r in code_bounds.items():
        for power, q in r.items():
            print(A,power,f"{q['uniform_code_amplitude_bound_float']:.12e}")
    print('harmonic lateral extension: intra-F excluded-window amplitude bounds')
    for power, q in transverse.items():
        print(power, f"{q['window_residual_amplitude_bound_float']:.12e}")
    print('compensated5D full longitudinal source upper bound:',
          f'{float(full_longitudinal_upper):.12e}')
    print('Saved',target)


if __name__ == '__main__':
    main()
