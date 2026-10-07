"""Independent random-bipartition control for the arbitrary-F low-k gate.

This is elementary color coding plus rectangular Cauchy-Binet. It uses no
Pfaffian norm identity or Boolean hypercontractivity. The shared exact-bit
mean/categorical compiler is owned by c01_s03 and accepts the supplied range
bound. Its conservative exponential prefactor is 4^k rather than central
binomial. Priority of this straightforward control is UNKNOWN.
"""
from math import comb, factorial
from low_sector_sampler import LowSector, ZERO, add, mul, conj, scale, matmul


def rectangular_minor_coefficient(g, rows, cols, k, row_scale, col_scale, stats=None):
    """Sum of all k-row/k-column squared minors of the scaled rectangle."""
    n = len(rows)
    if k == 0:
        return 1
    if min(n, len(cols)) < k:
        return 0
    m = [[scale(g[i][j], row_scale[i]*col_scale[j]) for j in cols] for i in rows]
    gram = [[ZERO for _ in rows] for _ in rows]
    for i in range(n):
        for j in range(n):
            value = ZERO
            for h in range(len(cols)):
                value = add(value, mul(m[i][h], conj(m[j][h])))
            gram[i][j] = value
    power, traces = gram, [0]
    for j in range(1, k+1):
        check_imaginary = sum(power[i][i][1] for i in range(n))
        assert check_imaginary == 0
        traces.append(sum(power[i][i][0] for i in range(n)))
        if j != k:
            power = matmul(power, gram)
    q = [1]
    for degree in range(1, k+1):
        numerator = sum((-1)**(j-1)*traces[j]*q[degree-j] for j in range(1, degree+1))
        assert numerator % degree == 0
        q.append(numerator//degree)
        assert q[-1] >= 0
    if stats is not None:
        stats['rectangular_coefficient_calls'] = stats.get('rectangular_coefficient_calls', 0) + 1
    return q[k]


class ColorSector(LowSector):
    def range_multiplier(self, k, a, b):
        if k == 0:
            return 1
        # With no forced spins, count both complementary orientations.
        if a == b == 0:
            return 1 << (2*k-1)
        return 1 << (2*k-a-b)

    def _forced_rectangle(self, k, rows, cols, up, down):
        a, b = len(up), len(down)
        if min(len(rows), len(cols)) < k:
            return 0
        value = 0
        for z in range(2*a+1):
            rs = [z if i in up else 1 for i in range(self.n)]
            for w in range(2*b+1):
                cs = [w if i in down else 1 for i in range(self.n)]
                coefficient = rectangular_minor_coefficient(self.g, rows, cols, k, rs, cs, self.stats)
                value += (-1)**(2*a-z+2*b-w)*comb(2*a,z)*comb(2*b,w)*coefficient
        divisor = factorial(2*a)*factorial(2*b)
        assert value % divisor == 0
        value //= divisor
        assert value >= 0
        return value

    def prefix_draw_integer(self, k, signs, up=(), down=(), empty=()):
        up, down, empty = self._restrictions(k, up, down, empty)
        a, b = len(up), len(down)
        if a > k or b > k or 2*k > self.n-len(empty):
            return 0
        free = set(range(self.n))-up-down-empty
        if len(signs) != self.n or any(signs[i] not in (-1,1) for i in free):
            raise ValueError('one Rademacher side bit per free site required')
        if k == 0:
            return 1
        left = sorted(set(up) | {i for i in free if signs[i] == 1})
        right = sorted(set(down) | {i for i in free if signs[i] == -1})
        subtotal = self._forced_rectangle(k, left, right, up, down)
        if a == b == 0:
            subtotal += self._forced_rectangle(k, right, left, up, down)
        return self.range_multiplier(k, a, b)*subtotal
