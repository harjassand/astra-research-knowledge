import csv,json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize_scalar, brentq
OUT=Path(__file__).resolve().parent
ROOT=OUT.parent/'autonomous_correction_evaluator'/'QEC data'/'source_data'
def parse(path):
 rows=[[x.replace("_unnorm", "") for x in row] for row in csv.reader(path.open())]; h=next(i for i,r in enumerate(rows) if r and 'storage_time_ms' in r and 'phy_fidelity' in r); end=next(i for i in range(h+1,len(rows)) if not rows[i]); data=list(csv.DictReader([','.join(r) for r in rows[h:end]])); h=next(i for i,r in enumerate(rows) if r and r[0]=='series'); p={r[0]:dict(zip(rows[h][1:],map(float,r[1:]))) for r in rows[h+1:h+4]}; return data,p
# At fixed tau the nuisance problem is convex weighted linear least squares.
# Enumerate unconstrained solution and every edge of triangular feasible domain.
def profile(tau,t,y,s,domain):
 e=np.exp(-(t/tau)**2); X=np.array([np.ones(len(t)),e]).T/s[:,None]; Y=y/s
 if domain.startswith('fixed'):
  a=float(domain[5:]); c=np.clip(np.dot(e/s,(y-a)/s)/max(np.dot(e/s,e/s),1e-300),0,1-a); candidates=[np.array([a,c])]
 else:
  amin=.4 if domain=='a_ge_0.4_diagnostic' else 0.; candidates=[]; ac=np.linalg.lstsq(X,Y,rcond=None)[0]
  if ac[0]>=amin and ac[1]>=0 and sum(ac)<=1: candidates.append(ac)
  c=np.clip(np.dot(e/s,(y-amin)/s)/max(np.dot(e/s,e/s),1e-300),0,1-amin); candidates.append([amin,c])
  a=np.clip(np.sum(y/s**2)/np.sum(1/s**2),amin,1); candidates.append([a,0])
  z=(1-e)/s; a=np.clip(np.dot(z,(y-e)/s)/np.dot(z,z),amin,1); candidates.append([a,1-a])
 vals=[float(np.sum((X@ac-Y)**2)) for ac in candidates]; i=np.argmin(vals); return vals[i],list(map(float,candidates[i]))
def cross(tau,a,c,F=.75):
 if a+c<=F:return 0.
 if a>=F:return None
 return float(tau*np.sqrt(-np.log((F-a)/c)))
results={}; profiles=[]; pairs={}
for fn in ['Fig4a_source.csv','EDFig4a_source.csv','Fig4b_source.csv','EDFig4b_source.csv']:
 data,params=parse(ROOT/fn); results[fn]={}; pairs[fn]=[]
 for r in data:
  if r['QEC_fidelity']:
   for p in data:
    if p['phy_fidelity'] and float(p['storage_time_ms'])==float(r['storage_time_ms']): pairs[fn].append({'t_ms':float(r['storage_time_ms']),'difference':float(r['QEC_fidelity'])-float(p['phy_fidelity'])})
 for series in ['phy','noQEC','QEC']:
  d=[r for r in data if r[series+'_fidelity']]; t=np.array([float(r['storage_time_ms']) for r in d]); y=np.array([float(r[series+'_fidelity']) for r in d]); s=np.array([float(r[series+'_err']) for r in d]); p=params[series]; tau=p['tau_ms']; a=p['a']; c=p['c']; z=(a+c*np.exp(-(t/tau)**2)-y)/s; q=float(z@z)
  r={'n':len(t),'reported':dict(p,weighted_SSE=q,max_abs_standardized_residual=float(max(abs(z))),cross_075_ms=cross(tau,a,c)), 'sensitivities':{}}
  for domain in ['simplex','fixed0.5','fixed0.25','a_ge_0.4_diagnostic']:
   grid=np.linspace(np.log(.001),np.log(1e5),1800); vals=np.array([profile(np.exp(x),t,y,s,domain)[0] for x in grid]); i=np.argmin(vals); opt=minimize_scalar(lambda x:profile(np.exp(x),t,y,s,domain)[0],bounds=(grid[max(0,i-1)],grid[min(len(grid)-1,i+1)]),method='bounded',options={'xatol':1e-12}); tau=float(np.exp(opt.x)); q,ac=profile(tau,t,y,s,domain); a,c=ac
   mask=vals<=q+1; selected=np.exp(grid[mask]); left=brentq(lambda x:profile(np.exp(x),t,y,s,domain)[0]-q-1,grid[0],opt.x); right=brentq(lambda x:profile(np.exp(x),t,y,s,domain)[0]-q-1,opt.x,grid[-1]); r['sensitivities'][domain]={'tau_ms':tau,'a':a,'c':c,'weighted_SSE':q,'cross_075_ms':cross(tau,a,c),'delta_SSE_le_1_tau_range_ms':[float(np.exp(left)),float(np.exp(right))]}
   for x,v in zip(grid,vals): profiles.append([fn,series,domain,float(np.exp(x)),float(v)])
  results[fn][series]=r
(OUT/'results.json').write_text(json.dumps({'fits':results,'paired_measured':pairs},indent=2))
with (OUT/'profiles.csv').open('w') as f:
 w=csv.writer(f); w.writerow(['file','series','domain','tau_ms','weighted_SSE']);w.writerows(profiles)
for fn,rr in results.items():
 print('\n',fn)
 for name,r in rr.items():
  print(name, 'reported',*[round(r['reported'][k],5) for k in ['tau_ms','a','c','weighted_SSE','cross_075_ms']])
  for mode,v in r['sensitivities'].items(): print(' ',mode,*[round(v[k],5) if v[k] is not None else None for k in ['tau_ms','a','c','weighted_SSE','cross_075_ms']],v['delta_SSE_le_1_tau_range_ms'])
 for mode in ['simplex','fixed0.5','fixed0.25','a_ge_0.4_diagnostic']:
  a=rr['QEC']['sensitivities'][mode]; b=rr['phy']['sensitivities'][mode]; print(mode,'ratio',a['tau_ms']/b['tau_ms'],'threshold ratio',a['cross_075_ms']/b['cross_075_ms'])
