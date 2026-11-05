#!/usr/bin/env python3
"""Scientific figures from saved records; plots are diagnostics, not proofs."""
from pathlib import Path
from fractions import Fraction
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent
d=json.loads((P/'physical_bridge_results.json').read_text())
tr=json.loads((P/'trajectory_traces.json').read_text())
cp=json.loads((P.parent/'independent'/'passive_compiler_path.json').read_text())
cr=json.loads((P.parent/'independent'/'passive_compiler_results.json').read_text())
complete=json.loads((P/'complete_operation_results.json').read_text())
f=lambda s:float(Fraction(s))
rates=np.r_[0.,np.geomspace(1e-8,1e6,63)]
weights=.6+np.cos(np.arange(64)*.71)**2;weights[0]*=5;weights/=weights.sum()
mr=np.array([f(m['pole']) for m in d['fit']['model']])
mw=np.array([f(m['weight']) for m in d['fit']['model']])
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,
                     'axes.spines.right':False,'axes.labelcolor':'#253546',
                     'text.color':'#253546','axes.titleweight':'bold'})
t=np.geomspace(1e-6,1,800)
fig,ax=plt.subplots(figsize=(7.3,3.2),layout='constrained')
ax.plot(t,np.exp(-np.outer(t,rates))@weights,lw=2,label='Original kernel (source diagnostic)',color='#253546')
ax.plot(t,np.exp(-np.outer(t,mr))@mw,lw=1.8,label='Acquired six-mode model',color='#167b91')
first=float(Fraction(1,32)/8)
ax.axvspan(1e-6,first,color='#e8edf2',alpha=.85,zorder=-1)
ax.axvline(first,color='#7f8c99',ls=':',lw=1)
ax.text(2e-6,.59,'No kernel samples here',fontsize=9,color='#596674')
ax.set_xscale('log');ax.set_xlim(1e-6,1);ax.set_ylim(.54,1.02)
ax.set_xlabel('Time after the ideal impulse');ax.set_ylabel('Kernel strength')
ax.set_title('Integrated accuracy permits unresolved fast response',loc='left',fontsize=12)
ax.legend(loc='upper right',frameon=False,fontsize=8.5)
fig.savefig(P/'kernel_figure.png',dpi=220);plt.close(fig)
t=np.array(tr['time']);truth=np.array(tr['dc_true'])
knots=np.array([[f(a),f(b)] for a,b in cp['knots']])
compiled=np.interp(t,knots[:,0],knots[:,1])
err=abs(compiled-truth);bound=complete['final_uniform_trajectory_bound']
fig,axs=plt.subplots(1,2,figsize=(7.3,3.05),layout='constrained')
ax=axs[0]
ax.fill_between(t,compiled-bound,compiled+bound,color='#cce8ec',alpha=.8,label='Certified error band')
ax.plot(t,truth,color='#253546',lw=2,label='Source simulation')
ax.plot(t,compiled,color='#167b91',lw=1.5,ls='--',label='Finite compiled path')
ax.set_xlabel('Deployment time');ax.set_ylabel('Observed coordinate')
ax.set_title('A DC query after acquisition',loc='left',fontsize=11)
ax.legend(loc='upper left',frameon=False,fontsize=7.5)
ax=axs[1]
ax.semilogy(t,np.maximum(err,1e-10),color='#167b91',lw=1.6,label='Sampled source/path discrepancy')
ax.axhline(bound,color='#b56d28',ls='--',label='Uniform theorem bound')
ax.set_xlim(0,1);ax.set_ylim(1e-8,.03)
ax.set_xlabel('Deployment time');ax.set_ylabel('Absolute error')
ax.set_title('Diagnostic and certificate differ',loc='left',fontsize=11)
ax.legend(loc='lower right',frameon=False,fontsize=7.1)
fig.savefig(P/'trajectory_figure.png',dpi=220);plt.close(fig)
print(json.dumps({'compiled_path_sampled_max_error':float(max(err)),
                  'uniform_certified_bound':bound}))
