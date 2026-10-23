#!/usr/bin/env python3
"""Export a scientific figure from the frozen principal results; no rerun."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

root = Path(__file__).resolve().parent
data = json.loads((root/"results/principal_results.json").read_text())
styles = {
    "pure_IMH": ("Pure independence MH", "#176a70", "o", "-"),
    "local_then_global": ("Local then global", "#c34934", "s", "-"),
    "global_then_local": ("Global then local", "#915fa2", "D", "-"),
    "mixture_expected_global_match": ("Mixture (expected global count)", "#b17c12", "^", "--"),
}
plt.rcParams.update({"font.size": 10, "axes.spines.top": False,
                     "axes.spines.right": False, "svg.fonttype": "none"})
fig, axes = plt.subplots(1, 2, figsize=(11, 4.9), sharey=True)
for ax, family in zip(axes, data["families"][1:]):
    rows = family["matched_cost_results"]
    x = [r["total_global_candidates"] for r in rows]
    for key, (label, color, marker, line) in styles.items():
        ax.plot(x, [float(r["TV"][key]) for r in rows], color=color,
                marker=marker, linestyle=line, markersize=4, label=label)
    init = family["certified_initialization"]
    ax.scatter([init["final_total_candidates"]], [float(init["TV_after_local_global"])],
               s=95, marker="*", facecolors="none", edgecolors="#121212", zorder=5,
               label="IMH initialization, then local/global")
    ax.axhline(.01, color="#777777", linewidth=.9, linestyle=":")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylim(.00065, .18)
    ax.set_xlabel("Total global candidates, including initialization")
    ax.set_title(f"Target trap mass p = {family['p']}\nForward KL = {float(family['forward_KL']):.6f}")
    ax.grid(axis="y", alpha=.15)
axes[0].set_ylabel("Total-variation error")
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False,
           bbox_to_anchor=(.5, .025))
fig.suptitle("Adding local moves can destroy the proposal-start guarantee", fontsize=14, y=.99)
fig.text(.5, .005, "Numerically evaluated finite transition laws; not trajectory simulations or an application benchmark.",
         ha="center", fontsize=8, color="#444444")
fig.tight_layout(rect=(0, .21, 1, .96))
out = root/"figures"
out.mkdir(exist_ok=True)
for suffix in ("png", "pdf"):
    fig.savefig(out/f"hybrid_boundary.{suffix}", dpi=190, bbox_inches="tight")
(out/"plot_receipt.json").write_text(json.dumps({"matplotlib": matplotlib.__version__,
    "input": "results/principal_results.json", "new_sampling_runs": 0}, indent=2)+"\n")
print(str(out/"hybrid_boundary.png"))
