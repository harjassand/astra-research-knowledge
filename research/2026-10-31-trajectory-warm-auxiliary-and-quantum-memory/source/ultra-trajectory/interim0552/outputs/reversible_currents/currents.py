#!/usr/bin/env python3
"""One stationary binary record: a reversible-cover current certificate.

Only Python's standard library is required. All inferential decisions and the
returned logarithm enclosures use exact rational arithmetic. The theorem and
its assumptions are in PROOF.txt in this directory. In particular, stationary
hidden initialization and ordinary all-even Markov reversal are assumptions;
this program cannot verify them from its input.
"""
from fractions import Fraction
import argparse
import json
import math


def q_bound(n, score):
    """Two-sided Chernoff bound; score is a sum of n signs, in absolute value."""
    score = abs(score)
    if n < 1 or score > n or (n - score) % 2:
        raise ValueError("score must be an attainable sum of n signs")
    k = (n + score) // 2
    denominator = 2**n * k**k * (n-k)**(n-k)  # Python defines 0**0 = 1.
    return min(Fraction(1), Fraction(2*n**n, denominator))


def binary_score(record):
    if len(record) < 2 or any(a not in (0, 1) for a in record):
        raise ValueError("supply at least two binary observations")
    score = 0
    for t, (a, b) in enumerate(zip(record, record[1:])):
        score += (-1 if t % 2 else 1) * (1 if a == b else -1)
    return score


def _log_unit_bounds(x, terms):
    """Enclose log(x) for 1 <= x <= 2 using its positive atanh series."""
    if not Fraction(1) <= x <= Fraction(2):
        raise ValueError("unit interval reduction failed")
    z = (x-1)/(x+1)
    z2 = z*z
    power = z
    total = Fraction(0)
    for j in range(terms):
        total += 2*power/(2*j+1)
        power *= z2
    remainder = 2*power/((2*terms+1)*(1-z2))
    return total, total+remainder


def log_bounds(x, terms=40):
    """A certified rational enclosure for the natural logarithm of x > 0."""
    x = Fraction(x)
    if x <= 0 or terms < 1:
        raise ValueError("positive x and at least one series term required")
    exponent = x.numerator.bit_length() - x.denominator.bit_length()
    scale = Fraction(2**exponent) if exponent >= 0 else Fraction(1, 2**(-exponent))
    reduced = x/scale
    if reduced < 1:
        exponent -= 1
        reduced *= 2
    elif reduced >= 2:
        exponent += 1
        reduced /= 2
    lo, hi = _log_unit_bounds(reduced, terms)
    log2lo, log2hi = _log_unit_bounds(Fraction(2), terms)
    if exponent >= 0:
        return lo+exponent*log2lo, hi+exponent*log2hi
    return lo+exponent*log2hi, hi+exponent*log2lo


def lower_rate_interval(n, score, alpha=Fraction(1, 40), terms=40, output_bits=96):
    """Enclose the ideal (1-alpha)-confidence lower endpoint, in nats/step.

    The LOWER end of this enclosure is itself a conservative certificate.
    This is a fixed-horizon confidence statement, not an anytime guarantee.
    """
    alpha = Fraction(alpha)
    if not 0 < alpha < 1:
        raise ValueError("alpha must lie strictly between 0 and 1")
    q = q_bound(n, score)
    if q >= alpha:
        return Fraction(0), Fraction(0)
    alo, ahi = log_bounds(alpha/q, terms)
    blo, bhi = log_bounds((1-alpha)/(1-q), terms)
    factor = Fraction(4, n)
    lo = factor*(alpha*alo + (1-alpha)*blo)
    hi = factor*(alpha*ahi + (1-alpha)*bhi)
    # Keep the returned certificate small. Rounding is directed and exact.
    scale = 2**output_bits
    lo = Fraction((lo*scale).numerator//(lo*scale).denominator, scale)
    upper = hi*scale
    hi = Fraction(-((-upper.numerator)//upper.denominator), scale)
    return max(Fraction(0), lo), max(Fraction(0), hi)


def critical_score(n, alpha=Fraction(1, 40)):
    for score in range(n % 2, n+1, 2):
        if q_bound(n, score) <= alpha:
            return score
    return None


def binomial_power(n, critical, p=Fraction(3, 4)):
    """Exact source power for the four-state construction in PROOF.txt."""
    if critical is None:
        return Fraction(0)
    p = Fraction(p)
    if not 0 <= p <= 1:
        raise ValueError("p must be a probability")
    numerator = sum(math.comb(n, k) * p.numerator**k
                    * (p.denominator-p.numerator)**(n-k)
                    for k in range(n+1) if abs(2*k-n) >= critical)
    return Fraction(numerator, p.denominator**n)


def fraction_json(x):
    return {"numerator": str(x.numerator), "denominator": str(x.denominator)}


def evaluate(record, alpha=Fraction(1, 40)):
    n = len(record)-1
    score = binary_score(record)
    q = q_bound(n, score)
    lo, hi = lower_rate_interval(n, score, alpha)
    return {
        "observations": n+1, "transitions": n, "signed_score": score,
        "absolute_score": abs(score), "alpha": fraction_json(Fraction(alpha)),
        "null_tail_bound": fraction_json(q), "reject_reversible": q <= alpha,
        "rate_lower_bound_rational": fraction_json(lo),
        "ideal_endpoint_enclosure": [fraction_json(lo), fraction_json(hi)],
        "rate_lower_bound_decimal_preview": float(lo),
        "units": "nats per observed discrete step",
        "contract": "fixed horizon; hidden chain stationary; ordinary all-even reversal",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bits", help="one binary record, e.g. 001100110011")
    parser.add_argument("--alpha", default="1/40")
    args = parser.parse_args()
    if any(a not in "01" for a in args.bits):
        parser.error("bits may contain only 0 and 1")
    print(json.dumps(evaluate([int(a) for a in args.bits], Fraction(args.alpha)), indent=2))


if __name__ == "__main__":
    main()
