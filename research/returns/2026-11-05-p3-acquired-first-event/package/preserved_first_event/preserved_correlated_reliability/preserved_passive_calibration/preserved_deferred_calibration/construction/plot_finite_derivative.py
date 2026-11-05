import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent
d=json.loads((p/"finite_derivative_diagnostic.json").read_text())
plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False,
                     "pdf.fonttype":42})
fig,ax=plt.subplots(figsize=(7.0,3.6))
colors=["#185f9c","#c15f1a","#2a855d","#885ca3","#b2414b"]
for row,color in zip(d["coefficient_checks"][:5],colors):
    ax.semilogy([x["degree"] for x in row["estimates"]],
                [x["absolute_error"] for x in row["estimates"]],
                marker="o",markersize=4,label=row["label"],color=color)
ax.set_xlabel("Interpolation degree")
ax.set_ylabel("Absolute coefficient error")
ax.set_xticks([3,4,5,6,8,10])
ax.set_title("Finite interpolation of calculated output correlations",loc="left",pad=12)
ax.grid(axis="y",alpha=.22)
ax.legend(ncol=5,frameon=False,loc="lower left")
fig.tight_layout()
fig.savefig(p/"finite_derivative_convergence.pdf")
fig.savefig(p/"finite_derivative_convergence.png",dpi=170)
