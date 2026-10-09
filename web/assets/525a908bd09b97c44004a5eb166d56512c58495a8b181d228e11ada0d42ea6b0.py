"""Exact finite belief-game solver for the A03 scalar unknown-gain example.

All numeric quantities are integer-scaled: x units are quarters; observation
units are eighths. Disturbance w in {-1/4,0,1/4}, sensor error v in
{-1/8,0,1/8}, actions u in {-3/4,0,3/4}, and safety X=[-1/4,1].
The unknown gain theta is fixed in {-1,+1}; dynamics are x' = theta*u+w.
"""
from functools import lru_cache

THETA = (-1, 1)
ACTIONS = (-2, 0, 2)  # quarter units
W = (-1, 0, 1)        # quarter units
V = (-1, 0, 1)        # eighth units
SAFE_X = (-1, 0, 1, 2, 3, 4)  # quarter units in [-1/4,1]
Q = tuple((th, x) for th in THETA for x in SAFE_X)
Q_INDEX = {q: i for i, q in enumerate(Q)}
N = len(Q)
ALL = (1 << N) - 1

# For each (state-model hypothesis, action), store every possible
# (next-hypothesis, observation) pair and whether every successor is safe.
TRANS = {}
for qi, (theta, _x) in enumerate(Q):
    for a in ACTIONS:
        pairs = set()
        safe = True
        for w in W:
            x_next = theta * a + w
            if x_next not in SAFE_X:
                safe = False
                continue
            q_next = Q_INDEX[(theta, x_next)]
            for v in V:
                y = 2 * x_next + v  # quarter x to eighth y
                pairs.add((q_next, y))
        TRANS[(qi, a)] = (safe, tuple(sorted(pairs)))


def qbits(mask):
    """Indices set in an integer belief mask."""
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def model_count(mask):
    return len({Q[i][0] for i in qbits(mask)})


def successors(mask, action):
    """Return None if unsafe; otherwise map each observation to a belief mask."""
    posts = {}
    for qi in qbits(mask):
        safe, pairs = TRANS[(qi, action)]
        if not safe:
            return None
        for qj, y in pairs:
            posts[y] = posts.get(y, 0) | (1 << qj)
    return posts


def safe_actions(mask, viable):
    allowed = []
    for action in ACTIONS:
        posts = successors(mask, action)
        if posts is not None and all(post in viable for post in posts.values()):
            allowed.append(action)
    return allowed


def greatest_safe_viability_kernel():
    """Greatest fixed point over all nonempty beliefs of safe hypotheses."""
    viable = set(range(1, ALL + 1))
    iterations = 0
    while True:
        iterations += 1
        keep = set()
        for mask in viable:
            if safe_actions(mask, viable):
                keep.add(mask)
        if keep == viable:
            return viable, iterations
        viable = keep


def robust_distinguishing_value(initial, horizon, viable):
    """Minimize worst-case terminal number of consistent models.

    The returned policy is a finite observation tree. Ties minimize the
    worst-case sum of |u| (scaled action units); sensor and table costs are
    charged separately in the report.
    """
    @lru_cache(None)
    def solve(mask, h):
        if h == 0:
            return model_count(mask), 0, None
        candidates = []
        for action in safe_actions(mask, viable):
            posts = successors(mask, action)
            child_rows = {y: solve(post, h - 1) for y, post in sorted(posts.items())}
            worst_models = max(row[0] for row in child_rows.values())
            worst_action_cost = abs(action) + max(row[1] for row in child_rows.values())
            candidates.append((worst_models, worst_action_cost, action, child_rows))
        if not candidates:
            return float("inf"), float("inf"), None
        best = min(candidates, key=lambda row: (row[0], row[1], abs(row[2]), row[2]))
        return best

    return solve(initial, horizon), solve.cache_info()


def main():
    initial = (1 << Q_INDEX[(1, 0)]) | (1 << Q_INDEX[(-1, 0)])
    viable, iterations = greatest_safe_viability_kernel()
    actions = safe_actions(initial, viable)
    value, cache = robust_distinguishing_value(initial, 4, viable)

    print(f"hypotheses={N}; beliefs_enumerated={ALL}; viability_beliefs={len(viable)}")
    print(f"viability_fixpoint_iterations={iterations}")
    print(f"initial_model_count={model_count(initial)}")
    print(f"initial_robust_safe_actions_quarters={actions}")
    print(f"horizon=4; minimum_worst_case_terminal_model_count={value[0]}")
    print(f"selected_first_action_quarters={value[2]}")
    print(f"memoized_belief_horizon_states={cache.currsize}")
    print("known_gain_policy: theta=+1 -> u=+1/2; theta=-1 -> u=-1/2")
    print("known_gain_all_disturbance_states=[1/4,3/4] subset [-1/4,1]")
    print("unknown_gain_robust_policy: u=0; y support is identical for both gains")


if __name__ == "__main__":
    main()
