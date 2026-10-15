"""Plot extracted CSV with system Matplotlib, absent in bundled Python.

Source workbooks are read only by analyze_conductance.py in bundled Python.
"""
from pathlib import Path
import csv
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
BASE = Path(__file__).resolve().parents[1]
results = json.loads((BASE / "evidence" / "conductance_analysis.json").read_text())
minimum = results["minimum"]
def values(name):
    with (BASE / "evidence" / f"published_{name}_values.csv").open() as stream:
        return [dict(time_hours=float(r["time_hours"]), value=float(r["value"]))
                for r in csv.DictReader(stream)]
ed, ref, voltage = values("ed"), values("reference"), values("voltage")
plt.rcParams.update({"font.size": 10})

fig, axes = plt.subplots(2, 1, figsize=(9, 6), sharex=True,
                         gridspec_kw={"height_ratios": [2, 1]}, constrained_layout=True)
axes[0].plot([x["time_hours"] for x in ed], [x["value"] for x in ed],
             color="#176b9b", label="Dilution cell")
axes[0].plot([x["time_hours"] for x in ref], [x["value"] for x in ref],
             color="#606870", label="Reference cell")
axes[0].axhline(0.5, color="#999999", lw=0.7, ls=":")
axes[0].scatter([minimum["time_hours"]], [minimum["value"]], color="#176b9b", s=28)
axes[0].annotate(f"Minimum {minimum['value']:.4f} at {minimum['time_hours']:.2f} h",
                 xy=(minimum["time_hours"], minimum["value"]),
                 xytext=(44, 0.61), arrowprops=dict(arrowstyle="-", lw=.7))
axes[0].set_ylabel("Conductance / initial conductance")
axes[0].set_ylim(0.44, 1.06)
axes[0].legend(loc="lower right", frameon=False)
axes[0].set_title("Published KCl electrodialysis experiment: acquired source values")
axes[1].plot([x["time_hours"] for x in voltage], [x["value"] for x in voltage],
             lw=0.7, color="#8c4666")
axes[1].set_ylabel("Output voltage (mV)")
axes[1].set_xlabel("Elapsed time (hours)")
axes[1].set_xlim(0, 96)
for axis in axes:
    axis.spines[["top", "right"]].set_visible(False)
    axis.grid(axis="y", alpha=0.18)
fig.savefig(BASE / "evidence" / "published_conductance.png", dpi=170)
print(json.dumps(results, indent=2))
