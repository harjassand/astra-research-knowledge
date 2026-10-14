#!/usr/bin/env python3
"""Exact reversibility and alpha-order checks for the append-only correction."""
from __future__ import annotations

from fractions import Fraction as F
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPLICA = ROOT / "replica"
sys.path.insert(0, str(REPLICA))

from model import Compiler, discover_partition, from_transcript


def main() -> None:
    replay = json.loads((HERE / "fresh_replay_results.json").read_text())
    fresh = {item["name"]: item["exact_high_precision_alpha_recertification"]
             for item in replay["tensor_replays"]}
    records = []
    for name in ("reverse_A", "reverse_B", "reverse_matched_tensor"):
        transcript = json.loads((REPLICA / f"{name}_transcript.json").read_text())
        model = from_transcript(18, transcript)
        groups, _ = discover_partition(model)
        compiler = Compiler(model, groups)
        block = next(b for b, group in enumerate(groups) if model["target"] in group)
        K = compiler.refraw[block]
        p = compiler.prob[block]
        q = len(K)

        balance_checks = 0
        for i in range(q):
            for j in range(q):
                assert p[i] * F(K[i, j]) == p[j] * F(K[j, i]), (name, i, j)
                balance_checks += 1

        asym_pairs = [(i, j) for i in range(q) for j in range(i + 1, q)
                      if F(K[i, j]) != F(K[j, i])]
        assert asym_pairs, f"{name}: raw K unexpectedly Euclidean symmetric"
        sample_i, sample_j = asym_pairs[0]
        assert all(F(K[i, j]) <= 0 for i in range(q) for j in range(q) if i != j)
        flip_edges = 0
        for i in range(q):
            for bit in range(len(groups[block])):
                j = i ^ (1 << bit)
                assert F(K[i, j]) < 0, (name, i, j)
                flip_edges += 1

        target_local = groups[block].index(model["target"])
        target_rows = 0
        row_sums = []
        for i in range(q):
            row_sum = sum(F(K[i, j]) for j in range(q))
            expected = model["kappa"] * int(compiler.bits[block][i, target_local])
            assert row_sum == expected, (name, i, row_sum, expected)
            if expected > 0:
                target_rows += 1
        assert target_rows > 0

        old = json.loads((REPLICA / f"{name}.json").read_text())
        old_alpha = F(old["alpha_lower"])
        new_alpha = F(fresh[name]["alpha_lower"])
        assert old_alpha <= new_alpha, name
        records.append({
            "name": name,
            "target_block": block,
            "local_states": q,
            "probability_sum_exactly_one": sum(p, F(0)) == 1,
            "exact_detailed_balance_pair_checks": balance_checks,
            "all_detailed_balance_equalities_hold": True,
            "raw_K_euclidean_symmetric": False,
            "raw_K_unequal_unordered_pairs": len(asym_pairs),
            "raw_K_asymmetry_witness": {
                "i": sample_i,
                "j": sample_j,
                "K_ij": str(F(K[sample_i, sample_j])),
                "K_ji": str(F(K[sample_j, sample_i])),
                "p_i_K_ij": str(p[sample_i] * F(K[sample_i, sample_j])),
                "p_j_K_ji": str(p[sample_j] * F(K[sample_j, sample_i])),
            },
            "all_offdiagonals_nonpositive": True,
            "exact_nonzero_flip_edges_checked": flip_edges,
            "target_killing_rows": target_rows,
            "all_row_sums_equal_target_killing": True,
            "retained_old_alpha": str(old_alpha),
            "fresh_exact_replay_alpha": str(new_alpha),
            "old_alpha_le_fresh_alpha_exactly": True,
        })

    output = {
        "scope": "exact rational checks on three retained synthetic canonical local killed generators",
        "no_source_or_frozen_artifact_modified": True,
        "records": records,
        "interpretation": (
            "The raw local K matrices are reversible but generally nonsymmetric in Euclidean coordinates. "
            "Their exact detailed balance makes them self-adjoint under the local equilibrium weights; "
            "the fresh exact alpha bounds therefore remain valid through the inverse infinity-norm and "
            "spectral-radius argument stated in WEIGHTED_ALPHA_CORRECTION.md."
        ),
    }
    out = HERE / "weighted_alpha_exact_checks.json"
    out.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"cases": len(records), "all_exact_checks_passed": True,
                      "result_file": out.name}, indent=2))


if __name__ == "__main__":
    main()
