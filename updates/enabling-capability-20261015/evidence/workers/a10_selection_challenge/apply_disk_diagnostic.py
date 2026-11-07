"""Apply conditional disk certificate to real HLV observations.
The 1/3-sigma envelope multipliers are sensitivity scenarios, NOT hard bounds.
Known L1 glitch is the adversarial negative control: no claim of new gravity.
"""
from pathlib import Path
import json,time
import numpy as np
import h5py
from scipy import signal
from calibration_disk import disk_certificate
P=Path(__file__).resolve().parent;t0=time.perf_counter();fs=4096
D=np.load(P/'data/network_psd_and_response_v2.npz');F=D['response'][:3];delays=D['delays'][:3];freq=D['freq'];PSD=D['psd'][:3]
x=[]
for k in ['H1','L1','V1']:
 with h5py.File(P/'data'/f'{k}_GW170817_32s.hdf5') as f:x.append(f['strain/Strain'][:])
x=np.array(x)
C=[np.loadtxt(P/'data/calibration/GWTC1_GW170817_CalEnv'/f'GWTC1_GW170817_{k}_CalEnv.txt') for k in ['H','L','V']]

def eps_at(f,k):
 out=[]
 for c in C:
  vals=np.array([np.interp(f,c[:,0],c[:,j]) for j in range(1,7)])
  mag=[vals[0]+k*(vals[2]-vals[0]),vals[0]+k*(vals[4]-vals[0])]
  ph=[vals[1]+k*(vals[3]-vals[1]),vals[1]+k*(vals[5]-vals[1])]
  out.append(max(abs(a*np.exp(1j*p)-1) for a in mag for p in ph))
 return np.array(out)
rows=[]
for start in [1,3,5,7,9,11,13,14,15,17,19,21,23,25,27,29]:
 n=fs;seg=x[:,start*fs:(start+1)*fs];win=signal.windows.hann(n,sym=False)
 ff=np.fft.rfft((seg-seg.mean(axis=1,keepdims=True))*win,axis=1);f=np.fft.rfftfreq(n,1/fs)
 S=np.array([np.interp(f,freq,p) for p in PSD]);z=ff*np.sqrt(2/(fs*np.sum(win**2)))/np.sqrt(S)
 z*=np.exp(2j*np.pi*f[None,:]*delays[:,None]);out={}
 for lo,hi in [(50,500),(1000,1500)]:
  vals={k:[] for k in [0,1,3]}
  for j in np.flatnonzero((f>=lo)&(f<=hi)):
   A=F[:,:2]*(1e-22/np.sqrt(S[:,j]))[:,None];u,s,vh=np.linalg.svd(A,full_matrices=True);w=u[:,-1]
   for k in vals:
    eps=eps_at(f[j],k) if k>0 else np.zeros(3)
    vals[k].append(disk_certificate(z[:,j],w,eps)['noise_normalized_lower'])
  out[f'{lo}-{hi}']={str(k):float(np.mean(v)) for k,v in vals.items()}
 rows.append({'start_s':start,'statistics':out})
r={'status':'CONDITIONAL_SENSITIVITY_DIAGNOSTIC','rows':rows,'calibration_complex_disk_radii':{str(f):{str(k):eps_at(f,k).tolist() for k in [1,3]} for f in [50,100,500,1000,1250,1500]},'units':'Mean per-frequency normalized lower statistic; one-sided real-spectrum coefficients; no calibrated p-value.', 'central_result':'Known L1 instrumental glitch is a real counterexample to interpreting a residual beyond calibration tolerance as extra GW polarization. Noise/glitch identification is a distinct acquired premise.','limitations':['Source calibration values are marginal median/1-sigma summaries; treating k-sigma boxes as deterministic simultaneous bounds is NOT justified.','Spectral PSD estimated on 12 post-event seconds; Hann windows correlate adjacent frequencies; no null distribution is claimed.','Frequency-wise complex disks relax actual calibration frequency correlations, so bound is conservative for contained calibrations.','Known instrumental glitch lies in start_s=14 window; response alternatives cannot turn it into scientific evidence.'],'runtime_s':time.perf_counter()-t0}
(P/'REAL_DISK_DIAGNOSTIC.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
