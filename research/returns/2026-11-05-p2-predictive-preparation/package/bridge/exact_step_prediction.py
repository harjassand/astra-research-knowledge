"""Compile a finite response table and smooth force program to exact polynomials.

Only acquired table data, baseline, and the requested input enter this module.
It never imports a microscopic source, its modes, or its initial state.
The physical confidence/error budget is separate from this exact arithmetic.
"""
from __future__ import annotations

from fractions import Fraction as F
from pathlib import Path
from math import comb
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent


def fstr(x: F) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def polyadd(a, b):
    out = list(a) + [F(0)] * max(0, len(b) - len(a))
    for i, x in enumerate(b):
        out[i] += x
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def polyscale(a, s):
    return [s * x for x in a]


def polymul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def polyvalue(p, t):
    ans = F(0)
    for x in reversed(p):
        ans = ans * t + x
    return ans


def affine_power(offset, slope, n):
    return [F(comb(n, j)) * offset ** (n-j) * slope ** j for j in range(n+1)]


def density_coefficients(ramp):
    return {2: F(30)/ramp**3, 3: -F(60)/ramp**4, 4: F(30)/ramp**5}


def primitive_at_affine(ramp, affine, extra_power=0):
    offset, slope = affine
    out = [F(0)]
    for power, coefficient in density_coefficients(ramp).items():
        exponent = power + extra_power + 1
        out = polyadd(out, polyscale(affine_power(offset, slope, exponent),
                                    coefficient / exponent))
    return out


def filtered_value(times, values, t, start, ramp):
    """Exact integral of linear S_hat(t-start-s) against a quintic-ramp density."""
    tau = t-start
    if tau <= 0:
        return F(0)
    ans = F(0)
    for i in range(len(times)-1):
        lo = max(F(0), tau-times[i+1])
        hi = min(ramp, tau-times[i])
        if hi <= lo:
            continue
        slope = (values[i+1]-values[i])/(times[i+1]-times[i])
        intercept = values[i]-slope*times[i]
        for power, c in density_coefficients(ramp).items():
            ans += c*((slope*tau+intercept)*(hi**(power+1)-lo**(power+1))/(power+1)
                      -slope*(hi**(power+2)-lo**(power+2))/(power+2))
    return ans


def filtered_polynomial(times, values, start, ramp, midpoint):
    """Polynomial valid between all shifted table/ramp breakpoints."""
    out = [F(0)]
    visits = 0
    for i in range(len(times)-1):
        lo_at_mid = max(F(0), midpoint-start-times[i+1])
        hi_at_mid = min(ramp, midpoint-start-times[i])
        if hi_at_mid <= lo_at_mid:
            continue
        visits += 1
        lo = (F(0), F(0)) if lo_at_mid == 0 else (-start-times[i+1], F(1))
        hi = (ramp, F(0)) if hi_at_mid == ramp else (-start-times[i], F(1))
        slope = (values[i+1]-values[i])/(times[i+1]-times[i])
        intercept = values[i]-slope*times[i]-slope*start
        p0 = polyadd(primitive_at_affine(ramp, hi), polyscale(primitive_at_affine(ramp, lo), -1))
        p1 = polyadd(primitive_at_affine(ramp, hi, 1), polyscale(primitive_at_affine(ramp, lo, 1), -1))
        out = polyadd(out, polyadd(polymul([intercept, slope], p0), polyscale(p1, -slope)))
    assert len(out) <= 7
    return out, visits


def compile_path(table, program):
    ts = [F(x) for x in table["times_exact"]]
    ys = [F(x) for x in table["values_exact"]]
    baseline = F(table["deployment_baseline_exact"])
    horizon = F(table["horizon_exact"])
    ramps = [(F(r["start_exact"]), F(r["ramp_exact"]), F(r["increment_exact"])) for r in program]
    assert ts[0] == 0 and ts[-1] == horizon and ys[0] == 0
    assert all(b>a for a,b in zip(ts,ts[1:]))
    assert all(start >= 0 and ramp > 0 for start,ramp,c in ramps)
    breaks = {F(0), horizon}
    for start, ramp, _ in ramps:
        for t in ts:
            for z in (start+t, start+ramp+t):
                if 0<z<horizon:
                    breaks.add(z)
    breaks = sorted(breaks)
    segments = []
    visits = 0
    for lo, hi in zip(breaks, breaks[1:]):
        coeffs = [baseline]
        for start, ramp, c in ramps:
            p, n = filtered_polynomial(ts, ys, start, ramp, (lo+hi)/2)
            visits += n
            coeffs = polyadd(coeffs, polyscale(p,c))
        segments.append({"left_exact":fstr(lo), "right_exact":fstr(hi),
                         "coefficients_exact":[fstr(x) for x in coeffs]})
    variation = sum(abs(c) for _,_,c in ramps)
    error = (F(table["readiness_error_exact"])
             + variation*F(table["response_error_exact"])
             + F(table.get("delivery_error_exact","0")))
    bits = sum(abs(F(c).numerator).bit_length()+F(c).denominator.bit_length()
               for s in segments for c in s["coefficients_exact"])
    return {
        "definition":"baseline + sum increment * integral_0^ramp S_hat(t-start-s) rho_ramp(s) ds",
        "force_program":program,
        "horizon_exact":fstr(horizon),
        "variation_upper_bound_exact":fstr(variation),
        "uniform_physical_error_bound_exact":fstr(error),
        "uniform_physical_error_bound":float(error),
        "numerical_polynomial_error_exact":"0",
        "segments":segments,
        "execution":{"segments":len(segments),"degree_at_most":6,
                     "active_table_segment_visits":visits,
                     "coefficient_integer_payload_bits":bits},
    }


def evaluate_path(path, t):
    t=F(t)
    segs=path["segments"]
    for s in segs:
        if F(s["left_exact"])<=t<=F(s["right_exact"]):
            return polyvalue([F(x) for x in s["coefficients_exact"]],t)
    raise ValueError("Time outside the emitted path")


def main():
    started=time.perf_counter()
    table_path=HERE/"acquired_step_response.json"
    table=json.loads(table_path.read_text())
    program=[{"start_exact":"0","ramp_exact":"1/20","increment_exact":"4/5"}]
    path=compile_path(table,program)
    path["acquired_table_sha256"]=hashlib.sha256(table_path.read_bytes()).hexdigest()
    target=HERE/"exact_prediction_path.json"
    target.write_text(json.dumps(path,indent=2)+"\n")
    result={"path_sha256":hashlib.sha256(target.read_bytes()).hexdigest(),
            "table_sha256":path["acquired_table_sha256"],
            "uniform_physical_error_bound_exact":path["uniform_physical_error_bound_exact"],
            "uniform_physical_error_bound":path["uniform_physical_error_bound"],
            "execution":path["execution"],
            "elapsed_seconds":time.perf_counter()-started,
            "scope":"Exact compilation from acquired data. Does not certify the floating source simulation or physical premises."}
    (HERE/"exact_prediction_compiler_results.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
