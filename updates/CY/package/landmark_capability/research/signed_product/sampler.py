"""Exact rational positive-part sampling from an acquired signed product law.

This does not certify how the input mixture was acquired.  Given rational
coefficients/factors, it exactly samples the normalized positive part of the
augmented law.  Exactness is conditional on a fair randbelow primitive;
the executable demonstration uses a seeded pseudorandom generator.
"""
from __future__ import annotations

from bisect import bisect_right
from fractions import Fraction as F
from math import lcm
import random


class SignedProductSampler:
    def __init__(self, components, *, randbelow=None):
        self.components = [(F(c), tuple(map(F, p))) for c, p in components if c]
        if not self.components:
            raise ValueError("At least one nonzero component is required")
        self.n = len(self.components[0][1])
        if any(len(p) != self.n or any(q < 0 or q > 1 for q in p)
               for _, p in self.components):
            raise ValueError("All factors must be probability vectors of equal length")
        self.dead = 1 - sum(c for c, _ in self.components)
        weights = [abs(c) for c, _ in self.components] + [abs(self.dead)]
        denominator = lcm(*(x.denominator for x in weights))
        tickets = [x.numerator * (denominator // x.denominator) for x in weights]
        running = 0
        self.cumulative = []
        for ticket in tickets:
            running += ticket
            self.cumulative.append(running)
        self.total_tickets = running
        self.absolute_mass = sum(weights)
        self.randbelow = randbelow or random.SystemRandom().randrange
        self.attempts = 0

    def bernoulli(self, p):
        return self.randbelow(p.denominator) < p.numerator

    def point(self, x):
        """Return signed mass and absolute-mixture mass at x; None means dead."""
        if x is None:
            return self.dead, abs(self.dead)
        signed = F(0)
        absolute = F(0)
        for c, p in self.components:
            mass = F(1)
            for i, q in enumerate(p):
                mass *= q if (x >> i) & 1 else 1 - q
            signed += c * mass
            absolute += abs(c) * mass
        return signed, absolute

    def draw(self):
        while True:
            self.attempts += 1
            index = bisect_right(self.cumulative, self.randbelow(self.total_tickets))
            if index == len(self.components):
                x = None
            else:
                x = sum(int(self.bernoulli(q)) << i
                        for i, q in enumerate(self.components[index][1]))
            signed, absolute = self.point(x)
            if signed > 0 and self.bernoulli(signed / absolute):
                return x

    def draw_alive_prefix(self):
        """Sample by positive child-prefix masses, with no rejection loop.

        If the signed law is eta-close in L1 to a positive alive law of mass
        s, the output is at most n*eta/s away in TV from that law conditioned
        on survival.  This is generally NOT the global positive-part law.
        """
        weights = [c for c, _ in self.components]
        x = 0
        for i in range(self.n):
            one = sum(w * p[i] for w, (_, p) in zip(weights, self.components))
            zero = sum(weights) - one
            positive_one, positive_zero = max(one, 0), max(zero, 0)
            total = positive_one + positive_zero
            bit = self.bernoulli(positive_one / total if total else F(1, 2))
            x |= int(bit) << i
            weights = [w * (p[i] if bit else 1 - p[i])
                       for w, (_, p) in zip(weights, self.components)]
        return x


def prefix_law_dense(sampler):
    """Small-instance verification only; draw_alive_prefix never enumerates."""
    law = {0: F(1)}
    for i in range(sampler.n):
        out = {}
        for prefix, probability in law.items():
            signed = [F(0), F(0)]
            for c, p in sampler.components:
                w = c
                for j in range(i):
                    w *= p[j] if (prefix >> j) & 1 else 1 - p[j]
                signed[0] += w * (1 - p[i])
                signed[1] += w * p[i]
            positive = [max(v, 0) for v in signed]
            total = sum(positive)
            for bit in (0, 1):
                conditional = positive[bit] / total if total else F(1, 2)
                out[prefix | (bit << i)] = probability * conditional
        law = out
    return law


def demonstration():
    import json
    from pathlib import Path
    # A deliberately signed, slightly nonpositive approximation.  The sampler
    # must clamp by the total point mass, not discard negative components.
    cases = [
        [(F(1), (F(1, 2),) * 4), (F(-1, 16), (F(1),) * 4)],
        [(F(1), (F(1, 2),) * 4), (F(-1, 8), (F(1),) * 4)],
        [(F(3, 4), (F(1, 3), F(4, 5))),
         (F(2, 3), (F(2, 3), F(1, 4))),
         (F(-1, 2), (F(0), F(1)))],
    ]
    rows = []
    for seed, components in enumerate(cases):
        rng = random.Random(seed)
        sampler = SignedProductSampler(components, randbelow=rng.randrange)
        points = [None] + list(range(1 << sampler.n))
        values = [sampler.point(x) for x in points]
        assert sum(v for v, _ in values) == 1
        assert sum(a for _, a in values) == sampler.absolute_mass
        positive_mass = sum(max(v, 0) for v, _ in values)
        acceptance = positive_mass / sampler.absolute_mass
        # Enumeration is a small independent identity check, never used by draw.
        proposal_then_accept = [
            a / sampler.absolute_mass * max(v, 0) / a if a else F(0)
            for v, a in values
        ]
        assert sum(proposal_then_accept) == acceptance
        assert [x / acceptance for x in proposal_then_accept] == [
            max(v, 0) / positive_mass for v, _ in values
        ]
        assert acceptance >= 1 / sampler.absolute_mass
        draws = [sampler.draw() for _ in range(2000)]
        assert all(sampler.point(x)[0] > 0 for x in draws)
        rows.append({
            "n": sampler.n, "components": len(components),
            "absolute_coefficient_mass": str(sampler.absolute_mass),
            "positive_part_mass": str(positive_mass),
            "exact_acceptance_probability": str(acceptance),
            "draws": len(draws), "attempts": sampler.attempts,
            "exact_enumerated_identity": "PASS",
        })
    prefix_cases = []
    for scale in (F(1), F(1, 1 << 60)):
        # Both large terms cancel; the retained rare law is not a product.
        n = 4
        p = (F(1, 2),) * n
        components = [(F(1), p), (-(1 - scale), p),
                      (-scale / 16, (F(1),) * n)]
        sampler = SignedProductSampler(components, randbelow=random.Random(99).randrange)
        law = prefix_law_dense(sampler)
        assert law == {x: F(0) if x == 15 else F(1, 15) for x in range(16)}
        assert all(sampler.draw_alive_prefix() != 15 for _ in range(1000))
        prefix_cases.append({"alive_mass": str(15 * scale / 16),
                             "exact_conditioned_law": "uniform on 15 non-target states",
                             "prefix_decisions_per_draw": n, "identity": "PASS"})
    approximate = SignedProductSampler(cases[1])
    law = prefix_law_dense(approximate)
    target = {x: F(0) if x == 15 else F(1, 15) for x in range(16)}
    tv = sum(abs(law[x] - target[x]) for x in target) / 2
    eta, alive_mass = F(1, 16), F(15, 16)
    assert tv <= approximate.n * eta / alive_mass
    prefix_cases.append({"approximate_input_l1_error": str(eta),
                         "actual_output_tv": str(tv),
                         "proved_tv_bound": str(approximate.n * eta / alive_mass),
                         "identity": "PASS"})
    result = {"status": "exact rational law identities; seeded draw demonstration",
              "cases": rows, "prefix_sampler": prefix_cases}
    Path(__file__).with_name("receipt.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    demonstration()
