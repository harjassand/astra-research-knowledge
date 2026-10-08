#!/usr/bin/env python3
"""Visualize retained finite diagnostics, without treating them as proof."""
from pathlib import Path
import json
import math
import tempfile
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

root = Path(__file__).resolve().parents[2]
package = Path(__file__).resolve().parent.parent
packaged = (package / "proofs").is_dir()
source = (package / "proofs/curie_weiss/exact_marginals.json" if packaged
          else root / "work/agents/curie_weiss/exact_marginals.json")
rows = json.loads(source.read_text())["local"]
out = (Path(tempfile.mkdtemp(prefix="research-critical-figure-")) if packaged
       else root / "outputs/research/figures")
out.mkdir(parents=True, exist_ok=True)
fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.5), constrained_layout=True)
colors = ["#BECBD3", "#7A9CAC", "#3E7C91", "#205971", "#102D46"]
for N, color in zip(sorted({r["N"] for r in rows}), colors):
    values = sorted((r for r in rows if r["N"] == N and r["r"] >= 2), key=lambda x:x["r"])
    x = [v["r"]/math.sqrt(N) for v in values]
    axes[0].plot(x, [v["half_trace"] for v in values], "o-", ms=3.8, lw=1.2, color=color, label=f"N = {N:,}")
    axes[1].plot(x, [v["KL"] for v in values], "o-", ms=3.8, lw=1.2, color=color)
for ax in axes:
    ax.set_xscale("log")
    ax.set_xlabel(r"Accessed fraction of the critical scale  $r/\sqrt{N}$")
    ax.axvline(1, color="#AA6040", ls="--", lw=1)
    ax.grid(alpha=.17)
    ax.spines[["top","right"]].set_visible(False)
axes[0].set_ylabel(r"Trace distance  $\frac{1}{2}\|\rho_r-I/2^r\|_1$")
axes[0].set_ylim(0,1.02)
axes[0].legend(frameon=False, fontsize=9, loc="upper left")
axes[1].set_ylabel("Relative entropy (natural logarithms)")
axes[1].set_yscale("log")
fig.suptitle(r"Critical isotropic Curie–Weiss state: $\rho_N\propto e^{2J^2/N}$", fontsize=15)
fig.text(.5,-.055,"Finite block-spectrum diagnostics; connecting lines guide the eye. The written proofs establish the asymptotic window.",ha="center",fontsize=9)
fig.savefig(out/"critical-local-window.png",dpi=180,bbox_inches="tight")
fig.savefig(out/"critical-local-window.svg",bbox_inches="tight")
print(out/"critical-local-window.png")
