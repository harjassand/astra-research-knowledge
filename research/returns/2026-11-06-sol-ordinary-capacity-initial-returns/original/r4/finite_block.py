"""Exact-rational components of the ordinary quantum-capacity lower search.

This is NOT a terminating capacity evaluator.  finite_block_interval terminates
for every fixed block length, but its general exhaustive grid is enormous.
Only Python's standard library is used.  Choi matrices are normalized.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from math import ceil


@dataclass(frozen=True)
class G:
    """A Gaussian rational."""
    re: F = F(0)
    im: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, "re", F(self.re))
        object.__setattr__(self, "im", F(self.im))

    @staticmethod
    def coerce(x):
        return x if isinstance(x, G) else G(F(x))

    def __add__(self, y):
        y = G.coerce(y)
        return G(self.re + y.re, self.im + y.im)

    __radd__ = __add__

    def __neg__(self):
        return G(-self.re, -self.im)

    def __sub__(self, y):
        return self + (-G.coerce(y))

    def __rsub__(self, y):
        return G.coerce(y) + (-self)

    def __mul__(self, y):
        y = G.coerce(y)
        return G(self.re*y.re-self.im*y.im, self.re*y.im+self.im*y.re)

    __rmul__ = __mul__

    def __truediv__(self, y):
        y = G.coerce(y)
        t = y.re*y.re + y.im*y.im
        if not t:
            raise ZeroDivisionError
        return self*y.conj()*G(1/t)

    def conj(self):
        return G(self.re, -self.im)

    def abs2(self):
        return self.re*self.re + self.im*self.im


ZERO, ONE = G(), G(1)


def zeros(n, m=None):
    m = n if m is None else m
    return [[ZERO for _ in range(m)] for _ in range(n)]


def identity(n):
    out = zeros(n)
    for i in range(n):
        out[i][i] = ONE
    return out


def matmul(a, b):
    n, k, m = len(a), len(b), len(b[0])
    out = zeros(n, m)
    for i in range(n):
        for l in range(k):
            if a[i][l] == ZERO:
                continue
            for j in range(m):
                if b[l][j] != ZERO:
                    out[i][j] = out[i][j] + a[i][l]*b[l][j]
    return out


def trace(a):
    out = sum((a[i][i] for i in range(len(a))), ZERO)
    assert not out.im
    return out.re


def projector(v):
    v = [G.coerce(z) for z in v]
    norm2 = sum((z.abs2() for z in v), F(0))
    if not norm2:
        raise ValueError("Zero vector")
    return [[z*w.conj()/norm2 for w in v] for z in v]


def ln2_interval(width):
    """Certified rational bounds using ln 2 = 2 atanh(1/3)."""
    width = F(width)
    if width <= 0:
        raise ValueError("Positive width required")
    total, j = F(0), 0
    while True:
        total += F(2, (2*j+1)*3**(2*j+1))
        m = j+1
        tail = F(9, 4*(2*m+1)*3**(2*m+1))
        if tail <= width:
            return total, total+tail
        j += 1


def entropy_interval(rho, width=F(1, 64)):
    """Bounds S(rho), in bits, with interval width at most width.

    rho is promised PSD and trace one. No eigenvalue/eigenvector oracle is
    used.  -x ln x = sum_{k>=1} x(1-x)^k/k, with uniform remainder <=1/(L+1).
    """
    width = F(width)
    if width <= 0:
        raise ValueError("Positive width required")
    d = len(rho)
    assert trace(rho) == 1
    for i in range(d):
        for j in range(d):
            assert rho[i][j] == rho[j][i].conj()
    lo_log, hi_log = ln2_interval(width/F(8*d))
    L = max(1, ceil(F(4*d)/width)-1)
    complement = [[G(int(i == j))-rho[i][j] for j in range(d)] for i in range(d)]
    power = matmul(rho, complement)
    total = F(0)
    remainder = F(d, L+1)
    for k in range(1, L+1):
        if all(z == ZERO for row in power for z in row):
            remainder = F(0)
            break
        t = trace(power)
        assert t >= 0
        total += t/k
        if k != L:
            power = matmul(power, complement)
    out = total/hi_log, (total+remainder)/lo_log
    assert out[1]-out[0] <= width
    return out


def digits(x, base, count):
    out = [0]*count
    for i in range(count-1, -1, -1):
        out[i], x = x % base, x // base
    return out


def tensor_choi(J, a, b, n):
    """Grouped A^n B^n ordering, not the interleaved Kronecker ordering."""
    A, B = a**n, b**n
    da = [digits(i, a, n) for i in range(A)]
    db = [digits(i, b, n) for i in range(B)]
    out = zeros(A*B)
    for i, j, u, v in product(range(A), range(A), range(B), range(B)):
        t = ONE
        for k in range(n):
            t *= J[da[i][k]*b+db[u][k]][da[j][k]*b+db[v][k]]
        out[i*B+u][j*B+v] = t
    return out, A, B


def channel_outputs_from_purification(J, a, b, vector):
    """Return B and R B for the rational pure projector on R A, dim R=a."""
    if len(vector) != a*a:
        raise ValueError("Purification vector has wrong dimension")
    psi = projector(vector)
    rb, out_b = zeros(a*b), zeros(b)
    for r, s, u, v in product(range(a), range(a), range(b), range(b)):
        z = ZERO
        for i, j in product(range(a), repeat=2):
            z += psi[r*a+i][s*a+j]*a*J[i*b+u][j*b+v]
        rb[r*b+u][s*b+v] = z
        if r == s:
            out_b[u][v] += z
    assert trace(rb) == trace(out_b) == 1
    return out_b, rb


def coherent_information_interval(J, a, b, vector, width=F(1, 32)):
    out_b, rb = channel_outputs_from_purification(J, a, b, vector)
    lb, ub = entropy_interval(out_b, F(width)/2)
    lr, ur = entropy_interval(rb, F(width)/2)
    assert (ub-lb)+(ur-lr) <= width
    return lb-ur, ub-lr


def finite_block_interval(J, a, b, n, error=F(1, 8), max_points=None):
    """Certified interval for (1/n) max I_c, with width <=error.

    All promised channels are supported. max_points is only an operational
    guard: exceeding it raises, and never produces a certified answer.
    """
    error = F(error)
    if error <= 0 or n < 1:
        raise ValueError("Positive precision and block length required")
    if min(a, b) == 1:
        return F(0), F(0)
    Jn, A, B = tensor_choi(J, a, b, n)
    scale = max(2, ceil(F(32*(a+2*b+1))/error))
    delta = F(1, scale*scale)
    M = 2*A*scale*scale
    point_count = (2*M+1)**(2*A*A)-1
    if max_points is not None and point_count > max_points:
        raise RuntimeError(f"Exhaustive grid has {point_count} vectors")
    lower, upper = F(0), F(0)
    for coords in product(range(-M, M+1), repeat=2*A*A):
        if not any(coords):
            continue
        vector = [G(coords[2*i], coords[2*i+1]) for i in range(A*A)]
        l, u = coherent_information_interval(Jn, A, B, vector, n*error/4)
        lower, upper = max(lower, l/n), max(upper, u/n)
    # Fannes on B and RB; use the elementary h_2(delta)<=4 sqrt(delta).
    covering_error = delta*(a+2*b)+F(8, scale*n)
    answer = lower, upper+covering_error
    assert answer[1]-answer[0] <= error
    return answer


def choi_from_kraus(kraus):
    b, a = len(kraus[0]), len(kraus[0][0])
    out = zeros(a*b)
    for K in kraus:
        for i, j, u, v in product(range(a), range(a), range(b), range(b)):
            out[i*b+u][j*b+v] += G.coerce(K[u][i])*G.coerce(K[v][j]).conj()/a
    return out, a, b


def verify_normalized_choi(J, a, b):
    """Check the affine normalization; PSD follows from Kraus construction."""
    assert len(J) == a*b
    for i, j in product(range(a), repeat=2):
        assert sum((J[i*b+k][j*b+k] for k in range(b)), ZERO) == G(F(int(i == j), a))


def is_psd(matrix):
    """Exact Hermitian Schur-complement test, including singular matrices."""
    M = [[G.coerce(z) for z in row] for row in matrix]
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j] != M[j][i].conj():
                return False
    while M:
        if any(M[i][i].im or M[i][i].re < 0 for i in range(len(M))):
            return False
        pivots = [i for i in range(len(M)) if M[i][i].re > 0]
        if not pivots:
            return all(z == ZERO for row in M for z in row)
        p = pivots[0]
        rest = [i for i in range(len(M)) if i != p]
        pivot = M[p][p]
        M = [[M[i][j]-M[i][p]*M[p][j]/pivot for j in rest] for i in rest]
    return True


def affine_choi_projection(K, a, b):
    """Orthogonal affine projection onto Tr_B J=I_A/a."""
    defect = zeros(a)
    for i, j in product(range(a), repeat=2):
        defect[i][j] = sum((K[i*b+k][j*b+k] for k in range(b)), ZERO)-G(F(int(i == j), a))
    return [[K[i*b+u][j*b+v]-(defect[i][j]/b if u == v else ZERO)
             for j, v in product(range(a), range(b))]
            for i, u in product(range(a), range(b))]


def rational_channel_net(a, b, delta, max_points=None):
    """A finite full-diamond-norm delta-net of all a-to-b channels.

    Enumerate a rational Hermitian cube grid, project to the TP affine slice,
    and retain exactly its PSD points. This is valid on the boundary too.
    The proof and explicit mesh-size bound are in REPORT.txt.
    """
    delta = F(delta)
    if not 0 < delta <= 1:
        raise ValueError("delta must lie in (0,1]")
    D = a*b
    M = ceil(F(32*a*D*D)/delta)
    point_count = (2*M+1)**(D*D)
    if max_points is not None and point_count > max_points:
        raise RuntimeError(f"Channel net has {point_count} affine candidates")
    for params in product(range(-M, M+1), repeat=D*D):
        K, index = zeros(D), 0
        for i in range(D):
            K[i][i] = G(F(params[index], M))
            index += 1
        for i in range(D):
            for j in range(i+1, D):
                z = G(F(params[index], M), F(params[index+1], M))
                index += 2
                K[i][j], K[j][i] = z, z.conj()
        assert index == D*D
        J = affine_choi_projection(K, a, b)
        if is_psd(J):
            yield J


if __name__ == "__main__":
    raise SystemExit("Run check_interfaces.py. No full capacity evaluator is claimed.")
