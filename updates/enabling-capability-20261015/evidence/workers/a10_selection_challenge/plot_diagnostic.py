from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent
D=np.load(P/'data/network_psd_and_response_v2.npz');F=D['response'];S=D['psd'];freq=D['freq'];sel=np.flatnonzero((freq>=1000)&(freq<=1500))
rat=[]
for j in sel:
 vals=[]
 for ind in [[0,1,2],[0,1,2,3]]:
  Z=F[ind]*(1e-22/np.sqrt(S[ind,j]))[:,None];u,s,vh=np.linalg.svd(Z[:,:2],full_matrices=True);vals.append(np.linalg.norm(u[:,2:].T@Z[:,2])**2)
 rat.append(vals[1]/vals[0])
r=json.loads((P/'REAL_DISK_DIAGNOSTIC.json').read_text());t=[x['start_s']-15.43+.5 for x in r['rows']]
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(1,2,figsize=(11,4.2),layout='constrained')
ax[0].semilogy(freq[sel],rat,color='#3267a8',alpha=.55,lw=.8)
ax[0].axhline(1,color='gray',lw=1);ax[0].axhline(np.median(rat),color='#d88020',lw=1.5,label=f'Median {np.median(rat):.1f}×')
ax[0].set(xlabel='Frequency (Hz)',ylabel='Scalar information: HLVG / HLV',title='Fourth detector adds conditional information')
ax[0].legend(frameon=False,loc='upper right');ax[0].text(.03,.03,'Tensor + breathing model; no vector modes\nSame gain from ordinary weighted least squares',transform=ax[0].transAxes,va='bottom',fontsize=9,bbox=dict(facecolor='white',alpha=.9,edgecolor='none'))
for k,label,col in [('0','Nominal calibration','#3267a8'),('3','Expanded calibration scenario','#b4514e')]:
 vals=[x['statistics']['50-500'][k] for x in r['rows']];ax[1].semilogy(t,vals,'o-',label=label,color=col,lw=1,ms=4)
ax[1].axvspan(-1.65,-.45,color='#dddddd',alpha=.5)
ax[1].set(xlabel='Time relative to merger (s)',ylabel='Mean null statistic, 50–500 Hz',title='Known instrumental glitch survives gain robustness')
ax[1].legend(frameon=False,loc='upper right',fontsize=9)
ax[1].text(-1.25,19,'Known L1 glitch',ha='right',fontsize=9)
fig.suptitle('GW170817 open-data selection challenge: information gain is not a new scientific operation',fontsize=12)
fig.supxlabel('Diagnostic only: 32 s clips, 12 s estimated noise PSD, long-wavelength response. No astrophysical p-value or discovery claim.',fontsize=9)
fig.savefig(P/'NETWORK_DIAGNOSTIC.png',dpi=180)
fig.savefig(P/'NETWORK_DIAGNOSTIC.pdf')
