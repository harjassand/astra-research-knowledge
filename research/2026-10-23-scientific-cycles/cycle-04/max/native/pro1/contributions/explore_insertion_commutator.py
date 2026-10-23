#!/usr/bin/env python3
"""Finite principal sections of an infinite-Fock commutator.

This is not a reflecting bath, an invariant-state calculation, or an
all-length positivity proof. Two extra levels guard the tested principal
section. The substantive corrector result uses ||A|| <= 4 instead.
"""
from itertools import product
import json
import time
import resource
import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import eigsh


def run():
    records = []
    for depth in (3, 4, 5, 6):
        words = [()] + [w for length in range(1, depth + 3)
                        for w in product((1, 2), repeat=length)]
        index = {w: j for j, w in enumerate(words)}
        size = len(words)
        shift = lil_matrix((size, size))
        for word, j in index.items():
            if (1,) + word in index:
                shift[index[(1,) + word], j] = 1
        shift = shift.tocsr()
        for ratio in (0.2, 0.7, 0.99):
            insertion = lil_matrix((size, size))
            for word, j in index.items():
                for k in range(len(word) + 1):
                    new_word = word[:k] + (1,) + word[k:]
                    if new_word in index:
                        insertion[index[new_word], j] += ratio ** k
            insertion = insertion.tocsr()
            commutator = ((shift.T - shift) @ (insertion + insertion.T)
                          - (insertion + insertion.T) @ (shift.T - shift))
            keep = sum(2 ** j for j in range(depth + 1))
            principal = commutator[:keep, :keep]
            minimum = float(eigsh(principal, k=1, which="SA",
                                  return_eigenvectors=False)[0])
            records.append({"depth": depth, "ratio": ratio,
                            "principal_minimum_eigenvalue": minimum})
    return records


if __name__ == "__main__":
    wall = time.perf_counter()
    cpu = time.process_time()
    values = run()
    print(json.dumps({
        "scope": "Finite floating-point principal-section probe only",
        "commutator": "[S1* - S1, B_r + B_r*] = 2 A_r",
        "global_positive_operator_claim": False,
        "records": values,
        "resources": {
            "wall_seconds": time.perf_counter() - wall,
            "cpu_seconds": time.process_time() - cpu,
            "maximum_rss_platform_units": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        },
    }, indent=2))
