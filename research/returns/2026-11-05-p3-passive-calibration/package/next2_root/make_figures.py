"""Plot already recorded synthetic results; performs no further sampling."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

here=Path(__file__).resolve().parent
out=here/'figures';out.mkdir(exist_ok=True)
strong=json.loads((here/'passive_photocount_results.json').read_text())
matched=json.loads((here/'matched_photocount_results.json').read_text())
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,
                     'savefig.dpi':180,'font.family':'DejaVu Sans'})
fig,ax=plt.subplots(2,1,figsize=(9,7),gridspec_kw={'height_ratios':[1.15,1]},constrained_layout=True)
x=np.arange(len(strong['rows']))
truth=[a['theta'] for a in strong['rows']]
ax[0].bar(x,truth,width=.68,color='#d8e3ec',label='True coefficient')
ax[0].plot(x-.12,[a['nonlinear_fit'] for a in strong['rows']],'o',ms=4.5,color='#116b87',label='Stronger LO: 2 million blocks')
ax[0].plot(x+.12,[a['nonlinear_fit'] for a in matched['rows']],'s',ms=4.5,color='#d47637',label='Matched LO: 2 million blocks')
ax[0].set_xticks(x,strong['labels']);ax[0].set_ylabel('Hamiltonian coefficient')
ax[0].axhline(0,color='#88939d',lw=.7);ax[0].legend(loc='upper right',fontsize=8)
ax[0].set_title('Classical photon records recover a small interacting Hamiltonian',loc='left',weight='bold')
steps=np.arange(1,9)
ax[1].semilogy(steps,strong['exact_mean_iteration_errors'],'o-',color='#475c4d',label='Exact response means')
ax[1].semilogy(steps,strong['sample_iteration_errors'],'o-',color='#116b87',label='Stronger LO, sampled')
ax[1].semilogy(steps,matched['sample_iteration_errors'],'s-',color='#d47637',label='Matched LO, sampled')
ax[1].set_xticks(steps);ax[1].set_xlabel('Nonlinear inverse iteration');ax[1].set_ylabel('Maximum coefficient error')
ax[1].grid(axis='y',alpha=.2);ax[1].legend(fontsize=8)
ax[1].set_title('The sampled inverse reaches its noise floor',loc='left',weight='bold')
fig.savefig(out/'photon_count_calibration.png');plt.close(fig)

z=json.loads((here.parent/'next2_reliability/results.json').read_text())
fig,ax=plt.subplots(1,2,figsize=(9,3.7),constrained_layout=True)
for j,row in enumerate(z['monte_carlo']):
    ref=float(row['reference_F_120d']);lo,hi=map(float,row['F_interval'])
    mid=(lo+hi)/2
    ax[0].errorbar(j,mid/ref,yerr=[[mid/ref-lo/ref],[hi/ref-mid/ref]],fmt='o',capsize=5,color='#116b87')
ax[0].axhline(1,color='#475c4d',ls='--',label='High-precision reference')
ax[0].set_xticks(range(3),['0.25','2','20']);ax[0].set_ylim(.90,1.07)
ax[0].set_xlabel('Uniformized deadline');ax[0].set_ylabel('Interval divided by reference CDF')
ax[0].set_title('Short paths estimate probabilities near $10^{-25}$',fontsize=10,loc='left')
row=z['tail_queries'][1];lo,hi=map(float,row['interval']);ref=float(row['reference_F_120d'])
ax[1].errorbar([0],[(lo+hi)/2],yerr=[[(hi-lo)/2],[(hi-lo)/2]],fmt='o',capsize=9,color='#d47637')
ax[1].axhline(ref,color='#475c4d',ls='--',label='Reference CDF')
ax[1].set_xticks([0],['$u=10^{24}$']);ax[1].set_xlim(-.7,.7);ax[1].set_ylim(.34,.42)
ax[1].set_ylabel('First-failure probability');ax[1].set_title('A short reverse window supports a long deadline',fontsize=10,loc='left')
ax[1].legend(fontsize=8)
fig.savefig(out/'reliability_diagnostic.png');plt.close(fig)
print('Created two figures from the saved evidence only.')
