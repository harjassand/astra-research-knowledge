#!/usr/bin/env python3
"""Replay ONLY owned sampler copies on independently accepted saved models.

Force each positive outer branch once, instrument all getrandbits calls, and
check exact physical local outputs. Never invokes LP, compilation, or a peer
test; fixed sampler inputs are taken from our pinned owned snapshots.
"""
from datetime import datetime, timezone
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import json
import sys
import time

OWN = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(OWN / "replay/c03_s01/implementation"))
sys.path.insert(0, str(OWN.parent / "algorithm_review"))
import independent_posterior_verifier as independent
import filtered_sector_compiler as small_sampler
import filtered_sector_scaling as large_sampler


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


class CountedForcedBranch:
    def __init__(self, outer_bits, outer_draw):
        self.outer_bits, self.outer_draw = outer_bits, outer_draw
        self.calls = []

    def getrandbits(self, bits):
        need(type(bits) is int and bits >= 0, "illegal getrandbits width")
        self.calls.append(bits)
        if len(self.calls) == 1:
            need(bits == self.outer_bits and 0 <= self.outer_draw < 2 ** bits,
                 "outer distribution requested unexpected bits")
            return self.outer_draw
        # Deterministic control input, not a random-distribution experiment.
        # Exercise both boundary ranks/nodes and nonzero phase labels.
        return (2 ** bits - 1) if len(self.calls) % 2 == 0 else 0


def run_case(name, sampler):
    raw = (OWN / "source_snapshots" / name).read_bytes()
    model = json.loads(raw)["model"]
    N, ob = model["N"], model["outer_sampling_bits"]
    expected = model["predetermined_random_bits_per_sample"]
    start = time.perf_counter()
    cumulative = 0
    distinct_width_patterns = set()
    local_checks = 0
    for index, branch in enumerate(model["branches"]):
        probability = independent.rational(branch["probability"])
        width = probability * 2 ** ob
        need(width.denominator == 1 and width > 0, "nonpositive outer branch interval")
        rng = CountedForcedBranch(ob, cumulative)
        output = sampler.sample_filtered(model, rng)
        need(output["branch_index"] == index, "actual sampler selected wrong forced branch")
        need(sum(rng.calls) == expected == output["random_bits_consumed"],
             "measured finite-bit consumption disagrees with guarantee")
        block = branch["Dicke_model"]
        base = [ob, 128, 128, block["node_weight_bits"], block["phase_sampling_bits"]]
        padding = model["max_inner_sampling_bits"] - sum(base[-2:])
        expected_calls = base + ([padding] if padding else [])
        need(rng.calls == expected_calls, "measured getrandbits schedule inconsistent")
        distinct_width_patterns.add(tuple(rng.calls))
        k, u = branch["k"], branch["u"]
        subset, ones = output["subset"], output["complement_ones"]
        need(output["k"] == k and output["u"] == u
             and len(subset) == len(set(subset)) == k and subset == sorted(subset)
             and all(0 <= i < N for i in subset), "invalid actual subset output")
        need(len(ones) == len(set(ones)) == u and ones == sorted(ones)
             and all(0 <= i < N and i not in subset for i in ones),
             "invalid actual complement string output")
        local = output["local_density_matrices"]
        need(len(local) == N, "wrong number of physical local factors")
        same_block = None
        for i, density in enumerate(local):
            independent.verify_local_density(density)
            local_checks += 1
            if i in subset:
                if same_block is None:
                    same_block = density
                else:
                    need(density == same_block, "Dicke block factors not identical")
            else:
                need([independent.rational(x) for x in density["diagonal"]]
                     == [Q(int(i not in ones)), Q(int(i in ones))]
                     and independent.rational(density["upper_right_real"]) == 0
                     and independent.rational(density["upper_right_imag"]) == 0,
                     "complement local factor does not encode sampled string")
        need(output["ensemble_target_trace_distance_upper"]
             == model["total_target_trace_distance_upper"], "sample wrong target budget")
        cumulative += int(width)
        need(time.perf_counter() - start < 55, "owned sampler replay reached bounded case cap")
    need(cumulative == 2 ** ob, "outer integer intervals do not cover all fair-bit inputs")
    return {"N": N, "model_sha256": sha256(raw).hexdigest(),
            "forced_positive_branches": len(model["branches"]),
            "exact_local_PSD_trace_one_checks": local_checks,
            "measured_bits_for_every_branch": expected,
            "observed_getrandbits_width_patterns": [list(x) for x in sorted(distinct_width_patterns)],
            "wall_seconds": time.perf_counter() - start}


def main():
    began = time.perf_counter()
    cases = [run_case("filtered_N" + str(n) + ".json", small_sampler) for n in (8, 16)]
    cases += [run_case("scaling_N" + str(n) + ".json", large_sampler) for n in (32, 64)]
    result = {"utc": datetime.now(timezone.utc).isoformat(),
              "status": "PASS actual owned sampler on every delivered positive branch",
              "cases": cases, "code_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
              "scope": "Fixed inputs force branches for path/bit/physical-output checking; posterior probability guarantees are independent analytic checks, not inferred from these control inputs. Only owned snapshots imported; no optimizer/acquisition calls.",
              "wall_seconds": time.perf_counter() - began}
    (OWN / "OWNED_FILTERED_SAMPLER_REPLAY.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"],
                      "branches": sum(x["forced_positive_branches"] for x in cases),
                      "local_PSD_checks": sum(x["exact_local_PSD_trace_one_checks"] for x in cases),
                      "wall_seconds": result["wall_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
