#!/usr/bin/env python3
"""Evaluate proved Cycle10 formulas. No native Markov chain is simulated.

The output is a visualization and finite scalar diagnostic, not an exact
arithmetic certificate or evidence for an unproved minimax phase upper.
"""
import argparse
import json
import math
import io
import os
from pathlib import Path
import resource
import time


def softplus(x):
    return max(x, 0.0) + math.log1p(math.exp(-abs(x)))


def finite_control_cost(progress, d, r):
    """Numerical evaluation of the proved count minimum, not its proof."""
    gamma = math.log1p(r)
    h = lambda a: softplus(math.log(r) + a)
    # A J=1 candidate gives a rigorous search cutoff in exact reals since
    # every J-cost is >= J gamma. Extra endpoints protect this float display.
    ceiling = math.ceil(h(max(progress - d, 0.0)) / gamma) + 2
    values = [(j * h(max(progress / j - d, 0.0)), j)
              for j in range(1, ceiling + 1)]
    return min(values)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path,
                        default=Path(__file__).resolve().parents[1] / "evidence" / "critical_profile")
    args = parser.parse_args()
    start, cpu = time.monotonic(), time.process_time()
    args.out.mkdir(parents=True, exist_ok=True)
    K, alpha, d, s = 1.0, 0.5, 3.0, -1.0
    beta = 1.0 - alpha
    r = alpha * math.exp(-K) / beta
    gamma, t = math.log1p(r), r / (1.0 + r)
    d_star = gamma / t
    assert d > d_star
    b0, coefficient = 1.0 - math.exp(-K), gamma / d
    transport_upper = b0 * math.exp(-s)
    envelope_upper = max(K, transport_upper)
    psi = lambda x: min((d * t - gamma) * x, gamma * (1.0 - x))
    amplitude = lambda x: transport_upper * math.exp(-psi(x))
    phase_star = d_star / d
    records = []
    for x in [0.0, 0.25, phase_star, 0.5, 0.75, 1.0]:
        U = d * (100.0 + x)
        cost, count = finite_control_cost(U, d, r)
        records.append({"phase": x, "phase_penalty": psi(x),
                        "native_family_amplitude": amplitude(x),
                        "minimax_lower_amplitude": max(K, amplitude(x)),
                        "finite_control_progress": U,
                        "finite_control_optimal_count": count,
                        "finite_control_excess": cost - coefficient * U,
                        "limit_phase_excess": psi(x)})
    result = {
        "claim_scope": "Numerical evaluation of proved formulas; no native chain simulation",
        "parameters_frozen_in_source_before_execution": {"K": K, "alpha": alpha, "d": d, "s": s},
        "derived": {"r": r, "gamma": gamma, "d_star": d_star,
                    "c_d": coefficient, "phase_of_largest_penalty": phase_star,
                    "all_class_limsup": envelope_upper,
                    "all_class_liminf_lower": max(K, amplitude(phase_star)),
                    "all_class_liminf_exact": None},
        "selected_calculations": records,
        "exact_arithmetic_certificate": False,
        "historical_suites_rerun": False,
        "native_graph_materialized": False,
    }
    (args.out / "VALUES.json").write_text(json.dumps(result, indent=2) + "\n")
    os.environ.setdefault("MPLCONFIGDIR", str(args.out.parent.parent.parent / "plot_cache"))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})
    xs = [i / 600.0 for i in range(601)]
    ys = [amplitude(x) for x in xs]
    lows = [max(K, y) for y in ys]
    fig, ax = plt.subplots(figsize=(9.2, 5.6), layout="constrained")
    ax.fill_between(xs, lows, envelope_upper, color="#D6E2EF", alpha=0.8,
                    label="Unresolved gap for unrestricted minimax risk")
    ax.axhline(envelope_upper, color="#102B4E", lw=2,
               label="Proved universal upper; exact limsup")
    ax.plot(xs, ys, color="#007E77", lw=2.6,
            label="Proved amplitude of the native tree family")
    ax.axhline(K, color="#8A4856", ls="--", lw=1.8,
               label="Ordinary IMH minimax amplitude")
    ax.scatter([phase_star], [amplitude(phase_star)], color="#007E77", s=34, zorder=4)
    ax.set(xlim=(0, 1), ylim=(0.9, 1.84),
           xlabel=r"Crossing phase $\{u_n/d\}$",
           ylabel=r"Critical amplitude: $(\log n)\,\mathrm{TV}$")
    ax.set_title("An attained phase penalty does not prove minimax oscillation", loc="left", pad=18)
    ax.text(0, 1.01, "K = 1, α = 1/2, d = 3, s = −1 · formulas, not simulated chain data",
            transform=ax.transAxes, fontsize=10, color="#555555")
    ax.grid(axis="y", alpha=0.15)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="lower center", frameon=False, fontsize=9.3)
    # Use explicit checked writes: a previous direct-path export produced an
    # incomplete PNG in this runtime despite successful renderer return.
    for extension in ["png", "pdf"]:
        buffer = io.BytesIO()
        fig.savefig(buffer, format=extension, dpi=190)
        payload = buffer.getvalue()
        with (args.out / ("critical_profile." + extension)).open("wb") as stream:
            for offset in range(0, len(payload), 16384):
                chunk = payload[offset:offset + 16384]
                written = stream.write(chunk)
                if written != len(chunk):
                    raise OSError("Incomplete figure write")
        if (args.out / ("critical_profile." + extension)).read_bytes() != payload:
            raise OSError("Figure readback differs from renderer bytes")
    from PIL import Image
    with Image.open(args.out / "critical_profile.png") as rendered:
        rendered.verify()
    plt.close(fig)
    usage = resource.getrusage(resource.RUSAGE_SELF)
    receipt = {"wall_seconds": time.monotonic() - start,
               "process_cpu_seconds": time.process_time() - cpu,
               "peak_rss_kib_linux": usage.ru_maxrss,
               "includes": "Formula evaluation, plotting imports and PNG/PDF rendering",
               "excludes": "Scientific reasoning, design, inference and historical discovery",
               "total_discovery_cost": None}
    (args.out / "RESOURCE_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"out": str(args.out), "derived": result["derived"], "resources": receipt}, indent=2))


if __name__ == "__main__":
    main()
