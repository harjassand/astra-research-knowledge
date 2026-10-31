"""Acquire a noisy local group law and compile binary-horizon ring evolution.

Research diagnostic, not a novelty claim or a physical experiment. The learner
receives only labelled pair-query results. No group coordinates, decomposition,
or long-time simulator are passed to it. All arithmetic is exact and stdlib-only.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import ceil, gcd, log
from random import Random
from time import perf_counter
import json


class NotClassTwoGroup(ValueError):
    pass


class NoisyPairOracle:
    def __init__(self, table, noise, seed):
        self._table = table
        self.noise = noise
        self.rng = Random(seed)
        self.calls = 0
        self.q = len(table)

    def query(self, a, b):
        self.calls += 1
        ans = self._table[a][b]
        if self.rng.random() < self.noise:
            wrong = self.rng.randrange(self.q - 1)
            return wrong + (wrong >= ans)
        return ans


def acquire_table(oracle, noise_upper, delta):
    """Conditional correctness bias >= 1-noise_upper is a supplied premise."""
    q = oracle.q
    gamma = 0.5 - noise_upper
    if gamma <= 0:
        raise ValueError("Positive correct-label majority bias is required")
    repeats = ceil(log(q * q / delta) / (2 * gamma * gamma))
    if repeats % 2 == 0:
        repeats += 1
    table = []
    for a in range(q):
        row = []
        for b in range(q):
            counts = Counter(oracle.query(a, b) for _ in range(repeats))
            label, count = counts.most_common(1)[0]
            if count <= repeats // 2:
                raise ValueError("No strict majority; acquisition abstains")
            row.append(label)
        table.append(row)
    return table, repeats


@dataclass
class AcquiredGroup:
    table: list
    identity: int
    inverses: list
    exponent: int
    commutators: list
    powers: list
    associativity_checks: int
    centrality_checks: int

    @classmethod
    def certify(cls, table):
        q = len(table)
        if any(len(row) != q or any(v < 0 or v >= q for v in row)
               for row in table):
            raise NotClassTwoGroup("Not a total labelled binary table")
        candidates = [e for e in range(q)
                      if all(table[e][a] == a == table[a][e]
                             for a in range(q))]
        if len(candidates) != 1:
            raise NotClassTwoGroup("No unique two-sided identity")
        e = candidates[0]
        inverses = []
        for a in range(q):
            matches = [b for b in range(q)
                       if table[a][b] == e == table[b][a]]
            if len(matches) != 1:
                raise NotClassTwoGroup("No unique two-sided inverse")
            inverses.append(matches[0])
        assoc = 0
        for a in range(q):
            for b in range(q):
                for c in range(q):
                    assoc += 1
                    if table[table[a][b]][c] != table[a][table[b][c]]:
                        raise NotClassTwoGroup("Associativity fails")
        comm = [[0] * q for _ in range(q)]
        central = 0
        for a in range(q):
            for b in range(q):
                k = table[table[table[inverses[a]][inverses[b]]][a]][b]
                comm[a][b] = k
                for c in range(q):
                    central += 1
                    if table[k][c] != table[c][k]:
                        raise NotClassTwoGroup("A commutator is not central")
        exponent = 1
        for a in range(q):
            power = e
            for order in range(1, q + 1):
                power = table[power][a]
                if power == e:
                    exponent = exponent * order // gcd(exponent, order)
                    break
            else:
                raise NotClassTwoGroup("Invalid finite group order")
        powers = []
        for a in range(q):
            row = [e]
            for k in range(1, 2 * exponent):
                row.append(table[row[-1]][a])
            powers.append(row)
        return cls(table, e, inverses, exponent, comm, powers, assoc, central)


@dataclass(frozen=True)
class Word:
    """x_0^a_0 ... x_(n-1)^a_(n-1) product_(i<j) [x_i,x_j]^b_ij."""
    a: tuple
    b: tuple
    exponent: int

    @property
    def n(self):
        return len(self.a)

    @classmethod
    def make(cls, a, b, exponent):
        n = len(a)
        return cls(tuple(v % (2 * exponent) for v in a),
                   tuple(tuple(b[i][j] % exponent if i < j else 0
                               for j in range(n)) for i in range(n)),
                   exponent)

    @classmethod
    def identity(cls, n, exponent):
        a = [0] * n
        a[0] = 1
        return cls.make(a, [[0] * n for _ in range(n)], exponent)

    @classmethod
    def neighbor_product(cls, n, exponent):
        a = [0] * n
        a[0] += 1
        a[1 % n] += 1
        return cls.make(a, [[0] * n for _ in range(n)], exponent)

    def shifted(self, offset):
        """Replace every x_i by x_(i+offset mod n), then collect."""
        n, E = self.n, self.exponent
        a = [0] * n
        b = [[0] * n for _ in range(n)]
        for i in range(n):
            a[(i + offset) % n] = self.a[i]
        for i in range(n):
            u = (i + offset) % n
            for j in range(i + 1, n):
                v = (j + offset) % n
                if u < v:
                    b[u][v] += self.b[i][j]
                else:
                    b[v][u] -= self.b[i][j] + self.a[i] * self.a[j]
        return Word.make(a, b, E)

    def evaluate(self, state, group, offset=0):
        n = self.n
        x = [state[(i + offset) % n] for i in range(n)]
        out = group.identity
        mul, powers = group.table, group.powers
        for i in range(n):
            out = mul[out][powers[x[i]][self.a[i]]]
        for i in range(n):
            for j in range(i + 1, n):
                if self.b[i][j]:
                    c = group.commutators[x[i]][x[j]]
                    out = mul[out][powers[c][self.b[i][j]]]
        return out

    def evaluate_ring(self, state, group):
        return [self.evaluate(state, group, i) for i in range(self.n)]


def matmul(A, B, modulus):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            a = A[i][k] % modulus
            if a:
                for j in range(n):
                    C[i][j] += a * B[k][j]
        for j in range(n):
            C[i][j] %= modulus
    return C


def compose(outer, inner):
    """Return the base word of equivariant map outer after map inner.

    O(n^3) exact modular operations, O(n^2) space. Matrices here implement
    collection of acquired nonlinear group words; they are not supplied models.
    """
    assert outer.n == inner.n and outer.exponent == inner.exponent
    n, E = outer.n, outer.exponent
    M = 2 * E
    A = [[inner.a[(j - i) % n] for j in range(n)] for i in range(n)]
    a = [sum(outer.a[i] * A[i][j] for i in range(n)) % M
         for j in range(n)]
    K = [[0] * n for _ in range(n)]
    for i in range(n):
        K[i][i] = -(outer.a[i] * (outer.a[i] - 1) // 2) % E
        for j in range(i + 1, n):
            K[i][j] = outer.b[i][j]
            K[j][i] = (-outer.b[i][j] - outer.a[i] * outer.a[j]) % E
    At = [list(row) for row in zip(*A)]
    D = matmul(matmul(At, K, E), A, E)
    for i in range(n):
        V = inner.shifted(i)
        for j in range(n):
            for k in range(j + 1, n):
                D[j][k] = (D[j][k] + outer.a[i] * V.b[j][k]) % E
    return Word.make(a, D, E)


def compile_power(n, exponent, horizon):
    if horizon < 0:
        raise ValueError("Horizon must be nonnegative")
    answer = Word.identity(n, exponent)
    base = Word.neighbor_product(n, exponent)
    compositions = 0
    t = horizon
    while t:
        if t & 1:
            answer = compose(base, answer)
            compositions += 1
        t >>= 1
        if t:
            base = compose(base, base)
            compositions += 1
    return answer, compositions


def direct_simulation(table, state, horizon):
    x = list(state)
    n = len(x)
    for _ in range(horizon):
        x = [table[x[i]][x[(i + 1) % n]] for i in range(n)]
    return x


def hidden_heisenberg(p, seed=918):
    """Synthetic source. Coordinates stay outside all acquisition/compile APIs."""
    states = [(a, b, c) for a in range(p) for b in range(p) for c in range(p)]
    labels = list(range(len(states)))
    Random(seed).shuffle(labels)
    encode = dict(zip(states, labels))
    table = [[0] * len(states) for _ in states]
    for a, b, c in states:
        for d, e, f in states:
            table[encode[a, b, c]][encode[d, e, f]] = encode[
                (a + d) % p, (b + e) % p, (c + f + a * e) % p]
    return table


def symmetric_group_three():
    from itertools import permutations
    states = list(permutations(range(3)))
    labels = {x: i for i, x in enumerate(states)}
    return [[labels[tuple(a[b[i]] for i in range(3))] for b in states]
            for a in states]


def quaternion_group():
    """Q8 also exercises even exponent, for which a modulo E alone is unsafe."""
    table = [[0] * 8 for _ in range(8)]
    for a in range(8):
        for b in range(8):
            sign = (-1 if a >= 4 else 1) * (-1 if b >= 4 else 1)
            i, j = a % 4, b % 4
            if i == 0:
                k = j
            elif j == 0:
                k = i
            elif i == j:
                sign, k = -sign, 0
            else:
                k = 6 - i - j
                if (i, j) not in [(1, 2), (2, 3), (3, 1)]:
                    sign = -sign
            table[a][b] = k + (4 if sign < 0 else 0)
    return table


def linear_shadow_period_43():
    """Exact order of 1+X in F3[X]/(X^43-1), using verified factor descent."""
    def factor(n):
        result, p = {}, 2
        while p * p <= n:
            while n % p == 0:
                result[p] = result.get(p, 0) + 1
                n //= p
            p = 3 if p == 2 else p + 2
        if n > 1:
            result[n] = result.get(n, 0) + 1
        return result

    fs = {}
    for number in [3**21 - 1, 3**21 + 1]:
        for p, k in factor(number).items():
            fs[p] = fs.get(p, 0) + k
    n = 43
    identity = [1] + [0] * (n - 1)
    base = [1, 1] + [0] * (n - 2)

    def mul(a, b):
        c = [0] * n
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                c[(i + j) % n] += x * y
        return [x % 3 for x in c]

    def power(t):
        a, b = identity, base
        while t:
            if t & 1:
                a = mul(a, b)
            t >>= 1
            if t:
                b = mul(b, b)
        return a

    period = 3**42 - 1
    assert power(period) == identity
    for p in fs:
        while period % p == 0 and power(period // p) == identity:
            period //= p
    return period


def run_diagnostic():
    true_table = hidden_heisenberg(3)
    noise_upper, delta = 0.20, 1e-6
    oracle = NoisyPairOracle(true_table, 0.18, 31)
    start = perf_counter()
    learned_table, repeats = acquire_table(oracle, noise_upper, delta)
    acquired = AcquiredGroup.certify(learned_table)
    acquisition_seconds = perf_counter() - start
    assert learned_table == true_table  # Diagnostic only, not used by learner.

    rng = Random(881)
    cases = []
    for n in [1, 2, 3, 5, 8, 12]:
        for T in [0, 1, 2, 3, 5, 16, 37, 113, 1000]:
            state = [rng.randrange(oracle.q) for _ in range(n)]
            summary, compositions = compile_power(n, acquired.exponent, T)
            fast = summary.evaluate_ring(state, acquired)
            expected = direct_simulation(learned_table, state, T)
            assert fast == expected, (n, T, state, fast, expected)
            cases.append((n, T))

    # Test arbitrary nonlinear equivariant words, not just powers of one map.
    composition_cases = 0
    for n in [2, 3, 5, 8]:
        for _ in range(20):
            words = []
            for _ in range(2):
                a = [rng.randrange(2 * acquired.exponent) for _ in range(n)]
                b = [[rng.randrange(acquired.exponent) for _ in range(n)]
                     for _ in range(n)]
                words.append(Word.make(a, b, acquired.exponent))
            outer, inner = words
            state = [rng.randrange(oracle.q) for _ in range(n)]
            lhs = compose(outer, inner).evaluate_ring(state, acquired)
            rhs = outer.evaluate_ring(inner.evaluate_ring(state, acquired), acquired)
            assert lhs == rhs
            composition_cases += 1

    q8 = AcquiredGroup.certify(quaternion_group())
    even_exponent_cases = 0
    for n in [1, 2, 3, 5, 8]:
        for T in [1, 2, 3, 11, 64, 131]:
            state = [rng.randrange(8) for _ in range(n)]
            summary, _ = compile_power(n, q8.exponent, T)
            assert summary.evaluate_ring(state, q8) == direct_simulation(q8.table, state, T)
            even_exponent_cases += 1

    # Reuse the same acquired law at a binary horizon beyond explicit replay.
    n, horizon = 43, 10**18 + 12345
    noncommuting = next((a, b) for a in range(oracle.q) for b in range(oracle.q)
                       if acquired.commutators[a][b] != acquired.identity)
    state = list(noncommuting) + [acquired.identity] * (n - 2)
    start = perf_counter()
    summary, compositions = compile_power(n, acquired.exponent, horizon)
    out = summary.evaluate_ring(state, acquired)
    huge_seconds = perf_counter() - start
    # A metamorphic check also crosses a large horizon using two subpowers.
    left, _ = compile_power(n, acquired.exponent, horizon // 2)
    right, _ = compile_power(n, acquired.exponent, horizon - horizon // 2)
    assert right.evaluate_ring(left.evaluate_ring(state, acquired), acquired) == out

    rejected = False
    try:
        AcquiredGroup.certify(symmetric_group_three())
    except NotClassTwoGroup:
        rejected = True
    assert rejected
    return {
        "status": "synthetic mathematical diagnostic; no novelty or physical claim",
        "alphabet_size": oracle.q,
        "noise_actual": 0.18,
        "noise_upper_supplied": noise_upper,
        "delta": delta,
        "repeats_per_pair": repeats,
        "experimental_pair_queries": oracle.calls,
        "whole_table_exact_in_synthetic_check": True,
        "acquisition_and_class_certification_seconds": acquisition_seconds,
        "associativity_checks": acquired.associativity_checks,
        "centrality_checks": acquired.centrality_checks,
        "acquired_exponent": acquired.exponent,
        "finite_direct_replay_cases": len(cases),
        "arbitrary_word_composition_cases": composition_cases,
        "Q8_even_exponent_replay_cases": even_exponent_cases,
        "huge_horizon": horizon,
        "huge_ring_length": n,
        "huge_state_has_noncommuting_symbols": True,
        "huge_linear_shadow_exact_period": linear_shadow_period_43(),
        "huge_summary_scalar_slots": n + n * (n - 1) // 2,
        "huge_compositions": compositions,
        "huge_compile_and_execute_seconds": huge_seconds,
        "huge_output": out,
        "huge_split_composition_check": True,
        "huge_direct_replay_performed": False,
        "nonclass_two_S3_rejected": rejected,
    }


if __name__ == "__main__":
    print(json.dumps(run_diagnostic(), indent=2))
