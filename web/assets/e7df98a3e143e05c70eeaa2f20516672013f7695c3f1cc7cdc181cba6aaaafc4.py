"""Finite smoke checks for the CYCLE2 wrapper; not a proof or Li validation."""

from fractions import Fraction as F

from cycle2_bipartite_sampler import sample_bipartite_perfect_matching


def _first_integer(bound: int) -> int:
    return 0


def _all_positive_signs(columns):
    return (1,) * len(columns)


def check_unequal_rational_marginals() -> None:
    edges = ((0, 0), (0, 1), (1, 0), (1, 1))
    x = (F(1, 3), F(2, 3), F(2, 3), F(1, 3))
    features = ((F(0),),) * 4
    for level in (0, 1, 2, 4):
        sample = sample_bipartite_perfect_matching(
            2, 2, edges, x, features, level, _first_integer, _all_positive_signs
        )
        assert len(sample.matching_edge_ids) == 2
        assert sample.feature_error == (F(0),)
        assert max(map(abs, sample.feature_error)) <= sample.path_bound


def check_cycle_obstruction(k: int) -> None:
    # Cycle order: L_i-R_i, then L_(i+1)-R_i.
    edges = tuple(
        edge
        for i in range(k)
        for edge in ((i, i), ((i + 1) % k, i))
    )
    x = (F(1, 2),) * (2 * k)
    features = tuple((F(1 if edge_id % 2 == 0 else -1),) for edge_id in range(2 * k))

    outputs = []
    for draw in (0, 1):
        def randbelow(bound: int, draw: int = draw) -> int:
            return draw % bound

        sample = sample_bipartite_perfect_matching(
            k, k, edges, x, features, 1, randbelow, _all_positive_signs
        )
        outputs.append(sample)
        assert len(sample.matching_edge_ids) == k
        assert abs(sample.feature_error[0]) == k
        assert abs(sample.feature_error[0]) <= sample.path_bound
    assert outputs[0].matching_edge_ids != outputs[1].matching_edge_ids


if __name__ == "__main__":
    check_unequal_rational_marginals()
    for cycle_half_length in (2, 3, 5):
        check_cycle_obstruction(cycle_half_length)
    print("CYCLE2 exact smoke checks passed (finite scope only).")
