"""Diagnostic-only image correspondence, no relabeling or model scoring."""
import sys,json
from pathlib import Path
import numpy as np
sys.path.insert(0,'/workspace/shared/stm_prediction_run');import audit
out=[]
def detrend(a):
 yy,xx=np.indices(a.shape);X=np.c_[np.ones(a.size),xx.ravel(),yy.ravel()];return a-(X@np.linalg.lstsq(X,a.ravel(),rcond=None)[0]).reshape(a.shape)
def corr(a,b):
 a=a-a.mean();b=b-b.mean();return float(np.sum(a*b)/np.sqrt(np.sum(a*a)*np.sum(b*b)))
for eid in (0,1500,2920):
 root=audit.parse(audit.CONTROL/f'acquired/training_data_and_model_parameters/training_data/{eid:05d}.npy');e=root.state[4][0];start=e['episode_start_info'];prev=start;entries=[('start',start)]
 for j,info in enumerate(e['transitions']['info']):
  im=info['img_info']
  if all(im[k] is not prev[k] for k in audit.IMAGES):entries.append((j,im))
  prev=im
 for j,im in entries:
  shape=im['img_forward'].state[1];F=detrend(np.array(audit.array(im['img_forward'])).reshape(shape));B=detrend(np.array(audit.array(im['img_backward'])).reshape(shape));scores=[]
  for dy in range(-3,4):
   for dx in range(-20,21):
    fy=slice(max(dy,0),min(shape[0],shape[0]+dy));by=slice(max(-dy,0),min(shape[0],shape[0]-dy));fx=slice(max(dx,0),min(shape[1],shape[1]+dx));bx=slice(max(-dx,0),min(shape[1],shape[1]-dx));scores.append((corr(F[fy,fx],B[by,bx]),dx,dy))
  best=max(scores);out.append({'episode':eid,'boundary':j,'method':'plane-detrended overlap Pearson, shifts dx[-20,20],dy[-3,3], no interpolation','unshifted_correlation':corr(F,B),'best_correlation':best[0],'F_relative_to_B_shift_x_pixels':best[1],'F_relative_to_B_shift_y_pixels':best[2],'x_shift_nm':best[1]*audit.vec(im['len_nm'])[0]/shape[1]})
print(json.dumps(out,indent=2))
