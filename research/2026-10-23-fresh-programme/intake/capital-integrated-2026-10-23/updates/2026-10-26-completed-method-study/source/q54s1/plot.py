#!/usr/local/bin/python3
"""Render the model construction. Re-run construct.py first to refresh data."""
from pathlib import Path
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.special import ndtr
from construct import hidden, M_LOWER, SAFE, TARGET, CENTER, SIGMA

HERE=Path(__file__).resolve().parent
plt.rcParams.update({'font.size':10, 'axes.spines.top':False, 'axes.spines.right':False,
                     'savefig.dpi':180, 'font.family':'DejaVu Sans'})
fig, axes=plt.subplots(1,3,figsize=(13.2,3.8),constrained_layout=True)
x=np.linspace(0,1,1200)
ax=axes[0]
ax.axvspan(0,SAFE,color='#d8e7db',alpha=.75,label='Allowed interrogation')
ax.plot(x,M_LOWER*x,color='#245d8c',lw=2,label=r'$f_0(x)=x$')
ax.plot(x,M_LOWER*x+hidden(x,.01),color='#b24e35',lw=2,label=r'$f_1(x)$, $\delta=0.01$')
ax.axvline(CENTER,color='#999999',ls=':',lw=1)
ax.scatter([TARGET,TARGET],[M_LOWER*TARGET,M_LOWER*TARGET+hidden(TARGET,.01)],color=['#245d8c','#b24e35'],zorder=4)
ax.annotate('Target force gap = 1.4',xy=(.97,1.7),xytext=(.21,1.55),arrowprops={'arrowstyle':'->','color':'#444444'},fontsize=9)
ax.set(xlabel='Displacement',ylabel='Force',title='A. Stable passive laws; hidden transition')
ax.legend(loc='upper left',fontsize=8,frameon=False)

ax=axes[1]
with (HERE/'rate_sweep.csv').open() as f:
    rows=list(csv.DictReader(f))
deltas=np.array([float(r['delta']) for r in rows])
counts=np.array([float(r['n_for_5pct_error_rounded_float']) for r in rows])
order=np.argsort(1/deltas)
ax.plot((1/deltas)[order],counts[order],color='#7d3d8b',marker='o',lw=1.8)
ax.set_yscale('log')
ax.set(xlabel=r'Inverse transition width, $1/\delta$',ylabel='Scalar force readings for 5% error',title='B. Exact optimal acquisition cost')
ax.grid(axis='y',alpha=.22)
ax.text(.04,.94,r'Known pair; Gaussian noise $\sigma=10^{-3}$',transform=ax.transAxes,va='top',fontsize=8)

ax=axes[2]
n=np.geomspace(1,5000,500)
eps=float(hidden(SAFE,.025))
diff=eps-float(hidden(SAFE-.05,.025))
ax.plot(n,ndtr(-np.sqrt(n)*eps/(2*SIGMA)),label='Endpoint: exact adaptive optimum',color='#245d8c',lw=2)
ax.plot(n,ndtr(-np.sqrt(n)*diff/(4*SIGMA)),label='Paired finite differences',color='#b24e35',lw=2)
ax.set_xscale('log')
ax.set(xlabel='Same total scalar force readings',ylabel='Hypothesis error probability',title=r'C. Differential bridge loses ($\delta=0.025$)',ylim=(0,.51))
ax.grid(axis='y',alpha=.22)
ax.legend(loc='upper right',fontsize=8,frameon=False)
fig.suptitle('Q54: a mathematical obstruction to uniform safe extrapolation',fontsize=13)
fig.savefig(HERE/'construction.png')
fig.savefig(HERE/'construction.pdf')
