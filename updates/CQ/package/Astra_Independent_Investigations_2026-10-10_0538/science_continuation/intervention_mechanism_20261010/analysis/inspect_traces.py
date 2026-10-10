import pathlib,sys,json
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'python_packages'))
import numpy as np,pandas as pd,matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
for file in ['data/03_Under pulse-wise external torque/01_Assisting_direction/traces_4000Hz/201222_019.txt','data/01_Without external torque/traces_4000Hz/210128_015.txt']:
 x=np.loadtxt(ROOT/'raw/extracted'/file,usecols=(0,3,4)); t=x[:,0]/4000
 fig,axs=plt.subplots(3,1,figsize=(14,9))
 for j in [1,2]:
  v=savgol_filter(x[:,j],401,1,deriv=1,delta=1/4000)
  for ax,rng in zip(axs,[(0,80),(19,30),(20,24)]):
   mask=(t>rng[0])&(t<rng[1]);ax.plot(t[mask][::20],v[mask][::20],label=['','centroid','longaxis'][j]);ax.set_xlim(rng)
   if rng[0]>0: ax.set_ylim(-4,15)
 axs[0].legend();fig.suptitle(file);fig.tight_layout();fig.savefig(ROOT/'results'/('inspect_'+pathlib.Path(file).stem+'.png'));plt.close(fig)
 print(file,'baseline',np.diff(x[(t>=1)&(t<9),1:],axis=0).mean(axis=0)*4000)
