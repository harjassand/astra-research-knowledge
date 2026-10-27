#!/usr/bin/env python3
"""Focused independent checks of the root mixed-quadratic implementation.

Finite exhaustive validation only; this does not run the asymptotic phase
counter.  The tests deliberately include rejection paths and degenerate
retained representations, rather than mirroring the successful fixtures.
"""
from pathlib import Path
import importlib.util
import json
import random
import hashlib

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work_mixed_root/mixed_quadratic_compiler.py"
spec = importlib.util.spec_from_file_location("root_mixed_audit_target", SOURCE)
target = importlib.util.module_from_spec(spec)
spec.loader.exec_module(target)


def rank(values):
    basis = {}
    for value in values:
        while value:
            p = value.bit_length()-1
            if p in basis:
                value ^= basis[p]
            else:
                basis[p] = value
                break
    return len(basis)


def literal_sum(B, terms, b):
    n, half = len(B), 1 << (b-1)
    result = [0]*half
    for x in range(1 << n):
        exponent = sum(coefficient for support, coefficient in terms
                       if all(not (support >> i & 1) or (x >> i & 1)
                              for i in range(n)))
        exponent += half*sum((B[i] >> j & 1)*(x >> i & 1)*(x >> j & 1)
                             for i in range(n) for j in range(i))
        residue = exponent % (2*half)
        result[residue % half] += 1 if residue < half else -1
    return result


def replay(B, cert):
    removed = set(cert["initially_removed"])
    I = cert["pivots"]
    for step in cert["punctures"]:
        R = [j for j in range(len(B)) if j not in removed]
        U = target.independent([target.pack(B[i], R) for i in I])
        word = 0
        for j, u in enumerate(U):
            if step["coefficients"] >> j & 1:
                word ^= u
        support = [R[j] for j in range(len(R)) if word >> j & 1]
        assert support == step["support"]
        assert word and rank(U) == step["rank_before"]
        removed.update(support)
        R2 = [j for j in range(len(B)) if j not in removed]
        assert rank([target.pack(B[i], R2) for i in I]) == step["rank_after"]
        assert step["rank_after"] < step["rank_before"]
    assert sorted(removed) == cert["removed"]
    R = cert["retained"]
    assert R == [i for i in range(len(B)) if i not in removed]
    C, S = cert["low_rank_matrix"], cert["sparse_matrix"]
    assert [a ^ s for a, s in zip(C, S)] == target.restrict(B, R)
    assert target.alternating(C) and target.alternating(S)
    assert rank(C) == cert["low_rank"] <= cert["final_code_dimension"]
    assert target.edge_count(S) == cert["residual_edges"]
    U = cert["code_generators"]
    if "method" not in cert:
        actual_min = min((w.bit_count() for a, w in target.codewords(U) if a),
                         default=len(R)+1)
        assert actual_min == cert["minimum_code_distance"]
        assert [(a ^ c).bit_count() for a, c in zip(target.restrict(B, R), C)] == cert["decoded_column_distances"]


def run():
    records = []
    puncture_rounds = 0
    for n in (2, 4, 6, 8, 10, 12, 16):
        B = [((1 << n)-1) ^ (1 << i) for i in range(n)]
        assert rank(B) == n
        cert = target.candidate(B, tuple(range(n)), (), 1, 0)
        assert cert is not None
        assert cert["removed"] == list(range(n))
        assert not cert["retained"] and not cert["code_generators"]
        assert target.candidate(B, tuple(range(n)), (), 1, 0, n-1) is None
        replay(B, cert)
        puncture_rounds += len(cert["punctures"])
        records.append(dict(family="even full-rank J+I", n=n,
                            erased=len(cert["removed"]),
                            punctures=len(cert["punctures"])))

    star = target.matrix_from_edges(4, [(0, 1), (0, 2), (0, 3)])
    # Empty code fails radius decoding at the centre.
    assert target.candidate(star, (), (), 1, 3) is None
    # All columns decode, but their chosen words form a nonsymmetric matrix.
    assert target.candidate(star, (0,), (), 1, 3) is None
    complete4 = [14, 13, 11, 7]
    # Every retained column decodes to 111: symmetric, but diagonal nonzero.
    assert target.candidate(complete4, (0,), (0,), 1, 3) is None
    edge = target.matrix_from_edges(3, [(0, 1)])
    # Radius decoding succeeds, but the global residual edge budget fails.
    assert target.candidate(edge, (), (), 1, 0) is None
    assert target.acquire(star, 0, 2) is None
    sparse = target.acquire(star, 0, 3)
    assert sparse is not None and not sparse["removed"]
    assert max(sparse["decoded_column_distances"]) == 3
    replay(star, sparse)
    rejects = 5 + 7

    # A surviving code can have dimension larger than the decoded rank.
    redundant = target.candidate(star, (0,), (0,), 1, 0)
    assert redundant is not None
    assert redundant["final_code_dimension"] == 1 and redundant["low_rank"] == 0
    replay(star, redundant)
    # Both pivot indices are outside the retained variables.
    bipartite = target.matrix_from_edges(8, [(i, j) for i in range(4) for j in range(4, 8)])
    external = target.candidate(bipartite, (0, 4), (0, 4), 1, 0)
    assert external is not None and external["low_rank"] == 2
    replay(bipartite, external)

    rng = random.Random(2710202609)
    count_checks = 0
    full_rank8 = [255 ^ (1 << i) for i in range(8)]
    fixtures = [(star, sparse), (star, redundant), (bipartite, external),
                (full_rank8, target.candidate(full_rank8, tuple(range(8)), (), 1, 0))]
    for B, cert in fixtures:
        n = len(B)
        for b in (1, 3):
            terms = [(0, -1), (0, 0), (1, 3), ((1 << n)-1, -5)]
            for _ in range(2*n):
                support = sum(1 << i for i in rng.sample(range(n), min(3, n)))
                terms.append((support, rng.randrange(-9, 10)))
            actual, normalization = target.exact_compiled(B, terms, b, cert)
            expected = literal_sum(B, terms, b)
            assert actual == expected, (B, b, actual, expected)
            count_checks += 1
            records.append(dict(family="independent literal phase sum", n=n,
                                order=1 << b, sum=actual,
                                deleted=len(cert["removed"]),
                                latent_dimension=normalization["latent_dimension"],
                                decoded_rank=cert["low_rank"]))

    published = ROOT / "work_mixed_root/mixed_quadratic_results.json"
    for record in json.loads(published.read_text())["fixtures"]:
        b = record["phase_order"].bit_length()-1
        replay(record["raw_matrix"], record["certificate"])
        expected = literal_sum(record["raw_matrix"], record["local_terms"], b)
        assert expected == record["exact_sum"]
        count_checks += 1

    return dict(status="all focused exact assertions passed",
                source=str(SOURCE.relative_to(ROOT)),
                source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                full_rank_boundary_fixtures=7,
                replayed_boundary_punctures=puncture_rounds,
                rejection_assertions=rejects,
                independent_exact_phase_sums=count_checks,
                records=records,
                limitation="Finite exhaustive phase sums, not the asymptotic counter.")


if __name__ == "__main__":
    result = run()
    destination = Path(__file__).with_name("root_mixed_focus_results.json")
    destination.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k: v for k, v in result.items() if k != "records"}))
