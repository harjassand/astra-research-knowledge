"""Exact facet certificate for a controlled two-species mass-action example.

This is a finite certificate for the displayed example.  Multiaffinity on
each box facet makes vertex checks sufficient; it is not evidence for the
general affine-minimum lemma or the Extended Permanence Conjecture.
"""

from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json


def coupled(a, b, k):
    # 0 <-> A+B and A <-> B; rates ordered by those four arrows.
    inflow, outflow, a_to_b, b_to_a = k
    common = inflow - outflow * a * b
    exchange = -a_to_b * a + b_to_a * b
    return common + exchange, common - exchange


def separate(a, b, k):
    # 0 <-> A and 0 <-> B.
    a_in, a_out, b_in, b_out = k
    return a_in - a_out * a, b_in - b_out * b


def exact_facet_checks():
    low, high = Q(1, 4), Q(4)
    controls = tuple(product((Q(1), Q(2)), repeat=4))
    report = {}
    total_checks = 0
    for name, field in (('coupled', coupled), ('separate', separate)):
        margins = {}
        for coordinate in (0, 1):
            for side, value, orientation in (
                ('lower', low, Q(1)), ('upper', high, Q(-1))
            ):
                checks = []
                for other in (low, high):
                    point = (value, other) if coordinate == 0 else (other, value)
                    for rates in controls:
                        inward = orientation * field(*point, rates)[coordinate]
                        assert inward > 0, (name, point, rates, inward)
                        checks.append(inward)
                        total_checks += 1
                margins[f'{coordinate}_{side}'] = str(min(checks))
        report[name] = margins
    return {
        'arithmetic': 'exact rational',
        'box': ['1/4', '4'],
        'active_rate_interval': ['1', '2'],
        'vertex_checks': total_checks,
        'minimum_inward_margin': '1/2',
        'facet_margins': report,
        'reason_vertices_suffice': (
            'Each facet field is affine separately in the free coordinate and '
            'each rate, so its extrema on the rectangle occur at vertices.'
        ),
        'scope': 'Displayed two-mode example only; no general theorem replay.',
    }


if __name__ == '__main__':
    report = exact_facet_checks()
    target = Path(__file__).with_name('switching_example_certificate.json')
    target.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
