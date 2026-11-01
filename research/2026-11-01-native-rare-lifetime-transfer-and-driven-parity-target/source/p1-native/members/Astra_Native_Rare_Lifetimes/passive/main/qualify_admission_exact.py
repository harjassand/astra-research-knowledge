"""Exact arithmetic postprocessing of the all-rate native fixture.

This removes floating inversion from the data-to-rate-box calculation. It does
not turn the seeded floating-time source simulation into a physical experiment
or a formally exact realization of ideal continuous clocks.
"""
from fractions import Fraction as F
from pathlib import Path
import json


def reference():
    q = [[F(0) for _ in range(16)] for _ in range(16)]
    alpha = [F(3, 5), F(4, 5), F(7, 10)]
    for x in range(16):
        for i in range(4):
            q[x][x ^ (1 << i)] += F(1, 2)
        for i in range(3):
            code = (x >> i) & 3
            nxt = ([1, 3, 2, 0] if i % 2 == 0 else [3, 0, 2, 1])[code]
            if nxt != code:
                q[x][x ^ ((code ^ nxt) << i)] += alpha[i]
    return q


def main():
    here = Path(__file__).resolve().parent
    raw = json.loads((here.parent/'computation/native_rate_counts.json').read_text())
    q = reference()
    eta, threshold = F(1, 25), F(12)
    minima = []
    checked_edges = set()
    for cell in raw['cells']:
        n = F(cell['count'])
        r = F(cell['exposure'])
        assert r == 100000
        states = [x for x in range(16) if x & cell['context_mask'] == cell['context_value']]
        rates = {q[x][x ^ cell['mask']] for x in states}
        assert len(rates) == 1
        qref = rates.pop()
        assert qref > 0
        assert abs(F(str(cell['reference_rate']))-qref) < F(1, 10**12)
        lower_mu, upper_mu = (1-eta)*qref*r, (1+eta)*qref*r
        assert lower_mu < n < upper_mu
        # For D(N,mu)=N log(N/mu)-N+mu, integration of D''=1/N
        # proves D >= (N-mu)^2/(2 max(N,mu)). Entirely rational.
        margins = [(n-mu)**2/(2*max(n, mu)) for mu in (lower_mu, upper_mu)]
        assert min(margins) > threshold
        minima.extend(margins)
        for x in states:
            checked_edges.add((x, x ^ cell['mask']))
    expected_edges = {(x,y) for x in range(16) for y in range(16) if q[x][y] > 0}
    assert checked_edges == expected_edges
    # Positive Taylor terms give a LOWER bound on exp(12).
    term = F(1)
    exp_lower = term
    for k in range(1, 81):
        term *= threshold/k
        exp_lower += term
    fail_upper = 2*len(raw['cells'])/exp_lower
    assert fail_upper < F(1, 2500)
    out = dict(all_checks_passed=True, rate_box=str(eta), cells=len(raw['cells']),
               all_supported_global_edges_covered=len(expected_edges),
               exposure_quota=100000,
               deviance_threshold=str(threshold),
               smallest_exact_deviance_lower_bound=str(min(minima)),
               simultaneous_failure_upper_rational=str(fail_upper),
               simultaneous_failure_upper_decimal=float(fail_upper),
               confidence_strictly_greater_than='2499/2500 = 0.9996',
               reference_primitive_rates={'flips':'1/2','cycles':['3/5','4/5','7/10']},
               status='Exact arithmetic implication for ideal count/exposure data; source fixture remains a numerical simulation.')
    (here/'exact_native_admission.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='simultaneous_failure_upper_rational'}, indent=2))


if __name__ == '__main__':
    main()
