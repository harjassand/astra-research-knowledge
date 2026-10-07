"""Exact Gaussian moment audit and rational sufficient-coefficient estimator.
Ideal Gaussian statistical risk is not a certified finite-bit digitizer.
"""
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
import math
import json
import time


def add(a, b):
    out = defaultdict(F, a)
    for k, v in b.items():
        out[k] += v
    return {k:v for k,v in out.items() if v}


def scale(a, c):
    return {k:F(c)*v for k,v in a.items() if c*v}


def multiply(a, b):
    out = defaultdict(F)
    for i, v in a.items():
        for j, w in b.items():
            out[tuple(x+y for x,y in zip(i,j))] += v*w
    return dict(out)


def gaussian_expectation(poly):
    ans = F(0)
    for exponents, c in poly.items():
        m = 1
        for k in exponents:
            if k % 2:
                m = 0
                break
            m *= math.prod(range(1, k, 2))
        ans += c*m
    return ans


def diagonal_risk_numerator(eigenvalues, noise_variance=F(1)):
    eig = list(map(F, eigenvalues))
    n = len(eig)
    zero = (0,)*n
    S = {}
    f = {zero:-sum(eig)}
    for i, val in enumerate(eig):
        k = tuple(2 if j == i else 0 for j in range(n))
        S[k] = F(1)
        f[k] = val
    Hnorm2 = add(add(multiply(S,S), scale(S,-2)), {zero:F(n)})
    f2 = multiply(f,f)
    energy = gaussian_expectation(multiply(f2,Hnorm2))
    noise = F(noise_variance)*gaussian_expectation(Hnorm2)
    norm2 = sum(x*x for x in eig)
    numerator = energy+noise-4*norm2
    formula = (2*n*n+18*n+28)*norm2+8*sum(eig)**2+F(noise_variance)*n*(n+1)
    assert numerator == formula
    return numerator


def rational_moment_estimate(samples):
    if not samples:
        raise ValueError('labeled observations required')
    n = len(samples[0][0])
    out = [[F(0) for _ in range(n)] for _ in range(n)]
    operations = 0
    for x, y in samples:
        x = list(map(F, x))
        y = F(y)
        if len(x) != n:
            raise ValueError('dimension mismatch')
        for i in range(n):
            for j in range(i, n):
                out[i][j] += y*(x[i]*x[j]-(i == j))
                operations += 4
    K = len(samples)
    for i in range(n):
        for j in range(i, n):
            out[i][j] /= 2*K
            out[j][i] = out[i][j]
            operations += 1
    return out, {'labeled_samples_read':K, 'feature_dimension':n,
                 'symmetric_coefficients_acquired':n*(n+1)//2,
                 'rational_operations':operations,
                 'max_output_fraction_bits':max(max(x.numerator.bit_length(),x.denominator.bit_length()) for row in out for x in row)}


def main():
    start = time.perf_counter()
    checks = []
    for n in range(1,9):
        for vals in [[F(1)]*n, [F((-1)**i,i+1) for i in range(n)],
                     [F(1)]+[F(0)]*(n-1)]:
            for noise in [F(0),F(1),F(3,2)]:
                num = diagonal_risk_numerator(vals,noise)
                checks.append({'n':n,'eigenvalues':list(map(str,vals)),
                               'noise_variance':str(noise),'four_K_times_MSE_exact':str(num)})
    samples = [([F(1),F(0)],F(1)),([F(0),F(2)],F(-1)),([F(1,2),F(-1,2)],F(3,4))]
    estimate, cost = rational_moment_estimate(samples)
    assert estimate == [[F(7,96),F(-1,32)],[F(-1,32),F(-73,96)]]
    out = Path(__file__).with_name('quadratic_inference_checks.json')
    result = {'exact_gaussian_polynomial_moment_checks':checks,
              'supplied_rational_label_estimator':{'estimate':[[str(x) for x in row] for row in estimate], 'cost':cost,
              'scope':'Actual arithmetic estimator on supplied observations; these fixtures are not sampled Gaussian observations and are not empirical capability evidence.'},
              'elapsed_seconds':time.perf_counter()-start,
              'statistical_model':'Ideal real Gaussian features and unit/known Gaussian label noise.',
              'precision_gate':'UNKNOWN Gaussian digitizer/sample acquisition; no finite-bit risk transfer claimed.',
              'harness_repair':'Initial hand-entered first fixture coefficient -1/96 was wrong; direct rational summation gives 7/96. Gaussian risk formula was unchanged and all 72 moment cases already passed.'}
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'exact_Gaussian_moment_cases':len(checks),'estimator_cost':cost,
                      'seconds':result['elapsed_seconds'],'output':str(out)}))

if __name__ == '__main__':
    main()
