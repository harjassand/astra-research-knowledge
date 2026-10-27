"""Acquire sparse Pauli generators from a raw quadratic Boolean phase.

All validation backends are finite exact enumeration or exact elimination of
the introduced linear constraints.  This file does not implement the
governing asymptotic local-phase algorithm and makes no practical speed claim.
Standard library only; run this file to produce its ordinary results JSON.
"""
from __future__ import annotations

import itertools
import json
import random
from pathlib import Path


def parity(x: int) -> int:
    return x.bit_count() & 1


def matvec(rows: list[int], x: int) -> int:
    return sum(parity(row & x) << j for j, row in enumerate(rows))


def add_basis(basis: dict[int, int], vector: int) -> bool:
    x = vector
    while x:
        p = x.bit_length() - 1
        if p in basis:
            x ^= basis[p]
        else:
            basis[p] = x
            return True
    return False


def rank(rows: list[int]) -> int:
    b: dict[int, int] = {}
    for x in rows:
        add_basis(b, x)
    return len(b)


def kernel(rows: list[int], columns: int) -> list[int]:
    """A basis of the nullspace of the binary row constraints."""
    pivots: dict[int, int] = {}
    for row in rows:
        add_basis(pivots, row)
    out = []
    for f in range(columns):
        if f in pivots:
            continue
        x = 1 << f
        for p in sorted(pivots):
            if parity(pivots[p] & x):
                x ^= 1 << p
        assert all(parity(row & x) == 0 for row in rows)
        out.append(x)
    return out


def validate_matrix(rows: list[int]) -> None:
    n = len(rows)
    for i, row in enumerate(rows):
        if row < 0 or row >> n or ((row >> i) & 1):
            raise ValueError("matrix must be alternating and have valid rows")
        for j in range(i):
            if ((row >> j) ^ (rows[j] >> i)) & 1:
                raise ValueError("matrix must be symmetric")


def quadratic(rows: list[int], x: int) -> int:
    answer = 0
    while x:
        bit = x & -x
        i = bit.bit_length() - 1
        x ^= bit
        answer ^= parity(rows[i] & x)
    return answer


def eval_anf(terms: set[int], x: int) -> int:
    value = 0
    for support in terms:
        value ^= (x & support) == support
    return int(value)


def acquire(rows: list[int], maximum_support: int,
            total_support_budget: int | None = None) -> dict:
    """The algorithm sees only raw B and the search limit, never a witness."""
    validate_matrix(rows)
    n = len(rows)
    if not 0 <= maximum_support <= n:
        raise ValueError("invalid support budget")
    if total_support_budget is not None and total_support_budget < 0:
        raise ValueError("invalid total support budget")
    linear_basis: dict[int, int] = {}
    selected: list[int] = []
    weights: list[int] = []
    subset_count = 0
    kernel_vector_count = 0
    ranks_at_weight = [0]
    exhausted_budget = False
    total_weight = 0
    for weight in range(1, maximum_support + 1):
        for support in itertools.combinations(range(n), weight):
            subset_count += 1
            support_mask = sum(1 << v for v in support)
            equations = [
                sum(((rows[v] >> u) & 1) << j for j, u in enumerate(support))
                for v in range(n) if not ((support_mask >> v) & 1)
            ]
            for local in kernel(equations, weight):
                kernel_vector_count += 1
                a = sum(((local >> j) & 1) << v for j, v in enumerate(support))
                z = matvec(rows, a)
                actual_weight = (a | z).bit_count()
                assert actual_weight <= weight
                reduced = a
                while reduced and (reduced.bit_length() - 1) in linear_basis:
                    reduced ^= linear_basis[reduced.bit_length() - 1]
                if reduced:
                    # Anything of smaller support was already in the span.
                    assert actual_weight == weight
                    if total_support_budget is not None and total_weight + actual_weight > total_support_budget:
                        exhausted_budget = True
                        break
                    assert add_basis(linear_basis, a)
                    selected.append(a)
                    weights.append(actual_weight)
                    total_weight += actual_weight
            if exhausted_budget:
                break
        ranks_at_weight.append(len(selected))
        if exhausted_budget:
            break
    dense = []
    for i in range(n):
        if add_basis(linear_basis, 1 << i):
            dense.append(1 << i)
    assert len(selected) + len(dense) == n
    zrows = [matvec(rows, a) for a in selected]
    return {
        "n": n,
        "support_budget": maximum_support,
        "total_support_budget": total_support_budget,
        "exhausted_total_support_budget": exhausted_budget,
        "short_generators": selected,
        "short_z_rows": zrows,
        "dense_completion": dense,
        "rank": len(selected),
        "defect": len(dense),
        "weights": weights,
        "total_pauli_support": sum(weights),
        "total_x_support": sum(a.bit_count() for a in selected),
        "total_z_support": sum(z.bit_count() for z in zrows),
        "ranks_at_weight": ranks_at_weight,
        "searched_supports": subset_count,
        "kernel_basis_vectors": kernel_vector_count,
    }


def true_minimum_weight_basis(rows: list[int]) -> dict:
    """Finite audit only: enumerate every nonzero graph-code word."""
    n = len(rows)
    choices = sorted(((a | matvec(rows, a)).bit_count(), a)
                     for a in range(1, 1 << n))
    b: dict[int, int] = {}
    chosen = []
    for weight, a in choices:
        if add_basis(b, a):
            chosen.append((weight, a))
        if len(chosen) == n:
            break
    return {"weight": sum(w for w, _ in chosen),
            "weights": [w for w, _ in chosen],
            "basis": [a for _, a in chosen]}


def acquire_x_budget(rows: list[int], maximum_support: int, x_budget: int) -> dict:
    """Greedy by X weight inside the acquired short-support graph-code span.

    Kernel vectors are streamed, including their linear combinations. This is
    needed for the X-weight objective; an arbitrary kernel basis alone would
    not implement minimum-X-weight matroid greedy.
    """
    validate_matrix(rows)
    n = len(rows)
    if not 0 <= maximum_support <= n or x_budget < 0:
        raise ValueError("invalid search or X budget")
    basis: dict[int, int] = {}
    selected = []
    x_cost = 0
    stop = False
    searched_supports = 0
    streamed_words = 0
    for x_weight in range(1, maximum_support + 1):
        for size in range(x_weight, maximum_support + 1):
            for support in itertools.combinations(range(n), size):
                searched_supports += 1
                mask = sum(1 << v for v in support)
                equations = [
                    sum(((rows[v] >> u) & 1) << j for j, u in enumerate(support))
                    for v in range(n) if not ((mask >> v) & 1)
                ]
                kb = kernel(equations, size)
                for coefficients in range(1, 1 << len(kb)):
                    local = xor_combination(kb, coefficients)
                    if local.bit_count() != x_weight:
                        continue
                    streamed_words += 1
                    a = sum(((local >> j) & 1) << v for j, v in enumerate(support))
                    reduced = a
                    while reduced and (reduced.bit_length() - 1) in basis:
                        reduced ^= basis[reduced.bit_length() - 1]
                    if not reduced:
                        continue
                    if x_cost + x_weight > x_budget:
                        stop = True
                        break
                    assert add_basis(basis, a)
                    selected.append(a)
                    x_cost += x_weight
                if stop or len(selected) == n:
                    break
            if stop or len(selected) == n:
                break
        if stop or len(selected) == n:
            break
    dense = []
    for i in range(n):
        if add_basis(basis, 1 << i):
            dense.append(1 << i)
    zrows = [matvec(rows, a) for a in selected]
    weights = [(a | z).bit_count() for a, z in zip(selected, zrows)]
    assert all(w <= maximum_support for w in weights)
    return {"n": n, "support_budget": maximum_support, "x_budget": x_budget,
            "objective": "minimum X weight prefix among joint-support-limited words",
            "short_generators": selected, "short_z_rows": zrows,
            "dense_completion": dense, "rank": len(selected), "defect": len(dense),
            "weights": weights, "x_weights": [a.bit_count() for a in selected],
            "total_pauli_support": sum(weights), "total_x_support": x_cost,
            "total_z_support": sum(z.bit_count() for z in zrows),
            "searched_supports": searched_supports, "streamed_words": streamed_words}


def xor_combination(vectors: list[int], selector: int) -> int:
    value = 0
    for j, row in enumerate(vectors):
        if (selector >> j) & 1:
            value ^= row
    return value


def compile_branch(rows: list[int], foreground: set[int], certificate: dict,
                   dense_selector: int) -> dict:
    """Build a fixed-locality ANF with Fourier-enforced affine wire updates."""
    n = len(rows)
    short = certificate["short_generators"]
    zrows = certificate["short_z_rows"]
    r = len(short)
    initial = xor_combination(certificate["dense_completion"], dense_selector)
    # A state is either (constant, bit) or (variable, index).
    states = [("constant", (initial >> v) & 1) for v in range(n)]
    terms: set[int] = set()
    updates = []
    variables = r

    def toggle(support: int) -> None:
        if support in terms:
            terms.remove(support)
        else:
            terms.add(support)

    def add_product(indices: list[int], state=None) -> None:
        support = sum(1 << j for j in set(indices))
        if state is not None:
            kind, value = state
            if kind == "constant":
                if not value:
                    return
            else:
                support |= 1 << value
        toggle(support)

    if quadratic(rows, initial):
        toggle(0)
    for j, (a, z) in enumerate(zip(short, zrows)):
        if quadratic(rows, a):
            add_product([j])
        for v in range(n):
            previous = states[v]
            if (z >> v) & 1:
                add_product([j], previous)
            if (a >> v) & 1:
                next_state = variables
                multiplier = variables + 1
                variables += 2
                add_product([multiplier, next_state])
                add_product([multiplier], previous)
                add_product([multiplier, j])
                updates.append({"selector": j, "coordinate": v,
                                "previous": previous, "next": next_state,
                                "multiplier": multiplier})
                states[v] = ("variable", next_state)
    for support in foreground:
        term = 0
        alive = True
        for v in range(n):
            if not ((support >> v) & 1):
                continue
            kind, value = states[v]
            if kind == "constant":
                if not value:
                    alive = False
                    break
            else:
                term |= 1 << value
        if alive:
            toggle(term)
    assert len(updates) == certificate["total_x_support"]
    assert variables == r + 2 * len(updates)
    return {"variables": variables, "terms": terms, "updates": updates,
            "final_states": states, "initial": initial,
            "normalization_exponent": len(updates), "selectors": r}


def valid_trace(branch: dict, selector: int, multiplier_assignment: int = 0) -> tuple[int, int]:
    assignment = selector
    for j, update in enumerate(branch["updates"]):
        kind, value = update["previous"]
        previous = value if kind == "constant" else ((assignment >> value) & 1)
        next_value = previous ^ ((selector >> update["selector"]) & 1)
        assignment |= next_value << update["next"]
        assignment |= ((multiplier_assignment >> j) & 1) << update["multiplier"]
    original = 0
    for v, (kind, value) in enumerate(branch["final_states"]):
        original |= (value if kind == "constant" else ((assignment >> value) & 1)) << v
    return assignment, original


def count_by_constraint_elimination(rows: list[int], foreground: set[int], certificate: dict) -> tuple[int, dict]:
    """Finite validator: eliminate exactly the affine constraints, then enumerate selectors."""
    total = 0
    trace_checks = 0
    nonzero_multiplier_checks = 0
    branch_records = []
    for dense in range(1 << certificate["defect"]):
        branch = compile_branch(rows, foreground, certificate, dense)
        leaf = 0
        for selector in range(1 << certificate["rank"]):
            assignment, x = valid_trace(branch, selector)
            phase = eval_anf(branch["terms"], assignment)
            assert phase == quadratic(rows, x) ^ eval_anf(foreground, x)
            trace_checks += 1
            # A valid trace cancels every Fourier multiplier exactly.
            masks = [0, (1 << len(branch["updates"])) - 1]
            for multiplier_mask in masks:
                other, other_x = valid_trace(branch, selector, multiplier_mask)
                assert other_x == x and eval_anf(branch["terms"], other) == phase
                nonzero_multiplier_checks += int(multiplier_mask != 0)
            leaf += 1 if phase == 0 else -1
        total += leaf
        branch_records.append({"variables": branch["variables"],
                               "phase_terms": len(branch["terms"]),
                               "normalization_exponent": len(branch["updates"]),
                               "normalized_count": leaf})
    return total, {"valid_trace_identities": trace_checks,
                   "nonzero_multiplier_identities": nonzero_multiplier_checks,
                   "branches": branch_records}


def exhaustive_phase_sum(branch: dict) -> int:
    return sum(1 if eval_anf(branch["terms"], x) == 0 else -1
               for x in range(1 << branch["variables"]))


def direct_count(rows: list[int], foreground: set[int]) -> int:
    return sum(1 if quadratic(rows, x) ^ eval_anf(foreground, x) == 0 else -1
               for x in range(1 << len(rows)))


def cubic_structure_sizes(foreground: set[int], n: int) -> dict:
    """Independent binary linear tests; no centroid decomposition is assumed."""
    pairs = [[0]*n for _ in range(n)]
    for mask in foreground:
        if mask.bit_count() != 3:
            continue
        a, b, c = [i for i in range(n) if (mask >> i) & 1]
        for i, j, k in ((a, b, c), (a, c, b), (b, c, a)):
            pairs[i][j] ^= 1 << k
            pairs[j][i] ^= 1 << k
    radical_dimension = n - rank([pairs[i][j] for i in range(n) for j in range(i+1,n)])
    center_equations = []
    for i in range(n):
        for j in range(n):
            for k in range(n):
                center_equations.append((pairs[j][k] << (n*i)) ^ (pairs[i][k] << (n*j)))
                center_equations.append((pairs[j][k] << (n*i)) ^ (pairs[i][j] << (n*k)))
    centroid_dimension = n*n-rank(center_equations)
    return {"third_derivative_radical_dimension": radical_dimension,
            "centroid_dimension": centroid_dimension,
            "single_primitive_block_certified": radical_dimension == 0 and centroid_dimension == 1}


def inverse(rows: list[int]) -> list[int]:
    n = len(rows)
    work = [row | (1 << (n + i)) for i, row in enumerate(rows)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if (work[i] >> j) & 1), None)
        if pivot is None:
            raise ValueError("singular")
        work[pivot], work[j] = work[j], work[pivot]
        for i in range(n):
            if i != j and ((work[i] >> j) & 1):
                work[i] ^= work[j]
    return [row >> n for row in work]


def bipartite_sparse_inverse(n: int, rng: random.Random) -> tuple[list[int], list[int]]:
    assert n % 2 == 0
    t = n // 2
    upper = [1 << i for i in range(t)]
    for i in range(t - 1):
        upper[i] |= 1 << (i + 1)
        if i + 3 < t and rng.randrange(2):
            upper[i] |= 1 << (i + 3)
    sparse = [row << t for row in upper]
    sparse += [sum(((upper[i] >> j) & 1) << i for i in range(t)) for j in range(t)]
    raw = inverse(sparse)
    validate_matrix(raw)
    return raw, sparse


def principal_pivot(rows: list[int], chosen: list[int]) -> list[int]:
    """Acquire the graph form after swapping X and Z on the chosen sites."""
    n = len(rows)
    mask = sum(1 << i for i in chosen)
    full = (1 << n) - 1
    xrows = [((1 << i) & (full ^ mask)) | (rows[i] & mask) for i in range(n)]
    zrows = [(rows[i] & (full ^ mask)) | ((1 << i) & mask) for i in range(n)]
    inv_x = inverse(xrows)
    out = [xor_combination(zrows, row) for row in inv_x]
    validate_matrix(out)
    return out


def run_checks() -> dict:
    rng = random.Random(8314729)
    records = []
    prefix_cases = 0
    prefix_budget_cases = 0
    x_prefix_cases = 0
    total_trace_checks = 0
    full_phase_checks = 0
    full_phase_assignments = 0
    # The exact minimum-weight code basis is compared on every small graph.
    for n in range(2, 10):
        for repetition in range(3):
            rows = [0] * n
            for i in range(n):
                for j in range(i):
                    if rng.randrange(2):
                        rows[i] |= 1 << j
                        rows[j] |= 1 << i
            optimal = true_minimum_weight_basis(rows)
            for w in range(min(3, n) + 1):
                cert = acquire(rows, w)
                expected = [v for v in optimal["weights"] if v <= w]
                assert cert["weights"] == expected
                assert cert["total_pauli_support"] + cert["defect"] * (w + 1) <= optimal["weight"]
                prefix_cases += 1
                for budget in (0, 1, n, 2*n, 3*n):
                    budget_cert = acquire(rows, w, budget)
                    expected_budget = []
                    for value in expected:
                        if sum(expected_budget) + value > budget:
                            break
                        expected_budget.append(value)
                    assert budget_cert["weights"] == expected_budget
                    prefix_budget_cases += 1
                if n <= 7:
                    x_choices = sorted((a.bit_count(), a) for a in range(1, 1 << n)
                                       if (a | matvec(rows, a)).bit_count() <= w)
                    for budget in (n, 2*n):
                        truth_basis: dict[int, int] = {}
                        truth_weights = []
                        for weight, a in x_choices:
                            if add_basis(truth_basis, a):
                                if sum(truth_weights) + weight > budget:
                                    break
                                truth_weights.append(weight)
                        xcert = acquire_x_budget(rows, w, budget)
                        assert xcert["x_weights"] == truth_weights
                        x_prefix_cases += 1

    fixtures = []
    # Empty and singular backgrounds, including a genuine dense completion branch.
    fixtures.append(("zero_3", [0, 0, 0], 1))
    fixtures.append(("edge_2", [2, 1], 2))
    fixtures.append(("complete_4_with_y_phases", [15 ^ (1 << i) for i in range(4)], 2))
    fixtures.append(("complete_5_singular", [31 ^ (1 << i) for i in range(5)], 2))
    fixtures.append(("complete_7_singular", [127 ^ (1 << i) for i in range(7)], 2))
    for n in (4, 6, 8, 12, 18):
        rows, witness = bipartite_sparse_inverse(n, rng)
        fixtures.append((f"inverse_sparse_{n}", rows, 3))
    # A partial transform is not necessarily the all-coordinate inverse.
    raw, _ = bipartite_sparse_inverse(10, rng)
    pivot = principal_pivot(raw, [0, 5])
    fixtures.append(("partial_pivot_10", pivot, 4))
    # A random case with no favorable promise still gives an exact representation.
    random_rows = [0] * 8
    for i in range(8):
        for j in range(i):
            if rng.randrange(2):
                random_rows[i] |= 1 << j
                random_rows[j] |= 1 << i
    fixtures.append(("unfavorable_random_8", random_rows, 1))
    for name, rows, w in fixtures:
        n = len(rows)
        foreground = {sum(1 << j for j in range(i, min(i + 3, n)))
                      for i in range(0, n, 3)}
        if n >= 4:
            foreground ^= {1, (1 << (n - 1)) | 2 | 4}
        cert = acquire(rows, w)
        result, detail = count_by_constraint_elimination(rows, foreground, cert)
        expected = direct_count(rows, foreground)
        assert result == expected
        total_trace_checks += detail["valid_trace_identities"]
        direct_phase_numerators = []
        for dense in range(1 << cert["defect"]):
            branch = compile_branch(rows, foreground, cert, dense)
            if branch["variables"] <= 18:
                numerator = exhaustive_phase_sum(branch)
                assert numerator == detail["branches"][dense]["normalized_count"] * (1 << len(branch["updates"]))
                direct_phase_numerators.append(numerator)
                full_phase_checks += 1
                full_phase_assignments += 1 << branch["variables"]
        records.append({"name": name, "raw_matrix": rows,
                        "raw_quadratic_rank": rank(rows),
                        "raw_edges": sum(row.bit_count() for row in rows) // 2,
                        "foreground": sorted(foreground),
                        "certificate": cert, "signed_count": result,
                        "zero_count": ((1 << n) + result) // 2,
                        "validation": detail,
                        "fully_enumerated_phase_numerators": direct_phase_numerators})
    # Robust sparse-inverse cases: the unknown sparse multiplier remains useful
    # even after sparse quadratic corruption makes the raw inverse dense.
    robust_records = []
    for n, support_budget in ((8, 4), (10, 5), (12, 5)):
        raw, hidden_q = bipartite_sparse_inverse(n, rng)
        corruption = [0] * n
        for _ in range(n // 2):
            i, j = rng.sample(range(n), 2)
            corruption[i] ^= 1 << j
            corruption[j] ^= 1 << i
        rows = [a ^ b for a, b in zip(raw, corruption)]
        foreground = {sum(1 << j for j in rng.sample(range(n), 3)) for _ in range(2*n)}
        # Only raw B enters this acquisition. The witness is used afterward to
        # audit the structural theorem, not to guide the search.
        x_budget = sum(row.bit_count() for row in hidden_q)
        cert = acquire_x_budget(rows, support_budget, x_budget)
        count, detail = count_by_constraint_elimination(rows, foreground, cert)
        assert count == direct_count(rows, foreground)
        total_trace_checks += detail["valid_trace_identities"]
        hidden_weights = [(a | matvec(rows, a)).bit_count() for a in hidden_q]
        hidden_short = sum(w <= support_budget for w in hidden_weights)
        assert cert["rank"] >= hidden_short
        cycle_foreground = {sum(1 << ((i+j) % n) for j in range(3)) for i in range(n)}
        cycle_count, cycle_detail = count_by_constraint_elimination(rows, cycle_foreground, cert)
        assert cycle_count == direct_count(rows, cycle_foreground)
        total_trace_checks += cycle_detail["valid_trace_identities"]
        cycle_structure = cubic_structure_sizes(cycle_foreground, n)
        assert cycle_structure["single_primitive_block_certified"]
        robust_records.append({"n": n, "raw_matrix": rows,
                               "corruption_edges": sum(a.bit_count() for a in corruption)//2,
                               "raw_rank": rank(rows),
                               "raw_edges": sum(a.bit_count() for a in rows)//2,
                               "hidden_q": hidden_q,
                               "hidden_joint_weights": hidden_weights,
                               "foreground": sorted(foreground),
                               "foreground_structure": cubic_structure_sizes(foreground, n),
                               "certificate": cert, "signed_count": count,
                               "validation": detail,
                               "cycle_foreground": sorted(cycle_foreground),
                               "cycle_signed_count": cycle_count,
                               "cycle_foreground_structure": cycle_structure,
                               "cycle_validation": cycle_detail})
    cycle_centroid_checks = []
    for n in range(7, 25):
        foreground = {sum(1 << ((i+j) % n) for j in range(3)) for i in range(n)}
        structure = cubic_structure_sizes(foreground, n)
        assert structure["single_primitive_block_certified"]
        cycle_centroid_checks.append({"n": n, **structure})
    rejection_count = 0
    for rows, w in [([1], 1), ([2, 0], 1), ([4, 0], 1), ([0], 2), ([0], -1)]:
        try:
            acquire(rows, w)
        except ValueError:
            rejection_count += 1
        else:
            raise AssertionError("invalid input accepted")
    return {"status": "all exact assertions passed",
            "minimum_weight_prefix_audits": prefix_cases,
            "minimum_weight_budget_prefix_audits": prefix_budget_cases,
            "minimum_x_weight_prefix_audits": x_prefix_cases,
            "raw_matrix_count_cases": len(records),
            "valid_trace_identities": total_trace_checks,
            "fully_enumerated_compiled_phase_cases": full_phase_checks,
            "fully_enumerated_compiled_phase_assignments": full_phase_assignments,
            "malformed_inputs_rejected": rejection_count,
            "asymptotic_phase_engine_executed": False,
            "practical_speed_claim": False,
            "records": records, "robust_sparse_inverse_records": robust_records,
            "cycle_centroid_checks": cycle_centroid_checks}


if __name__ == "__main__":
    result = run_checks()
    path = Path(__file__).with_name("sparse_stabilizer_results.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: value for key, value in result.items()
                      if key not in ("records", "robust_sparse_inverse_records", "cycle_centroid_checks")}, indent=2))
