"""Tiny independent smoke check of the copied c01_s03 low-sector sampler."""
import importlib.util
import json
from fractions import Fraction
from pathlib import Path
from random import Random

ROOT = Path(__file__).resolve().parent
source = ROOT / "low_sector_sampler_peer_copy.py"
spec = importlib.util.spec_from_file_location("low_sector_sampler_peer_copy", source)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# F is the two-site swap. Its only legal k=1 configurations have amplitudes 1,
# so the exact norm is 2 and the Born law is uniform on the two orientations.
sector = module.LowSector([[0, 1], [1, 0]])
count = sector.estimate(1, Fraction(1, 4), Fraction(1, 4), rng=Random(7))
sample = sector.born_sample(1, Fraction(1, 4), rng=Random(7))
assert count == 2
assert sample["status"] == "OK"
assert len(sample["I"]) == len(sample["J"]) == 1
assert set(sample["I"]).isdisjoint(sample["J"])
print(json.dumps({
    "status": "PASS_TINY_COPIED_PROGRAM_SMOKE",
    "fixture": "n=2 swap matrix, k=1",
    "exact_norm": str(count),
    "sample": sample,
    "estimator_stats": sector.stats,
    "scope": "single deterministic small fixture; not a confidence or scaling test"
}, indent=2))
