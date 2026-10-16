import sys,json
from pathlib import Path
import numpy as np
sys.path.insert(0,'/workspace/shared/stm_prediction_run')
import audit
out=[]
for eid in (0,1500,2920):
 p=audit.CONTROL/f'acquired/training_data_and_model_parameters/training_data/{eid:05d}.npy';root=audit.parse(p);e=root.state[4][0];start=e['episode_start_info'];prev=start
 entries=[('start',start,start['info'],'start_')]
 for j,info in enumerate(e['transitions']['info']):
  im=info['img_info']
  if all(im[k] is not prev[k] for k in audit.IMAGES):entries.append((j,im,info,'atom_'))
  prev=im
 records=[]
 for j,im,info,pre in entries:
  f=np.array(audit.vec(info[pre+'absolute_nm_f']));b=np.array(audit.vec(info[pre+'absolute_nm_b']));rf=np.array(audit.vec(info[pre+'relative_nm_f']));rb=np.array(audit.vec(info[pre+'relative_nm_b']));off=np.array(audit.vec(im['offset_nm']));extent=np.array(audit.vec(im['len_nm']));shape=im['img_forward'].state[1]
  pixsize=extent/np.array(shape);origin=off-np.array([extent[0]/2,0]);fp=(f-origin)/pixsize;bp=(b-origin)/pixsize
  F=np.array(audit.array(im['img_forward'])).reshape(shape);B=np.array(audit.array(im['img_backward'])).reshape(shape)
  def corr(a,b):return float(np.corrcoef(a.ravel(),b.ravel())[0,1])
  records.append({'boundary':j,'f_nm':f.tolist(),'b_nm':b.tolist(),'f_minus_b_nm':(f-b).tolist(),'absolute_disagreement_nm':float(np.linalg.norm(f-b)),'relative_disagreement_nm':float(np.linalg.norm(rf-rb)),'relative_f_minus_b_nm':(rf-rb).tolist(),'implied_template_f_minus_b_nm':((f-rf)-(b-rb)).tolist(),'offset_nm':off.tolist(),'extent_nm':extent.tolist(),'shape':shape,'f_inferred_pixel_xy':fp.tolist(),'b_inferred_pixel_xy':bp.tolist(),'raw_pair_correlation':corr(F,B),'flip_x_correlation':corr(F,B[:,::-1]),'flip_y_correlation':corr(F,B[::-1]),'flip_xy_correlation':corr(F,B[::-1,::-1])})
 out.append({'episode':eid,'unique_scan_records_including_reset':records})
print(json.dumps(out,indent=2))
