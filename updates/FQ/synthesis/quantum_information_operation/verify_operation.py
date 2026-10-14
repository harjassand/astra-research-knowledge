#!/usr/bin/env python3
"""Finite checks for the accompanying conditional-exchange information report.

Only NumPy and the Python standard library are used. These checks are evidence
for finite instances, not an external proof review or a hardware experiment.
All output is written next to this script; no source packet or repository is
modified.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent
RNG = np.random.default_rng(202610150713)


def tensor(*states):
    result = np.array([[1.0]], dtype=complex)
    for state in states:
        result = np.kron(result, state)
    return result


def reorder(state, dims, order):
    n = len(dims)
    axes = list(order) + [n + i for i in order]
    return state.reshape(tuple(dims) * 2).transpose(axes).reshape(state.shape)


def reduce(state, dims, keep):
    keep = list(keep)
    drop = [i for i in range(len(dims)) if i not in keep]
    perm = reorder(state, dims, keep + drop)
    d_keep = math.prod(dims[i] for i in keep)
    d_drop = math.prod(dims[i] for i in drop)
    return np.einsum("abcb->ac", perm.reshape(d_keep, d_drop, d_keep, d_drop))


def entropy(state):
    values = np.linalg.eigvalsh((state + state.conj().T) / 2)
    values = values[values > 1e-13]
    return float(-np.sum(values * np.log2(values)))


def random_state(d):
    x = RNG.normal(size=(d, d)) + 1j * RNG.normal(size=(d, d))
    x = x @ x.conj().T
    return x / np.trace(x)


def close(a, b, tol=2e-10):
    error = float(np.max(np.abs(np.asarray(a) - np.asarray(b))))
    assert error < tol, (error, tol)
    return error


def cycles(perm):
    seen, result = set(), []
    for start in range(len(perm)):
        if start in seen:
            continue
        component, i = [], start
        while i not in seen:
            seen.add(i)
            component.append(i)
            i = perm[i]
        result.append(component)
    return result


def pair_triple_route(labels):
    # perm[i] is the donor whose A (logical R,S) appears at recipient i.
    perm = list(range(len(labels)))
    for c in set(labels):
        group = [i for i, value in enumerate(labels) if value == c]
        if len(group) <= 1:
            continue
        if len(group) % 2:
            a, b, d = group[:3]
            perm[a], perm[b], perm[d] = b, d, a
            group = group[3:]
        for a, b in zip(group[0::2], group[1::2]):
            perm[a], perm[b] = b, a
    return perm


def correlation_graph_checks():
    max_errors = {"tagged_product": 0.0, "global_mutual_information": 0.0,
                  "output_multi_information": 0.0, "retained_mutual_information": 0.0,
                  "disjoint_retained_product": 0.0}
    cases = 0
    # Includes non-derangements to check the number-moved correction.
    configurations = [(2, [1, 0]), (3, [1, 2, 0]),
                      (3, [1, 0, 2]), (4, [1, 0, 3, 2]),
                      (4, [1, 2, 3, 0])]
    for n, perm in configurations:
        for _ in range(3):
            rho = random_state(4)
            rho_a, rho_e = reduce(rho, [2, 2], [0]), reduce(rho, [2, 2], [1])
            info = entropy(rho_a) + entropy(rho_e) - entropy(rho)
            original = tensor(*([rho] * n))
            order = [item for i in range(n) for item in (2 * perm[i], 2 * i + 1)]
            output = reorder(original, [2] * (2 * n), order)
            local_entropies = []
            for i in range(n):
                marginal = reduce(output, [2] * (2 * n), [2 * i, 2 * i + 1])
                target = rho if perm[i] == i else tensor(rho_a, rho_e)
                error = close(marginal, target)
                max_errors["tagged_product"] = max(max_errors["tagged_product"], error)
                local_entropies.append(entropy(marginal))
            all_a = reduce(output, [2] * (2 * n), list(range(0, 2 * n, 2)))
            all_e = reduce(output, [2] * (2 * n), list(range(1, 2 * n, 2)))
            global_info = entropy(all_a) + entropy(all_e) - entropy(output)
            error = close(global_info, n * info)
            max_errors["global_mutual_information"] = max(max_errors["global_mutual_information"], error)
            moved = sum(perm[i] != i for i in range(n))
            error = close(sum(local_entropies) - entropy(output), moved * info)
            max_errors["output_multi_information"] = max(max_errors["output_multi_information"], error)
            for bits in itertools.product((False, True), repeat=n):
                retained = [i for i, flag in enumerate(bits) if flag]
                if not retained:
                    continue
                marginal = reduce(output, [2] * (2 * n),
                                  [item for i in retained for item in (2 * i, 2 * i + 1)])
                a = reduce(marginal, [2] * (2 * len(retained)), list(range(0, 2 * len(retained), 2)))
                e = reduce(marginal, [2] * (2 * len(retained)), list(range(1, 2 * len(retained), 2)))
                overlap = len(set(retained).intersection(perm[i] for i in retained))
                error = close(entropy(a) + entropy(e) - entropy(marginal), overlap * info)
                max_errors["retained_mutual_information"] = max(max_errors["retained_mutual_information"], error)
                if overlap == 0:
                    error = close(marginal, tensor(*([tensor(rho_a, rho_e)] * len(retained))))
                    max_errors["disjoint_retained_product"] = max(max_errors["disjoint_retained_product"], error)
                cases += 1
    return {"passed": True, "retained_subset_cases": cases, "max_errors": max_errors}


def compilation_checks():
    table = []
    for n in range(2, 9):
        best = n
        tested = 0
        for perm in itertools.permutations(range(n)):
            if any(perm[i] == i for i in range(n)):
                continue
            best = min(best, n - len(cycles(perm)))
            tested += 1
        route = pair_triple_route([0] * n)
        observed = n - len(cycles(route))
        assert best == observed == math.ceil(n / 2)
        table.append({"class_size": n, "derangements_enumerated": tested,
                      "minimum_block_swaps": best, "checkpoint_cycle_swaps": n - 1})
    return {"passed": True, "table": table}


def polynomial_checks():
    table = []
    for m in range(1, 7):
        n = 2 * m - 1
        order = n + 1
        diff = sum(Fraction((-1) ** (order - j) * math.comb(order, j))
                   * Fraction(j, order) ** (2 * m) for j in range(order + 1))
        target = Fraction(math.factorial(order), order ** order)
        assert diff == target > 0
        for degree in range(n + 1):
            observed = sum(Fraction((-1) ** (order - j) * math.comb(order, j))
                           * Fraction(j, order) ** degree for j in range(order + 1))
            assert observed == 0
        table.append({"N": n, "m": m, "target_finite_difference": str(diff),
                      "uniform_trace_error_lower_bound": str(diff / (2 ** order))})
    return {"passed": True, "note": "Finite differences certify the degree mismatch, not arbitrary channels by enumeration.",
            "table": table}


def label_lipschitz_checks():
    # Extreme vertices suffice: every change is affine in the six scores.
    maximum, witness, cases = 0, None, 0
    for n in range(1, 8):
        compositions = [(a, b, n - a - b) for a in range(n + 1) for b in range(n - a + 1)]
        for scores in itertools.product((0, 1), repeat=6):
            natural, dec = scores[:3], scores[3:]
            def value(counts):
                return sum(0 if k == 0 else natural[c] if k == 1 else k * dec[c]
                           for c, k in enumerate(counts))
            for counts in compositions:
                for old in range(3):
                    if counts[old] == 0:
                        continue
                    for new in range(3):
                        if new == old:
                            continue
                        changed = list(counts)
                        changed[old] -= 1
                        changed[new] += 1
                        delta = abs(value(changed) - value(counts))
                        assert delta <= 3
                        cases += 1
                        if delta > maximum:
                            maximum = delta
                            witness = {"counts": counts, "old": old, "new": new,
                                       "natural_scores": natural, "decorrelated_scores": dec}
    assert maximum == 3
    return {"passed": True, "cases": cases, "max_sum_change": maximum,
            "bounded_score_witness": witness}


def reference_pairing_countermodel():
    psi = np.zeros(8, dtype=complex)
    psi[0] = psi[5] = 1 / math.sqrt(2)  # (r,s,e)=(0,0,0),(1,0,1)
    rho = np.outer(psi, psi.conj())
    original = tensor(rho, rho)
    routed = reorder(original, [2] * 6, [0, 4, 2, 3, 1, 5])
    routing_error = close(routed, original)
    future = reorder(routed, [2] * 6, [0, 2, 1, 3, 5, 4])
    bell = np.array([1, 0, 0, 1], dtype=complex) / math.sqrt(2)
    effect = np.outer(bell, bell.conj())
    resident = float(np.trace(effect @ reduce(future, [2] * 6, [0, 1])).real)
    donor = float(np.trace(effect @ reduce(future, [2] * 6, [3, 1])).real)
    close(resident, 1)
    close(donor, 0.25)
    return {"passed": True, "physical_state_routing_change_max_entry": routing_error,
            "resident_reference_Bell_score": resident, "donor_reference_Bell_score": donor,
            "tracked_contrast": resident - donor}


def bell_cycle_checks():
    table = []
    for n in range(2, 8):
        perm = list(range(1, n)) + [0]
        for u in (Fraction(1, 5), Fraction(1, 2)):
            distribution = []
            for bits in itertools.product((0, 1), repeat=n):
                probability = math.prod(u if bit else 1 - u for bit in bits)
                scores = [int(bits[perm[i]] == bits[i]) for i in range(n)]
                assert sum(1 - score for score in scores) % 2 == 0
                distribution.append((probability, scores))
            q = (1 - u) ** 2 + u ** 2
            mean = sum(p * sum(x) for p, x in distribution)
            variance = sum(p * (sum(x) - mean) ** 2 for p, x in distribution)
            v = u * (1 - u)
            expected = 2 * n * q * (1 - q) if n == 2 else 4 * n * v * (1 - 3 * v)
            assert mean == n * q and variance == expected
            table.append({"cycle_length": n, "u": str(u), "mean_each": str(q),
                          "sum_variance": str(variance), "iid_sum_variance": str(n * q * (1 - q)),
                          "global_even_mismatch_constraint": True})
    return {"passed": True, "table": table}


def concentration_mgf_checks():
    # Exact finite enumeration of a nontrivial condition-matched Bell phase assay.
    n, p, u = 5, (Fraction(3, 5), Fraction(2, 5)), (Fraction(1, 5), Fraction(2, 5))
    distribution = []
    for labels in itertools.product((0, 1), repeat=n):
        label_probability = math.prod(p[c] for c in labels)
        perm = pair_triple_route(labels)
        component_denominator = sum(len(component) ** 2 for component in cycles(perm))
        assert component_denominator <= 3 * n
        conditional = []
        for bits in itertools.product((0, 1), repeat=n):
            probability = math.prod(u[c] if bit else 1 - u[c] for c, bit in zip(labels, bits))
            total = sum(int(bits[perm[i]] == bits[i]) for i in range(n))
            conditional.append((float(probability), total))
            distribution.append((float(label_probability * probability), total))
        mean = sum(probability * total for probability, total in conditional)
        for lam in np.linspace(-2, 2, 17):
            mgf = sum(probability * math.exp(lam * (total - mean)) for probability, total in conditional)
            assert mgf <= math.exp(component_denominator * lam ** 2 / 8) + 1e-10
    mean = sum(probability * total for probability, total in distribution)
    max_ratio = 0.0
    for lam in np.linspace(-2, 2, 33):
        mgf = sum(probability * math.exp(lam * (total - mean)) for probability, total in distribution)
        bound = math.exp(12 * n * lam ** 2 / 8)
        assert mgf <= bound + 1e-10
        max_ratio = max(max_ratio, mgf / bound)
    b, delta, batch_n = 4000, 0.05, 32
    original_radius = math.sqrt(math.log(8 / delta) / (2 * b))
    new_radius = math.sqrt(6 * math.log(8 / delta) / (b * batch_n))
    return {"passed": True, "enumerated_label_and_phase_assignments": len(distribution),
            "largest_unconditional_mgf_to_bound_ratio": max_ratio,
            "example": {"B": b, "N": batch_n, "delta": delta,
                        "old_four_arm_radius": original_radius,
                        "new_four_arm_radius": new_radius,
                        "new_two_arm_radius": 2 * new_radius,
                        "complete_replica_preparations_four_arms": 4 * b * batch_n}}


def source_hashes():
    packet = Path("/Users/harjas/Downloads/astra_conditional_exchange")
    return {str(path): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(packet.iterdir()) if path.is_file()}


def main():
    results = {
        "scope": "Finite algebra, entropy, exact enumeration and consistency checks; no hardware or novelty verification.",
        "numpy_version": np.__version__,
        "seed": 202610150713,
        "source_packet_hashes": source_hashes(),
        "correlation_graph": correlation_graph_checks(),
        "minimum_swap_compilation": compilation_checks(),
        "universal_polynomial_no_go": polynomial_checks(),
        "label_mean_lipschitz": label_lipschitz_checks(),
        "reference_pairing_countermodel": reference_pairing_countermodel(),
        "Bell_phase_cycle_correlations": bell_cycle_checks(),
        "concentration_mgf": concentration_mgf_checks(),
    }
    path = OUT / "verification_results.json"
    path.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({"all_checks_passed": True, "results": str(path),
                      "example": results["concentration_mgf"]["example"]}, indent=2))


if __name__ == "__main__":
    main()
