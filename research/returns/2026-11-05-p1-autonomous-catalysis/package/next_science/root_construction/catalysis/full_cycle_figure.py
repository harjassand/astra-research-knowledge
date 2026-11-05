from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
d=json.loads((HERE/'thermal_competition_results.json').read_text())
p=json.loads((ROOT/'observation2'/'pulse_resource_bounds.json').read_text())['parameters']
audit=json.loads((ROOT/'transfer'/'catalytic_poisson_audit_results.json').read_text())[1]['capture_on_minus_capture_off']
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,axs=plt.subplots(1,3,figsize=(13,4.3),layout='constrained')
points=d['S16_digitization']['points']
axs[0].errorbar([x['overpotential_mV'] for x in points],[x['gain_digitized'] for x in points],
 yerr=[x['gain_pixel_error_halfwidth'] for x in points],fmt='o-',color='#9440a2',lw=1.7,ms=4)
axs[0].set(title='A. Published turnover gain',xlabel='Overpotential (mV)',ylabel='Modified / bare TOF',ylim=(2.95,3.65))
axs[0].text(.02,.03,'Geometric digitization error only;\nnot an experimental confidence interval.',transform=axs[0].transAxes,fontsize=8,color='#555555')
J0=4.0; G=3.3
for I,label,color in [(p['I_exponential_s'],'Decaying barrier pulse','#087f8c'),(p['I_rectangle_s'],'Optimistic rectangular pulse','#d07832')]:
 m=np.geomspace(1,.99/(J0*I),450)
 axs[1].semilogx(m,1/(1-J0*m*I),color=color,label=label)
 req=(1-1/G)/(J0*I)
 axs[1].scatter([req],[G],color=color,s=24)
 axs[1].annotate(f'{req:,.0f}',(req,G),xytext=(0,8),textcoords='offset points',ha='center',fontsize=8,color=color)
axs[1].axhline(G,color='#777777',ls=':',lw=1)
axs[1].set(title='B. Complete-cycle resource bound',xlabel='Received pulses per target turnover, m',ylabel='Upper bound on turnover gain',ylim=(.95,5),xlim=(1,1e5))
axs[1].legend(loc='upper left',fontsize=7.5)
axs[1].text(.02,.03,'Conditional: J₀ = 4 s⁻¹, T = 298 K,\nΔbarrier = 0.192 eV, lifetime = 41 ns.',transform=axs[1].transAxes,fontsize=8,color='#555555')
vals=[float(audit['changed_channel_contributions']['capture']),float(audit['changed_channel_contributions']['ordinary']),float(audit['net_change'])]
axs[2].bar([0,1,2],vals,color=['#087f8c','#c76450','#333333'],width=.62)
axs[2].axhline(0,color='#777777',lw=.8)
axs[2].set_xticks([0,1,2],['Capture\nchannels','Replaced\nchannels','Net'])
axs[2].set(title='C. Reversible synthetic counterexample',ylabel='Contribution to current change (s⁻¹)',ylim=(-4.6,4.6))
axs[2].text(0,3.45,'+3.239712914',ha='center',fontsize=8)
axs[2].text(1,-3.75,'−3.239712897',ha='center',fontsize=8)
axs[2].annotate('Net: 1.76 × 10⁻⁸ s⁻¹',(2,0),xytext=(1.2,1.7),arrowprops={'arrowstyle':'->','color':'#444444'},fontsize=8)
axs[2].text(.02,.025,'Constructed 72-state model;\nnot fitted to the measured catalyst.',transform=axs[2].transAxes,fontsize=8,color='#555555')
fig.suptitle('Energy transferred, reaction accelerated, and extra product are different quantities',fontsize=14)
fig.savefig(HERE/'full_cycle_evidence.png',dpi=180)
print(str(HERE/'full_cycle_evidence.png'))
