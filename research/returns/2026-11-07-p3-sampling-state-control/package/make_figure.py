"""Static scientific figure from exact compiler counts and algebraic errors."""
import math
from pathlib import Path
from fractions import Fraction as F
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sampling_control import compile_plan, compile_fair_bit_plan

root=Path(__file__).resolve().parent
Ns=np.unique(np.logspace(2,6,25).astype(int))
caps={m:[] for m in ['global','per_cell']}
for N in Ns:
    for mode in caps:
        p=compile_plan(int(N),F(11,40),F(13,56),F(193,476),
                       F(1,1000),F(1,1000),F(1,1000),mode,F(9,10))
        r=compile_fair_bit_plan(p,F(31,152),F(13,56),F(1,1000))
        caps[mode].append(r['source_total_with_control'])
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
fig,axs=plt.subplots(1,2,figsize=(13,5.2),layout='constrained')
axs[0].loglog(Ns,caps['global'],label='Shared total cap',color='#1664a5',lw=2.5)
axs[0].loglog(Ns,caps['per_cell'],label='Separate cap at each site',color='#bb6509',lw=2.5)
axs[0].set(xlabel='Site-output slots K',ylabel='Hard cap on raw probe outcomes',
           title='Bounded information and randomness supply')
axs[0].legend(frameon=False,loc='upper left')
axs[0].grid(alpha=.2,which='major')
axs[0].text(.02,.03,'Includes fair-bit extraction.\nNative reset, readout and holding costs are additional.',
            transform=axs[0].transAxes,fontsize=9,color='#555555')

w=np.linspace(.42,.66,700)
ea=np.abs(.1+.3*w-.25)
eb=np.abs(1/18+w/3-.25)
axs[1].plot(w,ea,label='Apparatus A',color='#1664a5',lw=2)
axs[1].plot(w,eb,label='Apparatus B',color='#bb6509',lw=2)
axs[1].plot(w,np.maximum(ea,eb),label='Worst of the two',color='#303846',lw=2.5,ls='--')
axs[1].scatter([31/57],[1/76],color='#b0263a',zorder=5,s=35)
axs[1].annotate('Unavoidable error 1/76',xy=(31/57,1/76),xytext=(.45,.047),
                arrowprops={'arrowstyle':'->','color':'#b0263a'},color='#8b2031')
axs[1].set(xlabel='Probability of choosing the hot setting',ylabel='One-site trace error',
           title='Identical probes can hide different physical states',ylim=(0,.07))
axs[1].legend(frameon=False,loc='upper right',fontsize=9)
axs[1].grid(alpha=.2)
fig.suptitle('Source-driven state control: a constructive gain and a necessary calibration anchor',fontsize=15)
fig.savefig(root/'SAMPLING_COST_AND_ANCHOR.png',dpi=180)
fig.savefig(root/'SAMPLING_COST_AND_ANCHOR.svg')
print('Saved scientific figure.')
