"""Regenerate the scientific figure from the independent audit results."""
import os
os.environ.setdefault('MPLCONFIGDIR','producer-workspace/astra_plot_config')
from pathlib import Path
import json,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parent
r=json.loads((root.parent/'independent/audit_gaussian_extension_results.json').read_text())['records'][-1]
fig,ax=plt.subplots(figsize=(8,5))
for key,color,name in [('neumann','#3b6d9a','Neumann'),('chebyshev','#ab4a24','Chebyshev')]:
    d=r[key];x=[v['order'] for v in d]
    ax.semilogy(x,[v['relative_error'] for v in d],marker='o',color=color,label=name+' observed error')
    ax.semilogy(x,[v['bound'] for v in d],linestyle='--',color=color,alpha=.8,label=name+' proved bound')
ax.set(xlabel='Polynomial degree',ylabel='Relative error in the mean',title='Controlled nonintegrable kinetics under disorder')
ax.grid(alpha=.2);ax.legend(frameon=False,fontsize=9)
fig.text(.12,.015,'8 wall coordinates; two-spectator rate multiplier; full-state inverse used only to check the answer.',fontsize=9)
fig.tight_layout(rect=(0,.04,1,1))
fig.savefig(root/'convergence.png',dpi=170);fig.savefig(root/'convergence.svg')
