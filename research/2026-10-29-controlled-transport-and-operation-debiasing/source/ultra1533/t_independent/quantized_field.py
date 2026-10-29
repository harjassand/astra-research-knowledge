"""Outward-Arb quantized conditional Gaussian completion.

Every returned bin is certified for the same persistent lazy iid-bit uniforms.
The runtime library is treated as an outward elementary interval oracle; a seeded
PRNG run diagnoses the program and is not a physical source of iid fair bits.
"""
from flint import fmpq, arb, ctx


def exact_ldl(covariance):
    n = covariance.nrows()
    lower = [[fmpq(i == j) for j in range(n)] for i in range(n)]
    diagonal = []
    for i in range(n):
        value = covariance[i, i] - sum((lower[i][k] ** 2 * diagonal[k] for k in range(i)), fmpq(0))
        assert value > 0
        diagonal.append(value)
        for j in range(i + 1, n):
            lower[j][i] = (covariance[j, i] - sum((lower[j][k] * lower[i][k] * diagonal[k] for k in range(i)), fmpq(0))) / value
    return lower, diagonal


class DyadicUniform:
    def __init__(self, bits):
        self.bits, self.word, self.depth = bits, 0, 0

    def at(self, depth):
        if depth > self.depth:
            extra = depth - self.depth
            self.word = (self.word << extra) + self.bits.get(extra, "uniform")
            self.depth = depth
        return arb(fmpq(2 * self.word + 1, 1 << (self.depth + 1)), fmpq(1, 1 << (self.depth + 1)))


class GaussianRealSample:
    """Persistent exact-real Gaussian sample; evaluations only refine its bits."""
    def __init__(self, covariance, components, bits, factor=None):
        self.n, self.components = covariance.nrows(), components
        self.lower, self.diagonal = exact_ldl(covariance) if factor is None else factor
        self.pairs = (self.n * components + 1) // 2
        self.uniforms = [(DyadicUniform(bits), DyadicUniform(bits)) for _ in range(self.pairs)]

    def evaluate(self, depth):
        ctx.prec = 4 * depth + 128
        normal = []
        for radial, angle in self.uniforms:
            U, V = radial.at(depth), angle.at(depth)
            if not (U > 0 and U < 1):
                return None
            radius, phase = (-2 * U.log()).sqrt(), 2 * arb.pi() * V
            normal.extend([radius * phase.cos(), radius * phase.sin()])
        roots = [arb(d).sqrt() for d in self.diagonal]
        return [[sum((arb(self.lower[i][k]) * roots[k] * normal[component * self.n + k]
                      for k in range(i + 1)), arb(0)) for i in range(self.n)]
                for component in range(self.components)]

    def quantize(self, width, starting_depth=32):
        depth, iterations = starting_depth, 0
        while True:
            iterations += 1
            field = self.evaluate(depth)
            bins = []
            if field is not None:
                for component in field:
                    for value in component:
                        candidate = (value / arb(width)).floor()
                        if not candidate.is_exact():
                            break
                        bins.append(int(candidate.unique_fmpz()))
                    if len(bins) % self.n:
                        break
                if len(bins) == self.n * self.components:
                    return bins, {"uniform_depth": depth, "interval_precision": ctx.prec,
                                  "refinement_rounds": iterations, "independent_box_muller_pairs": self.pairs,
                                  "width": str(width)}
            depth *= 2


def quantized_gaussian(covariance, components, width, bits):
    n = covariance.nrows()
    lower, diagonal = exact_ldl(covariance)
    total = n * components
    pairs = (total + 1) // 2
    uniforms = [(DyadicUniform(bits), DyadicUniform(bits)) for _ in range(pairs)]
    depth = 32
    iterations = 0
    while True:
        iterations += 1
        ctx.prec = 4 * depth + 128
        normal = []
        ready = True
        for radial, angle in uniforms:
            U, V = radial.at(depth), angle.at(depth)
            if not (U > 0 and U < 1):
                ready = False
                break
            radius = (-2 * U.log()).sqrt()
            phase = 2 * arb.pi() * V
            normal.extend([radius * phase.cos(), radius * phase.sin()])
        if ready:
            roots = [arb(d).sqrt() for d in diagonal]
            bins = []
            for component in range(components):
                for i in range(n):
                    value = sum((arb(lower[i][k]) * roots[k] * normal[component * n + k] for k in range(i + 1)), arb(0))
                    candidate = (value / arb(width)).floor()
                    if not candidate.is_exact():
                        ready = False
                        break
                    bins.append(int(candidate.unique_fmpz()))
                if not ready:
                    break
            if ready:
                return bins, {"uniform_depth": depth, "interval_precision": ctx.prec, "refinement_rounds": iterations,
                              "independent_box_muller_pairs": pairs, "width": str(width)}
        # Refine the SAME random variables. No replacement/rejection of a field.
        depth *= 2


def sample_quantized(frame, bits, counts, width=fmpq(1, 4)):
    state, covariance = frame.sample(bits, counts)
    bins, stats = quantized_gaussian(covariance, frame.components, fmpq(width), bits)
    return state, bins, stats
