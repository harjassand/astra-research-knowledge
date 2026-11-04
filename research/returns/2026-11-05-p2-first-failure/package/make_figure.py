import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

root=Path(__file__).resolve().parent
data=json.loads((root/'results.json').read_text())
exp=json.loads((root/'parallel_experiment.json').read_text())
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,
                     'axes.spines.right':False,'axes.labelcolor':'#263445',
                     'text.color':'#263445','axes.titleweight':'bold'})
fig,ax=plt.subplots(1,2,figsize=(11,4.2),layout='constrained')
x=np.array([v['slow_edges'] for v in data['chattering_parallel']])
y=np.array([v['frequency_undercount_factor'] for v in data['chattering_parallel']])
ax[0].plot(x,y,'o-',color='#147d92',lw=2)
ax[0].axhline(1,color='#a2aab4',ls='--',lw=1)
ax[0].set(xlabel='Ordinary parallel edges (plus one faster edge)',
          ylabel='First-failure mean / reciprocal failure frequency',
          title='Repeated failures can form clusters')
ax[0].grid(axis='y',alpha=.15)
mean=exp['point_estimate']/1e9
lo,hi=np.array(exp['mean_interval'])/1e9
ax[1].errorbar([mean],[1],xerr=[[mean-lo],[hi-mean]],fmt='o',capsize=6,
               color='#147d92',lw=2,label='Conditioned short-path estimate; 99% interval')
ax[1].plot([exp['exact_birth_death_mean']/1e9],[.5],'D',color='#263445',
           label='Exact birth-death mean')
ax[1].plot([exp['inverse_stationary_frequency']/1e9],[0],'x',ms=9,mew=2,
           color='#cc7b31',label='Reciprocal stationary failure frequency')
ax[1].set_yticks([0,.5,1],['Frequency inverse','Exact mean','Short-path estimate'])
ax[1].set(xlabel='Mean first-failure time (billions of model units)',
          title='40 ordinary repairable parallel edges',ylim=(-.35,1.35))
ax[1].grid(axis='x',alpha=.15)
fig.savefig(root/'figures/reliability_results.pdf',bbox_inches='tight')
fig.savefig(root/'figures/reliability_results.png',dpi=170,bbox_inches='tight')
