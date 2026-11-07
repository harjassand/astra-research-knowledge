"""Real-data response/sensitivity audit; no astrophysical discovery claim.
Reproduce: .venv/bin/python analyze_network.py
The measured data are GWOSC-calibrated strain, not independent strain truth.
Noise PSDs use 12 s post-event data, insufficient for calibrated tail claims.
"""
from pathlib import Path
import hashlib,json,time,platform
import numpy as np
import scipy
from scipy import signal,ndimage
import h5py,lal
P=Path(__file__).resolve().parent
t0=time.perf_counter(); fs=4096; gps=1187008882.43
ra=np.deg2rad(197.450374);dec=np.deg2rad(-23.381495)
order=['H1','L1','V1','G1'];dets={d.frDetector.prefix:d for d in lal.CachedDetectors}
gmst=lal.GreenwichMeanSiderealTime(lal.LIGOTimeGPS(gps))
F6=np.array([lal.ComputeDetAMResponseExtraModes(dets[k].response,ra,dec,0.,gmst) for k in order])
# LAL ordering: plus,cross,breathing,longitudinal,vector_x,vector_y.
# Drop longitudinal: exactly opposite breathing in long-wavelength, trace-free response.
F=F6[:,[0,1,2,4,5]]
delays=np.array([lal.TimeDelayFromEarthCenter(dets[k].location,ra,dec,lal.LIGOTimeGPS(gps)) for k in order])
x=[];quality={}
for k in order:
 with h5py.File(P/'data'/f'{k}_GW170817_32s.hdf5') as f:
  x.append(f['strain/Strain'][:]);quality[k]={n:np.unique(f[n][:],return_counts=True) for n in ['quality/simple/DQmask','quality/injections/Injmask']}
x=np.asarray(x); relative_event=gps-1187008867
# Noise-only prospective diagnostic: same fixed post-event interval for every detector.
freq,psd=signal.welch(x[:,18*fs:30*fs],fs=fs,nperseg=fs,noverlap=fs//2,average='median',axis=1)
# Keep resolved spectral lines in PSD; smoothing them away invalidates residual-energy normalization.
np.savez(P/'data/network_psd_and_response_v2.npz',freq=freq,psd=psd,response=F,delays=delays)

def null_basis(a):
 u,s,vh=np.linalg.svd(a,full_matrices=True); r=np.linalg.matrix_rank(a)
 return u[:,r:],s

def info(freq_index,indices):
 scale=1e-22 # keep numerical units near one
 w=scale/np.sqrt(psd[indices,freq_index]);a=F[indices,:2]*w[:,None];b=F[indices,2]*w
 n,s=null_basis(a); val=np.linalg.norm(n.T@b)**2
 return dict(scalar_profile_information=val,scalar_strain_asd=np.inf if val==0 else scale/np.sqrt(val),tensor_singular_values=s.tolist(),null_b_response=(n.T@b).tolist())

def rank_countermodel(indices):
 a=F[indices,:2];b=F[indices,2:];n,_=null_basis(a);proj=n.T@b
 u,s,vh=np.linalg.svd(proj,full_matrices=True);r=np.linalg.matrix_rank(proj);v=vh[r]
 ht=-np.linalg.lstsq(a,b@v,rcond=None)[0]
 residual=a@ht+b@v
 return dict(detectors=[order[i] for i in indices],matrix_rank=int(np.linalg.matrix_rank(F[indices])),tensor_rank=int(np.linalg.matrix_rank(a)),extra_response_rank_after_tensor=int(r),extra_nullity=int(3-r),extra_mode_unit_vector=v.tolist(),tensor_compensation=ht.tolist(),network_residual=residual.tolist(),residual_norm=float(np.linalg.norm(residual)),extra_norm=float(np.linalg.norm(v)),claim='Any multiple of this mixed extra-mode waveform plus tensor compensation leaves the network signal unchanged under the stated response model.')
rows=[]
for f in [50,100,200,500,1000,1250,1500]:
 j=int(np.argmin(abs(freq-f)));a=info(j,[0,1,2]);b=info(j,[0,1,2,3]);rows.append(dict(frequency_hz=float(freq[j]),asd={k:float(np.sqrt(psd[i,j])) for i,k in enumerate(order)},HLV=a,HLVG=b,scalar_information_gain_HLVG_over_HLV=b['scalar_profile_information']/a['scalar_profile_information'],G1_calibration_documented_for_this_band=f>=1000))
# Windowed exact-frequency projectors; diagnostic only, not discovery p-values.
def residual_features(start,duration=1.):
 n=int(duration*fs); seg=x[:,int(start*fs):int(start*fs)+n]
 win=signal.windows.hann(n,sym=False); fft=np.fft.rfft((seg-seg.mean(axis=1,keepdims=True))*win,axis=1)
 f=np.fft.rfftfreq(n,1/fs); S=np.array([np.interp(f,freq,p) for p in psd]);
 z=fft*np.sqrt(2/(fs*np.sum(win**2)))/np.sqrt(S)
 # d_i(t)=s(t-delay_i), so undo exp(-2pi if delay_i).
 z*=np.exp(2j*np.pi*f[None,:]*delays[:,None])
 ans={}
 for name,ind in [('HLV',[0,1,2]),('HLVG',[0,1,2,3])]:
  vals=[]
  for j in range(1,len(f)):
   w=1e-22/np.sqrt(S[ind,j]);a=F[ind,:2]*w[:,None];null,_=null_basis(a)
   vals.append(float(np.linalg.norm(null.T@z[ind,j])**2/null.shape[1]))
  vals=np.asarray(vals)
  ans[name]={f'{lo}-{hi}':float(np.mean(vals[(f[1:]>=lo)&(f[1:]<=hi)])) for lo,hi in [(50,500),(1000,1500)]}
 return ans
features={str(s):residual_features(s) for s in [1,3,5,7,9,11,13,14,15,17,19,21,23,25,27,29]}
report=dict(status='SCOPED_DIAGNOSTIC_NOT_DISCOVERY',gps=gps,sky_deg=[float(np.rad2deg(ra)),float(np.rad2deg(dec))],source='DES optical counterpart sky; LAL detector response; actual four GWOSC calibrated strain streams',detector_order=order,modes=['plus','cross','breathing','vector_x','vector_y'],response=F.tolist(),longitudinal_plus_breathing_max_abs=float(np.max(abs(F6[:,2]+F6[:,3]))),delays_s=delays.tolist(),countermodels=[rank_countermodel([0,1,2]),rank_countermodel([0,1,2,3])],sensitivity=rows,window_start_s=features,quality={k:{n:{'values':v[0].tolist(),'counts':v[1].tolist()} for n,v in q.items()} for k,q in quality.items()},limitations=['G1 calibration/status documented only for 1-4 kHz; its low-frequency gain is hypothetical and is not acquired scientific capability.','G1 was not in science mode; its DQmask is 127 despite documentation restricting its valid science use.','L1 raw GWTC-1 stream has a known glitch around 14.389 s; raw mean null energy is not evidence for new polarization.','32 s clips omit most of the BNS inspiral; event JSON offers clips although legacy event-page text says 32 s files were not originally distributed.','The 12 s estimated PSD and correlated Hann bins do not establish Gaussian stationary noise or valid extreme-tail probabilities.','Calibration envelopes are median and 1-sigma summaries, not hard simultaneous bounds.','Long-wavelength response used at 1-1.9 kHz is an approximation; finite-arm transfer response must be included before high-precision inference.','Scalar information gain assumes vector modes are excluded. Arbitrary mixed-mode power remains unbounded in both networks.'],runtime_s=time.perf_counter()-t0,versions={'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'h5py':h5py.__version__,'lal':lal.__version__})
(P/'NETWORK_AUDIT_v2.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:report[k] for k in ['countermodels','sensitivity','window_start_s','runtime_s']},indent=2))
