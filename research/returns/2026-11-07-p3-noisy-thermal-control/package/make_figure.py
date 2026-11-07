"""Static scientific figure: one analytic law and one labeled finite fixture."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

p=Path(__file__).resolve().parent
r=json.loads((p/"FINITE_QUANTUM_DIAGNOSTIC.json").read_text())
plt.rcParams.update({"font.size":11,"axes.spines.top":False,"axes.spines.right":False})
fig,ax=plt.subplots(1,2,figsize=(11.5,4.5),layout="constrained")
g=np.linspace(0,.97,400)
ax[0].plot(g,1/(1-g),lw=2.6,color="#1c6685")
ax[0].axvline(.25,color="#bc6c25",ls="--",lw=1)
ax[0].scatter([.25],[4/3],color="#bc6c25",zorder=5)
ax[0].set(xlabel="Modeled actuator gain g",ylabel="Repair rate / background rate",
          title="Exact scalar balance: x = b / (1 − g)",ylim=(0,20),xlim=(0,1))
ax[0].text(.03,.89,"Specific repair law;\nnot a hardware noise threshold",transform=ax[0].transAxes,fontsize=10)
rows=r["joint_reference_trajectory"]
ax[1].semilogy([z["time"] for z in rows],[z["joint_trace_distance"] for z in rows],"o-",lw=2,color="#1c6685")
ax[1].set(xlabel="Time in the declared generator units",ylabel="Joint trace distance to σ ⊗ ρR",
          title="Noncommuting 3-qubit constructed model")
ax[1].text(.03,.12,"Retained entangled reference\nBinary64 diagnostic; no apparatus data",transform=ax[1].transAxes,fontsize=10)
fig.suptitle("Noisy thermal control: repair cost and complete-output behavior",fontsize=14)
fig.savefig(p/"NOISY_THERMAL_CONTROL.png",dpi=190)
fig.savefig(p/"NOISY_THERMAL_CONTROL.svg")
print("Saved figure")
