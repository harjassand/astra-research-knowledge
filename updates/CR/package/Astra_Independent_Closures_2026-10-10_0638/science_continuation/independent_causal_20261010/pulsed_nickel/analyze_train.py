import numpy as np,json
from pathlib import Path
from scipy.optimize import minimize_scalar
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).parent;a=np.load(p/'trace_sheet2.npy')
x=np.arange(.2,4.81,.2)
def kernel(t,d=.2):
 t=np.atleast_1d(t);n=np.arange(10000);q=t[:,None]+n*(5+d)
 return np.sum(1/np.sqrt(q)-1/np.sqrt(q+d),axis=1)
def norm(k):return (k-k[-1])/(k[0]-k[-1])
k=norm(kernel(x));results=[];fig,axs=plt.subplots(1,3,figsize=(13,4))
for r in range(3):
 t,i=a[:,2*r:2*r+2].T;sel=(t>=1800)&(t<3600)&np.isfinite(i);t=t[sel];i=i[sel];phase=np.mod(t,5.2);phase[np.isclose(phase,5.2,atol=.0002)]=0
 y=np.array([np.median(i[np.abs(phase-z)<.001]) for z in x]);yn=norm(y)
 fun=lambda tau:np.mean((yn[1:-1]-norm(np.exp(-x/tau))[1:-1])**2)
 f=minimize_scalar(fun,bounds=(.03,10),method='bounded')
 current_phase_range=float(np.nanmax(y)-np.nanmin(y));noise=float(np.nanmedian([np.std(i[np.abs(phase-z)<.001]) for z in x]));
 out={'replicate':r+1,'n_samples':len(i),'phase_range_A':current_phase_range,'within_phase_sd_A':noise,'diffusive_NRMSE':float(np.sqrt(np.mean((yn[1:-1]-k[1:-1])**2))),'exponential_NRMSE':float(np.sqrt(f.fun)),'tau_s':float(f.x),'fraction_positive_current':float(np.mean(i>0)),'x_s':x.tolist(),'median_current_A':y.tolist(),'normalized_profile':yn.tolist()};results.append(out)
 axs[r].plot(x,yn,'o',label='data');axs[r].plot(x,k,label='diffusion');axs[r].plot(x,norm(np.exp(-x/f.x)),label='exponential');axs[r].set_title(f'Run {r+1}, tau={f.x:.3f}');axs[r].legend();axs[r].set_ylim(-.2,1.2)
print(json.dumps([{k:v for k,v in o.items() if k not in ['x_s','median_current_A','normalized_profile']} for o in results],indent=2))
(p/'train_results.json').write_text(json.dumps(results,indent=2));fig.tight_layout();fig.savefig(p/'train_profiles.png')
