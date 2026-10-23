"""Exact finite-state proof check of adaptive squeeze rejection.

This checks all accept/reject threshold regions, all reachable cache states,
and a task chosen from the previous accepted sample. It is not a frequency
test. Its small range table is an independently computed checking fixture,
not a source interface or the growing-chain learner.
"""

from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
BS = tuple(map(F, ("1/8", "1/4", "3/8", "1/2")))
PRIOR = tuple(F(i, 10) for i in (1, 2, 3, 4))
EPS = F(1, 4)
TASKS = ((1, 1), (0, 2), (1, 2), (2, 2), (2, 4))
CHILDREN = {0: (1, 2), 1: (3, 4), 2: (5, 6)}
POINTS = {0: (0, 1, 2, 3), 1: (0, 1), 2: (2, 3),
          3: (0,), 4: (1,), 5: (2,), 6: (3,)}
PATHS = {x: (0, 1 if x < 2 else 2, 3 + x) for x in range(4)}


def forward(b):
    return 3 * b * (1 - b)


def range_program(node):
    lo, hi = BS[min(POINTS[node])], BS[max(POINTS[node])]
    vals = (lo * (1 - lo), hi * (1 - hi))
    g_hi = F(1, 4) if lo <= F(1, 2) <= hi else max(vals)
    return 3 * min(vals), 3 * g_hi


def weight(f, task):
    s, n = task
    p = EPS + (1 - 2 * EPS) * f
    return p ** s * (1 - p) ** (n - s)


@lru_cache(None)
def bounds(node, task):
    lo, hi = range_program(node)
    p0 = EPS + (1 - 2 * EPS) * lo
    p1 = EPS + (1 - 2 * EPS) * hi
    s, n = task
    vals = [weight(lo, task), weight(hi, task)]
    if 0 < s < n and p0 <= F(s, n) <= p1:
        p = F(s, n)
        vals.append(p ** s * (1 - p) ** (n - s))
    return min(vals[:2]), max(vals)


def leaves(state, node=0):
    if node < 3 and state & (1 << node):
        return leaves(state, CHILDREN[node][0]) + leaves(state, CHILDREN[node][1])
    return [node]


def leaf_for(state, x):
    return next(node for node in leaves(state) if x in POINTS[node])


def decide(state, x, u, task, wrong=False):
    node = leaf_for(state, x)
    old = bounds(node, task)[1]
    while True:
        low, high = bounds(node, task)
        if u < low / old:
            return True, state
        if u >= high / old:
            return False, state
        assert node in CHILDREN
        state |= 1 << node
        node = next(ch for ch in CHILDREN[node] if x in POINTS[ch])
        if wrong:
            old = bounds(node, task)[1]


def transitions(state, task, wrong=False):
    zu = sum(sum(PRIOR[x] for x in POINTS[node]) * bounds(node, task)[1]
             for node in leaves(state))
    out = {}
    for x in range(4):
        start = leaf_for(state, x)
        old = bounds(start, task)[1]
        qx = PRIOR[x] * old / zu
        ratios = {F(0), F(1)}
        path = PATHS[x]
        tail = path[path.index(start):]
        for node in tail:
            for value in bounds(node, task):
                ratios.add(value / old)
                if wrong:
                    # Possible changed-denominator threshold regions.
                    for prev in tail:
                        ratios.add(value / bounds(prev, task)[1])
        cutoffs = sorted(v for v in ratios if 0 <= v <= 1)
        for left, right in zip(cutoffs, cutoffs[1:]):
            accept, new_state = decide(state, x, (left + right) / 2, task, wrong)
            key = (accept, x if accept else -1, new_state)
            out[key] = out.get(key, F(0)) + qx * (right - left)
    assert sum(out.values()) == 1
    return out, zu


@lru_cache(None)
def final_law(state, task):
    trans, _ = transitions(state, task)
    result = {}
    loop = F(0)
    for (accept, x, new_state), prob in trans.items():
        if accept:
            key = (x, new_state)
            result[key] = result.get(key, F(0)) + prob
        elif new_state == state:
            loop += prob
        else:
            assert (new_state | state) == new_state
            for key, q in final_law(new_state, task).items():
                result[key] = result.get(key, F(0)) + prob * q
    assert loop < 1
    result = {key: q / (1 - loop) for key, q in result.items()}
    assert sum(result.values()) == 1
    return result


def posterior(task):
    masses = [PRIOR[x] * weight(forward(BS[x]), task) for x in range(4)]
    z = sum(masses)
    return tuple(q / z for q in masses)


def main():
    states = [0, 1, 3, 5, 7]
    one_step_checks = 0
    eventual_checks = 0
    for state in states:
        for task in TASKS:
            trans, zu = transitions(state, task)
            for x in range(4):
                got = sum(p for (ok, y, _), p in trans.items() if ok and y == x)
                assert got == PRIOR[x] * weight(forward(BS[x]), task) / zu
                one_step_checks += 1
            law = final_law(state, task)
            marg = tuple(sum(p for (y, _), p in law.items() if y == x)
                         for x in range(4))
            assert marg == posterior(task)
            eventual_checks += 1

    first = (1, 1)
    next_tasks = ((0, 2), (1, 2), (2, 2), (2, 4))
    joint = {(i, j): F(0) for i in range(4) for j in range(4)}
    for (x, state), p in final_law(0, first).items():
        for (y, _), q in final_law(state, next_tasks[x]).items():
            joint[x, y] += p * q
    for x in range(4):
        for y in range(4):
            assert joint[x, y] == posterior(first)[x] * posterior(next_tasks[x])[y]

    # Minimal exact changed-denominator counter, with the actual quadratic
    # interval range from the proof file. Both points wrongly accept surely.
    weights = (F(17, 32), F(20, 32))
    old = max(weights)
    correct_trial = tuple(F(1, 2) * w / old for w in weights)
    correct = tuple(p / sum(correct_trial) for p in correct_trial)
    wrong = (F(1, 2), F(1, 2))
    assert correct == (F(17, 37), F(20, 37))
    assert wrong != correct

    report = {
        "status": "PASS",
        "arithmetic": "exact Fraction; no empirical frequency test",
        "reachable_cache_states": states,
        "one_proposal_point_mass_identities": one_step_checks,
        "eventual_posterior_identities": eventual_checks,
        "adaptive_two_task_joint_identities": len(joint),
        "absorbing_self_loops": "summed exactly as 1/(1-loop)",
        "wrong_denominator_posterior": list(map(str, wrong)),
        "correct_posterior": list(map(str, correct)),
        "input_interface_scope": "small exact checking fixture, not the production learner",
    }
    (HERE / "exact_adaptive_law_check.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
