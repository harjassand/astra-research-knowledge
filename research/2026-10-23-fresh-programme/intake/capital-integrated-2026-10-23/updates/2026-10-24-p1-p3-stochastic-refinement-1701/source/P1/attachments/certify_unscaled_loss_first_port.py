#!/usr/bin/env python3
"""Private P1 exact-arithmetic certificate for a two-mode open Kerr record.

No floating point enters an enclosure. Fractions generate alternating Taylor
bounds for elementary functions. All subsequent arithmetic rounds outwards to
a fixed dyadic grid. Monotone rectangle sums certify the sole time integral.
Floats in the JSON are explicitly display-only.

Fixed physical inputs: d=g=1, theta=1/1024, eta=theta*kappa=1/64,
kappa=16, R=I-theta*[[2,-1],[-1,2]]. Kerr and ordinary loss act on [0,3].
Only first detected output port +/- in [2,3] is exposed; no event time is read.
The two loss outputs are interfered on a balanced real mixer before detection.
"""

from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

BITS = 160
SCALE = 1 << BITS
CELLS = 4096


def ceildiv(a, b):
    assert b > 0
    return -((-a) // b)


@dataclass(frozen=True)
class I:
    lo: int
    hi: int

    def __post_init__(self):
        assert self.lo <= self.hi

    @staticmethod
    def of(x):
        if isinstance(x, I):
            return x
        x = F(x)
        return I((x.numerator * SCALE) // x.denominator,
                 ceildiv(x.numerator * SCALE, x.denominator))

    def __add__(self, y):
        y = I.of(y)
        return I(self.lo+y.lo, self.hi+y.hi)

    __radd__ = __add__

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, y):
        return self + (-I.of(y))

    def __rsub__(self, y):
        return I.of(y) + (-self)

    def __mul__(self, y):
        y = I.of(y)
        products = [self.lo*y.lo, self.lo*y.hi,
                    self.hi*y.lo, self.hi*y.hi]
        return I(min(products)//SCALE, ceildiv(max(products), SCALE))

    __rmul__ = __mul__

    def reciprocal(self):
        assert self.lo > 0
        return I((SCALE*SCALE)//self.hi, ceildiv(SCALE*SCALE, self.lo))

    def __truediv__(self, y):
        return self * I.of(y).reciprocal()

    def __rtruediv__(self, y):
        return I.of(y) * self.reciprocal()

    def __pow__(self, n):
        assert isinstance(n, int) and n >= 0
        z = I.of(1)
        for _ in range(n):
            z = z*self
        return z


def enclosure(a, b):
    assert a <= b
    return I(I.of(a).lo, I.of(b).hi)


def exp_neg(t):
    """Taylor's signed remainder gives odd lower and even upper sums."""
    assert 0 <= t <= 3
    term = F(1)
    even = term
    for k in range(1, 65):
        term *= -t/F(k)
        even += term
    odd = even + term*(-t/F(65))
    assert odd <= even
    return enclosure(odd, even)


def sin_cos(t):
    """Alternating series, t in [0,3/1024]; terms decrease throughout."""
    assert 0 <= t <= F(3, 1024)
    term, so = t, t
    for k in range(1, 9):
        term *= -t*t/F((2*k)*(2*k+1))
        so += term
    sl = so + term*(-t*t/F(18*19))
    term, co = F(1), F(1)
    for k in range(1, 9):
        term *= -t*t/F((2*k-1)*(2*k))
        co += term
    cl = co + term*(-t*t/F(17*18))
    return enclosure(sl, so), enclosure(cl, co)


def polar_exp(t, chi):
    a = exp_neg(t)
    sn, cs = sin_cos(chi*t)
    return a, a*cs, -a*sn


def abs_interval(x):
    if x.lo >= 0:
        return x
    if x.hi <= 0:
        return -x
    return I(0, max(-x.lo, x.hi))


def tv(p, q):
    return sum((abs_interval(x-y) for x, y in zip(p, q)), I.of(0))/2


def record(survival, balance):
    ans = (survival, (1-survival+balance)/2,
           (1-survival-balance)/2)
    assert all(x.lo >= 0 and x.hi <= SCALE for x in ans)
    assert sum(x.lo for x in ans) <= SCALE <= sum(x.hi for x in ans)
    return ans


def dump(x):
    if isinstance(x, I):
        return {"lower_numerator": str(x.lo),
                "upper_numerator": str(x.hi),
                "denominator": str(SCALE),
                "display_only": [float(F(x.lo, SCALE)), float(F(x.hi, SCALE))]}
    if isinstance(x, F):
        return {"numerator": str(x.numerator), "denominator": str(x.denominator)}
    if isinstance(x, dict):
        return {k: dump(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [dump(v) for v in x]
    return x


def main():
    began = time.monotonic()
    theta = F(1, 1024)
    kappa, g, d = F(16), F(1), F(1)
    eta, chi = theta*kappa, theta*g
    alpha, beta = F(2), F(1)
    r, s = 1-alpha*theta, beta*theta
    delta = (1-r)**2-s*s
    delta_bar = alpha*alpha-beta*beta
    t0, final_t = F(2), F(3)
    assert delta == delta_bar*theta*theta
    assert 0 < r-s < r+s < 1
    assert 0 < eta < 1

    # These elementary inequalities prove monotonicity of the exact coherence
    # integrand on [0,3]: f_R'<=0, f_I'<=0, D'(f)>=0, exp(-t)'<0.
    # tan(chi*t)<=2*chi*t for chi*t<=1/2 and 2*eta*T<=1 suffice.
    assert chi*final_t <= F(1, 2)
    assert 2*eta*final_t <= 1
    a0, er0, ei0 = polar_exp(t0, chi)

    names = ("exact_quantum", "exact_quantum_no_kerr", "damped_nonlinear_limit",
             "damped_amplitude_old_phase", "old_weak_bath_law")
    low_sum = {k: 0 for k in names}
    high_sum = {k: 0 for k in names}
    minima = None

    for j in range(CELLS+1):
        t = t0+(final_t-t0)*F(j, CELLS)
        a, er, ei = polar_exp(t, chi)

        # f = E + [(1-E)-eta*(E(t0)-E)]/(1+i*chi).
        bre = 1-(1-eta)*er-eta*er0
        bim = -(1-eta)*ei-eta*ei0
        fr = er+(bre+chi*bim)/(1+chi*chi)
        fi = ei+(bim-chi*bre)/(1+chi*chi)
        determinant = ((1-(r+s)*fr)*(1-(r-s)*fr)
                       +(r*r-s*s)*fi*fi)
        assert determinant.lo > 0
        exact = 2*eta*a*delta*s/(determinant**2)

        u, v = 1-a, a0-a
        zeta_t = 1-eta*v
        zero_kerr_determinant = (1-(r+s)*zeta_t)*(1-(r-s)*zeta_t)
        no_kerr = 2*eta*a*delta*s/(zero_kerr_determinant**2)
        qa = (alpha+kappa*v)**2-beta*beta
        good = 2*kappa*delta_bar*beta*a/((qa+g*g*u*u)**2)
        patched = 2*kappa*delta_bar*beta*a/((qa+g*g*t*t)**2)
        old_q = (alpha+kappa*(t-t0))**2-beta*beta+g*g*t*t
        old = I.of(2*kappa*delta_bar*beta/(old_q*old_q))
        values = (exact, no_kerr, good, patched, old)
        assert all(vv.lo > 0 for vv in values)
        # Monotonicity has an analytic proof; these disjoint intervals also
        # check that every pair of adjacent sample enclosures decreases.
        if minima is not None:
            assert all(vv.hi <= previous for vv, previous in zip(values, minima))
        minima = [vv.lo for vv in values]
        for name, val in zip(names, values):
            if j > 0:
                low_sum[name] += val.lo
            if j < CELLS:
                high_sum[name] += val.hi

    balances = {name: I(low_sum[name], high_sum[name])
                * ((final_t-t0)/CELLS) for name in names}
    zeta = 1-eta*(a0-a)
    quantum_s = delta/((1-(r+s)*zeta)*(1-(r-s)*zeta))
    leading_s = delta_bar/((alpha+kappa*(a0-a))**2-beta*beta)
    old_s = I.of(delta_bar/((alpha+kappa*(final_t-t0))**2-beta*beta))
    records = {
        "exact_quantum": record(quantum_s, balances["exact_quantum"]),
        "exact_quantum_no_kerr": record(quantum_s, balances["exact_quantum_no_kerr"]),
        "damped_nonlinear_limit": record(leading_s, balances["damped_nonlinear_limit"]),
        "damped_amplitude_old_phase": record(leading_s, balances["damped_amplitude_old_phase"]),
        "old_weak_bath_law": record(old_s, balances["old_weak_bath_law"]),
    }
    result = {
        "status": "RIGOROUS_OUTWARD_ARITHMETIC_AND_MONOTONE_QUADRATURE",
        "scope": "One first-port latch in [2,3]; exact quantum dynamics acts throughout [0,3].",
        "order": ["no_detected_loss", "first_plus", "first_minus"],
        "inputs": {"theta":theta,"d":d,"g":g,"chi":chi,"kappa":kappa,
                   "eta":eta,"alpha":alpha,"beta":beta,"r":r,"s":s,
                   "delta":delta,"detect_from":t0,"detect_to":final_t},
        "arithmetic": {"dyadic_bits": BITS, "rectangle_cells": CELLS,
                       "exp_even_degree":64,"exp_odd_degree":65,
                       "sin_upper_degree":17,"cos_upper_degree":16},
        "balances": balances,
        "records": records,
        "record_TV": {
            "exact_quantum_kerr_vs_no_kerr_same_complete_pooled_count_law":
                (balances["exact_quantum_no_kerr"]-balances["exact_quantum"])/2,
            "exact_quantum_vs_damped_nonlinear_limit":
                tv(records["exact_quantum"], records["damped_nonlinear_limit"]),
            "exact_quantum_vs_damped_amplitude_old_phase":
                tv(records["exact_quantum"], records["damped_amplitude_old_phase"]),
            "exact_quantum_vs_old_weak_bath_law":
                tv(records["exact_quantum"], records["old_weak_bath_law"]),
            "leading_phase_only_gap":
                (balances["damped_nonlinear_limit"]
                 -balances["damped_amplitude_old_phase"])/2,
        },
        "predecessor": {"authors":"Mogilevtsev, Tyc, Korolkova", "year":2009,
                        "url":"https://arxiv.org/pdf/0904.3235", "revision":"v1",
                        "relevant_interface":"Sec III Eq16; Sec IV Eqs18-20; supplied Markovian loss"},
        "runtime_seconds_observed":time.monotonic()-began,
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "nonclaims": ["No acquired measurement or microscopic bath derivation.",
                      "This record does not certify trace distance of full quantum states.",
                      "One finite-record benchmark is not a generic exact posterior closure.",
                      "Displayed floats are not arithmetic premises."]
    }
    output = Path(__file__).with_name("UNSCALED_LOSS_FIRST_PORT_CERTIFICATE.json")
    output.write_text(json.dumps(dump(result), indent=2)+"\n")
    print(json.dumps({"certificate":str(output),
                      "record_TV": {k: dump(v)["display_only"]
                                    for k,v in result["record_TV"].items()},
                      "records": {k:[dump(x)["display_only"] for x in vs]
                                  for k,vs in records.items()},
                      "runtime_seconds_observed":result["runtime_seconds_observed"]}, indent=2))


if __name__ == "__main__":
    main()
