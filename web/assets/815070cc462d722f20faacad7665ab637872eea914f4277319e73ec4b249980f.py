#!/usr/bin/env python3
"""Exact mathematical negative controls, separate from corrupt-file controls."""
from fractions import Fraction as Q
from math import factorial
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json


def exp_sum(x, degree):
    return sum((x**j / factorial(j) for j in range(degree + 1)), Q(0))


def main():
    # Loosening the vertical lemma from c<=2S to merely c<=2 is false.
    # log u <= u-1 bounds the logarithm from above. All hyperbolic acquisition
    # uses independent exact positive Taylor terms and a geometric remainder.
    C, c, t = Q(1, 4), Q(7, 4), Q(1, 100)
    z = c * t
    cosh_lower = sum((z**j / factorial(j) for j in range(0, 9, 2)), Q(0))
    cosh_upper = cosh_lower + z**10 / factorial(10) / (1 - z**2 / (11 * 12))
    sinh_lower = z + z**3 / 6
    Q_upper = ((1 + t**2) * cosh_upper - 2 * t * sinh_lower + (1 - t**2) * (2 * C - 1)) / 2
    F_upper = Q_upper / C - 1 + c * t**2 / 2
    assert 2 * (1 - C) < c < 2 and F_upper < 0
    # Actual full Gibbs state, not only a limiting symmetric-sector law.
    # N2 alpha4 delta3/2 has unnormalized smallest PT eigenvalue
    # exp(4)[exp(-3/4)-1/2]+1/2.
    assert exp_sum(Q(3, 4), 4) > Q(40, 19)
    assert exp_sum(Q(4), 6) > 48
    PT_upper = -Q(48, 40) + Q(1, 2)
    assert PT_upper < 0
    result = {
        'status': 'PASS exact negative controls rejected false stronger scopes',
        'utc': datetime.now(timezone.utc).isoformat(),
        'source_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'vertical_false_scope': {
            'C': str(C), 'c': str(c), 't': str(t), 'z': str(z),
            'Q_upper': str(Q_upper), 'F_upper': str(F_upper),
            'violation': 'c<=2 alone does not imply the correlated-edge lemma; c<=2S is load-bearing'},
        'actual_Gibbs_false_scope': {
            'N': 2, 'alpha': '4', 'delta': '3/2', 'h': '0',
            'unnormalized_minimum_PT_eigenvalue_upper': str(PT_upper),
            'violation': 'unrestricted axial delta is false, already at finite alpha4 and N2'},
    }
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'vertical_F_upper_negative': F_upper < 0,
                      'actual_Gibbs_PT_upper': str(PT_upper)}))


if __name__ == '__main__':
    main()
