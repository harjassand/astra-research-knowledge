#!/usr/bin/env python3
"""Exact conservative one-trace acquisition budgets on the same source."""
from fractions import Fraction as Q
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "outputs/reversible_currents"))
from currents import log_bounds
from dual_trace import load_certificate


def sufficient(n, delta, R, C, boundary, log_upper=Q(369, 100)):
    # n delta-boundary >= C sqrt(2 n ell)+R sqrt((2n-1)ell).
    # Isolate and square with both sign checks; all decisions are rational.
    A = n*delta-boundary
    x2, y2 = C*C*2*n*log_upper, R*R*(2*n-1)*log_upper
    gap = A*A-x2-y2
    return A >= 0 and gap >= 0 and gap*gap >= 4*x2*y2


def main():
    cert = load_certificate(ROOT/'outputs/reversible_currents/symmetric_dual.json')
    assert log_bounds(Q(40))[1] < Q(369, 100)
    # Exact binary-complement averaging gives this pair-product expression.
    for wi, w in enumerate(cert['words']):
        k0 = 1 if w[0] == w[1] else -1
        k1 = 1 if w[1] == w[2] else -1
        expected = Q(1, 128)-Q(3, 1184)*(k0+k1)+Q(1, 8)*k0*k1
        assert expected == cert['H'][wi]
    rows = []
    for name, delta, R, C, boundary in [
        ('frozen_symmetrized_predictive_dual', Q(3,128), cert['R'], cert['C'], cert['R']/2),
        ('ordinary_reflection', Q(1,4), Q(2), Q(2), Q(0)),
    ]:
        for n in range(1, 20001):
            if sufficient(n, delta, R, C, boundary):
                break
        else:
            raise RuntimeError('budget search cap reached')
        rows.append({'method': name, 'windows': n, 'transitions': n+1,
            'observed_bits': n+2, 'stationary_preparations': 1,
            'delta': str(delta), 'range': str(R), 'C': str(C),
            'boundary': str(boundary), 'log_upper': '369/100',
            'type_I_risk_at_most': '1/40', 'type_II_risk_at_most': '1/40',
            'proof': 'D9/D10 plus conditional iid-driving-sign bounded differences',
            'minimality': 'first integer satisfying this sufficient inequality only'})
    result = {'contract': 'one consecutive stationary source trace; no resets or mixing bound',
        'source': 'four-state b=1/2 construction; synthetic mathematical control',
        'rows': rows,
        'current_control': {'transitions': 88, 'observed_bits': 89,
            'power_exact': 'see reversible_current_power.json'},
        'sampling_advantage_for_predictive_dual_on_this_control': False,
        'alternative_power_derivation':
            'Hsym=1/128-(3/1184)(k_t+k_t+1)+(1/8)k_t*k_t+1; '
            'k_t=(-1)^t q0 eta_t, eta iid mean 1/2. Conditional mean=-3n/128 '
            'for either q0; endpoint influences <=R, interior <=2R; '
            'sum squared influences=(4n-2)R^2. McDiarmid upper tail '
            'exp(-2u^2/((4n-2)R^2)). Ordinary reflection uses the same '
            'driving signs and influence calculation, R=2.'}
    target=ROOT/'work/reversible_dual_budget.json'
    target.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
