#!/usr/bin/env python3
"""Exact admission checks for PROOF.txt; not numerical proof of a generic witness."""
from fractions import Fraction as F
from itertools import product, combinations
import json
from pathlib import Path
import time


def kronecker(a, b):
    return [[x * y for x in ar for y in br] for ar in a for br in b]


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def bell_projector(x, z):
    vec = [F(0) for _ in range(4)]
    vec[x] = F(1)
    vec[2 + (1 ^ x)] = F((-1) ** z)
    return [[a * b / 2 for b in vec] for a in vec]


def erase(m, n, site):
    """Normalized partial trace on a binary site, counted left to right."""
    dim = 2 ** n
    bit = n - 1 - site
    mask = 1 << bit
    result = [[F(0) for _ in range(dim)] for _ in range(dim)]
    for i in range(dim):
        for j in range(dim):
            if (i & mask) != (j & mask):
                continue
            i0, j0 = i & ~mask, j & ~mask
            result[i][j] = (m[i0][j0] + m[i0 | mask][j0 | mask]) / 2
    return result


def main():
    start_w, start_c = time.perf_counter(), time.process_time()
    blocks = [kronecker(eye(2), bell_projector(x, z))
              for x, z in product(range(2), repeat=2)]
    expected = [[F(int(i == j), 4) for j in range(8)] for i in range(8)]
    assert all(erase(block, 3, 1) == expected for block in blocks)
    assert all(sum(block[i][i] for i in range(8)) == 2 for block in blocks)
    assert all(sum(blocks[u][i][j] for u in range(4)) == F(int(i == j))
               for i in range(8) for j in range(8))
    # R_u E_2(R_u) has trace 1/2, versus Tr R_u=2: survival 1/4.
    compressed_traces = []
    for block in blocks:
        tr = sum(block[i][j] * expected[j][i] for i in range(8) for j in range(8))
        assert tr == F(1, 2)
        compressed_traces.append(str(tr))
    # Three macroscopic slabs can have arbitrary L>=1. Check cut edge counts
    # at unit slab length, which then scale exactly by L.
    matchings = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]
    cuts = []
    for second in range(1, 4):
        left = {0, second}
        crossing = [sum(int((a in left) != (b in left)) for a, b in matching)
                    for matching in matchings]
        assert sorted(crossing) == [0, 2, 2]
        assert sum(crossing) == 4
        cuts.append({"left_tasks_zero_based": sorted(left),
                     "crossing_per_slab": crossing,
                     "cut_rank_log2_per_L": 4,
                     "balanced_dimension_log2_per_L": 6})
    result = {"status": "PASS", "arithmetic": "exact Fraction",
              "block_count": 4, "block_rank": 2,
              "E2_Ru_identity": "I_8/4 for every u",
              "compressed_input_trace": 2,
              "compressed_output_traces": compressed_traces,
              "same_label_survival": "1/4", "balanced_cuts": cuts,
              "wall_seconds": time.perf_counter() - start_w,
              "cpu_seconds": time.process_time() - start_c,
              "generic_witness_validation": "NOT_CLAIMED"}
    path = Path(__file__).with_name("RESULT.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
