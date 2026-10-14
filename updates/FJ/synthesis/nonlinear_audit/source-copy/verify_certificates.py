"""Verify the two global certificates with exact rational arithmetic.

This verifies the algebraic enclosures, not floating-point Monte Carlo output,
transcendental function implementations, or the numerical FFT reference.
Run: python verify_certificates.py
No third-party dependencies.
"""
from fractions import Fraction as Q
import json
from pathlib import Path


def assess(name: str, h: Q, R: Q, low: Q, high: Q,
           b2: Q, b3: Q, b4: Q) -> dict:
    P = b2*h**2 + b3*h**3 + b4*h**4
    slope = 2*b2*h + 3*b3*h**2 + 4*b4*h**3
    slack = low*h - R - P
    q = 1 - (low - slope)/high
    valid = h > 0 and 0 < low <= high and slack >= 0 and slope < low
    def encode(x: Q) -> dict:
        return {'numerator': x.numerator, 'denominator': x.denominator,
                'decimal_approximation': float(x)}
    return {'name':name, 'valid':valid, 'radius':encode(h),
            'residual_bound':encode(R), 'tangent_lower':encode(low),
            'proposal_rate':encode(high), 'enclosure_slack':encode(slack),
            'nonlinear_slope':encode(slope), 'offspring_bound':encode(q),
            'expected_node_bound':encode(1/(1-q)) if valid else None}


def verify() -> dict:
    one=Q(1)
    simple=(Q(10),Q(101),Q(101),Q(150),Q(100),Q(25))
    c0=assess('constant predictor',Q(1,8),*simple)
    # Every quantity below is a rational number; the enclosure follows from
    # |cos x|, |cos 7x|, |sin 13x| <= 1, not from sampled locations.
    E=10*(Q(45,100)/102+Q(3,10)/150+Q(1,4)/270)
    lo,hi=one-E,one+E
    R=25*(6*E**2+4*E**3+E**4)
    c1=assess('one screened linear correction',Q(11,1000),R,
              1+100*lo**3,1+100*hi**3,150*hi**2,100*hi,Q(25))
    small=assess('too-small radius',Q(1,20),*simple)
    large=assess('enclosure without finite-work certificate',Q(3,10),*simple)
    assert c0['valid'] and c1['valid']
    assert not small['valid'] and not large['valid']
    assert large['enclosure_slack']['numerator'] > 0
    return {'method':'exact rational arithmetic', 'certificates':[c0,c1],
            'negative_tests':[small,large],
            'scope':'Algebraic global certificates only; not interval verification of the sampler.'}


if __name__ == '__main__':
    result=verify()
    path=Path(__file__).with_name('exact_certificate_checks.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
