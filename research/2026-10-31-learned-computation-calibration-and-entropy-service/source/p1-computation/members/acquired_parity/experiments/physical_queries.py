#!/usr/bin/env python3
"""Physical parity evidence via its acquired overlap with the feature space.

The conventional signed partition executor is reused.  The compiler computes
all contributing Fourier twists and an actual joint fiber lift. No rejection
from a rare evidence event is used by the conditional sampler.
"""
from __future__ import annotations

from fractions import Fraction as Q
from pathlib import Path
import json
import random
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from learn_planar import (ga, ScalarOracle, acquire_certified, basis, parity,
                         GF2System, BitSource, lincomb, RetainedPfaffian,
                         RetainedElimination, clamp)
try:
    from parity_acquisition import basis_and_relations, span
except ImportError:
    from next_independent.parity_acquisition import basis_and_relations, span


class PhysicalEvidence:
    def __init__(self, n, A, weights, engine, C=None, z=0, twist_budget=65536):
        self.n, self.A, self.weights, self.engine = n, tuple(A), tuple(tuple(w) for w in weights), engine
        self.C, self.z = tuple(C or []), z
        self.A_system = GF2System(A, n)
        self.C_system = GF2System(self.C, n)
        self.C_system.particular(z)  # reject inconsistent or malformed evidence
        self.reduced_C = self.C_system.rref_rows
        self.reduced_z = sum(parity(t & z) << i for i, t in enumerate(self.C_system.transforms))
        self.q = self.C_system.rank
        self.joint = GF2System(list(A) + list(self.C), n)
        self.t = self.A_system.rank + self.q - self.joint.rank
        K = [sum(((a >> i) & 1) << e for e, a in enumerate(A)) for i in range(n)]
        self.coefficients = GF2System(K, len(A))
        all_rows = list(A) + self.reduced_C
        augmented = [sum(((a >> i) & 1) << e for e, a in enumerate(all_rows)) for i in range(n)]
        self.augmented_coefficients = GF2System(augmented, len(all_rows))
        _, relations = basis_and_relations(list(A) + self.reduced_C)
        self.overlap_basis = basis([r >> len(A) for r in relations])
        assert len(self.overlap_basis) == self.t
        if (1 << self.t) > twist_budget:
            raise ValueError("Declared signed-query budget exceeded")
        self.twists = []
        for u in span(self.overlap_basis):
            c = lincomb(self.reduced_C, u)
            lam = self.coefficients.particular(c)
            sign = -1 if parity(u & self.reduced_z) else 1
            self.twists.append((lam, sign))
        self.kernel_calls = 0

    def partition(self, feature_evidence=None):
        """At most 2^t signed code sums for arbitrary consistent Cx=z."""
        factors = clamp(self.weights, feature_evidence or {})
        total = Q(0)
        for lam, sign in self.twists:
            twisted = [(w[0], -w[1]) if (lam >> e) & 1 else w
                       for e, w in enumerate(factors)]
            total += sign * self.engine.signed_partition(twisted)
            self.kernel_calls += 1
        answer = total * Q(1 << (self.n - self.A_system.rank), 1 << self.q)
        assert answer >= 0
        return answer

    def parity_numerator(self, c, feature_evidence=None):
        """Sum W(x)(-1)^(c.x) under Cx=z, using an affine overlap coset."""
        try:
            solution = self.augmented_coefficients.particular(c)
        except ValueError:
            if c < 0 or c >= (1 << self.n):
                raise
            return Q(0)
        u0 = solution >> len(self.A)
        factors = clamp(self.weights, feature_evidence or {})
        total = Q(0)
        for v in span(self.overlap_basis):
            u = u0 ^ v
            mask = c ^ lincomb(self.reduced_C, u)
            lam = self.coefficients.particular(mask)
            twisted = [(w[0], -w[1]) if (lam >> e) & 1 else w for e, w in enumerate(factors)]
            total += (-1 if parity(u & self.reduced_z) else 1) * self.engine.signed_partition(twisted)
            self.kernel_calls += 1
        return total * Q(1 << (self.n - self.A_system.rank), 1 << self.q)

    def sample(self, bits, feature_evidence=None):
        """O((s+1)2^t) signed sums, then uniform joint affine-fiber lift."""
        fixed = dict(feature_evidence or {})
        current = self.partition(fixed)
        if not current:
            raise ValueError("The joint evidence has zero mass")
        y = sum(b << e for e, b in fixed.items())
        for e in range(len(self.A)):
            if e in fixed:
                continue
            fixed[e] = 0
            z0 = self.partition(fixed)
            p0 = z0 / current
            if bits.randbelow(p0.denominator) < p0.numerator:
                current = z0
            else:
                fixed[e] = 1
                y |= 1 << e
                current -= z0
        rhs = y | (self.z << len(self.A))
        x0 = self.joint.particular(rhs)
        return x0 ^ lincomb(self.joint.kernel, bits.getrandbits(len(self.joint.kernel)))


def brute(n, A, weights, C, z, feature_evidence=None):
    fixed = feature_evidence or {}
    total = Q(0)
    law = {}
    for x in range(1 << n):
        if any(parity(c & x) != ((z >> j) & 1) for j, c in enumerate(C)):
            continue
        if any(parity(A[e] & x) != b for e, b in fixed.items()):
            continue
        value = 1
        for a, w in zip(A, weights):
            value *= w[parity(a & x)]
        law[x] = value
        total += value
    return total, {x: Q(w, total) for x, w in law.items()} if total else {}


def exact_sampler_law(query, feature_evidence=None):
    """Enumerate branch probabilities for a tiny instance, including joint lift."""
    initial = dict(feature_evidence or {})
    start = query.partition(initial)
    if not start:
        return {}
    output = {}
    def visit(e, fixed, probability, mass):
        if e == len(query.A):
            y = sum(b << j for j, b in fixed.items())
            x0 = query.joint.particular(y | (query.z << len(query.A)))
            kernel = query.joint.kernel
            for mask in range(1 << len(kernel)):
                x = x0 ^ lincomb(kernel, mask)
                output[x] = output.get(x, Q(0)) + probability / (1 << len(kernel))
            return
        if e in fixed:
            visit(e + 1, fixed, probability, mass)
            return
        both = dict(fixed)
        both[e] = 0
        z0 = query.partition(both)
        if z0:
            visit(e + 1, both, probability * z0 / mass, z0)
        if mass - z0:
            both = dict(fixed)
            both[e] = 1
            visit(e + 1, both, probability * (mass-z0) / mass, mass-z0)
    visit(0, initial, Q(1), start)
    return output


def run():
    rng = random.Random(310311)
    nv, edges = ga.cube_fixture()
    K = ga.hidden_matrix(nv, edges, 3838)
    n = len(K)
    hidden = ga.columns(K, len(edges))
    coefs = [rng.choice([-2, -1, 1, 2]) for _ in hidden]
    learned = acquire_certified(n, len(hidden) + 1, .01,
                               ScalarOracle(n, hidden, coefs, 1), random.Random(43))
    assert learned["success"] and set(learned["support"]) == set(hidden)
    A = learned["support"]
    K = [sum(((a >> i) & 1) << e for e, a in enumerate(A)) for i in range(n)]
    G = ga.acquire_graph(K, len(A), 3)
    D = ga.acquire_graph(ga.nullspace(K, len(A)), len(A), 4)
    rotation = ga.acquire_sphere_embedding(G, D)
    pf, ve = RetainedPfaffian(G, rotation), RetainedElimination(G)
    # Equal pairs deliberately force zero-sum signed factors, exercising the
    # interpolation branch rather than assuming away its singularity.
    weights = [(3, 3) if e % 3 == 0 else (rng.randrange(1, 7), rng.randrange(1, 7))
               for e in range(len(A))]
    single_readouts, joint_cases = 0, 0
    for c in [1 << i for i in range(n)] + [rng.randrange(1, 1 << n) for _ in range(9)]:
        for z in (0, 1):
            query = PhysicalEvidence(n, A, weights, pf, [c], z)
            answer = query.partition()
            direct, _ = brute(n, A, weights, [c], z)
            assert answer == direct
            single_readouts += 1
    for _ in range(6):
        C = []
        while len(C) < 3:
            c = rng.randrange(1, 1 << n)
            if len(basis(C + [c])) > len(C):
                C.append(c)
        z = rng.randrange(8)
        qp, qv = PhysicalEvidence(n, A, weights, pf, C, z), PhysicalEvidence(n, A, weights, ve, C, z)
        direct, _ = brute(n, A, weights, C, z)
        assert qp.partition() == qv.partition() == direct
        joint_cases += 1
    C, z = [1, 2], 1
    query = PhysicalEvidence(n, A, weights, ve, C, z)
    direct_mass, direct_law = brute(n, A, weights, C, z)
    assert exact_sampler_law(query) == direct_law
    for c in range(1 << n):
        exact = sum(prob * (-1 if parity(c & x) else 1) for x, prob in direct_law.items())
        assert query.parity_numerator(c) == exact * direct_mass
    bits = BitSource(730)
    for _ in range(20):
        x = query.sample(bits)
        assert all(parity(c & x) == ((z >> j) & 1) for j, c in enumerate(C))
    # Larger test reuses the actually acquired masks from the main experiment.
    previous = json.loads((HERE.parent / "results" / "learned_planar.json").read_text())
    large_A, large_n = previous["retained_support"], previous["n"]
    large_K = [sum(((a >> i) & 1) << e for e, a in enumerate(large_A)) for i in range(large_n)]
    large_G = ga.acquire_graph(large_K, len(large_A), 3)
    large_engine = RetainedElimination(large_G)
    base = basis(large_A)
    outside, working = [], list(base)
    while len(outside) < 6:
        c = rng.getrandbits(large_n)
        if len(basis(working + [c])) > len(working):
            outside.append(c)
            working.append(c)
    inside = [base[0] ^ base[1], base[2] ^ base[3]]
    C = outside + inside
    witness = rng.getrandbits(large_n)
    z = sum(parity(c & witness) << j for j, c in enumerate(C))
    large_weights = [(rng.randrange(1, 9), rng.randrange(1, 9)) for _ in large_A]
    large = PhysicalEvidence(large_n, large_A, large_weights, large_engine, C, z)
    assert large.q == 8 and large.t == 2 and len(large.twists) == 4
    start = time.perf_counter()
    mass = large.partition()
    seconds = time.perf_counter() - start
    # Check against the simpler 2^q Fourier expansion on the SAME retained
    # graph; zero outside-fiber characters are independently skipped by solve.
    full = Q(0)
    full_nonzero = 0
    for u in range(1 << large.q):
        c = lincomb(large.reduced_C, u)
        try:
            lam = large.coefficients.particular(c)
        except ValueError:
            continue
        full_nonzero += 1
        twisted = [(w[0], -w[1]) if (lam >> e) & 1 else w for e, w in enumerate(large.weights)]
        full += (-1 if parity(u & large.reduced_z) else 1) * large_engine.signed_partition(twisted)
    full *= Q(1 << (large_n - large.A_system.rank), 1 << large.q)
    assert full == mass and full_nonzero == 4
    large_bits = BitSource(929)
    before = large.kernel_calls
    start = time.perf_counter()
    for _ in range(4):
        x = large.sample(large_bits)
        assert all(parity(c & x) == ((z >> j) & 1) for j, c in enumerate(C))
    large_sample_seconds = time.perf_counter() - start
    result = {"small_acquisition_queries": learned["query_count"], "small_n": n,
              "exact_physical_single_parity_event_checks": single_readouts,
              "exact_three_parity_joint_evidence_checks": joint_cases,
              "complete_conditional_sampler_law_checked": True,
              "exact_conditional_physical_parity_numerators_checked": 1 << n,
              "signed_pfaffian_requests": pf.signed_requests,
              "actual_pfaffian_eliminations": pf.calls,
              "interpolation_eliminations": pf.interpolation_evaluations,
              "small_conditional_samples": 20,
              "large_n": large_n, "large_features": len(large_A),
              "large_rank_A": large.A_system.rank, "large_evidence_rank": large.q,
              "large_overlap_rank": large.t, "twists_per_partition": len(large.twists),
              "full_evidence_Fourier_terms_without_overlap_reduction": 1 << large.q,
              "large_partition_bits": {"numerator": mass.numerator.bit_length(),
                                       "denominator": mass.denominator.bit_length()},
              "large_partition_seconds": seconds,
              "large_conditional_samples": 4,
              "large_sample_signed_kernel_calls": large.kernel_calls - before,
              "large_sample_seconds": large_sample_seconds,
              "large_sample_random_bits": large_bits.bits_used,
              "new_energy_queries_for_large_extension": 0,
              "scope": "The physical-evidence theorem is fixed-parameter in overlap rank t, with no unrestricted polynomial guarantee."}
    (HERE.parent / "results" / "physical_queries.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    run()
