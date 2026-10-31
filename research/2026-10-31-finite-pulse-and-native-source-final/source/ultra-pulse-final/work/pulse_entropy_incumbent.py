#!/usr/bin/env python3
"""Stronger ordinary joint confidence-set KL incumbent, same frozen data.

The rectangle-only marginal baseline discards the simplex relation. This
ordinary convex tangent certificate keeps it. No sampling advantage is claimed.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'outputs/pulse_entropy'
sys.path.insert(0, str(ROOT/'work'))
from pulse_entropy import logs, down, linear_range, dual_witness


def vertices(box):
    found = set()
    for free in range(4):
        fixed = [j for j in range(4) if j != free]
        for sides in product((0, 1), repeat=3):
            p = [F(0)]*4
            for j, side in zip(fixed, sides):
                p[j] = box[j][side]
            p[free] = 1-sum(p)
            if box[free][0] <= p[free] <= box[free][1]:
                found.add(tuple(p))
    return sorted(found)


def KL_interval(r, s):
    low = high = F(0)
    for mass, reference in ((r, s), (1-r, 1-s)):
        if mass:
            lo, hi = logs(mass/reference)
            low += mass*lo
            high += mass*hi
    return low, high


def evaluate(saved, B):
    box = [tuple(map(F, row)) for row in saved['probability_box']]
    delta = linear_range([0, 1, -1, 0], box)
    if delta[0] <= 0 <= delta[1]:
        # Convexity and continuity imply a feasible law with r=s.
        return {'ordinary_joint_set_KL_rate_lower': '0', 'rate_preview': 0.0,
            'optimum_gap_upper': '0', 'global_minimum_certified': True,
            'reason': 'feasible simplex section intersects equal endpoint means',
            'vertices_evaluated': 0}
    best = F(0)
    primal_upper = None
    winning = None
    all_vertices = vertices(box)
    for p in all_vertices:
        r, s = p[2]+p[3], p[1]+p[3]
        assert 0 < r < 1 and 0 < s < 1
        # Ordinary supporting hyperplane of jointly convex binary KL.
        w = r*(1-s)/(s*(1-r))
        Z0 = (1-s)/(1-r)
        low, receipt = dual_witness(box, z=F(1), w=w, v=F(1), Z0=Z0)
        upper = KL_interval(r, s)[1]
        if primal_upper is None or upper < primal_upper:
            primal_upper = upper
        if low >= best:
            best, winning = low, receipt
    assert best <= primal_upper
    gap = primal_upper-best
    return {'ordinary_joint_set_KL_rate_lower': str(down(4*best/B)),
        'rate_preview': float(down(4*best/B)), 'optimum_gap_upper': str(gap),
        'optimum_gap_preview': float(gap), 'global_minimum_certified': gap < F(1, 2**80),
        'vertices_evaluated': len(all_vertices), 'supporting_hyperplane': winning,
        'method': 'jointly convex binary KL on same box/simplex; exact supporting tangent lower and feasible vertex upper',
        'new_physical_or_statistical_assumptions': False}


def main():
    start = time.perf_counter()
    protocol = json.loads((OUT/'PROTOCOL.json').read_text())
    B = F(protocol['B'])
    rows = []
    for source in ('driven', 'equilibrium'):
        saved = json.loads((OUT/(source+'_inference.json')).read_text())
        result = evaluate(saved, B)
        rows.append({'source': source, 'frozen_receiver_lower_preview': saved['rate_lower_preview'], **result})
    receipt = {'status': 'ORDINARY_JOINT_CONFIDENCE_SET_INCUMBENT_CERTIFIED',
        'same_records_clock_gate_confidence_box_and_risk': True,
        'extra_draws': 0, 'frozen_files_changed': False, 'records': rows,
        'claim': 'the original rectangle comparator is weaker; no algorithmic advantage over the ordinary coupled KL method',
        'CPU_wall_seconds': time.perf_counter()-start,
        'code_SHA256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT/'incumbent.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps({'status': receipt['status'], 'records': [{
        'source': x['source'], 'frozen_lower': x['frozen_receiver_lower_preview'],
        'ordinary_coupled_KL': x['rate_preview'], 'global_optimum_gap': x['optimum_gap_upper'],
        'vertices': x['vertices_evaluated']} for x in rows], 'seconds': receipt['CPU_wall_seconds']}, indent=2))


if __name__ == '__main__':
    main()
