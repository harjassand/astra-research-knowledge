"""Finite rational monotone CFTP for Gaussian scale-mixture fields.

No floating-point value governs the returned conductance state. A seeded Python
PRNG supplies diagnostic bits; the mathematical sampler uses iid fair bits.
Conditional continuous fields are not returned by this module.
"""
from dataclasses import dataclass
from math import ceil
import random
from flint import fmpq, fmpq_mat


def cycle(n):
    return [(i, (i + 1) % n) for i in range(n)]


def torus(side, dim=2):
    n = side ** dim
    edges = []
    for v in range(n):
        coord = [(v // (side ** k)) % side for k in range(dim)]
        for k in range(dim):
            target = v + side ** k if coord[k] + 1 < side else v - (side - 1) * side ** k
            edges.append((v, target))
    assert side >= 3
    return edges


@dataclass
class Counts:
    fair_bits: int = 0
    edge_bits: int = 0
    uniform_bits: int = 0
    threshold_tests: int = 0
    state_updates: int = 0
    inverse_rank_updates: int = 0
    runs: int = 0
    sampled_words: int = 0
    largest_window: int = 0
    max_returned_inverse_numerator_bits: int = 0
    max_returned_inverse_denominator_bits: int = 0


class Bits:
    def __init__(self, seed, counts):
        self.rng = random.Random(seed)
        self.counts = counts

    def get(self, n, purpose):
        self.counts.fair_bits += n
        if purpose == "edge":
            self.counts.edge_bits += n
        else:
            self.counts.uniform_bits += n
        return self.rng.getrandbits(n)

    def edge(self, m):
        width = (m - 1).bit_length()
        while True:
            value = self.get(width, "edge")
            if value < m:
                return value


class LazyUniform:
    def __init__(self, bits):
        self.bits = bits
        self.word = 0
        self.n = 0

    def refine(self):
        self.word = 2 * self.word + self.bits.get(1, "uniform")
        self.n += 1

    def choose(self, determinant_ratio, prior, components):
        """Return U < p/[p+(1-p)*D**(components/2)] exactly."""
        D = determinant_ratio ** components
        p2, pm2 = prior * prior, (1 - prior) ** 2

        def below(value):
            self.bits.counts.threshold_tests += 1
            return value * value * pm2 * D < p2 * (1 - value) ** 2

        while True:
            lo = fmpq(self.word, 1 << self.n)
            hi = fmpq(self.word + 1, 1 << self.n)
            if below(hi):
                return True
            if not below(lo):
                return False
            self.refine()


class Frame:
    def __init__(self, vertices, edges, contrast=fmpq(2), prior=fmpq(1, 2), components=1, contraction_bound=None):
        assert isinstance(vertices, int) and vertices >= 2 and len(edges) >= 1
        assert isinstance(components, int) and components >= 1
        self.vertices, self.edges = vertices, edges
        self.size, self.m = vertices - 1, len(edges)
        self.q, self.rho = fmpq(contrast), fmpq(contrast) - 1
        self.prior, self.components = fmpq(prior), components
        assert self.q >= 1 and 0 < self.prior < 1 and components >= 1
        self.columns = []
        for u, v in edges:
            assert u != v and 0 <= u < vertices and 0 <= v < vertices
            b = [0] * self.size
            if u:
                b[u - 1] += 1
            if v:
                b[v - 1] -= 1
            self.columns.append(fmpq_mat([[x] for x in b]))
        self.base = fmpq_mat(self.size, self.size)
        for b in self.columns:
            self.base += b * b.transpose()
        self.base_inverse = self.base.inv()
        self.original_c = fmpq(components, 8) * self.q * self.rho ** 2
        self.c = self.original_c if contraction_bound is None else fmpq(contraction_bound)
        if contraction_bound is not None:
            assert self.c >= 0
            # Exact check c >= r*q*(sqrt(q)-1)^2/8, with no floating sqrt.
            A = self.q + 1 - 8 * self.c / (components * self.q)
            assert A <= 0 or A * A <= 4 * self.q
        assert self.c < 1
        # ceil_log2(m)+1 >= log(m)+1; the explicit proof's conservative window.
        ell = (self.m - 1).bit_length() + 1
        bound = fmpq(self.m * ell) / (1 - self.c)
        self.initial_window = (int(bound.p) + int(bound.q) - 1) // int(bound.q)

    def inverse_for(self, state):
        L = fmpq_mat(self.base)
        for x, b in zip(state, self.columns):
            if x:
                L += self.rho * (b * b.transpose())
        return L.inv()

    def determinant_for(self, state):
        L = fmpq_mat(self.base)
        for x, b in zip(state, self.columns):
            if x:
                L += self.rho * (b * b.transpose())
        return L.det()

    def low_ratio(self, inverse, state, e):
        b = self.columns[e]
        column = inverse * b
        R = (b.transpose() * column)[0, 0]
        Rlow = R / (1 - self.rho * R) if state[e] else R
        assert Rlow > 0
        return 1 + self.rho * Rlow, column, R

    def update(self, inverse, state, e, uniform, counts):
        ratio, column, R = self.low_ratio(inverse, state, e)
        value = int(uniform.choose(ratio, self.prior, self.components))
        counts.state_updates += 1
        if value != state[e]:
            delta = self.rho * (value - state[e])
            factor = delta / (1 + delta * R)
            inverse = inverse - factor * (column * column.transpose())
            state[e] = value
            counts.inverse_rank_updates += 1
        return inverse

    def account_inverse(self, inverse, counts):
        for i in range(self.size):
            for j in range(self.size):
                value = inverse[i, j]
                counts.max_returned_inverse_numerator_bits = max(counts.max_returned_inverse_numerator_bits, abs(int(value.p)).bit_length())
                counts.max_returned_inverse_denominator_bits = max(counts.max_returned_inverse_denominator_bits, int(value.q).bit_length())

    def sample(self, bits, counts):
        word = [(bits.edge(self.m), LazyUniform(bits)) for _ in range(self.initial_window)]
        while True:
            counts.runs += 1
            counts.largest_window = max(counts.largest_window, len(word))
            low, high = [0] * self.m, [1] * self.m
            lowinv, highinv = fmpq_mat(self.base_inverse), self.base_inverse / self.q
            for e, uniform in word:
                lowinv = self.update(lowinv, low, e, uniform, counts)
                highinv = self.update(highinv, high, e, uniform, counts)
                assert low[e] <= high[e]
            if low == high:
                assert lowinv == highinv
                self.account_inverse(lowinv, counts)
                counts.sampled_words += 1
                return tuple(low), lowinv
            # Prepend new maps, retain and REPLAY every old random map.
            word = [(bits.edge(self.m), LazyUniform(bits)) for _ in range(len(word))] + word


def draw_batch(frame, samples, seed):
    counts = Counts()
    bits = Bits(seed, counts)
    output = [frame.sample(bits, counts)[0] for _ in range(samples)]
    return output, counts


if __name__ == "__main__":
    import json, time
    from dataclasses import asdict
    started = time.perf_counter()
    frame = Frame(16, torus(4))
    output, counts = draw_batch(frame, 1, 2026103001)
    print(json.dumps({"seconds": time.perf_counter() - started, "state": output[0], "counts": asdict(counts)}))
