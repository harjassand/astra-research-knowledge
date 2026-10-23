"""Reconstruct published CSVs, not new trajectories or independent experiments.
Fits are deterministic descriptions; no confidence intervals inferred from time samples.
"""
from pathlib import Path
import json,csv,hashlib,time,resource,math
import numpy as np
from scipy.optimize import curve_fit
p=Path(__file__).parent;src=p.parent/'nitrite_finishing/dataset';start=time.perf_counter()
metadata=json.loads((src.parent/'zenodo_metadata.json').read_text())
for it in metadata['files']:
 raw=(src/it['key']).read_bytes();assert len(raw)==it['size'];assert 'md5:'+hashlib.md5(raw).hexdigest()==it['checksum']
def columns(name):
 rows=list(csv.reader((src/name).open(encoding='utf-8-sig',errors='replace')))
 return rows[0],rows[1:]
def pairs(rows,index):
 out=[]
 for row in rows:
  try:
   a,b=float(row[index]),float(row[index+1])
   if math.isfinite(a) and math.isfinite(b):out.append((a,b))
  except (ValueError,IndexError):pass
 return np.array(out)
head,rows=columns('Figure_3.csv');a=pairs(rows,0);cal=np.polyfit(a[:,0],a[:,1],1);pred=np.polyval(cal,a[:,0]);origin=(a[:,0]@a[:,1])/(a[:,0]@a[:,0])
out={'source_license':metadata['metadata'].get('license'),'dataset_record':metadata.get('id'),'calibration':{'labels':head,'points':a.tolist(),'ratio_vs_Ceff_slope':float(cal[0]),'intercept':float(cal[1]),'residuals':(a[:,1]-pred).tolist(),'through_origin_slope':float(origin),'scope':'Ordinary unweighted descriptions of five source calibration points, not a matrix-effect or statistical uncertainty bound.'},'fits':[],'controls':[]}
model=lambda t,A,k:A*(-np.expm1(-k*t))
for name in ['Figure_6A.csv','Figure_2D.csv']:
 head,rows=columns(name)
 for j in range(0,len(head),2):
  xy=pairs(rows,j)
  if len(xy)==0:continue
  x,y=xy.T
  fit,_=curve_fit(model,x,y,p0=[max(y),.001],bounds=([0,0],[10000,1]),maxfev=20000)
  out['fits'].append({'source':name,'column':head[j+1],'N_time_points':len(x),'time_range_s':[float(min(x)),float(max(x))],'last_value_source_units':float(y[-1]),'maximum_value_source_units':float(max(y)),'A_mM':float(fit[0]),'k_s-1':float(fit[1]),'rms_residual_mM':float(np.sqrt(np.mean((y-model(x,*fit))**2))),'negative_values_preserved':int(sum(y<0)),'scope':'No replicate/error model; dataset may contain processed or fitted series. Fourth concentration label is650mM vs625mM in article.'})
head,rows=columns('Figure_4.csv')
for j in range(0,len(head),2):
 xy=pairs(rows,j);x,y=xy.T
 out['controls'].append({'label':head[j+1],'value_at_2700s_linear_interpolation':float(np.interp(2700,x,y)),'last_time':float(x[-1]),'last_value':float(y[-1]),'scope':'Descriptive source series, not independent replicate CI or closed N balance.'})
head,rows=columns('Figure_1.csv');xy=pairs(rows,0)
out['radius_record']={'min_nm':float(min(xy[:,1])),'max_nm':float(max(xy[:,1])),'median_nm':float(np.median(xy[:,1])),'N':len(xy),'scope':'Unfiltered record includes excursions; not accepted as all-times constant radius.'}
out['elapsed_s']=time.perf_counter()-start;out['peak_RSS_KiB']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
(p/'dataset_result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
