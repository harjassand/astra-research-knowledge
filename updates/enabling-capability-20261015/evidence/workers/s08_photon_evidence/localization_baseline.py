"""Conditional spatial Poisson-ML baseline on real1500-photon blocks.
Uses source fiber geometry/dark rates and detector-efficiency vector. This is
not an independent count/separation ground-truth validation. Coordinates um.
"""
from pathlib import Path
import json,time,zipfile,sys
import numpy as np
from scipy.optimize import minimize
from numpy.polynomial.legendre import leggauss
import photon_baseline as p
H=Path(__file__).resolve().parent
EFF=np.array([.676,.665,.737,.705,.631,.829,.731,.733,1,.937,.741,.748,.705,.739,.744])
EFF_NEW=np.array([.7789,.6939,.8252,.7963,.7139,.8743,.8108,.7980,.9547,1,.8391,.8348,.7379,.7174,.8129])
XY=np.array([[309.1,209.3,318.8,219,112,233.6,129,408.9,457,505.7,301.6,398.9,425.4,262.6,337.9],
 [155.8,119.3,258.1,221.5,182.6,323.8,280,194.8,398.9,243.2,53.52,90.01,301.6,435.4,364.8]]).T/748
# Fixed polar disk quadrature for15 circular fiber cores radius50/748um.
nodes,weights=leggauss(10);rad=(nodes+1)*.5*50/748;rw=weights*.5*50/748*rad
ang=np.arange(48)*2*np.pi/48;w=(rw[:,None]*np.ones((1,48))*2*np.pi/48).ravel()
pts=(XY[:,None,:]+np.stack([rad[:,None]*np.cos(ang),rad[:,None]*np.sin(ang)],axis=-1).reshape(1,-1,2))
D=np.delete(p.DARK,13)
def integrals(v):
 x,y,sx,sy,theta=v
 q=pts-np.array([x,y]);c,s=np.cos(theta),np.sin(theta)
 a=c*q[:,:,0]+s*q[:,:,1];b=-s*q[:,:,0]+c*q[:,:,1]
 return (np.exp(-.5*((a/sx)**2+(b/sy)**2))@w)/(2*np.pi*sx*sy)
def fit(counts,dt,eff):
 # Total signal expressed as counts after collection; normalized shape,
 # directraw-count likelihood avoids subtracting noisy counts beforefit.
 def mu(v):
  g=integrals(v[1:6])*eff;g/=g.sum()
  return np.exp(v[0])*g+D*dt+np.exp(v[6])*eff/eff.sum()
 def obj(v):
  m=mu(v);return float(np.sum(m-counts*np.log(m)))
 mean=(np.maximum(counts-D*dt,0)/eff)@XY/(np.maximum(counts-D*dt,0)/eff).sum()
 initial=np.r_[np.log(max(counts.sum()-D.sum()*dt,10)),mean[0],mean[1],.13,.13,0,np.log(1.)]
 bounds=[(np.log(10),np.log(3000)),(.03,.8),(-.02,.7),(.08,.18),(.08,.18),(-np.pi/2,np.pi/2),(-8,np.log(300))]
 result=minimize(obj,initial,method='L-BFGS-B',bounds=bounds,options={'maxiter':250,'ftol':1e-10,'gtol':1e-5})
 v=result.x;m=mu(v)
 # Observed shape model uncertainty from Poisson Fisher information only.
 eps=1e-5;J=np.column_stack([(mu(v+np.eye(7)[j]*eps)-mu(v-np.eye(7)[j]*eps))/(2*eps) for j in range(7)])
 cov=np.linalg.pinv(J.T@(J/m[:,None]),rcond=1e-9)
 return dict(xy_um=v[1:3].tolist(),sigma_um=v[3:5].tolist(),theta=float(v[5]),
  signal_counts=float(np.exp(v[0])),extra_background_counts=float(np.exp(v[6])),
  poisson_only_xy_se_nm=(np.sqrt(np.maximum(np.diag(cov)[1:3],0))*1000).tolist(),
  poisson_deviance=float(2*np.sum(np.where(counts>0,counts*np.log(np.maximum(counts,1)/m),0)-counts+m)),
  converged=bool(result.success),nfev=int(result.nfev))
def two_tracks(data):
 if len(data)<4:return None
 xy=np.array([d['fit']['xy_um'] for d in data]);t=np.array([d['time_s'] for d in data]);t-=t.mean()
 center=xy.mean(axis=0);v=np.linalg.svd(xy-center,full_matrices=False)[2][0]
 labels=((xy-center)@v>0).astype(int);drift=np.zeros(2)
 for k in range(100):
  X=np.c_[np.ones(len(t)),labels,t]
  coef=np.linalg.lstsq(X,xy,rcond=None)[0]
  errs=np.array([np.sum((xy-(coef[0]+j*coef[1]+t[:,None]*coef[2]))**2,axis=1) for j in [0,1]]).T
  lab=errs.argmin(axis=1)
  if np.array_equal(lab,labels):break
  labels=lab
 return dict(conditional_two_track_separation_nm=float(np.linalg.norm(coef[1])*1000),
  drift_nm_per_s=(coef[2]*1000).tolist(),cluster_sizes=np.bincount(labels,minlength=2).tolist(),
  residual_2d_rms_nm=float(np.sqrt(np.mean(np.min(errs,axis=1)))*1000),
  warning='Two tracks are fitted by construction; this is not evidence for exactly2 emitters or a validated100nm resolution.')
def main():
 start=time.perf_counter();r=json.loads((H/'BASELINE_ALL.json').read_text());z=zipfile.ZipFile(r['archive']['path'])
 blocks=[]
 for c in r['results']:
  cycle=int(c['file'][-8:-4]);times,chs,_=p.decode(z.read(c['file']))
  lookup=np.full(32,-1,dtype=int);lookup[p.CHANNELS]=np.arange(16);ix=lookup[chs]
  dt=c['meta']['duration_seconds'];fr=np.ceil(times*p.TPB*4/dt).astype(int)-1
  for frame in c['frames']:
   if frame['saved_g2']==-99:continue
   k=frame['frame']-1;sel=(fr==k)&(ix!=13);ts=times[sel];channels=ix[sel];channels=np.where(channels>13,channels-1,channels)
   for b in range(len(channels)//1500):
    cut=slice(b*1500,(b+1)*1500);counts=np.bincount(channels[cut],minlength=15);d=(ts[cut][-1]-ts[cut][0])*p.TPB
    block=dict(file=c['file'],frame=k+1,block=b,counts=counts.tolist(),duration_s=float(d),
      source_g2_dominance_pass=frame['saved_pass'],time_s=float((p.saved_rows(cycle)[0]/4)*.2+ts[cut][0]*p.TPB),
      rate_hz=float(1500/d))
    blocks.append(block)
 selected=[b for b in blocks if b['source_g2_dominance_pass']]
 # Sameblock photon budget for intensityonly comparator: lowest10%rate among
 # sourcevalidblocks. This differs from the paper's complete-data comparator.
 low=sorted(blocks,key=lambda b:b['rate_hz'])[:max(1,round(len(blocks)*.1))]
 outputs=[]
 for label,samp in [('source_g2_dominance',selected),('intensity_lowest10percent_available',low)]:
  data=[]
  for b in samp:
   record=b.copy();record['fit']=fit(np.array(b['counts']),b['duration_s'],EFF);data.append(record)
  outputs.append(dict(method=label,blocks=len(data),conditional_two_track_fit=two_tracks(data),data=data))
 # Calibration sensitivity on identicalselectedblocks: alternatepublisheddate
 # and uncorrectedcalibration, not an empirical uncertaintyinterval.
 sens=[]
 for label,eff in [('later_dated_vector',EFF_NEW),('equal_efficiency_assumption',np.ones(15))]:
  data=[]
  for b in selected:
   record=b.copy();record['fit']=fit(np.array(b['counts']),b['duration_s'],eff);data.append(record)
  sens.append(dict(efficiency_scenario=label,conditional_two_track_fit=two_tracks(data),
   median_shift_from_source_vector_nm=float(np.median([np.linalg.norm(np.array(a['fit']['xy_um'])-np.array(b['fit']['xy_um']))*1000 for a,b in zip(data,outputs[0]['data'])]))))
 out=dict(endpoint='Active-emitter localization near100nm separation, conditional on sourcegeometry/PSF/dark/efficiency',
  independent_truth='NOT_ACQUIRED',nominal_resolution_target_nm=100,photon_budget_per_block=1500,
  acquired_valid_blocks=len(blocks),available_raw_window_selection='Only47sourcevalidSPCfiles outof63; sparse12.6s acquisition subset of~44.2sMAT summarizedtrace',
  model='Poisson likelihood of15detector marks; GaussianPSF integrated over sourcefiberdisks; fittedellipticity+uniformextra-background, supplieddarkvector',
  scientific_limit='No fulltimestamp emitter-count likelihood, recovery/IRF/blinkingfit, independentcoordinate truth or calibratedresolutionclaim.',
  elapsed_seconds=time.perf_counter()-start,outputs=outputs,calibration_sensitivity=sens)
 (H/'LOCALIZATION_BASELINE.json').write_text(json.dumps(out,indent=2)); print(json.dumps({k:v for k,v in out.items() if k not in ['outputs','calibration_sensitivity']},indent=2))
 for x in outputs:print(x['method'],x['blocks'],x['conditional_two_track_fit'])
 print('sensitivity',sens)
if __name__=='__main__':main()
