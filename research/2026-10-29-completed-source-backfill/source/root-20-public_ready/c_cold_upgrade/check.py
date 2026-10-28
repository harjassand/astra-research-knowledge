"""Task C: exact-rational synthetic acquisition and independent analytic checks.

No physical source is queried. The learner's audit consumes only three report
centres plus the stipulated deterministic error and shape/cap contracts.
"""

from fractions import Fraction as F
from decimal import Decimal, localcontext
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
delta = F(1, 5)
x = (F(1, 50), F(1, 50))
h = (F(1, 100), F(1, 100))
epsilon = F(1, 10**8)
c = (F(1, 10), F(1, 20))
m = F(1)
L = (F(1), F(2))
B = (F(2), F(4))


def dec(q, digits=24):
    with localcontext() as ctx:
        ctx.prec = 70
        return format(Decimal(q.numerator) / Decimal(q.denominator), f'.{digits}f')


def scalar_source(u):
    # Synthetic source-only value, from diagonal Q in TASK_C.txt.
    return (1 + u[0]) / (1 + 2*u[0]) + (1 + u[1]) / (2 + 4*u[1])


def report_source(u):
    return F(3, 2) + 1 / scalar_source(u)


def reciprocal_interval(r):
    assert r - epsilon > F(3, 2)
    return (1 / (r + epsilon - F(3, 2)),
            1 / (r - epsilon - F(3, 2)))


def simplex_bound(point, lower, upper):
    zero = -sum(a*b for a, b in zip(point, lower))
    vertices = [(delta-point[j])*upper[j]
                - sum(point[i]*lower[i] for i in range(2) if i != j)
                for j in range(2)]
    return max([zero] + vertices), [zero] + vertices


def audit(reaction_intervals, curvature, prices):
    a0, b0 = reaction_intervals[0]
    lower, upper = [], []
    for i in range(2):
        ai, bi = reaction_intervals[i+1]
        lower.append((a0-bi)/h[i] - prices[i])
        upper.append((b0-ai)/h[i] - prices[i] + curvature[i]*h[i]/2)
    value, vertices = simplex_bound(x, lower, upper)
    return {'lower': lower, 'upper': upper, 'curvature': curvature,
            'regret_upper': value, 'vertex_bounds': vertices}


points = [x] + [tuple(x[j] + (h[i] if j == i else 0)
                       for j in range(2)) for i in range(2)]
assert all(min(u) >= 0 and sum(u) <= delta for u in points)
centres = [report_source(u) for u in points]
intervals = [reciprocal_interval(r) for r in centres]
assert all(a <= scalar_source(u) <= b
           for u, (a,b) in zip(points, intervals))

# Published source theorem: ||e||^2 = 2, supplied only for this fixture.
M_published = [2*(2*L[i]**2/m**3 + B[i]/m**2) for i in range(2)]

# Elementary new deduction from the source proof: on a convex-Z segment,
# Z(t) <= max(b0, bi), and ||Q^-1 e||^2 <= Z/m.
M_observed = [(2*L[i]**2/m**2 + B[i]/m)
              * max(intervals[0][1], intervals[i+1][1]) for i in range(2)]

published = audit(intervals, M_published, c)
observed = audit(intervals, M_observed, c)


def true_gradient(u):
    # Independent verifier, not consumed by either learner audit.
    return (1/(1+2*u[0])**2-c[0],
            1/(2*(1+2*u[1])**2)-c[1])


true_g = true_gradient(x)
true_tangent, _ = simplex_bound(x, true_g, true_g)
for result in (published, observed):
    assert all(result['lower'][i] <= true_g[i] <= result['upper'][i]
               for i in range(2))
    assert result['regret_upper'] >= true_tangent >= 0


def objective_without_offset(u):
    return -scalar_source(u)-sum(c[i]*u[i] for i in range(2))


# Verify actual synthetic regret in an exact rational bracket. Both partial
# derivatives stay positive on [0,delta]^2, so an optimum uses the full dose.
# Along that edge the derivative is strictly decreasing, with opposite signs
# at the two endpoints. Rational bisection locates its unique zero.
def edge_derivative(t):
    g = true_gradient((t, delta-t))
    return g[0]-g[1]


lo, hi = F(0), delta
assert edge_derivative(lo) > 0 > edge_derivative(hi)
for _ in range(120):
    mid = (lo+hi)/2
    if edge_derivative(mid) > 0:
        lo = mid
    else:
        hi = mid
y = ((lo+hi)/2, delta-(lo+hi)/2)
actual_regret_lower = objective_without_offset(y)-objective_without_offset(x)
y_g = true_gradient(y)
residual, _ = simplex_bound(y, y_g, y_g)
actual_regret_upper = actual_regret_lower + residual
assert actual_regret_upper <= observed['regret_upper']
assert actual_regret_upper-actual_regret_lower < F(1,10**34)

# Repricing requires no new centres for a fixed audited x. Check the exact
# shift relation on a different price vector as a software sanity check.
c_prime = (F(1,4), F(1,10))
repriced = audit(intervals, M_published, c_prime)
assert all(repriced['lower'][i] == published['lower'][i]+c[i]-c_prime[i]
           and repriced['upper'][i] == published['upper'][i]+c[i]-c_prime[i]
           for i in range(2))

# A C2 monotone alternative preserving all three acquired reports while
# violating Loewner concavity: add 2*(u1-.03)_+^3 to Q's first diagonal.
# On [0,.2], its extra derivative is 6*(u1-.03)_+^2 and extra second
# derivative is 12*(u1-.03)_+. The analytic cap proof is in REPORT.md.
tau = F(3,100)
assert all(u[0] <= tau for u in points)
alternative_second_at_delta = -2/(1+delta)**3 + 12*(delta-tau)
assert alternative_second_at_delta == F(2383,2700) > 0


def serialize(v):
    if isinstance(v, F):
        return {'exact': str(v), 'decimal': dec(v)}
    if isinstance(v, dict):
        return {k:serialize(a) for k,a in v.items()}
    if isinstance(v,(tuple,list)):
        return [serialize(a) for a in v]
    return v


results = {
    'kind': 'synthetic exact-rational calculation; no physical acquisition',
    'input': {'delta':delta,'x':x,'h':h,'epsilon':epsilon,'prices':c},
    'points':points,'report_centres':centres,'Z_intervals':intervals,
    'published_audit':published,'dimension_free_audit':observed,
    'verifier_only':{'true_gradient_at_x':true_g,
                     'true_gradient_tangent_upper':true_tangent,
                     'maximizer_candidate':y,
                     'actual_regret_lower':actual_regret_lower,
                     'actual_regret_upper':actual_regret_upper,
                     'optimality_residual':residual},
    'repricing_check':{'new_prices':c_prime,'audit':repriced},
    'alternative_nonconcave_second_at_delta':alternative_second_at_delta,
    'checks':'all exact assertions passed',
}
(OUT/'results.json').write_text(json.dumps(serialize(results),indent=2)+'\n')
print('Three exact scalar centres:')
for u,r,interval in zip(points,centres,intervals):
    print(tuple(map(str,u)),str(r),dec(r), 'Z:',*[dec(q) for q in interval])
for name, result in [('Published',published),('Dimension-free',observed)]:
    print(name,'M',*[dec(v) for v in result['curvature']])
    print(name,'lower',*[dec(v) for v in result['lower']])
    print(name,'upper',*[dec(v) for v in result['upper']])
    print(name,'vertex bounds',*[dec(v) for v in result['vertex_bounds']])
    print(name,'regret upper',dec(result['regret_upper']))
print('Verifier true gradient',*[dec(v) for v in true_g])
print('Verifier tangent upper',dec(true_tangent))
print('Actual-regret bracket',dec(actual_regret_lower,40),dec(actual_regret_upper,40))
print('Synthetic optimum candidate',*[dec(v) for v in y])
print('Repriced published bound',dec(repriced['regret_upper']))
print('All exact assertions passed.')
