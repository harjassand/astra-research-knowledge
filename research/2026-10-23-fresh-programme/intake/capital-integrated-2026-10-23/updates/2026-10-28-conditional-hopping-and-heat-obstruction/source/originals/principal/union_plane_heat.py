from pathlib import Path
import itertools,numpy as np,json
OUT=Path(__file__).parent;d=np.load(OUT/'interfaces.npz');p=np.array([1,1,16,-13,0,0,4,-4,0.]);xp=[(i,j) for i in range(4) for j in range(i,4)];zp=[(i,j) for i in range(6) for j in range(i,6)]
planes=list(itertools.combinations(range(4),2));rows=[];PP=[]
for plane in planes:
 r=np.load(OUT/f'plane_{plane[0]}{plane[1]}.npz');rows.extend(r['rows']);PP.append(r['P'])
rows=np.array(rows);ON=d['ON'][rows];U,sig,_=np.linalg.svd(ON,full_matrices=True);rank=np.count_nonzero(sig>1e-9);D=U[:,rank:].T
P=np.zeros((378,468))
for i in range(6):P[63*i:63*i+63,78*i:78*i+78]=PP[i]
Ef=(d['E']@p)[rows];Ed=d['Ed'][rows];T=np.column_stack((D@P,D@Ed));Ti=np.linalg.pinv(T,rcond=1e-10);rhs=D@Ef;anchor=Ti@rhs;proj=np.eye(469)-Ti@T
ij=np.triu_indices(12);wt=np.where(ij[0]==ij[1],1.,np.sqrt(2.))
def mat(v):
 M=np.zeros((12,12));M[ij]=v/wt;M[(ij[1],ij[0])]=v/wt;return M
y=anchor.copy();dual=y*0
for step in range(30000):
 xx=anchor+proj@(y-dual);yp=np.zeros(469)
 for i in range(6):
  sl=slice(i*78,(i+1)*78);ev,V=np.linalg.eigh(mat(xx[sl]+dual[sl]));M=(V*np.maximum(ev,0))@V.T;yp[sl]=M[ij]*wt
 yp[-1]=max(0.,xx[-1]+dual[-1]);dual+=xx-yp;res=np.linalg.norm(xx-yp);change=np.linalg.norm(yp-y);y=yp
 if res<1e-9 and change<1e-9:break
print(json.dumps(dict(rank=int(rank),residual=float(res),change=float(change),gamma=float(xx[-1]),iterations=step,status='NUMERICAL_ONLY')),flush=True)
np.savez(OUT/'union_planes.npz',rows=rows,P=P,D=D,T=T,Ti=Ti,dual=dual,heat=xx)
