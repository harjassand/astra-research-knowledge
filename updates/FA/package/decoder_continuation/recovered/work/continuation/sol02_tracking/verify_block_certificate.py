#!/usr/bin/env python3
"""Independent exact replay; imports no synthesis code."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
path = HERE / "block_controller_certificate.npz"
data = np.load(path, allow_pickle=False)
directions = data["directions"]
denominator = int(data["denominator"])
kden = int(data["kden"])
cap = int(data["cap"])
rn, rd = int(data["radius_numerator"]), int(data["radius_denominator"])
extent, lattice = int(data["extent"]), int(data["lattice"])
winning, policy = data["winning"], data["policy"]
assert lattice == denominator * kden
assert len(winning) == len(directions) + 1 == len(policy) + 1
assert winning[0, extent, extent]
coordinates = np.arange(-extent, extent + 1, dtype=np.int64)
xx, yy = np.meshgrid(coordinates, coordinates)
ball = (xx * xx + yy * yy) * rd * rd <= (rn * lattice)**2
assert all(not np.any(layer & ~ball) for layer in winning)
assert np.all(np.sum(directions * directions, axis=1) <= denominator**2)
transitions = 0
for step, (vx, vy) in enumerate(directions):
    rows, cols = np.where(winning[step])
    actions = policy[step, rows, cols].astype(np.int64)
    assert np.all((actions == 1) | (actions == -1))
    for noise in range(-cap, cap + 1):
        coefficients = actions * kden + noise
        nr, nc = rows + vy * coefficients, cols + vx * coefficients
        assert np.all((nr >= 0) & (nr < len(coordinates)))
        assert np.all((nc >= 0) & (nc < len(coordinates)))
        assert np.all(winning[step + 1, nr, nc])
        transitions += len(rows)
receipt = {
    "status": "PASS",
    "evidence_status": "exact finite certificate replay with integer shifts and integer ball tests",
    "certificate_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    "chosen_action_universal_noise_transitions_checked": transitions,
    "winning_counts": [int(layer.sum()) for layer in winning],
    "origin_winning": True,
    "safe_virtual_radius": f"{rn}/{rd}",
    "continuous_claim_requires": "the scalar quantization/feedback transfer and supplied exact rational directions in RESULT.txt",
    "hardware_or_acquired_actuator_validation": False,
}
(HERE / "block_certificate_replay.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
