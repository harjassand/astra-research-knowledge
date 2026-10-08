#!/usr/bin/env python3
"""Plot the internally derived rate criterion; the picture is not a proof."""
from pathlib import Path
import tempfile
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mpmath as mp

root = Path(__file__).resolve().parents[2]
package = Path(__file__).resolve().parent.parent
out = (Path(tempfile.mkdtemp(prefix="research-phase-figure-"))
       if (package / "proofs").is_dir()
       else root / "outputs" / "research" / "figures")
out.mkdir(parents=True, exist_ok=True)
beta = np.linspace(0.005, 5, 700)
mp.mp.dps = 40
h = np.array([float((1 + mp.mpf(str(b))*mp.exp(2*mp.mpf(str(b)))
                    * (2*mp.mpf(str(b)))**(-mp.mpf(str(b)))
                    * mp.gammainc(mp.mpf(str(b)), 0, 2*mp.mpf(str(b))))/2)
              for b in beta])
threshold = 1/h
fig, ax = plt.subplots(figsize=(8.6, 5.4), constrained_layout=True)
ax.fill_between(beta, 0, threshold, color="#D6EAF2")
ax.fill_between(beta, threshold, 1, color="#E8E6E2")
ax.plot(beta, threshold, color="#243B4A", lw=2.2)
ax.plot([0.2], [0.2], "o", color="#AF522B", ms=7, zorder=5)
ax.annotate("Audited fixture (1, 1, 1, 4, 1)", xy=(0.2,0.2),
            xytext=(0.6,0.28), fontsize=10, color="#7D351A",
            arrowprops={"arrowstyle":"-", "color":"#AF522B"})
ax.text(2.9, 0.66, "Nonexplosive\nincluding the boundary", ha="center", fontsize=13)
ax.text(1.75, 0.075, "Almost-sure explosion", ha="center", fontsize=12)
ax.set(xlim=(0,5), ylim=(0,1), xlabel=r"Birth-to-pair-death ratio  $\beta=k_2/(k_3+k_4)$",
       ylabel=r"Fraction of pair deaths losing A  $q=k_4/(k_3+k_4)$")
ax.set_title("Exact rate criterion for the five-reaction model", loc="left", fontsize=16, pad=16)
ax.spines[["top","right"]].set_visible(False)
ax.grid(alpha=.16)
fig.text(.5, -.025,
         r"Boundary: $q h(\beta)=1$. All rates are fixed and positive; $k_0,k_1$ affect timing, not this criterion.",
         ha="center", fontsize=10)
fig.savefig(out / "chemical-rate-phase.png", dpi=180, bbox_inches="tight")
fig.savefig(out / "chemical-rate-phase.svg", bbox_inches="tight")
np.savetxt(out / "chemical-rate-phase-data.csv", np.c_[beta,h,threshold],
           delimiter=",", header="beta,h_beta,q_critical", comments="")
print(out / "chemical-rate-phase.png")
