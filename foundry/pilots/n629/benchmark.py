"""One bounded scenario/method per process; setup is charged to all methods."""
import json
from random import Random
import sys
import time

from common import source_sampler
from reference import enumerate_pairs, rejection, valid

SCENARIOS = [
    {"id": "disjoint_m6_w2", "m": 6, "blocks": [[1, 2, 4], [8, 16, 32]]},
    {"id": "disjoint_m8_w2", "m": 8, "blocks": [[1<<i for i in range(4)], [1<<i for i in range(4, 8)]]},
    {"id": "disjoint_m10_w2", "m": 10, "blocks": [[1<<i for i in range(5)], [1<<i for i in range(5, 10)]]},
    {"id": "coordinate_m5_w5", "m": 5, "blocks": [[1<<i] for i in range(5)]},
    {"id": "common_kernel_m8_w4", "m": 8, "blocks": [[1<<i] for i in range(4)]},
    {"id": "large_m30_w3", "m": 30, "blocks": [[1<<i for i in range(j*10, (j+1)*10)] for j in range(3)]},
] + [{"id": f"repeated_m4_w{w}", "m": 4, "blocks": [[1, 2, 4, 8]]*w}
     for w in (1, 3, 5, 7)]


def run(index, method, replicate):
    case = SCENARIOS[index]
    m, blocks = case["m"], case["blocks"]
    seed, count = 62900 + replicate, 16
    rng = Random(seed)
    # Module loading is charged by the process receipt for every method, but
    # excluded from the algorithm timer consistently with reference imports.
    Sampler = source_sampler() if method == "fpt" else None
    start = time.perf_counter()
    result = dict(case, method=method, replicate=replicate, seed=seed, requested_draws=count,
                  candidate_pairs=4**m, input_matrix_bits=m*sum(map(len, blocks)),
                  input_json_bytes=len(json.dumps({"m": m, "blocks": blocks}, sort_keys=True).encode()),
                  expanded_terms=5**len(blocks))
    if method == "fpt":
        sampler = Sampler(m, blocks)
        prepared = time.perf_counter()
        draws = [sampler.draw(rng) for _ in range(count)]
        result.update(exact_count=sampler.total, merged_terms=len(sampler.terms), status="passed")
    elif method == "brute":
        if 4**m > 2**20:
            return dict(result, status="skipped_pair_budget", max_candidate_pairs=2**20)
        pairs = enumerate_pairs(m, blocks)
        prepared = time.perf_counter()
        draws = [pairs[rng.randrange(len(pairs))] for _ in range(count)]
        result.update(exact_count=len(pairs), status="passed")
    elif method == "rejection":
        prepared = time.perf_counter()
        rejected = rejection(m, blocks, count, seed)
        draws = rejected.pop("draws")
        result.update(rejected)
    else:
        raise ValueError(method)
    end = time.perf_counter()
    # Validation time is reported separately from algorithm work for every arm.
    assert all(valid(blocks, *pair) for pair in draws)
    result.update(setup_wall_seconds=prepared-start, draw_wall_seconds=end-prepared,
                  algorithm_wall_seconds=end-start, validated_draws=len(draws), draws=draws)
    return result


if __name__ == "__main__":
    print(json.dumps(run(int(sys.argv[1]), sys.argv[2], int(sys.argv[3])), sort_keys=True))
