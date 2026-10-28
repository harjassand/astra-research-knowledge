"""Exact replay of adaptive fresh batches and queue; no source trajectories."""
from collections import deque
from fractions import Fraction as F
from pathlib import Path
import hashlib
import importlib.util
import json
import sys
from replay_multiboundary_review import logs

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT/'results/ADAPTIVE_COARSE_RAW_RECEIPTS.json'
RESULT = ROOT/'results/ADAPTIVE_COARSE_COVER.json'
CODE = ROOT/'core/adaptive_coarse_cover.py'


def main():
    receipts, saved = (json.loads(p.read_text()) for p in (RAW, RESULT))
    epsilon, delta = F(1, 16), F(1, 1000)
    queue, nodes = deque(['0', '1']), {}
    budgets = []
    totals = dict(primitive_applications=0, coarse_observations=0, fresh_preparations=0)
    for j, r in enumerate(receipts, 1):
        assert queue and queue.popleft() == r['word']
        n = r['trials']
        # Independent 40-term rational logarithm enclosure. It verifies both
        # the needed paid lower bound and the exact ceiling for this receipt.
        loglo, loghi = logs(2*j*(j+1)/delta)
        multiplier = 2/epsilon**2
        assert F(n-1) < multiplier*loglo <= multiplier*loghi <= F(n)
        budgets.append(dict(index=j, trials=n, tail_allowance=str(delta/F(j*(j+1))),
                            exact_log_ceiling_verified=True))
        live = r['survivors_by_depth']
        assert len(live) == len(r['word'])+1 and live[0] == n and live[-1] == r['survived']
        assert all(0 <= b <= a for a, b in zip(live, live[1:]))
        steps = sum(live[:-1])
        assert r['primitive_applications'] == r['coarse_observations'] == steps
        assert r['fresh_preparations'] == n
        for key in totals:
            totals[key] += r[key]
        center, radius = F(r['survived'], n), epsilon/2
        lo, hi = max(F(0), center-radius), min(F(1), center+radius)
        terminal = hi <= 2*epsilon
        prediction = hi/2 if terminal else (lo+hi)/2
        error = hi/2 if terminal else (hi-lo)/2
        assert error <= epsilon
        assert r['word'] not in nodes
        nodes[r['word']] = dict(kind='terminal' if terminal else 'branch',
            interval=[str(lo), str(hi)], prediction=str(prediction), error_bound=str(error))
        if not terminal:
            queue.extend([r['word']+'0', r['word']+'1'])
    assert not queue
    cover = saved['cover']
    assert nodes == cover['nodes']
    terminals = sum(x['kind'] == 'terminal' for x in nodes.values())
    branches = len(nodes)-terminals
    assert terminals == cover['terminal_nodes'] == branches+2
    assert branches == cover['branch_nodes']
    assert max(map(len, nodes)) == cover['maximum_prefix_length'] == 5
    assert len(nodes) == len(receipts) == 38
    for word, node in nodes.items():
        if node['kind'] == 'branch':
            assert word+'0' in nodes and word+'1' in nodes
        else:
            assert word+'0' not in nodes and word+'1' not in nodes
    assert totals == saved['complete_costs']
    assert F(cover['all_word_absolute_error']) == epsilon
    assert F(cover['failure_probability_upper']) == delta
    assert saved['uses_prior_receipts'] is False and saved['uses_lifetime_pilot'] is False
    # This checks inference only; source creation and queries are disabled.
    sys.path.insert(0, str(ROOT/'core'))
    spec = importlib.util.spec_from_file_location('reviewed_adaptive_coarse', CODE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    def forbidden(*args, **kwargs):
        raise AssertionError('Inference requested source access')
    module.PrivateInstrument = module.fast_probability = module.hidden_check = module.query = forbidden
    assert module.infer(receipts) == cover
    out = dict(result_sha256=hashlib.sha256(RESULT.read_bytes()).hexdigest(),
        raw_receipt_sha256=hashlib.sha256(RAW.read_bytes()).hexdigest(),
        code_sha256=hashlib.sha256(CODE.read_bytes()).hexdigest(),
        adaptive_batches_verified=len(receipts), exact_batch_log_ceilings=budgets,
        queue_complete=True, terminal_nodes=terminals, branch_nodes=branches,
        complete_costs=totals, source_disabled_inference_reproduced=True,
        confidence_basis='Conditional fresh-batch Hoeffding, with deterministic summable delta/[j(j+1)] allocation over all possible j.',
        accepted_midpoint_terminal_theorem_reaudited=False,
        new_trajectories_generated=0, all_reviewed_checks_passed=True)
    path = Path(__file__).with_name('ADAPTIVE_COARSE_COVER_REVIEW_RESULTS.json')
    path.write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k:v for k, v in out.items() if k != 'exact_batch_log_ceilings'}, indent=2))


if __name__ == '__main__':
    main()
