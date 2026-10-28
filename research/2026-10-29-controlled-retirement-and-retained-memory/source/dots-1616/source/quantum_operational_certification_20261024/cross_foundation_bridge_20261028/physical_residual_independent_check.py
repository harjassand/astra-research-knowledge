#!/usr/bin/env python3
"""Independent exact audit fixture: nonzero reachable kernel, stopping, final readout.

Analytic algebra only. No acquisition, randomness, feasibility search or source edits.
The physical memory is two classical bits embedded in a four-level quantum system.
The first bit is observed; the second is invisible and physically retained.
"""
from pathlib import Path
import hashlib
import itertools
import json
import sympy as s

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'COUNT_CERTIFIED_PHYSICAL_RESIDUAL_SIMULATOR.md'
SOURCE_HASH = '59b53f8b7a4d54e2f38cb7eb3d643c13d4b356646a3de14967dfa1df6d0da6f2'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_HASH
Q = s.Rational
eye = s.eye(4)
trace = s.ones(1, 4)
visible1 = s.Matrix([[0, 1, 0, 1]])
start = s.Matrix([Q(2, 3), Q(1, 3), 0, 0])
X = s.zeros(4)
F = s.zeros(4)
for i in range(4):
    X[i ^ 1, i] = 1
    F[i ^ 2, i] = 1
M0 = s.diag(1, 0, 1, 0)
M1 = eye - M0
G = s.Matrix.hstack(start, X * start)
tests = s.Matrix.vstack(trace, visible1)
H = tests * G
U = H.inv()
assert H == s.Matrix([[1, 1], [Q(1, 3), Q(2, 3)]])
assert H.det() == Q(1, 3)

def maps(flip):
    # B is a quantum random-unitary channel, not merely a stochastic proposal.
    return {'B': [(1 - flip) * eye + flip * X], 'X': [X],
            'F': [F], 'M': [M0, M1]}

true = maps(Q(1, 5))
fit = maps(Q(201, 1000))
true_effects = [s.Matrix([[Q(1, 5), Q(4, 5), Q(1, 5), Q(4, 5)]])]
fit_effects = [s.Matrix([[Q(201, 1000), Q(799, 1000), Q(201, 1000), Q(799, 1000)]])]
true_effects.append(trace - true_effects[0])
fit_effects.append(trace - fit_effects[0])

# Check complete physical instruments on the FULL four-level quantum memory.
# X/F are permutation unitaries; M's Kraus operators are orthogonal projectors.
choi_ranks = {}
for name, flip in [('true', Q(1, 5)), ('fit', Q(201, 1000))]:
    ks = {'B': [[s.sqrt(1 - flip) * eye, s.sqrt(flip) * X]],
          'X': [[X]], 'F': [[F]], 'M': [[M0], [M1]]}
    choi_ranks[name] = {}
    for action, branches in ks.items():
        complete = sum((k.T * k for branch in branches for k in branch), s.zeros(4))
        assert complete == eye
        ranks = []
        for branch in branches:
            vs = [k.reshape(16, 1) for k in branch]
            choi = sum((v * v.T for v in vs), s.zeros(16))
            ranks.append(choi.rank())
            assert choi.det() == 0
        choi_ranks[name][action] = ranks
for effs in [true_effects, fit_effects]:
    assert sum(effs, s.zeros(1, 4)) == trace
    assert all(0 <= x <= 1 for eff in effs for x in eff)

Ct = {a: [U * tests * m * G for m in ms] for a, ms in true.items()}
Cf = {a: [U * tests * m * G for m in ms] for a, ms in fit.items()}
massrow = s.ones(1, 2)
for cs in [Ct, Cf]:
    for ms in cs.values():
        assert massrow * sum(ms, s.zeros(2)) == massrow

# Independently establish complete reachable / observable spans by saturation.
def independent_columns(vectors):
    A = s.Matrix.hstack(*vectors)
    return A[:, A.rref()[1]]

def saturate_columns(initial, matrices):
    V = independent_columns(initial)
    dims = [V.cols]
    while True:
        W = independent_columns([V[:, j] for j in range(V.cols)] +
                                [m * V[:, j] for m in matrices for j in range(V.cols)])
        if W.cols == V.cols:
            return V, dims
        V = W
        dims.append(V.cols)

rank_reports = {}
for name, mm, effects in [('true', true, true_effects), ('fit', fit, fit_effects)]:
    matrices = [m for ms in mm.values() for m in ms]
    reachable, rdims = saturate_columns([start], matrices)
    observable, odims = saturate_columns([trace.T] + [f.T for f in effects],
                                        [m.T for m in matrices])
    assert reachable.cols == 4
    assert (observable.T * reachable).rank() == 2
    rank_reports[name] = {'reachable_dimension': reachable.cols,
                          'reachable_growth': rdims,
                          'observable_seed_growth': odims,
                          'observable_rank': 2}

# A real reachable unobservable kernel, including all declared terminal seeds.
K = s.Matrix.hstack(eye[:, 0] - eye[:, 2], eye[:, 1] - eye[:, 3])
assert trace * K == s.zeros(1, 2)
assert all(e * K == s.zeros(1, 2) for e in fit_effects)
nonintertwining = []
for a, ms in fit.items():
    for o, physical in enumerate(ms):
        assert physical * K == K * (physical * K)[:2, :]
        defect = physical * G - G * Cf[a][o]
        assert defect == K * defect[:2, :]
        if defect != s.zeros(4, 2):
            nonintertwining.append((a, o))
assert ('F', 0) in nonintertwining
assert start == G[:, 0]

# Hypothetical rational simultaneous bands around exact analytic midpoints.
w = Q(1, 100000)
DH = s.Matrix([[0, 0], [w, w]])
A = abs(U) * DH
assert max(sum(A[i, j] for j in range(2)) for i in range(2)) < 1
inverse_bound = (s.eye(2) - A).inv() * abs(U)
R = inverse_bound - abs(U)
Kcore = max(sum(abs(x) for x in U * v) + (massrow * R * v)[0]
            for v in [s.Matrix([1, 0]), s.Matrix([1, 1])])
assert Kcore >= 3
Es, gs = {}, {}
residual_corner_checks = 0
inverse_corner_checks = 0
inverse_corners = []
for signs in itertools.product([-1, 1], repeat=2):
    perturbed = H + s.Matrix([[0, 0], [signs[0] * w, signs[1] * w]])
    inv = perturbed.inv()
    assert all(abs(inv[i, j]) <= inverse_bound[i, j] for i in range(2) for j in range(2))
    assert all(abs(inv[i, j] - U[i, j]) <= R[i, j] for i in range(2) for j in range(2))
    assert all(sum(abs(x) for x in inv * v) <= Kcore
               for v in [s.Matrix([1, 0]), s.Matrix([1, 1])])
    inverse_corners.append((perturbed, inv))
    inverse_corner_checks += 1
for a, ms in true.items():
    Es[a] = []
    for o, physical in enumerate(ms):
        hzt = tests * physical * G
        hzf = tests * fit[a][o] * G
        hz_hat = (hzt + hzf) / 2
        dz = abs(hzt - hzf) / 2 + s.ones(2) * w
        if len(ms) == 1:
            dz[0, :] = s.zeros(1, 2)
        c = Cf[a][o]
        e = inverse_bound * (dz + DH * abs(c) + abs(H * c - hz_hat))
        actual = abs(Ct[a][o] - c)
        assert all(e[i, j] >= actual[i, j] for i in range(2) for j in range(2))
        for perturbed, inv in inverse_corners:
            for signs in itertools.product([-1, 1], repeat=4):
                shifted = hz_hat + s.Matrix(2, 2, lambda i, j: signs[2 * i + j] * dz[i, j])
                discrepancy = inv * shifted - c
                assert perturbed * discrepancy == shifted - perturbed * c
                assert all(abs(discrepancy[i, j]) <= e[i, j]
                           for i in range(2) for j in range(2))
                residual_corner_checks += 1
        bz = inverse_bound * (abs(hz_hat) + dz)
        universal = 2 * inverse_bound * (dz + DH * bz)
        assert all(universal[i, j] >= e[i, j] for i in range(2) for j in range(2))
        assert all(bz[i, j] >= abs(c[i, j]) for i in range(2) for j in range(2))
        Es[a].append(e)
    gs[a] = max(sum(e[i, j] for e in Es[a] for i in range(2)) for j in range(2))
b = Kcore * max(gs.values()) / 2
qt = [e * G for e in true_effects]
qf = [e * G for e in fit_effects]
terminal_band = [abs(x - y) for x, y in zip(qt, qf)]
bterm = Kcore * max(sum(q[0, j] for q in terminal_band) for j in range(2)) / 2

# Same policy in both models; full records include outcomes and genuinely final bits.
def policy(h):
    depth = len(h)
    if depth == 4 and h[3] == h[0]:
        return None
    if depth == 6:
        return None
    return ['M', ('B' if h[0] == 0 else 'X') if h else 'B', 'F', 'M', 'B', 'M'][depth]

def final_order(h):
    return [1, 0] if sum(h) % 2 else [0, 1]

def physical_law(mm, effects, h, v):
    a = policy(h)
    if a is None:
        return {h + ('terminal', j): (effects[o] * v)[0]
                for j, o in enumerate(final_order(h))}
    answer = {}
    for o, m in enumerate(mm[a]):
        answer.update(physical_law(mm, effects, h + (o,), m * v))
    return answer

pt = physical_law(true, true_effects, (), start)
pf = physical_law(fit, fit_effects, (), start)
assert pt.keys() == pf.keys()
assert sum(pt.values()) == sum(pf.values()) == 1
assert all(p >= 0 for p in list(pt.values()) + list(pf.values()))
tv = sum(abs(pt[h] - pf[h]) for h in pt) / 2
telescope = {h: s.S.Zero for h in pt}
call_mass = s.S.Zero
stop_mass = s.S.Zero
negative_prefixes = 0
max_ratio = s.S.Zero
signed_suffix_tests = 0
local_bound = s.S.Zero

def add_signed(target, increment):
    for h, value in increment.items():
        target[h] += value

def visit(h, real_state, coordinates):
    global call_mass, stop_mass, negative_prefixes, max_ratio, signed_suffix_tests, local_bound
    p = (trace * real_state)[0]
    assert tests * real_state == H * coordinates
    assert (massrow * coordinates)[0] == p
    assert all(0 <= x <= p for x in H * coordinates)
    if p:
        ratio = sum(abs(x) for x in coordinates) / p
        max_ratio = max(max_ratio, ratio)
        assert ratio <= Kcore
    negative_prefixes += int(any(x < 0 for x in coordinates))
    a = policy(h)
    if a is None:
        stop_mass += p
        for j, o in enumerate(final_order(h)):
            discrepancy = ((qt[o] - qf[o]) * coordinates)[0]
            assert discrepancy == ((true_effects[o] - fit_effects[o]) * real_state)[0]
            telescope[h + ('terminal', j)] += discrepancy
        return
    call_mass += p
    local_bound += Kcore * gs[a] * p / 2
    for o, physical in enumerate(true[a]):
        insertion = (Ct[a][o] - Cf[a][o]) * coordinates
        # Key independent check: lift insertion and use PHYSICAL fitted suffix,
        # not fitted quotient recursion. The core section does not intertwine F.
        signed = physical_law(fit, fit_effects, h + (o,), G * insertion)
        assert sum(abs(v) for v in signed.values()) <= sum(abs(x) for x in insertion)
        add_signed(telescope, signed)
        signed_suffix_tests += 1
        visit(h + (o,), physical * real_state, Ct[a][o] * coordinates)

visit((), start, s.Matrix([1, 0]))
assert stop_mass == 1
assert all(telescope[h] == pt[h] - pf[h] for h in pt)
assert negative_prefixes > 0
assert call_mass < 6
assert tv <= local_bound + bterm <= b * call_mass + bterm

# Reproduce indispensable exact-rank obstruction independently.
bad0 = s.Matrix([[0, 0], [1, 0]])
bad1 = s.Matrix([[0, 0], [0, 1]])
badstart = s.Matrix([1, 0])
badtrace = s.ones(1, 2)
assert (badtrace * bad0 * badstart)[0] == 1
assert (badtrace * bad1 * badstart)[0] == 0
assert (badtrace * bad1 * bad0 * badstart)[0] == 1
assert s.Matrix([[1, 1], [0, 1]]).rank() == 2

# Rational equations can have physical rank-boundary points but no rational point.
# This small illustration is not a simulation of the theorem's acquisition search.
t = (3 + s.sqrt(5)) / 6
algebraic_pure_state = s.Matrix([[t, Q(1, 3)], [Q(1, 3), 1 - t]])
assert s.simplify(algebraic_pure_state.det()) == 0
assert algebraic_pure_state.trace() == 1 and 0 < 1 - t < t < 1
assert s.simplify(9 * t * t - 9 * t + 1) == 0
assert t.is_rational is False

def encode(obj):
    if isinstance(obj, dict): return {str(k): encode(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)): return [encode(x) for x in obj]
    if isinstance(obj, s.Basic): return str(obj)
    return obj

report = {
    'status': 'PASS independent exact diagnostic',
    'source_sha256': SOURCE_HASH,
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'source_calls': 0, 'rng_calls': 0, 'counts_acquired': False,
    'semialgebraic_solver_executed': False,
    'physical_dimension': 4, 'core_rank': 2, 'core_determinant': H.det(),
    'rank_certificates': rank_reports, 'reachable_unobservable_kernel_dimension': 2,
    'nonintertwining_branches': nonintertwining,
    'full_quantum_choi_ranks': choi_ranks,
    'K_core': Kcore, 'b': b, 'b_term': bterm,
    'true_expected_calls': call_mass, 'maximum_calls': 6,
    'transcript_TV': tv, 'transcript_TV_float': float(tv),
    'local_call_bound_plus_terminal': local_bound + bterm,
    'expected_call_bound_plus_terminal': b * call_mass + bterm,
    'expected_call_bound_plus_terminal_float': float(b * call_mass + bterm),
    'negative_true_prefix_nodes': negative_prefixes,
    'max_true_coordinate_to_mass_ratio': max_ratio,
    'physical_signed_suffix_contractions_checked': signed_suffix_tests,
    'exact_telescope_residual': 0,
    'all_feasible_residual_domination_Eq17_checked': True,
    'inverse_and_positive_cube_corner_checks': inverse_corner_checks,
    'exact_residual_interval_corner_checks': residual_corner_checks,
    'rational_polynomial_boundary_illustration': {
        'density_diagonal_t': t, 'offdiagonal': Q(1, 3),
        'density_rank': 1, 'rational_point_exists': False,
        'polynomial': '9*t**2 - 9*t + 1 = 0; t > 1/2'},
    'drop_rank_counterexample': {'one_step_residual': 0, 'depth_two_TV': 1, 'candidate_rank': 2},
}
(ROOT / 'physical_residual_independent_check.json').write_text(json.dumps(encode(report), indent=2) + '\n')
print(json.dumps(encode(report), indent=2))
