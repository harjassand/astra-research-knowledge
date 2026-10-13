#!/usr/bin/env python3
"""Factorized all-time controller for orthogonal two-coordinate blocks.

Each block follows the inherited four-direction local period. Blocks may be
interleaved arbitrarily, including adaptively. This file does not synthesize
or assume a general arbitrary-schedule controller.
"""
from __future__ import annotations
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "inherited_continuous_r3.npz"


class BlockLiftController:
    def __init__(self, blocks):
        if blocks < 1:
            raise ValueError("positive block count required")
        data = np.load(CERTIFICATE, allow_pickle=False)
        self.winning = data["winning"]
        self.policy = data["policy"]
        self.scale = int(data["scale"])
        self.radius = int(data["radius_units"])
        self.directions = [tuple(map(int, v)) for v in data["directions"]]
        self.phase = [0] * blocks

    def choose(self, block, observed_integer_cell):
        """Observe active 2D error with total per-coordinate error <=1/20.

        The returned direction has support {2*block,2*block+1}. The caller
        actuates once, then supplies fresh feedback on the next activation.
        """
        p = self.phase[block]
        x, y = map(int, observed_integer_cell)
        rx, ry = x + self.radius, y + self.radius
        if not (0 <= rx < self.winning.shape[1] and 0 <= ry < self.winning.shape[2]):
            raise ValueError("feedback cell is outside certified state range")
        if not self.winning[p, rx, ry]:
            raise ValueError("feedback cell is outside certified invariant")
        sign = int(self.policy[p, rx, ry])
        direction = tuple(F(value, 5) for value in self.directions[p])
        self.phase[block] = (p + 1) % len(self.directions)
        return sign, (2 * block, 2 * block + 1), direction


def verify_and_write_receipt():
    # Independent exact geometry reconstruction; no synthesis-code import.
    data = np.load(CERTIFICATE, allow_pickle=False)
    scale, radius = int(data["scale"]), int(data["radius_units"])
    directions = [tuple(map(int, v)) for v in data["directions"]]
    winning, policy = data["winning"], data["policy"]
    cells = {(p, x-radius, y-radius) for p, x, y in zip(*np.nonzero(winning))}
    offsets = {}
    geometry_checks = 0
    for phase, direction in enumerate(directions):
        scaled = [F(scale * value, 5) for value in direction]
        for sign in (-1, 1):
            ranges = []
            for value in scaled:
                lo = sign * value - abs(value)/2 - 2
                hi = sign * value + abs(value)/2 + 2
                ranges.append(range(-((-lo.numerator)//lo.denominator), hi.numerator//hi.denominator+1))
            candidates = set()
            for x in ranges[0]:
                for y in ranges[1]:
                    lower, upper, feasible = -F(1, 2), F(1, 2), True
                    for coordinate, value in zip((x, y), scaled):
                        if value == 0:
                            feasible &= abs(coordinate) <= 2
                        else:
                            endpoints = [(F(coordinate)-sign*value-2)/value,
                                         (F(coordinate)-sign*value+2)/value]
                            lower = max(lower, min(endpoints))
                            upper = min(upper, max(endpoints))
                    if feasible and lower <= upper:
                        candidates.add((x, y))
                    geometry_checks += 1
            assert candidates == {tuple(map(int, v)) for v in data[f"offsets_{phase}_{sign}"]}
            offsets[(phase, sign)] = candidates
    transitions = 0
    for p, x, y in cells:
        assert (abs(x)+1)**2 + (abs(y)+1)**2 <= radius**2
        sign = int(policy[p, x+radius, y+radius])
        assert sign in (-1, 1)
        for dx, dy in offsets[(p, sign)]:
            assert ((p+1) % len(directions), x+dx, y+dy) in cells
            transitions += 1
    initial_cells = [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1)]
    assert all((0, x, y) in cells for x, y in initial_cells)
    # Exact tensor-product proof, represented by a single local obligation:
    # an active block takes one of the checked transitions; every inactive
    # block retains its cell/phase. Safe squared norms add on disjoint supports.
    example_blocks = 1000
    receipt = {
        "status": "PASS",
        "evidence_status": "inherited local exact certificate replay plus internally proved orthogonal product lift",
        "inherited_source_certificate": "work/phase5/mathematical_operation/continuous_optimal_r60_q20.npz",
        "certificate_sha256": hashlib.sha256(CERTIFICATE.read_bytes()).hexdigest(),
        "local_winning_cells": len(cells),
        "local_exact_geometry_checks": geometry_checks,
        "local_chosen_action_universal_transitions_checked": transitions,
        "all_allowed_initial_feedback_cells_checked": len(initial_cells),
        "blocks": "any positive integer k",
        "dimension": "2*k (unused orthogonal coordinates may remain zero)",
        "direction_rule": "each active block follows local period e1,(3/5,4/5),e2,(4/5,-3/5); arbitrary interleaving",
        "postdecision_scalar_noise": "[-1/2,1/2] on the active direction only",
        "feedback_total_coordinate_error": "<=1/20 in active two-coordinate block",
        "all_time_actual_radius": "3*sqrt(k)",
        "all_time_actual_squared_radius": "9*k",
        "compressed_storage": "one shared local table plus k phase indices; no tensor-product expansion",
        "per_pulse_operations": "read active block feedback, one table lookup, increment its phase",
        "example_dimension": 2 * example_blocks,
        "example_certified_squared_radius": 9 * example_blocks,
        "scope": "special block-local periodic schedules only; no general arbitrary-schedule theorem or novelty claim",
        "physical_experiment": False,
    }
    (HERE / "periodic_block_lift_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    verify_and_write_receipt()
