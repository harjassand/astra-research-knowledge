import pathlib,sys,json,os
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'python_packages'));os.environ['MPLCONFIGDIR']=str(ROOT/'analysis/mplcache')
import numpy as np,pandas as pd,matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
s=pd.read_csv(ROOT/'raw/selected_manifest.csv');s=s[s.split=='discovery'];out=[]
fig,axs=plt.subplots(len(s),1,figsize=(15,2.1*len(s)),squeeze=False)
for ax,(_,r) in zip(axs[:,0],s.iterrows()):
 f=ROOT/'raw/extracted'/r.path
 if not f.exists():print('MISSING',f);continue
 x=np.loadtxt(f,usecols=(0,4));t=x[:,0]/4000;ang=x[:,1];v=savgol_filter(ang,401,1,deriv=1,delta=1/4000);base=np.median(v[(t>1)&(t<9)]);vn=v/base
 if base<0:vn=-vn
 mask=(t>=19.8)&(t<51);ax.plot(t[mask][::20],vn[mask][::20],lw=.6);ax.set_ylim(-.2,.65);ax.axhline(.05,c='r',ls=':');ax.set_title(f'{r.cell} {r.file}, baseline={base:.2f} Hz',fontsize=8)
 for edge in np.arange(21.5,50,1.5):
  if '03_' in r.group: ax.axvspan(edge-.5,edge,alpha=.15,color='gray')
 # Candidate persistent onset within each off window, first event only, using 150ms survival above threshold allowing 10% gaps.
 for frac in [.025,.05,.075,.1]:
  positive=(vn>frac).astype(float);persist=np.convolve(positive,np.ones(601)/601,mode='same')
  intervals=[(20, min(t[-1],80))] if '01_Without' in r.group else [(20,21)]+[(float(a),float(a+1)) for a in np.arange(21.5,50,1.5)]
  found=False
  for pulse,(start,end) in enumerate(intervals):
   valid=(t>start+.1)&(t<end-.1)&(persist>.90)&(vn>frac)
   idx=np.flatnonzero(valid)
   onset=t[idx[0]]-start if len(idx) else None
   out.append(dict(cell=r.cell,file=r.file,group=r.group,frac=frac,pulse=pulse,start=start,end=end,baseline=base,reset_velocity=np.mean(vn[(t>20.2)&(t<20.8)]),initial_off=np.mean(vn[(t>start+.1)&(t<start+.25)]),onset=onset))
   if onset is not None:
    if frac==.05:ax.axvline(start+onset,c='r')
    break
fig.tight_layout();fig.savefig(ROOT/'results/discovery_traces.png',dpi=120)
d=pd.DataFrame(out);d.to_csv(ROOT/'results/discovery_events.csv',index=False)
print(d[(d.frac==.05)&d.onset.notna()][['cell','group','pulse','onset','initial_off','reset_velocity']].to_string(index=False))
