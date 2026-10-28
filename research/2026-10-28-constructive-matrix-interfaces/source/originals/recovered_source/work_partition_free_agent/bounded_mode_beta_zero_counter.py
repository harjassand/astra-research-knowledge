#!/usr/bin/env python3
"""Exact beta-zero counting with acquired, shared power-sum modes.

The global state is a weighted monomial simplex, not all partitions or
one alphabet per primary factor. Local Hall tables are still manufactured
and charged. If R is the number of acquired modes, time is t^O(R) poly(a,t).
No bounded R, shape, degree, or decomposition is silently assumed.
"""
from pathlib import Path
from fractions import Fraction
from functools import lru_cache
import itertools, math, sys, time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / p) for p in (
    'work_matrix_root', 'work_multiprimary_audit',
    'work_norm_frontier_agent', 'work_norm_slice_agent')]
from mixed_cycle_kernel import mixed_cycle_minor_numerator
from cyclic_primary_pfaffian import coefficient_degree_bound
from arbitrary_beta_zero_hall_aggregate import (
    acquire_local_aggregates, multiply_outside)
from arbitrary_operator_hall import power_multiply, quotient_matrix
from simple_operator_quadratic import matrix_source_anf
from krylov_square_source import quadratic_anf_sum
from feedback_nilpotent_gaussians import shifted_trace_polynomial


def weighted_power_ring(t, modes):
    """Divided-power monomials with sum_r r*k_r <= t, and their products."""
    modes = tuple(sorted(set(modes)))
    if any(type(r) is not int or not 1 <= r <= t for r in modes):
        raise ValueError('positive integer power modes at most the ambient size required')
    states = []
    def visit(j, budget, prefix):
        if j == len(modes):
            states.append(prefix)
            return
        for k in range(budget // modes[j] + 1):
            visit(j + 1, budget - modes[j] * k, prefix + (k,))
    visit(0, t, ())
    index = {state: i for i, state in enumerate(states)}
    splits = []
    for state in states:
        terms = []
        for left in itertools.product(*(range(k + 1) for k in state)):
            right = tuple(k - j for k, j in zip(state, left))
            terms.append((index[left], index[right],
                math.prod(math.comb(k, j) for k, j in zip(state, left))))
        splits.append(terms)
    physical = [sum(r * k for r, k in zip(modes, state)) for state in states]
    specifications = [dict(degree=r, maximum=t // r) for r in modes]
    return specifications, states, index, splits, physical


@lru_cache(None)
def power_mode_profile_weights(t, q, modes):
    """All L_(t,h)(prod p_r**k_r) in a manufactured weighted simplex.

    Unlike the squarefree interface, repeated powers do not require
    distinct actual irreducibles. Positive Hall convolution expresses
    repeated F_(1)[p_r] factors as a convex combination of physical flag
    functions at one irreducible. Thus the same population bound applies.
    """
    started = time.perf_counter()
    if type(t) is not int or t < 1 or type(q) is not int or q < 2 or q & (q - 1):
        raise ValueError('positive ambient size and binary field cardinality required')
    modes = tuple(sorted(set(modes)))
    specs, states, index, splits, physical = weighted_power_ring(t, modes)
    bounds = [4 * (c + 1) * q ** coefficient_degree_bound(t, c) for c in physical]
    bits = (2 * max(bounds) + 1).bit_length()
    a = q.bit_length() - 1
    cutoff = (bits + a - 1) // a
    r = t // 2
    shift = r * r if t % 2 else r * (r - 1)
    modulus = 1 << (bits + a * shift)
    small = 1 << bits
    raw, metadata = mixed_cycle_minor_numerator(
        t, q, specs, states, splits, physical, modulus, cutoff)
    prefactor = math.prod(1 - q ** j for j in range(1, t + 1))
    divisor = q ** shift
    weights = {}
    for state, c, row, bound in zip(states, physical, raw, bounds):
        residues = []
        for value in row:
            if value % divisor:
                raise AssertionError('profile q-shift divisibility failed')
            residue = (value // divisor) * prefactor % small
            residues.append(residue - small if residue >= small // 2 else residue)
        if any(residues[j] for j in range(8) if (c - j) % 2):
            raise AssertionError('profile phase parity failed')
        output = [residues[(c - 2 * h) % 8] for h in range(4)]
        if min(output) < 0 or sum(output) > bound:
            raise AssertionError('Hall-convex population bound failed')
        weights[state] = tuple(output)
    if weights[states[0]] != (1, 0, 0, 0):
        raise AssertionError('empty profile normalization failed')
    metadata.update(ambient_size=t, field_degree=a, power_modes=modes,
        power_mode_count=len(modes), weighted_monomial_states=len(states),
        output_precision_bits=bits, stored_integer_bits=bits + a * shift,
        field_population_cap_required=False, repeated_factors_Hall_convexity=True,
        enumerated_unrestricted_partitions=0, factorial_denominators=0,
        time_bound='poly(a,t,M), M=#{k>=0: sum_r r*k_r<=t}',
        seconds=time.perf_counter() - started)
    return weights, metadata


class PowerModeProfileFunctional:
    def __init__(self, q, t, modes):
        self.modes = tuple(sorted(set(modes)))
        self.position = {r: i for i, r in enumerate(self.modes)}
        self.weights, self.metadata = power_mode_profile_weights(t, q, self.modes)

    @lru_cache(None)
    def power_value(self, rho):
        state = [0] * len(self.modes)
        for r in rho:
            state[self.position[r]] += 1
        return self.weights[tuple(state)]

    def evaluate_rational(self, polynomial):
        """Read a general rational polynomial, without physical integrality."""
        answer = [Fraction(0)] * 4
        for rho, coefficient in polynomial.items():
            values = self.power_value(rho)
            for h in range(4):
                answer[h] += coefficient * values[h]
        return answer

    def evaluate(self, polynomial):
        answer = self.evaluate_rational(polynomial)
        if any(value.denominator != 1 for value in answer):
            raise AssertionError('physical Hall polynomial readout is not integral')
        return [value.numerator for value in answer]


def acquired_modes(primary):
    return tuple(sorted({item['degree'] * r for item in primary
                         for r in range(1, item['multiplicity'] + 1)}))


def bounded_mode_beta_zero_count(D, field_h, phi=(), eta=0, profile_backend='modes'):
    """Full original-domain count, polynomial for fixed acquired mode count."""
    started = time.perf_counter()
    F, primary, local, characteristic = acquire_local_aggregates(D, field_h)
    q = F.q
    t = len(D)
    phi = set(phi)
    if (type(eta) is not int or not 0 <= eta < q or
        any(type(v) is not int or v < 0 or v.bit_length() > F.a or v.bit_count() > 2 for v in phi)):
        raise ValueError('field eta and an explicit Boolean quadratic trace polynomial required')
    modes = acquired_modes(primary)
    if profile_backend == 'modes':
        functional = PowerModeProfileFunctional(q, t, modes)
    elif profile_backend == 'defect':
        from multiplicity_defect_profile import DefectProfileFunctional
        functional = DefectProfileFunctional(q, t, primary)
    else:
        raise ValueError('unknown profile backend')
    eligible = [i for i, item in enumerate(primary) if item['degree'] <= 2]
    linear = [i for i, item in enumerate(primary) if item['degree'] == 1]
    exceptional_sets = [()] + [(i,) for i in eligible] + list(itertools.combinations(linear, 2))
    answer = Fraction(0)
    gaussian_cache = {}
    leaves = 0
    largest_product = 0
    for exceptional in exceptional_sets:
        outside = multiply_outside(local, exceptional)
        largest_product = max(largest_product, *(len(poly) for poly in outside))
        for selected in itertools.product(*(local[i]['odd'] for i in exceptional)):
            flag = {(): Fraction(1)}
            population = 1
            rho = []
            for item in selected:
                flag = power_multiply(flag, item['flag'])
                population *= item['population']
                rho.append(item['rho'])
            key = (exceptional, tuple(rho))
            if key not in gaussian_cache:
                residual = quotient_matrix([primary[i] for i in exceptional], rho, F)
                b = len(residual)
                denominator = q ** (b * (b - 1) // 2)
                gaussians = []
                for parity in range(2 if eta else 1):
                    shifted = shifted_trace_polynomial(phi, F, eta if parity else 0, 0)
                    value = quadratic_anf_sum(matrix_source_anf(residual, F, 0, shifted, eta), F.a * b * b)
                    gaussians.append(Fraction(value, denominator))
                gaussian_cache[key] = gaussians
            gaussians = gaussian_cache[key]
            subtotal = Fraction(0)
            for epsilon, polynomial in enumerate(outside):
                combined = power_multiply(polynomial, flag)
                largest_product = max(largest_product, len(combined))
                weights = functional.evaluate(combined)
                subtotal += sum(weights[h] * gaussians[(h + epsilon) % len(gaussians)] for h in range(4))
            answer += population * subtotal
            leaves += 1
    gap = answer * q ** (t * t + t * (t - 1) // 2)
    n = 3 * F.a * t * t
    if gap.denominator != 1 or abs(gap) > 1 << n:
        raise AssertionError('invalid original-domain signed gap')
    gap = gap.numerator
    if gap % 2:
        raise AssertionError('invalid gap parity')
    return dict(original_independent_bits=n, gap=gap, ones=((1 << n) - gap) // 2,
        source_operator=D, field_polynomial=field_h, beta=0, eta=eta,
        trace_quadratic_anf=sorted(phi), acquired_characteristic=characteristic,
        acquired_primary=primary, acquired_power_modes=modes,
        number_of_primary_factors=len(primary),
        maximum_primary_multiplicity=max(item['multiplicity'] for item in primary),
        local_Hall_pair_counts=[item['all_local_pairs'] for item in local],
        exceptional_factor_sets=len(exceptional_sets), exceptional_Hall_leaves=leaves,
        exceptional_quotient_gaussians=len(gaussian_cache),
        largest_product_states=largest_product, profile_kernel=functional.metadata,
        supplied_primary_decomposition=False, full_original_domain=True,
        auxiliary_independent_inputs=0, enumerated_original_assignments=0,
        enumerated_global_unrestricted_partitions=0,
        time_bound=functional.metadata['time_bound'], profile_backend=profile_backend,
        polynomial_for_fixed_power_mode_count=True,
        unrestricted_polynomial_counter=False, seconds=time.perf_counter() - started)


def compile_bounded_mode_trace_response(D, field_h, eta=0):
    """At most two evaluations of any trace program, on certified spectra."""
    started = time.perf_counter()
    F, primary, local, characteristic = acquire_local_aggregates(D, field_h)
    if type(eta) is not int or not 0 <= eta < F.q:
        raise ValueError('field eta required')
    for item in primary:
        d = item['degree']
        f = item['irreducible']
        if d < 2 or (d == 2 and F.mul(F.mul(eta, eta), f[1]) == 1):
            raise ValueError('spectrum does not certify the two-point trace response')
    t = len(D)
    modes = acquired_modes(primary)
    functional = PowerModeProfileFunctional(F.q, t, modes)
    combined = multiply_outside(local, ())
    scale = F.q ** (t * t + t * (t - 1) // 2)
    points = {}
    for epsilon, polynomial in enumerate(combined):
        for h, value in enumerate(functional.evaluate(polynomial)):
            point = eta if (h + epsilon) % 2 else 0
            points[point] = points.get(point, 0) + scale * value
    points = {x: value for x, value in points.items() if value}
    if len(points) > 2 or any(value < 0 for value in points.values()):
        raise AssertionError('invalid positive trace response')
    return dict(field_polynomial=field_h, field_degree=F.a, matrix_size=t,
        beta=0, eta=eta, original_independent_bits=3 * F.a * t * t,
        counted_domain_size=F.q ** (3 * t * t), acquired_primary=primary,
        acquired_characteristic=characteristic, acquired_power_modes=modes,
        response=[dict(kind='point', argument=x, coefficient=value) for x, value in sorted(points.items())],
        maximum_trace_program_evaluations=len(points), profile_kernel=functional.metadata,
        supplied_primary_decomposition=False, full_original_domain=True,
        trace_program_expanded=False, unrestricted_polynomial_counter=False,
        time_bound='poly(a,t,M)+at most two trace-program evaluations',
        seconds=time.perf_counter() - started)


if __name__ == '__main__':
    import argparse, json
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--trace-response', action='store_true')
    args = parser.parse_args()
    data = json.loads(args.source.read_text())
    if args.trace_response:
        result = compile_bounded_mode_trace_response(data['D'], data['h'], data.get('eta', 0))
    else:
        result = bounded_mode_beta_zero_count(data['D'], data['h'], data.get('phi', ()), data.get('eta', 0))
    rendered = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end='')
