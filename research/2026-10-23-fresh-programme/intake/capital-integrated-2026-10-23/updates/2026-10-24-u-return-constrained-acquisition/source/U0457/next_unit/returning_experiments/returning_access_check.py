#!/usr/bin/env python3
"""Exact minimal check of MECHANISM_TEST_SPEC, with ordinary strong planning.

Standard-library integers/finite sets only. No random draws or truth access in
the planner. This is a mechanism/certificate check, not a performance benchmark.
"""

from collections import defaultdict, deque
from itertools import combinations
import json
from pathlib import Path
import time


ACTIONS = ("a", "b")
STATE_NAMES = ("H0", "H1", "S0", "S1", "T0", "T1", "D")
DEAD = 6
WORLDS = ((0, 0), (0, 1), (1, 0), (1, 1))  # candidate (theta, anchor phi)
INITIAL = tuple(phi for theta, phi in WORLDS)


def transition(theta, state, action):
    """A prior candidate program; returns (ordinary output, successor)."""
    if state < 2:
        phi = state
        return (1, 2 + phi) if action == "a" else (phi, 4 + phi)
    if state < 4:
        phi = state - 2
        return (theta, phi) if action == "a" else (1, DEAD)
    if state < 6:
        phi = state - 4
        correct = (action == "a") == (theta == 0)
        return (0, phi if correct else DEAD)
    return 0, DEAD


def equivalence(theta):
    """Largest Mealy bisimulation, calculated rather than hardcoded H=H."""
    rel = {(p, q) for p in range(7) for q in range(7)}
    while True:
        new = set()
        for p, q in rel:
            good = True
            for action in ACTIONS:
                op, dp = transition(theta, p, action)
                oq, dq = transition(theta, q, action)
                good &= op == oq and (dp, dq) in rel
            if good:
                new.add((p, q))
        if new == rel:
            return rel
        rel = new


EQUIV = (equivalence(0), equivalence(1))


def members(node):
    return tuple(w for w, state in enumerate(node) if state >= 0)


def mask(node):
    return sum(1 << w for w in members(node))


def returned(node):
    return all(
        (state, WORLDS[w][1]) in EQUIV[WORLDS[w][0]]
        for w, state in enumerate(node) if state >= 0
    )


def canonical(node):
    """Internal congruence quotient only: causes NO physical reset/action."""
    assert returned(node)
    return tuple(WORLDS[w][1] if state >= 0 else -1
                 for w, state in enumerate(node))


def successor(node, action):
    split = {}
    evaluations = 0
    for w in members(node):
        theta, _ = WORLDS[w]
        out, dest = transition(theta, node[w], action)
        evaluations += 1
        if out not in split:
            split[out] = [-1] * len(WORLDS)
        split[out][w] = dest
    return {out: tuple(dest) for out, dest in split.items()}, evaluations


def build_graph(initial):
    seen, queue, graph = {initial}, deque([initial]), {}
    transition_evals = 0
    while queue:
        node = queue.popleft()
        graph[node] = {}
        for action in ACTIONS:
            children, count = successor(node, action)
            transition_evals += count
            graph[node][action] = children
            for child in children.values():
                if child not in seen:
                    seen.add(child)
                    queue.append(child)
    return graph, transition_evals


def solve(graph, pair=None, singleton=False):
    """Least fixed point; value is minimum worst-case finite action length."""
    def goal(node):
        separated = ((len(members(node)) == 1) if singleton else
                     (pair is None or not all(node[w] >= 0 for w in pair)))
        return returned(node) and separated

    rank = {node: 0 for node in graph if goal(node)}
    policy = {}
    sweeps = action_tests = 0
    while True:
        additions = {}
        for node in graph:
            if node in rank:
                continue
            for action in ACTIONS:
                action_tests += 1
                children = tuple(graph[node][action].values())
                if all(child in rank for child in children):
                    depth = 1 + max(rank[child] for child in children)
                    candidate = depth, action
                    if node not in additions or candidate < additions[node]:
                        additions[node] = candidate
        sweeps += 1
        if not additions:
            break
        for node, (depth, action) in additions.items():
            rank[node], policy[node] = depth, action
    return {"rank": rank, "policy": policy,
            "sweeps": sweeps, "action_tests": action_tests}


def tree(graph, solution, node):
    rank, policy = solution["rank"], solution["policy"]
    assert node in rank
    if rank[node] == 0:
        return {"stop": True}
    action = policy[node]
    kids = graph[node][action]
    assert all(rank[child] < rank[node] for child in kids.values())
    return {"action": action, "branches": {
        str(out): tree(graph, solution, child)
        for out, child in sorted(kids.items())}}


def plan_statistics(plan):
    if "stop" in plan:
        return {"internal_nodes": 0, "leaves": 1, "max_depth": 0}
    sub = [plan_statistics(child) for child in plan["branches"].values()]
    return {"internal_nodes": 1 + sum(s["internal_nodes"] for s in sub),
            "leaves": sum(s["leaves"] for s in sub),
            "max_depth": 1 + max(s["max_depth"] for s in sub)}


def certify(plan, node):
    """Check public tree against EVERY compatible candidate, not truth only."""
    if "stop" in plan:
        assert returned(node)
        return [node]
    kids, _ = successor(node, plan["action"])
    assert set(plan["branches"]) == {str(out) for out in kids}
    leaves = []
    for out, child in kids.items():
        leaves.extend(certify(plan["branches"][str(out)], child))
    return leaves


def execute(plan, node, true_world, physical_state):
    """Evaluator supplies actual outputs; planning never receives this index."""
    transcript = []
    while "stop" not in plan:
        action = plan["action"]
        theta, _ = WORLDS[true_world]
        out, physical_state = transition(theta, physical_state, action)
        kids, _ = successor(node, action)
        node = kids[out]
        assert node[true_world] == physical_state
        transcript.append([action, out])
        plan = plan["branches"][str(out)]
    assert returned(node)
    return node, physical_state, transcript


def forced_first(graph, return_solution, start, action):
    kids = graph[start][action]
    if not all(child in return_solution["rank"] for child in kids.values()):
        return None
    return {"action": action, "branches": {
        str(out): tree(graph, return_solution, child)
        for out, child in sorted(kids.items())}}


def main():
    started = time.perf_counter()
    graph, transition_evals = build_graph(INITIAL)
    return_solution = solve(graph)
    pair_solutions = {pair: solve(graph, pair) for pair in combinations(range(4), 2)}

    # No primitive globally resets, and no single output value names a state.
    for theta in (0, 1):
        for action in ACTIONS:
            assert len({transition(theta, q, action)[1] for q in range(7)}) > 1
            for output in (0, 1):
                assert sum(transition(theta, q, action)[0] == output
                           for q in range(7)) > 1
        assert all((DEAD, phi) not in EQUIV[theta] for phi in (0, 1))

    initial_b = forced_first(graph, return_solution, INITIAL, "b")
    assert initial_b is None

    source = {"action": "a", "branches": {"1": {
        "action": "a", "branches": {"0": {"stop": True},
                                      "1": {"stop": True}}}}}
    source_leaves = certify(source, INITIAL)
    assert sorted(mask(node) for node in source_leaves) == [3, 12]
    acquired = {}
    executions = []
    for node in source_leaves:
        start = canonical(node)
        target = forced_first(graph, return_solution, start, "b")
        assert target is not None
        leaves = certify(target, start)
        assert all(len(members(leaf)) == 1 for leaf in leaves)
        acquired[str(mask(start))] = {
            "target_plan": target,
            "plan_statistics": plan_statistics(target),
            "post_source_world_count": len(members(start))}

    for true_world, (theta, phi) in enumerate(WORLDS):
        node, physical, source_log = execute(source, INITIAL, true_world, phi)
        learned_start = canonical(node)
        target = acquired[str(mask(learned_start))]["target_plan"]
        final, physical, target_log = execute(target, learned_start, true_world, physical)
        assert len(members(final)) == 1 and physical == phi
        assert source_log == [["a", 1], ["a", theta]]
        assert target_log == [["b", phi], ["a" if theta == 0 else "b", 0]]
        executions.append({"evaluator_world": [theta, phi],
                           "source_transcript": source_log,
                           "target_transcript": target_log,
                           "primitive_actions": len(source_log) + len(target_log),
                           "final_world_mask": mask(final)})

    # Direct conventional planner: explicit singleton-and-return terminal goal.
    # Pair separation alone permits an early stop on other-world branches.
    full_solution = solve(graph, singleton=True)
    full_plan = tree(graph, full_solution, INITIAL)
    full_leaves = certify(full_plan, INITIAL)
    assert all(len(members(leaf)) == 1 for leaf in full_leaves)
    assert plan_statistics(full_plan)["max_depth"] == 4

    # Explore all choices of separated pair, using each pair's independently
    # synthesized minimum-depth witness. This supplements, not proves, confluence.
    terminal_by_truth = defaultdict(set)
    stage_counts, traces_checked = set(), 0

    def explore(start, truth, physical, stages, events):
        nonlocal traces_checked
        choices = []
        for pair in combinations(members(start), 2):
            sol = pair_solutions[pair]
            if start in sol["rank"]:
                choices.append(tree(graph, sol, start))
        if not choices:
            terminal_by_truth[truth].add(mask(start))
            stage_counts.add(stages)
            traces_checked += 1
            return
        assert stages < len(WORLDS) - 1
        for plan in choices:
            leaves = certify(plan, start)
            assert len({mask(leaf) for leaf in leaves}) >= 2
            nxt, physical_nxt, log = execute(plan, start, truth, physical)
            assert len(members(nxt)) < len(members(start))
            explore(canonical(nxt), truth, physical_nxt,
                    stages + 1, events + len(log))

    for truth, (_, phi) in enumerate(WORLDS):
        explore(INITIAL, truth, phi, 0, 0)
        assert terminal_by_truth[truth] == {1 << truth}

    # Read-only predictor destruction check: b followed by the wrong return
    # lands in D, where all future output predictions are trivially exact.
    # It is deliberately a counterexample to prediction sufficiency, NOT the
    # conventional comparator used to claim an algorithmic improvement.
    for theta in (0, 1):
        _, q = transition(theta, 0, "b")
        _, q = transition(theta, q, "b" if theta == 0 else "a")
        assert q == DEAD
        assert all(transition(theta, q, action) == (0, DEAD) for action in ACTIONS)
        assert transition(theta, 0, "a")[0] == 1

    solutions = [return_solution, full_solution] + list(pair_solutions.values())
    result = {
        "status": "PASS",
        "scope": "exact finite stipulated class; standard strong-belief planner",
        "pointed_worlds": len(WORLDS),
        "candidate_machines": 2,
        "states_per_candidate": 7,
        "action_count": 2,
        "class_transition_entries": 28,
        "class_output_entries": 28,
        "reachable_epistemic_nodes": len(graph),
        "crude_node_upper_bound": 8 ** 4 - 1,
        "graph_candidate_transition_evaluations": transition_evals,
        "fixed_point_solves": len(solutions),
        "fixed_point_sweeps": sum(s["sweeps"] for s in solutions),
        "fixed_point_action_tests": sum(s["action_tests"] for s in solutions),
        "b_first_return_before_source": False,
        "source_plan": source,
        "source_plan_statistics": plan_statistics(source),
        "acquired_target_plans": acquired,
        "all_true_world_executions": executions,
        "standard_planner_full_plan": full_plan,
        "standard_planner_full_plan_statistics": plan_statistics(full_plan),
        "minimum_pair_worst_case_depths": {
            str(pair): sol["rank"].get(INITIAL) for pair, sol in pair_solutions.items()},
        "greedy_minimum_witness_paths_checked": traces_checked,
        "greedy_successful_stage_counts": sorted(stage_counts),
        "terminal_truth_cells": {str(k): sorted(v) for k, v in terminal_by_truth.items()},
        "arithmetic": "exact Python integer/finite-set decisions; no stochastic sampling",
        "elapsed_seconds_unbenchmarked": time.perf_counter() - started,
        "limitations": [
            "synthetic stipulated transition class and allowed anchor prior",
            "no novelty, physical transfer, or speed advantage over strong planning",
            "search counts exclude human derivation/development effort",
            "no stochastic observations, approximate return, hidden resource protection",
            "newly licensed means immediate execution after paid calibration",
            "confluence proved separately; finite witness exploration is only a check"]}
    out = Path(__file__).with_name("RETURNING_ACCESS_CHECK.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in (
        "status", "reachable_epistemic_nodes", "graph_candidate_transition_evaluations",
        "fixed_point_solves", "fixed_point_sweeps", "fixed_point_action_tests",
        "b_first_return_before_source", "greedy_minimum_witness_paths_checked",
        "greedy_successful_stage_counts", "terminal_truth_cells",
        "elapsed_seconds_unbenchmarked")}, indent=2))


if __name__ == "__main__":
    main()
