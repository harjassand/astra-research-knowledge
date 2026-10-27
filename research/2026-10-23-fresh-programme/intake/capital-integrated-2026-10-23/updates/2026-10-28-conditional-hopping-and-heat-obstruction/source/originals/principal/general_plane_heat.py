from pathlib import Path
import numpy as np,json,itertools,time
OUT=Path(__file__).parent;d=np.load(OUT/'interfaces.npz');p=np.array([1,1,16,-13,0,0,4,-4,0.]);xp=[(i,j) for i in range(4) for j in range(i,4)];zp=[(i,j) for i in range(6) for j in range(i,6)]
ij=np.triu_indices(12);wt=np.where(ij[0]==ij[1],1.,np.sqrt(2.))
def mat(v):
 M=np.zeros((12,12));M[ij]=v/wt;M[(ij[1],ij[0])]=v/wt;return M
# Map polynomial coefficients (s²,st,t²) times quadratic z to Q12.
V=np.zeros((78,63))
for h in range(63):
 coef=np.zeros(63);coef[h]=1;M=[]
 for k in range(3):
  mm=np.zeros((6,6))
  for l,(a,b) in enumerate(zp):mm[a,b]=mm[b,a]=coef[21*k+l]*(1 if a==b else .5)
  M.append(mm)
 Q=np.block([[M[0],M[1]/2],[M[1]/2,M[2]]]);V[:,h]=Q[ij]*wt
skew=[]
for a,b in itertools.combinations(range(6),2):
 K=np.zeros((6,6));K[a,b]=1;K[b,a]=-1;Q=np.block([[np.zeros((6,6)),K],[-K,np.zeros((6,6))]]);skew.append(Q[ij]*wt)
skew=np.array(skew).T
planes=[]
for a,b in itertools.combinations(range(4),2):planes.append(np.eye(4)[:,[a,b]])
rng=np.random.default_rng(20261027)
while len(planes)<24:
 plane=rng.integers(-2,3,size=(4,2)).astype(float)
 if np.linalg.matrix_rank(plane)==2:planes.append(plane)
N=len(planes);B=np.zeros((78*N+1,46+15*N));anchor=np.zeros(78*N+1);Ls=[]
for h,plane in enumerate(planes):
 transform=np.array([[plane[i,0]*plane[j,0] for i,j in xp],[(plane[i,0]*plane[j,1]+plane[i,1]*plane[j,0]) for i,j in xp],[plane[i,1]*plane[j,1] for i,j in xp]])
 L=np.kron(transform,np.eye(21));Ls.append(L);sl=slice(h*78,(h+1)*78)
 anchor[sl]=V@L@d['E']@p;B[sl,:45]=V@L@d['ON'];B[sl,45]=-V@L@d['Ed'];B[sl,46+15*h:46+15*(h+1)]=skew
B[-1,45]=1;Bi=np.linalg.pinv(B,rcond=1e-10);y=anchor.copy();dual=y*0;tick=time.monotonic()
for step in range(15000):
 v=y-dual;xx=anchor+B@(Bi@(v-anchor));yp=np.zeros_like(xx)
 for h in range(N):
  sl=slice(78*h,78*(h+1));ev,U=np.linalg.eigh(mat(xx[sl]+dual[sl]));M=(U*np.maximum(ev,0))@U.T;yp[sl]=M[ij]*wt
 yp[-1]=max(0.,xx[-1]+dual[-1]);dual+=xx-yp;res=np.linalg.norm(xx-yp);change=np.linalg.norm(yp-y);y=yp
 if step%3000==0:print(step,res,change,xx[-1],time.monotonic()-tick,flush=True)
 if res<1e-8 and change<1e-8:break
rec=dict(planes=[x.tolist() for x in planes],residual=float(res),change=float(change),iterations=step,gamma=float(xx[-1]),status='NUMERICAL_ONLY')
(OUT/'general_plane_results.json').write_text(json.dumps(rec,indent=2)+'\n');np.savez(OUT/'general_planes.npz',planes=planes,heat=xx,dual=dual,B=B,Bi=Bi,anchor=anchor,V=V,L=np.array(Ls));print('FINAL',rec['residual'],rec['change'],flush=True)
