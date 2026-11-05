#!/usr/bin/env python3
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parents[1]
out=root/'figures';out.mkdir(exist_ok=True)
f=json.loads((root/'results/growing_family.json').read_text())
n=np.array([x['N'] for x in f]);lo=np.array([x['log10_certified_value_lower'] for x in f]);hi=np.array([x['log10_certified_value_upper'] for x in f]);v=np.array([x['log10_optimal_work'] for x in f])
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(1,2,figsize=(10.7,4.2),gridspec_kw={'width_ratios':[1.3,1]},layout='constrained')
ax[0].fill_between(n,lo,hi,color='#8fb7dc',alpha=.55,label='Value range from acquired probability intervals')
ax[0].plot(n,v,color='#173f5f',marker='o',label='Exact value of the synthetic source')
ax[0].set(xlabel='Failure depth N',ylabel='log10(expected useful output)',title='Same certified controller at every depth')
ax[0].legend(loc='upper left',fontsize=8,frameon=False)
ax[1].semilogy(n,10**(hi-lo),color='#b84a31',marker='o')
ax[1].set(xlabel='Failure depth N',ylabel='Upper / lower value allowed by the data',title='The absolute forecast remains unresolved')
ax[1].grid(axis='y',alpha=.2)
fig.suptitle('Optimal decisions can stay fixed while value uncertainty grows',fontsize=14,fontweight='bold')
fig.savefig(out/'policy_vs_value.pdf');fig.savefig(out/'policy_vs_value.png',dpi=180)
print(out/'policy_vs_value.png')
