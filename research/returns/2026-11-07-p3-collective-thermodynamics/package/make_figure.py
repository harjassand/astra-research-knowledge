"""Scientific illustration; the JSON interval certificates govern the claims."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,
                     'axes.spines.right':False,'figure.dpi':160,'savefig.dpi':200})
fig,ax=plt.subplots(1,2,figsize=(11.2,4.4),gridspec_kw={'width_ratios':[1.15,1]})
x=np.linspace(0,1,1000); Gamma=32/27
gap=-(1-x*x)**2-Gamma*x+Gamma
ax[0].plot(x,gap,color='#245b87',lw=2.2)
ax[0].scatter([1/3,1],[0,0],color='#ae542a',s=45,zorder=5)
ax[0].axhline(0,color='#8a9299',lw=.7)
ax[0].annotate('Two ordered phases\n'+r'$z=\pm2\sqrt{2}/3$',(1/3,0),xytext=(.06,.075),
               arrowprops={'arrowstyle':'-','color':'#ae542a'},color='#703719')
ax[0].annotate('Transverse phase\n$z=0$',(1,0),xytext=(.68,.075),
               arrowprops={'arrowstyle':'-','color':'#ae542a'},color='#703719')
ax[0].set(xlabel='Transverse magnetization $x$',ylabel='Energy above the common minimum',
          title='Noncommuting quartic model at coexistence',xlim=(-.015,1.02),ylim=(-.008,.20))
ax[0].text(.02,.95,r'$P=-z^4-\frac{32}{27}x$,  $T=0$',transform=ax[0].transAxes,va='top')
d=json.loads((ROOT/'SCHUR_DIAGNOSTIC.json').read_text())['finite_size_rows']
ns=np.array([r['N'] for r in d]); xpos=np.arange(len(ns)); width=.34
ax[1].bar(xpos-width/2,[float(4**int(n)) for n in ns],width,label='Dense full matrix',color='#89949d')
ax[1].bar(xpos+width/2,[r['stored_matrix_entries'] for r in d],width,label='All spin-sector blocks',color='#245b87')
ax[1].set_yscale('log'); ax[1].set_xticks(xpos,[str(n) for n in ns])
ax[1].set(xlabel='Number of spins $N$',ylabel='Stored complex matrix entries',
          title='Representation cost with every sector retained')
ax[1].legend(frameon=False,loc='upper left'); ax[1].set_ylim(1,1e43)
ax[1].text(.04,.56,'64 spins: 33 blocks\nLargest block: 65 × 65\n47,905 stored entries',
           transform=ax[1].transAxes,ha='left',va='top',color='#245b87',
           bbox={'facecolor':'white','edgecolor':'none','alpha':.9,'pad':5})
fig.suptitle('Collective thermodynamics: coexistence retained, Hilbert enumeration removed',
             fontsize=13,fontweight='bold',y=1.01)
fig.text(.01,-.015,'Left: analytic audit, independent of the numerical optimizer.  Right: representation counts, not laboratory acquisition costs.',
         fontsize=9,color='#4e5961')
fig.tight_layout(); fig.savefig(ROOT/'RESULTS.png',bbox_inches='tight')
