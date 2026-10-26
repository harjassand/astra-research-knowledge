from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from switch_stress import frontier

p=Path(__file__).resolve().parent
d=json.loads((p/'switch_stress_results.json').read_text())
fig,ax=plt.subplots(1,2,figsize=(10.8,4.1),layout='constrained')
kk=np.geomspace(1.05,1e5,250)
cc=np.array([np.sqrt(frontier(k)[0]) for k in kk])
ax[0].loglog(kk,cc,label='Global ideal bound over all bounded curves',lw=2)
ax[0].loglog(kk[kk>=10],(3/4)**(1/6)*kk[kk>=10]**(-1/3),':',label='Large-contrast asymptote')
rows=d['threshold_frontier']
ax[0].scatter([r['k'] for r in rows],[np.sqrt(r['ordinary_best_cv2']) for r in rows],
              s=30,facecolors='none',edgecolors='black',label='Ordinary scalar optimization',zorder=3)
ax[0].set(xlabel='Conductance contrast K',ylabel='Minimum full-waveform CV',
          title='Self-cooling source: exact ideal frontier')
ax[0].legend(fontsize=8)
for k in [100.,1000.]:
    rr=[r for r in d['smooth_retuned_comparators'] if r['k']==k]
    line,=ax[1].semilogx([r['width_fraction'] for r in rr],[r['cv'] for r in rr],
                         'o-',label=f'Retuned smooth curve, K={k:g}')
    ax[1].axhline(np.sqrt(frontier(k)[0]),color=line.get_color(),ls=':',lw=1)
ax[1].set(xlabel='Transition width / initial temperature rise',ylabel='Full-waveform CV',
          title='Illustrative smooth models; no device data')
ax[1].legend(fontsize=8)
for a in ax:
    a.spines[['top','right']].set_visible(False)
    a.grid(alpha=.18)
fig.savefig(p/'stage2_contrast_frontier.png',dpi=180)
print(p/'stage2_contrast_frontier.png')
