#!/usr/bin/env python3
"""Separate post-freeze review of adversary Sections 4 and 5.

Uses an independently built three-qubit two-predicate algebra. Does not import
or execute the other worker's scientific code, and does not modify its files.
"""
import datetime
import hashlib
import json
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
PEER = HERE.parent / 'gd_compiler_adversary' / 'PROOFS.md'
EXPECTED_PEER_SHA = 'a978f58856c505125a0c8c1ae64ae8cb9ab787db16cc3eb2fd41a34df3e80101'
EXPECTED_GENESIS_SEAL_SHA = '85618d0b734da8e00ec9b09afe26f0ff6c5003231edee508781beedcc023ca0f'
RNG = np.random.default_rng(2026101613)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def adj(a):
    return a.conj().T


def units(d):
    for i in range(d):
        for j in range(d):
            x = np.zeros((d, d), complex)
            x[i, j] = 1
            yield x


def max_map_error(left, right, d):
    return max(float(np.max(np.abs(left(x) - right(x)))) for x in units(d))


def choi_rect(action, din, dout):
    out = np.zeros((dout * din, dout * din), complex)
    for x in units(din):
        out += np.kron(action(x), x) / din
    return out


def run():
    start = time.perf_counter()
    assert sha(PEER) == EXPECTED_PEER_SHA
    assert sha(HERE / 'FROZEN.json') == EXPECTED_GENESIS_SEAL_SHA
    genesis_manifest = json.loads((HERE / 'FROZEN.json').read_text())
    assert all(sha(Path(item['path'])) == item['sha256'] for item in genesis_manifest['artifacts'])
    ident = np.eye(2, dtype=complex)
    x = np.array([[0, 1], [1, 0]], complex)
    y = np.array([[0, -1j], [1j, 0]], complex)
    z = np.diag([1, -1]).astype(complex)
    embed = lambda a: np.kron(np.kron(a, ident), ident)
    axes = [embed(x), embed(y), embed(z)]
    full_i = np.eye(8, dtype=complex)
    s = np.kron(np.kron(z, z), ident)
    t = np.kron(np.kron(z, ident), z)
    pi = (full_i - s) @ (full_i - t) / 4
    inactive = full_i - pi
    a = axes[0] @ pi
    bs = [-1j * p @ a for p in axes]
    active_basis = np.eye(8)[:, np.flatnonzero(np.diag(pi).real > .5)]
    rank = active_basis.shape[1]
    vectors = np.column_stack([(op @ active_basis).reshape(-1) / np.sqrt(rank) for op in [a] + bs])
    gram_error = float(np.max(np.abs(adj(vectors) @ vectors - np.eye(4))))
    kappa = .7

    def conditional(action, rho):
        return action @ rho @ adj(action) + inactive @ rho @ inactive

    c0 = lambda rho: conditional(a, rho)
    cs = [lambda rho, b=b: conditional(b, rho) for b in bs]
    nav = lambda rho: (c0(rho) + sum((c(rho) for c in cs), np.zeros_like(rho))) / 4
    map_errs, scalar_errs, cp_mins, rate_lowers, restriction_errs = [], [], [], [], []
    cases = 0
    for m in (1, 2, 3):
        theta_c = float(np.arctan(1 / np.sqrt(m)))
        for theta_0 in (.02, .8 * theta_c, theta_c, theta_c + .08, np.pi / 2):
            if theta_0 < theta_c:
                q0 = np.sin(theta_0) ** 2
                t0 = np.sin(theta_0) * np.cos(theta_0)
                alpha = kappa * (q0 + np.sqrt(m) * t0)
                beta = kappa * (t0 / np.sqrt(m) - q0)
            else:
                alpha, beta = kappa, 0.0
            rate = alpha + m * beta
            # Independent endpoint dual calculation after projection and averaging.
            lower_angle = min(theta_0, theta_c)
            ql = np.sin(lower_angle) ** 2
            tl = np.sin(lower_angle) * np.cos(lower_angle)
            b_opt = max(0, kappa * (tl / np.sqrt(m) - ql))
            a_opt = kappa * ql + kappa * kappa * ql * (1 - ql) / (b_opt + kappa * ql)
            rate_lowers.append(abs(rate - a_opt - m * b_opt))
            for sample in range(4):
                u = RNG.normal(size=m)
                u /= np.linalg.norm(u)
                theta = theta_0 if sample == 0 else 0 if sample == 1 else RNG.uniform(-theta_0, theta_0)
                p_u = sum((uj * pj for uj, pj in zip(u, axes)), np.zeros_like(full_i))
                unitary = np.cos(theta) * full_i - 1j * np.sin(theta) * p_u
                actual_a = unitary @ a
                ctheta = lambda rho: conditional(actual_a, rho)
                nmap = lambda rho: (alpha * c0(rho) + beta * sum((c(rho) for c in cs[:m]), np.zeros_like(rho))) / rate
                proposal = lambda rho: nmap(rho) + kappa * (ctheta(rho) - c0(rho)) / rate
                w = np.r_[np.cos(theta), np.sin(theta) * u]
                block = np.diag(np.r_[alpha, np.full(m, beta)]) + kappa * (np.outer(w, w) - np.diag(np.r_[1, np.zeros(m)]))
                vals, eigvecs = np.linalg.eigh(block)
                ops = [a] + bs[:m]
                ks = [sum((np.sqrt(max(0, val)) * eigvecs[i, j] * op for i, op in enumerate(ops)), np.zeros_like(full_i)) for j, val in enumerate(vals)]
                ks.append(np.sqrt(rate) * inactive)
                kraus_map = lambda rho: sum((k @ rho @ adj(k) for k in ks), np.zeros_like(rho)) / rate
                map_errs.append(max_map_error(proposal, kraus_map, 8))
                scalar_errs.append(float(np.linalg.norm(sum((adj(k) @ k for k in ks), np.zeros_like(full_i)) - rate * full_i, 2)))
                cp_mins.append(float(np.linalg.eigvalsh(choi_rect(proposal, 8, 8))[0]))
                if sample == 0:
                    restricted_error = lambda rho: kappa * (ctheta(active_basis @ rho @ adj(active_basis)) - c0(active_basis @ rho @ adj(active_basis)))
                    expected = vectors[:, :m + 1] @ (kappa * (np.outer(w, w) - np.diag(np.r_[1, np.zeros(m)]))) @ adj(vectors[:, :m + 1])
                    actual = choi_rect(restricted_error, rank, 8)
                    restriction_errs.append(float(np.max(np.abs(actual - expected))))
                cases += 1

    invariant_errs = []
    for sample in range(8):
        u = RNG.normal(size=3)
        u /= np.linalg.norm(u)
        theta = RNG.uniform(-np.pi, np.pi)
        pu = sum((uj * pj for uj, pj in zip(u, axes)), np.zeros_like(full_i))
        common_u = np.cos(theta) * full_i - 1j * np.sin(theta) * pu
        actual_average = lambda rho: sum((conditional(common_u @ action, rho) for action in [a] + bs), np.zeros_like(rho)) / 4
        invariant_errs.append(max_map_error(actual_average, nav, 8))
    invariant_cp_mins = []
    for theta_0 in (.02, .5, np.pi / 2):
        nu = 4 * kappa * np.sin(theta_0)
        for sample in range(4):
            u = RNG.normal(size=3)
            u /= np.linalg.norm(u)
            theta = theta_0 if sample == 0 else RNG.uniform(-theta_0, theta_0)
            pu = sum((uj * pj for uj, pj in zip(u, axes)), np.zeros_like(full_i))
            actual_a = (np.cos(theta) * full_i - 1j * np.sin(theta) * pu) @ a
            proposal = lambda rho: nav(rho) + kappa * (conditional(actual_a, rho) - c0(rho)) / nu
            invariant_cp_mins.append(float(np.linalg.eigvalsh(choi_rect(proposal, 8, 8))[0]))
    # A command-dependent rotation is deliberately outside the shared-U premise.
    command_rotations = [full_i, np.cos(.31) * full_i - 1j * np.sin(.31) * axes[2], full_i, full_i]
    mismatched_average = lambda rho: sum((conditional(u @ action, rho) for u, action in zip(command_rotations, [a] + bs)), np.zeros_like(rho)) / 4
    outside_model_error = max_map_error(mismatched_average, nav, 8)

    unchanged_peer = sha(PEER) == EXPECTED_PEER_SHA
    unchanged_genesis = sha(HERE / 'FROZEN.json') == EXPECTED_GENESIS_SEAL_SHA and all(sha(Path(item['path'])) == item['sha256'] for item in genesis_manifest['artifacts'])
    result = {
        'recorded_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'source': {'path': str(PEER), 'sha256_before': EXPECTED_PEER_SHA, 'sha256_after': sha(PEER), 'operative_review_sections': [4, 5], 'context_read': 'Whole PROOFS.md tool output was viewed after own genesis freeze; no peer code or check output read or executed.'},
        'own_genesis_seal_sha256': EXPECTED_GENESIS_SEAL_SHA,
        'review_authorization': 'Explicit root follow-up task: independently review adversary PROOFS.md Sections 4 and 5; save separate cross-review; do not alter frozen source.',
        'minimal_algebra': {'qubits': 3, 'active_rank': rank, 'scope': 'Two independent commuting predicates and one written face; exact 11-qubit orthogonality follows separately from the stated Pauli supports.', 'restricted_choi_gram_error': gram_error},
        'rotation_minimax_checks': {'cases': cases, 'map_error_max': max(map_errs), 'scalar_rate_error_max': max(scalar_errs), 'choi_min': min(cp_mins), 'endpoint_dual_rate_error_max': max(rate_lowers), 'restricted_input_choi_error_max': max(restriction_errs), 'zero_angle_convention': 'Error and floor zero; omit zero clock; never divide by zero rate.'},
        'common_actuator_floor_checks': {'invariance_cases': 8, 'invariance_error_max': max(invariant_errs), 'proposal_cases': 12, 'choi_min': min(invariant_cp_mins), 'command_dependent_rotation_control_error': outside_model_error},
        'peer_source_unchanged': unchanged_peer, 'own_genesis_frozen_artifacts_unchanged': unchanged_genesis,
        'runtime_seconds': time.perf_counter() - start, 'numpy': np.__version__, 'packages_installed': False, 'peer_scientific_scripts_executed': False,
        'all_checks_pass': bool(gram_error < 1e-12 and max(map_errs) < 1e-12 and max(scalar_errs) < 1e-12 and min(cp_mins) > -1e-12 and max(rate_lowers) < 1e-12 and max(restriction_errs) < 1e-12 and max(invariant_errs) < 1e-12 and min(invariant_cp_mins) > -1e-12 and outside_model_error > 1e-3 and unchanged_peer and unchanged_genesis),
        'evidence_boundary': 'Finite double-precision checks plus separate analytic review; no external peer review, physical qualification or historical novelty conclusion.'
    }
    (HERE / 'CROSS_REVIEW_CHECKS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    return 0 if result['all_checks_pass'] else 1


if __name__ == '__main__':
    raise SystemExit(run())
