"""Scientific plot of mathematical bounds; no experimental data."""

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent


def main():
    plt.rcParams.update({"font.size": 11, "axes.spines.top": False,
                         "axes.spines.right": False, "savefig.dpi": 180})
    n = np.logspace(2, 8, 500)
    lam, r, b, e = 1., 10., 15., .01
    fig, axes = plt.subplots(1, 3, figsize=(15.8, 4.9))
    colors = ["#1465a2", "#d36a20"]
    for degree, color, label in [(0, colors[0], "Product target"),
                                  (4, colors[1], "Graph target, degree at most 4")]:
        D = degree + 1
        C = (b * np.sqrt(D) + np.sqrt(D * b * b + lam * (lam + D * r))) / lam
        cap = C * C / (n + C * C)
        axes[0].loglog(n, cap, color=color, lw=2.4, label=label)
        drift_loss = n * lam * (1 - e) - (lam + D * r) * e - 2 * b * np.sqrt(D * n * e * (1 - e))
        valid = drift_loss > 0
        axes[2].loglog(n[valid], e / drift_loss[valid], color=color, lw=2.4, label=label)
    axes[0].axhline(.99, color="#555555", ls=":", lw=1.4, label="Requested fidelity 0.99")
    axes[0].set(xlabel="Number of physical output qubits N", ylabel="Universal fidelity upper bound",
                title="A   Fixed local strength loses global fidelity", ylim=(5e-6, 1.15))
    axes[0].legend(fontsize=8.7, loc="lower left")
    axes[0].text(.97, .93, "λ = 1; return bound = 10/site\nCoupling bound = 15/site",
                 transform=axes[0].transAxes, fontsize=8.3, va="top", ha="right",
                 bbox={"facecolor": "white", "edgecolor": "none", "alpha": .85})
    generic = lam * (n * (1 - e) - e) / (e + 2 * np.sqrt(n * e * (1 - e)))
    absorbing = lam * (n * (1 - e) / e - 1)
    axes[1].loglog(n, generic, color="#1465a2", lw=2.4, label="General coherent controllers: necessary")
    axes[1].loglog(n, absorbing, color="#8d3a74", lw=2.4, label="Target-preserving controllers: necessary")
    axes[1].loglog(n, n / e, color="#333333", lw=1.5, ls="--", label="Ideal pumps: stationary sufficiency")
    axes[1].set(xlabel="Number of physical output qubits N", ylabel="Rate or coupling / λ",
                title="B   Strength must grow for 99% fidelity")
    axes[1].legend(fontsize=8.2, loc="upper left")
    axes[2].set(xlabel="Number of physical output qubits N", ylabel="Maximum uninterrupted 99% interval × λ",
                title="C   Even perfect initialization has a deadline")
    axes[2].legend(fontsize=8.7, loc="lower left")
    for ax in axes:
        ax.grid(True, which="major", alpha=.18)
        ax.set_xlim(1e2, 1e8)
    fig.suptitle("Complete physical output under independent local noise and bounded control", fontsize=16, y=.99)
    fig.text(.5, .015, "Mathematical bounds with arbitrary auxiliary systems. No device measurements. The optimum for general coherent control is not asserted.",
             ha="center", fontsize=9)
    fig.tight_layout(rect=(0, .045, 1, .94), w_pad=2.5)
    for ext in ("png", "svg"):
        fig.savefig(HERE / f"PHYSICAL_OUTPUT_LIMITS.{ext}")
    print("Saved PHYSICAL_OUTPUT_LIMITS.png and PHYSICAL_OUTPUT_LIMITS.svg")


if __name__ == "__main__":
    main()
