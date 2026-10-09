"""Small exhaustive checks accompanying v1.txt; not proofs of the lemmas."""

from collections import Counter
from fractions import Fraction
from itertools import permutations, product
from math import factorial


def rank_one_greedy(items):
    """Unit-weight U_{1,3}, with labels breaking ties increasingly."""
    return {min(items)} if items else set()


def snapshot_before_target(initial_bits, order, target, accepted_only):
    C = {i for i, bit in enumerate(initial_bits) if bit}
    accepted = set()
    for t, e in enumerate(order):
        if t == target:
            return frozenset(C)
        C_next = C ^ {e}
        finalized = set(accepted) if accepted_only else set(order[:t])
        passes = (rank_one_greedy(C) & finalized) == (
            rank_one_greedy(C_next) & finalized
        )
        if passes:
            # Real value is the complement of the initial sample bit.
            if e not in C and e in rank_one_greedy(C_next):
                accepted.add(e)
            C = C_next
    raise ValueError("target must be a virtual step in the order")


def check_accepted_only_bias():
    order = (1, 0, 2)
    all_finalized = Counter(
        snapshot_before_target(bits, order, 2, False)
        for bits in product((0, 1), repeat=3)
    )
    accepted_only = Counter(
        snapshot_before_target(bits, order, 2, True)
        for bits in product((0, 1), repeat=3)
    )
    assert set(all_finalized.values()) == {1}
    assert accepted_only == Counter(
        {
            frozenset({1}): 2,
            frozenset({1, 2}): 2,
            frozenset({0}): 1,
            frozenset({0, 2}): 1,
            frozenset(): 1,
            frozenset({2}): 1,
        }
    )
    assert frozenset({0, 1}) not in accepted_only
    assert frozenset({0, 1, 2}) not in accepted_only
    print("accepted-only rank-one snapshot check: PASS")
    print("  all-finalized:", dict(all_finalized))
    print("  accepted-only:", dict(accepted_only))


def check_candidate_flip_identity():
    """Exhaust the identity for a rank-one exact optimizer at p=1/3."""
    weights = (5, 4, 2)
    n = len(weights)
    p, q = Fraction(1, 3), Fraction(2, 3)

    def H(S):
        return frozenset({max(S, key=lambda i: (weights[i], -i))}) if S else frozenset()

    def prob(S):
        return p ** len(S) * q ** (n - len(S))

    lhs = Fraction(0)
    rhs_inner = Fraction(0)
    for mask in range(1 << n):
        P = frozenset(i for i in range(n) if mask >> i & 1)
        candidates = [
            e for e in range(n)
            if e not in P and e in H(P | {e})
        ]
        lhs += prob(P) * sum(weights[e] for e in candidates)
        rhs_inner += prob(P) * sum(weights[e] for e in H(P))
    assert lhs == (q / p) * rhs_inner
    assert lhs == Fraction(154, 27)
    print("candidate flip identity check: PASS", "lhs=", lhs)


def check_k_blocker_probability(max_k=6):
    """Enumerate orders of one target plus k distinct blockers."""
    for k in range(1, max_k + 1):
        universe = tuple(range(k + 1))  # target is 0
        wins = sum(order[0] == 0 for order in permutations(universe))
        assert Fraction(wins, factorial(k + 1)) == Fraction(1, k + 1)
    print(f"distinct-blocker probability check, k=1..{max_k}: PASS")


if __name__ == "__main__":
    check_accepted_only_bias()
    check_candidate_flip_identity()
    check_k_blocker_probability()
