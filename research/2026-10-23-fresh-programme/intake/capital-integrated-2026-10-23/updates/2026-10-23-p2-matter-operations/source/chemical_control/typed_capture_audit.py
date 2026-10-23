"""Independent exact audit of the parent's O(H)/P typed capture model.

Own state representation, exchange/lock generator, completion oracle, and
type-preserving quotient. Parent source is loaded only for cross-comparison.
Vertex permutations preserve the parity of EVERY stub. No individual type
flips, and no optional global OH/P swap, are used in the quotient.
All clocks are synthetic. No chemical kinetics or physical guard is inferred.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import hashlib
import itertools
import json
import math
import types

OUT = Path(__file__).resolve().parent
SOURCE = OUT.parent / "network_control" / "collective_capture.py"
PARENT_RESULTS = SOURCE.with_name("collective_capture_results.json")
SOURCE_BYTES = SOURCE.read_bytes()
SOURCE_HASH = hashlib.sha256(SOURCE_BYTES).hexdigest()
capture = types.ModuleType("typed_capture_parent_under_review")
capture.__file__ = str(SOURCE)
exec(compile(SOURCE_BYTES, str(SOURCE), "exec"), capture.__dict__)

V = 4
PERMS = tuple(itertools.permutations(range(V)))
# pi(i) is the phosphate partner of OH arm i; bit i marks that directed bond.
INITIAL = ((0, 2, 3, 1), 0)
POLICIES = ("unrestricted", "stub_guard", "connected_guard")


def to_parent(state):
    pi, mask = state
    locked, opened = [], []
    for i, j in enumerate(pi):
        edge = tuple(sorted((2*i, 2*j+1)))
        (locked if mask >> i & 1 else opened).append(edge)
    return tuple(sorted(locked)), tuple(sorted(opened))


def from_parent(state):
    pi, mask = [-1]*V, 0
    locked, opened = state
    stubs = [s for edge in locked+opened for s in edge]
    assert sorted(stubs) == list(range(2*V))
    for is_locked, edges in ((True, locked), (False, opened)):
        for a, b in edges:
            assert a % 2 != b % 2
            oh, phosphate = (a, b) if a % 2 == 0 else (b, a)
            i, j = oh//2, phosphate//2
            assert pi[i] == -1
            pi[i] = j
            if is_locked:
                assert i != j
                mask |= 1 << i
    assert sorted(pi) == list(range(V))
    return tuple(pi), mask


def unlocked_arms(state):
    pi, mask = state
    oh = tuple(i for i in range(V) if not (mask >> i & 1))
    phosphate = tuple(sorted(pi[i] for i in oh))
    return oh, phosphate


def hall_degree_guard(state):
    oh, phosphate = unlocked_arms(state)
    assert len(oh) == len(phosphate)
    n = len(oh)
    return all((i in oh)+(i in phosphate) <= n for i in range(V))


def proper_directed_cycle_guard(state):
    pi, mask = state
    for start in range(V):
        order, v = {}, start
        while mask >> v & 1:
            if v in order:
                cycle_length = len(order)-order[v]
                if cycle_length < V:
                    return False
                break
            order[v] = len(order)
            v = pi[v]
    return True


def connected_permutation(pi):
    seen, v = set(), 0
    while v not in seen:
        seen.add(v)
        v = pi[v]
    return len(seen) == V


@lru_cache(None)
def completion_oracle(locked_pairs, require_connected):
    # Exhaustive independent bijection oracle, no parent's pairings routine.
    return any(
        all(q[i] == j for i, j in locked_pairs)
        and all(q[i] != i for i in range(V))
        and (not require_connected or connected_permutation(q))
        for q in PERMS)


def locked_pairs(state):
    pi, mask = state
    return tuple((i, pi[i]) for i in range(V) if mask >> i & 1)


def independent_transitions(state, policy):
    pi, mask = state
    unlocked = tuple(i for i in range(V) if not (mask >> i & 1))
    result = Counter()
    for i in unlocked:
        if pi[i] == i:
            continue
        nxt = (pi, mask | (1 << i))
        if policy == "stub_guard" and not hall_degree_guard(nxt):
            continue
        if policy == "connected_guard" and not proper_directed_cycle_guard(nxt):
            continue
        result[nxt] += F(1)
    for i, j in itertools.combinations(unlocked, 2):
        q = list(pi)
        q[i], q[j] = q[j], q[i]
        result[(tuple(q), mask)] += F(1)
    return dict(result)


@lru_cache(None)
def vertex_orbit(state):
    pi, mask = state
    images = []
    for p in PERMS:
        q, newmask = [-1]*V, 0
        for i in range(V):
            q[p[i]] = p[pi[i]]
            if mask >> i & 1:
                newmask |= 1 << p[i]
        images.append((tuple(q), newmask))
    return min(images)


def category(state):
    pi, mask = state
    loops = sum(i == j for i, j in enumerate(pi))
    if loops:
        assert loops == 1 and V-mask.bit_count() == 1
        return 2
    assert mask.bit_count() == V
    return 0 if connected_permutation(pi) else 1


def fraction_elimination(matrix, rhs_count):
    # Exact Gauss-Jordan algorithm adapted from the earlier untyped audit.
    n = len(matrix)
    for j in range(n):
        pivot = next(i for i in range(j, n) if matrix[i][j])
        matrix[j], matrix[pivot] = matrix[pivot], matrix[j]
        denominator = matrix[j][j]
        for k in range(j, n+rhs_count):
            matrix[j][k] /= denominator
        for i in range(n):
            if i != j and matrix[i][j]:
                factor = matrix[i][j]
                for k in range(j, n+rhs_count):
                    matrix[i][k] -= factor*matrix[j][k]
    return [row[n:] for row in matrix]


def balanced_subset_audit():
    checked = 0
    for mask in range(1 << (2*V)):
        oh = [i for i in range(V) if mask >> (2*i) & 1]
        phosphate = [i for i in range(V) if mask >> (2*i+1) & 1]
        if len(oh) != len(phosphate):
            continue
        n = len(oh)
        condition = all((i in oh)+(i in phosphate) <= n for i in range(V))
        actual = any(all(i != j for i, j in zip(oh, q))
                     for q in itertools.permutations(phosphate))
        assert condition == actual
        checked += 1
    assert checked == 70
    return checked


def exact_case(policy, parent_cases):
    states, seen, raw = [INITIAL], {INITIAL}, {}
    checked_candidate_locks = 0
    for state in states:
        pi, mask = state
        parent_state = to_parent(state)
        assert from_parent(parent_state) == state
        assert all(a % 2 != b % 2 for a, b in parent_state[0]+parent_state[1])
        ours = independent_transitions(state, policy)
        theirs = {from_parent(z): F(rate) for z, rate in capture.transitions(
            parent_state, policy, 1., 1., typed=True).items()}
        assert ours == theirs, (policy, state, "generator mismatch")
        raw[state] = ours
        opened_count = V-mask.bit_count()
        exchange_hazard = sum(rate for z, rate in ours.items() if z[1] == mask)
        assert exchange_hazard == math.comb(opened_count, 2)
        if policy == "unrestricted":
            lock_hazard = sum(rate for z, rate in ours.items() if z[1] != mask)
            assert lock_hazard == sum(not(mask >> i & 1) and pi[i] != i
                                      for i in range(V))
        stubs = tuple(sorted(s for edge in parent_state[1] for s in edge))
        actual_connected = completion_oracle(locked_pairs(state), True)
        assert proper_directed_cycle_guard(state) == actual_connected
        assert actual_connected == capture.feasible_connected(parent_state[0], stubs, True)
        assert hall_degree_guard(state) == completion_oracle(locked_pairs(state), False)
        assert hall_degree_guard(state) == capture.feasible_loopfree(parent_state[1])
        for i in range(V):
            if not (mask >> i & 1) and pi[i] != i:
                candidate = (pi, mask | (1 << i))
                assert proper_directed_cycle_guard(candidate) == completion_oracle(
                    locked_pairs(candidate), True)
                checked_candidate_locks += 1
        for nxt in ours:
            if nxt not in seen:
                seen.add(nxt)
                states.append(nxt)

    if policy == "unrestricted":
        full_admissible_space = {
            (q, mask) for q in PERMS for mask in range(1 << V)
            if all(not (mask >> i & 1) or q[i] != i for i in range(V))}
        assert seen == full_admissible_space

    aggregate, representative = {}, {}
    for state in states:
        os = vertex_orbit(state)
        representative.setdefault(os, state)
        events = Counter()
        for nxt, rate in raw[state].items():
            oz = vertex_orbit(nxt)
            if oz != os:
                events[oz] += rate
        events = dict(events)
        if os in aggregate:
            assert events == aggregate[os], "Strong lumpability failed"
        else:
            aggregate[os] = events
        if not events:
            assert not raw[state], "Unanalysed nonterminal closed orbit"

    transient = [s for s, ev in aggregate.items() if ev]
    index = {s: i for i, s in enumerate(transient)}
    n = len(transient)
    matrix = [[F(0) for _ in range(n+4)] for _ in range(n)]
    for s, i in index.items():
        matrix[i][i] = sum(aggregate[s].values())
        matrix[i][n+3] = 1
        for z, rate in aggregate[s].items():
            if z in index:
                matrix[i][index[z]] -= rate
            else:
                matrix[i][n+category(representative[z])] += rate
    solutions = fraction_elimination(matrix, 4)
    for row in solutions:
        assert all(0 <= x <= 1 for x in row[:3])
        assert sum(row[:3]) == 1 and row[3] > 0
    answer = solutions[index[vertex_orbit(INITIAL)]]
    assert answer[2] >= F(1, 15) if policy == "unrestricted" else answer[2] == 0
    if policy == "connected_guard":
        assert answer[:3] == [1, 0, 0]

    parent = next(r for r in parent_cases if r["arm_chemistry"] ==
                  "opposite_polarity_only" and r["policy"] == policy
                  and r["kappa_over_nu"] == 1)
    parent_numbers = [parent[k] for k in (
        "final_connected_loopfree_probability",
        "final_disconnected_loopfree_probability", "final_one_loop_jam_probability",
        "mean_absorption_time_in_nu_inverse")]
    max_difference = max(abs(float(x)-y) for x, y in zip(answer, parent_numbers))
    assert max_difference < 1e-10
    assert len(states) == parent["reachable_states"]
    terminal_count = sum(not raw[s] for s in states)
    assert terminal_count == parent["terminal_states"]
    return dict(
        policy=policy, kappa_over_nu=1,
        arm_states=len(states), terminal_states=terminal_count,
        orbit_states=len(aggregate), transient_orbits=n,
        exact_probabilities_connected_disconnected_jam=[str(x) for x in answer[:3]],
        decimal_probabilities=[float(x) for x in answer[:3]],
        mean_absorption_time_exact_in_nu_inverse=str(answer[3]),
        mean_absorption_time_decimal_in_nu_inverse=float(answer[3]),
        maximum_difference_from_parent_numerical_result=max_difference,
        generator_comparison="INDEPENDENT_TYPED_GENERATOR_MATCHES_ON_EVERY_REACHABLE_STATE",
        exchange_hazard="EXACTLY_CHOOSE_UNLOCKED_BONDS_2_TIMES_NU",
        polarity_invariance="EVERY_REACHABLE_STATE_AND_TRANSITION_CHECKED",
        strong_lumpability="CHECKED_EXACTLY_FOR_VERTEX_PERMUTATIONS_ONLY",
        directed_cycle_completion="MATCHES_INDEPENDENT_AND_PARENT_TYPED_COMPLETION_ORACLES",
        candidate_locks_with_cycle_oracle_check=checked_candidate_locks)


def main():
    assert to_parent(INITIAL) == capture.TYPED_INITIAL
    # Explicit parity check for every permitted symmetry lift.
    assert all((2*p[s//2]+s%2) % 2 == s % 2
               for p in PERMS for s in range(2*V))
    parent_bytes = PARENT_RESULTS.read_bytes()
    parent = json.loads(parent_bytes)
    result = dict(
        status="EXACT_RATIONAL_TYPED_MODEL_AUDIT",
        source_under_review=str(SOURCE.relative_to(OUT.parent)),
        source_sha256=SOURCE_HASH,
        parent_result_sha256=hashlib.sha256(parent_bytes).hexdigest(),
        representation="Permutation OH i -> phosphate pi(i), with locked directed tails",
        symmetry="Simultaneous vertex relabeling only; no individual or global type flips",
        independent_components="Typed generator, bijection completion oracle, directed cycle guard, orbit construction, exact rational solution",
        loopfree_hall_balanced_subsets_checked=balanced_subset_audit(),
        rates="Synthetic kappa=nu=1; no physical kinetic parameters",
        acquired_measurements="NONE", physical_guard_interface="UNKNOWN",
        model_receipt="UNKNOWN", tokens="UNKNOWN", spend="UNKNOWN",
        cases=[exact_case(p, parent["cases"]) for p in POLICIES])
    result["source_unchanged_during_audit"] = hashlib.sha256(
        SOURCE.read_bytes()).hexdigest() == SOURCE_HASH
    assert result["source_unchanged_during_audit"]
    (OUT / "typed_capture_audit_results.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
