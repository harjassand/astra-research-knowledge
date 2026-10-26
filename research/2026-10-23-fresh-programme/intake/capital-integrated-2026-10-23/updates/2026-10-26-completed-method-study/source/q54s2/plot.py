#!/usr/local/bin/python3
from pathlib import Path
import csv,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent
summary=json.loads((P/'summary.json').read_text())
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':180})
fig,axes=plt.subplots(1,3,figsize=(13.4,4),constrained_layout=True)
raw=np.load(P/'sprt_raw.npz')
counts=np.r_[raw['delta_0.025_H0_counts'],raw['delta_0.025_H1_counts']]
q=np.sort(counts)
axes[0].plot(q,np.arange(1,len(q)+1)/len(q),color='#275f8c',lw=2,label='Ordinary SPRT sample-count CDF')
axes[0].axvline(177,color='#ae513c',ls='--',label='Fixed-n 5% threshold: 177')
axes[0].axvline(counts.mean(),color='#5d8b5f',ls=':',label=f'SPRT mean: {counts.mean():.1f}')
axes[0].set(xlabel='Scalar readings (same endpoint/noise)',ylabel='Probability of having stopped',title='A. Sequential stopping improves constants',xlim=(0,counts.max()+10),ylim=(0,1.02))
axes[0].legend(fontsize=8,frameon=False,loc='lower right')
axes[0].grid(axis='y',alpha=.2)
with (P/'withheld_cases.csv').open() as f: rows=list(csv.DictReader(f))
order=np.argsort([float(r['true_target']) for r in rows])
lo=np.array([float(rows[i]['target_lower']) for i in order]);hi=np.array([float(rows[i]['target_upper']) for i in order]);truth=np.array([float(rows[i]['true_target']) for i in order])
x=np.arange(len(rows))
axes[1].vlines(x,lo,hi,color='#b9c6d1',lw=.8)
axes[1].plot(x,truth,color='#1c2833',lw=1.5,label='Withheld target truth')
axes[1].set(xlabel='200 cases, ordered by target truth',ylabel='Force at withheld displacement b=1',title='B. Sharp compatible-law target intervals',ylim=(.8,5.1))
axes[1].legend(frameon=False,fontsize=8)
axes[1].text(.03,.96,'Five analytic families; 17 safe readings each',transform=axes[1].transAxes,va='top',fontsize=8)
vals=[summary['certificates'][k] for k in ['safe','unsafe','unknown']]
axes[2].bar(['Below ceiling','Above ceiling','UNKNOWN'],vals,color=['#5d8b5f','#275f8c','#aeb5bc'])
for j,v in enumerate(vals):axes[2].text(j,v+6,str(v),ha='center')
axes[2].set(ylabel='Force-ceiling task decisions',title='C. Exact certificate = ordinary LP',ylim=(0,470))
axes[2].text(.5,.92,'800 tasks; zero observed incorrect certificates',transform=axes[2].transAxes,ha='center',fontsize=8)
axes[2].text(.5,.85,'402 unresolved tasks retained',transform=axes[2].transAxes,ha='center',fontsize=8)
fig.suptitle('Q54 stage 2: strongest ordinary methods retained; no new acquisition capability',fontsize=13)
fig.savefig(P/'stage2_stress.png');fig.savefig(P/'stage2_stress.pdf')
