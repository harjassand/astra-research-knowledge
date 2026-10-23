"""Exact small check of the derivative-critical harmonic secant bound."""
from fractions import Fraction as F
from pathlib import Path
import json
import time
from check_secant import mv, upper, up


def g(x):
    return x-F(3, 4)*x*x+F(1, 4)*x**3


start = time.perf_counter()
A = [[F(1, 2), F(1, 2), F(0)], [F(0), F(1, 3), F(2, 3)],
     [F(1, 4), F(0), F(3, 4)]]
x, scalar, cumulative = [F(1), F(0), F(0)], F(1), F(0)
steps = 8
for n in range(steps):
    bound = F(2, n+2)
    assert 0 < scalar <= bound
    assert all(0 <= v <= scalar for v in x)
    cumulative += scalar
    assert cumulative <= 2*sum((F(1, k) for k in range(2, n+3)), F(0))
    next_scalar = g(scalar)
    assert 1/next_scalar-1/scalar >= F(1, 2)
    scalar = next_scalar
    x = [F(1, 4)*v+F(1, 4)*upper(z) for v, z in zip(x, mv(A, x))]

# The rounded upper envelope is still valid, but is not itself harmonically decaying.
grid = F(1)
first_grid_harmonic_failure = None
for n in range(1, 513):
    grid = up(g(grid), 8)
    if grid > F(2, n+2) and first_grid_harmonic_failure is None:
        first_grid_harmonic_failure = n
assert first_grid_harmonic_failure is not None
assert up(g(grid), 8) == grid
result = {'exact_scalar_and_three_site_steps': steps,
          'reciprocal_increment_and_cumulative_bound_hold_exactly': True,
          'rounded_upper_endpoint_warning': {
              'fractional_grid_bits': 8,
              'first_n_exceeding_unrounded_harmonic_bound': first_grid_harmonic_failure,
              'n': 512, 'rounded_endpoint': str(grid),
              'unrounded_analytic_upper': str(F(2, 514)),
              'rounded_endpoint_is_fixed_point': True},
          'elapsed_seconds_observed': time.perf_counter()-start}
Path(__file__).with_name('secant_critical_results.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
