"""Exact finite-alphabet check of the stationary-joining Fano correction.

The physical readout is the constant symbol 0 of a rigid flat-torus flow.
An external iid reference uses 0 with probability 1-delta and spreads the
remaining mass uniformly over K-1 symbols. Their product joining has symbol
error delta and reference entropy exactly F_K(delta), so the certified
residual rate is zero and the zero-power flow is consistent with the bound.
"""
from fractions import Fraction
import sympy as sp


def main() -> None:
    K = 3
    delta = Fraction(1, 4)
    probs = [Fraction(1, 1) - delta] + [delta / (K - 1)] * (K - 1)
    p = [sp.Rational(v.numerator, v.denominator) for v in probs]
    d = sp.Rational(delta.numerator, delta.denominator)
    entropy = sp.simplify(-sum(v * sp.log(v) for v in p))
    fano = sp.simplify(-d * sp.log(d) - (1 - d) * sp.log(1 - d)
                       + d * sp.log(K - 1))
    mismatch = sp.simplify(sum(p[1:]))
    residual = sp.simplify(entropy - fano)
    assert mismatch == d
    assert sp.simplify(residual) == 0
    print({
        "alphabet_size": K,
        "delta": str(delta),
        "reference_distribution": [str(v) for v in probs],
        "stationary_joining": "constant physical 0 symbol x independent iid reference",
        "symbol_error_exact": str(mismatch),
        "reference_entropy_equals_fano_correction": bool(sp.simplify(entropy - fano) == 0),
        "residual_rate_after_correction": str(residual),
        "flat_torus_physical_strain_and_work": 0,
        "status": "PASS",
        "scope": "Exact symbolic Fano sharpness/boundary illustration; no ergodic-theory theorem check.",
    })


if __name__ == "__main__":
    main()
