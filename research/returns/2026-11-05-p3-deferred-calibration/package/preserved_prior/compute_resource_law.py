#!/usr/bin/env python3
"""Reproduce analytic resource-bound figures and finite-slew meter checks.

Scope and normalization
-----------------------
This program evaluates the root manuscript's supplied conservative full-CQ
bound for initially unencoded sources with independent hidden lambda D[Z]
dephasing, k-site interactions, and the manuscript's summed per-site control
budget Omega. It does not prove that information bound or extend its access
model. With r=Omega/lambda >= 1, the supplied expressions are

    q_k = exp[-1/(k r)] + (1-exp[-1/(k r)]) 2^(-1/k),
    copies_lower = max(1, (2/3) q_k^(-n)),
    beta = exp[-atan(sqrt(r^2-1))/sqrt(r^2-1)],
    copies_sufficient = 8 ln(3) beta^(-2n).

The continuous value beta=e^-1 is used at r=1. Copy expressions are plotted
without integer rounding; a sufficient integer count is the ceiling. These
are bounds from distinct arguments, not asserted optimal copy counts. The
positive construction uses the protected local meters and their access model
specified in the manuscript; it does not acquire these ports for free.

Finite-slew checks integrate the damped source-to-protected-meter transfer
equations x'=-2 lambda x-Omega(t)y, y'=Omega(t)x, from (x,y)=(1,0).
Controls start and end at zero, have |Omega'|<=S, peak <=Omega_max, and pulse
area pi/2. With no dephasing the endpoint is y=1. The checked conservative
bound is beta_pulse=y(T)>=1-2 lambda T. These are numerical ODE diagnostics,
not a substitute for the analytic proof or a simulation of the full n-qubit
experiment. Time and rate units in those diagnostics set lambda=1.

Outputs (beside this script):
  resource_law.png       Publication-size raster figure.
  resource_law.pdf       The same standalone vector figure.
  resource_law.json      Numerical table, figure parameters, and 18 ODE checks.

Dependencies: Python 3, NumPy, SciPy, Matplotlib. No network access is used.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import time

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp


LN10 = math.log(10.0)
SUFFICIENT_PREFACTOR = 8.0 * math.log(3.0)


def log_meter_bias(ratio):
    """Stable log(beta) for the supplied optimal constant pulse, r>=1."""
    ratio = np.asarray(ratio, dtype=float)
    if np.any(ratio < 1.0) or np.any(~np.isfinite(ratio)):
        raise ValueError("Omega/lambda must be finite and at least one")
    frequency = np.sqrt((ratio - 1.0) * (ratio + 1.0))
    result = np.full_like(ratio, -1.0)
    nonzero = frequency > 0.0
    result[nonzero] = -np.arctan(frequency[nonzero]) / frequency[nonzero]
    return result


def log_full_cq_factor(ratio, k):
    """Stable log(q_k), retaining precision for large control/noise ratios."""
    ratio = np.asarray(ratio, dtype=float)
    if k < 1 or int(k) != k or np.any(ratio <= 0):
        raise ValueError("k must be a positive integer and ratios positive")
    lost = -np.expm1(-1.0 / (k * ratio))
    contraction = -math.expm1(-math.log(2.0) / k)
    return np.log1p(-contraction * lost)


def resource_values(n, ratio, k=2):
    """Return a finite JSON-ready resource row; retain huge counts as logs."""
    log_beta = float(log_meter_bias(ratio))
    log_q = float(log_full_cq_factor(ratio, k))
    log_lower = max(0.0, math.log(2.0 / 3.0) - n * log_q)
    log_overhead = -2.0 * n * log_beta
    log_sufficient = math.log(SUFFICIENT_PREFACTOR) + log_overhead

    def manageable_count(log_count):
        return math.exp(log_count) if log_count < 690.0 else None

    return {
        "n": int(n),
        "k": int(k),
        "Omega_over_lambda": float(ratio),
        "q_k": math.exp(log_q),
        "beta": math.exp(log_beta),
        "log10_GHZ_copy_lower_bound": log_lower / LN10,
        "log10_local_meter_sufficient_copies": log_sufficient / LN10,
        "log10_local_meter_overhead": log_overhead / LN10,
        "GHZ_copy_lower_bound_unrounded": manageable_count(log_lower),
        "local_meter_sufficient_copies_unrounded": manageable_count(log_sufficient),
        "large_count_encoding": "null counts are supplied without overflow by log10 fields",
    }


def pulse_segments(peak, slew, area=math.pi / 2.0):
    """Symmetric triangle or trapezoid, represented by affine ramp segments."""
    triangular_peak = math.sqrt(area * slew)
    if triangular_peak <= peak:
        ramp_time = triangular_peak / slew
        return "triangle", triangular_peak, [
            (ramp_time, 0.0, slew),
            (ramp_time, triangular_peak, -slew),
        ]
    ramp_time = peak / slew
    flat_time = area / peak - ramp_time
    if flat_time < -1e-14:
        raise ArithmeticError("Invalid plateau duration")
    return "trapezoid", peak, [
        (ramp_time, 0.0, slew),
        (max(0.0, flat_time), peak, 0.0),
        (ramp_time, peak, -slew),
    ]


def integrate_segments(segments, dephasing):
    """Integrate each affine control segment separately at its exact joins."""
    state = np.array([1.0, 0.0, 0.0])  # source, protected meter, control area
    largest_norm_squared = 1.0
    evaluations = 0
    for duration, initial_control, slope in segments:
        if duration <= 0:
            continue

        def rhs(t, current):
            control = initial_control + slope * t
            x, y, _ = current
            return [-2.0 * dephasing * x - control * y,
                    control * x, control]

        solution = solve_ivp(
            rhs, (0.0, duration), state, method="DOP853",
            rtol=2e-12, atol=2e-14,
            max_step=duration / 8.0,
        )
        if not solution.success:
            raise RuntimeError(solution.message)
        state = solution.y[:, -1]
        largest_norm_squared = max(
            largest_norm_squared,
            float(np.max(solution.y[0] ** 2 + solution.y[1] ** 2)),
        )
        evaluations += solution.nfev
    return state, largest_norm_squared, evaluations


def finite_slew_checks():
    """Eighteen nontrivial finite-duration tests, with positive lower bounds."""
    checks = []
    for peak in (10.0, 30.0, 100.0):
        for slew in (100.0, 300.0, 1000.0, 3000.0, 10000.0, 100000.0):
            shape, used_peak, segments = pulse_segments(peak, slew)
            duration = sum(segment[0] for segment in segments)
            state, maximum_norm, evaluations = integrate_segments(segments, 1.0)
            noiseless, _, _ = integrate_segments(segments, 0.0)
            beta = float(state[1])
            lower = 1.0 - 2.0 * duration
            area_error = abs(float(state[2]) - math.pi / 2.0)
            noiseless_error = abs(float(noiseless[1]) - 1.0)
            if lower <= 0:
                raise AssertionError("A trivial negative lower-bound test was selected")
            if beta < lower - 1e-10:
                raise AssertionError("Finite-slew acquisition bound violated")
            if area_error > 1e-10 or noiseless_error > 1e-10:
                raise AssertionError("Pulse area or noiseless transfer is inaccurate")
            if maximum_norm > 1.0 + 1e-10:
                raise AssertionError("Damped transfer acquired unphysical norm")
            checks.append({
                "shape": shape,
                "lambda": 1.0,
                "Omega_max": peak,
                "slew_S": slew,
                "used_peak": used_peak,
                "duration_T": duration,
                "control_area": float(state[2]),
                "absolute_area_error": area_error,
                "beta_from_ODE": beta,
                "proved_lower_1_minus_2lambdaT": lower,
                "lower_bound_margin": beta - lower,
                "noiseless_transfer_error": noiseless_error,
                "maximum_norm_squared": maximum_norm,
                "ODE_rhs_evaluations": evaluations,
                "passed": True,
            })
    return checks


def constant_pulse_checks():
    """Check the normalization against the supplied closed-form bias."""
    checks = []
    for ratio in (1.0, 1.2, 3.0, 10.0, 100.0):
        frequency = math.sqrt((ratio - 1.0) * (ratio + 1.0))
        duration = math.atan(frequency) / frequency if frequency else 1.0
        state, _, _ = integrate_segments([(duration, ratio, 0.0)], 1.0)
        exact = math.exp(float(log_meter_bias(ratio)))
        error = abs(float(state[1]) - exact)
        if error > 1e-10:
            raise AssertionError("Constant-meter normalization mismatch")
        checks.append({
            "Omega_over_lambda": ratio,
            "optimal_duration_lambdaT": duration,
            "analytic_beta": exact,
            "ODE_beta": float(state[1]),
            "absolute_error": error,
        })
    return checks


def make_figure(destination):
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.titlesize": 11.5,
        "axes.labelsize": 10.5,
        "legend.fontsize": 9,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.8,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "savefig.facecolor": "white",
    })
    fig, axes = plt.subplots(1, 2, figsize=(12.2, 5.25))
    fig.subplots_adjust(left=.075, right=.98, bottom=.18, top=.77, wspace=.28)
    fig.suptitle("Resource bounds for acquiring global coherence", fontsize=16,
                 fontweight="semibold", x=.075, y=.97, ha="left")
    fig.text(.075, .905,
             "Initially unencoded sources with independent hidden dephasing",
             fontsize=11, color="#3b4750")
    fig.text(.075, .858,
             "Bounds from distinct constructions; the plotted copy counts are not asserted optimal.",
             fontsize=9.5, color="#555f68")

    n, k = 1000, 2
    ratios = np.geomspace(1.0, 1e4, 700)
    lower = np.maximum(0.0, math.log(2 / 3) - n * log_full_cq_factor(ratios, k)) / LN10
    sufficient = (math.log(SUFFICIENT_PREFACTOR) - 2 * n * log_meter_bias(ratios)) / LN10
    ax = axes[0]
    ax.plot(ratios, sufficient, color="#2763ad", lw=2.4,
            label=r"Sufficient local-meter copies: $8\ln(3)\,\beta^{-2n}$")
    ax.plot(ratios, lower, color="#a34261", lw=2.4, ls=(0, (5, 2)),
            label=r"GHZ-copy lower bound: $\max\{1,\frac{2}{3}q_k^{-n}\}$")
    ax.set_xscale("log")
    ax.set_xlim(1, 1e4)
    ax.set_ylim(-12, 915)
    ax.set_title(r"(a) Fixed register: $n=1{,}000$, $k=2$", loc="left", pad=12)
    ax.set_xlabel(r"Peak control / hidden dephasing, $\Omega/\lambda$")
    ax.set_ylabel(r"$\log_{10}$(copy-count expression)")
    ax.legend(loc="upper right", frameon=False, handlelength=2.4)
    ax.grid(axis="both", which="major", color="#d9dfe4", lw=.7, alpha=.8)
    ax.set_axisbelow(True)
    ax.text(.97, .45, r"Conservative full-CQ bound" + "\n" + r"and protected local-meter construction",
            transform=ax.transAxes, ha="right", color="#58636d", fontsize=9)

    register_sizes = np.geomspace(10, 1e4, 600)
    families = [
        (np.full_like(register_sizes, 100.0), r"$\Omega/\lambda=100$", "#2763ad", "-"),
        (register_sizes / np.log(register_sizes), r"$\Omega/\lambda=n/\ln n$", "#c47626", (0, (5, 2))),
        (register_sizes, r"$\Omega/\lambda=n$", "#258273", (0, (2, 2))),
    ]
    ax = axes[1]
    for ratio, label, color, style in families:
        overhead = -2 * register_sizes * log_meter_bias(ratio) / LN10
        ax.plot(register_sizes, overhead, label=label, color=color, lw=2.4, ls=style)
    ax.set_xscale("log")
    ax.set_xlim(10, 1e4)
    ax.set_ylim(-2.0, 145)
    ax.set_title("(b) Local-meter overhead as the register grows", loc="left", pad=12)
    ax.set_xlabel(r"Number of source qubits, $n$")
    ax.set_ylabel(r"$\log_{10}$(meter overhead $\beta^{-2n}$)")
    ax.legend(loc="upper left", frameon=False, handlelength=2.4)
    ax.grid(axis="both", which="major", color="#d9dfe4", lw=.7, alpha=.8)
    ax.set_axisbelow(True)
    ax.text(.44, .48, "Fixed control: exponential overhead\n"
            r"$n/\ln n$ control: polynomial overhead" + "\n"
            r"$n$ control: bounded overhead",
            transform=ax.transAxes, color="#58636d", fontsize=9, linespacing=1.65)

    fig.text(.075, .062,
             r"$\beta=\exp[-\arctan\sqrt{r^2-1}/\sqrt{r^2-1}]$ for $r=\Omega/\lambda>1$; "
             r"$\beta=e^{-1}$ at $r=1$. Natural logarithms are used in $n/\ln n$.",
             fontsize=9, color="#46515b")
    fig.text(.075, .025,
             "Panel (b) excludes the constant sufficient-copy prefactor. Counts are unrounded; "
             "meter access and preparation costs are outside these curves.",
             fontsize=8.5, color="#58636d")
    fig.savefig(destination / "resource_law.png", dpi=240)
    fig.savefig(destination / "resource_law.pdf")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    arguments = parser.parse_args()
    destination = arguments.output_dir.resolve()
    destination.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()

    rows = []
    for n in (100, 1000, 10000):
        for ratio in (1, 3, 10, 30, 100, 300, 1000, 3000, 10000):
            row = resource_values(n, ratio)
            row["control_family"] = "fixed_ratio"
            rows.append(row)
        for name, ratio in (("n_over_ln_n", n / math.log(n)), ("n", n)):
            row = resource_values(n, ratio)
            row["control_family"] = name
            rows.append(row)

    finite_checks = finite_slew_checks()
    constant_checks = constant_pulse_checks()
    make_figure(destination)
    summary = {
        "finite_slew_check_count": len(finite_checks),
        "triangle_check_count": sum(c["shape"] == "triangle" for c in finite_checks),
        "trapezoid_check_count": sum(c["shape"] == "trapezoid" for c in finite_checks),
        "maximum_absolute_area_error": max(c["absolute_area_error"] for c in finite_checks),
        "maximum_noiseless_transfer_error": max(c["noiseless_transfer_error"] for c in finite_checks),
        "minimum_finite_slew_bound_margin": min(c["lower_bound_margin"] for c in finite_checks),
        "maximum_constant_pulse_error": max(c["absolute_error"] for c in constant_checks),
        "all_checks_passed": True,
        "runtime_seconds": time.monotonic() - started,
    }
    output = {
        "scope": "Supplied main full-CQ lower bound and protected local-meter upper construction; not optimal sample counts or full-system simulation.",
        "logarithm_conventions": {"resource_values": "base 10", "n_over_ln_n": "natural"},
        "copy_count_convention": "Expressions unrounded; ceiling is sufficient for an integer upper prescription.",
        "figure": {"panel_a_n": 1000, "panel_a_k": 2, "Omega_over_lambda_range": [1, 10000],
                   "panel_b_n_range": [10, 10000]},
        "table": rows,
        "finite_slew_checks": finite_checks,
        "constant_pulse_normalization_checks": constant_checks,
        "check_summary": summary,
    }
    with (destination / "resource_law.json").open("w", encoding="utf-8") as handle:
        json.dump(output, handle, indent=2, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"output_directory": str(destination), "table_rows": len(rows), **summary}, indent=2))


if __name__ == "__main__":
    main()
