"""Small exact audit checks; does not run the acquisition benchmark."""
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib
import json
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from discover_chain import (discover_triangle_path, RetainedFeatureTrellis,
                            BitSource, parity, lincomb)


def sampler_law(answer):
    if answer.code_partition == 0:
        return {}
    compiler = answer.compiler
    paths = [(0, 0, Fraction(1))]
    for j in range(len(compiler.order) - 1, -1, -1):
        nxt = []
        original = compiler.order[j]
        for state, y, probability in paths:
            branches = []
            for source, target, bit in compiler.trellis.transitions[j]:
                if target != state or (original in answer.evidence and answer.evidence[original] != bit):
                    continue
                mass = answer.tables[j][source] * answer.weights[original][bit]
                if mass:
                    branches.append((source, bit, mass))
            normalizer = sum(mass for _, _, mass in branches)
            for source, bit, mass in branches:
                nxt.append((source, y | (bit << j), probability * Fraction(mass, normalizer)))
        paths = nxt
    kernel = compiler.lift_system.kernel
    law = {}
    for state, y, probability in paths:
        assert state == 0
        base = compiler.lift_system.particular(y)
        for choice in range(1 << len(kernel)):
            x = base ^ lincomb(kernel, choice)
            law[x] = law.get(x, Fraction(0)) + probability / (1 << len(kernel))
    return law


def main():
    rng = random.Random(20261102)
    support = [1, 2, 4, 3, 6, 8, 16]
    for _ in range(12):
        rng.shuffle(support)
        certificate = discover_triangle_path(support)
        assert certificate["status"] == "CERTIFIED" and certificate["width"] == 1
        assert certificate["relation_rank"] == 2

    support = [1, 2, 3, 4]  # One triangle, one independent feature, one free x bit.
    certificate = discover_triangle_path(support)
    compiler = RetainedFeatureTrellis(4, support, certificate["order"])
    weights = [(2, 3), (5, 7), (11, 13), (17, 19)]
    feasible, impossible = 0, 0
    for values in product((None, 0, 1), repeat=4):
        evidence = {j: value for j, value in enumerate(values) if value is not None}
        answer = compiler.evaluate(weights, evidence)
        direct = {}
        for x in range(16):
            if any(parity(support[j] & x) != value for j, value in evidence.items()):
                continue
            weight = 1
            for a, pair in zip(support, weights):
                weight *= pair[parity(a & x)]
            direct[x] = weight
        z = sum(direct.values())
        assert answer.partition == z
        if not z:
            impossible += 1
            for operation in (answer.map_input, lambda: answer.sample(BitSource(1))):
                try:
                    operation()
                except ValueError:
                    pass
                else:
                    raise AssertionError("Inconsistent evidence was not rejected")
        else:
            feasible += 1
            assert answer.map_mass == max(direct.values())
            assert direct[answer.map_input()] == answer.map_mass
            assert sampler_law(answer) == {x: Fraction(w, z) for x, w in direct.items()}

    independent = RetainedFeatureTrellis(2, [1], [0])
    mutable = [(1, 2)]
    saved = independent.evaluate(mutable)
    mutable[0] = (7, 1)
    expected = {0: Fraction(1, 6), 2: Fraction(1, 6),
                1: Fraction(1, 3), 3: Fraction(1, 3)}
    assert sampler_law(saved) == expected
    forced = independent.evaluate([(7, 11)], {0: 0})
    source = BitSource(0)
    forced.sample(source)
    assert source.bits_used == 1

    target = HERE / "discover_chain.py"
    report = {
        "root_file_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        "permuted_path_plus_independent_feature_checks": 12,
        "all_feature_clamp_patterns": 81,
        "feasible_exact_partition_MAP_sampler_laws": feasible,
        "inconsistent_patterns_rejected": impossible,
        "caller_weight_mutation_does_not_change_saved_law": True,
        "one_forced_feature_sample_random_bits_equals_free_fiber_bits": source.bits_used,
        "scope": "Targeted exact finite audit; no acquisition benchmark rerun."
    }
    (ROOT / "results" / "chain_audit.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
