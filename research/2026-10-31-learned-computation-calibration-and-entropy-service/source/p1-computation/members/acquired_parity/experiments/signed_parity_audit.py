#!/usr/bin/env python3
"""Independent small audit of signed Pfaffians and physical-parity projection.

Does not modify the production nonnegative-factor implementation. The dummy
positive Fisher construction supplies topology; signed external weights and
prefactors are inserted separately and checked against direct x enumeration.
"""
from fractions import Fraction as Q
from math import comb, prod
from random import Random
import json
import graphic_acquisition as g


def represent(target, vectors):
    base = {}
    for j, a in enumerate(vectors):
        x, tag = a, 1 << j
        while x:
            p = x.bit_length() - 1
            if p in base:
                y, t = base[p]
                x ^= y
                tag ^= t
            else:
                base[p] = x, tag
                break
    tag = 0
    while target:
        p = target.bit_length() - 1
        if p not in base:
            return None
        x, t = base[p]
        target ^= x
        tag ^= t
    return tag


def xor_selected(vectors, mask):
    value = 0
    for i in g.bit_members(mask):
        value ^= vectors[i]
    return value


class SignedAuditKernel:
    def __init__(self, graph, embedding):
        self.graph, self.embedding = graph, embedding
        self.calls = 0
        self.negative_prefactors = 0
        self.interpolation_cases = 0
        self.max_q = 0

    def regular(self, weights):
        graph, embedding = self.graph, self.embedding
        n, ew, faces, pre, matching = g.fisher_cubic(
            graph, embedding, [(Q(1), Q(1))] * len(weights))
        for e, (u, v) in enumerate(graph["edges"]):
            w0, w1 = weights[e]
            a, b = (w0 + w1) / 2, (w0 - w1) / 2
            assert a
            pu = 4 * u + 1 + embedding["rotation"][u].index(v)
            pv = 4 * v + 1 + embedding["rotation"][v].index(u)
            ew[tuple(sorted((pu, pv)))] = b / a
            pre *= a
        mat, orientation = g.kasteleyn_matrix(n, ew, faces)
        self.calls += 1
        self.negative_prefactors += int(pre < 0)
        return pre * g.matching_orientation_sign(matching, orientation) * g.pfaffian(mat) / 2

    def signed(self, weights):
        if any(w0 == w1 == 0 for w0, w1 in weights):
            return Q(0)
        zeros = [e for e, (w0, w1) in enumerate(weights) if w0 + w1 == 0]
        q = len(zeros)
        self.max_q = max(self.max_q, q)
        if not q:
            return self.regular(weights)
        self.interpolation_cases += 1
        result = Q(0)
        for j in range(1, q + 2):
            modified = list(weights)
            for e in zeros:
                w0, w1 = modified[e]
                modified[e] = w0 + j, w1 + j
            result += (-1) ** (j - 1) * comb(q + 1, j) * self.regular(modified)
        return result


def run():
    nv, edges = g.cube_fixture()
    original_rows = g.hidden_matrix(nv, edges, 904)
    s, n, rng = len(edges), 9, Random(710)
    lifts = []
    while len(lifts) < len(original_rows):
        a = rng.randrange(1, 1 << n)
        if len(g.basis(lifts + [a])) > len(lifts):
            lifts.append(a)
    masks = [xor_selected(lifts, col) for col in g.columns(original_rows, s)]
    acquired_rows = [sum(((a >> i) & 1) << e for e, a in enumerate(masks))
                     for i in range(n)]
    graph = g.acquire_graph(acquired_rows, s, 3)
    dual = g.acquire_graph(g.nullspace(acquired_rows, s), s, 4)
    embedding = g.acquire_sphere_embedding(graph, dual)
    assert embedding is not None
    kernel = SignedAuditKernel(graph, embedding)
    weights = [(Q(e + 2, 3), Q(e + 2, 3)) if e % 3 == 0
               else (Q(e % 2 + 2, 3), Q(e % 5 + 1, 2)) for e in range(s)]
    rank_a = len(g.basis(masks))
    fiber = 1 << (n - rank_a)
    physical_values = [prod(weights[e][(a & x).bit_count() & 1]
                            for e, a in enumerate(masks)) for x in range(1 << n)]
    cache = {}

    def twist(c):
        if c in cache:
            return cache[c]
        lam = represent(c, masks)
        if lam is None:
            answer = Q(0)
        else:
            signed = [(w0, -w1 if (lam >> e) & 1 else w1)
                      for e, (w0, w1) in enumerate(weights)]
            answer = fiber * kernel.signed(signed)
        direct = sum((-w if (c & x).bit_count() & 1 else w)
                     for x, w in enumerate(physical_values))
        assert answer == direct
        cache[c] = answer
        return answer

    # Include lambdas supported on equal pairs, and terms producing negative a.
    lam_masks = [0, 1, 3, 5, 17, 33, 65, 0b1001001001, (1 << s) - 1]
    queries = [xor_selected(masks, lam) for lam in lam_masks]
    outside = next(c for c in range(1, 1 << n) if represent(c, masks) is None)
    queries.append(outside)
    for c in queries:
        twist(c)

    # Force the interpolation boundary directly, including q=12 and Q=0.
    all_equal = [(Q(1), Q(-1)) for _ in range(s)]
    assert kernel.signed(all_equal) == g.brute_cut_partition(acquired_rows, s, all_equal)
    assert kernel.signed([(Q(0), Q(0))] + weights[1:]) == 0

    evidence = [masks[0], masks[1], outside]
    k, z = len(evidence), 0b101
    t = rank_a + len(g.basis(evidence)) - len(g.basis(masks + evidence))
    mass, mass_terms = Q(0), 0
    for u in range(1 << k):
        c = xor_selected(evidence, u)
        if represent(c, masks) is not None:
            mass_terms += 1
            mass += (-1 if (u & z).bit_count() & 1 else 1) * twist(c)
    mass /= 1 << k
    direct_mass = sum(w for x, w in enumerate(physical_values)
                      if all(((c & x).bit_count() & 1) == ((z >> j) & 1)
                             for j, c in enumerate(evidence)))
    assert mass == direct_mass and mass > 0 and mass_terms == 1 << t

    conditional_queries = [masks[2] ^ outside]
    outside_both = next((c for c in range(1, 1 << n)
                        if represent(c, masks + evidence) is None), None)
    if outside_both is not None:
        conditional_queries.append(outside_both)
    for c in conditional_queries:
        numerator, terms = Q(0), 0
        for u in range(1 << k):
            target = c ^ xor_selected(evidence, u)
            if represent(target, masks) is not None:
                terms += 1
                numerator += (-1 if (u & z).bit_count() & 1 else 1) * twist(target)
        numerator /= 1 << k
        direct = sum((-w if (c & x).bit_count() & 1 else w)
                     for x, w in enumerate(physical_values)
                     if all(((row & x).bit_count() & 1) == ((z >> j) & 1)
                            for j, row in enumerate(evidence)))
        assert numerator == direct and terms in (0, 1 << t)
    return {"physical_bits": n, "features": s, "rank_A": rank_a,
            "physical_states_directly_enumerated": 1 << n,
            "distinct_physical_twists_verified": len(cache),
            "pfaffian_calls": kernel.calls,
            "negative_prefactor_calls": kernel.negative_prefactors,
            "interpolation_cases": kernel.interpolation_cases,
            "maximum_zero_a_edges": kernel.max_q,
            "evidence_rank": k, "overlap_dimension": t,
            "nonzero_possible_projection_terms": mass_terms,
            "evidence_mass": str(mass), "verified": True}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
