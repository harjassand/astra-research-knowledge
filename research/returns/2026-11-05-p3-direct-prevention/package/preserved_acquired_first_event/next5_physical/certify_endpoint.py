"""Directed-rounding enclosure of the finite endpoint diagnostic.

All ordinary operations round outward. Decimal exp/sqrt are correctly rounded
to nearest; taking the adjacent representable number on either side encloses
the exact result. No Monte Carlo statement is used in the certificate.
The implementation assumes Python's documented decimal arithmetic contract.
"""
from decimal import Decimal, Context, localcontext, ROUND_FLOOR, ROUND_CEILING
from pathlib import Path
import json

C = Context(prec=100)


def calc(fn, rounding):
    with localcontext(C) as ctx:
        ctx.rounding = rounding
        return fn()


class I:
    def __init__(self, lo, hi=None):
        self.lo = Decimal(str(lo))
        self.hi = self.lo if hi is None else Decimal(str(hi))
        assert self.lo <= self.hi

    @staticmethod
    def cast(x):
        return x if isinstance(x, I) else I(x)

    def __add__(self, x):
        x = I.cast(x)
        return I(calc(lambda: self.lo + x.lo, ROUND_FLOOR),
                 calc(lambda: self.hi + x.hi, ROUND_CEILING))

    __radd__ = __add__

    def __neg__(self):
        # copy_negate is exact and unaffected by the ambient context.
        return I(self.hi.copy_negate(), self.lo.copy_negate())

    def __sub__(self, x):
        return self + (-I.cast(x))

    def __rsub__(self, x):
        return I.cast(x) - self

    def __mul__(self, x):
        x = I.cast(x)
        pairs = [(y, z) for y in [self.lo, self.hi] for z in [x.lo, x.hi]]
        return I(min(calc(lambda: y * z, ROUND_FLOOR) for y, z in pairs),
                 max(calc(lambda: y * z, ROUND_CEILING) for y, z in pairs))

    __rmul__ = __mul__

    def __truediv__(self, x):
        x = I.cast(x)
        assert not x.lo <= 0 <= x.hi
        inv = I(calc(lambda: Decimal(1) / x.hi, ROUND_FLOOR),
                calc(lambda: Decimal(1) / x.lo, ROUND_CEILING))
        return self * inv

    def __rtruediv__(self, x):
        return I.cast(x) / self

    def __pow__(self, n):
        assert isinstance(n, int) and n >= 0
        out = I(1)
        for _ in range(n):
            out = out * self
        return out

    def exp(self):
        with localcontext(C):
            return I(self.lo.exp().next_minus(), self.hi.exp().next_plus())

    def sqrt(self):
        assert self.lo >= 0
        with localcontext(C):
            return I(self.lo.sqrt().next_minus(), self.hi.sqrt().next_plus())

    def log(self):
        assert self.lo > 0
        with localcontext(C):
            return I(self.lo.ln().next_minus(), self.hi.ln().next_plus())

    def record(self):
        return {"lower": str(self.lo), "upper": str(self.hi)}


def imax(*xs):
    return I(max(x.lo for x in xs), max(x.hi for x in xs))


def spectral(a, M):
    lam = a / (M - 1)
    disc = ((1 - lam)**2 + 4 * lam * a).sqrt()
    rp = (1 + lam + disc) / (2 * (1 - a))
    rm = lam / ((1 - a) * rp)
    wm = (rp - 1) / (rp - rm)
    return [(1 - wm, rp), (wm, rm)]


def component(r, U, h, T):
    z, disp, work = I(0), I(0), I(0)
    for length, start, slope in [(h, I(0), U / h),
                                 (T - 2 * h, U, I(0)),
                                 (h, U, -U / h)]:
        er = (-r * length).exp()
        i0 = (1 - er) / r
        i1 = (1 - er - r * length * er) / r**2
        aa = z - start / r + slope / r**2
        bb = start / r - slope / r**2
        dd = slope / r
        integ = aa * i0 + bb * length + dd * length**2 / 2
        tinteg = aa * i1 + bb * length**2 / 2 + dd * length**3 / 3
        disp = disp + integ
        work = work + start * integ + slope * tinteg
        z = aa * er + bb + dd * length
    var = 2 * (T / r + ((-r * T).exp() - 1) / r**2)
    return disp, var, work


def pulse(modes, U, h, T):
    out = [I(0), I(0), I(0)]
    for w, r in modes:
        vals = component(r, U, h, T)
        out = [x + w * y for x, y in zip(out, vals)]
    return out


def main():
    a, M, U, h, T = I('.0001'), I(1000), I(10), I(1), I(800)
    m0, v0, w0 = pulse([(I(1), I(1))], U, h, T)
    m1, v1, w1 = pulse(spectral(a, M), U, h, T)
    gap, mid = m1 - m0, (m1 + m0) / 2
    threshold = I('8142.67668356')
    threshold_error = I('1e-8')
    delta = threshold - mid
    assert max(delta.lo.copy_abs(), delta.hi.copy_abs()) < threshold_error.lo

    sigma, step, ef, dt = I('.25'), I('.01'), I('.0001'), I('.0001')
    bias, timing_allowance, q_bound = I('.01'), I(1), I(1)
    vmax = imax(v0, v1)
    varmax = vmax + 2 * sigma**2
    force_offset = ef * vmax / 2
    bounded = force_offset + step + bias + timing_allowance + threshold_error
    timing = 2 * dt * (2 + (U + ef) * (1 + 2 * a * (T + 2 * dt)))
    timing = timing / timing_allowance
    separation = gap / 2 - bounded
    assert separation.lo > 0
    chernoff = (-(separation**2) / (2 * varmax)).exp()
    satmargin = I(12000) - imax(m0, m1) - force_offset
    satmargin = satmargin - q_bound - timing_allowance - bias - step
    assert satmargin.lo > 0
    saturation = 4 * (-(satmargin**2) / (2 * varmax)).exp()
    combined = timing + chernoff + saturation
    assert combined.hi < Decimal('.003273')

    # E|stationary J| <= 1, so this also covers bounded, causal force error.
    absolute_work = imax(w0, w1) + ef * imax(m0, m1)
    absolute_work = absolute_work + ef * (U + ef) * vmax / 2
    absolute_work = absolute_work + U * (T - h) + ef * T
    reserve = I(100000000)
    reserve_failure = absolute_work / reserve
    assert reserve_failure.hi < Decimal('.001')
    with_reserve = combined + reserve_failure
    assert with_reserve.hi < Decimal('.004183')

    inclusive_time = T + 4 * dt + I('.02')
    lam = a / (M - 1)
    passive_kl = -(1 - a).log() / 2 + inclusive_time * (1 + lam) * a / (4 * (1 - a))
    passive_tv = (passive_kl / 2).sqrt()
    passive_error_lower = (1 - passive_tv) / 2
    assert passive_error_lower.lo > Decimal('.449934')
    effort = U**2 * (T - 4 * h / 3)
    actual_effort = effort + 2 * ef * U * (T - h) + ef**2 * T
    ah = I('1e-10')
    hidden_kl = ah * (1 + inclusive_time) + ah**2 * actual_effort * inclusive_time**2
    hidden_tv = (hidden_kl / 2).sqrt()
    assert hidden_tv.hi < Decimal('.000201')

    result = {
        "arithmetic_contract": "100-significant-digit Decimal; directed rounding for arithmetic; adjacent outward numbers after correctly rounded exp, log and sqrt.",
        "status": "all_rigorous_interval_assertions_passed_under_arithmetic_contract",
        "mean_reference": m0.record(), "mean_alternative": m1.record(),
        "mean_separation": gap.record(), "variance_reference": v0.record(),
        "variance_alternative": v1.record(), "threshold": threshold.record(),
        "threshold_error": delta.record(), "bounded_offset": bounded.record(),
        "timing_error_probability": timing.record(),
        "gaussian_tail": chernoff.record(), "saturation_probability": saturation.record(),
        "complete_meter_and_force_error_probability": combined.record(),
        "expected_absolute_work_upper": absolute_work.record(),
        "finite_mechanical_work_reserve": reserve.record(),
        "reserve_depletion_probability_upper": reserve_failure.record(),
        "error_including_work_reserve_abort": with_reserve.record(),
        "inclusive_time_budget": inclusive_time.record(),
        "actual_force_effort_upper": actual_effort.record(),
        "passive_kl_upper": passive_kl.record(),
        "passive_record_TV_upper": passive_tv.record(),
        "passive_maximum_error_lower_bound": passive_error_lower.record(),
        "hidden_transport_1e9_record_TV_upper": hidden_tv.record(),
        "scope": "Calibrated interface and supplied stationary velocity initialization; no hardware manufacture or thermal bath simulation. Two Gaussian endpoint detector errors are independent. Early energy-reserve shutdown must be declared as abort. At the start of the unforced lead-in, position lies within one coordinate unit of its fiducial."
    }
    path = Path(__file__).with_name('endpoint_certificate.json')
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({"status": result['status'],
                      "meter_force_error_upper": str(combined.hi),
                      "error_with_reserve_abort_upper": str(with_reserve.hi),
                      "work_reserve": str(reserve.hi)}, indent=2))


if __name__ == '__main__':
    main()
