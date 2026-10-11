#!/usr/bin/env python3
"""Focused exact checks of the population operation and succinct coupling."""
from fractions import Fraction
import json
from pathlib import Path
import random
from dfa_solver import Model, solve, verify, round_layered_flow

HERE = Path(__file__).resolve().parent
spec = json.loads((HERE / "dfa_noncommutative.json").read_text())
model = Model(spec)
assert model.delta[model.delta[0][0]][1] != model.delta[model.delta[0][1]][0]
receipts = {"noncommutativity": {"a_then_b_from_s0": "s2", "b_then_a_from_s0": "s1"}, "cases": []}

cases = [("noncommutative_unbounded", spec, None),
         ("noncommutative_binary_trillion", spec, 10**12),
         ("positive_return_unbounded", json.loads((HERE / "dfa_positive_return.json").read_text()), None),
         ("positive_gap_binary_trillion", json.loads((HERE / "dfa_positive_gap.json").read_text()), 10**12)]
for name, data, horizon in cases:
    cert, witness = solve(data, horizon)
    path = HERE / (name + ".certificate.json")
    path.write_text(json.dumps(cert, indent=2) + "\n")
    checked = verify(data, json.loads(path.read_text()))
    if name == "positive_return_unbounded":
        assert cert["witness_horizon"] == 2
        assert cert["actual_repaired_terminal"] == ["1", "0"]
    if name == "positive_gap_binary_trillion":
        assert Fraction(cert["true_optimum_interval"][0]) > 0
        assert cert["actual_repaired_tv"] == "2/3"
    if horizon:
        assert cert["witness_horizon"] == horizon
        assert cert["witness_node_count"] < 10_000
        assert max(q["depth"] for r in cert["seed_receipts"] for q in r["queries"]) < 100
    rng = random.Random(20261011)
    sample = witness.sample(rng.getrandbits)
    t = cert["witness_horizon"]//2
    assert witness.query(t, sample["branch"], sample["seed"]) == witness.query(t, sample["branch"], sample["seed"])
    # Force one rejected integer draw to check the public cost receipt. This
    # deterministic source is a contract test, not a purported fair source.
    calls = [0]
    def forced_rejection(width):
        calls[0] += 1
        return (1 << width)-1 if calls[0] == 1 else 0
    rejected = witness.sample(forced_rejection)
    assert rejected["integer_rejections"] >= 1
    receipts["cases"].append({"name": name, "verification": checked,
        **{k: cert[k] for k in ["graph", "witness_horizon", "witness_node_count", "distinct_leaf_count",
              "filler_quantile_denominator", "quantile_support_bound", "coupling_word_support_upper_bound",
              "empirical_optimum_tv", "true_optimum_interval", "actual_repaired_terminal", "actual_repaired_tv"]},
        "certificate_bytes": path.stat().st_size,
        "public_sampler_demo_prng_receipt": sample,
        "public_sampler_rejection_contract_test": rejected})

rounding = round_layered_flow(spec, [(list("aaab"), "1/2"), (list("bbba"), "1/2")], 3)
assert rounding["cycle_adjustments"] > 0
(HERE / "layered_flow_rounding.certificate.json").write_text(json.dumps(rounding, indent=2)+"\n")
receipts["layered_flow_rounding"] = rounding
receipts["scope"] = "Exact finite certificates and internal implementation checks; no historical novelty or external certification claim."
(HERE / "dfa_checks.json").write_text(json.dumps(receipts, indent=2)+"\n")
print(json.dumps(receipts, indent=2))
