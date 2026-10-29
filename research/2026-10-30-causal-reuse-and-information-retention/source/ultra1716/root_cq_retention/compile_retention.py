"""Exact support/retention and finite violating-prior compiler.

Input matrices use [real rational string, imaginary rational string].
No optimizer, logarithms, sampled references or physical channel calls.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys
import time
import sympy as sp


def rat(value):
    value = F(value)
    return sp.Rational(value.numerator, value.denominator)


def parse(rows):
    return sp.Matrix([[rat(x[0])+sp.I*rat(x[1]) for x in row] for row in rows])


def real(value):
    value = sp.expand_complex(value)
    assert sp.im(value) == 0
    return sp.re(value)


def psd(matrix):
    assert matrix == matrix.conjugate().T
    residual = matrix.copy()
    pivots = []
    for j in range(matrix.rows):
        pivot = real(residual[j, j])
        assert pivot >= 0
        pivots.append(pivot)
        if pivot == 0:
            assert all(residual[j, k] == 0 for k in range(j+1, matrix.rows))
            continue
        for k in range(j+1, matrix.rows):
            for ell in range(j+1, matrix.rows):
                residual[k, ell] = sp.cancel(residual[k, ell]
                    -residual[k, j]*residual[j, ell]/pivot)
    return pivots


def kernel_projector(matrix):
    vectors = matrix.nullspace()
    if not vectors:
        return sp.zeros(matrix.rows)
    basis = sp.Matrix.hstack(*vectors)
    result = basis*(basis.conjugate().T*basis).inv()*basis.conjugate().T
    assert result*result == result and matrix*result == sp.zeros(matrix.rows)
    return result


def floor_positive(matrix):
    pk = kernel_projector(matrix)
    inverse = (matrix+pk).inv()-pk
    return min(sp.Rational(1), 1/real(sp.trace(inverse)))


def encode(matrix):
    return [[[str(sp.re(x)), str(sp.im(x))] for x in row]
            for row in matrix.tolist()]


def main():
    start = time.perf_counter()
    path = Path(sys.argv[1]).resolve()
    raw = path.read_bytes()
    data = json.loads(raw)
    states = [parse(x) for x in data['states']]
    n, d = len(states), states[0].rows
    assert n >= 2 and all(x.shape == (d, d) for x in states)
    for state in states:
        psd(state)
        assert sp.trace(state) == 1
    total = sum(states, sp.zeros(d))
    common = kernel_projector(total)
    projectors = [kernel_projector(total-x)-common for x in states]
    weights = [real(sp.trace(x*p)) for x, p in zip(states, projectors)]
    for i, p in enumerate(projectors):
        assert p == p.conjugate().T and p*p == p
        assert all(p*state == sp.zeros(d) for j, state in enumerate(states) if i != j)
    assert all(0 <= x <= 1 for x in weights)
    rmin = min(weights)
    checks = 0
    if rmin > 0:
        extraction = [p/r for p, r in zip(projectors, weights)]
        for i in range(n):
            for j in range(n):
                assert real(sp.trace(extraction[i]*states[j])) == int(i == j)
                for k in range(n):
                    expected = 1/weights[j] if i == j == k else 0
                    assert sp.trace(extraction[i]*states[j]*extraction[k]) == expected
                    assert sp.trace(extraction[i]*extraction[k]*states[j]) == expected
                    checks += 2
    witness = None
    if 'reject_reverse_factor' in data:
        c = rat(data['reject_reverse_factor'])
        assert c >= 0 and c*rmin < 1
        i = weights.index(rmin)
        omega = (total-states[i])/(n-1)
        a, b = floor_positive(states[i]+omega), floor_positive(omega)
        bound = 8/(a*b)
        h = 0
        while sp.Integer(2)**h < bound:
            h += 1
        threshold = c*h/(1-c*rmin)
        k = max(h, int(sp.floor(threshold))+1)
        assert k >= h and k*(1-c*rmin) > c*h
        witness = {'input_label': i, 'factor': str(c), 'a': str(a), 'b': str(b),
                   'h': h, 'dyadic_exponent_k': k,
                   'recipe': 'p=e_i; q_i=2^-k; q_j=(1-2^-k)/(n-1)',
                   'strict_divergence_violation_proved_without_logs': True,
                   'denominator_bit_cost_at_least': k}
        if k <= 4096:
            epsilon = sp.Rational(1, 2**k)
            witness['q_exact'] = [str(epsilon if j == i else (1-epsilon)/(n-1))
                                  for j in range(n)]
        else:
            witness['q_exact'] = 'NOT_MATERIALIZED; exact dyadic recipe above'
    result = {'status': 'EXACT_CQ_CONDITIONAL_RETENTION_AND_REJECTION',
              'input_sha256': hashlib.sha256(raw).hexdigest(),
              'labels': n, 'output_dimension': d,
              'private_weights': [str(x) for x in weights],
              'sharp_retention': str(rmin),
              'sharp_reverse_factor': str(1/rmin) if rmin else 'INFINITE',
              'kernel_projectors': [encode(x) for x in projectors],
              'exact_left_right_extraction_entries': checks,
              'finite_rejection_witness': witness,
              'matrix_logs_or_roots_or_solver_calls': 0,
              'quantum_reference_or_channel_samples': 0,
              'seconds_after_imports': time.perf_counter()-start}
    out = path.with_name(path.stem+'_RESULT.json')
    out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'kernel_projectors'}, indent=2))


if __name__ == '__main__':
    main()
