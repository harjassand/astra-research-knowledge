"""Exact rational finite-block coherent-information certificates.

Python standard library only.  This is a finite-block evaluator, not a
terminating evaluator of regularized quantum capacity.  Run this file for
small identity/dephasing/erasure fixtures.  The full net routine is deliberately
not run: its stated exhaustive cost is part of the mathematical construction.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from math import isqrt


@dataclass(frozen=True)
class Q:
    re: F = F(0)
    im: F = F(0)

    @staticmethod
    def of(z):
        return z if isinstance(z, Q) else Q(F(z))

    def __add__(self, z):
        z = Q.of(z)
        return Q(self.re + z.re, self.im + z.im)

    __radd__ = __add__

    def __neg__(self):
        return Q(-self.re, -self.im)

    def __sub__(self, z):
        return self + (-Q.of(z))

    def __rsub__(self, z):
        return Q.of(z) + (-self)

    def __mul__(self, z):
        z = Q.of(z)
        return Q(self.re * z.re - self.im * z.im,
                 self.re * z.im + self.im * z.re)

    __rmul__ = __mul__

    def __truediv__(self, z):
        z = Q.of(z)
        norm = z.re * z.re + z.im * z.im
        return Q((self.re * z.re + self.im * z.im) / norm,
                 (self.im * z.re - self.re * z.im) / norm)

    def conj(self):
        return Q(self.re, -self.im)


def zeros(n, m=None):
    return [[Q() for _ in range(n if m is None else m)] for _ in range(n)]


def identity(n):
    z = zeros(n)
    for i in range(n):
        z[i][i] = Q(F(1))
    return z


def mm(a, b):
    """Exact matrix product, omitting identically zero summands."""
    z = zeros(len(a), len(b[0]))
    for i in range(len(a)):
        for k in range(len(b)):
            if a[i][k] == Q():
                continue
            for j in range(len(b[0])):
                if b[k][j] != Q():
                    z[i][j] = z[i][j] + a[i][k] * b[k][j]
    return z


def trace(a):
    return sum((a[i][i] for i in range(len(a))), Q())


def ln2_interval(target=F(1, 10**12)):
    """artanh(1/3) series, with an exact rational tail enclosure."""
    z = F(0)
    k = 0
    while True:
        z += F(2, (2 * k + 1) * 3 ** (2 * k + 1))
        k += 1
        tail = F(9, 4 * (2 * k + 1) * 3 ** (2 * k + 1))
        if tail <= target:
            return z, z + tail


def entropy_interval(sigma, m=128, ln_target=F(1, 10**12)):
    """Certified entropy in bits, for a promised rational density matrix.

    P_m = sum_{k=1}^m Tr[sigma (I-sigma)^k]/k.
    0 <= S_nats(sigma)-P_m <= dimension/(m+1).
    """
    dim = len(sigma)
    one_minus = [[(Q(F(1)) if i == j else Q()) - sigma[i][j]
                  for j in range(dim)] for i in range(dim)]
    power_times_sigma = sigma
    poly = F(0)
    for k in range(1, m + 1):
        power_times_sigma = mm(power_times_sigma, one_minus)
        tr = trace(power_times_sigma)
        assert tr.im == 0
        poly += tr.re / k
    assert poly >= 0
    ell, upper_ell = ln2_interval(ln_target)
    return poly / upper_ell, (poly + F(dim, m + 1)) / ell


def output_on_gram(j, a, b, p):
    """Return B and RB for the input rho=P P*/Tr(P P*).

    J is normalized and ordered (input, output).  P has a rows; its columns
    label R.  Every calculation is rational, including the purification's
    density matrix.  No complementary channel or matrix square root is needed.
    """
    reference_dim = len(p[0])
    norm = sum((z.re*z.re + z.im*z.im for row in p for z in row), F(0))
    if norm == 0:
        raise ValueError("zero Gram factor")
    rb = zeros(reference_dim * b)
    for r in range(reference_dim):
        for s in range(reference_dim):
            for u in range(b):
                for v in range(b):
                    value = Q()
                    for i in range(a):
                        if p[i][r] == Q():
                            continue
                        for k in range(a):
                            if p[k][s] != Q():
                                value += p[i][r] * p[k][s].conj() * j[i*b+u][k*b+v]
                    rb[r*b+u][s*b+v] = value * a / norm
    bout = zeros(b)
    for u in range(b):
        for v in range(b):
            bout[u][v] = sum((rb[r*b+u][r*b+v] for r in range(reference_dim)), Q())
    assert trace(rb) == Q(F(1))
    assert trace(bout) == Q(F(1))
    return bout, rb


def gram_ic_interval(j, a, b, p, m=128, ln_target=F(1, 10**12)):
    bout, rb = output_on_gram(j, a, b, p)
    lb, ub = entropy_interval(bout, m, ln_target)
    lx, ux = entropy_interval(rb, m, ln_target)
    return lb - ux, ub - lx


def digits(number, base, n):
    out = [0] * n
    for i in range(n - 1, -1, -1):
        out[i] = number % base
        number //= base
    return out


def tensor_choi(j, a, b, n):
    """Normalized Choi of N**n, with input/output factors regrouped."""
    aa, bb = a**n, b**n
    da = [digits(i, a, n) for i in range(aa)]
    db = [digits(i, b, n) for i in range(bb)]
    out = zeros(aa * bb)
    for i in range(aa):
        for k in range(aa):
            for u in range(bb):
                for v in range(bb):
                    z = Q(F(1))
                    for t in range(n):
                        z *= j[da[i][t]*b+db[u][t]][da[k][t]*b+db[v][t]]
                    out[i*bb+u][k*bb+v] = z
    return out


def ceil_fraction(x):
    return -((-x.numerator) // x.denominator)


def ceil_log2(n):
    return (n - 1).bit_length()


def net_parameters(a, b, n, epsilon):
    """Conservative, explicitly computable parameters for a complete net.

    Returned interval width is <= epsilon for q_n=max Ic/n.
    The net includes (2H+1)**(2*d*d)-1 integer Gram factors.
    """
    epsilon = F(epsilon)
    if epsilon <= 0 or a < 1 or b < 1 or n < 1:
        raise ValueError("invalid dimensions/accuracy")
    d, bout_dim = a**n, b**n
    c = ceil_log2(a) + 2 * ceil_log2(b)
    u = min(F(1, 4), epsilon / (16 * (c + 8)))
    tau = u*u
    h = ceil_fraction(F(2*d) / tau)
    eta = n * epsilon / 8
    max_output_dim = d * bout_dim
    m = max(1, ceil_fraction(F(8*max_output_dim) / eta))
    ln_target = eta / (16*max_output_dim)
    return {"d": d, "bout_dim": bout_dim, "H": h, "m": m,
            "ln_target": ln_target, "net_margin_per_use": u*(c+8),
            "net_cardinality_upper": (2*h+1)**(2*d*d)-1}


def finite_block_interval(j, a, b, n, epsilon):
    """Total exhaustive evaluator of q_n; double-exponential-sized at best.

    This routine is a literal implementation of the proof, without an
    external optimization oracle.  It is not run in the fixture suite.
    """
    params = net_parameters(a, b, n, epsilon)
    d, bb, h = params["d"], params["bout_dim"], params["H"]
    block_j = tensor_choi(j, a, b, n)
    lower, upper = None, None
    for coeffs in product(range(-h, h+1), repeat=2*d*d):
        if not any(coeffs):
            continue
        p = [[Q(F(coeffs[2*(i*d+r)]), F(coeffs[2*(i*d+r)+1]))
              for r in range(d)] for i in range(d)]
        lo, hi = gram_ic_interval(block_j, d, bb, p,
                                 params["m"], params["ln_target"])
        lo, hi = lo/n, hi/n
        lower = lo if lower is None else max(lower, lo)
        upper = hi if upper is None else max(upper, hi)
    lower = max(F(0), lower)
    upper = max(F(0), upper) + params["net_margin_per_use"]
    assert upper - lower <= epsilon
    return lower, upper


def identity_choi(a):
    j = zeros(a*a)
    for i in range(a):
        for k in range(a):
            j[i*a+i][k*a+k] = Q(F(1, a))
    return j


def dephasing_choi(a):
    j = zeros(a*a)
    for i in range(a):
        j[i*a+i][i*a+i] = Q(F(1, a))
    return j


def erasure_choi(a, p):
    p = F(p)
    b = a+1
    j = zeros(a*b)
    for i in range(a):
        for k in range(a):
            j[i*b+i][k*b+k] = Q((1-p)/a)
        j[i*b+a][i*b+a] = Q(p/a)
    return j


def fixtures():
    gram = identity(2)
    cases = [
        ("qubit identity, maximally mixed", identity_choi(2), 2, F(1)),
        ("qubit dephasing, maximally mixed", dephasing_choi(2), 2, F(0)),
        ("qubit half erasure, maximally mixed", erasure_choi(2, F(1,2)), 3, F(0)),
        ("qubit quarter erasure, maximally mixed", erasure_choi(2, F(1,4)), 3, F(1,2)),
        ("qubit full erasure, maximally mixed", erasure_choi(2, F(1)), 3, F(-1)),
    ]
    for title, j, b, exact in cases:
        lo, hi = gram_ic_interval(j, 2, b, gram, m=128)
        assert lo <= exact <= hi
        print(f"{title}: [{float(lo):.10f}, {float(hi):.10f}], exact {exact}")
    j2 = tensor_choi(identity_choi(2), 2, 2, 2)
    assert j2 == identity_choi(4)
    print("Tensor normalization/regrouping: exact equality passed.")
    # A nonreal Gram factor verifies that conjugation is preserved exactly.
    p = [[Q(F(1)), Q(F(0), F(1))], [Q(F(1)), Q(F(1))]]
    bout, rb = output_on_gram(identity_choi(2), 2, 2, p)
    assert trace(mm(rb, rb)) == Q(F(1))
    assert all(rb[i][k] == rb[k][i].conj() for i in range(4) for k in range(4))
    print("Complex Gram purification: exact trace, purity, Hermiticity passed.")
    p = net_parameters(2, 2, 1, F(1,4))
    print("Full epsilon=1/4 one-use net parameters (not executed):")
    print(f"H={p['H']}; entropy series m={p['m']}; "
          f"net count has {len(str(p['net_cardinality_upper']))} decimal digits.")


if __name__ == "__main__":
    fixtures()
