from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from audit_data import load,pulse_info
BASE=Path(__file__).resolve().parents[1]
_,p,_=load(); pi=pulse_info(p,'pos'); ni=pulse_info(p,'neg')
g=json.loads((BASE/'results/paired_gate.json').read_text())
fig,axs=plt.subplots(1,3,figsize=(14.5,4.2),layout='constrained')
for sign,info,label in [('pos',pi,'Charge rise'),('neg',ni,'Discharge fall')]:
    age=info['t']-info['assumed_on_s']; mask=(age>0)&(age<10)
    axs[0].plot(age[mask],info['direction']*(info['v'][mask]-info['baseline_V'])*1000,label=label,lw=2)
axs[0].set(xlabel='Age after assumed current switch (s)',ylabel='Measured voltage increment (mV)',title='Cell 001: paired raw increments')
axs[0].legend(frameon=False); axs[0].grid(alpha=.2)
floors=[r['minimum_per_endpoint_uniform_error_mV'] for r in g['rows']]
axs[1].hist(floors,bins=16,color='#3f6b9e',edgecolor='white')
axs[1].axvline(np.median(floors),color='#c64e35',ls='--',label=f'Median {np.median(floors):.3f} mV')
axs[1].set(xlabel='Minimum increment discrepancy per endpoint (mV)',ylabel='Cells',title='Conditional gate fails for 92/92 cells')
axs[1].legend(frameon=False)
age=ni['t']-ni['assumed_on_s']; mask=(age>0)&(age<10)
axs[2].plot(age[mask],-(ni['v'][mask]-ni['baseline_V'])*1000,color='black',lw=2,label='Held-out discharge')
for kind,label in [('hybrid_charge_strict','Original hybrid-drt: strict'),('hybrid_charge_flexible','Original hybrid-drt: flexible')]:
    w=np.load(BASE/f'results/hybrid_{kind}_predictions.npz')
    axs[2].plot(age[mask],-w['neg_predicted_V'][mask]*1000,lw=1.7,label=label)
axs[2].set(xlabel='Age after assumed current switch (s)',ylabel='Voltage drop (mV)',title='Charge + EIS train; discharge held out')
axs[2].legend(frameon=False,fontsize=8); axs[2].grid(alpha=.2)
fig.suptitle('Measured voltage evidence; missing measured current and initial-state calibration remain gates',fontsize=12)
fig.savefig(BASE/'results/paired_pulse_boundary.png',dpi=180)
