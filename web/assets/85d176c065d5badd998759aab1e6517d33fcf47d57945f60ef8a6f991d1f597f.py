#!/usr/bin/env python3
"""Exact finite check for an adaptive action-selection gap in a 4-state HMM."""

from itertools import product

ACTIONS = ("A", "B", "C")
HYPOTHESES = ("h1", "h2", "h3", "h4")
EMISSION = {
    "h1": {"A": 0, "B": 0, "C": 0},
    "h2": {"A": 0, "B": 1, "C": 0},
    "h3": {"A": 1, "B": 0, "C": 0},
    "h4": {"A": 1, "B": 0, "C": 1},
}


def fixed_trace(h, actions):
    return tuple(EMISSION[h][a] for a in actions)


def fixed_likelihood(h, actions, observations):
    return int(tuple(observations) == fixed_trace(h, actions))


def adaptive_trace(h):
    first = EMISSION[h]["A"]
    second_action = "B" if first == 0 else "C"
    second = EMISSION[h][second_action]
    return ("A", second_action), (first, second)


def prior_series_likelihood(trace):
    """F(z)=uniform-prior probability of a joint action/observation word."""
    actions = tuple(a for a, _ in trace)
    observations = tuple(y for _, y in trace)
    return sum(fixed_likelihood(h, actions, observations) for h in HYPOTHESES) / 4


def main():
    # All adaptive policy transcripts are distinct and use two real actions.
    adaptive = {h: adaptive_trace(h) for h in HYPOTHESES}
    assert len({(a, y) for a, y in adaptive.values()}) == 4
    assert all(len(a) == 2 and len(y) == 2 for a, y in adaptive.values())

    # Full-data open-loop schedules of two actions: every ordered schedule
    # over the complete action alphabet has a collision.
    fixed_rows = []
    for actions in product(ACTIONS, repeat=2):
        signatures = {h: fixed_trace(h, actions) for h in HYPOTHESES}
        assert len(set(signatures.values())) < 4, (actions, signatures)
        fixed_rows.append(("".join(actions), len(set(signatures.values()))))

    # The strongest fixed full-data schedule ABC separates every state.
    abc = {h: fixed_trace(h, ACTIONS) for h in HYPOTHESES}
    assert len(set(abc.values())) == 4

    # One observation gives at most two transcripts, so no one-action policy
    # can identify all four states, even when its first action is randomized.
    assert all(len({EMISSION[h][a] for h in HYPOTHESES}) <= 2 for a in ACTIONS)

    # Exact 4x4 Hankel minor: rows and columns are the three-step code traces.
    code_traces = {
        h: tuple(zip(ACTIONS, fixed_trace(h, ACTIONS))) for h in HYPOTHESES
    }
    hankel_minor = [
        [prior_series_likelihood(code_traces[h] + code_traces[j]) for j in HYPOTHESES]
        for h in HYPOTHESES
    ]
    assert hankel_minor == [
        [0.25 if i == j else 0.0 for j in range(4)] for i in range(4)
    ]

    print("adaptive_policy,actions,observations")
    for h in HYPOTHESES:
        actions, observations = adaptive[h]
        print(f"{h},{''.join(actions)},{''.join(map(str, observations))}")
    print("fixed_two_action_schedules,distinct_full_data_signatures")
    for actions, n_signatures in fixed_rows:
        print(f"{actions},{n_signatures}")
    print("fixed_ABC_signatures=" + ";".join(
        f"{h}:{''.join(map(str, abc[h]))}" for h in HYPOTHESES
    ))
    print("rank4_hankel_minor=PASS")
    print("adaptive_minimax_actions=2;fixed_open_loop_minimax_actions=3")
    print("PASS")


if __name__ == "__main__":
    main()
