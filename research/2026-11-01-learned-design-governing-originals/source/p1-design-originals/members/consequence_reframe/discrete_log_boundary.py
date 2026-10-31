"""Finite diagnostic for the S3 binary-time prediction -> discrete-log reduction.

There is deliberately NO efficient fast-forward algorithm here. Prefix answers
are obtained by charged, ordinary simulation. This checks a mathematical
reduction, not a cryptanalytic advance.
"""

from __future__ import annotations

import json
from class2_fastforward import symmetric_group_three


def field_multiply(x, y, polynomial, degree):
    answer = 0
    while y:
        if y & 1:
            answer ^= x
        y >>= 1
        x <<= 1
        if x & (1 << degree):
            x ^= polynomial
    return answer


class S3Accumulator:
    def __init__(self, degree, polynomial, generator, target):
        self.degree = degree
        self.polynomial = polynomial
        self.generator = generator
        self.target = target
        self.table = symmetric_group_three()
        self.identity = next(e for e in range(6)
                             if all(self.table[e][a] == a == self.table[a][e]
                                    for a in range(6)))
        self.inverse = [next(b for b in range(6)
                             if self.table[a][b] == self.identity == self.table[b][a])
                        for a in range(6)]
        self.a = next(a for a in range(6) if a != self.identity
                      and self.table[a][a] == self.identity)
        self.c = next(c for c in range(6) if c != self.identity
                      and self.table[self.table[c][c]][c] == self.identity)
        assert self.commutator(self.c, self.a) == self.c
        columns = [field_multiply(generator, 1 << j, polynomial, degree)
                   for j in range(degree)]
        self.supports = [[j for j in range(degree) if (columns[j] >> i) & 1]
                         for i in range(degree)]
        self.group_operations = 0

    def mul(self, x, y):
        self.group_operations += 1
        return self.table[x][y]

    def commutator(self, x, y):
        t = self.table
        inv = self.inverse
        return t[t[t[inv[x]][inv[y]]][x]][y]

    def step(self, bits, accumulator):
        # [c^z,a^b]=c^(zb) for z,b in {0,1}.
        # This shared-subexpression circuit ANDs all equality bits in O(m) gates.
        indicator = self.c
        for i, u_i in enumerate(bits):
            target_i = self.a if (self.target >> i) & 1 else self.identity
            equality_bit = self.mul(self.mul(self.a, u_i), target_i)
            indicator = self.mul(
                self.mul(self.mul(self.inverse[indicator],
                                  self.inverse[equality_bit]), indicator),
                equality_bit)
        next_accumulator = self.mul(accumulator, indicator)
        next_bits = []
        for support in self.supports:
            u = self.identity
            for j in support:
                u = self.mul(u, bits[j])
            next_bits.append(u)
        return next_bits, next_accumulator

    def slow_prefix_answer(self, horizon):
        bits = [self.a] + [self.identity] * (self.degree - 1)
        accumulator = self.identity
        for _ in range(horizon):
            bits, accumulator = self.step(bits, accumulator)
        if accumulator not in (self.identity, self.c):
            raise AssertionError("This diagnostic only queries a unique-hit interval")
        return int(accumulator == self.c)


def find_discrete_log_with_prefix_oracle(prefix_oracle, period):
    # If x_k=target, prefix(T)=1 iff T>k on 0<=T<=period.
    low, high, calls = 0, period - 1, 0
    while low < high:
        mid = (low + high) // 2
        if prefix_oracle(mid + 1):
            high = mid
        else:
            low = mid + 1
        calls += 1
    return low, calls


def run_diagnostic():
    cases = []
    total_group_operations = 0
    for degree, polynomial in [(4, 0x13), (5, 0x25), (8, 0x11D)]:
        generator = 2
        period = (1 << degree) - 1
        orbit, x = [], 1
        for _ in range(period):
            orbit.append(x)
            x = field_multiply(generator, x, polynomial, degree)
        assert x == 1 and len(set(orbit)) == period
        exponents = list(range(period)) if degree <= 5 else [0, 1, 2, 31, 63, 127, 191, 254]
        maximum_calls = 0
        for expected in exponents:
            target = orbit[expected]
            circuit = S3Accumulator(degree, polynomial, generator, target)
            found, calls = find_discrete_log_with_prefix_oracle(
                circuit.slow_prefix_answer, period)
            assert found == expected
            assert circuit.slow_prefix_answer(expected) == 0
            assert circuit.slow_prefix_answer(expected + 1) == 1
            total_group_operations += circuit.group_operations
            maximum_calls = max(maximum_calls, calls)
        cases.append({"field_degree": degree, "period": period,
                      "targets_checked": len(exponents),
                      "maximum_prefix_queries": maximum_calls})
    return {"status": "reduction check only; all prefix queries use slow simulation",
            "cases": cases,
            "charged_group_operations": total_group_operations,
            "new_discrete_log_algorithm": False}


if __name__ == "__main__":
    print(json.dumps(run_diagnostic(), indent=2))
