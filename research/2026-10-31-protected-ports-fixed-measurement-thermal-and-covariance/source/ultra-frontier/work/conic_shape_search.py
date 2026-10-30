"""Finite shape search over exact conic ROC SDPs and actual Hessian fields."""
from pathlib import Path
from fractions import Fraction as R
import json,time,numpy as np
root=Path(__file__).resolve().parents[1];source=(root/'work/conic_capacity_model.py').read_text();helpers=(root/'work/conic_capacity_search.py').read_text();ns={'__file__':str(root/'work/conic_capacity_search.py'),'__name__':'conic_helpers'};exec(helpers[:helpers.index('rng=np.random.default_rng')],ns);field,moments,stats,fg,tensor=[ns[k] for k in ('field','moments','stats','fg','tensor')];C3=ns['C3'];nf=ns['nf'];freq=ns['freq'];minimize=ns['minimize'];rng=np.random.default_rng(20261101);old=json.loads((root/'work/conic_capacity_search.json').read_text());warm=np.array(old['best']['parameters']);start=time.perf_counter();records=[];best=None
cases=[]
for ratio in (R(1,4),R(1,2),R(1),R(2),R(4)):
 for x,y in ((R(1),R(0)),(R(3,5),R(4,5)),(R(5,13),R(12,13))):
  U=np.array([[x,-y],[y,x]],dtype=object);Ta=U@np.diag([ratio,R(1)])@U.T;cases.append([[R(v) for v in row] for row in Ta])
for case,TT in enumerate(cases):
 loc={'__file__':str(root/'work/conic_capacity_model.py'),'__name__':'conic_case_'+str(case),'T':TT};exec(source,loc);solver=loc['Model']();ns['T']=np.array(TT,float);ns['Q2']=np.array([tensor(P,2) for P in loc['Qext']]);x=warm.copy() if case%2==0 else np.concatenate((rng.normal(size=2*nf)/np.tile(1+np.sum(freq*freq,axis=1),2),np.eye(2).ravel()+.1*rng.normal(size=4)))
 for iteration in range(7):
  G=field(x);f,ell,qm=moments(G)
  try:p=solver.solve(ell,qm)
  except Exception as err:print('shape conic fit failed',case,iteration,type(err).__name__,str(err),flush=True);break
  if p is None:break
  c=np.array(p['cubic_coordinates']);q=np.array(p['quadratic_coordinates']);C=np.einsum('s,sijk->ijk',c,C3);Q=np.einsum('s,sij->ij',q,ns['Q2']);before=stats(G,C,Q);opt=minimize(lambda x:fg(x,C,Q),x,jac=True,method='L-BFGS-B',options={'maxiter':350,'ftol':1e-12,'gtol':1e-6,'maxls':40});x=opt.x;after=stats(field(x),C,Q);rec={'case':case,'T':[[str(v) for v in row] for row in TT],'iteration':iteration,'fit_energy':f+p['objective'],'before':before,'after':after,'parameters':x.tolist(),'polynomial':p,'optimizer_iterations':opt.nit};records.append(rec)
  if after['a']>0 and after['b']>0 and (best is None or after['ratio']>best['after']['ratio']):best=rec
  print(json.dumps({'case':case,'iteration':iteration,'fit_energy':rec['fit_energy'],'ratio_after':after['ratio'],'Gram_min':p['minimum_numerical_Gram_eigenvalue'],'seconds':time.perf_counter()-start}),flush=True);out={'scope':'Finite numerical shape and actual-field search with a lossless conic ROC representation. No global ROC/QC separation without independent exact conic and global extension reception.','records':records,'best':best,'seconds':time.perf_counter()-start};(root/'work/conic_shape_search.json').write_text(json.dumps(out,indent=2)+'\n')
  if rec['fit_energy']<-1e-5 or after['ratio']>1.0001:print('candidate requires exact conic, actual field, global extension checks',flush=True);break
 if best is not None and (best['fit_energy']<-1e-5 or best['after']['ratio']>1.0001):break
