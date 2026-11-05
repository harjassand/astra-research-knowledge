"""Independent eigenvector-exchange LP solve of reduced energy-moment SDP.
Exploratory numerics, not interval-certified. Bounds on coefficients are checked.
"""
import os,sys
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
sys.path.insert(0,str(__import__('pathlib').Path(__file__).resolve().parents[1]))
import numpy as np, scipy.linalg as la, scipy.optimize as opt, time,json,resource
from pathlib import Path
from test_repair import iso,local_apply
OUT=Path(__file__).parent

def run(A,n,tolerance=1e-7):
 start=time.perf_counter();d,D,_=A.shape;dim=d**n
 V2=iso(A,2).real;h=np.eye(d*d)-V2@V2.T;h=np.round(h*6)/6
 hs=[local_apply(np.eye(dim),h,(i,i+1),d,n).real for i in range(n-1)];m=n-1
 U=la.null_space(iso(A,n).T).real;r=U.shape[1]
 ant=lambda i,j:hs[i]@hs[j]+hs[j]@hs[i]
 diffs=[hs[i+1]-hs[i] for i in range(n-2)]
 for i in range(n-2):
  for j in range(i+1,n-2):diffs.append(ant(i+1,j+1)-ant(i,j))
 G=hs[0]+sum(ant(0,j) for j in range(1,m))
 q0=sum((hs[i]+hs[i+1])@(hs[i]+hs[i+1]) for i in range(m-1))/(m-1)
 for distance in range(2,m):q0+=sum(ant(i,i+distance) for i in range(m-distance))/(m-distance)
 P0=U.T@q0@U;groundmargin=la.eigvalsh(P0,subset_by_index=[0,0])[0]
 base=U.T@G@U;terms=np.stack([-U.T@hs[0]@U]+[U.T@x@U for x in diffs]);nv=len(terms)
 # Find q0 coordinates and independently check the strict feasible witness.
 flat=terms.reshape(nv,-1).T;x0=la.lstsq(flat,(P0-base).reshape(-1))[0]
 assert abs(x0[0]+1)<1e-8
 assert la.norm(base+np.einsum('i,ijk->jk',x0,terms)-P0)<1e-8
 # PSD requires every diagonal >=0; add eigenvector cuts thereafter.
 C=-np.stack([np.diag(x) for x in terms],axis=1);b=np.diag(base)
 objective=np.zeros(nv);objective[0]=-1;bounds=[(-1,2)]+[(-100,100)]*(nv-1)
 best=-1;bestx=x0;history=[];build=time.perf_counter()-start
 for it in range(400):
  lp=opt.linprog(objective,A_ub=C,b_ub=b,bounds=bounds,method='highs')
  if not lp.success:raise RuntimeError(lp.message)
  x=lp.x;Q=base+np.einsum('i,ijk->jk',x,terms)
  eig,vec=la.eigh(Q,subset_by_index=[0,min(7,r-1)]);emin=eig[0]
  t=max(0,-emin)/(groundmargin+max(0,-emin));candidate=(1-t)*x[0]-t
  if candidate>best:best=candidate;bestx=(1-t)*x+t*x0
  history.append([it,float(x[0]),float(best),float(emin)])
  if it%20==0:print(n,history[-1],flush=True)
  if x[0]-best<tolerance or emin> -1e-9:break
  use=vec[:,eig< -1e-10]
  if use.shape[1]==0:use=vec[:,:1]
  new=-np.einsum('pi,kpq,qi->ik',use,terms,use,optimize=True)
  rhs=np.einsum('pi,pq,qi->i',use,base,use,optimize=True)
  C=np.vstack([C,new]);b=np.r_[b,rhs]
 H=sum(hs);open_e=la.eigvalsh(U.T@H@U,subset_by_index=[0,0])[0]
 result={'n':n,'cone_dimension':r,'scalar_variables':nv,'iterations':it+1,'cuts':len(b),
 'LP_box_upper_exploratory':float(x[0]),'PSD_mixture_lower_exploratory':float(best),
 'last_min_eigenvalue':float(emin),'strict_witness_min_eigenvalue':float(groundmargin),
 'coefficient_bound':100,'max_abs_divergence_coefficient':float(max(abs(x[1:]))),
 'open_gap':float(open_e),'knabe':float((m*open_e-1)/(m-1)),
 'build_seconds':build,'total_seconds':time.perf_counter()-start,
 'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
 'best_coefficients':bestx.tolist(),'last_coefficients':x.tolist(),'history':history}
 (OUT/f'exchange_n{n}.json').write_text(json.dumps(result,indent=2)+'\n')
 print('DONE',json.dumps({k:v for k,v in result.items() if k not in ['history','best_coefficients','last_coefficients']}),flush=True)
 return result
if __name__=='__main__':
 A=np.load(OUT.parent/'mps_inputs.npz')['aklt']
 for n in [4,5,6]:run(A,n)
