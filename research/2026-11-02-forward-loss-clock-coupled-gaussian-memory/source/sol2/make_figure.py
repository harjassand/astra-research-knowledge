#!/usr/bin/env python3
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent
x=json.loads((P/'results/loss_clock_checks.json').read_text())['stiffness_sweep']
y=json.loads((P/'results/retained_process_check.json').read_text())
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,axs=plt.subplots(1,3,figsize=(13.3,3.8),layout='constrained')
rr=[r['R'] for r in x]
ax=axs[0]
ax.loglog(rr,[r['generic_normalized_dissipation_over_window'] for r in x],'o-',color='#9b4167',label=r'Normalized loss time $\tau\|L\|^2$')
ax.loglog(rr,[r['first_event']['actual_envelope_mass'] for r in x],'s-',color='#167a75',label=r'Computed clock mass $W(\tau)$')
ax.axhline(72,color='#167a75',ls='--',alpha=.6,label=r'Proved bound $18KM=72$')
ax.set(xlabel='Fast scale R',ylabel='Dimensionless source parameter',title='One slow mode remains')
ax.legend(fontsize=8,loc='upper left')
ax=axs[1]
ax.semilogx(rr,[r['prefix_source']['time_bits'] for r in x],'o-',color='#2467a8')
ax.set(xlabel='Fast scale R',ylabel='Bits / coherent prefix levels',title='CDF circuit resolves time in bits',ylim=(22,48))
ax.text(.04,.93,'43 bits address 8.8 trillion cells\nwith 43 coherent prefix levels',transform=ax.transAxes,va='top',fontsize=9)
ax=axs[2]
z=y['refinements']
ax.loglog([r['resolution'] for r in z],[r['diamond_upper_from_numerical_Choi'] for r in z],'o-',color='#167a75',label='Source-derived retained process')
ax.axhline(y['reset_bath_between_windows_Choi_trace_distance'],color='#9b4167',ls='--',label='Resetting bath: Choi distance')
ax.set(xlabel='Quadrature refinement',ylabel='Finite channel error diagnostic',title='Noncommuting intermediate control')
ax.legend(fontsize=8,loc='lower left')
fig.suptitle('Loss-clock identities and finite process checks',fontsize=14)
fig.savefig(P/'results'/'loss_clock_construction.png',dpi=180)
fig.savefig(P/'results'/'loss_clock_construction.pdf')
print('saved source-parameter and finite-channel figure')
