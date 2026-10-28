"""Independent bounded replay of coarse switching counts; no trajectories."""
from fractions import Fraction as F
from pathlib import Path
from math import factorial
import hashlib
import importlib.util
import json
from replay_multiboundary_review import check_endpoint

ROOT = Path(__file__).resolve().parents[2]
CODE = ROOT/'core/coarse_switching_cover.py'
RAW = ROOT/'results/COARSE_SWITCHING_RAW_RECEIPTS.json'
RESULT = ROOT/'results/COARSE_SWITCHING_COVER.json'


def confidence_endpoint(x, n, p, exponent, side):
    assert 0 <= p <= 1
    assert p <= F(x, n) if side == 'lower' else p >= F(x, n)
    check_endpoint(x, n, p, exponent, side)


def main():
    raw, result = (json.loads(p.read_text()) for p in (RAW, RESULT))
    pure, tapes = raw['repetitions'], raw['balanced_tapes']
    depth, n = tapes['depth'], tapes['trials']
    assert n == (1 << depth)*tapes['per_full_tape']
    counts = tapes['counts_by_prefix']
    assert set(counts) == {format(i, '0%db' % h) for h in range(1, depth+1) for i in range(1 << h)}
    assert len(counts) == (1 << (depth+1))-2
    by_depth = tapes['survivors_by_depth']
    assert len(by_depth) == depth+1 and by_depth[0] == n
    for word, r in counts.items():
        assert r['assigned_trials'] == n//(1 << len(word))
        assert 0 <= r['survived'] <= r['assigned_trials']
        if len(word) < depth:
            assert sum(counts[word+bit]['survived'] for bit in '01') <= r['survived']
    for h in range(1, depth+1):
        assert sum(r['survived'] for word, r in counts.items() if len(word) == h) == by_depth[h]
    assert tapes['primitive_applications'] == tapes['coarse_observations'] == sum(by_depth[:-1])
    assert tapes['fresh_preparations'] == n
    for r in pure:
        s = r['survivors_by_time']
        assert len(s) == r['cap']+1 and s[0] == r['trials']
        assert all(0 <= b <= a for a, b in zip(s, s[1:]))
        assert r['primitive_applications'] == r['coarse_observations'] == sum(s[:-1])
        assert r['fresh_preparations'] == r['trials']
    for key, total in result['complete_costs'].items():
        assert total == sum(r[key] for r in pure)+tapes[key]

    cover, target = result['cover'], F(result['cover']['all_word_error'])
    nodes = cover['nodes']
    assert '0' in nodes and '1' in nodes
    selected_endpoints = 0
    for word, node in nodes.items():
        record = counts[word]
        lo, hi = map(F, node['interval'])
        confidence_endpoint(record['survived'], record['assigned_trials'], lo, F(18), 'lower')
        confidence_endpoint(record['survived'], record['assigned_trials'], hi, F(18), 'upper')
        selected_endpoints += 2
        if len(word) > 1:
            assert nodes[word[:-1]]['kind'] == 'branch'
        if node['kind'] == 'terminal':
            assert F(node['prediction']) == 0 and F(node['all_extension_bound']) == hi <= target
            assert word+'0' not in nodes and word+'1' not in nodes
        else:
            assert node['kind'] == 'branch'
            assert word+'0' in nodes and word+'1' in nodes
            assert F(node['prediction']) == (lo+hi)/2
            assert F(node['error']) == (hi-lo)/2 <= target
            assert hi > target
    terminals = sum(x['kind'] == 'terminal' for x in nodes.values())
    branches = len(nodes)-terminals
    assert terminals == cover['terminal_nodes'] == branches+2
    assert branches == cover['branch_nodes']
    assert len(nodes) == cover['interval_count'] == 84
    assert max(map(len, nodes)) == cover['maximum_prefix_length'] == 7 <= depth
    assert cover['potential_interval_count'] == len(counts) == 2046

    spec = importlib.util.spec_from_file_location('reviewed_coarse_cover', CODE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    def forbidden(*args, **kwargs):
        raise AssertionError('Inference requested private source access')
    module.PrivateInstrument = module.hidden_check = module.fast_probability = forbidden
    isolated_cover = module.infer_cover({'depth': depth, 'counts_by_prefix': counts})
    assert isolated_cover == cover

    # Recompute every predeclared pure-curve upper endpoint and independently
    # verify it with the rational logarithm enclosure used above.
    candidates = []
    pure_endpoints = 0
    cap = min(r['cap'] for r in pure)
    for m in range(1, cap//2+1):
        uppers = []
        for r in pure:
            x = r['survivors_by_time'][2*m]
            upper = module.binomial_interval(x, r['trials'], F(12), upper_only=True)[1]
            confidence_endpoint(x, r['trials'], upper, F(12), 'upper')
            uppers.append(upper)
            pure_endpoints += 1
        s = max(uppers)
        if s < target:
            z, h = F(1), 0
            while z > target:
                z = s+F(m-1, m)*(z-s)
                h += 1
            candidates.append(dict(m=m, single_action_upper=str(s), half_length=h,
                all_switching_length=2*h, tail_bound=str(z)))
    tail = result['repetition_tail']
    assert candidates == tail['candidates']
    assert min(candidates, key=lambda x:(x['all_switching_length'], x['m'])) == tail['chosen']
    assert tail['one_sided_tails'] == pure_endpoints == 32
    assert tail['tail_exponent'] == 12 and cover['tail_exponent'] == 18
    def inverse_exp_upper(x):
        return 1/sum((F(x)**k/F(factorial(k)) for k in range(90)), F(0))
    failure = pure_endpoints*inverse_exp_upper(12)+2*len(counts)*inverse_exp_upper(18)
    assert failure < F(result['failure_probability_upper']) == F(1, 1000)
    out = dict(result_sha256=hashlib.sha256(RESULT.read_bytes()).hexdigest(),
        code_sha256=hashlib.sha256(CODE.read_bytes()).hexdigest(),
        raw_receipt_sha256=hashlib.sha256(RAW.read_bytes()).hexdigest(),
        selected_cover_confidence_endpoints_checked=selected_endpoints,
        pure_tail_confidence_endpoints_checked=pure_endpoints,
        potential_prefix_intervals=len(counts), selected_nodes=len(nodes),
        terminal_nodes=terminals, branch_nodes=branches,
        cover_completeness_and_unconditional_denominators_verified=True,
        isolated_inference_uses_only_observable_counts=True,
        paid_complete_costs=result['complete_costs'],
        union_failure_upper_diagnostic=float(failure),
        general_weak_poincare_lemma_review_scope='Separate scalar branch; only saved recurrence arithmetic checked here.',
        new_trajectories_generated=0, all_reviewed_checks_passed=True)
    path = Path(__file__).with_name('COARSE_SWITCHING_COVER_REVIEW_RESULTS.json')
    path.write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
