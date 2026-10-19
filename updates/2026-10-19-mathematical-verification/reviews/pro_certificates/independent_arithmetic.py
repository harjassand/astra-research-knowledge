#!/usr/bin/env python3
"""Independent arithmetic audit, with no imports from the archived package.

Rigorous part: integer endpoints on a dyadic grid, exact polynomial comparisons,
and explicit series tail bounds. Diagnostic part: Decimal elementary functions
and a direct matrix exponential; those diagnostics are explicitly uncertified.
This file was written before reading archived verification outputs.
"""
from decimal import Decimal, localcontext
from fractions import Fraction
from math import isqrt
from pathlib import Path
import json
import random
import time

HERE = Path(__file__).resolve().parent
BITS = 256
UNIT = 1 << BITS

def ceildiv(a, b):
    return -((-a) // b)

class Box:
    """Integer interval endpoints in units of 2**-BITS, independently implemented."""
    __slots__ = ("l", "u")

    def __init__(self, lower, upper):
        assert isinstance(lower, int) and isinstance(upper, int) and lower <= upper
        self.l, self.u = lower, upper

    @classmethod
    def exact(cls, x):
        f = Fraction(x)
        return cls(f.numerator * UNIT // f.denominator,
                   ceildiv(f.numerator * UNIT, f.denominator))

    @classmethod
    def hull(cls, l, u):
        return cls(cls.exact(l).l, cls.exact(u).u)

    def __add__(self, x):
        x = asbox(x)
        return Box(self.l + x.l, self.u + x.u)

    __radd__ = __add__

    def __neg__(self):
        return Box(-self.u, -self.l)

    def __sub__(self, x):
        return self + -asbox(x)

    def __rsub__(self, x):
        return asbox(x) + -self

    def __mul__(self, x):
        x = asbox(x)
        candidates = [self.l*x.l, self.l*x.u, self.u*x.l, self.u*x.u]
        return Box(min(candidates) // UNIT, ceildiv(max(candidates), UNIT))

    __rmul__ = __mul__

    def reciprocal(self):
        assert self.l > 0 or self.u < 0
        return Box(UNIT*UNIT // self.u, ceildiv(UNIT*UNIT, self.l))

    def __truediv__(self, x):
        return self * asbox(x).reciprocal()

    def __rtruediv__(self, x):
        return asbox(x) / self

    def sqrt(self):
        assert self.l >= 0
        lower = isqrt(self.l * UNIT)
        upper = isqrt(self.u * UNIT)
        if upper*upper < self.u*UNIT:
            upper += 1
        assert lower*lower <= self.l*UNIT
        assert upper*upper >= self.u*UNIT
        return Box(lower, upper)

    def ln(self):
        assert self.l > 0
        return Box(log_endpoint(self.l).l, log_endpoint(self.u).u)

    def contains(self, f):
        f = Fraction(f)
        return self.l*f.denominator <= f.numerator*UNIT <= self.u*f.denominator

    def fractions(self):
        return Fraction(self.l, UNIT), Fraction(self.u, UNIT)

    def decimal(self, digits=40):
        q = 10**digits
        def fmt(x):
            sign = "-" if x < 0 else ""
            whole, frac = divmod(abs(x), q)
            return f"{sign}{whole}.{frac:0{digits}d}"
        return [fmt(self.l*q // UNIT), fmt(ceildiv(self.u*q, UNIT))]

def asbox(x):
    return x if isinstance(x, Box) else Box.exact(x)

def log_endpoint(integer):
    """ln(integer/UNIT): exact binary scaling + 96 terms of a dyadic enclosure.

    For 1 <= r < 2, z=(r-1)/(r+1) lies in [0,1/3). The remainder of
    2*sum(z**(2n+1)/(2n+1), n=0..N-1) is <=
    (9/4)*3**(-(2N+1))/(2N+1). We use that uniform rational bound,
    independent of the accumulated interval's dependency/rounding.
    """
    assert integer > 0
    r = Fraction(integer, UNIT)
    k = r.numerator.bit_length() - r.denominator.bit_length()
    r /= Fraction(2)**k
    if r < 1:
        r *= 2
        k -= 1
    if r >= 2:
        r /= 2
        k += 1
    assert 1 <= r < 2
    z = Box.exact((r-1)/(r+1))
    z2 = z*z
    power = z
    total = Box.exact(0)
    nterms = 96
    for n in range(nterms):
        total += power/(2*n+1)
        power *= z2
    tail = Fraction(9, 4*(2*nterms+1)*3**(2*nterms+1))
    local = 2*total + Box.hull(0, tail)
    if k:
        local += k*LOG_TWO
    return local

def exact_atanh_log2():
    n = 110
    z = Fraction(1, 3)
    s = 2*sum((z**(2*k+1)/(2*k+1) for k in range(n)), Fraction(0))
    t = 2*z**(2*n+1)/((2*n+1)*(1-z*z))
    return Box.hull(s, s+t), t

def alternate_atan(z, n):
    partial = sum(((-1)**k*z**(2*k+1)/(2*k+1) for k in range(n)), Fraction(0))
    next_term = (-1)**n*z**(2*n+1)/(2*n+1)
    return Box.hull(min(partial, partial+next_term), max(partial, partial+next_term)), abs(next_term)

LOG_TWO, LOG_TWO_TAIL = exact_atanh_log2()
# tan(atan(1/2)+atan(1/3))=1; both summands are positive and sum < pi/2.
# Thus this sum is pi/4. This differs from the source's Machin identity.
ATAN_HALF, PI_TAIL_HALF = alternate_atan(Fraction(1, 2), 150)
ATAN_THIRD, PI_TAIL_THIRD = alternate_atan(Fraction(1, 3), 110)
PI = 4*(ATAN_HALF + ATAN_THIRD)
OMEGA = 2*PI
A = 8*LOG_TWO
B = 18*LOG_TWO

def objective(a):
    a = asbox(a)
    s = (2*(a*a + OMEGA*OMEGA)).sqrt()
    c1, c2 = B-a, B+3*a
    assert (c1-s).l > 0 and (c2-2*s).l > 0
    # Split logarithms (rather than source's log of a quotient).
    l1 = (c1+s).ln() - (c1-s).ln()
    l2 = (c2+2*s).ln() - (c2-2*s).ln()
    value = s*(2*l1+l2)/4
    sp = 2*a/s
    # Differentiate split logarithms directly, with no source M7 code.
    l1p = (-1+sp)/(c1+s) - (-1-sp)/(c1-s)
    l2p = (3+2*sp)/(c2+2*s) - (3-2*sp)/(c2-2*s)
    derivative = (sp*(2*l1+l2) + s*(2*l1p+l2p))/4
    return value, derivative, {"c1_minus_s": c1-s, "c2_minus_2s": c2-2*s}

def arithmetic_self_checks():
    rng = random.Random(0x19C3A)
    tests = 0
    for _ in range(300):
        a, b = [Fraction(rng.randrange(-10000,10000),rng.randrange(1,500)) for _ in range(2)]
        ai, bi = Box.exact(a), Box.exact(b)
        assert (ai+bi).contains(a+b)
        assert (ai-bi).contains(a-b)
        assert (ai*bi).contains(a*b)
        tests += 3
        if b and not (bi.l <= 0 <= bi.u):
            assert (ai/bi).contains(a/b)
            tests += 1
        sq = Box.exact(abs(a)).sqrt()
        l,u = sq.fractions()
        assert l*l <= abs(a) <= u*u
        tests += 1
    # Monotone log known identities, with negative range-reduction exponents.
    for k in range(-30,31):
        interval = Box.exact(Fraction(2)**k).ln() - k*LOG_TWO
        assert interval.l <= 0 <= interval.u
        tests += 1
    return tests

def entropy_certificate():
    left, right = Fraction(229,100), Fraction(23,10)
    _,dl,_ = objective(left)
    _,dr,_ = objective(right)
    assert dl.u < 0 < dr.l
    initial = [dl.decimal(40),dr.decimal(40)]
    iterations = 0
    while right-left > Fraction(1,10**36):
        mid = (left+right)/2
        _,d,_ = objective(mid)
        assert d.u < 0 or d.l > 0
        if d.u < 0:
            left = mid
        else:
            right = mid
        iterations += 1
    value,_,margins = objective(Box.hull(left,right))
    _,dl,_ = objective(left)
    _,dr,_ = objective(right)
    assert dl.u < 0 < dr.l
    assert value.l > Box.exact("26.178911678346").u
    assert value.u < Box.exact("26.178911678347").l
    root = Box.hull(left,right)
    cut_margin = root - (B-2*A)
    assert cut_margin.l > 0
    t = OMEGA/Box.exact(7).sqrt()
    witness = {"b_minus_5t": B-5*t, "2a_minus_b_plus_t": 2*A-B+t,
               "b_plus_3t": B+3*t,"b_plus_11t": B+11*t}
    assert all(x.l > 0 for x in witness.values())
    aminus = -3*B + 2*Box.exact(2).sqrt()*(B*B+OMEGA*OMEGA).sqrt()
    aplus = -B + Box.exact(2).sqrt()*(B*B-OMEGA*OMEGA).sqrt()
    assert (root-aminus).l > 0 and (aplus-root).l > 0
    # Exact rational spectral matrix identity, independently rebuilt.
    nums = [[264193,260097,262143,262143],[260097,264193,262143,262143],
            [262143,262143,262147,262143],[262143,262143,262143,262147]]
    p = [[Fraction(x,2**20) for x in row] for row in nums]
    assert all(sum(row)==1 for row in p)
    assert all(p[i][j]==p[j][i] and p[i][j]>0 for i in range(4) for j in range(4))
    for v,e in [([1,1,1,1],Fraction(1)),([1,-1,0,0],Fraction(1,256)),
                ([1,1,-1,-1],Fraction(1,2**18)),([0,0,1,-1],Fraction(1,2**18))]:
        assert [sum(row[j]*v[j] for j in range(4)) for row in p] == [e*x for x in v]
    return {"label":"rigorous_exact_integer_dyadic_intervals",
            "root_interval": root.decimal(40), "root_exact_rational_endpoints":[str(left),str(right)],
            "initial_derivative_intervals": initial,"final_derivative_intervals":[dl.decimal(70),dr.decimal(70)],
            "bisection_iterations":iterations,"entropy_interval":value.decimal(40),
            "published_12_digit_strict_interval_proved":True,
            "root_above_constraint_margin":cut_margin.decimal(40),
            "scalar_feasible_open_interval":[aminus.decimal(40),aplus.decimal(40)],
            "optimizer_positive_rate_numerators":{k:v.decimal(40) for k,v in margins.items()},
            "Q0_positive_rate_numerators":{k:v.decimal(40) for k,v in witness.items()},
            "Q0_min_offdiagonal_lower_interval":(min(witness.values(),key=lambda x:x.l)/4).decimal(40),
            "principal_log_entry_12":((2*A-B)/4).decimal(40),
            "exact_rational_spectral_matrix_checks":True}, root

def nth_root_bracket(n, target, decimal_digits):
    # Decimal grid, different from the source's binary grid.
    scale = 10**decimal_digits
    value = target*scale**n
    assert value.denominator == 1
    low,high = 0,scale
    while high-low > 1:
        mid = (low+high)//2
        if Fraction(mid**n) < value:
            low = mid
        else:
            high = mid
    assert low**n < value < high**n
    return Fraction(low,scale),Fraction(high,scale)

def hidden_certificate():
    yl,yh = nth_root_bracket(64,Fraction(1,2),90)
    # Exact Fractions: no Box arithmetic here.
    ml,mh = (2*yl**8-1-yh**18)/4,(2*yh**8-1-yl**18)/4
    alpha, nu = Fraction(1,64),Fraction(1,2**18)
    c = nu/2
    factor = Fraction(2**38)*(c/64 + Fraction(63,16))
    cl,ch = factor*yl**19,factor*yh**19
    floorl,floorh = ml/(4*ch),mh/(4*cl)
    defectl,defecth = ml/(2**36*yh**18*(1-alpha)),mh/(2**36*yl**18*(1-alpha))
    assert 0 < ml < mh and 0 < cl < ch
    assert mh/cl < c
    assert defectl > Fraction("4.99e-14")
    assert floorl > Fraction("7.89e-16")
    # C = alpha*c**(alpha-1) + 4*(1-alpha)*c**(alpha-2).
    # Since c=2**-19 and y=2**(-1/64), c**alpha=y**19;
    # factorization is y**19/c**2 * (alpha*c+4*(1-alpha)).
    assert factor == (alpha*c+4*(1-alpha))/c**2
    # nu**(2-alpha)=2**-36/y**18, proved by exponent equality:
    assert -18*(2-alpha) == -36+Fraction(18,64)
    def show(l,u,d=60):
        return Box.hull(l,u).decimal(d)
    return {"label":"rigorous_exact_fraction_polynomial_root_isolation",
            "root_equation":"y^64=1/2, y>0", "root_decimal_grid_places":90,
            "root_exact_endpoints":[str(yl),str(yh)], "root_interval":show(yl,yh),
            "m_interval":show(ml,mh),"C_interval":show(cl,ch),
            "m_over_C_interval":show(ml/ch,mh/cl),"a0_over_2":str(c),
            "min_branch_is_m_over_C":True,"equilibrium_defect_interval":show(defectl,defecth),
            "hidden_sigma_interval":show(floorl,floorh),
            "strict_defect_above_4_99e_minus14":True,"strict_sigma_above_7_89e_minus16":True,
            "C_factorization_exactly_matches_theorem":True,"nu_power_identity_exact":True}

def decimal_diagnostics(root):
    with localcontext() as ctx:
        ctx.prec = 120
        D = Decimal
        # Gauss-Legendre pi, unrelated to either rational arctangent identity.
        ag,bg,t,p = D(1),D(1)/D(2).sqrt(),D(1)/4,D(1)
        for _ in range(9):
            an = (ag+bg)/2
            bg = (ag*bg).sqrt()
            t -= p*(ag-an)**2
            ag,p = an,2*p
        pi = (ag+bg)**2/(4*t)
        ln2 = D(2).ln()
        a,b,w = 8*ln2,18*ln2,2*pi
        def eval_dec(x):
            s = (2*(x*x+w*w)).sqrt()
            c1,c2 = b-x,b+3*x
            l1 = (c1+s).ln()-(c1-s).ln()
            l2 = (c2+2*s).ln()-(c2-2*s).ln()
            sp = 2*x/s
            d1 = (-1+sp)/(c1+s)-(-1-sp)/(c1-s)
            d2 = (3+2*sp)/(c2+2*s)-(3-2*sp)/(c2-2*s)
            return s*(2*l1+l2)/4,(sp*(2*l1+l2)+s*(2*d1+d2))/4
        lo,hi = D("2.29"),D("2.30")
        for _ in range(340):
            mid = (lo+hi)/2
            if eval_dec(mid)[1] < 0:
                lo = mid
            else:
                hi = mid
        x = (lo+hi)/2
        val = eval_dec(x)[0]
        rt2 = D(2).sqrt()
        v = [1/rt2,-1/rt2,D(0),D(0)]
        u = [D(1)/2,D(1)/2,-D(1)/2,-D(1)/2]
        ww = [D(0),D(0),1/rt2,-1/rt2]
        r = (x*x+w*w).sqrt()
        q = [[-a*v[i]*v[j]-b*(u[i]*u[j]+ww[i]*ww[j])
              +x*(u[i]*u[j]-ww[i]*ww[j])+r*u[i]*ww[j]-r*ww[i]*u[j]
              for j in range(4)] for i in range(4)]
        direct_entropy = sum(((q[i][j]-q[j][i])/4*(q[i][j]/q[j][i]).ln()
                              for i in range(4) for j in range(i+1,4)),D(0))
        def mm(a,b):
            return [[sum((a[i][k]*b[k][j] for k in range(4)),D(0))
                     for j in range(4)] for i in range(4)]
        ident = [[D(int(i==j)) for j in range(4)] for i in range(4)]
        # exp(Q/64) by Taylor, then six squarings.
        scaled = [[e/64 for e in row] for row in q]
        acc = [row[:] for row in ident]
        term = [row[:] for row in ident]
        for k in range(1,180):
            term = [[e/k for e in row] for row in mm(term,scaled)]
            acc = [[acc[i][j]+term[i][j] for j in range(4)] for i in range(4)]
        for _ in range(6):
            acc = mm(acc,acc)
        nums = [[264193,260097,262143,262143],[260097,264193,262143,262143],
                [262143,262143,262147,262143],[262143,262143,262143,262147]]
        matrix_error = max(abs(acc[i][j]-D(nums[i][j])/2**20) for i in range(4) for j in range(4))
        y = (-ln2/64).exp()
        m = (2*y**8-1-y**18)/4
        nu,c,alpha = D(2)**-18,D(2)**-19,D(1)/64
        const = alpha*c**(alpha-1)+4*(1-alpha)*c**(alpha-2)
        floor = m/(4*const)
        defect = m*nu**(2-alpha)/(1-alpha)
        root_l,root_u = [D(f.numerator)/D(f.denominator) for f in root.fractions()]
        return {"label":"UNCERTIFIED_high_precision_sanity_check",
                "decimal_precision":ctx.prec,"pi_Gauss_Legendre":str(pi),
                "optimizer":str(x),"optimizer_inside_exact_interval":root_l < x < root_u,
                "scalar_entropy":str(val),"direct_pairwise_entropy":str(direct_entropy),
                "scalar_vs_pairwise_difference":str(abs(val-direct_entropy)),
                "matrix_exponential_max_abs_error":str(matrix_error),
                "Q_row_sum_max_abs_error":str(max(abs(sum(row)) for row in q)),
                "Q_column_sum_max_abs_error":str(max(abs(sum(q[i][j] for i in range(4))) for j in range(4))),
                "Q_min_offdiagonal":str(min(q[i][j] for i in range(4) for j in range(4) if i!=j)),
                "hidden_m":str(m),"hidden_C_direct_real_power":str(const),
                "hidden_sigma_direct_real_power":str(floor),"equilibrium_defect_direct_real_power":str(defect)}

def main():
    start = time.monotonic()
    count = arithmetic_self_checks()
    entropy,root = entropy_certificate()
    hidden = hidden_certificate()
    diagnostic = decimal_diagnostics(root)
    out = {"status":"PASS","implementation":"independently written; source scripts never imported",
           "rigorous_grid":"dyadic 2^-256; exact integer outward rounding",
           "arithmetic_self_check_assertions":count,
           "rigorous_constants":{"pi":PI.decimal(70),"log2":LOG_TWO.decimal(70),
                                  "pi_method":"4*(atan(1/2)+atan(1/3)), alternating series",
                                  "atan_half_next_term_bound":str(PI_TAIL_HALF),
                                  "atan_third_next_term_bound":str(PI_TAIL_THIRD),
                                  "ln2_exact_tail_bound":str(LOG_TWO_TAIL)},
           "entropy":entropy,"hidden":hidden,"diagnostic":diagnostic,
           "wall_seconds":time.monotonic()-start}
    (HERE / "independent_arithmetic.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"status":out["status"],"wall_seconds":out["wall_seconds"],
                      "entropy":entropy["entropy_interval"],"optimizer":entropy["root_interval"],
                      "hidden_sigma":hidden["hidden_sigma_interval"],
                      "equilibrium_defect":hidden["equilibrium_defect_interval"],
                      "diagnostic_matrix_error":diagnostic["matrix_exponential_max_abs_error"]},indent=2))

if __name__ == "__main__":
    main()
