#!/usr/bin/env python3
"""Manufacture at most t trace characters and two points for every D, beta=0.

The short output is constructed in exp(O(sqrt(t)))*poly(a,t), not assumed
free.  Pairing its Walsh terms with an arbitrary Boolean program is a
separate charged computation.  No field elements or input assignments are
enumerated by this compiler.
"""
from pathlib import Path
from fractions import Fraction
import json, sys, time
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/p) for p in ('work_matrix_root', 'work_multiprimary_audit',
    'work_norm_frontier_agent', 'work_norm_slice_agent', 'work_norm_glue_agent')]
from arbitrary_beta_zero_hall_aggregate import (acquire_local_aggregates,
    multiply_outside, arbitrary_beta_zero_count, add_scaled)
from arbitrary_operator_hall import (RefinedProfileFunctional, power_multiply,
    quotient_matrix)
from matrix_kloosterman import Field
from simple_operator_quadratic import matrix_source_anf
from krylov_square_source import quadratic_anf_sum


def square_root(value, F):
    result = value
    for _ in range(F.a-1): result = F.mul(result, result)
    return result


def trace_frequency(gamma, F):
    return sum(F.trace(F.mul(gamma, 1 << j)) << j for j in range(F.a))


def possible_characters(primary, F, eta):
    """Only acquired linear roots and resonant quadratic factors survive."""
    eta2 = F.mul(eta, eta); found = {}
    for i, item in enumerate(primary):
        f = item['irreducible']; degree = item['degree']
        if degree == 1:
            gamma = square_root(f[0], F) ^ F.mul(eta, f[0])
        elif degree == 2 and F.mul(eta2, f[1]) == 1:
            gamma = F.mul(eta, square_root(f[0], F))
        else: continue
        found.setdefault(gamma, []).append(i)
    return found


def even_points(local, functional, F, t, eta):
    polynomials = multiply_outside(local, ())
    scale = F.q ** (t*t+t*(t-1)//2); points = {}
    for epsilon, poly in enumerate(polynomials):
        for height, value in enumerate(functional.evaluate(poly)):
            point = eta if (height+epsilon) % 2 else 0
            points[point] = points.get(point, 0) + scale*value
    return {x: y for x, y in points.items() if y}, polynomials


def compile_beta_zero_fourier_response(D, field_h, eta=0, method='factorized'):
    """All-operator trace response; method='probes' is an exact reference.

    The factorized route multiplies local Hall/Gaussian polynomials in
    the explicit partition basis.  It computes neither a Cartesian tuple
    of primary quotient types nor the field's full trace histogram.
    """
    begun = time.perf_counter()
    if method not in ('factorized', 'probes'): raise ValueError('unknown reconstruction method')
    F, primary, local, characteristic = acquire_local_aggregates(D, field_h)
    if type(eta) is not int or not 0 <= eta < F.q: raise ValueError('field eta required')
    t = len(D); q = F.q; K = t*t+t*(t-1)//2
    functional = RefinedProfileFunctional(q, t)
    points, even_polys = even_points(local, functional, F, t, eta)
    candidates = possible_characters(primary, F, eta)
    terms = [dict(kind='point', argument=x, coefficient=c) for x, c in sorted(points.items())]
    records = []; gaussians = {}; probe_count = 0
    for gamma, active in sorted(candidates.items()):
        frequency = trace_frequency(gamma, F)
        point_character = sum(c*(-1 if F.trace(F.mul(gamma, x)) else 1)
                              for x, c in points.items())
        if method == 'probes':
            phi = tuple(1 << j for j in range(F.a) if (frequency >> j) & 1)
            raw = arbitrary_beta_zero_count(D, field_h, phi, eta)['gap']
            probe_count += 1
            coefficient = Fraction(raw-point_character, q)
            full_states = None
        else:
            # At a fixed character, every admissible primary is independent
            # after the exact cross-primary Sylvester integration.
            combined = {(): Fraction(1)}
            parity_sign = -1 if F.trace(F.mul(gamma, eta)) else 1
            for i, item in enumerate(local):
                polynomial = add_scaled(dict(item['even'][0]), item['even'][1], parity_sign)
                if i in active:
                    for leaf in item['odd']:
                        key = (i, tuple(leaf['rho']), gamma)
                        if key not in gaussians:
                            A = quotient_matrix([primary[i]], [leaf['rho']], F)
                            b = len(A)
                            phi = {1 << j for j in range(F.a) if (frequency >> j) & 1}
                            value = quadratic_anf_sum(matrix_source_anf(A, F, 0, phi, eta), F.a*b*b)
                            gaussians[key] = Fraction(value, q**(b*(b-1)//2))
                        polynomial = add_scaled(polynomial, leaf['flag'],
                            leaf['population']*gaussians[key])
                combined = power_multiply(combined, polynomial)
            # Exact-active-nonempty subtraction avoids counting even-only
            # quotient types once at every possible character.
            weighted_even = add_scaled(dict(even_polys[0]), even_polys[1], parity_sign)
            nonempty = add_scaled(combined, weighted_even, -1)
            values = functional.evaluate(nonempty)
            coefficient = q**(K-1)*sum(value*parity_sign**h for h, value in enumerate(values))
            full_states = len(combined)
        coefficient = Fraction(coefficient)
        if coefficient.denominator != 1: raise AssertionError('trace character coefficient is not integral')
        coefficient = coefficient.numerator
        if coefficient: terms.append(dict(kind='walsh', argument=frequency, coefficient=coefficient))
        records.append(dict(field_character=gamma, binary_frequency=frequency,
            admissible_odd_primary_indices=active, coefficient=coefficient,
            combined_partition_states=full_states))
    terms.sort(key=lambda item: (item['kind'], item['argument']))
    n = 3*F.a*t*t
    return dict(field_polynomial=field_h, field_degree=F.a, matrix_size=t,
        beta=0, eta=eta, rank_cap=t, padding=t, full_matrix_domain=True,
        original_independent_bits=n, counted_domain_size=1 << n,
        response=terms, remaining_walsh_terms=sum(x['kind']=='walsh' for x in terms),
        manufactured_point_terms=sum(x['kind']=='point' for x in terms),
        acquired_characteristic=characteristic, acquired_primary=primary,
        source_primary_decomposition_supplied=False, original_domain_preserved=True,
        auxiliary_independent_inputs=0, trace_program_anf_expanded=False,
        compiled_without_field_enumeration=True, enumerated_field_elements=0,
        candidate_characters=len(candidates), character_records=records,
        exact_full_counter_probes=probe_count, local_quadratic_gaussians=len(gaussians),
        explicit_partition_states=len(functional.power), reconstruction_method=method,
        response_term_bound=t+2, bit_time_bound='exp(O(sqrt(t)))*poly(a,t)',
        arbitrary_program_pairing_cost_included=False, seconds=time.perf_counter()-begun)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path); parser.add_argument('--output', type=Path)
    parser.add_argument('--method', choices=('factorized', 'probes'), default='factorized')
    args = parser.parse_args(); source = json.loads(args.source.read_text())
    result = compile_beta_zero_fourier_response(source['D'], source['h'], source.get('eta', 0), args.method)
    rendered = json.dumps(result, indent=2)+'\n'
    if args.output: args.output.write_text(rendered)
    else: print(rendered, end='')
