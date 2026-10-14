"""Independent exact planning check; no specimen, data, or physical validation.

This file does not execute the incoming scientific checker. It constructs
matrix exponentials by a signed Taylor series and an induced-norm tail bound.
The variance-sensitive confidence budget requires a separately valid variance
upper bound; here that bound is computed for the supplied mathematical ring.
"""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

OUT = Path(__file__).resolve().parent


def matrix_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def add_interval(a, b):
    return a[0] + b[0], a[1] + b[1]


def mul_interval(a, b):
    values = [x*y for x in a for y in b]
    return min(values), max(values)


def scale_interval(a, c):
    return mul_interval(a, (c, c))


def sum_intervals(values):
    result = F(0), F(0)
    for value in values:
        result = add_interval(result, value)
    return result


def transition(q, t, terms=12):
    """Every entry enclosure follows from ||tail||_infinity <= tail_bound."""
    n = len(q)
    qt = [[x*t for x in row] for row in q]
    norm = max(sum(abs(x) for x in row) for row in qt)
    assert norm < 1
    eye = [[F(i == j) for j in range(n)] for i in range(n)]
    power = eye
    partial = [[F(i == j) for j in range(n)] for i in range(n)]
    for k in range(1, terms+1):
        power = matrix_mul(power, qt)
        partial = [[partial[i][j]+power[i][j]/factorial(k)
                    for j in range(n)] for i in range(n)]
    tail = norm**(terms+1) / factorial(terms+1) / (1-norm/F(terms+2))
    return [[(max(F(0), x-tail), min(F(1), x+tail)) for x in row]
            for row in partial], tail


def ceil_fraction(x):
    return -((-x.numerator)//x.denominator)


def display(value):
    if isinstance(value, tuple):
        return {'lo':str(value[0]), 'hi':str(value[1]),
                'lo_float':float(value[0]), 'hi_float':float(value[1])}
    return {'exact':str(value), 'float':float(value)}


qrate = F(1,20)
q = [[-(1+qrate),F(1),qrate],
     [qrate,-(1+qrate),F(1)],
     [F(1),qrate,-(1+qrate)]]
pi = [F(1,3)]*3
b = [0,1,1]
t = F(1,1000)
r = F(39991,40000)
p, tail = transition(q,t)

# The detector is the source's deterministic B={1,2} labeling.
prob = {}
for left in (0,1):
    for middle in (0,1):
        for right in (0,1):
            prob[left,middle,right] = sum_intervals(
                scale_interval(mul_interval(p[i][j],p[j][k]),pi[i])
                for i in range(3) for j in range(3) for k in range(3)
                if (b[i],b[j],b[k]) == (left,middle,right))

mean = sum_intervals(scale_interval(pr,F(y)*(F(x)-r)*(F(z)-r))
                     for (x,y,z),pr in prob.items())
second = sum_intervals(scale_interval(pr,(F(y)*(F(x)-r)*(F(z)-r))**2)
                       for (x,y,z),pr in prob.items())
d = -mean[1], -mean[0]
assert d[0] > 0
variance_upper = second[1]  # Var W <= E W^2, an exact conservative bound.
width = max(r,1-r)
delta = d[0]/2

# log(20)<3, proved without a floating log: a lower partial sum for e^3 exceeds20.
assert sum(F(3)**k/factorial(k) for k in range(9)) > 20
ell = F(3)
bernstein_n = ceil_fraction(2*ell*(variance_upper+width*delta/3)/delta**2)
hoeffding_n = ceil_fraction(ell*width**2/(2*delta**2))
assert F(bernstein_n)*delta**2 >= 2*ell*(variance_upper+width*delta/3)
assert F(hoeffding_n)*2*delta**2 >= ell*width**2

incoming=OUT/'late_pr87_sources/SMALL_GAP_EXTENSION_v0001.json'
fixture=json.loads(incoming.read_text())
source_lo=F(fixture['D']['lower_decimal'])
source_hi=F(fixture['D']['upper_decimal'])
assert d[0] <= source_lo <= source_hi <= d[1]

result={
 'created_at_utc':datetime.now(timezone.utc).isoformat(),
 'status':'PASS',
 'source_pr':87,
 'source_head':'a69ae39e8a23cc4d5b337bfa01ef2bd5ccbb7a0c',
 'method':'Independent rational signed-matrix Taylor enclosure, 12 terms, induced infinity norm tail.',
 'gap':str(t),'r':str(r),'transition_tail_bound':display(tail),
 'mean_score':display(mean),'D':display(d),'second_moment':display(second),
 'known_variance_upper':display(variance_upper),
 'confidence_radius_target':display(delta),
 'log_inverse_alpha_upper':'3 > log(20)',
 'iid_bernstein_sufficient_radius_budget':bernstein_n,
 'iid_hoeffding_sufficient_radius_budget_with_same_log_upper':hoeffding_n,
 'budget_ratio_hoeffding_over_bernstein':float(F(hoeffding_n,bernstein_n)),
 'source_hoeffding_budget':fixture['iid_windows_for_half_expected_margin_at_alpha_0_05_planning_only'],
 'scope':'Known-variance planning calculation for the supplied exact generator. No variance calibration, independent stationary physical trials, timing, parity, readout, or practical superiority acquired. Both budgets concern a confidence radius equal to half the exact expected margin; they are not necessary sample lower bounds.',
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
(OUT/'LATE_PR87_ACQUISITION_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','D','second_moment',
 'iid_bernstein_sufficient_radius_budget',
 'iid_hoeffding_sufficient_radius_budget_with_same_log_upper',
 'budget_ratio_hoeffding_over_bernstein']},indent=2))
