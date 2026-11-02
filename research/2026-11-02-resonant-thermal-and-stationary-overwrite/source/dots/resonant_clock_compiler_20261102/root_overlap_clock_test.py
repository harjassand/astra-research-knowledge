"""Two overlapping XX/ZZ checks: exact gauge blocks, tuned/untuned path clocks.
Finite diagnostic, no many-check or asymptotic theorem. Sparse low-energy trace
bounds use computed gaps and are numerical corroboration, not interval certificates.
"""
import numpy as np,json,math,sys
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh
from scipy.special import logsumexp

def Hblock(K,g,c,sx,sz):
 pos=[0,K//2]; xp=[0]*K;zp=[0]*K
 for q in range(K):
  xp[q]=sum(1<<j for j,p in enumerate(pos) if p<q);zp[q]=xp[q]
 rows=[];cols=[];data=[]
 for q in range(K):
  for r in range(K):
   i=q*K+r;rows.append(i);cols.append(i);data.append((c if q==0 else 2.)+(c if r==0 else 2.))
   for a,j in [(0,q),(1,r)]:
    h=g if j in [0,K-1] else 1.
    if a==0:
     p=(-1.)**(zp[r].bit_count()%2) if j==K-1 else 1.
     if j==K-1:p*=sx
     k=((q+1)%K)*K+r
    else:
     zmask=next((1<<b for b,v in enumerate(pos) if v==j),0)
     p=(-1.)**((xp[q]&zmask).bit_count()%2)
     if j==K-1:p*=sz
     k=q*K+(r+1)%K
    v=-h*p;rows.extend([i,k]);cols.extend([k,i]);data.extend([v,v])
 return coo_matrix((data,(rows,cols)),shape=(K*K,K*K)).tocsr()
def isolate(K,g,c,s):
 H=np.diag([c]+[2.]*(K-1))
 for j in range(K):
  h=g if j in [0,K-1] else 1.;v=-h*(s if j==K-1 else 1.)
  H[j,(j+1)%K]+=v;H[(j+1)%K,j]+=v
 return np.linalg.eigvalsh(H)
records=[]
Ks=[int(x) for x in sys.argv[1:]] or [3,8,24,64]
for K in Ks:
 for eta in [.1,.3]:
  for tuned in [False,True]:
   g=eta/(math.sqrt(K) if tuned else K);c=2*g*g if tuned else 0.;J0=2*g*g/K;beta=5/J0
   iep=isolate(K,g,c,1);iem=isolate(K,g,c,-1);Jiso=(iem[0]-iep[0])/2
   F={};gaps=[];unc=[]
   for sx in [-1,1]:
    for sz in [-1,1]:
     H=Hblock(K,g,c,sx,sz)
     if K<=8:
      ev=np.linalg.eigvalsh(H.toarray());f=-logsumexp(-beta*ev)/beta;u=0
     else:
      ev=np.sort(eigsh(H,k=3,which='SA',tol=1e-11,return_eigenvectors=False,maxiter=30000));f=ev[0]
      u=np.log1p((K*K-1)*np.exp(-beta*(ev[1]-ev[0])))/beta
     F[sx,sz]=f;gaps.append(float(ev[1]-ev[0]));unc.append(float(u))
   jx=-sum(x*f for (x,z),f in F.items())/4;jz=-sum(z*f for (x,z),f in F.items())/4;jxz=-sum(x*z*f for (x,z),f in F.items())/4
   r=dict(K=K,eta=eta,tuned=tuned,g=g,counterterm=c,J0=J0,Jisolated=Jiso,isolated_plus_ground=float(iep[0]),beta=beta,Jx=jx,Jz=jz,Jxz=jxz,singleton_ratio_min=min(jx,jz)/Jiso,cross_ratio=abs(jxz)/Jiso,min_computed_gap=min(gaps),numeric_free_energy_uncertainty=max(unc),sector_ground_or_free_energies={str(s):float(v) for s,v in F.items()})
   records.append(r);print(json.dumps(r),flush=True)
   open(__file__.replace('.py','.json'),'w').write(json.dumps(records,indent=2)+'\n')
