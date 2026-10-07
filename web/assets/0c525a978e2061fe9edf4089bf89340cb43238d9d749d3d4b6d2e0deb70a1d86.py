#!/usr/bin/env python3
"""Targeted repaired-code replay, using only owned source copies."""
from copy import deepcopy
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import importlib.util
import json
import random
import subprocess
import sys
import time

OWN = Path(__file__).resolve().parent
ROOT = OWN.parents[4]
REPLAY = OWN / "replay/c03_s01/implementation"
sys.path.insert(0, str(REPLAY))
import dicke_compiler as dicke
import whole_gibbs_compiler as whole


class CountingBits(random.Random):
    def __init__(self, seed):
        super().__init__(seed)
        self.bits_used = 0

    def getrandbits(self, k):
        self.bits_used += k
        return super().getrandbits(k)


def main():
    start = time.perf_counter()
    code = REPLAY / "dicke_compiler.py"
    assert sha256(code.read_bytes()).hexdigest() == "18978186d75d38d93f454e574bc4baffa79e07481df97f6903b13342450e4aa5"
    assert sha256((REPLAY / "whole_gibbs_compiler.py").read_bytes()).hexdigest() == "1a1466354cffe3999f7bb15ff2ffe7cd4c91c5b7c8f95e3c73aa1f5c83827612"
    source = ROOT / "work/cycle6/c03_s01/implementation"
    data = json.loads((source / "delta1_checks.json").read_text())
    model = next(m for m in data["models"] if m["n"] == 8 and dicke.from_record(m["h"]) == Q(1, 3))
    assert dicke.verify_model(model)
    bad = deepcopy(model)
    bad["phase_modulus"] = 1
    rejected = []
    for name, operation in [("posterior verifier", lambda: dicke.verify_model(bad)),
                            ("sampler guard", lambda: dicke.sample_product(bad, random.Random(0)))]:
        try:
            operation()
        except (AssertionError, ValueError):
            rejected.append(name)
        else:
            raise AssertionError("repaired code accepted phase modulus corruption")
    optimized = subprocess.run([sys.executable, "-O", str(code)], capture_output=True, text=True, timeout=10)
    assert optimized.returncode != 0 and "without -O/-OO" in optimized.stderr
    api = json.loads((source / "whole_api_checks.json").read_text())
    draws = []
    for index, example in enumerate(api["examples"]):
        outer = example["model"]
        assert whole.verify_whole_model(outer)
        rng = CountingBits(12345 + index)
        for repetition in range(8):
            before = rng.bits_used
            sample = whole.sample_whole_gibbs(outer, rng)
            used = rng.bits_used - before
            assert used == outer["predetermined_random_bits_per_sample"] == sample["random_bits_consumed"]
            assert len(sample["subset"]) == sample["k"] and len(sample["complement_ones"]) == sample["u"]
            assert set(sample["subset"]).isdisjoint(sample["complement_ones"])
            for local in sample["local_density_matrices"]:
                a, b = map(dicke.from_record, local["diagonal"])
                re, im = map(dicke.from_record, (local["upper_right_real"], local["upper_right_imag"]))
                assert min(a, b) >= 0 and a + b == 1 and re * re + im * im <= a * b
            draws.append({"N": outer["N"], "repetition": repetition, "actual_bits": used,
                          "all_local_states_exact_PSD_trace_one": True})
    # Domain obstruction is independently exact, separate from the guard.
    import independent_posterior_verifier as independent
    a, b = independent.independent_exp_minus(Q(1))
    u2lo, u2hi = a / (1 + 2 * b), b / (1 + 2 * a)
    assert u2hi - Q(1, 4) < 0
    try:
        dicke.numeric_quadrature(2, Q(2), Q(0), 100)
    except (ArithmeticError, ValueError):
        outside_rejected = True
    else:
        raise AssertionError("outside-domain negative Gram passed Cholesky")
    result = {"status": "PASS repaired frozen code, owned-copy replay only",
              "dicke_sha256": sha256(code.read_bytes()).hexdigest(),
              "whole_sha256": sha256((REPLAY / "whole_gibbs_compiler.py").read_bytes()).hexdigest(),
              "phase_counterexample_rejected_by": rejected,
              "optimized_python_fail_closed": True,
              "whole_models_replayed": len(api["examples"]), "actual_counted_finite_bit_draws": len(draws),
              "draws": draws, "outside_delta2_negative_Gram_upper": str(u2hi - Q(1, 4)),
              "outside_delta2_bypass_Cholesky_rejected": outside_rejected,
              "randomness_scope": "seeded pseudorandom draws exercise exact bit counts and PSD output; fair-bit distribution theorem is separately audited",
              "wall_seconds": time.perf_counter() - start}
    (OWN / "REPAIRED_OWNED_REPLAY.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("status", "whole_models_replayed", "actual_counted_finite_bit_draws", "wall_seconds")}, indent=2))


if __name__ == "__main__":
    main()
