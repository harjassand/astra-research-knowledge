"""Plot exact analytic recovery bounds; this is not a large-register simulation."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

dest=Path(__file__).resolve().parent.parent/'output'/'pdf'
dest.mkdir(parents=True,exist_ok=True)
theta=.1
loss=np.geomspace(1e-8,.1,600)
b=np.sin(theta)**4
g=1-np.cos(theta)**4
a=(1-loss)*b/((1-loss)*b+loss*g)
lower=.75*(1-np.sqrt(a))
upper=.75*(1-a)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(7.3,3.8),layout='constrained')
ax.fill_between(loss,lower,upper,color='#dbe6f2',label='Interval containing the optimal error')
ax.plot(loss,upper,color='#163a63',lw=2,label='Achieved by the reverse Petz decoder')
ax.plot(loss,lower,color='#2a8c7d',lw=2,label='Lower bound for every decoder')
ax.axhline(.01,color='#a45529',ls='--',lw=1,label='Target error 0.01')
ax.set(xscale='log',yscale='log',xlabel='Independent lost-carrier probability',ylabel='Half-diamond error',ylim=(1e-6,1),xlim=(1e-8,.1))
ax.grid(which='major',alpha=.15)
ax.legend(loc='lower right',fontsize=8,frameon=False)
fig.savefig(dest/'loss_bounds.pdf')
fig.savefig(dest/'loss_bounds.png',dpi=190)
