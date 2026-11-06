"""Exact rational checks for the explicit response-sensitivity family.

Uses only Python's standard library. No sampled PDE solve is used.
The universal proof, including moment control for every T, is in
RESEARCH_REPORT.txt. This file computes enclosures for selected T values
and checks the rational numerical bounds used in the example.
"""
from fractions import Fraction as Q
from decimal import Decimal, localcontext
from pathlib import Path
import json

PRECISION = 1024

def floor_dyadic(x, bits):
    return Q((x.numerator << bits) // x.denominator, 1 << bits)

def ceil_dyadic(x, bits):
    n = x.numerator << bits
    return Q(-((-n) // x.denominator), 1 << bits)

def outward(lo, hi, bits=PRECISION):
    assert lo <= hi
    return floor_dyadic(lo, bits), ceil_dyadic(hi, bits)

def log2_interval(bits=PRECISION):
    # log 2 = 2 atanh(1/3); all terms positive.
    n = (bits + 12) // 3 + 2  # 9 > 2^3
    u = Q(1, 3)
    p = u
    total = Q(0)
    for k in range(n):
        total += p / (2*k + 1)
        p *= u*u
    tail = 2*p / ((2*n + 1)*(1-u*u))
    return outward(2*total, 2*total + tail, bits)

def atan_interval(denominator, bits=PRECISION):
    x = Q(1, denominator)
    power, sign, total, k = x, 1, Q(0), 0
    tolerance = Q(1, 1 << (bits+12))
    while True:
        term = sign*power/(2*k+1)
        new_total = total + term
        if abs(term) < tolerance:
            return outward(min(total, new_total), max(total, new_total), bits+8)
        total = new_total
        power *= x*x
        sign = -sign
        k += 1

def pi_interval(bits=PRECISION):
    # Machin's identity follows from the tangent addition formula:
    # pi = 16 atan(1/5) - 4 atan(1/239).
    a, b = atan_interval(5, bits), atan_interval(239, bits)
    return outward(16*a[0]-4*b[1], 16*a[1]-4*b[0], bits)

def exp_negative_point(x, bits=PRECISION):
    assert x >= 0
    y, squarings = x, 0
    while y > Q(1, 2):
        y /= 2
        squarings += 1
    workbits = bits + squarings + 16
    tolerance = Q(1, 1 << (workbits+4))
    total, term, k = Q(1), Q(1), 0
    while True:
        k += 1
        term = -term*y/k
        new_total = total+term
        if abs(term) < tolerance:
            lo, hi = min(total, new_total), max(total, new_total)
            break
        total = new_total
    lo, hi = outward(lo, hi, workbits)
    assert lo >= 0
    for _ in range(squarings):
        lo, hi = outward(lo*lo, hi*hi, workbits)
    return outward(lo, hi, bits)

def exp_negative_interval(lo, hi, bits=PRECISION):
    assert 0 <= lo <= hi
    return exp_negative_point(hi, bits)[0], exp_negative_point(lo, bits)[1]

def decimal_string(x, digits=14):
    with localcontext() as ctx:
        ctx.prec = digits
        return format(Decimal(x.numerator)/Decimal(x.denominator), ".10E")

def dyadic_interval(lo, hi, mantissa_bits=96):
    """Compact exact outward enclosure: mantissa * 2^binary_exponent."""
    assert 0 < lo <= hi
    k = hi.numerator.bit_length()-hi.denominator.bit_length()
    if hi < (Q(1 << k) if k >= 0 else Q(1, 1 << (-k))):
        k -= 1
    bits = max(0, mantissa_bits-k)
    low, high = floor_dyadic(lo, bits), ceil_dyadic(hi, bits)
    return {
        "lower_mantissa": str(low.numerator * ((1 << bits)//low.denominator)),
        "upper_mantissa": str(high.numerator * ((1 << bits)//high.denominator)),
        "binary_exponent": -bits,
        "display_lower_approximate": decimal_string(low),
        "display_upper_approximate": decimal_string(high),
    }

def main():
    ln2 = log2_interval()
    pi = pi_interval()
    exp_minus_one = exp_negative_point(Q(1))
    assert Q(0) < ln2[0] < ln2[1] < Q(1)
    assert Q(3) < pi[0] <= pi[1] < Q(22, 7)
    assert 1/exp_minus_one[0] < Q(3)
    moment_upper = Q(3)+Q(11, 32)*Q(22, 7)
    assert moment_upper == Q(457, 112) < Q(5)

    rows = []
    for t in (16, 64, 256):
        j = t.bit_length()-1
        assert 1 << j == t
        # v_T = pi/(4T) exp[-8 - (g(4)-g(T))],
        # g(T)=(log T+1)/T, with T a power of two.
        w_coefficient = Q(1, 2)-Q(j, t)
        w_constant = Q(1, 4)-Q(1, t)
        assert w_coefficient >= 0 and w_constant >= 0
        exponent_lo = Q(8)+w_constant+w_coefficient*ln2[0]
        exponent_hi = Q(8)+w_constant+w_coefficient*ln2[1]
        ev = exp_negative_interval(exponent_lo, exponent_hi)
        v = outward(pi[0]*ev[0]/(4*t), pi[1]*ev[1]/(4*t))
        er = exp_negative_point(Q(2*t))
        eta = outward(pi[0]*er[0]/16, pi[1]*er[1]/16)
        assert 0 < eta[0] <= eta[1] < v[0] < v[1] < 1
        gap_lower = v[0]/(2-v[0])
        gap_upper = v[1]
        assert eta[1] < gap_lower < gap_upper
        amplification_lower = gap_lower/eta[1]
        rows.append({
            "T": t,
            "coefficient_L1_error": dyadic_interval(*eta),
            "image_volume": dyadic_interval(*v),
            "effective_gap_enclosure": dyadic_interval(gap_lower, gap_upper),
            "minimum_worst_case_error_lower_bound": dyadic_interval(
                gap_lower/2, gap_lower/2),
            "gap_to_coefficient_error_ratio_lower_bound_approximate":
                decimal_string(amplification_lower),
            "interpretation":
                "Actual tensor gap lies between the stated lower and upper bounds; "
                "no exact effective tensor for the disk inclusion was assumed."
        })

    record = {
        "scope": "Exact rational enclosures for selected explicit family members. "
                 "The all-T and all-coefficient theorems are analytic, not inferred "
                 "from these checks.",
        "parameters": {"tau": "1", "M": "5", "T0": "4", "R": "1/4"},
        "uniform_moment_upper_bound": "457/112",
        "moment_bound_is_less_than_M": True,
        "calculation": "Rational power series with rigorous tails and outward "
                       "dyadic rounding; no elementary-function or PDE oracle.",
        "working_dyadic_bits": PRECISION,
        "rows": rows,
    }
    path = Path(__file__).with_name("FAMILY_BOUNDS.json")
    path.write_text(json.dumps(record, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({
        "verified": True,
        "uniform_moment_bound": str(moment_upper),
        "examples": [
            {"T": row["T"],
             "coefficient_error_approximate": row["coefficient_L1_error"]
                 ["display_upper_approximate"],
             "response_gap_lower_approximate": row["effective_gap_enclosure"]
                 ["display_lower_approximate"]}
            for row in rows],
        "output": str(path)
    }, indent=2))

if __name__ == "__main__":
    main()

