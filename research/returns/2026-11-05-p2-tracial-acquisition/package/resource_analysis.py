#!/usr/bin/env python3
"""Exact formula evaluations for the tracial-collision research note.

These are analytic resource calculations, not large-bath simulations.
All errors use half the diamond distance. Run from any working directory.
"""
from pathlib import Path
import json
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

def first_integer(log_target, log_step):
    n = max(0, math.ceil(log_target / log_step))
    while n and (n-1)*log_step <= log_target:
        n -= 1
    while n*log_step > log_target:
        n += 1
    return n

def counts(theta, eps=0.01, d=2, m=1):
    c = 1-d**-2
    ell_log = math.log1p(-math.sin(theta)**4)
    # Exact explicit product-decoder condition: (1-c*r)^m >= 1-eps.
    r_upper = -math.expm1(math.log1p(-eps)/m)/c
    # Centered Renes necessary condition for arbitrary collective decoder.
    p_global = math.exp(-2*m*math.log(d))
    needed_petz = (1-eps)**2 + eps**2*p_global/(1-p_global)
    r_necessary = -math.expm1(math.log(needed_petz)/m)/c
    suff = first_integer(math.log(min(1.0, r_upper)), ell_log)
    nec = first_integer(math.log(min(1.0, r_necessary)), ell_log)
    source = first_integer(math.log(eps/c), 2*math.log(math.cos(theta)))
    return {
        "d": d, "modules": m, "theta": theta, "half_diamond_target": eps,
        "single_source_forgetting_collisions": source,
        "any_collective_decoder_necessary_collisions_per_module": nec,
        "reverse_decoder_sufficient_collisions_per_module": suff,
        "stored_output_qudits": m*suff,
        "source_collisions": m*suff,
        "inverse_collisions_without_routing": m*suff,
        "source_port_bank_routing_swaps_if_serial": m*suff*(suff-1)//2,
        "decoder_sweep_routing_swaps": m*max(0,suff-1),
        "two_qubit_gates_in_junction_layout": m*(suff*suff+5*suff-2)//2,
        "operation_qubits_in_junction_layout": m*(suff+2),
        "pulse_edge_configurations_upper_bound": m*(2*suff+1),
        "formula_status": "exact formula evaluation, not a many-body simulation"
    }

rows = [counts(th, m=m) for m in (1, 1000) for th in (0.05,0.1,0.2,0.4)]
report = {
    "error_convention": "epsilon = half diamond distance",
    "resource_count_scope": "Independent modules; arbitrary entangled input and collective final decoding. Routing follows finite supplement; count assumption must match that schedule.",
    "rows": rows,
}

plt.rcParams.update({"font.size": 10, "axes.labelsize": 10,
                    "axes.titlesize": 12, "legend.fontsize": 8.5,
                    "figure.dpi": 150, "savefig.dpi": 220,
                    "axes.spines.top": False, "axes.spines.right": False})
blue, orange, teal = "#245c9b", "#b96520", "#16857f"

theta, c, eps = 0.1, 0.75, 0.01
N = np.geomspace(1,200000,700)
log_r = N*np.log1p(-np.sin(theta)**4)
r = np.exp(log_r)
alpha = -np.expm1(log_r)
upper = c*r
lower = c*r/(1+np.sqrt(alpha))
source = c*np.exp(2*N*np.log(np.cos(theta)))
fig, axes = plt.subplots(1,2,figsize=(11.0,4.1),layout="constrained")
ax=axes[0]
ax.loglog(N,source,color=blue,lw=2,label="Source distance from mixed state (exact)")
ax.loglog(N,upper,color=orange,lw=2,label="Reverse decoder error (exact)")
ax.loglog(N,lower,color=orange,lw=1.4,ls="--",label="Every decoder: necessary error")
ax.fill_between(N,lower,upper,color=orange,alpha=.14)
ax.axhline(eps,color="0.5",ls=":",lw=1)
ax.set(xlabel="Number of fresh collisions N",ylabel="Half diamond distance",
       title=r"A. One qubit, $\theta=0.1$",ylim=(1e-6,1),xlim=(1,200000))
ax.legend(loc="lower left",frameon=False)
ax.grid(alpha=.15,which="major")
ths=np.geomspace(.025,.5,130)
rr=[counts(float(th)) for th in ths]
ns=np.array([x["single_source_forgetting_collisions"] for x in rr])
nl=np.array([x["any_collective_decoder_necessary_collisions_per_module"] for x in rr])
nu=np.array([x["reverse_decoder_sufficient_collisions_per_module"] for x in rr])
ax=axes[1]
ax.loglog(ths,ns,color=blue,lw=2,label=r"Source forgetting: $\Theta(\theta^{-2})$")
ax.loglog(ths,nu,color=orange,lw=2,label=r"Output recovery: $\Theta(\theta^{-4})$")
ax.loglog(ths,nl,color=orange,lw=1.4,ls="--")
ax.fill_between(ths,nl,nu,color=orange,alpha=.14)
ax.set(xlabel=r"Collision action $\theta$ (radians)",ylabel="Collisions to error 0.01",
       title="B. Necessary and sufficient budgets")
ax.legend(frameon=False,loc="upper right")
ax.grid(alpha=.15,which="major")
fig.savefig(FIG/"acquisition_clocks.png")
fig.set_size_inches(7.4, 6.6)
stacked = fig.add_gridspec(2,1)
for i,ax in enumerate(axes):
    ax.set_subplotspec(stacked[i,0])
fig.savefig(FIG/"acquisition_clocks.pdf")
plt.close(fig)

fig,axes=plt.subplots(1,2,figsize=(11,4.1),layout="constrained")
M=np.unique(np.geomspace(1,1e6,500).astype(int))
gh=5.
delta=gh/M
q=(-np.expm1(-delta))**2
log_r=M*np.log1p(-q)
alpha=-np.expm1(log_r)
bath_bound=np.minimum(1,.5*np.sqrt(3*alpha))
ax=axes[0]
ax.loglog(M,bath_bound,color=teal,lw=2,label="Entire bath distance from constant channel (upper bound)")
ax.axhline(c*np.exp(-gh),color=blue,lw=2,label="Source distance from mixed state (exact)")
ax.set(xlabel=r"Fresh collision count M in fixed interval $\gamma h=5$",
       ylabel="Half diamond distance",title="A. Identical source channel for every M")
ax.legend(frameon=False,loc="upper right",fontsize=8)
ax.grid(alpha=.15,which="major")
deltas=np.geomspace(1e-5,.7,500)
q=(-np.expm1(-deltas))**2
n=np.ceil(np.log(eps/c)/np.log1p(-q))
nsource=np.ceil(np.log(c/eps)/deltas)
ax=axes[1]
ax.loglog(deltas,n*deltas,color=orange,lw=2,label="Reverse decoder: collection time")
ax.loglog(deltas,nsource*deltas,color=blue,lw=2,label="Source forgetting time")
ax.set(xlabel=r"Dimensionless collision duration $\gamma\Delta$",
       ylabel=r"Dimensionless time $\gamma T$ to error 0.01",
       title="B. Fixed exact source relaxation rate")
ax.legend(frameon=False,loc="upper right")
ax.grid(alpha=.15,which="major")
fig.savefig(FIG/"same_source_dynamics.png")
fig.set_size_inches(7.4, 6.6)
stacked = fig.add_gridspec(2,1)
for i,ax in enumerate(axes):
    ax.set_subplotspec(stacked[i,0])
fig.savefig(FIG/"same_source_dynamics.pdf")
plt.close(fig)
(ROOT/"resource_counts.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps({"rows": rows,"figures":["acquisition_clocks.pdf","same_source_dynamics.pdf"]},indent=2))
