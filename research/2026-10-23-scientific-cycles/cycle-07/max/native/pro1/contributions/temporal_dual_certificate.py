#!/usr/bin/env python3
"""Focused exact rational dual certificate from the unchanged Cycle5 source.

Verifies the full prefix-operator certificate at k=4. This does not use a
floating-point eigensolver and does not claim an all-k formula.
"""
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
from math import comb
import argparse
import hashlib
import json
import platform
import resource
import time
import zipfile


SOURCE_NAME = "Astra_Amplification_Cycle5_PRO1_20261022"
SOURCE_SHA256 = "7cc0ba564d5e9d483527b9c4f55928d17bcba0b27db9604875286faa27128654"
MEMBER = SOURCE_NAME + "/contributions/four_call_representation.json"


def sparse_string(matrix):
    return [[i, j, str(v)] for (i, j), v in sorted(matrix.items()) if v]


def run(source_zip):
    started = time.perf_counter()
    blob = source_zip.read_bytes()
    digest = hashlib.sha256(blob).hexdigest()
    assert digest == SOURCE_SHA256
    with zipfile.ZipFile(source_zip) as archive:
        representation = json.loads(archive.read(MEMBER))
    input_words = representation["input_words"]
    prefixes = representation["bath_prefix_words"]
    entries = representation["bulk_drift_coefficients"]["1"]
    k = len(input_words[0])
    assert k == 4 and len(prefixes) == 16 and len(input_words) == 81
    q = [sum(c != 0 for c in x) for x in input_words]
    sigma = [F(1, 2 ** (k + r)) for r in q]
    assert sum(sigma) == 1

    def contract(tau):
        h = defaultdict(F)
        for i, u, j, v, a in entries:
            h[i, j] += tau.get((v, u), F(0)) * a
        for i in range(len(input_words)):
            h[i, i] += 2 * q[i] - k
        h = {ij: value for ij, value in h.items() if value}
        assert all(i != j and q[i] == q[j] for i, j in h)
        assert all(h.get((j, i), 0) == value for (i, j), value in h.items())
        variance = sum(sigma[i] * value * value for (i, j), value in h.items())
        operator = defaultdict(F)
        for i, u, j, v, a in entries:
            # Tr_A[(sigma H tensor I) G1] uses its (j,i) entry.
            operator[u, v] += sigma[j] * h.get((j, i), F(0)) * a
        operator = {uv: value for uv, value in operator.items() if value}
        assert all(operator.get((v, u), 0) == value for (u, v), value in operator.items())
        return h, variance, operator

    prefix_q = [sum(c == 1 for c in word) for word in prefixes]
    tau_sym = {(u, v): F(1, (k + 1) * comb(k, prefix_q[u]))
               for u in range(len(prefixes)) for v in range(len(prefixes))
               if prefix_q[u] == prefix_q[v]}
    assert sum(tau_sym.get((u, u), 0) for u in range(len(prefixes))) == 1
    h, variance, operator = contract(tau_sym)
    assert variance == F(17, 16)
    assert all(value <= 0 for (u, v), value in operator.items() if u != v)
    row_sums = [sum(operator.get((u, v), 0) for v in range(len(prefixes)))
                for u in range(len(prefixes))]
    assert all(total == variance for total in row_sums)
    # Therefore operator - variance*I is exactly a real weighted graph
    # Laplacian. Its quadratic form is sum_{u<v} -L_uv |z_u-z_v|^2 >= 0.
    laplacian_edges = [[u, v, str(-value)] for (u, v), value in sorted(operator.items())
                       if u < v and value]
    assert all(F(weight) > 0 for u, v, weight in laplacian_edges)
    expectation = sum(tau_sym.get((v, u), 0) * value
                      for (u, v), value in operator.items())
    assert expectation == variance

    tau_uniform = {(u, u): F(1, len(prefixes)) for u in range(len(prefixes))}
    hu, vu, lu = contract(tau_uniform)
    assert vu == F(561, 512)
    assert len({lu.get((u, u), F(0)) for u in range(len(prefixes))}) > 1
    return {
        "status": "PASS exact rational full-operator certificate",
        "scope": "k=4 only; no large-k or physical coding consequence asserted by this replay",
        "source_zip": str(source_zip),
        "source_bytes": len(blob),
        "source_sha256": digest,
        "source_member": MEMBER,
        "dual_tau": "P_sym,4 / 5",
        "v4": str(variance),
        "A4": "17*ln(2)/128 per block",
        "optimizer": "X=-(ln(2)/2)*sigma*H_sym",
        "operator_certificate": "T(sigma H_sym)=(17/16)I+weighted graph Laplacian",
        "all_row_sums": str(row_sums[0]),
        "laplacian_edges": laplacian_edges,
        "H_sym_sparse": sparse_string(h),
        "T_sigma_H_sym_sparse": sparse_string(operator),
        "uniform_prefix_variance": str(vu),
        "uniform_prefix_not_stationary": True,
        "uniform_gradient_diagonal_values": sorted({str(lu.get((u, u), F(0))) for u in range(len(prefixes))}),
        "wall_seconds": time.perf_counter() - started,
        "max_rss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "python": platform.python_version(),
        "research_discovery_cost": "unknown; replay is not discovery cost",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    root = Path(__file__).resolve().parents[1]
    parser.add_argument("--source", type=Path,
                        default=root / "preserved" / (SOURCE_NAME + ".zip"))
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("temporal_dual_certificate.json"))
    args = parser.parse_args()
    result = run(args.source)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    excluded = {"H_sym_sparse", "T_sigma_H_sym_sparse", "laplacian_edges"}
    print(json.dumps({key: value for key, value in result.items() if key not in excluded}, indent=2))
