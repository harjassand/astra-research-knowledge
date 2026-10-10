import numpy as np,json
from pathlib import Path
from scipy.optimize import minimize_scalar
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).parent
x=np.arange(.2,4.81,.2)
def kernel(t,d):
 t=np.atleast_1d(t);n=np.arange(10000);q=t[:,None]+n*(5+d)
 return np.sum(1/np.sqrt(q)-1/np.sqrt(q+d),axis=1)
def norm(k):return (k-k[-1])/(k[0]-k[-1])
train=json.loads((p/'train_results.json').read_text());tau=np.mean([q['tau_s'] for q in train[:2]]);results=[];fig,axs=plt.subplots(2,3,figsize=(13,8))
for row,(sheet,duration) in enumerate([(7,.04),(6,1.)]):
 a=np.load(p/f'trace_sheet{sheet}.npy'); period=5+duration;k=norm(kernel(x,duration));e=norm(np.exp(-x/tau))
 for r in range(3):
  t,i=a[:,2*r:2*r+2].T;sel=(t>=1800)&(t<3600)&np.isfinite(i);t=t[sel];i=i[sel];phase=np.mod(t,period);phase[np.isclose(phase,period,atol=.002)]=0
  y=np.array([np.median(i[np.abs(phase-z)<.005]) if np.any(np.abs(phase-z)<.005) else np.nan for z in x]);yn=norm(y)
  rg=float(np.nanmax(y)-np.nanmin(y));noise=float(np.nanmedian([np.std(i[np.abs(phase-z)<.005]) for z in x])); anodic=(phase>=5-0.002)|(phase<=.002);apos=float(np.nanmedian(i[anodic])) if np.any(anodic) else np.nan
  ok=bool((apos>0)&(rg>noise)&np.all(np.isfinite(y)))
  o={'pulse_duration_s':duration,'sheet':sheet,'replicate':r+1,'n_samples':len(i),'phase_range_A':rg,'within_phase_sd_A':noise,'anodic_median_A':apos,'acquisition_pass':ok,'diffusive_NRMSE':float(np.sqrt(np.nanmean((yn[1:-1]-k[1:-1])**2))),'exponential_NRMSE':float(np.sqrt(np.nanmean((yn[1:-1]-e[1:-1])**2))),'fixed_tau_s':float(tau),'fraction_positive_current':float(np.mean(i>0)),'x_s':x.tolist(),'median_current_A':y.tolist(),'normalized_profile':yn.tolist()};results.append(o)
  ax=axs[row,r];ax.plot(x,yn,'o',label='observed');ax.plot(x,k,label='diffusive prediction');ax.plot(x,e,label='fixed exponential');ax.set_title(f'a={duration}s, Run {r+1}, usable={ok}');ax.set_ylim(-.2,1.2);ax.legend(fontsize=8)
print(json.dumps([{k:v for k,v in o.items() if k not in ['x_s','median_current_A','normalized_profile']} for o in results],indent=2))
(p/'validation_results.json').write_text(json.dumps(results,indent=2));fig.tight_layout();fig.savefig(p/'validation_profiles.png')
