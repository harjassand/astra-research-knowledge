"""Exact scalar admission for the stronger clean-copy lemma; no trajectories."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import time

t0 = time.perf_counter()
F0 = 3 * (Q(1, 256) + Q(25, 32) ** 32) / 256
margin = Q(15, 32 * 8192) - Q(17, 16) * F0 - Q(1, 2**20)
assert margin > 0
assert 3 * (Q(1, 64) + Q(25, 32) ** 32) < Q(1, 8)
assert Q(1, 4096) - Q(2, 16384) == Q(1, 8192)
out = {
    "status": "EXACT_RATIONAL_CONSTANTS_PASS",
    "F0": str(F0),
    "copy_drift_margin_per_bit": str(margin),
    "initial_density": "1/4096",
    "source_exit_density": "1/256",
    "copy_excursion_density": "1/8192",
    "walk_length": 32,
    "update_fair_bits": 288,
    "random_draws": 0,
    "physical_trajectories": 0,
    "elapsed_seconds": time.perf_counter() - t0,
    "scope": "Scalar constants only; does not prove the analytic restart/Palm lemmas or build a handshake",
    "consumer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
Path(__file__).with_name("CONSTANTS.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
