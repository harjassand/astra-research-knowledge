"""Nontracial pure-singlet fusion receiver: actual finite-history diagnostic.

The state is the complete input-reference/source/receiver Choi state, in
SU(2) multiplicity blocks. No conditional traciality, bath purifier, bath
preparation key, or source feedback is used. The adaptive choice maximizes
the Petz recovery fidelity for the *joint* source/receiver channel. That
choice is computed from the known model, not by measuring the hidden state.

This is an implemented receiver class, not a proof of target performance.
"""
import argparse
from functools import lru_cache
import json
import math
from pathlib import Path
import sys
import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'online'))
import adaptive_fusion as af


def insert_bit(bits, bit, k, position):
    """Insert bit into k-1-bit integer at position counted from the left."""
    shift = k - position - 1
    lower = bits & ((1 << shift) - 1)
    upper = bits >> shift
    return (upper << (shift + 1)) | (bit << shift) | lower


def trace_external(blocks, twj, k, position):
    """Exact partial trace of one exterior spin-1/2, retaining spin J."""
    result = {}
    for twl in af.total_labels(twj, k - 1):
        physical = np.zeros((2**(k-1), 2**(k-1)), complex)
        for bit, magnetic in [(0, 1), (1, -1)]:
            old = af.density_slice(blocks, twj, k, twl + magnetic)
            indices = [insert_bit(bits, bit, k, position)
                       for bits in range(2**(k-1))]
            physical += old[np.ix_(indices, indices)]
        basis = af.coupled_basis(twj, k-1, twl, twl)
        result[twl] = basis.conj().T @ physical @ basis
    return result


def lift_external_identity(blocks, twj, k, position):
    """Insert the unnormalized identity on an exterior spin-1/2."""
    result = {}
    for twl in af.total_labels(twj, k):
        physical = np.zeros((2**k, 2**k), complex)
        for bit, magnetic in [(0, 1), (1, -1)]:
            old = af.density_slice(blocks, twj, k-1, twl-magnetic)
            indices = [insert_bit(bits, bit, k, position)
                       for bits in range(2**(k-1))]
            physical[np.ix_(indices, indices)] = old
        basis = af.coupled_basis(twj, k, twl, twl)
        result[twl] = basis.conj().T @ physical @ basis
    return result


def petz_fidelity(blocks, twj, k=3):
    """Probability-weighted Fe for arbitrary (possibly unnormalized) Choi."""
    marginal = trace_external(blocks, twj, k, 0)
    inverse = {}
    for twl, matrix in marginal.items():
        vals, vecs = np.linalg.eigh((matrix + matrix.conj().T)/2)
        cutoff = max(float(vals[-1]), 1e-300) * 1e-11
        factors = np.zeros_like(vals)
        factors[vals > cutoff] = 1 / np.sqrt(vals[vals > cutoff])
        inverse[twl] = (vecs * factors) @ vecs.conj().T
    lifted = lift_external_identity(inverse, twj, k, 0)
    fidelity = 0.0
    for twl, rho in blocks.items():
        product = rho @ lifted[twl]
        fidelity += (twl + 1) * np.trace(product @ product).real / 2
    return float(fidelity)


def pure_initial_state():
    """Singlet reference/source tensor singlet receiver/spin-1/2."""
    singlet = np.array([0, 1, -1, 0], complex) / math.sqrt(2)
    rho = np.kron(np.outer(singlet, singlet.conj()),
                  np.outer(singlet, singlet.conj()))
    blocks = {}
    for twl in af.total_labels(1, 3):
        basis = af.coupled_basis(1, 3, twl, twl)
        physical = np.zeros((8, 8), complex)
        valid = []
        for bits in range(8):
            mq = twl - af.magnetization(bits, 3)
            valid.append(2*bits + (1-mq)//2 if abs(mq) <= 1 else None)
        for row in range(8):
            for col in range(8):
                if valid[row] is not None and valid[col] is not None:
                    physical[row, col] = rho[valid[row], valid[col]]
        blocks[twl] = basis.conj().T @ physical @ basis
    return blocks


def angle_direction(angles):
    polar, azimuth = angles
    return np.array([math.sin(polar)*math.cos(azimuth),
                     math.sin(polar)*math.sin(azimuth), math.cos(polar)])


def direction_angles(direction):
    return np.array([math.acos(np.clip(direction[2], -1, 1)),
                     math.atan2(direction[1], direction[0])])


def optimize_direction(incoming, twj, previous=None, restarts=2, target='joint'):
    if twj == 0:
        return np.array([0., 0., 1.]), af.branches(incoming, twj, np.array([0., 0., 1.]))

    def evaluate(direction):
        outcomes = af.branches(incoming, twj, direction)
        value = 0.0
        for jp, state, probability in outcomes.values():
            if target == 'joint':
                value += probability * petz_fidelity(state, jp)
            elif target == 'acquired':
                value += probability * petz_fidelity(trace_external(state, jp, 3, 1), jp, 2)
            else:
                raise ValueError(target)
        return value, outcomes

    candidates = [np.array([0., 0., 1.]), np.array([0., 0., -1.]),
                  np.array([1., 0., 0.]), np.array([0., 1., 0.])]
    if previous is not None:
        candidates.insert(0, previous)
    # An exact quadratic optimizer for the unweighted objective is another
    # deterministic start, not a restriction on the weighted optimization.
    candidates.append(af.optimal_direction(incoming, twj)[0])
    scored = [(evaluate(n)[0], n) for n in candidates]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    best_value, best_direction = scored[0]

    def objective(angles):
        return -evaluate(angle_direction(angles))[0]

    for _, start in scored[:restarts]:
        result = minimize(objective, direction_angles(start), method='Nelder-Mead',
                          options={'xatol': 2e-5, 'fatol': 1e-10, 'maxiter': 100})
        if -result.fun > best_value:
            best_value = float(-result.fun)
            best_direction = angle_direction(result.x)
    return best_direction, evaluate(best_direction)[1]


def dense_output(blocks, twj):
    """Small-spin diagnostic only: invariant reference/receiver/spin state."""
    k = 2
    dim = 4 * (twj+1)
    rho = np.zeros((dim, dim), complex)
    for twm in range(-twj-k, twj+k+1, 2):
        sl = af.density_slice(blocks, twj, k, twm)
        for row in range(4):
            mr = twm - af.magnetization(row, k)
            if abs(mr) > twj:
                continue
            ir = row*(twj+1) + (twj-mr)//2
            for col in range(4):
                mc = twm - af.magnetization(col, k)
                if abs(mc) <= twj:
                    ic = col*(twj+1) + (twj-mc)//2
                    rho[ir, ic] = sl[row, col]
    # Input-reference was time-reversed. Undo that for the readout utility.
    y = np.array([[0, -1j], [1j, 0]], complex)
    transform = np.kron(y, np.eye(2*(twj+1)))
    return transform @ rho @ transform.conj().T


def trajectory(theta, n, seed=1729, restarts=2, target='joint', log_every=0,
               first_upper=False):
    rng = np.random.default_rng(seed)
    state = pure_initial_state()
    twj = 1
    previous = None
    initial_fe = petz_fidelity(state, twj)
    assert abs(initial_fe-1) < 1e-9, initial_fe
    assert abs(petz_fidelity(trace_external(state, twj, 3, 1), twj, 2)-.25) < 1e-9
    records = []
    checkpoints = {1, 2, 3, 5, 10, 20, 50, 100, 200, 500, 1000, n}
    max_spin = .5
    total_expected_loss = 0.0
    for step in range(1, n+1):
        before = petz_fidelity(state, twj)
        incoming = af.append_and_collide(state, twj, theta)
        appended = petz_fidelity(incoming, twj, 4)
        assert abs(before-appended) < 2e-8, (before, appended)
        if step == 1 and first_upper:
            direction = np.array([math.sqrt(3)/2, 0., .5])
            outcomes = af.branches(incoming, twj, direction)
        else:
            direction, outcomes = optimize_direction(incoming, twj, previous, restarts, target)
        assert abs(sum(x[2] for x in outcomes.values())-1) < 1e-8
        after_expected = sum(p*petz_fidelity(b, j) for j, b, p in outcomes.values())
        assert after_expected <= before+1e-8, (before, after_expected)
        total_expected_loss += before-after_expected
        signs = list(outcomes)
        probabilities = np.array([outcomes[s][2] for s in signs])
        probabilities /= probabilities.sum()
        sign = signs[int(rng.choice(len(signs), p=probabilities))]
        twj, state, probability = outcomes[sign]
        previous = direction
        max_spin = max(max_spin, twj/2)
        if step in checkpoints or (log_every and step % log_every == 0):
            output = trace_external(state, twj, 3, 1)
            record = {'step': step, 'spin': twj/2,
                      'joint_petz_fidelity': petz_fidelity(state, twj),
                      'acquired_petz_fidelity': petz_fidelity(output, twj, 2),
                      'sum_expected_loss': total_expected_loss,
                      'last_probability': probability,
                      'direction': direction.tolist()}
            if twj <= 100:
                from covariant_spin_readout import optimal_readout
                record['optimal_acquired_fidelity'] = optimal_readout(dense_output(output, twj), twj/2)['optimal_entanglement_fidelity']
            records.append(record)
            print(json.dumps(record), flush=True)
    return {'status': 'actual pure-singlet nontracial receiver diagnostic; no performance theorem',
            'theta': theta, 'N': n, 'seed': seed, 'restarts': restarts,
            'objective': target, 'first_upper': first_upper,
            'max_spin': max_spin, 'records': records}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--theta', type=float, default=.3)
    parser.add_argument('--n', type=int, default=100)
    parser.add_argument('--seed', type=int, default=1729)
    parser.add_argument('--restarts', type=int, default=2)
    parser.add_argument('--objective', choices=['joint', 'acquired'], default='joint')
    parser.add_argument('--log-every', type=int, default=0)
    parser.add_argument('--first-upper', action='store_true')
    args = parser.parse_args()
    result = trajectory(args.theta, args.n, args.seed, args.restarts, args.objective,
                        args.log_every, args.first_upper)
    name = f'pure_adaptive_theta{args.theta}_N{args.n}_seed{args.seed}_{args.objective}'
    name += ('_firstupper' if args.first_upper else '') + '.json'
    Path(__file__).with_name(name).write_text(json.dumps(result, indent=2)+'\n')


if __name__ == '__main__':
    main()
