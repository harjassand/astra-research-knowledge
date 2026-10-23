#!/usr/bin/env python3
"""A figure of the proved law; no simulation, fitting, or asymptotic estimation."""
from pathlib import Path
import hashlib
import io
import json
import math
import resource
import time
import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "phase_law"
OUT.mkdir(parents=True, exist_ok=True)
wall = time.perf_counter()
cpu = time.process_time()
# Unchanged illustrative constants from Cycle10, not a fitted case.
K, alpha, d, s = 1.0, 0.5, 3.0, -1.0
beta = 1-alpha
r = alpha*math.exp(-K)/beta
b0 = -math.expm1(-K)
gamma = math.log1p(r)
t = r/(1+r)
d_star = gamma/t
x_star = d_star/d
B = d*t-gamma
xs = sorted(set([i/600 for i in range(601)] + [x_star]))
psi = [min(B*x, gamma*(1-x)) for x in xs]
transport = [b0*math.exp(-s-z) for z in psi]
ys = [max(K,y) for y in transport]
limsup = max(K,b0*math.exp(-s))
liminf = max(K,b0*math.exp(-s-gamma*(1-d_star/d)))
values = {
    "scope": "Formula evaluation of the proved unrestricted minimax profile; not finite-chain data",
    "parameters": {"K": K, "alpha": alpha, "d": d, "s": s},
    "d_star": d_star, "minimum_phase": x_star,
    "exact_formula_liminf_numeric": liminf,
    "exact_formula_limsup_numeric": limsup,
    "ordinary_IMH_amplitude": K,
    "phase": xs, "profile": ys
}
(OUT/"VALUES.json").write_text(json.dumps(values,indent=2)+"\n")
plt.rcParams.update({"font.size":11,"axes.spines.top":False,
                     "axes.spines.right":False})
fig,ax=plt.subplots(figsize=(9.4,5.6),layout="constrained")
ax.plot(xs,ys,color="#006B70",lw=2.6,label="Proved unrestricted hybrid amplitude")
ax.axhline(K,color="#555555",lw=1.8,ls="--",label="Ordinary IMH amplitude K")
ax.scatter([0,x_star,1],[limsup,liminf,limsup],color="#006B70",s=30,zorder=4)
ax.annotate(f"Exact limsup  {limsup:.6f}",(0,limsup),
            xytext=(18,-24),textcoords="offset points",color="#005459")
ax.annotate(f"Exact liminf  {liminf:.6f}",(x_star,liminf),
            xytext=(10,-29),textcoords="offset points",color="#005459")
ax.set(xlim=(0,1),ylim=(0.93,1.83),
       xlabel=r"Phase  $\{\eta_n\log n/d\}$",
       ylabel=r"Leading amplitude of  $(\log n)R_n$")
ax.set_title("Exact minimax critical amplitude",loc="left",fontsize=16,pad=24)
ax.text(0,1.025,"K = 1    α = 1/2    d = 3    s = −1",
        transform=ax.transAxes,fontsize=10.5,color="#444444")
ax.grid(axis="y",alpha=.18)
ax.legend(loc="upper center",bbox_to_anchor=(.5,-.14),frameon=False,ncol=1)
fig.text(.99,.005,"Exact formula • no chain simulation",ha="right",
         fontsize=9,color="#555555")
buf=io.BytesIO()
fig.savefig(buf,format="png",dpi=180)
payload=buf.getvalue()
dest=OUT/"critical_minimax_phase.png"
with dest.open("wb") as f:
    for start in range(0,len(payload),16384):
        assert f.write(payload[start:start+16384])==len(payload[start:start+16384])
assert dest.read_bytes()==payload
with Image.open(dest) as im:
    im.verify()
plt.close(fig)
receipt={
    "utc_finished":datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "cpu_seconds":time.process_time()-cpu,
    "wall_seconds":time.perf_counter()-wall,
    "max_rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    "scope":"Formula visualization and checked image export, not discovery or scientific replay",
    "png_bytes":len(payload),"png_sha256":hashlib.sha256(payload).hexdigest(),
    "discovery_inference_design_totals":"unknown"
}
(OUT/"RESOURCE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"liminf":liminf,"limsup":limsup,"resources":receipt},indent=2))
