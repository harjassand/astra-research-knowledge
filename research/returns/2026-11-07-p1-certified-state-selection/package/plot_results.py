"""Scientific figure from the executed trace and mathematical certificates."""
from pathlib import Path
from fractions import Fraction as Q
import csv,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
p=json.loads((ROOT/'results/PLAN.json').read_text())
v=json.loads((ROOT/'results/VERIFICATION.json').read_text())
q=lambda k:float(Q(p[k]))
trace=np.genfromtxt(ROOT/'results/TRACE.csv',delimiter=',',names=True)
t=np.linspace(0,q('total_retention_law_duration'),600)
family=100*(q('source_only_equilibrium_relative_error')+
    (q('handover_transient_coefficient')*np.exp(-q('full_state_local_contraction_rate')*t)+
     q('retention_error_floor'))/min(float(Q(x)) for x in p['target_amplitudes']))
settle=q('settling_time_after_switch')
posterior=100*float(Q(v['a_posteriori_continuous_relative_port_error']))
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
fig,(ax,bx)=plt.subplots(2,1,figsize=(10,7.2),sharex=True,gridspec_kw={'height_ratios':[2,1]})
ax.plot(t,family,color='#164b75',lw=2.4,label='Uniform bound over the source/error family')
ax.plot(trace['time_after_switch'],100*trace['relative_port_error_to_nominal'],
        color='#9b4a0c',lw=1.5,label='Executed port record (displayed at reduced density)')
ax.hlines(5,settle,t[-1],color='#164b75',ls='--',lw=1.3,label='Requested 5% family guarantee')
ax.hlines(posterior,settle,t[-1],color='#158267',ls='--',lw=2,
          label='Complete-record certificate: below 0.02%')
ax.axvspan(settle,t[-1],color='#158267',alpha=.07)
ax.set_yscale('log');ax.set_ylim(0.0001,30)
ax.set_ylabel('Maximum relative port error (%)')
ax.set_title('Finite write, certified handover, sustained collective pattern',loc='left',fontweight='bold',pad=14)
ax.grid(True,which='major',alpha=.18)
ax.legend(loc='center left',fontsize=9,frameon=True,framealpha=.95)
commands=np.vstack([trace[f'command{i+1}'] for i in range(6)]).T
bx.plot(trace['time_after_switch'],np.linalg.norm(commands,axis=1),color='#7142a0',lw=1.8,label='Executed held-command norm')
bx.axhline(q('retention_ideal_command_norm_upper')+q('control_evaluation_error_L2'),
           color='#7142a0',ls=':',label='Certified command range')
bx.axvspan(settle,t[-1],color='#158267',alpha=.07)
bx.set_ylabel('Drive command norm')
bx.set_xlabel('Source time after handover (nine-unit write already completed)')
bx.set_ylim(0,7.5);bx.grid(True,alpha=.18);bx.legend(loc='lower left',fontsize=9)
fig.text(.095,.018,'512 hidden software-source states; 6 accessible ports. Bounds include bounded adversarial errors and actuator lag.\nVirtual source time and software execution do not establish a physical real-time implementation.',fontsize=9,color='#444444')
fig.tight_layout(rect=(0,.065,1,1))
fig.savefig(ROOT/'results/SELECTION_CERTIFICATES.png',dpi=180)
fig.savefig(ROOT/'results/SELECTION_CERTIFICATES.svg')
plt.close(fig)
