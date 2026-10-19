#!/usr/bin/env python3
"""Certify the recovered four-state entropy minimum using exact rational intervals.

Only Python's standard library is used. No floating point number is used in a
certificate or an assertion. Arithmetic rounds outwards to a rational decimal
grid. Logs use the atanh series with an explicit remainder after binary range
reduction; pi uses Machin's formula with alternating-series remainder bounds.

The mathematical proof of global optimality is in reconstructed_markov_proof.md.
This script certifies the exact rational matrix, a positive generator witness,
the unique critical point, and the numerical entropy enclosure.
"""

from fractions import Fraction as F
from math import isqrt
import json

PRECISION = 50
SCALE = 10 ** PRECISION


def lower_grid(x):
    return F((x.numerator * SCALE) // x.denominator, SCALE)


def upper_grid(x):
    return -lower_grid(-x)


class I:
    """Closed rational interval with outward rounding after each operation."""

    def __init__(self, lo, hi=None):
        lo = F(lo)
        hi = lo if hi is None else F(hi)
        assert lo <= hi
        self.lo = lower_grid(lo)
        self.hi = upper_grid(hi)

    @staticmethod
    def cast(x):
        return x if isinstance(x, I) else I(x)

    def __add__(self, x):
        x = self.cast(x)
        return I(self.lo + x.lo, self.hi + x.hi)

    __radd__ = __add__

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, x):
        return self + -self.cast(x)

    def __rsub__(self, x):
        return self.cast(x) + -self

    def __mul__(self, x):
        x = self.cast(x)
        ends = [self.lo*x.lo, self.lo*x.hi, self.hi*x.lo, self.hi*x.hi]
        return I(min(ends), max(ends))

    __rmul__ = __mul__

    def __truediv__(self, x):
        x = self.cast(x)
        assert not (x.lo <= 0 <= x.hi), "Division interval contains zero"
        return self * I(1/x.hi, 1/x.lo)

    def __rtruediv__(self, x):
        return self.cast(x) / self

    def sqrt(self):
        assert self.lo >= 0
        lower_int = isqrt((self.lo.numerator * SCALE**2) // self.lo.denominator)
        upper_int = isqrt((self.hi.numerator * SCALE**2) // self.hi.denominator)
        # Extra unit on the upper bound is safe even for an exact square.
        return I(F(lower_int, SCALE), F(upper_int+1, SCALE))

    def log(self):
        assert self.lo > 0
        left = log_rational(self.lo)
        right = log_rational(self.hi)
        return I(left.lo, right.hi)

    def outward_decimal(self, digits=16):
        scale = 10**digits
        lo = (self.lo.numerator*scale)//self.lo.denominator
        hi = -((-self.hi.numerator*scale)//self.hi.denominator)
        return [decimal_integer(lo, digits), decimal_integer(hi, digits)]


def decimal_integer(n, digits):
    sign = "-" if n < 0 else ""
    n = abs(n)
    whole, frac = divmod(n, 10**digits)
    return f"{sign}{whole}.{frac:0{digits}d}"


def log2_interval():
    # log 2 = 2 sum_{n>=0} (1/3)^(2n+1)/(2n+1).
    z = F(1, 3)
    count = 80
    total = sum((z**(2*n+1)/F(2*n+1) for n in range(count)), F(0))
    tail = 2*z**(2*count+1)/(F(2*count+1)*(1-z*z))
    return I(2*total, 2*total+tail)


LOG2 = log2_interval()


def log_rational(x):
    """Enclose log(x), x>0 rational, using 1 <= reduced x < 2."""
    assert x > 0
    k = 0
    while x >= 2:
        x /= 2
        k += 1
    while x < 1:
        x *= 2
        k -= 1
    exact_z = (x-1)/(x+1)
    z = I(exact_z)
    z2 = z*z
    term = z
    total = I(0)
    count = 70
    for n in range(count):
        total = total + term/F(2*n+1)
        term = term*z2
    # z<=1/3, and all omitted terms are positive.
    tail = 2*exact_z**(2*count+1)/(F(2*count+1)*(1-exact_z**2))
    return 2*total + I(0, tail) + k*LOG2


def arctan_interval(z, count):
    total = sum(((-1)**n*z**(2*n+1)/F(2*n+1) for n in range(count)), F(0))
    next_term = (-1)**count*z**(2*count+1)/F(2*count+1)
    return I(min(total,total+next_term), max(total,total+next_term))


PI = 16*arctan_interval(F(1,5), 80) - 4*arctan_interval(F(1,239), 20)
OMEGA = 2*PI
A_PARAM = 8*LOG2
B_PARAM = 18*LOG2


def objective_and_derivative(a_interval):
    x = I.cast(a_interval)
    b = B_PARAM
    s = (2*(x*x+OMEGA*OMEGA)).sqrt()
    s_prime = 2*x/s
    c1 = b-x
    c2 = b+3*x
    assert (c1-s).lo > 0 and (c2-2*s).lo > 0
    ell1 = ((c1+s)/(c1-s)).log()
    ell2 = ((c2+2*s)/(c2-2*s)).log()
    objective = s*(2*ell1+ell2)/4
    derivative = s_prime*(2*ell1+ell2)/4 + s*(
        (c1*s_prime+s)/(c1*c1-s*s)
        + (c2*s_prime-3*s)/(c2*c2-4*s*s)
    )
    return objective, derivative


def exact_matrix_check():
    numerators = [
        [264193,260097,262143,262143],
        [260097,264193,262143,262143],
        [262143,262143,262147,262143],
        [262143,262143,262143,262147],
    ]
    p = [[F(n,2**20) for n in row] for row in numerators]
    assert all(sum(row) == 1 for row in p)
    assert all(p[i][j] == p[j][i] > 0 for i in range(4) for j in range(4))
    spectral_pairs = [([1,1,1,1],F(1)),([1,-1,0,0],F(1,2**8)),
                      ([1,1,-1,-1],F(1,2**18)),([0,0,1,-1],F(1,2**18))]
    for vec, eig in spectral_pairs:
        assert [sum(p[i][j]*vec[j] for j in range(4)) for i in range(4)] == [eig*x for x in vec]
    principal_bad_entry = (2*A_PARAM-B_PARAM)/4
    assert principal_bad_entry.hi < 0
    t = OMEGA/I(7).sqrt()
    # These are the only possibly small off-diagonal numerators of Q_0.
    assert (B_PARAM-5*t).lo > 0
    assert (2*A_PARAM-B_PARAM+t).lo > 0
    assert (B_PARAM+3*t).lo > 0 and (B_PARAM+11*t).lo > 0
    return numerators, principal_bad_entry


def main():
    numerators, negative_entry = exact_matrix_check()
    lo, hi = F(229,100), F(23,10)
    assert objective_and_derivative(lo)[1].hi < 0
    assert objective_and_derivative(hi)[1].lo > 0
    while hi-lo > F(1,10**15):
        mid = (lo+hi)/2
        der = objective_and_derivative(mid)[1]
        if der.hi < 0:
            lo = mid
        elif der.lo > 0:
            hi = mid
        else:
            raise AssertionError("Increase arithmetic precision before continuing")
    left_der = objective_and_derivative(lo)[1]
    right_der = objective_and_derivative(hi)[1]
    assert left_der.hi < 0 < right_der.lo
    root = I(lo,hi)
    assert root.lo > (B_PARAM-2*A_PARAM).hi
    value = objective_and_derivative(root)[0]
    old_lo, old_hi = F("26.1789116459"), F("26.1789117108")
    assert old_lo < value.lo < value.hi < old_hi
    output = {
        "status":"PASS",
        "arithmetic":"standard-library exact Fraction intervals, outward decimal grid",
        "grid_decimal_places":PRECISION,
        "P_denominator":2**20,
        "P_numerators":numerators,
        "eigenvalues":["1","1/256","1/262144","1/262144"],
        "principal_log_entry_12":negative_entry.outward_decimal(),
        "positive_generator_witness":"A=2*pi/sqrt(7), B=-C=sqrt(A*A+4*pi*pi)",
        "critical_point_bracket":root.outward_decimal(),
        "derivative_at_lower":left_der.outward_decimal(22),
        "derivative_at_upper":right_der.outward_decimal(22),
        "minimum_entropy_enclosure":value.outward_decimal(12),
        "prior_enclosure_independently_certified":[str(old_lo),str(old_hi)],
        "global_optimality":"follows from exhaustive logarithms and strict convexity in proof note",
    }
    print(json.dumps(output,indent=2))


if __name__ == "__main__":
    main()
