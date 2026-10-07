"""Exact P2 Gibbs measurement sampler on bounded connected components.

Counts are acquired by dense INTEGER matrices on each bounded component.
This is an end-to-end restricted-class algorithm, not a Chen--Liu FPRAS.
The mathematical guarantee assumes independent unbiased random bits.
Only standard Python libraries are used. Outputs stay beside this script.
See BOUNDED_THERMAL_PROOF.txt for quantifiers, costs and error accounting.
"""
from __future__ import annotations

import argparse
from bisect import bisect_right
from dataclasses import dataclass
from fractions import Fraction as F
from hashlib import sha256
from math import gcd, isqrt, lcm
from pathlib import Path
import json
import random
import time


def ceil_q(x: F) -> int:
    return -((-x.numerator) // x.denominator)


def ceil_sqrt_q(x: F) -> int:
    if x < 0:
        raise ValueError("negative square-root argument")
    a = isqrt(x.numerator // x.denominator)
    return a + int(a * a * x.denominator < x.numerator)


def ceil_log2_q(x: F) -> int:
    if x <= 1:
        return 0
    r = max(0, x.numerator.bit_length() - x.denominator.bit_length())
    while (1 << r) * x.denominator < x.numerator:
        r += 1
    return r


def p2(x: F) -> F:
    return 1 + x + x * x / 2


@dataclass(frozen=True)
class Limits:
    max_width: int = 4
    max_components: int = 32
    max_layers: int = 512
    max_entry_bits: int = 32768
    max_global_ratio_bits: int = 262144
    max_input_bits: int = 256
    max_samples: int = 100000
    max_observable_terms: int = 32


@dataclass(frozen=True)
class ComponentInput:
    n: int
    edges: tuple[tuple[int, int, F, F], ...]
    fields: tuple[tuple[F, F], ...]


@dataclass
class Arithmetic:
    matrix_multiplies: int = 0
    integer_products: int = 0
    integer_additions: int = 0


def eye(n: int):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def mm(A, B, stats: Arithmetic):
    n = len(A)
    out = [[0] * n for _ in range(n)]
    stats.matrix_multiplies += 1
    for i in range(n):
        for k in range(n):
            a = A[i][k]
            if a:
                for j in range(n):
                    b = B[k][j]
                    if b:
                        out[i][j] += a * b
                        stats.integer_products += 1
                        stats.integer_additions += 1
    return out


def power(A, m: int, stats: Arithmetic):
    out = eye(len(A))
    while m:
        if m & 1:
            out = mm(out, A, stats)
        m >>= 1
        if m:
            A = mm(A, A, stats)
    return out


def entry_height(K):
    return max(abs(x).bit_length() for row in K for x in row)


def integer_gate(n, vertices, local):
    den = lcm(*(x.denominator for row in local for x in row))
    dim = 1 << n
    out = [[0] * dim for _ in range(dim)]
    for b in range(dim):
        col = sum(((b >> v) & 1) << j for j, v in enumerate(vertices))
        for row in range(len(local)):
            val = local[row][col] * den
            assert val.denominator == 1
            if val:
                a = b
                for j, v in enumerate(vertices):
                    a = (a & ~(1 << v)) | (((row >> j) & 1) << v)
                out[a][b] = val.numerator
    return out, den


def checked_inputs(data: ComponentInput, beta: F, lim: Limits):
    if not 1 <= data.n <= lim.max_width:
        raise ValueError("component width outside admitted resource cap")
    if beta < 0 or len(data.fields) != data.n:
        raise ValueError("invalid temperature or field arity")
    seen = set()
    scalars = [beta]
    for u, v, alpha, gamma in data.edges:
        if not (0 <= u < data.n and 0 <= v < data.n and u != v):
            raise ValueError("invalid loopless edge")
        pair = tuple(sorted((u, v)))
        if pair in seen:
            raise ValueError("duplicate edge; combine its coefficients first")
        seen.add(pair)
        if alpha < abs(gamma):
            raise ValueError("edge outside admitted alpha>=|gamma| cone")
        scalars.extend((alpha, gamma))
    for b, c in data.fields:
        if b < 0:
            raise ValueError("negative transverse field outside this gauge")
        scalars.extend((b, c))
    for x in scalars:
        if max(x.numerator.bit_length(), x.denominator.bit_length()) > lim.max_input_bits:
            raise ValueError("input rational exceeds stated bit cap")


class DyadicCDF:
    """Exact law of floor-grid inverse CDF; no rejection or variable tape."""
    def __init__(self, weights, delta: F):
        if not 0 < delta <= 1 or any(w < 0 for w in weights):
            raise ValueError("bad CDF input")
        total = sum(weights)
        if total <= 0:
            raise ValueError("zero normalizer")
        self.pi = tuple(F(w, total) for w in weights)
        self.bits = ceil_log2_q(F(len(weights) - 1) / delta)
        self.grid = 1 << self.bits
        cdf = F(0)
        thresholds = []
        for p in self.pi:
            cdf += p
            thresholds.append(ceil_q(cdf * self.grid))
        assert thresholds[-1] == self.grid
        self.thresholds = tuple(thresholds)
        previous = 0
        law = []
        for bound in thresholds:
            law.append(F(bound - previous, self.grid))
            previous = bound
        self.mu = tuple(law)
        self.actual_tv = sum(abs(p - q) for p, q in zip(self.pi, self.mu)) / 2
        self.proved_tv = F(len(weights) - 1, self.grid)
        assert self.actual_tv <= self.proved_tv <= delta

    def from_bits(self, j: int) -> int:
        if not 0 <= j < self.grid:
            raise ValueError("random tape integer outside its fixed range")
        return bisect_right(self.thresholds, j)

    def draw(self, rng) -> int:
        return self.from_bits(rng.getrandbits(self.bits))


class CompiledComponent:
    def __init__(self, data: ComponentInput, beta: F, kappa: F,
                 delta: F, lim: Limits, stats: Arithmetic):
        checked_inputs(data, beta, lim)
        self.n = data.n
        self.dim = 1 << self.n
        self.C = 3 * sum((a for _, _, a, _ in data.edges), F(0))
        self.C += sum((b + abs(c) for b, c in data.fields), F(0))
        self.tau = 2 * beta * self.C
        self.m = max(1, ceil_q(2 * self.tau),
                     ceil_sqrt_q(F(43, 60) * self.tau ** 3 / kappa))
        if self.m > lim.max_layers:
            raise ValueError("proved layer schedule exceeds admitted cost cap")
        self.generator_bound = F(43, 60) * self.tau ** 3 / self.m ** 2
        assert self.generator_bound <= kappa and self.m >= 2 * self.tau
        h = beta / (2 * self.m)
        W, Wden = eye(self.dim), 1
        self.p = 0
        for u, v, alpha, gamma in data.edges:
            if not alpha:
                continue
            low = p2(h * (alpha - gamma))
            middle = p2(h * (3 * alpha + gamma))
            high = p2(h * (5 * alpha - gamma))
            a, b, c = middle, (high + low) / 2, (high - low) / 2
            assert a > 0 and b > 0 and c >= 0 and abs(a - b) <= c <= a + b
            gate, den = integer_gate(self.n, (u, v),
                                     [[a, F(0), F(0), F(0)],
                                      [F(0), b, c, F(0)],
                                      [F(0), c, b, F(0)],
                                      [F(0), F(0), F(0), a]])
            W = mm(W, gate, stats)
            Wden *= den
            self.p += 1
            if max(entry_height(W), Wden.bit_length()) > lim.max_entry_bits:
                raise ValueError("intermediate gate product exceeds admitted bit cap")
        for v, (b, c) in enumerate(data.fields):
            if not (b or c):
                continue
            r = b + abs(c)
            v0 = 1 + h * (r + c) + h * h * ((r + c) ** 2 + b * b) / 2
            u0 = 1 + h * (r - c) + h * h * ((r - c) ** 2 + b * b) / 2
            d = h * b + h * h * r * b
            assert u0 > 0 and v0 > 0 and d >= 0 and u0 * v0 > d * d
            gate, den = integer_gate(self.n, (v,), [[v0, d], [d, u0]])
            W = mm(W, gate, stats)
            Wden *= den
            self.p += 1
            if max(entry_height(W), Wden.bit_length()) > lim.max_entry_bits:
                raise ValueError("intermediate gate product exceeds admitted bit cap")
        B = mm(W, list(map(list, zip(*W))), stats)
        self.preflight_bit_bound = max(self.m * (entry_height(B) + self.n),
                                       2 * self.m * Wden.bit_length())
        if self.preflight_bit_bound > lim.max_entry_bits:
            raise ValueError("conservative power operand bound exceeds admitted bit cap")
        self.K = power(B, self.m, stats)
        self.Kden = Wden ** (2 * self.m)
        self.trace = sum(self.K[b][b] for b in range(self.dim))
        self.max_bits = max(entry_height(self.K), self.Kden.bit_length())
        if self.max_bits > lim.max_entry_bits:
            raise ValueError("acquired integer matrix exceeds admitted bit cap")
        assert all(x >= 0 for row in self.K for x in row)
        assert all(self.K[a][b] == self.K[b][a] for a in range(self.dim) for b in range(self.dim))
        assert all(self.K[b][b] > 0 for b in range(self.dim))
        self.cdf = DyadicCDF([self.K[b][b] for b in range(self.dim)], delta)

    def digest(self):
        h = sha256()
        for row in self.K:
            for x in row:
                data = x.to_bytes(max(1, (x.bit_length() + 7) // 8), "big")
                h.update(len(data).to_bytes(8, "big")); h.update(data)
        return h.hexdigest()


class PauliObservable:
    """Rational sum of I/X/Z strings, with l1 coefficient norm <=1."""
    def __init__(self, terms, widths):
        self.widths = tuple(widths)
        n = sum(widths)
        if not terms or sum(abs(F(c)) for c, _ in terms) > 1:
            raise ValueError("observable norm certificate sum |coefficients|<=1 failed")
        self.terms = []
        for c, word in terms:
            if len(word) != n or any(x not in "IXZ" for x in word):
                raise ValueError("observable must be an I/X/Z Pauli string of full arity")
            offset, masks = 0, []
            for width in widths:
                local = word[offset:offset + width]
                masks.append((sum((x == "X") << j for j, x in enumerate(local)),
                              sum((x == "Z") << j for j, x in enumerate(local))))
                offset += width
            self.terms.append((F(c), word, tuple(masks)))
        self.row_sparsity_bound = len(self.terms)

    def local_values(self, comp, masks):
        flip, signmask = masks
        return tuple(F((-1 if (b & signmask).bit_count() & 1 else 1) * comp.K[b ^ flip][b],
                       comp.K[b][b]) for b in range(comp.dim))

    def ratio(self, components, state, limits):
        total = F(0)
        for coefficient, _, masks in self.terms:
            num, den = 1, 1
            for comp, b, (flip, signmask) in zip(components, state, masks):
                if not flip:
                    num *= -1 if (b & signmask).bit_count() & 1 else 1
                else:
                    num *= (-1 if (b & signmask).bit_count() & 1 else 1) * comp.K[b ^ flip][b]
                    den *= comp.K[b][b]
            if max(abs(num).bit_length(), den.bit_length()) > limits.max_global_ratio_bits:
                raise ValueError("global ratio operand exceeds admitted bit cap")
            total += coefficient * F(num, den)
        return total

    def exact_moments(self, components, law):
        tables = [[self.local_values(comp, masks[j]) for j, comp in enumerate(components)]
                  for _, _, masks in self.terms]
        first, second, sup = F(0), F(0), F(0)
        for k, (coefficient, _, _) in enumerate(self.terms):
            value, bound = coefficient, abs(coefficient)
            for j, comp in enumerate(components):
                probs = comp.cdf.pi if law == "pi" else comp.cdf.mu
                value *= sum((p * x for p, x in zip(probs, tables[k][j])), F(0))
                bound *= max(abs(x) for x in tables[k][j])
            first += value
            sup += bound
        for k, (ck, _, _) in enumerate(self.terms):
            for l, (cl, _, _) in enumerate(self.terms):
                value = ck * cl
                for j, comp in enumerate(components):
                    probs = comp.cdf.pi if law == "pi" else comp.cdf.mu
                    value *= sum((p * x * y for p, x, y in
                                  zip(probs, tables[k][j], tables[l][j])), F(0))
                second += value
        return first, second, sup


def quantize_clip(x: F, T: F, bits: int) -> int:
    x = max(-T, min(T, x))
    scale = 1 << bits
    # Deterministic nearest dyadic, ties toward positive infinity.
    return (2 * x.numerator * scale + x.denominator) // (2 * x.denominator)


class BoundedThermal:
    def __init__(self, inputs, beta: F, observable: PauliObservable,
                 epsilon: F, sampler_epsilon: F, limits=Limits()):
        if not 0 < epsilon <= 1 or not 0 < sampler_epsilon <= 1:
            raise ValueError("errors must lie in (0,1]")
        if not 1 <= len(inputs) <= limits.max_components:
            raise ValueError("component count outside admitted resource cap")
        if observable.widths != tuple(x.n for x in inputs):
            raise ValueError("observable/component mismatch")
        if len(observable.terms) > limits.max_observable_terms:
            raise ValueError("observable term count exceeds admitted cost cap")
        for coefficient, _, _ in observable.terms:
            if max(abs(coefficient.numerator).bit_length(), coefficient.denominator.bit_length()) > limits.max_input_bits:
                raise ValueError("observable coefficient exceeds rational input bit cap")
        self.inputs, self.beta, self.observable = inputs, beta, observable
        self.epsilon, self.sampler_epsilon, self.limits = epsilon, sampler_epsilon, limits
        self.kappa = min(sampler_epsilon / 2, epsilon / 100)
        self.delta = min(sampler_epsilon / 2, epsilon * epsilon / 1000)
        self.T = 10 / epsilon
        self.value_bits = ceil_log2_q(1000 / epsilon)
        self.samples = ceil_q(256 / (epsilon * epsilon))
        if self.samples > limits.max_samples:
            raise ValueError("proved sample schedule exceeds admitted cost cap")
        self.stats = Arithmetic()
        start = time.monotonic()
        J = len(inputs)
        self.components = [CompiledComponent(x, beta, self.kappa / J,
                                             self.delta / J, limits, self.stats)
                           for x in inputs]
        if sum(x.max_bits for x in self.components) > limits.max_global_ratio_bits:
            raise ValueError("global ratio bit bound exceeds admitted cost cap")
        self.compile_seconds = time.monotonic() - start
        self.generator_bound = sum((x.generator_bound for x in self.components), F(0))
        self.exact_cdf_tv_sum = sum((x.cdf.actual_tv for x in self.components), F(0))
        self.cdf_tv_sum_bound = sum((x.cdf.proved_tv for x in self.components), F(0))
        assert self.generator_bound <= self.kappa
        assert self.cdf_tv_sum_bound <= self.delta
        self.pi_mean, self.pi_second, self.ratio_sup_bound = observable.exact_moments(self.components, "pi")
        self.mu_mean, self.mu_second, _ = observable.exact_moments(self.components, "mu")
        assert 0 <= self.pi_second <= 1

    def sample(self, rng):
        return tuple(comp.cdf.draw(rng) for comp in self.components)

    def estimate(self, rng):
        start = time.monotonic()
        total = 0
        hist = [[0] * x.dim for x in self.components]
        examples = []
        for index in range(self.samples):
            state = self.sample(rng)
            for j, b in enumerate(state):
                hist[j][b] += 1
            if index < 12:
                examples.append("".join(format(b, f"0{comp.n}b")[::-1]
                                        for b, comp in zip(state, self.components)))
            total += quantize_clip(self.observable.ratio(self.components, state, self.limits),
                                   self.T, self.value_bits)
        estimate = F(total, self.samples * (1 << self.value_bits))
        estimate = max(F(-1), min(F(1), estimate))
        return {"estimate_rational": str(estimate), "estimate_decimal": float(estimate),
                "estimation_seconds": time.monotonic() - start,
                "sample_count": self.samples,
                "fair_random_bits": self.samples * sum(x.cdf.bits for x in self.components),
                "sample_examples_qubit_order": examples,
                "component_histograms": hist,
                "absolute_error_against_exact_compiled_state": float(abs(estimate - self.pi_mean))}

    def report(self):
        # Moment expressions can have long integers: decimal summaries below
        # are observations, while guarantees are exact rational small bounds.
        return {"scope": "Exact dense counts on bounded disconnected components; no Chen-Liu FPRAS",
                "n": sum(x.n for x in self.inputs), "components": len(self.components),
                "beta": str(self.beta), "epsilon": str(self.epsilon),
                "sampler_epsilon": str(self.sampler_epsilon),
                "limits": vars(self.limits), "compile_seconds": self.compile_seconds,
                "arithmetic_observed": vars(self.stats),
                "proved_generator_bound": str(self.generator_bound),
                "proved_cdf_tv_sum": str(self.cdf_tv_sum_bound),
                "exact_cdf_tv_sum_decimal": float(self.exact_cdf_tv_sum),
                "proved_Gibbs_measurement_TV_bound": str(self.generator_bound + self.cdf_tv_sum_bound),
                "compiled_state_exact_mean_decimal": float(self.pi_mean),
                "compiled_state_exact_second_moment_decimal": float(self.pi_second),
                "implemented_dyadic_law_exact_mean_decimal": float(self.mu_mean),
                "implemented_dyadic_law_exact_second_moment_decimal": float(self.mu_second),
                "pointwise_ratio_sup_bound_decimal": float(self.ratio_sup_bound),
                "clipping_provably_inactive_on_this_instance": self.ratio_sup_bound <= self.T,
                "single_estimate_failure_upper_bound": "3/160",
                "observable_bias_upper_bound": str(self.epsilon / 5),
                "observable_norm_certificate": "sum absolute rational Pauli coefficients <=1",
                "observable_terms": [{"coefficient": str(c), "word": word} for c, word, _ in self.observable.terms],
                "components_metadata": [{"width": x.n, "local_terms": x.p, "C": str(x.C),
                                         "tau": str(x.tau), "layers": x.m,
                                         "generator_bound": str(x.generator_bound),
                                         "maximum_acquired_integer_bits": x.max_bits,
                                         "preflight_integer_bit_bound": x.preflight_bit_bound,
                                         "fixed_random_bits_per_sample": x.cdf.bits,
                                         "integer_K_sha256": x.digest()}
                                        for x in self.components]}


def make_demo(count: int):
    blocks = []
    for j in range(count):
        a = F(1, 8) if j % 2 == 0 else F(3, 16)
        edges = ((0, 1, a, a / 2), (1, 2, a, -a / 3), (0, 2, a / 2, F(0)))
        fields = ((F(1, 16), F(1, 32)), (F(1, 12), -F(1, 24)), (F(1, 20), F(0)))
        blocks.append(ComponentInput(3, edges, fields))
    n = 3 * count
    terms = [(F(1, 3), "X" + "I" * (n - 1)),
             (F(1, 3), "X" * n), (F(1, 3), "Z" * n)]
    return blocks, PauliObservable(terms, [3] * count)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--components", type=int, default=16)
    parser.add_argument("--beta", default="1/8")
    parser.add_argument("--epsilon", default="1/5")
    parser.add_argument("--sampler-epsilon", default="1/10")
    parser.add_argument("--seed", type=int, default=None,
                        help="deterministic diagnostic replay only; default SystemRandom")
    parser.add_argument("--output", default="bounded_thermal_run.json")
    args = parser.parse_args()
    if Path(args.output).name != args.output:
        parser.error("output must be a basename in the owned script directory")
    inputs, obs = make_demo(args.components)
    engine = BoundedThermal(inputs, F(args.beta), obs, F(args.epsilon), F(args.sampler_epsilon))
    rng = random.SystemRandom() if args.seed is None else random.Random(args.seed)
    result = engine.report()
    result.update(engine.estimate(rng))
    result["random_source"] = "SystemRandom; ideal independent fair-bit contract" if args.seed is None else f"seeded diagnostic replay {args.seed}; probability theorem not inferred from PRNG seed"
    result["status"] = "COMPLETE_RESTRICTED_CLASS_THERMAL_SAMPLING_AND_ESTIMATION"
    result["input_blocks"] = [{"n": x.n,
                               "edges": [[u, v, str(a), str(g)] for u, v, a, g in x.edges],
                               "fields": [[str(b), str(c)] for b, c in x.fields]}
                              for x in inputs]
    path = Path(__file__).with_name(args.output)
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ["status", "n", "components", "compile_seconds",
                                           "estimation_seconds", "sample_count", "fair_random_bits",
                                           "proved_Gibbs_measurement_TV_bound", "estimate_decimal",
                                           "absolute_error_against_exact_compiled_state"]}, indent=2))


if __name__ == "__main__":
    main()
