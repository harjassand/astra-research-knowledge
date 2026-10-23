#!/usr/bin/env python3
"""Exact brackets for the same-v constants; an illustration of the proved law.

The figure is not a fitted chain experiment. Its curve is equation (13) of
SHARP_DISTORTION_RATE.md. Rational interval decisions below do not depend on
floating-point plotting. Python standard library suffices without --figure.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import hashlib
import json
import math
import resource
import time
from datetime import datetime, timezone


def unit_log(x, terms=36):
    assert Q(1) <= x <= Q(2)
    z = (x-1)/(x+1)
    total, power = Q(0), z
    for j in range(terms):
        total += 2*power/(2*j+1)
        power *= z*z
    return total, total + 2*power/((2*terms+1)*(1-z*z))


def log_interval(x):
    x = Q(x)
    assert x > 0
    if x < 1:
        low, high = log_interval(1/x)
        return -high, -low
    e = 0
    while x >= 2:
        x /= 2
        e += 1
    low, high = unit_log(x)
    l2, h2 = unit_log(Q(2))
    return low+e*l2, high+e*h2


def ln_F_interval(c):
    a, b = log_interval(c)
    x, y = log_interval(1-c)
    factor = (1-c)/c
    return a+factor*x, b+factor*y


def packed(lo, hi):
    return {"lower": [str(lo.numerator), str(lo.denominator)],
            "upper": [str(hi.numerator), str(hi.denominator)],
            "lower_float_diagnostic": float(lo),
            "upper_float_diagnostic": float(hi)}


def constants():
    # F strictly increases. Solve log F(c)=-1 with certified rational signs.
    low, high = Q(1, 2), Q(3, 4)
    for _ in range(48):
        middle = (low+high)/2
        l, h = ln_F_interval(middle)
        if h < -1:
            low = middle
        elif l > -1:
            high = middle
        else:
            raise ArithmeticError("Refine log interval; never decide an overlapping sign")
    assert ln_F_interval(low)[1] < -1 < ln_F_interval(high)[0]
    ln2 = log_interval(Q(2))
    # Alternating Taylor series for exp(-1); odd/even partial sums enclose it.
    total, factorial = Q(0), 1
    for k in range(61):
        if k:
            factorial *= k
        total += Q((-1)**k, factorial)
    ehigh = total
    elow = ehigh-Q(1, factorial*61)
    gamma = (log_interval(1+elow)[0], log_interval(1+ehigh)[1])
    assert gamma[1] < low < high < ln2[0] < 1
    d_mid = (2*ln2[0]-1, 2*ln2[1]-1)
    return {"c0": packed(low, high), "log2": packed(*ln2),
            "gamma": packed(*gamma), "d_middle": packed(*d_mid),
            "exp_minus_one": packed(elow, ehigh),
            "strict_order_certified": True,
            "method": "36-term positive atanh log series with rational remainder; 48 rational bisections; alternating exp(-1) series through60 and61 terms",
            "theorem_constant_definition": "r=exp(-1); F(c0)=r; gamma=log(1+r); finite d=log4-1 gives c(d)=1/2 and g(d)=log2"}


def rate_c(d, r):
    # Floating plotting evaluation of the theorem's closed piecewise formula.
    if r >= math.exp(d):
        return 1.0
    threshold = (1+r)/r*math.log1p(r)
    if d >= threshold:
        return math.log1p(r)/d
    target = math.log(r)-d
    low, high = 0.0, 1.0
    for _ in range(70):
        c = (low+high)/2
        logf = math.log(c)+(1-c)/c*math.log1p(-c)
        if logf < target:
            low = c
        else:
            high = c
    return (low+high)/2


def draw(out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    r = math.exp(-1)
    ds = [6*i/600 for i in range(601)]
    gs = [(1+d)*rate_c(d, r) for d in ds]
    dmid = math.log(4)-1
    threshold = (1+r)/r*math.log1p(r)
    fig, ax = plt.subplots(figsize=(8.4, 4.6), constrained_layout=True)
    ax.plot(ds, gs, color="#176b86", linewidth=2.5, label="Proved coefficient g(d)")
    ax.axhline(1, color="#495463", linestyle=":", linewidth=1.6,
               label="Ordinary IMH exponent")
    ax.axhline(math.log1p(r), color="#9b542a", linestyle="--", linewidth=1.6,
               label="Limit as distortion grows")
    ax.axvline(threshold, color="#c1c6cb", linewidth=1)
    ax.scatter([0, dmid], [rate_c(0,r), math.log(2)], color="#176b86", zorder=4)
    ax.annotate("Matched: 0.64842", (0, rate_c(0,r)), xytext=(.65,.76),
                arrowprops={"arrowstyle":"-", "color":"#65727c"})
    ax.annotate("d = log 4 − 1: log 2", (dmid, math.log(2)), xytext=(1.25,.67),
                arrowprops={"arrowstyle":"-", "color":"#65727c"})
    ax.set(xlabel="Limiting discrepancy d", ylabel="Logarithmic risk exponent at v = log log n",
           xlim=(-.05,6), ylim=(.26,1.08),
           title="The same convergence scale can have different sharp rates")
    ax.text(.98,.95,"K = 1, α = 1/2\nHigher exponent means faster worst-case decay",
            transform=ax.transAxes, ha="right", va="top", fontsize=9, color="#48515a")
    ax.grid(axis="y", color="#e2e5e8", linewidth=.7)
    ax.spines[["top","right"]].set_visible(False)
    ax.legend(loc="lower right", frameon=False, fontsize=8)
    fig.savefig(out/"rate_function.png", dpi=180)
    fig.savefig(out/"rate_function.pdf")
    plt.close(fig)
    return {"input": {"K":1, "alpha":.5, "d_min":0, "d_max":6, "grid_points":601},
            "interpretation":"Illustration of the proved scalar formula; no finite-chain data or fitted asymptotic rate",
            "threshold_diagnostic":threshold,
            "values":[{"d":d,"g":g} for d,g in zip(ds,gs)]}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--figure", action="store_true")
    args = p.parse_args()
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        raise SystemExit("Refusing to overwrite existing evidence")
    args.output_dir.mkdir(parents=True,exist_ok=True)
    wall, cpu = time.monotonic(), time.process_time()
    started = datetime.now(timezone.utc).isoformat()
    result = constants()
    (args.output_dir/"CONSTANT_BRACKETS.json").write_text(json.dumps(result,indent=2)+"\n")
    if args.figure:
        figure = draw(args.output_dir)
        (args.output_dir/"FIGURE_INPUTS_AND_VALUES.json").write_text(json.dumps(figure,indent=2)+"\n")
    receipt = {"started_utc":started,"completed_utc":datetime.now(timezone.utc).isoformat(),
               "code_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "cpu_seconds":time.process_time()-cpu,"wall_seconds":time.monotonic()-wall,
               "peak_RSS_KiB_linux":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               "inference_cost":None,"discovery_cost":None,"figure_generated":args.figure}
    (args.output_dir/"RESOURCE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps({key:result[key]["lower_float_diagnostic"] for key in ("c0","log2","gamma","d_middle")},indent=2))
    print(json.dumps(receipt,indent=2))


if __name__ == "__main__":
    main()
