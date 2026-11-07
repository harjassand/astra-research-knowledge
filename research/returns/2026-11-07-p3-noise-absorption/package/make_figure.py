"""Scientific figure; curves from exact model formulas, not experimental data."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from operating_regime import binomial_tv

ROOT=Path(__file__).resolve().parent
plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False})
fig,axs=plt.subplots(1,2,figsize=(11.8,4.5),layout="constrained")
p=np.geomspace(.001,.49,250)
axs[0].loglog(p,1/(p*(1-p)),color="#1864ab",lw=2.5,label="Optimal total reset rate: 1/[p(1−p)]")
axs[0].loglog(p,2/p,color="#f08c00",lw=2,label="Four-actuator reset menu, uncapped: 2/p")
axs[0].set(xlabel="Minority target population p",ylabel="Required total reset rate / background rate",
           title="Known noise has a temperature-dependent rate price")
axs[0].grid(alpha=.2,which="both");axs[0].legend(frameon=False,fontsize=8,loc="upper right")
ns=np.unique(np.logspace(0,8,220).astype(int))
tv=[binomial_tv(int(n),.2,.202) for n in ns]
axs[1].semilogx(ns,tv,color="#2b8a3e",lw=2.5,label="Whole physical state")
axs[1].axhline(.002,color="#c92a2a",ls="--",lw=1.8,label="One factor: 0.002")
axs[1].set(xlabel="Number of factors N",ylabel="Trace distance",ylim=(-.02,1.04),
           title="Fixed local bias does not give fixed global accuracy")
axs[1].grid(alpha=.2);axs[1].legend(frameon=False,fontsize=9,loc="center left")
fig.suptitle("Local noise absorption: activity and information limits",fontsize=15,fontweight="bold")
fig.supxlabel("Exact declared-model formulas. Right: p=0.200 versus q=0.202; any common unitary dressing preserves global distance.",fontsize=9)
fig.savefig(ROOT/"NOISE_ACTIVITY_AND_CALIBRATION.png",dpi=180)
fig.savefig(ROOT/"NOISE_ACTIVITY_AND_CALIBRATION.svg")
