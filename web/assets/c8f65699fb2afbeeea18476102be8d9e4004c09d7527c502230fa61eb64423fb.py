#!/usr/bin/env python3
"""Finite enumeration check for the unknown-temperature EB bin decoder.

This checks the likelihood-ratio bin bound and weighted subset DP on a small
abstract fermion mode list. It is a numerical diagnostic, not a proof.
"""
from __future__ import annotations
import itertools
import json
import math
from pathlib import Path

energies = [0.113, 0.247, 0.516, 0.837, 1.074, 1.386, 1.719, 2.043]
zeta = 0.01
h = 0.70
width_grid = round(h / zeta)
tau_lo, tau_hi, tau_ref = 0.35, 0.95, 0.60
lam = 0.2
Q = len(energies)
tmax = 4

# Quantized energy defines the public bin label. The exact free-state weights
# retain the unrounded energies.
g = [math.floor(e / zeta) for e in energies]
subsets = []
for bits in itertools.product((0, 1), repeat=Q):
    t = sum(bits)
    if t > tmax:
        continue
    E = sum(x * e for x, e in zip(bits, energies))
    G = sum(x * gi for x, gi in zip(bits, g))
    label = (t, G // width_grid)
    subsets.append((bits, t, E, G, label))


def conditional(law_tau: float, label):
    rows = [row for row in subsets if row[4] == label]
    if not rows:
        return rows, []
    weights = [math.exp(-law_tau * E + law_tau * lam * t)
               for _, t, E, _, _ in rows]
    z = sum(weights)
    return rows, [w / z for w in weights]

# DP suffix recurrence over particle count and quantized energy.
# The dictionaries hold the exact mathematical weights on the quantized grid.
weights = [math.exp(-tau_ref * gi * zeta) for gi in g]
D = [[{} for _ in range(tmax + 1)] for _ in range(Q + 1)]
D[Q][0][0] = 1.0
for q in range(Q - 1, -1, -1):
    for j in range(tmax + 1):
        curr = dict(D[q + 1][j])
        if j:
            for energy_grid, value in D[q + 1][j - 1].items():
                target = energy_grid + g[q]
                curr[target] = curr.get(target, 0.0) + weights[q] * value
        D[q][j] = curr

max_shape_l1 = 0.0
max_quant_l1 = 0.0
max_dp_l1 = 0.0
checked_labels = 0
for label in sorted({row[4] for row in subsets}):
    rows_lo, p_lo = conditional(tau_lo, label)
    rows_hi, p_hi = conditional(tau_hi, label)
    rows_ref, p_ref = conditional(tau_ref, label)
    if not rows_ref:
        continue
    assert [r[0] for r in rows_lo] == [r[0] for r in rows_ref]
    shape = max(sum(abs(x - y) for x, y in zip(p_lo, p_ref)),
                sum(abs(x - y) for x, y in zip(p_hi, p_ref)))
    max_shape_l1 = max(max_shape_l1, shape)
    # The true-energy diameter in a quantized bin is at most h+2*t*zeta.
    shape_bound = math.exp((tau_hi - tau_lo) * (h + 2 * tmax * zeta)) - 1
    assert shape <= shape_bound + 1e-12

    approx = [math.exp(-tau_ref * row[3] * zeta) for row in rows_ref]
    za = sum(approx)
    p_approx = [x / za for x in approx]
    quant_err = sum(abs(x - y) for x, y in zip(p_ref, p_approx))
    max_quant_l1 = max(max_quant_l1, quant_err)
    quant_bound = math.exp(2 * tau_ref * tmax * zeta) - 1
    assert quant_err <= quant_bound + 1e-12

    t, b = label
    target_g = [row[3] for row in rows_ref]
    # Reconcile the DP bin mass with explicit subset enumeration.
    dpmass = sum(v for energy_grid, v in D[0][t].items()
                 if energy_grid // width_grid == b)
    exmass = sum(approx)
    max_dp_l1 = max(max_dp_l1, abs(dpmass - exmass))
    assert abs(dpmass - exmass) <= 1e-11 * max(1.0, exmass)
    # Every selected subset's approximate weight equals the DP product.
    for row, w in zip(rows_ref, approx):
        expected = math.prod(weights[q] for q, bit in enumerate(row[0]) if bit)
        assert abs(expected - w) <= 1e-12 * max(1.0, w)
    checked_labels += 1

result = {
    "status": "PASS",
    "scope": "8-mode exhaustive numerical enumeration; unknown-tau bin and DP convention check only",
    "subsets_checked": len(subsets),
    "labels_checked": checked_labels,
    "max_endpoint_conditional_l1": max_shape_l1,
    "max_shape_bound": math.exp((tau_hi - tau_lo) * (h + 2 * tmax * zeta)) - 1,
    "max_quantization_conditional_l1": max_quant_l1,
    "max_quantization_bound": math.exp(2 * tau_ref * tmax * zeta) - 1,
    "max_dp_mass_abs_error": max_dp_l1,
    "finite_diagnostic_only": True,
}
out = Path("outputs/research/spin_statistical/cycle2/d_dimensional_fermion/evidence/binned_archive_checks.json")
out.write_text(json.dumps(result, indent=2) + "\n")
print(out)
print(json.dumps(result, indent=2))
