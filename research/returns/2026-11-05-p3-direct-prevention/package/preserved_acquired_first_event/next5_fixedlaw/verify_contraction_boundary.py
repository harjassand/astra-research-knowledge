"""Reproducible exact diagnostics for contracting_machine.py.

Run: python next5_fixedlaw/verify_contraction_boundary.py
Writes execution_record.json beside this file.  No simulation establishes
undecidability; the mathematical reduction is in the companion proof.
"""

from __future__ import annotations

import hashlib
import json
import platform
import random
import time
from fractions import Fraction as F
from pathlib import Path

from contracting_machine import (
    ContractingCompiler,
    CounterMachine,
    Instruction,
    countdown_machine,
    dot,
    flag,
    nonhalting_machine,
    project_cone,
    projection_regions,
    scale,
    sqnorm,
    sub,
    vec,
)


def matrix_apply(matrix, vector):
    return tuple(dot(row, vector) for row in matrix)


def matrix_product(a, b):
    return tuple(
        tuple(sum((a[i][k] * b[k][j] for k in range(4)), F(0)) for j in range(4))
        for i in range(4)
    )


def compiler_certificate(compiler):
    regions = compiler.matrices()
    assert len(regions) == 54 * compiler.machine.m
    largest_sum = F(0)
    vertex_checks = 0
    for region in regions:
        M = region["matrix"]
        assert region["entry_absolute_sum"] <= compiler.C
        largest_sum = max(largest_sum, region["entry_absolute_sum"])
        for z, expected in zip(region["vertices"], region["outputs"]):
            x = (F(1), *z)
            assert matrix_apply(M, x) == expected
            assert compiler.cube_map(z) == expected
            assert all(dot(h, x) >= 0 for h in region["inequalities"])
            vertex_checks += 1
        for row in M:
            assert abs(row[1]) <= 2 * compiler.machine.m
            assert abs(row[2]) <= 4 and abs(row[3]) <= 4
    plane_checks = 0
    sample_grid = tuple(F(i, 16) for i in range(17))
    for label in range(1, compiler.machine.m + 1):
        for z0 in sample_grid:
            for z1 in sample_grid:
                actual = compiler.cube_map((compiler.label_value(label), z0, z1))
                assert actual == compiler.plane_map(label, z0, z1)
                plane_checks += 1
    return {
        "labels_including_halt": compiler.machine.m,
        "cube_tetrahedra": len(regions),
        "vertex_checks": vertex_checks,
        "control_plane_checks": plane_checks,
        "uniform_bound_C": compiler.C,
        "largest_actual_matrix_entry_sum": str(largest_sum),
        "scale_a": str(compiler.a),
        "certified_global_euclidean_lipschitz_upper_bound": "1/2",
        "explicit_global_region_upper_bound": 35 * len(regions),
    }


def check_projection(rng):
    regions = projection_regions()
    assert len(regions) == 35
    for region in regions:
        P = region["matrix"]
        assert P == tuple(tuple(P[j][i] for j in range(4)) for i in range(4))
        assert matrix_product(P, P) == P
    trials = 250
    for _ in range(trials):
        x = tuple(F(rng.randint(-40, 40), rng.randint(1, 11)) for _ in range(4))
        p = project_cone(x)
        assert p[0] >= 0 and all(0 <= coordinate <= p[0] for coordinate in p[1:])
        matching = [r for r in regions if all(dot(h, x) >= 0 for h in r["inequalities"])]
        assert matching
        assert all(matrix_apply(r["matrix"], x) == p for r in matching)
        # Projection on a closed convex cone: residual is orthogonal to p.
        assert dot(sub(x, p), p) == 0
        for _ in range(4):
            t = F(rng.randrange(16), 5)
            z = (t, *(t * F(rng.randrange(13), 12) for _ in range(3)))
            assert dot(sub(x, p), sub(z, p)) <= 0
    return {
        "explicit_projection_regions": len(regions),
        "symmetric_idempotent_matrices_checked_exactly": len(regions),
        "random_rational_input_checks": trials,
        "projection_variational_inequality_probes_per_input": 4,
    }


def check_valid_machine_steps(compiler):
    checks = 0
    for label in range(1, compiler.machine.m + 1):
        for counter0 in range(9):
            for counter1 in range(9):
                configuration = (label, counter0, counter1)
                successor = compiler.machine.step(configuration)
                expected = vec((0, 0, 0, 0)) if successor is None else scale(compiler.a, compiler.encode(successor))
                assert compiler(compiler.encode(configuration)) == expected
                checks += 1
    return checks


def trace_countdown(n):
    compiler = ContractingCompiler(countdown_machine())
    configuration = (1, n, 0)
    x = compiler.encode(configuration)
    expected_halt_time = 2 * n + 1
    expected_zero_time = 2 * n + 2
    max_denominator_bits = 0
    for k in range(expected_zero_time + 1):
        max_denominator_bits = max(max_denominator_bits, *(z.denominator.bit_length() for z in x))
        if k < expected_zero_time:
            assert configuration is not None
            assert x == scale(compiler.a**k, compiler.encode(configuration))
            assert x[0] > 0
            if k == expected_halt_time:
                assert configuration[0] == compiler.machine.m
                assert flag(x) == compiler.a**k / 4
            else:
                assert configuration[0] != compiler.machine.m
                assert flag(x) <= -(compiler.a**k) / 4
        else:
            assert not any(x) and configuration is None
        if k < expected_zero_time:
            x = compiler(x)
            configuration = compiler.machine.step(configuration)
    denominator = 4 * (2 * compiler.C) ** expected_halt_time
    return {
        "initial_counter0": n,
        "halt_label_arrival_step": expected_halt_time,
        "origin_arrival_step": expected_zero_time,
        "halt_flag_exact_expression": f"1/(4*{2 * compiler.C}^{expected_halt_time})",
        "minimum_b_with_2_to_minus_b_strictly_below_flag": denominator.bit_length(),
        "maximum_coordinate_denominator_bits": max_denominator_bits,
    }


def check_nonhalting_prefix(steps):
    compiler = ContractingCompiler(nonhalting_machine())
    x = compiler.encode((1, 0, 0))
    for n in range(steps + 1):
        expected = scale(compiler.a**n, (F(1), F(1, 4), F(1, 2**n), F(1)))
        assert x == expected and x[0] > 0 and flag(x) < 0
        x = compiler(x)
    return {
        "steps_checked": steps,
        "analytic_orbit": "(1/200)^n * (1,1/4,2^(-n),1)",
        "scope": "The formula proves nonhalting for this simple program; finite execution alone does not.",
    }


def check_global_composition(compiler, rng):
    digest = hashlib.sha256()
    probes = [tuple(F(rng.randint(-8, 8), 3) for _ in range(4)) for _ in range(8)]
    probes += [compiler.encode((1, 0, 0)), compiler.encode((3, 1, 2)), vec((0, 0, 0, 0))]
    covered = [0] * len(probes)
    expected = [compiler(x) for x in probes]
    count = 0
    for region in compiler.global_regions():
        count += 1
        digest.update(repr(region).encode("ascii"))
        for j, x in enumerate(probes):
            if all(dot(h, x) >= 0 for h in region["inequalities"]):
                assert matrix_apply(region["matrix"], x) == expected[j]
                covered[j] += 1
    assert count == 1890 * compiler.machine.m and min(covered) > 0
    pair_trials = 250
    for _ in range(pair_trials):
        x = tuple(F(rng.randint(-25, 25), 7) for _ in range(4))
        y = tuple(F(rng.randint(-25, 25), 11) for _ in range(4))
        gx, gy = compiler(x), compiler(y)
        assert 4 * sqnorm(sub(gx, gy)) <= sqnorm(sub(x, y))
        c = F(rng.randint(0, 31), 9)
        assert compiler(scale(c, x)) == scale(c, gx)
    return {
        "global_cells_emitted_including_redundant_cells": count,
        "compiled_description_sha256": digest.hexdigest(),
        "global_region_evaluation_probes": len(probes),
        "random_global_pair_contraction_checks": pair_trials,
        "random_positive_homogeneity_checks": pair_trials,
        "scope": "Exact finite diagnostics accompany, and do not replace, the global mathematical proof.",
    }


def main():
    started = time.perf_counter()
    rng = random.Random(20261105)
    mixed = CounterMachine([
        Instruction.inc(0, 2),
        Instruction.inc(1, 3),
        Instruction.decjz(0, zero=5, positive=4),
        Instruction.decjz(1, zero=6, positive=1),
        Instruction.inc(1, 6),
        Instruction.halt(),
    ])
    compilers = [ContractingCompiler(m) for m in (countdown_machine(), nonhalting_machine(), mixed)]
    report = {
        "status": "all exact assertions passed",
        "python": platform.python_version(),
        "arithmetic": "Python standard-library fractions.Fraction",
        "random_seed": 20261105,
        "projection": check_projection(rng),
        "compilers": [compiler_certificate(c) for c in compilers],
        "valid_encoded_transition_checks": [check_valid_machine_steps(c) for c in compilers],
        "countdown_traces": [trace_countdown(n) for n in (0, 1, 2, 5, 20, 100)],
        "nonhalting_example": check_nonhalting_prefix(120),
        "global_composition": check_global_composition(compilers[0], rng),
        "limitations": [
            "No proof assistant verification is claimed.",
            "No universal counter-machine execution is claimed.",
            "No finite-precision physical implementation is claimed.",
            "No historical originality for contraction-undecidability is claimed.",
        ],
    }
    report["elapsed_seconds"] = round(time.perf_counter() - started, 6)
    path = Path(__file__).with_name("execution_record.json")
    path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
