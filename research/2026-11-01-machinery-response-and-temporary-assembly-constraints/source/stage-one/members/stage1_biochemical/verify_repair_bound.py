#!/usr/bin/env python3
"""Verify finite blind-repair formulas against state/reward ODEs.

All parameter cases are illustrative dimensionless choices, not fitted ribosome
measurements. This checks the exact accounting derivation in the addendum.
"""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import solve_ivp

def phi(rate, time):
    return -np.expm1(-rate*time)/rate if rate else time

cases = [(1, .01, 1, .99, .5, 50), (1, .1, .3, 1, .7, 50),
         (.1, .1, 5, .8, .2, 12), (0, .1, 0, 1, 0, 12)]
results = []
for lam, delta, u, rho, s, time in cases:
    mu = rho*s*u
    q = (1-rho)*u
    k = lam+mu
    active = ((mu*phi(delta+q, time)+lam*phi(delta+q+k, time))/k
              if k else phi(delta+q, time))
    attempts = u*phi(q, time)
    def rhs(t, state):
        a, d, irreparable, work, count = state
        return [-(lam+delta+q)*a+mu*d,
                lam*a-(mu+delta+q)*d,
                delta*(a+d)-q*irreparable,
                a, u*(a+d+irreparable)]
    solution = solve_ivp(rhs, (0, time), [1, 0, 0, 0, 0],
                         rtol=1e-10, atol=1e-12).y[:, -1]
    assert np.isclose(solution[3], active, rtol=1e-8, atol=1e-9)
    assert np.isclose(solution[4], attempts, rtol=1e-8, atol=1e-9)
    results.append({'lambda': lam, 'delta': delta, 'u': u, 'rho': rho,
                    's': s, 'time': time, 'active_time': float(active),
                    'attempt_count': float(attempts),
                    'ODE_active_time_error': float(solution[3]-active),
                    'ODE_attempt_count_error': float(solution[4]-attempts)})
report = {'interpretation': 'Illustrative mathematical checks, not experimental claims.',
          'cases': results}
output = Path(__file__).resolve().parent / 'repair_bound_check.json'
output.write_text(json.dumps(report, indent=2)+'\n')
print('Verified 4 finite-horizon cases, including perfect retention and no repair.')
