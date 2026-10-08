#!/usr/bin/env python3
"""Exact Spin(15) r=0 check using the original seeds plus one attained state."""
from __future__ import annotations

from itertools import combinations
from pathlib import Path
import json
import sympy as sp

import r0_seed_cone_probe as base


def main():
    n = 7
    cert_path = Path(__file__).with_name('spin15_rational_seed_certificate.json')
    cert = json.loads(cert_path.read_text())
    vertices = [
        sp.Matrix([base.moment(n, h, k) for k in range(1, n + 1)])
        for h in range(n + 1)
    ]
    vertices.append(sp.Matrix([sp.Rational(x) for x in cert['grade_moments']]))
    cones = base.support_cones(vertices, n)
    rays = sorted(set().union(*(r for _, r in cones)))
    F = base.recoupling(n)
    Ds = [base.grade_diagonal(n, k) for k in range(1, n + 1)]
    trace = sp.Matrix([sp.binomial(2 * n + 1, k) for k in range(1, n + 1)])
    failures = []
    checks = 0
    minors = 0
    for ray in rays:
        alpha = sp.Matrix(ray)
        support_values = [v.dot(alpha) for v in vertices]
        support = max(support_values)
        winners = [j for j, x in enumerate(support_values) if x == support]
        bound = trace.dot(alpha) + support
        D = sum((alpha[k] * Ds[k] for k in range(n)), sp.zeros(n + 1))
        H = sp.simplify(D + F * D * F)
        gap = sp.simplify(bound * sp.eye(n + 1) - H)
        ok, checked, witness = base.psd_principal_minors(gap)
        checks += 1
        minors += checked
        if not ok:
            failures.append({
                'ray': list(ray),
                'winner_indices': winners,
                'seed_support': str(support),
                'trace': str(trace.dot(alpha)),
                'bound': str(bound),
                'witness': witness,
            })
    result = {
        'status': 'PASS_EXACT_R0_AUGMENTED_SEEDS' if not failures else 'FAIL_EXACT_R0_AUGMENTED_SEEDS',
        'n': n,
        'attained_seed_count': len(vertices),
        'support_cone_ray_counts': [len(r) for _, r in cones],
        'distinct_rays': len(rays),
        'ray_block_checks': checks,
        'principal_minor_checks': minors,
        'failures': failures,
        'scope': 'Exact r=0 block only; support lower bounded by nine explicitly attained pure spinors; no all-r or all-n claim.',
    }
    out = Path(__file__).with_name('r0_augmented_seed_check_n7.json')
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
