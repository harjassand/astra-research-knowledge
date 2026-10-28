"""Exact finite-lattice acquisition without individual coupling normalization.

All source access is through acquired node intervals. Hidden coefficients are
used only by the separate check driver, never by this law representation.
"""
from collections import defaultdict
from fractions import Fraction as F
from math import comb, factorial


def compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in compositions(total - first, length - 1):
                yield (first,) + rest


def falling_binomial(value, degree):
    out = F(1)
    for j in range(degree):
        out *= (value - j) / (j + 1)
    return out


def chebyshev(degree, value):
    if degree == 0:
        return F(1)
    before, current = F(1), F(value)
    for _ in range(1, degree):
        before, current = current, 2 * value * current - before
    return current


def barycentric(u, delta):
    assert delta > 0 and all(x >= 0 for x in u) and sum(u) <= delta
    return [1 - sum(u) / delta] + [x / delta for x in u]


def lagrange_weights(alphas, lambdas, degree):
    factors = [[falling_binomial(degree * x, j) for j in range(degree + 1)]
               for x in lambdas]
    answer = []
    for alpha in alphas:
        value = F(1)
        for i, count in enumerate(alpha):
            if count:
                value *= factors[i][count]
                if not value:
                    break
        answer.append(value)
    return answer


def bernstein_weight(alpha, lambdas, degree):
    value = F(factorial(degree))
    for count, x in zip(alpha, lambdas):
        if count:
            value *= x ** count / factorial(count)
            if not value:
                break
    return value


def bernstein_weights(alphas, lambdas, degree):
    return [bernstein_weight(alpha, lambdas, degree) for alpha in alphas]


def solve(matrix, rhs):
    a = [list(row) + [value] for row, value in zip(matrix, rhs)]
    n = len(rhs)
    for k in range(n):
        pivot = next(i for i in range(k, n) if a[i][k])
        a[k], a[pivot] = a[pivot], a[k]
        scale = a[k][k]
        a[k] = [x / scale for x in a[k]]
        for i in range(n):
            if i != k and a[i][k]:
                scale = a[i][k]
                a[i] = [x - scale * y for x, y in zip(a[i], a[k])]
    return [row[-1] for row in a]


def nodal_to_bernstein(alphas, values, degree):
    """Exact face-by-face transform, max block order binom(k-1,s-1).

    A node with barycentric support S only sees coefficients on subfaces of S.
    Lower-face coefficients are already known when the interior block is solved.
    """
    groups = defaultdict(list)
    nodal = dict(zip(alphas, values))
    ncoords = len(alphas[0])
    for alpha in alphas:
        groups[tuple(i for i, a in enumerate(alpha) if a)].append(alpha)
    coefficients = {}
    blocks = 0
    max_block = 0
    for support in sorted(groups, key=lambda s: (len(s), s)):
        interior = groups[support]
        all_on_face = []
        for local in compositions(degree, len(support)):
            alpha = [0] * ncoords
            for i, count in zip(support, local):
                alpha[i] = count
            all_on_face.append(tuple(alpha))
        lower_face = [a for a in all_on_face if a in coefficients]
        matrix, rhs = [], []
        for beta in interior:
            lambdas = [F(x, degree) for x in beta]
            matrix.append([bernstein_weight(a, lambdas, degree) for a in interior])
            rhs.append(nodal[beta] - sum(coefficients[a] * bernstein_weight(a, lambdas, degree)
                                        for a in lower_face))
        solutions = solve(matrix, rhs)
        coefficients.update(zip(interior, solutions))
        blocks += 1
        max_block = max(max_block, len(interior))
    assert len(coefficients) == len(alphas)
    return [coefficients[a] for a in alphas], {'face_blocks': blocks, 'maximum_block_order': max_block}


class SimplexLaw:
    def __init__(self, n, degree, delta=F(1, 5), G=F(1), kappa=F(1)):
        assert n >= 1 and degree >= 1 and delta > 0 and G >= 0 and kappa >= 0
        self.n, self.k = n, degree
        self.delta, self.G, self.kappa = F(delta), F(G), F(kappa)
        self.q = self.delta * self.kappa
        self.alphas = list(compositions(degree, n + 1))
        self.nodes = [[self.delta * a / degree for a in alpha[1:]] for alpha in self.alphas]
        assert len(self.nodes) == comb(n + degree, degree)
        self.lebesgue_upper = F(comb(2 * degree - 1, degree))
        self.taylor_remainder = self.delta * self.G ** 2 * self.q ** degree / (1 + self.q)
        self.spectral_comparator_error = (self.delta * self.G ** 2 /
            chebyshev(degree, (2 + self.q) / self.q)) if self.q else F(0)
        self.bernstein_bias = self.delta ** 2 * self.kappa * self.G ** 2 / degree
        self.intervals, self.midpoints, self.radii = [], [], []
        self.bernstein_coefficients = None
        self.transform_cost = None

    def ingest(self, intervals):
        assert not self.intervals and len(intervals) == len(self.nodes)
        for lo, hi in intervals:
            assert lo <= hi
            self.intervals.append((lo, hi))
            self.midpoints.append((lo + hi) / 2)
            self.radii.append((hi - lo) / 2)
        return self

    def acquire(self, oracle):
        return self.ingest([oracle.call(u) for u in self.nodes])

    def uniform_bounds(self):
        assert self.radii
        eps = max(self.radii)
        noise = self.lebesgue_upper * eps
        taylor_bias = (self.lebesgue_upper + 1) * self.taylor_remainder / 2
        spectral_bias = (self.lebesgue_upper + 1) * self.spectral_comparator_error
        return {
            'node_error_max': eps,
            'noise_amplification_upper': self.lebesgue_upper,
            'interpolation_noise_bound': noise,
            'taylor_bias_bound': taylor_bias,
            'spectral_bias_bound': spectral_bias,
            'interpolation_uniform_error': noise + min(taylor_bias, spectral_bias),
            'bernstein_centered_uniform_error': eps + self.bernstein_bias / 2,
            'bernstein_one_sided_bias': self.bernstein_bias,
        }

    def predict(self, u):
        assert self.intervals
        lambdas = barycentric(u, self.delta)
        weights = lagrange_weights(self.alphas, lambdas, self.k)
        positive = bernstein_weights(self.alphas, lambdas, self.k)
        assert sum(weights) == 1 and sum(positive) == 1 and all(w >= 0 for w in positive)
        lebesgue = sum(abs(w) for w in weights)
        assert lebesgue <= self.lebesgue_upper
        estimate = sum(w * y for w, y in zip(weights, self.midpoints))
        noise = sum(abs(w) * e for w, e in zip(weights, self.radii))
        bias = min((lebesgue + 1) * self.taylor_remainder / 2,
                   (lebesgue + 1) * self.spectral_comparator_error)
        radius = noise + bias
        b_estimate = sum(w * y for w, y in zip(positive, self.midpoints))
        b_noise = sum(w * e for w, e in zip(positive, self.radii))
        interpolation_interval = (estimate - radius, estimate + radius)
        bernstein_interval = (b_estimate - b_noise, b_estimate + b_noise + self.bernstein_bias)
        intersection = (max(interpolation_interval[0], bernstein_interval[0]),
                        min(interpolation_interval[1], bernstein_interval[1]))
        assert intersection[0] <= intersection[1]
        return {'estimate': estimate, 'lebesgue_at_query': lebesgue,
                'noise_radius_at_query': noise, 'model_bias_radius_at_query': bias,
                'interpolation_interval': interpolation_interval,
                'bernstein_estimate': b_estimate, 'bernstein_interval': bernstein_interval,
                'intersection_interval': intersection}

    def transform(self):
        self.bernstein_coefficients, self.transform_cost = nodal_to_bernstein(
            self.alphas, self.midpoints, self.k)
        return self

    def task_certificate(self, prices, candidate=None):
        """Value-only all-simplex certificate; no hidden gradient or extra reaction.

        The candidate defaults to the best acquired lower-value node. A caller
        can propose any legal candidate using separately recorded arithmetic.
        """
        assert len(prices) == self.n
        costs = [sum(c * u for c, u in zip(prices, node)) for node in self.nodes]
        best = max(range(len(self.nodes)), key=lambda i: self.intervals[i][0] - costs[i])
        if candidate is None:
            candidate = self.nodes[best]
            lower = self.intervals[best][0] - costs[best]
        else:
            lower = self.predict(candidate)['intersection_interval'][0] - sum(c * u for c, u in zip(prices, candidate))
        positive_upper = max(iv[1] - c for iv, c in zip(self.intervals, costs)) + self.bernstein_bias
        if self.bernstein_coefficients is None:
            self.transform()
        E = self.uniform_bounds()['interpolation_uniform_error']
        coefficient_upper = max(b - c for b, c in zip(self.bernstein_coefficients, costs)) + E
        upper = min(positive_upper, coefficient_upper)
        return {'candidate': candidate, 'candidate_lower_reward_without_baseline': lower,
                'positive_bernstein_global_upper': positive_upper,
                'interpolant_coefficient_global_upper': coefficient_upper,
                'global_upper_reward_without_baseline': upper,
                'continuous_simplex_regret': max(F(0), upper - lower),
                'extra_source_readings': 0,
                'scope': 'Full continuous simplex; coefficient maxima and interval lower bound, no convergence assumption.'}

    def ideal_costs(self):
        count = comb(self.n + self.k, self.k)
        return {'source_reaction_readings': count,
                'requested_nonzero_setting_writes': self.n * comb(self.n + self.k - 1, self.k - 1),
                'resets': count, 'maximum_active_controls': min(self.n, self.k),
                'maximum_dose': self.delta,
                'total_requested_dose': count * self.delta * self.n / (self.n + 1),
                'stored_coefficients': count,
                'calibration_readings': 'Added by the physical oracle; not included here.',
                'timing_scope': 'Each reaction pays preparation, settling, integration, reset; duration and energy unacquired.'}
