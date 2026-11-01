"""Exact discrete checks for persistent-memory gauge recovery.

No iid coin or reset is simulated. The checks establish finite algebra,
spatial correction of fixed bad reporters, and a cross-cycle error-family
invariant under arbitrary reports in a fresh-fault round.
"""
from pathlib import Path
from collections import deque
from itertools import combinations
import json

HERE = Path(__file__).resolve().parent


def pauli(x=0, z=0, n=9):
    return x | (z << n)


def commute(p, q, n=9):
    mask = (1 << n) - 1
    return (((p & mask) & (q >> n)).bit_count()
            + ((p >> n) & (q & mask)).bit_count()) % 2 == 0


def span(generators):
    out = {0}
    for g in generators:
        out |= {x ^ g for x in list(out)}
    return out


def algebra_check():
    n = 9
    site = lambda r, c: 3 * r + c
    gauges = []
    for r in range(3):
        for c in range(2):
            gauges.append(pauli(x=(1 << site(r, c)) | (1 << site(r, c + 1))))
    for r in range(2):
        for c in range(3):
            gauges.append(pauli(z=(1 << site(r, c)) | (1 << site(r + 1, c))))
    i = site(0, 0)
    generators = gauges + [pauli(x=1 << i), pauli(z=1 << i)]
    alg = span(generators)
    logical_x = pauli(x=sum(1 << site(r, 1) for r in range(3)))
    logical_z = pauli(z=sum(1 << site(1, c) for c in range(3)))
    assert not commute(logical_x, logical_z)
    assert all(commute(logical_x, a) and commute(logical_z, a) for a in alg)
    assert all((a ^ g) in alg for a in alg for g in generators)
    # Arbitrarily strong warm disturbances across every column can realize Z_L.
    all_columns = span(gauges + [pauli(z=1 << site(0, c)) for c in range(3)])
    bad_logical_z = pauli(z=sum(1 << site(0, c) for c in range(3)))
    assert bad_logical_z in all_columns
    # During force-off H gates, a module acts only at its dispersive site.
    # The full Pauli algebra of that site is included, not merely Z_i.
    assert pauli(x=1 << i, z=1 << i) in alg
    return {
        "physical_qubits": n,
        "gauge_group_size_ignoring_phase": len(span(gauges)),
        "persistent_single_site_algebra_size": len(alg),
        "generator_closure_checks": len(alg) * len(generators),
        "clean_row_column_logicals_commute_with_entire_algebra": True,
        "chosen_logical_X_Z_anticommute": True,
        "all_columns_strong_noise_contains_logical_Z": True,
    }


def parallel_star_check():
    """A parallel diagonal star plus one local fault is Pauli_k times gauge."""
    n, k, neighbours = 7, 3, (0, 2, 4, 6)
    xk, zk = pauli(x=1 << k, n=n), pauli(z=1 << k, n=n)
    diagonal_star = [pauli(z=1 << j, n=n) for j in (k,) + neighbours]
    incident_gauges = [pauli(z=(1 << k) | (1 << j), n=n)
                       for j in neighbours]
    actual_algebra = span([xk] + diagonal_star)
    representative_algebra = span([xk, zk] + incident_gauges)
    assert actual_algebra == representative_algebra
    return {
        "star_degree": len(neighbours),
        "algebra_size_ignoring_phase": len(actual_algebra),
        "single_site_Pauli_times_incident_gauge_equals_star_fault_algebra": True,
        "data_fault_may_corrupt_many_incident_reports_in_one_snapshot": True,
        "requires": "Distinct simultaneously controlled module fault domains; shared propagating apparatus faults are charged at their actual support."
    }


def edge_disjoint_paths(n, edges, source, target, count):
    """Polynomial unit-capacity max flow, using one bottleneck per edge."""
    size = n + 2 * len(edges)
    cap = [[0] * size for _ in range(size)]
    for k, (u, v) in enumerate(edges):
        ein, eout = n + 2 * k, n + 2 * k + 1
        cap[u][ein] = cap[v][ein] = count
        cap[ein][eout] = 1
        cap[eout][u] = cap[eout][v] = count
    residual = [row[:] for row in cap]
    value = 0
    while value < count:
        parent = [-1] * size
        parent[source] = source
        queue = deque([source])
        while queue and parent[target] < 0:
            u = queue.popleft()
            for v, c in enumerate(residual[u]):
                if c and parent[v] < 0:
                    parent[v] = u
                    queue.append(v)
        if parent[target] < 0:
            raise ValueError("Insufficient edge connectivity")
        v = target
        while v != source:
            u = parent[v]
            residual[u][v] -= 1
            residual[v][u] += 1
            v = u
        value += 1
    flow = [[max(0, cap[u][v] - residual[u][v]) for v in range(size)]
            for u in range(size)]
    paths = []
    for _ in range(count):
        parent = [-1] * size
        parent[source] = source
        queue = deque([source])
        while queue and parent[target] < 0:
            u = queue.popleft()
            for v, f in enumerate(flow[u]):
                if f and parent[v] < 0:
                    parent[v] = u
                    queue.append(v)
        assert parent[target] >= 0
        arcs = []
        v = target
        while v != source:
            u = parent[v]
            arcs.append((u, v))
            flow[u][v] -= 1
            v = u
        arcs.reverse()
        selected = [(u - n) // 2 for u, v in arcs
                    if u >= n and (u - n) % 2 == 0 and v == u + 1]
        paths.append(selected)
    assert len(set(k for path in paths for k in path)) == sum(map(len, paths))
    return paths


def cut_bits(vertex_bits, edges):
    return sum((((vertex_bits >> u) ^ (vertex_bits >> v)) & 1) << k
               for k, (u, v) in enumerate(edges))


def decode_cut(observed, n, edges, paths, b=1):
    vertices = 0
    for v in range(1, n):
        votes = [sum((observed >> k) & 1 for k in path) % 2 for path in paths[v]]
        if sum(votes) > len(votes) // 2:
            vertices |= 1 << v
    reconstructed = cut_bits(vertices, edges)
    mismatch = (reconstructed ^ observed).bit_count()
    return vertices, mismatch > b, mismatch


def spatial_check():
    n = 7
    edges = sorted({tuple(sorted((i, (i + 1) % n))) for i in range(n)}
                   | {(0, 3), (1, 4), (2, 5), (3, 6)})
    weights = [cut_bits(v << 1, edges).bit_count() for v in range(1, 1 << (n - 1))]
    distance = min(weights)
    assert distance == 3
    paths = {v: edge_disjoint_paths(n, edges, 0, v, 3) for v in range(1, n)}
    violations = []
    cases = 0
    for v in range(1 << (n - 1)):
        vertex_bits = v << 1  # Fix root sign to +1.
        codeword = cut_bits(vertex_bits, edges)
        for error in [0] + [1 << k for k in range(len(edges))]:
            cases += 1
            decoded, flag, _ = decode_cut(codeword ^ error, n, edges, paths)
            if decoded != vertex_bits or flag:
                violations.append((vertex_bits, error, decoded, flag))
    assert not violations
    outside = {"flagged": 0, "silent_wrong": 0, "correct": 0}
    counterexample = None
    for k, l in combinations(range(len(edges)), 2):
        observed = (1 << k) | (1 << l)
        decoded, flag, mismatch = decode_cut(observed, n, edges, paths)
        key = "flagged" if flag else ("silent_wrong" if decoded else "correct")
        outside[key] += 1
        if key == "silent_wrong" and counterexample is None:
            counterexample = {"bad_edges": [k, l], "decoded_vertices": decoded,
                              "distance_to_incorrect_cut": mismatch}
    return {
        "vertices": n, "edges": edges, "edge_count": len(edges),
        "edge_connectivity_and_cut_code_distance": distance,
        "edge_disjoint_paths_from_root": paths,
        "all_vertex_patterns_and_at_most_one_bad_edge_cases": cases,
        "violations": violations,
        "two_bad_edge_outside_contract_counts_for_zero_cut": outside,
        "two_bad_edge_silent_failure_example": counterexample,
        "three_spatial_replicas_of_path_edge_count": 3 * (n - 1),
        "complete_graph_edge_count": n * (n - 1) // 2,
        "seven_by_seven_graph_modules": 2 * n * len(edges),
        "two_mode_apparatus_modes_if_one_dedicated_module_per_edge": 4 * n * len(edges),
    }


def syndrome(e, n):
    return (e ^ (e >> 1)) & ((1 << (n - 1)) - 1)


def correction(syn, n):
    # Solve adjacent differences with bit0 fixed to zero, then choose the
    # lower-weight of the two complementary solutions (n is odd).
    candidate = 0
    bit = 0
    for i in range(n - 1):
        bit ^= (syn >> i) & 1
        candidate |= bit << (i + 1)
    complement = candidate ^ ((1 << n) - 1)
    return candidate if candidate.bit_count() < complement.bit_count() else complement


def temporal_recovery(n, initial, flip, fault_round, bad_report):
    state, previous, history = initial, None, []
    reached = False
    for r in range(1, 5):
        if r == fault_round:
            reached = True
            state ^= flip
            report = bad_report
        else:
            report = syndrome(state, n)
        history.append(report)
        if previous is not None and previous == report:
            return {"residual": state ^ correction(report, n),
                    "fault_reached": reached, "rounds": r,
                    "flag": False, "history": history}
        previous = report
    return {"residual": state, "fault_reached": reached,
            "rounds": 4, "flag": True, "history": history}


def temporal_check(n=7, b=1):
    fixed = 1 if b else 0
    one = [0] + [1 << k for k in range(n)]
    initial = sorted({e ^ d for e in one for d in [0, fixed]})
    outcomes = {}
    violations = []
    reached_count = 0
    for e0 in initial:
        for flip in one:
            possible = set()
            for fault_round in range(1, 5):
                for report in range(1 << (n - 1)):
                    r = temporal_recovery(n, e0, flip, fault_round, report)
                    reached_count += r["fault_reached"]
                    possible.add((r["residual"], r["fault_reached"]))
                    if r["flag"] or r["residual"] not in (0, flip):
                        if len(violations) < 10:
                            violations.append({"initial": e0, "flip": flip,
                                               "fault_round": fault_round,
                                               "report": report, "result": r})
            outcomes[(e0, flip)] = possible
    expected_success = (n - 1) // 2 >= b + 2
    if expected_success:
        assert not violations
    else:
        assert violations
    return {
        "component_length": n, "persistent_support_size": b,
        "previous_surviving_fault_components": 1,
        "new_fault_components": 1,
        "decoder_capacity": (n - 1) // 2,
        "initial_component_vectors": len(initial),
        "scheduled_cases": len(initial) * len(one) * 4 * (1 << (n - 1)),
        "reached_fault_cases": reached_count,
        "violations_first_ten": violations,
    }, outcomes


def cycle_check(n, b, outcomes):
    fixed = 1 if b else 0
    one = [0] + [1 << k for k in range(n)]
    z_boundary = {e ^ d for e in one for d in [0, fixed]}
    boundary = {(x, z) for x in one for z in z_boundary}
    outputs = set()
    cases = 0
    violations = []
    capacity = (n - 1) // 2
    # Exact invariant proof is in the report. We enumerate all boundary
    # components, all aggregate strong-memory Pauli components at the fixed
    # representative, all fresh Pauli components, and every possible
    # temporal-recovery output found above.
    for x0, z0 in boundary:
        for bx in {0, fixed}:
            for bz_before in {0, fixed}:
                for bz_after in {0, fixed}:
                    for fx in one:
                        for fz in one:
                            # The fresh event is in the X-syndrome block.
                            for rz, reached in outcomes[(z0 ^ bz_before, fz)]:
                                x_at_Z = x0 ^ bx ^ (fx if reached else 0)
                                assert x_at_Z.bit_count() <= capacity
                                x_out = x_at_Z ^ correction(syndrome(x_at_Z, n), n)
                                out = (x_out, rz ^ bz_after)
                                cases += 1
                                outputs.add(out)
                                if out not in boundary:
                                    violations.append(out)
                            # The fresh event is in the Z-syndrome block.
                            x_at_Z = x0 ^ bx
                            for rx, reached in outcomes[(x_at_Z, fx)]:
                                out = (rx, bz_after ^ (fz if reached else 0))
                                cases += 1
                                outputs.add(out)
                                if out not in boundary:
                                    violations.append(out)
    assert not violations
    return {"component_length": n, "persistent_support_size": b,
            "boundary_family_size": len(boundary), "output_family_size": len(outputs),
            "full_cycle_cases": cases, "violations": violations,
            "output_is_subset_of_same_boundary_family": outputs <= boundary,
            "induction_covers_arbitrarily_many_cycles_under_per_cycle_fault_budget": True,
            "assumed_max_new_faults_per_complete_cycle": 1,
            "important_scope": "Fault budget is over a COMPLETE X+Z cycle, not separately one per half-cycle. Strong nominal gauge-only memory is unrestricted; off-gauge strong support is bounded."}


def costs(n, graph_edges=None, b=0, s=1):
    edges = (n - 1) if graph_edges is None else graph_edges
    per_half_round = n * edges
    m = s + 1
    return {"data_qubits": n * n,
            "gauge_modules": 2 * per_half_round,
            "same_axis_round_meter_uses": per_half_round,
            "fault_free_cycle_meter_uses": 2 * m * per_half_round,
            "at_most_s_new_faults_cycle_meter_uses": m * (s + 2) * per_half_round,
            "hard_cap_meter_uses_even_when_contract_violated": 2 * m * m * per_half_round,
            "physical_Hadamards_per_cycle": 2 * n * n,
            "global_parallel_Hadamard_layers_per_cycle": 2,
            "fully_parallel_fault_free_sensing_time_in_meter_durations": 2 * m,
            "fully_parallel_at_most_s_faults_sensing_time_in_meter_durations": m * (s + 2),
            "fully_parallel_hard_cap_sensing_time_in_meter_durations": 2 * m * m,
            "parallelism_requirements": "Independently available calibrated module controls and receiver channels, explicit power/crosstalk constraints, and local fault domains.",
            "local_Z_phase_corrections_can_coalesce_per_qubit_per_same_axis_block": True,
            "localization": "Dedicated modules per edge; sharing requires a separate propagated-support contract."}


def main():
    t5, o5 = temporal_check(5, 0)
    t7, o7 = temporal_check(7, 1)
    fail5, _ = temporal_check(5, 1)
    result = {
        "algebra": algebra_check(),
        "parallel_star_fault_algebra": parallel_star_check(),
        "spatial_reporter_redundancy": spatial_check(),
        "old_error_plus_new_fault_no_strong_defect": t5,
        "old_error_plus_new_fault_plus_one_persistent_defect": t7,
        "insufficient_capacity_five_component_counterexample": fail5,
        "five_by_five_repeatable_cycle": cycle_check(5, 0, o5),
        "seven_by_seven_repeatable_cycle": cycle_check(7, 1, o7),
        "five_by_five_path_cost": costs(5),
        "seven_by_seven_path_cost_intact_reporters": costs(7, b=1),
        "seven_by_seven_redundant_graph_cost_one_broken_reporter": costs(7, 11, b=1),
        "scope": "Exact finite discrete algebra and adversarial record histories. Not a threshold, experimental rate, or iid device model. Quantum statements use the ordinary joint operator-algebra and actual receiver lemmas in the accompanying report."}
    path = HERE / "persistent_receiver_checks.json"
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ("spatial_reporter_redundancy",)}, indent=2))


if __name__ == "__main__":
    main()
