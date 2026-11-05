#!/usr/bin/env python3
"""Render the same analytic curves in a readable portrait report layout.

This performs no new simulation or verification. It imports the formulas
used by compute_resource_law.py and changes only the figure composition.
"""
from pathlib import Path
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from compute_resource_law import log_meter_bias, log_full_cq_factor, LN10, SUFFICIENT_PREFACTOR

plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 9,
    'axes.titlesize': 10, 'axes.labelsize': 9, 'legend.fontsize': 8,
    'axes.spines.top': False, 'axes.spines.right': False,
    'pdf.fonttype': 42, 'savefig.facecolor': 'white',
})
fig, axes = plt.subplots(2, 1, figsize=(6.3, 7.1))
fig.subplots_adjust(left=.13, right=.98, top=.90, bottom=.13, hspace=.56)
fig.suptitle('The cost of acquiring global coherence', x=.13, y=.985,
             ha='left', fontsize=12, fontweight='semibold')
fig.text(.13, .946, 'Independent hidden dephasing; initially unencoded source',
         fontsize=8.5, color='#4c5863')
n, k = 1000, 2
r = np.geomspace(1, 1e4, 700)
lower = np.maximum(0, math.log(2/3)-n*log_full_cq_factor(r,k))/LN10
upper = (math.log(SUFFICIENT_PREFACTOR)-2*n*log_meter_bias(r))/LN10
ax=axes[0]
ax.plot(r, upper, color='#2763ad', lw=2, label='Sufficient local-meter copies')
ax.plot(r, lower, color='#a34261', lw=2, ls='--', label='Copy lower bound, including feedback')
ax.set(xscale='log', xlim=(1,1e4), ylim=(-12,915),
       xlabel=r'Control / dephasing, $\Omega/\lambda$',
       ylabel=r'$\log_{10}$(copy-count bound)')
ax.set_title(r'(a) $n=1{,}000$, $k=2$; error at most $1/3$', loc='left', pad=9)
ax.legend(frameon=False, loc='upper right')
ax.text(.98,.47,'Distinct bounds; the gap is not\na statistical confidence interval.',
        ha='right', transform=ax.transAxes, color='#58636d', fontsize=8)
n=np.geomspace(10,1e4,600)
families=[(np.full_like(n,100.),r'$\Omega/\lambda=100$','#2763ad','-'),
          (n/np.log(n),r'$\Omega/\lambda=n/\ln n$','#c47626','--'),
          (n,r'$\Omega/\lambda=n$','#258273',':')]
ax=axes[1]
for r,label,color,style in families:
    ax.plot(n,-2*n*log_meter_bias(r)/LN10,label=label,color=color,ls=style,lw=2)
ax.set(xscale='log',xlim=(10,1e4),ylim=(-2,145),
       xlabel=r'Number of source qubits, $n$',
       ylabel=r'$\log_{10}$(meter overhead $\beta^{-2n}$)')
ax.set_title('(b) Fixed, polynomial, and bounded-copy regimes',loc='left',pad=9)
ax.legend(frameon=False,loc='upper left')
ax.text(.40,.47,'Fixed control: exponential overhead\n'
        r'$n/\ln n$: polynomial overhead'+'\n'+r'$n$: bounded overhead',
        transform=ax.transAxes,color='#58636d',fontsize=8,linespacing=1.65)
for ax in axes:
    ax.grid(which='major',color='#d9dfe4',lw=.7)
    ax.set_axisbelow(True)
fig.text(.13,.025,'Analytic model calculations. Preparation, calibration, and protected-memory costs are additional.',
         fontsize=7.3,color='#58636d')
root=Path(__file__).resolve().parent
fig.savefig(root/'resource_law_report.pdf')
fig.savefig(root/'resource_law_report.png',dpi=190)
plt.close(fig)
print('Saved resource_law_report.pdf and resource_law_report.png')
