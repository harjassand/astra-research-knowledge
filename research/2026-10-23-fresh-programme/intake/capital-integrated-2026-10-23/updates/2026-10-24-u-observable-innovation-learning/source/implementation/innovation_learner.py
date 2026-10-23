"""Learner-only innovation fit: no evaluator parameters, latent data or goals.

The exact confidence statement concerns the six moments, not the numerical
point fit. The point fit is a constrained weighted moment least-squares fit;
the denominator-aware intervals and contraction certificate are analytic.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np

HERE = Path(__file__).resolve().parent


def maps_and_jac(theta):
    s, l0, l1 = theta
    ls = np.array([l0, l1])
    values = [s*l0, s*l1]
    jac = [[l0, s, 0.0], [l1, 0.0, s]]
    for a in range(2):
        for b in range(2):
            values.append(s*ls[a]*ls[b])
            row = [ls[a]*ls[b], 0.0, 0.0]
            row[a+1] += s*ls[b]
            row[b+1] += s*ls[a]
            jac.append(row)
    return np.array(values), np.array(jac)


def point_fit(means, counts):
    # This solver has no statistical coverage role; C is kept separately.
    ref = int(np.argmax(np.abs(means[:2])))
    den = means[ref]
    if abs(den) > 1e-10:
        ls = np.array([means[2+2*a+ref]/den for a in range(2)])
        ls = np.clip(ls, -0.999, 0.999)
        s0 = np.clip(means[ref]/ls[ref], 0.001, 0.999) if abs(ls[ref]) > 1e-8 else 0.5
    else:
        ls, s0 = np.zeros(2), 0.5
    starts = [np.r_[s0, ls], np.array([0.25, 0.5, -0.5]),
              np.array([0.75, 0.8, -0.3]), np.array([0.75, -0.5, 0.5])]
    weights = counts / max(1, int(np.max(counts)))
    best = None
    diagnostics = []
    for start in starts:
        theta = start.copy()
        damping = 1e-5
        iterations = 0
        for iterations in range(100):
            prediction, jac = maps_and_jac(theta)
            residual = prediction - means
            loss = float(np.dot(weights, residual**2))
            step = np.linalg.solve(jac.T @ (weights[:, None]*jac) + damping*np.eye(3),
                                   jac.T @ (weights*residual))
            accepted = False
            for power in range(16):
                trial = np.clip(theta-step*(0.5**power), [0, -1, -1], [1, 1, 1])
                trial_loss = float(np.dot(weights, (maps_and_jac(trial)[0]-means)**2))
                if trial_loss <= loss:
                    accepted = True
                    break
            if not accepted:
                break
            movement = float(np.max(np.abs(trial-theta)))
            theta = trial
            if movement < 1e-11:
                break
        loss = float(np.dot(weights, (maps_and_jac(theta)[0]-means)**2))
        diagnostics.append({'start': start.tolist(), 'iterations': iterations+1,
                            'weighted_squared_loss': loss})
        if best is None or loss < best[0]:
            best = (loss, theta.copy())
    return best[1], diagnostics


def fit(actions, obs, seed=0, delta=0.05):
    del seed  # Deterministic, declared starts above.
    started = time.perf_counter()
    actions = np.asarray(actions, dtype=np.int8)
    obs = np.asarray(obs, dtype=np.int8)
    assert len(obs) == len(actions)+1
    assert set(np.unique(actions)).issubset({0, 1})
    assert set(np.unique(obs)).issubset({-1, 1})
    blocks = len(actions)//3
    t = 3*np.arange(blocks)
    products = [obs[t]*obs[t+1], obs[t]*obs[t+2]]
    masks = [actions[t] == a for a in range(2)]
    masks += [(actions[t] == a) & (actions[t+1] == b)
              for a in range(2) for b in range(2)]
    counts = np.array([int(mask.sum()) for mask in masks])
    sums = np.array([int(products[0 if j < 2 else 1][mask].sum())
                     for j, mask in enumerate(masks)])
    means = np.divide(sums, counts, out=np.zeros(6), where=counts > 0)
    radii = np.array([min(2.0, math.sqrt(2*math.log(12/delta)/n)) if n else 2.0
                      for n in counts])
    theta, diagnostics = point_fit(means, counts)
    intervals = []
    reference_intervals = []
    for a in range(2):
        lo, hi = -1.0, 1.0
        details = []
        for b in range(2):
            if abs(means[b]) > 0:
                center = means[2+2*a+b]/means[b]
                radius = (radii[2+2*a+b]+radii[b])/abs(means[b])
                lo, hi = max(lo, center-radius), min(hi, center+radius)
                details.append({'reference': b, 'center': float(center),
                                'radius': float(radius),
                                'reference_abs_lower': float(max(0, abs(means[b])-radii[b]))})
        intervals.append([float(lo), float(hi)])
        reference_intervals.append(details)
    # Conservative interval propagation using c_b^2 / c_bb, not a clipped
    # estimate mistaken for certainty. Intersect valid bounds across b.
    s_lo, s_hi = 0.0, 1.0
    for b in range(2):
        cabs_lo = max(0.0, abs(means[b])-radii[b])
        cabs_hi = min(1.0, abs(means[b])+radii[b])
        d_lo = max(0.0, means[2+3*b]-radii[2+3*b])
        d_hi = min(1.0, means[2+3*b]+radii[2+3*b])
        if d_hi > 0:
            s_lo = max(s_lo, cabs_lo**2/d_hi)
        if d_lo > 0:
            s_hi = min(s_hi, cabs_hi**2/d_lo)
    s_lo, s_hi = max(0.0, s_lo), min(1.0, s_hi)
    interval_outer_set_nonempty = (all(lo <= hi for lo,hi in intervals)
                                  and s_lo <= s_hi)
    # Nonempty OUTER intervals do not prove that the full semialgebraic C is
    # nonempty. A point-fit witness can prove numerical plausibility only;
    # an empty analytic intersection does decisively disable certification.
    abs_upper = [max(abs(lo), abs(hi)) for lo, hi in intervals]
    washout_action = int(np.argmin(abs_upper))
    washout_bound = abs_upper[washout_action]
    zeta = 1e-4
    if not interval_outer_set_nonempty:
        washout_steps = None
    elif washout_bound == 0:
        washout_steps = 1
    elif washout_bound < 1:
        washout_steps = max(1, 1+math.ceil(math.log(zeta/math.atanh(washout_bound)) /
                                         math.log(washout_bound)))
    else:
        washout_steps = None
    result = {
        'estimator': 'independent-block constrained moment fit',
        'eta': float(math.sqrt(theta[0])),
        'lambdas': theta[1:].tolist(), 'initial_prior_plus': 0.5,
        'initial_prior_status': 'unknown; filter forgets it after acquired washout',
        'fit_transitions': len(actions), 'fit_observations': len(obs),
        'block_count': blocks, 'used_feature_observations': 3*blocks,
        'charged_bridge_transitions': blocks,
        'unused_final_observation_count': len(obs)-3*blocks,
        'delta': delta, 'feature_order': ['c0', 'c1', 'c00', 'c01', 'c10', 'c11'],
        'counts': counts.tolist(), 'sums': sums.tolist(),
        'means': means.tolist(), 'radii': radii.tolist(),
        'lambda_intervals': intervals, 'eta_squared_interval': [s_lo, s_hi],
        'eta_interval': [math.sqrt(max(0,s_lo)), math.sqrt(max(0,s_hi))],
        'reference_intervals': reference_intervals,
        'confidence_object': 'exact six-moment semialgebraic constraints; point fit not coverage',
        'outer_intervals_nonempty': bool(interval_outer_set_nonempty),
        'point_fit_satisfies_all_moment_constraints': bool(np.all(
            np.abs(maps_and_jac(theta)[0]-means) <= radii)),
        'empty_intersection_policy': 'disable certificate; report misspecification or coverage failure',
        'washout': {'action': washout_action, 'abs_lambda_upper': washout_bound,
                    'initial_prior_tv_target': zeta, 'steps': washout_steps,
                    'bound_type': 'observed-filter initial-prior forgetting, per parameter in C'},
        'point_fit_starts': diagnostics,
        'runtime_seconds': time.perf_counter()-started,
        'raw_fit_sha256': hashlib.sha256(actions.tobytes()+obs.tobytes()).hexdigest(),
        'model_float_storage_bytes': int(theta.nbytes+means.nbytes+radii.nbytes+counts.nbytes+sums.nbytes),
        'retained_raw_storage_bytes': int(actions.nbytes+obs.nbytes),
    }
    return result


def main():
    public = HERE / 'learning_public_stream.npz'
    data = np.load(public)
    n = int(data['train_length'])
    result = fit(data['actions'][:n], data['obs'][:n+1])
    result['public_npz_sha256'] = hashlib.sha256(public.read_bytes()).hexdigest()
    (HERE / 'learning_innovation_fit.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in (
        'eta', 'lambdas', 'lambda_intervals', 'eta_interval', 'washout',
        'runtime_seconds')}))


if __name__ == '__main__':
    main()
