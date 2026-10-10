"""Four-state exact check of finite ancestry with state-carrying mode switches."""

from __future__ import annotations

from fractions import Fraction as F
from math import sqrt
from random import Random

from verify import invariant_and_response


def chain(delta: F):
    # B=(1/2)nu+(1/2)I, nu=(4/5,1/5).
    b = [[F(9, 10), F(1, 10)], [F(2, 5), F(3, 5)]]
    alpha = [F(1, 2), F(1, 2)]
    dalpha = [F(-1, 2), F(1, 2)]
    p = [[F(0) for _ in range(4)] for _ in range(4)]
    dp = [[F(0) for _ in range(4)] for _ in range(4)]
    for i in range(2):
        for x in range(2):
            s = 2 * i + x
            for j in range(2):
                for y in range(2):
                    t = 2 * j + y
                    # On a switch, the local bit becomes the destination mode.
                    # On a reset event with j=i, it is carried unchanged.
                    carry = F(y == (j if j != i else x))
                    p[s][t] = (1 - delta) * F(i == j) * b[x][y] + delta * alpha[j] * carry
                    dp[s][t] = delta * dalpha[j] * carry
    assert all(sum(row) == 1 for row in p)
    assert all(sum(row) == 0 for row in dp)
    return p, dp


def estimate(delta_denominator: int, rng: Random) -> tuple[int, int, int]:
    """At theta=0, Q(j,i)=alpha(i)=1/2; score is one sign per reset."""
    present_mode = rng.randrange(2)
    current = present_mode
    score = 2 * present_mode - 1  # alpha'/alpha
    forward_record: list[tuple[str, int]] = []
    reset_count = 0
    while True:
        if rng.randrange(delta_denominator) == 0:
            predecessor = rng.randrange(2)
            score += 2 * predecessor - 1  # Q'/Q
            forward_record.append(("carry", current if predecessor != current else -1))
            current = predecessor
            reset_count += 1
        elif rng.randrange(2) == 0:
            # This no-reset B transition used its state-independent atom.
            local_bit = int(rng.randrange(5) == 0)  # nu=(4/5,1/5)
            break
        else:
            forward_record.append(("residual", -1))  # B residual is identity
    for kind, dest in reversed(forward_record):
        if kind == "carry" and dest >= 0:
            local_bit = dest
    a = local_bit * (1 if present_mode == 0 else 2)
    return a * score, len(forward_record) + 1, reset_count


def main() -> None:
    for denom in [10, 100, 1000, 10000]:
        d = F(1, denom)
        p, dp = chain(d)
        _, _, response = invariant_and_response(p, dp, [F(0), F(1), F(0), F(2)])
        assert response == F(1, 10) + F(9, 10) * d * d
        expected_ancestor_steps = F(2) / (1 - d)
        expected_resets = F(2) * d / (1 - d)
        print(f"delta={d}, response={response}, E ancestor steps={expected_ancestor_steps}, E reset events={expected_resets}")
        if denom == 1000:
            rng = Random(20261010)
            draws = [estimate(denom, rng) for _ in range(300_000)]
            mean = sum(z for z, _, _ in draws) / len(draws)
            var = sum((z - mean) ** 2 for z, _, _ in draws) / len(draws)
            se = sqrt(var / len(draws))
            mean_steps = sum(t for _, t, _ in draws) / len(draws)
            mean_resets = sum(n for _, _, n in draws) / len(draws)
            assert abs(mean - float(response)) < 5 * se
            print(f"  MC mean={mean:.8f}, exact={float(response):.8f}, se={se:.4g}, mean_steps={mean_steps:.6f}, mean_resets={mean_resets:.6f}")


if __name__ == "__main__":
    main()
