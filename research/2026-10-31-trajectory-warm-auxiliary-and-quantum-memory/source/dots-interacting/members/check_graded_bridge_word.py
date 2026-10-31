"""Monte Carlo diagnostic of operator-valued total-excitation bridge.
Not the finite-bit quantum compiler or a practical performance benchmark.
"""
from pathlib import Path
import json,numpy as np
from scipy.linalg import expm,eigh
from scipy.special import gammaln,logsumexp
rng=np.random.default_rng(311620); L=2;T=.4;Gamma=.5;samples=2000
occ=[(i,j) for i in range(L+1) for j in range(L+1-i)];idx={x:i for i,x in enumerate(occ)};d=len(occ);D=2*d
I=np.eye(2);sx=np.array([[0,1],[1,0]],complex);sm=np.array([[0,1],[0,0]],complex)
a=[]
for mode in range(2):
 A=np.zeros((d,d),complex)
 for j,n in enumerate(occ):
  if n[mode]:
   m=list(n);m[mode]-=1;A[idx[tuple(m)],j]=np.sqrt(n[mode])
 a.append(A)
N=np.kron(I,np.diag([sum(n) for n in occ]));nv=np.diag(N).real
ids=[np.where(nv==n)[0] for n in range(L+1)]
n0=a[0].conj().T@a[0]
Hf=np.kron(.23*sx,np.eye(d))+np.kron(I,.7*n0@(n0-np.eye(d))+.41*(a[0].conj().T@a[1]+a[1].conj().T@a[0]))
e,v=eigh(Hf)
def drift(t,U):return v@(np.exp(-1j*e*t)[:,None]*(v.conj().T@U))
def bridge(n,m,lam):
 delta=2*lam;nu=Gamma/2;x=delta*T;one=-np.expm1(-x)
 logz=-x-2*np.log(one)-np.log(nu/delta)
 ks=np.arange(min(n,m)+1)
 logs=gammaln(n+1)-gammaln(ks+1)-gammaln(n-ks+1)+gammaln(m+1)-gammaln(m-ks+1)+ks*logz
 k=int(rng.choice(ks,p=np.exp(logs-logsumexp(logs))))
 def te():return -np.log1p(-rng.random()*one)/delta
 events=[(te(),-1) for _ in range(n-k)]+[(T-te(),1) for _ in range(m-k)]
 for _ in range(int(rng.poisson(nu*T))):
  b=T*rng.random();death=b+rng.exponential(1/delta)
  if death<=T:events.extend([(b,1),(death,-1)])
 return sorted(events)
def weight(m,n,lam):
 g=np.sqrt(Gamma*lam);x=2*lam*T;one=-np.expm1(-x);alpha=g*one/(2*lam);cc=Gamma*T/2-Gamma*one/(4*lam)
 vals=[(m+n-2*k)*np.log(alpha)-x*k-gammaln(m-k+1)-gammaln(n-k+1)-gammaln(k+1) for k in range(min(m,n)+1)]
 return np.exp(cc+.5*(gammaln(m+1)+gammaln(n+1))+logsumexp(vals))
rows=[]
for lam in [2.,100.]:
 g=np.sqrt(Gamma*lam)
 R=g*(np.kron(.6*sx,a[0].conj().T)+np.kron(.8*sm,a[1].conj().T))
 Op=R@np.diag(1/(g*np.sqrt(nv+1)));Om=Op.conj().T
 exact=expm(T*(-1j*(Hf+R+R.conj().T)-2*lam*N));estimate=np.zeros((D,D),complex);maxevents=0
 for n in range(L+1):
  initial=np.eye(D,dtype=complex)[:,ids[n]]
  for m in range(L+1):
   avg=np.zeros((D,len(ids[n])),complex)
   for _ in range(samples):
    ev=bridge(n,m,lam);maxevents=max(maxevents,len(ev));number=n;last=0.;word=initial.copy();zero=False
    for time,sign in ev:
     word=(-1j*(Op if sign==1 else Om))@drift(time-last,word)
     number+=sign;last=time
     if number>L:zero=True;break
    if not zero:
     assert number==m
     avg+=drift(T-last,word)
   estimate[np.ix_(ids[m],ids[n])]=weight(m,n,lam)*avg[ids[m],:]/samples
 error=float(np.linalg.norm(estimate-exact,'fro'))
 rows.append({'lambda':lam,'frobenius_error':error,'maximum_virtual_events':maxevents});assert error<.15
result={'seed':311620,'scope':'finite matrix Monte Carlo word diagnostic only','modes':2,'total_cutoff':L,'sector_dimensions':[len(x) for x in ids],'samples_per_sector_pair':samples,'Gamma':Gamma,'T':T,'rows':rows}
print(json.dumps(result,indent=2));Path(__file__).with_name('graded_bridge_word_checks.json').write_text(json.dumps(result,indent=2)+'\n')
