#!/usr/bin/env python3
"""Certified stationary product-event probabilities by renewal rewards.

All large-state operations are acquired local heat contractions. Only the
k-channel tree cofactors use dense linear algebra. No Abel extrapolation,
stationary oracle, trajectory simulation, or full-state enumeration is used.
The present implementation needs a positive statewise total-hazard floor.
"""
from __future__ import annotations

from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import time
import resource
import secrets
from contextlib import contextmanager
import certified_solver as cs


def determinant(a: list[list[F]]) -> F:
    a = [r[:] for r in a]
    det = F(1)
    for i in range(len(a)):
        pivot = next((j for j in range(i, len(a)) if a[j][i]), None)
        if pivot is None:
            return F(0)
        if pivot != i:
            a[pivot], a[i] = a[i], a[pivot]
            det = -det
        p = a[i][i]
        det *= p
        for j in range(i + 1, len(a)):
            factor = a[j][i] / p
            for k in range(i + 1, len(a)):
                a[j][k] -= factor * a[i][k]
    return det


def tree_weights(p: list[list[F]]) -> list[F]:
    k = len(p)
    lap = [[(sum(p[i][j] for j in range(k) if j != i)
             if i == l else -p[i][l]) for l in range(k)] for i in range(k)]
    weights = []
    for root in range(k):
        indices = [i for i in range(k) if i != root]
        weights.append(determinant([[lap[i][j] for j in indices] for i in indices]))
    if any(x <= 0 for x in weights):
        raise ArithmeticError("positive channel tree weights were not resolved")
    return weights


def stationary_intervals(model: cs.ResetModel, masks: list, accuracy: F,
                         *, max_attempts: int | None = 8) -> tuple[list, dict]:
    model.validate()
    if any(not any(x > 0 for pair in channel for x in pair) for channel in model.hazards):
        raise ValueError("remove inactive reset channels before using this implementation")
    if not 0 < accuracy < 1:
        raise ValueError("accuracy must be between zero and one")
    floor = sum(min(pair) for pair in model.local_total_hazards)
    if floor <= 0:
        raise ValueError("this implementation needs positive statewise total hazard")
    whole = tuple((True, True) for _ in range(model.n))
    all_masks = [*masks, whole]
    delta_bits = max(64, cs.ceil_log2(1 / accuracy) + 32 + 2 * model.n)
    attempt = 0
    while max_attempts is None or attempt < max_attempts:
        attempt += 1
        precision = max(224, delta_bits + 96)
        cs.set_interval_precision(precision)
        try:
            finite, norms = cs.integrate_product_contractions(
                model, all_masks, F(0), delta_bits, spectral_floor=floor)
        except ArithmeticError:
            delta_bits += 32
            continue
        delta = finite['delta']
        # For symmetric local killed generators, scalar relative quadrature
        # error delta gives operator error at most delta/floor.
        def entry(iv, left_norm, right_norm):
            center, radius = cs.scalar_interval_data(iv, delta * left_norm * right_norm / floor)
            return center, radius
        pdata = [[entry(finite['M'][l][j], norms['law_norms'][l+1], norms['hazard_norms'][j])
                  for j in range(model.k)] for l in range(model.k)]
        p = [[v[0] for v in row] for row in pdata]
        if any(p[i][j] <= 0 for i in range(model.k) for j in range(model.k) if i != j):
            delta_bits += 32
            continue
        theta = max((pdata[i][j][1] / p[i][j] for i in range(model.k)
                     for j in range(model.k) if i != j), default=F(0))
        if theta >= F(1, 2) or any(p[i][j] <= 0 for i in range(model.k)
                                    for j in range(model.k) if i != j):
            delta_bits += 32
            continue
        tw = tree_weights(p)
        # Both true and center cofactor weights are positive sums of products
        # of k-1 off-diagonal transition entries. Thus this relative enclosure
        # has no subtraction-sensitive determinant error assumption.
        low_tree = (1 - theta) ** (model.k - 1)
        high_tree = (1 + theta) ** (model.k - 1)
        rewards = []
        for gi in range(len(all_masks)):
            lo = hi = F(0)
            for l in range(model.k):
                center, radius = entry(finite['v'][l][gi], norms['law_norms'][l+1],
                                       norms['event_norms'][gi])
                lo += tw[l] * max(F(0), center - radius)
                hi += tw[l] * (center + radius)
            rewards.append((low_tree * lo, high_tree * hi))
        den_lo, den_hi = rewards[-1]
        if den_lo <= 0:
            delta_bits += 32
            continue
        intervals = []
        out_bits = cs.ceil_log2(8 / accuracy)
        for lo, hi in rewards[:-1]:
            lower, upper = lo / den_hi, hi / den_lo
            intervals.append(cs.outward_dyadic_interval((lower+upper)/2, (upper-lower)/2, out_bits))
        if all(hi-lo <= accuracy for lo, hi in intervals):
            return intervals, {'method':'renewal rewards and positive tree-weight intervals',
                'spectral_floor':cs.frac(floor), 'quadrature_delta_bits':delta_bits,
                'internal_precision_bits':precision, 'positive_nodes':finite['node_count'],
                'tree_relative_entry_error':cs.frac(theta),
                'requested_width':cs.frac(accuracy), 'attempts':attempt,
                'product_states_enumerated':False}
        delta_bits += 32
    raise ArithmeticError("precision adaptation limit reached")


@contextmanager
def uncapped_arithmetic():
    """Remove deliberate numeric work caps, not machine/resource limitations.

    The core uses module globals and is intentionally single-threaded.
    """
    old = cs.MAX_PRECISION_BITS, cs.MAX_NODES
    cs.MAX_PRECISION_BITS = None
    cs.MAX_NODES = None
    try:
        yield
    finally:
        cs.MAX_PRECISION_BITS, cs.MAX_NODES = old


def exact_sample(model: cs.ResetModel, randbit=None) -> dict:
    """Uncapped lazy sampler for this supported rational model class.

    Exact distribution is a mathematical guarantee under independent fair
    bits. The default is a cryptographic software source, not a certified
    source of physically ideal randomness. No level or precision cap exists.
    """
    if randbit is None:
        randbit = lambda: secrets.randbits(1)
    prefix = []
    decisions = []
    with uncapped_arithmetic():
        for coordinate in range(model.n):
            u = level = 0
            masks = [cs.event_mask_for_prefix(tuple(prefix), model.n, b) for b in (0, 1)]
            while True:
                level += 1
                bit = randbit()
                if bit not in (0, 1):
                    raise ValueError("randbit must return zero or one")
                u = 2*u + bit
                # Resolve child masses adaptively. This avoids using a tiny
                # global point-mass lower bound to overresolve every query.
                width = F(1, 1 << (level + 4))
                while True:
                    children, detail = stationary_intervals(model, masks, width, max_attempts=None)
                    try:
                        threshold = cs.ratio_interval(children[0], children[1])
                    except ArithmeticError:
                        width /= 4
                        continue
                    if threshold[1] - threshold[0] <= F(1, 1 << (level + 1)):
                        break
                    width /= 4
                ulo, uhi = F(u, 1 << level), F(u+1, 1 << level)
                if uhi <= threshold[0]:
                    selected = 0
                elif ulo >= threshold[1]:
                    selected = 1
                else:
                    continue
                prefix.append(selected)
                decisions.append({'coordinate':coordinate, 'uniform_bits':format(u, f'0{level}b'),
                    'uniform_interval':[cs.frac(ulo), cs.frac(uhi)],
                    'conditional_zero_interval':list(map(cs.frac, threshold)),
                    'selected':selected, 'oracle':detail})
                break
    return {'sample':prefix, 'decisions':decisions,
        'implementation_caps':'none on lazy levels, nodes, precision or adaptation',
        'randomness_contract':'independent ideal fair bits; default software source is secrets.randbits'}


def large_fixture(n: int) -> cs.ResetModel:
    # Heterogeneous rates and reset laws: no count-lumping symmetry.
    return cs.ResetModel(
        up=tuple(F(i+2, 3*i+7) for i in range(n)),
        down=tuple(F(2*i+3, 4*i+9) for i in range(n)),
        hazards=(tuple((F(i+1, 8*n*(i+2)), F(3*i+5, 8*n*(i+2))) for i in range(n)),
                 tuple((F(2*i+3, 8*n*(i+2)), F(i+1, 8*n*(i+2))) for i in range(n))),
        reset_one=(tuple(F(i+1, 4*i+7) for i in range(n)),
                   tuple(F(3*i+5, 4*i+7) for i in range(n))),
        initial_one=tuple(F(1, 2) for _ in range(n)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=3)
    parser.add_argument('--bits', type=int, default=24)
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('regenerative_receipt.json'))
    args = parser.parse_args()
    model = cs.make_fixture() if args.n == 3 else large_fixture(args.n)
    mask = cs.event_mask_for_prefix(tuple([1]*args.n), args.n)
    start = time.monotonic()
    intervals, detail = stationary_intervals(model, [mask], F(1, 1 << args.bits))
    lo, hi = intervals[0]
    receipt = {'status':'interval_enclosed_stationary_cylinder', 'n':args.n, 'k':model.k,
        'implicit_state_count':str(1 << args.n), 'event':'all coordinates equal one',
        'lower':cs.frac(lo), 'upper':cs.frac(hi), 'width':cs.frac(hi-lo),
        'elapsed_seconds':time.monotonic()-start,
        'max_rss_raw':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'max_rss_units':'bytes on macOS, kilobytes on Linux', 'details':detail,
        'input':{'up':[cs.frac(x) for x in model.up], 'down':[cs.frac(x) for x in model.down],
                 'hazards':[[[cs.frac(x) for x in pair] for pair in channel] for channel in model.hazards],
                 'reset_one':[[cs.frac(x) for x in row] for row in model.reset_one]},
        'scope':'Internal arithmetic and analytic enclosure; no independent proof validation or historical originality claim'}
    args.output.write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps({key:receipt[key] for key in ('status','n','lower','upper','width','elapsed_seconds','details')}, indent=2))


if __name__ == '__main__':
    main()
