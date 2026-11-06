#!/usr/bin/env python3
"""Exact finite checks for an UNSOLVED unrestricted SAT research attempt.

This is NOT a polynomial-time SAT algorithm. Enumerative functions deliberately
scan 2**n assignments. Finite tests validate instances and formulas; the proofs
of the parameterized statements are in RESEARCH_NOTE.txt.

No external packages, solvers, services, randomness, or workers are used.
Run: python3 verify.py --out results.json --fixtures fixtures
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
import json
from math import comb
from pathlib import Path


def energy(cnf, bits):
    return sum(not any(bits[abs(lit) - 1] == (lit > 0) for lit in c) for c in cnf)


def assignments(n):
    return product((0, 1), repeat=n)


def histogram(cnf, n, pin=None):
    ans = Counter()
    for bits in assignments(n):
        if pin is None or bits[pin[0]] == pin[1]:
            ans[energy(cnf, bits)] += 1
    return ans


def evaluate_hist(hist, q):
    return sum((count * q**e for e, count in hist.items()), Fraction(0))


def factorial_moments(hist, degree):
    return [sum(count * comb(e, j) for e, count in hist.items() if e >= j)
            for j in range(degree + 1)]


def frac(value):
    value = Fraction(value)
    return {"numerator": value.numerator, "denominator": value.denominator}


def prism_graph(k):
    assert k >= 3
    edges = [(i, (i + 1) % k) for i in range(k)]
    edges += [(k + i, k + (i + 1) % k) for i in range(k)]
    edges += [(i, k + i) for i in range(k)]
    assert len(set(tuple(sorted(e)) for e in edges)) == 3 * k
    scopes = [[] for _ in range(2 * k)]
    for edge_id, (u, v) in enumerate(edges, 1):
        scopes[u].append(edge_id)
        scopes[v].append(edge_id)
    assert all(len(scope) == 3 for scope in scopes)
    return edges, scopes


def xor_clauses(scope, charge):
    """One clause excluding each local assignment of the wrong parity."""
    return [tuple(v if bit == 0 else -v for v, bit in zip(scope, bits))
            for bits in product((0, 1), repeat=len(scope))
            if (sum(bits) & 1) != charge]


def prism_cnf(k, charge, selector=False):
    edges, scopes = prism_graph(k)
    if selector:
        scopes[0] = scopes[0] + [len(edges) + 1]
    cnf = []
    for v, scope in enumerate(scopes):
        cnf.extend(xor_clauses(scope, charge if v == 0 else 0))
    return tuple(cnf), len(edges) + int(selector)


def trap_cnf(k):
    """Variable 1 is s; variable 2 is a; variable i+2 is x_i."""
    assert k >= 1
    return ((1, 2), (1, -2)) + tuple((-1, -(i + 2)) for i in range(1, k + 1)), k + 2


def pad_to_three(cnf, n):
    """For each binary clause C, use (C or z) and (C or not z).

    Exactly preserves violated-clause count for every extension.
    """
    out = []
    for i, c in enumerate(cnf, 1):
        assert len(c) == 2
        z = n + i
        out += [c + (z,), c + (-z,)]
    return tuple(out), n + len(cnf)


def amplified_cnf(cnf, n):
    """Always-satisfiable formula whose s=0 mass encodes SAT of cnf."""
    s, k = n + 1, n + 4
    out = [tuple(c) + (s,) for c in cnf]
    out += [(-s, -(s + i)) for i in range(1, k + 1)]
    return tuple(out), n + k + 1, s, k


def parsimonious_3cnf(cnf, n):
    """Definitional gate encoding; every input has one gate-consistent extension."""
    out, gates = [], []
    size = n

    def gate(op, a=None, b=None):
        nonlocal size
        size += 1
        z = size
        if op == "or":
            out.extend([(-a, z), (-b, z), (a, b, -z)])
        elif op == "and":
            out.extend([(-z, a), (-z, b), (z, -a, -b)])
        elif op == "false":
            out.append((-z,))
        elif op == "true":
            out.append((z,))
        else:
            raise ValueError(op)
        gates.append((op, z, a, b))
        return z

    roots = []
    for c in cnf:
        if not c:
            roots.append(gate("false"))
            continue
        root = c[0]
        for lit in c[1:]:
            root = gate("or", root, lit)
        roots.append(root)
    root = roots[0] if roots else gate("true")
    for item in roots[1:]:
        root = gate("and", root, item)
    out.append((root,))
    return tuple(out), size, gates


def extend_gates(bits, gates):
    values = list(bits)

    def literal(wire):
        x = values[abs(wire) - 1]
        return x if wire > 0 else 1 - x

    for op, z, a, b in gates:
        assert z == len(values) + 1
        value = (literal(a) | literal(b)) if op == "or" else \
            (literal(a) & literal(b)) if op == "and" else int(op == "true")
        values.append(value)
    return tuple(values)


def exact_marginal_by_enumeration(cnf, n, prefix, q):
    """EXPONENTIAL reference computation. It is not a supplied oracle."""
    totals = [Fraction(0), Fraction(0)]
    for suffix in assignments(n - len(prefix)):
        bits = tuple(prefix) + suffix
        totals[suffix[0]] += q ** energy(cnf, bits)
    return totals[1] / sum(totals)


def conditional_round_reference(cnf, n):
    """Checks the rounding lemma using exponentially acquired marginals.

    Push each marginal toward the less likely branch by error 1/8.
    The rational perturbation is adversarial, deterministic, and bounded.
    """
    q = Fraction(1, 1 << (2 * n + 2))
    prefix = []
    for _ in range(n):
        p = exact_marginal_by_enumeration(cnf, n, prefix, q)
        estimate = min(Fraction(1), p + Fraction(1, 8)) if p <= Fraction(1, 2) \
            else max(Fraction(0), p - Fraction(1, 8))
        assert abs(estimate - p) <= Fraction(1, 8)
        chosen = int(estimate >= Fraction(1, 2))
        true_probability = p if chosen else 1 - p
        assert true_probability >= Fraction(3, 8)
        prefix.append(chosen)
    return tuple(prefix) if energy(cnf, tuple(prefix)) == 0 else None


def dimacs(cnf, n, comment):
    return f"c {comment}\np cnf {n} {len(cnf)}\n" + "".join(
        " ".join(map(str, c)) + (" " if c else "") + "0\n" for c in cnf)


def verify_moment_family():
    rows = []
    for k in (3, 4, 5):
        v, e = 2 * k, 3 * k
        records = []
        for charge in (0, 1):
            cnf, n = prism_cnf(k, charge)
            assert n == e and len(cnf) == 4 * v
            hist = histogram(cnf, n)
            expected = {j: (1 << (e - v + 1)) * comb(v, j)
                        for j in range(v + 1) if j % 2 == charge}
            assert dict(hist) == expected
            q = Fraction(1, 1 << (2 * n + 2))
            analytic = (1 << (e - v)) * ((1 + q)**v + (-1)**charge * (1 - q)**v)
            assert evaluate_hist(hist, q) == analytic
            records.append({"charge": charge, "histogram": dict(sorted(hist.items())),
                            "moments": factorial_moments(hist, v)})
        assert records[0]["moments"][:v] == records[1]["moments"][:v]
        assert records[0]["moments"][v] != records[1]["moments"][v]
        rows.append({"k": k, "vertices": v, "variables": e, "clauses": 4 * v,
                     "last_equal_moment_order": v - 1, "records": records})
    return rows


def verify_selector_marginals():
    rows = []
    for k in (3, 4, 5):
        v, e = 2 * k, 3 * k
        n = e + 1
        q = Fraction(1, 1 << (2 * n + 2))
        conditional = []
        probabilities = []
        for charge in (0, 1):
            cnf, actual_n = prism_cnf(k, charge, selector=True)
            assert actual_n == n and len(cnf) == 4 * v + 4
            h0 = histogram(cnf, n, (n - 1, 0))
            h1 = histogram(cnf, n, (n - 1, 1))
            z0, z1 = evaluate_hist(h0, q), evaluate_hist(h1, q)
            p = z1 / (z0 + z1)
            r = (1 - q) / (1 + q)
            analytic = (1 + (-1)**(charge + 1) * r**v) / 2
            assert p == analytic
            probabilities.append(p)
            conditional.append([factorial_moments(h0, v), factorial_moments(h1, v)])
        for s in (0, 1):
            assert conditional[0][s][:v] == conditional[1][s][:v]
            assert conditional[0][s][v] != conditional[1][s][v]
        assert probabilities[1] - probabilities[0] > Fraction(1, 4)
        rows.append({"k": k, "variables": n, "clauses": 4 * v + 4,
                     "last_equal_conditional_moment_order": v - 1,
                     "probability_s1_charge0": frac(probabilities[0]),
                     "probability_s1_charge1": frac(probabilities[1])})
    return rows


def verify_trap_family():
    rows = []
    for k in range(1, 11):
        cnf, n = trap_cnf(k)
        q = Fraction(1, 1 << (2 * n + 2))
        hist = histogram(cnf, n)
        expected = Counter({j: 2 * comb(k, j) for j in range(k + 1)})
        expected[1] += 1 << (k + 1)
        assert hist == expected and hist[0] == 2
        z = evaluate_hist(hist, q)
        assert z == 2 * ((1 + q)**k + (1 << k) * q)
        stationary_a = (1 << (k + 1)) * q / z
        phi = sum((Fraction(comb(k, j)) * q**j / (q + q**j)
                   for j in range(k + 1)), Fraction(0)) / ((k + 2) * (1 << k))
        assert stationary_a <= (1 << k) * q
        assert phi <= Fraction(1, 1 << k)
        if k >= 2:
            t = 1 << (k - 2)
            # Lower bound from the uniform initial distribution.
            tv_lower = Fraction(1, 2) * (1 - t * phi) - stationary_a
            assert tv_lower > Fraction(1, 4)
        else:
            t, tv_lower = 0, Fraction(1, 2) - stationary_a
        rows.append({"k": k, "variables": n, "clauses": len(cnf),
                     "q_exponent": 2 * n + 2,
                     "histogram": dict(sorted(hist.items())),
                     "pi_s0": frac(stationary_a), "exit_flow_per_step": frac(phi),
                     "checked_time_lower_bound": t,
                     "total_variation_lower_bound": frac(tv_lower)})
    padded_checks = []
    for k in (1, 2, 3, 4):
        base, n = trap_cnf(k)
        padded, pn = pad_to_three(base, n)
        expected = {j: count * (1 << len(base)) for j, count in histogram(base, n).items()}
        assert dict(histogram(padded, pn)) == expected
        padded_checks.append({"k": k, "variables": pn, "clauses": len(padded)})
    return rows, padded_checks


def verify_rounding_reduction():
    counts = []
    total = 0
    for n in range(4):
        # All non-tautological clauses on the declared n variables, including empty.
        clauses = [tuple((i + 1) if sign == 1 else -(i + 1)
                         for i, sign in enumerate(signs) if sign)
                   for signs in product((0, 1, -1), repeat=n)]
        checked = 0
        for m in range(min(3, len(clauses)) + 1):
            for cnf in combinations(clauses, m):
                witness = conditional_round_reference(cnf, n)
                truth = any(energy(cnf, bits) == 0 for bits in assignments(n))
                assert (witness is not None) == truth
                if witness is not None:
                    assert energy(cnf, witness) == 0
                hist = histogram(cnf, n)
                q = Fraction(1, 1 << (2 * n + 2))
                z = evaluate_hist(hist, q)
                satisfying_count = hist.get(0, 0)
                assert satisfying_count <= z < satisfying_count + Fraction(1, 2)
                checked += 1
        counts.append({"declared_variables": n, "formulas": checked})
        total += checked
    edge_cases = [(((1, 1), (-1,)), 1), (((1, -1),), 1),
                  (((1,), (1,), (-1,)), 1), (((), (1, -1)), 1)]
    for cnf, n in edge_cases:
        witness = conditional_round_reference(cnf, n)
        truth = any(energy(cnf, bits) == 0 for bits in assignments(n))
        assert (witness is not None) == truth
    return {"exhaustive_groups": counts, "formula_count": total,
            "additional_duplicate_tautology_empty_checks": len(edge_cases),
            "marginal_acquisition": "EXHAUSTIVE, EXPONENTIAL; not a polynomial SAT solver"}


def verify_one_marginal_reduction():
    checks = 0
    for n in range(3):
        clauses = [tuple((i + 1) if sign == 1 else -(i + 1)
                         for i, sign in enumerate(signs) if sign)
                   for signs in product((0, 1, -1), repeat=n)]
        for m in range(min(2, len(clauses)) + 1):
            for cnf in combinations(clauses, m):
                g, ng, s, k = amplified_cnf(cnf, n)
                q = Fraction(1, 1 << (2 * ng + 2))
                zh = evaluate_hist(histogram(cnf, n), q)
                z0 = evaluate_hist(histogram(g, ng, (s - 1, 0)), q)
                z1 = evaluate_hist(histogram(g, ng, (s - 1, 1)), q)
                assert z0 == (1 << k) * zh
                assert z1 == (1 << n) * (1 + q)**k
                truth = any(energy(cnf, bits) == 0 for bits in assignments(n))
                p0 = z0 / (z0 + z1)
                assert p0 >= Fraction(8, 9) if truth else p0 <= Fraction(1, 256)
                known_witness = (0,) * n + (1,) + (0,) * k
                assert energy(g, known_witness) == 0
                checks += 1

    # Local truth tables certify the parsimonious gate interface.
    gate_checks = 0
    for op in ("or", "and"):
        formula = ((-1, 3), (-2, 3), (1, 2, -3)) if op == "or" else \
            ((-3, 1), (-3, 2), (3, -1, -2))
        for a, b, z in assignments(3):
            target = (a | b) if op == "or" else (a & b)
            assert (energy(formula, (a, b, z)) == 0) == (z == target)
            gate_checks += 1

    all_eight = tuple(tuple(v if bit == 0 else -v
                            for v, bit in zip((1, 2, 3), bits))
                      for bits in assignments(3))
    compilation_checks = []
    for cnf in (all_eight, all_eight[:-1]):
        g, ng, s, k = amplified_cnf(cnf, 3)
        encoded, ne, gates = parsimonious_3cnf(g, ng)
        zero_counts = [0, 0]
        for bits in assignments(ng):
            ext = extend_gates(bits, gates)
            assert len(ext) == ne
            assert (energy(encoded, ext) == 0) == (energy(g, bits) == 0)
            if energy(encoded, ext) == 0:
                zero_counts[bits[s - 1]] += 1
        original_count = sum(energy(cnf, bits) == 0 for bits in assignments(3))
        assert zero_counts == [(1 << k) * original_count, 1 << 3]
        compilation_checks.append({"input_variables": 3, "input_clauses": len(cnf),
                                   "original_solutions": original_count,
                                   "compiled_variables": ne, "compiled_clauses": len(encoded),
                                   "maximum_clause_width": max(map(len, encoded)),
                                   "zero_counts_s0_s1": zero_counts,
                                   "input_assignments_checked": 1 << ng})
    return {"exact_partition_identity_instances": checks,
            "local_gate_truth_table_cases": gate_checks,
            "parsimonious_compilation": compilation_checks}


def write_fixtures(destination):
    destination.mkdir(parents=True, exist_ok=True)
    outputs = []
    for charge in (0, 1):
        for selector in (False, True):
            cnf, n = prism_cnf(3, charge, selector)
            name = f"prism_k3_charge{charge}" + ("_selector" if selector else "") + ".cnf"
            (destination / name).write_text(dimacs(cnf, n, name), encoding="utf-8")
            outputs.append({"file": name, "n": n, "clauses": len(cnf),
                            "literal_lists": [list(c) for c in cnf]})
    cnf, n = trap_cnf(6)
    for padded in (False, True):
        f, nn = pad_to_three(cnf, n) if padded else (cnf, n)
        name = "trap_k6" + ("_exact3" if padded else "") + ".cnf"
        (destination / name).write_text(dimacs(f, nn, name), encoding="utf-8")
        outputs.append({"file": name, "n": nn, "clauses": len(f),
                        "literal_lists": [list(c) for c in f]})
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("results.json"))
    parser.add_argument("--fixtures", type=Path, default=Path("fixtures"))
    args = parser.parse_args()
    result = {"status": "PASS", "unrestricted_SAT_resolution": "NOT_OBTAINED",
              "arithmetic": "exact integers and fractions; no floating point",
              "moment_family": verify_moment_family(),
              "selector_marginal_family": verify_selector_marginals()}
    result["trap_family"], result["padded_trap_checks"] = verify_trap_family()
    result["rounding_checks"] = verify_rounding_reduction()
    result["one_marginal_reduction_checks"] = verify_one_marginal_reduction()
    result["fixtures"] = write_fixtures(args.fixtures)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"],
                      "unrestricted_SAT_resolution": result["unrestricted_SAT_resolution"],
                      "moment_pairs": len(result["moment_family"]),
                      "selector_pairs": len(result["selector_marginal_family"]),
                      "trap_instances": len(result["trap_family"]),
                      "exact3_padding_instances": len(result["padded_trap_checks"]),
                      "rounding_formulas": result["rounding_checks"]["formula_count"],
                      "edge_cases": result["rounding_checks"]["additional_duplicate_tautology_empty_checks"]},
                     indent=2))


if __name__ == "__main__":
    main()
