import sys,itertools,math,json,time
from pathlib import Path
import numpy as np
from scipy.special import expit
sys.path.insert(0,str(Path(__file__).resolve().parent));from compare import acquire,State,failure,bar
q=np.array([.02,.07,.11,.17,.23]);E=np.array(list(itertools.product([0,1],repeat=5)),np.uint8);w=E.sum(1);P=np.prod(np.where(E,q,1-q),axis=1);sq=np.sqrt(q/(1-q));rho=1/11;errs=[]
for a,e in enumerate(E):
 lam=np.where(e,1/sq,sq).sum()
 for i in range(5):
  ee=e.copy();ee[i]^=1;b=np.flatnonzero(np.all(E==ee,axis=1))[0];ll=np.where(ee,1/sq,sq).sum();forward=(1/sq[i] if e[i] else sq[i])/lam*min(1,lam/ll);reverse=(1/sq[i] if ee[i] else sq[i])/ll*min(1,ll/lam);errs.append(abs(P[a]*forward-P[b]*reverse))
maxsr=0.
for a,e in enumerate(E):
 for b,f in enumerate(E):
  flip=np.where(e,rho*(1-q),rho*q);back=np.where(f,rho*(1-q),rho*q);pr=np.prod(np.where(e!=f,flip,1-flip));rev=np.prod(np.where(e!=f,back,1-back));maxsr=max(maxsr,abs(P[a]*pr-P[b]*rev))
# Exact enumerated distributions conditioned on a deliberately disconnected F.
F=(w>=3)|np.all(E==[1,0,0,0,0],axis=1);ts=[math.log(8),.7,0];probs=[];hist=[]
for t in ts:
 qt=expit(np.log(q/(1-q))+t);p=np.prod(np.where(E,qt,1-qt),axis=1);probs.append(float(p[F].sum()));hist.append(np.bincount(w[F].astype(int),weights=p[F]/p[F].sum(),minlength=6))
barerr=max(abs(bar(hist[j],hist[j+1],ts[j],ts[j+1],q)-math.log(probs[j+1]/probs[j])) for j in range(2))
m=acquire();rng=np.random.default_rng(202611054402);checks=0
for z in range(300):
 e=(rng.random(m.n)<m.q).astype(np.uint8);st=State(m,e);inds=rng.choice(m.n,int(rng.integers(1,15)),replace=False);st.flip(inds);truth=m.decode(st.e);f=int((st.e[m.cut].sum()+truth[m.cut].sum())%2);assert st.fail()==f;assert st.w==int(st.e.sum());assert np.array_equal(st.s,np.asarray(m.H@st.e,dtype=np.uint8)%2);st.flip(inds);assert np.array_equal(st.e,e);checks+=1
out=dict(zanella_max_detailed_balance_error=max(errs),subregion_max_detailed_balance_error=maxsr,BAR_max_log_error=barerr,actual_graph_incremental_checks=checks,scope='Floating mathematical sanity checks and exact bit-array invariants; no d21 mixing certificate')
assert max(errs)<1e-16 and maxsr<1e-16 and barerr<1e-10
print(json.dumps(out,indent=2));Path(__file__).with_name('kernel_checks.json').write_text(json.dumps(out,indent=2)+'\n')
