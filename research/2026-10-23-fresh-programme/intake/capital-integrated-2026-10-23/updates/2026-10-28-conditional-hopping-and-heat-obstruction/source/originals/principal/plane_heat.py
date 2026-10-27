from pathlib import Path
import itertools,numpy as np,json
OUT=Path(__file__).parent;d=np.load(OUT/'interfaces.npz');p=np.array([1,1,16,-13,0,0,4,-4,0.]);xp=[(i,j) for i in range(4) for j in range(i,4)];zp=[(i,j) for i in range(6) for j in range(i,6)]
recs=[]
for plane in itertools.combinations(range(4),2):
 sub=[i for i,pair in enumerate(xp) if all(k in plane for k in pair)];rows=np.array([21*i+j for i in sub for j in range(21)])
 ON=d['ON'][rows];U,sig,_=np.linalg.svd(ON,full_matrices=True);rank=np.count_nonzero(sig>1e-9);D=U[:,rank:].T
 feat=[(i,j) for i in plane for j in range(6)];ij=np.triu_indices(12);wt=np.where(ij[0]==ij[1],1.,np.sqrt(2.));P=np.zeros((63,78))
 look={(xp[i],z):21*h+j for h,i in enumerate(sub) for j,z in enumerate(zp)}
 for h,(i,j) in enumerate(zip(*ij)):
  aa=tuple(sorted((feat[i][0],feat[j][0])));zz=tuple(sorted((feat[i][1],feat[j][1])));P[look[aa,zz],h]=1. if i==j else np.sqrt(2.)
 Ef=(d['E']@p)[rows];Ed=d['Ed'][rows];T=np.column_stack((D@P,D@Ed));Ti=np.linalg.pinv(T,rcond=1e-10);rhs=D@Ef;anchor=Ti@rhs;proj=np.eye(79)-Ti@T
 def mat(v):
  M=np.zeros((12,12));M[ij]=v/wt;M[(ij[1],ij[0])]=v/wt;return M
 y=anchor.copy();dual=y*0
 for step in range(15000):
  xx=anchor+proj@(y-dual);ev,V=np.linalg.eigh(mat(xx[:-1]+dual[:-1]));M=(V*np.maximum(ev,0))@V.T;yp=np.r_[M[ij]*wt,max(0.,xx[-1]+dual[-1])];dual+=xx-yp;res=np.linalg.norm(xx-yp);change=np.linalg.norm(yp-y);y=yp
  if res<1e-9 and change<1e-9:break
 rec=dict(plane=plane,rank=int(rank),residual=float(res),change=float(change),gamma=float(xx[-1]),iterations=step,status='NUMERICAL_ONLY');recs.append(rec);print(json.dumps(rec),flush=True)
 np.savez(OUT/f'plane_{plane[0]}{plane[1]}.npz',plane=plane,rows=rows,P=P,D=D,T=T,Ti=Ti,dual=dual,heat=xx)
(OUT/'plane_results.json').write_text(json.dumps(recs,indent=2)+'\n')
