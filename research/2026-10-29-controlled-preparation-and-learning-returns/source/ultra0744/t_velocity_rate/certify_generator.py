"""Independent exact algebra controls; no producer sampler imported."""
from fractions import Fraction as F
import json
from pathlib import Path
import time
import sympy as sp


def main():
    started = time.perf_counter()
    hv, hw, hp = sp.symbols("hv hw hp", positive=True)
    pp, pq, pv, pw = sp.symbols("pp pq pv pw", real=True)
    hq = hv+hw-hp
    gain = (hp*pp+hq*pq)/(hv+hw)
    unsym = ((gain-pv)/hw+(gain-pw)/hv)/2
    sym = (hp*pp+hq*pq-hv*pv-hw*pw)/(2*hv*hw)
    assert sp.factor(unsym-sym) == 0
    x, y = sp.symbols("x y", nonnegative=True)
    # Both probability and rate-drift bounds reduce to manifestly positive forms.
    probability_excess = sp.expand((1+y*y)*(1+x)-x-y)
    assert sp.expand(probability_excess-(x*y*y+(y-sp.Rational(1,2))**2+
                                         sp.Rational(3,4))) == 0
    drift_excess = sp.expand((1+y*y)*(1+x)-y*(x+y))
    assert sp.expand(drift_excess-(1+x*((y-sp.Rational(1,2))**2+
                                      sp.Rational(3,4)))) == 0
    v = (F(1), F(2), F(2))
    w = (F(-2), F(2), F(2))
    sigma = (F(2,3), F(-1,3), F(2,3))
    r = F(3)
    p = tuple((vi+wi+r*si)/2 for vi,wi,si in zip(v,w,sigma))
    q = tuple((vi+wi-r*si)/2 for vi,wi,si in zip(v,w,sigma))
    squared = lambda z: sum(zi*zi for zi in z)
    assert squared(sigma) == 1
    assert squared(p)+squared(q) == squared(v)+squared(w)
    assert tuple(pi+qi for pi,qi in zip(p,q)) == tuple(vi+wi for vi,wi in zip(v,w))
    a, c = F(3,2), F(7)
    hs = [a+squared(z) for z in (v,w,p,q)]
    tests = [(F(1),)*4,
             tuple(1/h for h in hs),
             *[tuple(z[j]/h for z,h in zip((v,w,p,q),hs)) for j in range(3)],
             tuple(squared(z)/(1+squared(z)) for z in (v,w,p,q))]
    for psiv,psiw,psip,psiq in tests:
        h1,h2,h3,h4=hs
        average = (h3*psip+h4*psiq)/(h1+h2)
        raw = c*r*((average-psiv)/h2+(average-psiw)/h1)/2
        canonical = c*r*(h3*psip+h4*psiq-h1*psiv-h2*psiw)/(2*h1*h2)
        assert raw == canonical
    # 6-axis source: 2/3 of ordered pairs are orthogonal, |relative|=sqrt2.
    # For each orthogonal pair E(|p|^4+|q|^4)-2 = 2/3.
    source_m4_derivative = sp.Rational(1,2)*sp.Rational(2,3)*sp.sqrt(2)*sp.Rational(2,3)
    assert sp.simplify(source_m4_derivative-2*sp.sqrt(2)/9) == 0
    b = ((1+sp.sqrt(17))/2)**2
    root = (1+sp.sqrt(17))/2
    assert sp.simplify(-root**2+root+4) == 0
    # Nonflat source energies: initializer/rejection must NOT silently use f0=g0.
    source_p = (F(1,2), F(1,3), F(1,6))
    source_h = (F(1), F(2), F(5))
    source_g = tuple(p*h/2 for p,h in zip(source_p,source_h))
    assert sum(source_g) == 1
    assert sum(p/h for p,h in zip(source_g,source_h)) == F(1,2)
    assert tuple(2*p/h for p,h in zip(source_g,source_h)) == source_p
    result = {
        "status": "PASS_exact_algebra_only",
        "generic_generator_identity": True,
        "probability_bound_positive_polynomial": str(probability_excess),
        "clock_drift_bound_positive_polynomial": str(drift_excess),
        "literal_rational_conservation_and_test_controls": len(tests),
        "source_m4_derivative": str(source_m4_derivative),
        "uniform_m4_constant": str(b),
        "uniform_rate_constant_at_energy1": float(2*(1+sp.sqrt((1+b)/2))),
        "nonflat_source_tilt_and_physical_rejection_exact": True,
        "termination_theorem_verified_by_finite_tests": False,
        "elapsed_seconds": time.perf_counter()-started,
    }
    output=Path(__file__).parent/"outputs"/"GENERATOR_CERTIFICATE.json"
    output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
