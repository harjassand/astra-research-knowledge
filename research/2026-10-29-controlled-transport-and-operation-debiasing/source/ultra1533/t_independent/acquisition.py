"""One declared acquisition/control/comparison batch. No rerun-until-pass rule."""
import hashlib
import itertools
import json
from dataclasses import asdict
from pathlib import Path
import time
import numpy as np
from flint import fmpq, fmpq_mat, arb, ctx
from exact_conductance import Frame, cycle, torus, Counts, Bits, LazyUniform
from quantized_field import sample_quantized, exact_ldl
from ordinary import approximate_draw, GaussianRejection, alternating_gaussian

HERE = Path(__file__).resolve().parent


def bareiss(matrix):
    """Independent integer determinant (not a call to the producer inverse)."""
    A = [list(row) for row in matrix]
    n, sign, previous = len(A), 1, 1
    for k in range(n - 1):
        if A[k][k] == 0:
            pivot = next(j for j in range(k + 1, n) if A[j][k])
            A[k], A[pivot] = A[pivot], A[k]
            sign *= -1
        pivot = A[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                value = A[i][j] * pivot - A[i][k] * A[k][j]
                assert value % previous == 0
                A[i][j] = value // previous
        previous = pivot
        for i in range(k + 1, n):
            A[i][k] = 0
    return sign * A[-1][-1]


def literal_matrix(vertices, edges, state, q=2):
    A = [[0] * (vertices - 1) for _ in range(vertices - 1)]
    for (u, v), x in zip(edges, state):
        weight = 1 + (q - 1) * x
        if u:
            A[u - 1][u - 1] += weight
        if v:
            A[v - 1][v - 1] += weight
        if u and v:
            A[u - 1][v - 1] -= weight
            A[v - 1][u - 1] -= weight
    return A


def static_controls():
    started = time.perf_counter()
    ctx.prec = 192
    frame = Frame(6, cycle(6))
    states = list(itertools.product((0, 1), repeat=6))
    determinant, inverses, weights, conditionals = {}, {}, {}, {}
    ratio_checks = transfer_checks = 0
    columns = fmpq_mat([[frame.columns[e][i, 0] for e in range(frame.m)] for i in range(frame.size)])
    for state in states:
        det = bareiss(literal_matrix(6, frame.edges, state))
        assert det == frame.determinant_for(state)
        determinant[state] = det
        inverses[state] = inverse = frame.inverse_for(state)
        R = columns.transpose() * inverse * columns
        weighted = fmpq_mat([[fmpq(1 + state[i]) if i == j else 0 for j in range(6)] for i in range(6)])
        assert R * weighted * R == R
        transfer_checks += 36
        weights[state] = 1 / arb(det).sqrt()
    for state in states:
        conditionals[state] = []
        for e in range(frame.m):
            low = list(state); low[e] = 0
            high = list(state); high[e] = 1
            ratio = fmpq(determinant[tuple(high)], determinant[tuple(low)])
            assert frame.low_ratio(inverses[state], state, e)[0] == ratio
            ratio_checks += 1
            h = 1 / (1 + arb(ratio).sqrt())
            conditionals[state].append(h)
    largest = arb(0)
    adjacent_checks = 0
    for state in states:
        for f in range(frame.m):
            other = list(state); other[f] = 1 - other[f]; other = tuple(other)
            influence = sum((abs(conditionals[state][e] - conditionals[other][e]) for e in range(frame.m) if e != f), arb(0))
            assert influence < arb(fmpq(43, 1000))
            if float(influence.mid()) > float(largest.mid()):
                largest = influence
            adjacent_checks += 1
    Z = sum(weights.values(), arb(0))
    mean = sum((weights[s] * sum(s) for s in states), arb(0)) / Z
    second = sum((weights[s] * sum(s) ** 2 for s in states), arb(0)) / Z

    # Direct-vs-rank-one inverse controls, including additions AND removals.
    counts, state = Counts(), [0] * frame.m
    bits, inverse = Bits(2026103091, counts), fmpq_mat(frame.base_inverse)
    for _ in range(256):
        e = bits.edge(frame.m)
        inverse = frame.update(inverse, state, e, LazyUniform(bits), counts)
        assert inverse == frame.inverse_for(state)

    # Force the word-prepend/replay path; this special control does not use the
    # conservative default initial window or its displayed 8L execution bound.
    forced = Frame(6, cycle(6)); forced.initial_window = 1
    forced_counts = Counts()
    forced.sample(Bits(2026103092, forced_counts), forced_counts)
    assert forced_counts.runs >= 4 and forced_counts.largest_window >= 8

    # Exact conditional covariance factorization, independent reconstruction.
    lower, diagonal = exact_ldl(inverse)
    T = fmpq_mat(lower)
    D = fmpq_mat([[diagonal[i] if i == j else 0 for j in range(5)] for i in range(5)])
    assert T * D * T.transpose() == inverse

    # Nonconvex curvature, not inferred from a Monte Carlo observable.
    q2_curvature = (3 - arb(99).log()) / 2
    q4_curvature = (5 - 3 * arb(99).log()) / 2
    assert q2_curvature < -arb(fmpq(1, 2)) and q4_curvature < -4

    return {"seconds": time.perf_counter() - started, "states": len(states),
            "integer_determinant_checks": len(states), "exact_conditional_ratio_checks": ratio_checks,
            "exact_transfer_current_entries": transfer_checks, "adjacent_influence_checks": adjacent_checks,
            "max_influence_ball": str(largest), "influence_upper": "43/1000",
            "rank_update_direct_inverse_checks": 256, "forced_doubling": asdict(forced_counts),
            "exact_ldl_identity": True, "cycle_count_mean": str(mean), "cycle_count_variance": str(second - mean * mean),
            "cycle_mean_display": float(mean.mid()), "cycle_variance_display": float((second - mean * mean).mid()),
            "nonconvex_curvature_q2": str(q2_curvature), "nonconvex_curvature_q4": str(q4_curvature)}


def run_cases(protocol, controls):
    results = []
    for spec in protocol["cases"]:
        begin = time.perf_counter()
        edges = cycle(6) if spec["name"] == "cycle6" else torus(round(spec["vertices"] ** 0.5))
        frame = Frame(spec["vertices"], edges, fmpq(spec["q"]), fmpq(spec["p"]), spec["r"],
                      fmpq(spec["contraction_upper"]) if "contraction_upper" in spec else None)
        construction = time.perf_counter() - begin
        counts = Counts(); bits = Bits(spec["seed"], counts)
        output = []
        begin = time.perf_counter()
        for _ in range(spec.get("conductance_draws", spec.get("quantized_field_draws"))):
            if "quantized_field_draws" in spec:
                state, bins, field_stats = sample_quantized(frame, bits, counts, fmpq(spec["width"]))
                output.append({"conductance": state, "field_bins": bins, "field_stats": field_stats})
            else:
                state, _ = frame.sample(bits, counts)
                output.append({"conductance": state})
        elapsed = time.perf_counter() - begin
        record = {"name": spec["name"], "input": spec, "vertices": frame.vertices, "edges": frame.m,
                  "frame_seconds": construction, "sample_seconds": elapsed, "counts": asdict(counts),
                  "contraction_consumed": str(frame.c), "initial_window": frame.initial_window,
                  "proved_mean_state_update_upper_per_draw": 8 * frame.initial_window,
                  "output": output}
        if spec["name"] == "cycle6":
            observed = np.mean([sum(x["conductance"]) for x in output])
            sem = (controls["cycle_variance_display"] / len(output)) ** 0.5
            record["statistic"] = {"observable": "number of high conductances", "observed": float(observed),
                                   "exact_mean_display": controls["cycle_mean_display"], "sem": sem,
                                   "z": (observed - controls["cycle_mean_display"]) / sem,
                                   "policy": "retained diagnostic, not a proof or pass criterion"}
        (HERE / (spec["name"] + "_OUTPUT.json")).write_text(json.dumps(record, indent=2) + "\n")
        compact = {k: v for k, v in record.items() if k != "output"}
        compact["output_sha256"] = hashlib.sha256((HERE / (spec["name"] + "_OUTPUT.json")).read_bytes()).hexdigest()
        results.append(compact)
        print(json.dumps({"case": spec["name"], "seconds": elapsed, "bits": counts.fair_bits}), flush=True)
    return results


def comparators(protocol):
    frame = Frame(16, torus(4))
    records = {}
    # Same conditional and same literal quantized-output engine, proved TV1/100.
    counts = Counts(); bits = Bits(protocol["ordinary_seeds"][0], counts)
    start = time.perf_counter()
    approximate = [approximate_draw(frame, bits, counts) for _ in range(64)]
    records["proved_approximate_chain"] = {"seconds": time.perf_counter() - start, "counts": asdict(counts),
                                            "draws": 64, "steps_per_draw": approximate[0][2]["burnin_updates"],
                                            "tv_per_draw": "1/100", "joint_64_output_tv_bound": "16/25"}
    # Ordinary EXACT quantized full-field target; no uncontrolled burn-in.
    counts = Counts(); bits = Bits(protocol["ordinary_seeds"][2], counts)
    start = time.perf_counter()
    rejection = GaussianRejection(frame)
    rejected_field = [rejection.sample(bits) for _ in range(64)]
    records["exact_gaussian_rejection"] = {"seconds": time.perf_counter() - start, "counts": asdict(counts),
                                             "draws": 64, "proposals": rejection.proposals,
                                             "interval_evaluations": rejection.rounds, "max_depth": rejection.max_depth,
                                             "target": "identical exact quarter-grid full field law"}
    start = time.perf_counter()
    ordinary, stats = alternating_gaussian(frame, 64, protocol["ordinary_seeds"][1])
    records["latent_gaussian_gibbs"] = {"seconds": time.perf_counter() - start, "draws": 64, **stats}
    (HERE / "ORDINARY_OUTPUT.json").write_text(json.dumps({"proved_approximate": approximate,
                                                         "exact_gaussian_rejection": rejected_field,
                                                         "latent_gaussian": ordinary}, indent=2) + "\n")
    return records


def main():
    protocol = json.loads((HERE / "PROTOCOL.json").read_text())
    start = time.perf_counter()
    controls = static_controls()
    (HERE / "CONTROLS.json").write_text(json.dumps(controls, indent=2) + "\n")
    cases = run_cases(protocol, controls)
    baseline = comparators(protocol)
    record = {"status": "completed private computational construction; no independent audit/material acquisition",
              "total_seconds": time.perf_counter() - start, "protocol_sha256": hashlib.sha256((HERE / "PROTOCOL.json").read_bytes()).hexdigest(),
              "controls": controls, "cases": cases, "ordinary": baseline,
              "scope": "exact arithmetic/strict-Arb diagnostic under seeded bits; mathematical iid result under ideal fair bits and outward primitives",
              "physical_actions": 0}
    (HERE / "EXECUTION.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"total_seconds": record["total_seconds"], "ordinary": baseline}), flush=True)


if __name__ == "__main__":
    main()
