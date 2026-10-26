"""Plot exact model formulas; not measured or simulated trajectory data."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

out=Path(__file__).resolve().parent
e=np.geomspace(1e-4,.5,600)
rate=e*np.log((2+e/3)/(1+e/3))
fig,axs=plt.subplots(1,2,figsize=(10,4.4),layout='constrained')
axs[0].loglog(e,rate,color='#147d75',lw=2.5,label='Actual four-state path KL rate')
axs[0].axhline(3/11,color='#b24447',lw=2,ls='--',label='Matched Gaussian rate = 3/11')
axs[0].set(xlabel='Active stationary probability, ε',ylabel='Irreversibility per time unit',title='Same whitened covariance at every lag')
axs[0].legend(fontsize=9,loc='lower right',frameon=False)
axs[1].loglog(e,9/e-6+e/(1-e),color='#735796',lw=2.5,label='Fourth moment of whitened signal')
axs[1].loglog(e,1/e,color='#bf8135',lw=2,ls=':',label='Mean inactive waiting time')
axs[1].set(xlabel='Active stationary probability, ε',ylabel='Exact model quantity',title='The missing activity / amplitude information')
axs[1].legend(fontsize=9,loc='upper right',frameon=False)
for ax in axs:
    ax.grid(which='major',alpha=.18)
    ax.spines[['top','right']].set_visible(False)
fig.suptitle('Covariance alone does not give a universal non-Gaussian rate floor',fontsize=13)
fig.supxlabel('Exact CTMC construction; no measured data. Whitening depends on ε. Quantities use declared model units.',fontsize=9)
fig.savefig(out/'COVARIANCE_BOUNDARY.png',dpi=180)
fig.savefig(out/'COVARIANCE_BOUNDARY.pdf')
