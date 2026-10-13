"""Exhaustive exact checks for the common-radical theorem and counterexamples."""

from collections import Counter
from itertools import combinations
from pathlib import Path
import json

from joint_quadratic import (
    all_outputs,
    balance_count,
    common_radical_certificate,
    combinations_are_balanced,
    output,
    radical_balance_test,
    sample_fiber,
    verify_certificate,
    vectorial_balanced_radical_test,
)


def all_forms(n: int):
    pairs = list(combinations(range(n), 2))
    for c in range(2):
        for linear in range(1 << n):
            for pair_mask in range(1 << len(pairs)):
                terms = tuple(pairs[j] for j in range(len(pairs))
                              if (pair_mask >> j) & 1)
                yield (c, linear, terms)


def fiber_counts(n: int, forms):
    return Counter(all_outputs(n, forms))


class FixedBits:
    def __init__(self, value: int):
        self.value = value

    def getrandbits(self, n: int) -> int:
        assert 0 <= self.value < (1 << n)
        return self.value


def check_exhaustive_n3():
    forms = list(all_forms(3))
    assert len(forms) == 128
    balanced = [q for q in forms if balance_count(3, q) == 4]
    assert all(radical_balance_test(3, q) for q in balanced)
    assert all((balance_count(3, q) == 4) == radical_balance_test(3, q)
               for q in forms)

    balanced_pairs = 0
    surj_pairs = 0
    uniform_pairs = 0
    nonuniform_surj_pairs = 0
    sampler_seed_checks = 0
    output_histogram = Counter()

    for q1 in balanced:
        for q2 in balanced:
            pair = (q1, q2)
            balanced_pairs += 1
            counts = fiber_counts(3, pair)
            equal_fibers = (len(counts) == 4 and set(counts.values()) == {2})
            assert vectorial_balanced_radical_test(3, pair) == equal_fibers
            output_histogram[tuple(counts.get(b, 0) for b in range(4))] += 1
            cert = common_radical_certificate(3, pair)
            if cert is None:
                continue
            assert verify_certificate(3, pair, cert)
            surj_pairs += 1
            if len(counts) == 4 and len(set(counts.values())) == 1:
                uniform_pairs += 1
            else:
                nonuniform_surj_pairs += 1
                raise AssertionError("common-radical surjectivity did not yield uniform fibers")
            # Enumerate every sampler seed for every target. Each target output
            # point must have exactly 2^k seeds, and be in the requested fiber.
            for target in range(4):
                images = Counter()
                for seed in range(8):
                    corrected = sample_fiber(3, pair, target, cert, FixedBits(seed))
                    assert output(3, pair, corrected) == target
                    images[corrected] += 1
                assert len(images) == 2
                assert set(images.values()) == {4}
                sampler_seed_checks += 1

    return {
        "n": 3,
        "all_quadratic_forms": len(forms),
        "individually_balanced_forms": len(balanced),
        "ordered_individually_balanced_pairs": balanced_pairs,
        "pairs_with_surjective_common_radical_map": surj_pairs,
        "pairs_with_uniform_joint_fibers_and_surjective_common_radical_map": uniform_pairs,
        "surjective_common_radical_counterexamples": nonuniform_surj_pairs,
        "exhaustively_checked_target_certificates_and_seed_maps": sampler_seed_checks,
        "fiber_count_histograms_for_balanced_pairs": {
            str(list(key)): value for key, value in sorted(output_histogram.items())
        },
    }


def check_examples():
    # Two genuinely quadratic, individually balanced coordinates with all joint
    # targets present but unequal sizes: 10 on the diagonal, 6 off it.
    unequal = (
        (0, 1 << 4, ((0, 1),)),
        (0, 1 << 4, ((2, 3),)),
    )
    counts_unequal = fiber_counts(5, unequal)
    assert balance_count(5, unequal[0]) == 16
    assert balance_count(5, unequal[1]) == 16
    assert counts_unequal == Counter({0: 10, 3: 10, 1: 6, 2: 6})
    assert common_radical_certificate(5, unequal) is None

    # Identical balanced quadratics: the two off-diagonal joint fibers are empty.
    missing = ((0, 1 << 2, ((0, 1),)), (0, 1 << 2, ((0, 1),)))
    counts_missing = fiber_counts(3, missing)
    assert balance_count(3, missing[0]) == 4
    assert balance_count(3, missing[1]) == 4
    assert counts_missing == Counter({0: 4, 3: 4})

    # Rank(L)<k does not imply unequal or missing fibers. Every output
    # combination is balanced here, so all four fibers have size 2.
    uniform_rank_deficient = (
        (0, 1 << 2, ((0, 1),)),
        (0, (1 << 0) | (1 << 2), ((0, 1),)),
    )
    counts_uniform = fiber_counts(3, uniform_rank_deficient)
    assert balance_count(3, uniform_rank_deficient[0]) == 4
    assert balance_count(3, uniform_rank_deficient[1]) == 4
    assert counts_uniform == Counter({0: 2, 1: 2, 2: 2, 3: 2})
    assert common_radical_certificate(3, uniform_rank_deficient) is None
    assert combinations_are_balanced(3, uniform_rank_deficient)
    assert vectorial_balanced_radical_test(3, uniform_rank_deficient)

    return {
        "unequal_all_targets_present": {str(k): counts_unequal.get(k, 0) for k in range(4)},
        "missing_targets": {str(k): counts_missing.get(k, 0) for k in range(4)},
        "uniform_fibers_despite_rank_deficient_L": {str(k): counts_uniform.get(k, 0) for k in range(4)},
    }


def main():
    result = {
        "scope": "exact finite exhaustive diagnostics; no empirical or physical claim",
        "n3_exhaustive": check_exhaustive_n3(),
        "explicit_examples": check_examples(),
    }
    out = Path(__file__).with_name("evidence") / "exhaustive_results.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

