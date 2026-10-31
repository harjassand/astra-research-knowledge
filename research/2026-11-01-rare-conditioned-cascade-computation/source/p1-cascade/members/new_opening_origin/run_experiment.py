"""Reproduce count-only gauge learning, CP repair, and actual feedback planning."""
from __future__ import annotations
import json
import time
from itertools import product
from pathlib import Path
import numpy as np
from learner import learn, optimal_policy, policy_law, to_choi, from_choi
from source_fixture import acquire, SINGULAR_PREPARATIONS

ROOT = Path(__file__).resolve().parent


def serial(x):
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, (np.integer, np.floating)):
        return x.item()
    if isinstance(x, dict):
        return {k: serial(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [serial(v) for v in x]
    return x


def target_value(law):
    return sum(p for key, p in law.items() if key[-1][1] == 1)


def recovery_policy(actions, initial, horizon):
    """A monitored disturbance followed by an optimized conditional recovery.

    The task fixes X,D first, observes D's outcome, and permits `horizon`
    recovery calls before terminal M.  Optimization enumerates the full tree.
    """
    state = actions['X'][0] @ initial
    value, children, nodes = 0., [], 0
    for f in actions['D']:
        x = f @ state
        prob = float(x[0])
        nxt = x/prob if prob > 1e-13 else np.array([1.,0.,0.,0.])
        v, tree, n = optimal_policy(actions, nxt, horizon)
        value += prob*v
        children.append(tree); nodes += n
    return value, dict(action='X',children=[dict(action='D',children=children)]), nodes


def main():
    out = dict(scope='Synthetic aggregate counts, floating numerical diagnostic; not laboratory acquisition or interval-arithmetic proof.', runs=[])
    failed_data, failed_truth = acquire(1000000, preparations=SINGULAR_PREPARATIONS)
    try:
        learn(failed_data)
        failed_outcome = 'unexpected acceptance'
    except ValueError as exc:
        failed_outcome = str(exc)
    out['retained_failed_core'] = dict(preparations=SINGULAR_PREPARATIONS,
        n_per_slot=1000000, acquisition_bill=failed_data['bill'], outcome=failed_outcome,
        true_singular_values=np.linalg.svd(failed_truth['H'], compute_uv=False).tolist(),
        explanation='The four states z, Rx z, Ry z, Ry Rx z lie in an affine plane. The noisy numerical inverse did not establish a true core; the simultaneous inverse gate rejected it.')
    for n in [1000000, 100000000, 10000000000]:
        data, truth = acquire(n_per_slot=n)
        t0 = time.perf_counter()
        fitted = learn(data)
        elapsed = time.perf_counter() - t0
        horizon = 3
        total_calls = horizon + 3
        vfit, policy, visited = recovery_policy(fitted['actions'], fitted['initial'], horizon)
        p = policy_law(truth['actions'], truth['initial'], policy)
        q = policy_law(fitted['actions'], fitted['initial'], policy)
        tv = sum(abs(p.get(k, 0) - q.get(k, 0)) for k in p.keys() | q.keys()) / 2
        vbest, _, true_visited = recovery_policy(truth['actions'], truth['initial'], horizon)
        true_v = target_value(p)
        h = truth['H']
        true_c = {a: [np.linalg.solve(h, hz) for hz in hzs] for a, hzs in truth['shifted'].items()}
        max_band_violation = max(float(np.max(np.abs(c - cf) - e))
                                 for a, cs in true_c.items()
                                 for c, cf, e in zip(cs, fitted['C'][a], fitted['residual_bands'][a]))
        roundtrip = max(float(np.linalg.norm(from_choi(to_choi(f)) - f))
                        for fs in truth['actions'].values() for f in fs)
        branches = [(a,o,c) for a,cs in fitted['raw_C'].items() for o,c in enumerate(cs)]
        raw_min, raw_word = np.inf, None
        for word in product(range(len(branches)), repeat=3):
            state = np.eye(4)[:,0]
            for k in word:
                state = branches[k][2] @ state
            prob = float(sum(state))
            if prob < raw_min:
                raw_min, raw_word = prob, [(branches[k][0],branches[k][1]) for k in word]
        record = dict(n_per_slot=n, acquisition_bill=data['bill'], learner_seconds=elapsed,
                      core_condition=float(np.linalg.cond(h)), diagnostics=fitted['diagnostics'],
                      feedback=dict(recovery_horizon=horizon, forced_prefix=['X','D'], total_calls=total_calls,
                                    planner_state_visits=visited, evaluator_oracle_state_visits=true_visited,
                                    fitted_value=vfit, deployed_true_value=true_v, oracle_optimal_value=vbest,
                                    regret=vbest-true_v, full_transcript_TV=tv,
                                    uniform_TV_bound=min(1, fitted['diagnostics']['law']['b']*total_calls),
                                    policy_transfer_regret_bound=min(1, 2*fitted['diagnostics']['law']['b']*total_calls),
                                    policy=policy, terminal_records=len(p)),
                      checks=dict(choi_roundtrip_error=roundtrip,
                                  raw_signed_predictor_min_length_three_event=raw_min,
                                  raw_signed_predictor_min_word=raw_word,
                                  maximum_coordinate_band_violation=max_band_violation,
                                  true_law_sum=sum(p.values()), fitted_law_sum=sum(q.values()),
                                  true_min_probability=min(p.values()), fitted_min_probability=min(q.values())))
        out['runs'].append(record)
        if n == 100000000:
            (ROOT/'counts.json').write_text(json.dumps(serial(data), indent=2)+'\n')
            (ROOT/'fitted_model.json').write_text(json.dumps(serial({k:fitted[k] for k in ['actions','initial','S','C','diagnostics']}), indent=2)+'\n')
        if n == 10000000000:
            false_pure = learn(data,pure_anchor=True)
            out['retained_false_purity_attempt'] = dict(
                supplied_data='same mixed-source counts; no additional oracle calls',
                b=false_pure['diagnostics']['law']['b'],
                horizon_six_bound=min(1,6*false_pure['diagnostics']['law']['b']),
                explanation='Forcing the acquired start to be pure gives the wrong isotropic scale on this mixed-start source. The candidate remains CP but pays a nonvanishing model residual. The scalar search is necessary unless a pure-anchor premise is supplied.')
        print(json.dumps(serial(dict(n=n,bill=data['bill'],seconds=elapsed,
                                     b=fitted['diagnostics']['law']['b'], TV=tv,
                                     bound=record['feedback']['uniform_TV_bound'],
                                     fitted_value=vfit,deployed=true_v,optimal=vbest,
                                     regret=vbest-true_v,band_violation=max_band_violation,
                                     planner_visits=visited)), indent=2))
    (ROOT/'results.json').write_text(json.dumps(serial(out), indent=2)+'\n')


if __name__ == '__main__':
    main()
