import sys,json,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'root_additive_sunflower_20261010'))
from check_kernels import subspaces
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import csc_matrix

def run(m,limit):
 t=time.time(); ss=[s for s in subspaces(m) if 1<len(s)<(1<<(m-1))]
 planes=[(a,b,a^b) for a in range(1,1<<m) for b in range(a+1,1<<m) if b<a^b]
 rows=[]
 for u in planes:rows.append([int(sum(x in s for x in u)==1)for s in ss])
 for x in range(1,1<<m):rows.append([int(x not in s)for s in ss])
 A=csc_matrix(np.array(rows,dtype=float)); result=milp(c=np.ones(len(ss)),integrality=np.ones(len(ss)),bounds=Bounds(0,1),constraints=LinearConstraint(A,1,np.inf),options={'time_limit':limit,'mip_rel_gap':0,'disp':True})
 ans={'m':m,'w_target':m-1,'n_kernels':len(ss),'n_planes':len(planes),'seconds':time.time()-t,'status':result.status,'message':result.message,'fun':float(result.fun)if result.fun is not None else None,'dual_bound':float(result.mip_dual_bound)if getattr(result,'mip_dual_bound',None)is not None else None}
 if result.x is not None:
  inds=[i for i,x in enumerate(result.x)if x>0.5];ks=[ss[i]for i in inds]
  inter=set(range(1<<m));covered=0
  for k in ks:inter&=k
  for u in planes:covered+=any(sum(x in k for x in u)==1 for k in ks)
  ans.update(kernels=[sorted(k)for k in ks],exact_joint_kernel=sorted(inter),exact_planes_covered=covered,exact_check_pass=inter=={0}and covered==len(planes),counterexample=len(ks)<m and inter=={0}and covered==len(planes))
 return ans
if __name__=='__main__':
 m=int(sys.argv[1]);r=run(m,int(sys.argv[2]));Path(__file__).with_name(f'milp_m{m}.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
