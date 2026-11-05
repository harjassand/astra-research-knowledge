"""Reproduce the scoped calculations, not the unproved recovery converse."""
from pathlib import Path
import json
import math

import numpy as np
from scipy.integrate import quad
from scipy.special import gamma
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)


def toom(ones):
    candidates = set(ones)
    candidates.update((x - 1, y) for x, y in ones)
    candidates.update((x, y - 1) for x, y in ones)
    return {
        (x, y) for x, y in candidates
        if sum(z in ones for z in ((x, y), (x + 1, y), (x, y + 1))) >= 2
    }


def excess_moment(a, d, alpha):
    assert a >= 1 and alpha > d
    return float(gamma(d + 1) * gamma(alpha - d) / gamma(alpha) * a ** (d - alpha))


def cone_hazard(T, r0, v, lam, d, alpha):
    T = np.asarray(T)
    exponent = d + 1 - alpha
    coefficient = lam * 2 ** d * excess_moment(1, d, alpha)
    if abs(exponent) < 1e-12:
        return coefficient / v * np.log1p(v * T / r0)
    return coefficient / (v * exponent) * ((r0 + v * T) ** exponent - r0 ** exponent)


checks = []
for d, alpha in ((1, 2.0), (2, 2.5), (2, 3.0), (2, 4.0), (3, 5.0)):
    a, T, v, lam = 2.0, 7.0, 0.75, 0.03
    numerical, _ = quad(lambda r: (r-a)**d * alpha * r**(-alpha-1), a, np.inf)
    exact = excess_moment(a, d, alpha)
    numerical_hazard, _ = quad(lambda t: lam*2**d*excess_moment(a+v*t, d, alpha), 0, T)
    exact_hazard = float(cone_hazard(T, a, v, lam, d, alpha))
    assert math.isclose(numerical, exact, rel_tol=1e-8)
    assert math.isclose(numerical_hazard, exact_hazard, rel_tol=1e-10)
    # Independent big-burst footprint integral for a spacetime block.
    L = 3.0
    large_numeric, _ = quad(lambda r: (r+L)**d * alpha*r**(-alpha-1), L, np.inf)
    large_exact = alpha * L**(d-alpha) * sum(math.comb(d,j)/(alpha-j) for j in range(d+1))
    assert math.isclose(large_numeric, large_exact, rel_tol=1e-8)
    checks.append(dict(d=d, alpha=alpha, excess=exact, hazard=exact_hazard,
                       excess_relative_error=abs(numerical/exact-1),
                       large_burst_relative_error=abs(large_numeric/large_exact-1)))

left, right = {(1,0)}, {(0,1)}
assert toom(left) == toom(right) == set()
assert toom(left | right) == {(0,0)}
assert toom(toom(left | right)) == set()

plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":10,
                    "axes.spines.top":False, "axes.spines.right":False})
d, v, r0, flux = 2, 1., 1., .03
times = np.geomspace(1, 1e8, 600)
fig, axes = plt.subplots(1,2,figsize=(10,3.9), constrained_layout=True)
curves=[]
for alpha, color in ((2.5,"#b74f3b"),(3.,"#b0822b"),(4.,"#247a82")):
    mean_volume = 2**d * alpha/(alpha-d)
    lam = flux/mean_volume
    hazards=cone_hazard(times,r0,v,lam,d,alpha)
    errors=-np.expm1(-hazards)/2
    label=rf"$\alpha={alpha:g}$"
    axes[0].plot(times,errors,label=label,color=color,lw=2.3)
    axes[1].plot(times,hazards,label=label,color=color,lw=2.3)
    curves.append(dict(alpha=alpha, lam=lam, point_hit_rate=lam*mean_volume,
                       error_lower_bound_at_1e8=float(errors[-1])))
axes[0].set(xscale="log", xlabel="Elapsed time T", ylabel="Unavoidable binary error (lower bound)", ylim=(0,.51))
axes[0].axhline(.5,color="#777777",lw=.8,ls="--")
axes[1].set(xscale="log",yscale="log",xlabel="Elapsed time T",ylabel=r"Cumulative whole-cone erasures $\Lambda(T)$")
for ax in axes:
    ax.grid(True,which="major",alpha=.2)
    ax.legend(frameon=False,loc="upper left")
fig.savefig(FIGURES/"cone_erasure_bound.pdf")
fig.savefig(FIGURES/"cone_erasure_bound.png",dpi=210)
plt.close(fig)

receipt={"status":"PASS", "scope":"Closed-form identities and exact finite Toom examples only.",
         "integral_checks":checks,"toom_nonadditivity":True,
         "figure":{"d":d,"v":v,"r0":r0,"matched_point_hit_rate":flux,"curves":curves},
         "recovery_sufficiency_proved":False,"physical_validation_performed":False}
(RESULTS/"opening_checks.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"status":"PASS","integral_cases":len(checks),"toom_nonadditivity":True,
                  "recovery_sufficiency_proved":False}))
