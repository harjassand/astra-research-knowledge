#!/usr/bin/env python3
"""Exact finite checks for the decision-only SAT continuation.

All SAT evaluations in this file enumerate assignments. This is a reference
verifier for small mathematical fixtures, NOT a polynomial-time SAT solver.
Only Python's standard library is used. Run from any directory.
"""

from __future__ import annotations

import json
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def degree(p: int) -> int:
    return p.bit_length() - 1


def pmul(a: int, b: int) -> int:
    out = 0
    while b:
        if b & 1:
            out ^= a
        a <<= 1
        b >>= 1
    return out


def pmod(a: int, modulus: int) -> int:
    d = degree(modulus)
    assert d >= 0
    while degree(a) >= d:
        a ^= modulus << (degree(a) - d)
    return a


def pgcd(a: int, b: int) -> int:
    while b:
        a, b = b, pmod(a, b)
    return a


def ppow(a: int, exponent: int) -> int:
    out = 1
    while exponent:
        if exponent & 1:
            out = pmul(out, a)
        a = pmul(a, a)
        exponent >>= 1
    return out


def fmul(a: int, b: int, modulus: int) -> int:
    return pmod(pmul(a, b), modulus)


def fpow(a: int, exponent: int, modulus: int) -> int:
    out = 1
    while exponent:
        if exponent & 1:
            out = fmul(out, a, modulus)
        a = fmul(a, a, modulus)
        exponent >>= 1
    return out


def irreducible(p: int) -> bool:
    d = degree(p)
    if d < 1:
        return False
    x = pmod(2, p)
    v = x
    for k in range(1, d + 1):
        v = fmul(v, v, p)
        if k <= d // 2 and pgcd(v ^ x, p) != 1:
            return False
    return v == x


def first_irreducible(d: int) -> int:
    for p in range(1 << d, 1 << (d + 1)):
        if irreducible(p):
            return p
    raise AssertionError("No irreducible polynomial found")


def minimal_polynomial(a: int, modulus: int) -> int:
    """Find the first F2 dependence among 1,a,...,a^d."""
    d = degree(modulus)
    basis = {}
    power = 1
    for k in range(d + 1):
        v, relation = power, 1 << k
        while v:
            pivot = degree(v)
            if pivot not in basis:
                basis[pivot] = (v, relation)
                break
            bv, br = basis[pivot]
            v ^= bv
            relation ^= br
        if not v:
            return relation
        power = fmul(power, a, modulus)
    raise AssertionError("Finite-dimensional dependence was not found")


def support(p: int) -> list[int]:
    out = []
    while p:
        low = p & -p
        out.append(degree(low))
        p ^= low
    return out


def evaluate_hasse(p: int, a: int, order: int, modulus: int) -> int:
    # In characteristic 2, binomial(k,r) is odd iff every 1 bit of r is in k.
    out = 0
    for k in support(p):
        if order <= k and order & ~k == 0:
            out ^= fpow(a, k - order, modulus)
    return out


def annihilator(probes: list[dict]) -> int:
    """LCM of the minimal-polynomial powers for full Hasse jets."""
    powers = {}
    for probe in probes:
        mu = minimal_polynomial(probe["point"], probe["modulus"])
        powers[mu] = max(powers.get(mu, 0), probe["jet_length"])
    out = 1
    for mu, multiplicity in sorted(powers.items()):
        out = pmul(out, ppow(mu, multiplicity))
    return out


def support_cnf(p: int, n: int) -> list[list[int]]:
    """Return a CNF on named variables 0,...,n-1 with support exactly p."""
    assert p and degree(p) < (1 << n)
    ell = max(1, degree(p).bit_length())
    assert ell <= n
    clauses = [[-(i + 1)] for i in range(ell, n)]
    for code in range(1 << ell):
        if not (p >> code) & 1:
            clauses.append([-(i + 1) if (code >> i) & 1 else i + 1
                            for i in range(ell)])
    occurring = {abs(lit) for clause in clauses for lit in clause}
    for i in range(1, n + 1):
        if i not in occurring:
            clauses.append([i, -i])
    return clauses


def satisfied(clauses: list[list[int]], code: int) -> bool:
    return all(any(bool((code >> (abs(lit) - 1)) & 1) == (lit > 0)
                   for lit in clause) for clause in clauses)


def brute_support(clauses: list[list[int]], n: int) -> list[int]:
    return [code for code in range(1 << n) if satisfied(clauses, code)]


def reference_value(clauses: list[list[int]], n: int,
                    a: int, modulus: int) -> int:
    """Exponential reference evaluator; no complexity shortcut is claimed."""
    out = 0
    for code in brute_support(clauses, n):
        out ^= fpow(a, code, modulus)
    return out


def witness_from_nonzero(clauses: list[list[int]], n: int,
                         a: int, modulus: int) -> tuple[int, int] | None:
    current = [clause[:] for clause in clauses]
    value = reference_value(current, n, a, modulus)
    calls = 1
    if value == 0:
        return None
    code = 0
    for i in range(n):
        value_zero = reference_value(current + [[-(i + 1)]], n, a, modulus)
        calls += 1
        if value_zero:
            current.append([-(i + 1)])
            value = value_zero
        else:
            current.append([i + 1])
            code |= 1 << i
            # Parent = zero child + one child, so the one child retains value.
        assert value != 0
    assert satisfied(clauses, code)
    assert reference_value(current, n, a, modulus) == value
    return code, calls


def gf2_rank(columns: list[int]) -> int:
    basis = {}
    for v in columns:
        while v:
            pivot = degree(v)
            if pivot not in basis:
                basis[pivot] = v
                break
            v ^= basis[pivot]
    return len(basis)


def observation_rank(probes: list[dict], monomial_count: int) -> int:
    columns = []
    for k in range(monomial_count):
        packed = 0
        offset = 0
        for probe in probes:
            d = degree(probe["modulus"])
            for order in range(probe["jet_length"]):
                value = evaluate_hasse(1 << k, probe["point"], order,
                                       probe["modulus"])
                packed |= value << offset
                offset += d
        columns.append(packed)
    return gf2_rank(columns)


def universal_two_witness_cnf(d: int, h: int) -> tuple[int, list[list[int]], int]:
    n = d + h + 1
    lo, hi = h, d + h
    clauses = [[-(i + 1)] for i in range(n) if i not in (lo, hi)]
    clauses += [[lo + 1, hi + 1], [-(lo + 1), -(hi + 1)]]
    p = (1 << (1 << lo)) | (1 << (1 << hi))
    return n, clauses, p


def dimacs(n: int, clauses: list[list[int]]) -> str:
    return f"p cnf {n} {len(clauses)}\n" + "".join(
        " ".join(map(str, clause)) + " 0\n" for clause in clauses)


class LiftRing:
    """(Z/2^p)[u]/g(u), with a literal 0/1 monic lift of g."""

    def __init__(self, polynomial: int, precision: int):
        self.g = polynomial
        self.d = degree(polynomial)
        self.modulus = 1 << precision
        self.zero = (0,) * self.d
        self.one = (1,) + (0,) * (self.d - 1)

    def integer(self, value: int) -> tuple[int, ...]:
        return (value % self.modulus,) + (0,) * (self.d - 1)

    def lift(self, a: int) -> tuple[int, ...]:
        return tuple((a >> i) & 1 for i in range(self.d))

    def add(self, a: tuple, b: tuple) -> tuple:
        return tuple((x + y) % self.modulus for x, y in zip(a, b))

    def mul(self, a: tuple, b: tuple) -> tuple:
        tmp = [0] * (2 * self.d - 1)
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                tmp[i + j] += x * y
        for k in range(len(tmp) - 1, self.d - 1, -1):
            lead = tmp[k]
            for j in range(self.d):
                if (self.g >> j) & 1:
                    tmp[k - self.d + j] -= lead
        return tuple(x % self.modulus for x in tmp[:self.d])

    def pow(self, a: tuple, exponent: int) -> tuple:
        out = self.one
        while exponent:
            if exponent & 1:
                out = self.mul(out, a)
            a = self.mul(a, a)
            exponent >>= 1
        return out

    def mod_two(self, a: tuple) -> int:
        return sum((x & 1) << i for i, x in enumerate(a))


def run() -> dict:
    rng = random.Random(20261106)
    fields = {d: first_irreducible(d) for d in range(1, 7)}
    results = {"arithmetic": "exact integers and explicit polynomial bases",
               "reference_evaluator": "exhaustive; exponential in n",
               "checks": {}}
    count = 0
    for d, modulus in fields.items():
        for a in range(1 << d):
            mu = minimal_polynomial(a, modulus)
            assert 1 <= degree(mu) <= d
            assert irreducible(mu)
            assert evaluate_hasse(mu, a, 0, modulus) == 0
            assert evaluate_hasse(mu, a, 1, modulus) != 0
            count += 1
    results["checks"]["minimal_polynomials"] = count

    fixed_probes = [
        {"modulus": 3, "point": 0, "jet_length": 1},
        {"modulus": 3, "point": 1, "jet_length": 1},
        {"modulus": 7, "point": 2, "jet_length": 1},
        {"modulus": 11, "point": 2, "jet_length": 1},
    ]
    q = annihilator(fixed_probes)
    assert support(q) == [1, 2, 5, 7]
    clauses = support_cnf(q, 3)
    (ROOT / "fixtures" / "four_point_failure.cnf").write_text(dimacs(3, clauses))
    fixtures = [{"id": "four_point_failure", "n": 3,
                 "clauses": clauses, "probes": fixed_probes,
                 "support": support(q), "known_witness_code": degree(q),
                 "polynomial_exponents": support(q)}]

    constructions = 0
    for case in range(50):
        probes = []
        for _ in range(rng.randint(1, 6)):
            d = rng.randint(1, 5)
            probes.append({"modulus": fields[d],
                           "point": rng.randrange(1 << d),
                           "jet_length": rng.randint(1, 4)})
        poly = annihilator(probes)
        n = degree(poly).bit_length() + rng.randrange(3)
        cnf = support_cnf(poly, n)
        assert brute_support(cnf, n) == support(poly)
        assert satisfied(cnf, degree(poly))
        for probe in probes:
            for order in range(probe["jet_length"]):
                assert evaluate_hasse(poly, probe["point"], order,
                                      probe["modulus"]) == 0
        constructions += 1
        if case < 4:
            fixtures.append({"id": f"annihilator_{case}", "n": n,
                             "clauses": cnf, "probes": probes,
                             "support": support(poly),
                             "known_witness_code": degree(poly)})
    results["checks"]["compact_CNF_annihilators"] = constructions + 1

    ranks = []
    for _ in range(80):
        probes = []
        for _ in range(rng.randint(1, 5)):
            d = rng.randint(1, 4)
            probes.append({"modulus": fields[d],
                           "point": rng.randrange(1 << d),
                           "jet_length": rng.randint(1, 3)})
        monomials = 1 << rng.randint(1, 4)
        actual = observation_rank(probes, monomials)
        predicted = min(monomials, degree(annihilator(probes)))
        assert actual == predicted
        ranks.append({"monomials": monomials, "annihilator_degree":
                      degree(annihilator(probes)), "rank": actual})
    # Two distinct Frobenius conjugates provide redundant value constraints.
    conjugate_probes = [{"modulus": 7, "point": a, "jet_length": 1}
                        for a in (2, 3)]
    assert degree(annihilator(conjugate_probes)) == 2
    assert observation_rank(conjugate_probes, 8) == 2
    results["checks"]["joint_jet_exact_rank"] = len(ranks) + 1

    universal = []
    for d in range(1, 7):
        for h in range(5):
            n, cnf, poly = universal_two_witness_cnf(d, h)
            assert brute_support(cnf, n) == [1 << h, 1 << (d + h)]
            for a in range(1 << d):
                for order in range(1 << h):
                    assert evaluate_hasse(poly, a, order, fields[d]) == 0
                assert evaluate_hasse(poly, a, 1 << h, fields[d]) == 1
            universal.append({"d": d, "h": h, "n": n,
                              "field_modulus": fields[d],
                              "all_points_tested": 1 << d,
                              "jet_length": 1 << h,
                              "witnesses": [1 << h, 1 << (d + h)]})
    results["checks"]["universal_two_witness_families"] = len(universal)
    n, cnf, _ = universal_two_witness_cnf(4, 3)
    (ROOT / "fixtures" / "all_F16_eight_jets_failure.cnf").write_text(dimacs(n, cnf))

    successes, zero_values = 0, 0
    for _ in range(150):
        n = rng.randint(1, 8)
        cnf = []
        for _ in range(rng.randint(0, 4 * n)):
            width = rng.randint(1, min(n, 4))
            indices = rng.sample(range(1, n + 1), width)
            cnf.append([i if rng.randrange(2) else -i for i in indices])
        occurring = {abs(lit) for clause in cnf for lit in clause}
        cnf += [[i, -i] for i in range(1, n + 1) if i not in occurring]
        d = rng.randint(1, 5)
        a = rng.randrange(1 << d)
        found = witness_from_nonzero(cnf, n, a, fields[d])
        if found is None:
            zero_values += 1
        else:
            witness, calls = found
            assert satisfied(cnf, witness)
            assert calls == n + 1
            successes += 1
    results["checks"]["nonzero_value_to_witness"] = {
        "trials": 150, "nonzero_values_with_verified_witness": successes,
        "zero_values_no_UNSAT_claim": zero_values}

    lifted_checks = []
    for d in range(1, 6):
        for m in range(1, 5):
            e = 2 * m
            ring = LiftRing(fields[d], e + 1)
            a = (1 << d) - 1
            alpha = ring.lift(a)
            # A nonzero monomial (a unique witness) tests the sharp precision.
            exponent = 1 + d + m
            value = ring.pow(alpha, exponent)
            assert ring.mod_two(value) == fpow(a, exponent, fields[d]) != 0
            weak = ring.mul(ring.integer(1 << e), value)
            assert all(c % (1 << e) == 0 for c in weak)
            recovered = sum(((c >> e) & 1) << i for i, c in enumerate(weak))
            assert recovered == ring.mod_two(value)
            assert weak != ring.zero
            lifted_checks.append({"field_degree": d, "original_wires": m,
                                  "weak_wires": e,
                                  "precision_for_this_embedding": e + 1,
                                  "surviving_modes": 1 << e,
                                  "characteristic_two_value": recovered})
    results["checks"]["weak_wire_one_bit_precision"] = len(lifted_checks)

    results["four_point_fixture"] = fixtures[0]
    results["joint_jet_rank_examples"] = ranks[:8]
    results["universal_two_witness_instances"] = universal
    results["weak_wire_precision_instances"] = lifted_checks
    results["status"] = "PASS: finite exact checks; unrestricted SAT unresolved"
    (ROOT / "FIXTURES.json").write_text(json.dumps(fixtures, indent=2) + "\n")
    (ROOT / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({"checks": results["checks"], "status": results["status"]},
                     indent=2))
    return results


if __name__ == "__main__":
    run()
