#!/usr/bin/env python3
"""Acquire a quadratic support selector using eigenvector cuts and a 3-var LP.

This is not an SOS/SDP relaxation. Each retained cut is an actual necessary
global-support inequality. A sampled positive margin remains diagnostic until
the resulting exact ternary forms are proved nonnegative.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import json,time
import numpy as np
import sympy as S
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]/'sol6_openings_20261027/independent_opening/vendor'))
from scipy.optimize import linprog,minimize

H=np.array([
 [[2,0,0,0],[0,-2,0,0],[0,0,2,0],[0,0,0,-2]],
 [[0,2,0,0],[2,0,0,0],[0,0,0,2],[0,0,2,0]],
 [[0,0,0,2],[0,0,-2,0],[0,-2,0,0],[2,0,0,0]],
],dtype=float)
CX=H[0]/2; CZ=H[2]/2

def main():
 started=time.perf_counter()
 p=list(map(S.Rational,json.loads((HERE.parent/'common_cone_review/EXACT_SYMMETRIC_TARGET.json').read_text())['coefficients']))
 k1=p[0]; k2=(p[0]+p[1]+p[2]+p[3])/4
 d=(p[6]-p[7])/8; r=(p[0]+p[1]+p[2])/4
 K=np.array([[1,0,float(d/k1)],[0,float(k2/k1),0],
             [float(d/k1),0,float(r/k1)]])

 def spinor(n):
  n=np.atleast_2d(n)
  z1=np.sqrt(np.maximum((1+n[:,0])/2,1e-30))
  return np.column_stack((z1,n[:,1]/(2*z1),np.zeros(len(n)),n[:,2]/(2*z1)))

 def matrix(n):
  v=spinor(n)
  h=np.einsum('ni,kij,nj->nk',v,H,v)/2
  J=np.einsum('kij,nj->nki',H,v)
  kh=h@K
  f=np.einsum('ni,ni->n',h,kh)
  middle=K[None,:,:]-np.einsum('ni,nj->nij',kh,kh)/f[:,None,None]
  T=np.einsum('nki,nkl,nlj->nij',J,middle,J)+np.einsum('nk,kij->nij',kh,H)
  return T,h[:,2]/2

 count=2048
 idx=np.arange(count)+.5
 z=1-2*idx/count
 phi=idx*np.pi*(3-np.sqrt(5))
 n=np.column_stack((np.sqrt(1-z*z)*np.cos(phi),
                    np.sqrt(1-z*z)*np.sin(phi),z))
 th=np.linspace(0,2*np.pi,1024,endpoint=False)+.0001
 n=np.vstack((n,np.column_stack((np.cos(th),np.sin(th),np.zeros(len(th))))))
 T,det=matrix(n)
 cuts=[]; right=[]; witnesses=[]

 def add_cut(t,determinant,v,rvec):
  cuts.append([determinant*(v@CX@v),determinant*(v@CZ@v),1])
  right.append(v@t@v)
  witnesses.append({'R':rvec.tolist(),'A':v.tolist()})

 for i in range(0,len(n),64):
  for v in np.eye(4):add_cut(T[i],det[i],v,spinor(n[i])[0])
 history=[]
 solution=None
 for it in range(80):
  lp=linprog([0,0,-1],A_ub=np.array(cuts),b_ub=np.array(right),
             bounds=[(-100,100),(-100,100),(-10,10)],method='highs')
  if not lp.success: raise RuntimeError(lp.message)
  alpha,beta,margin=lp.x
  values,vectors=np.linalg.eigh(T-det[:,None,None]*(alpha*CX+beta*CZ))
  order=np.argsort(values[:,0])[:24]
  worst=float(values[order[0],0])
  history.append({'iteration':it,'alpha':float(alpha),'beta':float(beta),
                  'LP_margin':float(margin),'sample_margin':worst,'cut_count':len(cuts)})
  solution=(alpha,beta,margin,worst)
  if margin-worst<1e-9:break
  for i in order: add_cut(T[i],det[i],vectors[i,:,0],spinor(n[i])[0])

 alpha,beta,margin,worst=solution
 def direction(angles):
  theta,phi=angles
  return np.array([np.sin(theta)*np.cos(phi),np.sin(theta)*np.sin(phi),np.cos(theta)])
 def objective(angles):
  t,de=matrix(direction(angles))
  return np.linalg.eigvalsh(t[0]-de[0]*(alpha*CX+beta*CZ))[0]
 results=[]
 for i in np.argsort(values[:,0])[:16]:
  start=[np.arccos(n[i,2]),np.arctan2(n[i,1],n[i,0])]
  op=minimize(objective,start,method='Nelder-Mead',
              options={'xatol':1e-11,'fatol':1e-12,'maxiter':180})
  results.append({'value':float(op.fun),'angles':op.x.tolist(),
                  'direction':direction(op.x).tolist(),'success':bool(op.success)})
 results.sort(key=lambda z:z['value'])
 out={'status':'NUMERICAL_SELECTOR_ACQUISITION_ONLY',
      'K_normalized':K.tolist(),'alpha_normalized':float(alpha),
      'beta_normalized':float(beta),'LP_margin':float(margin),
      'sample_margin':float(worst),'global_local_checks':results,
      'history':history,'active_cuts':[
        {'index':i,'dual_weight':float(-weight),'coefficients':cuts[i],
         'right':float(right[i]),**witnesses[i]}
        for i,weight in enumerate(lp.ineqlin.marginals) if weight < -1e-8],
      'elapsed_seconds':time.perf_counter()-started}
 (HERE/'QUADRATIC_SUPPORT_GEOMETRY.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k not in ['history','global_local_checks']},indent=2))
 print('best local check',results[0])

if __name__=='__main__':main()
