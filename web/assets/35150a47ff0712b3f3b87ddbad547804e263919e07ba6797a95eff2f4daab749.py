import numpy as np,json

def solve_m(A,h):
 m=np.zeros(A.shape[0])
 def obj(m):return m@m+np.sum(np.logaddexp(h-2*A.T@m,-h+2*A.T@m))
 for _ in range(100):
  t=np.tanh(h-2*A.T@m); d=1-t*t
  grad=2*(m-A@t); H=2*np.eye(len(m))+4*(A*d)@A.T
  step=np.linalg.solve(H,grad)
  if np.linalg.norm(grad)<1e-11:break
  lr=1.
  while obj(m-lr*step)>obj(m)-.1*lr*grad@step:lr/=2
  m-=lr*step
 return m,t,d

rng=np.random.default_rng(7731)
results=[]
for n in [12,16]:
 xs=(((np.arange(2**n,dtype=np.uint64)[:,None]>>np.arange(n,dtype=np.uint64))&1).astype(float)*2-1)
 theta=np.linspace(0,2*np.pi,n,endpoint=False)+.17
 for eta in [.15,.3,.6]:
  A=eta*np.stack([np.cos(theta),np.sin(theta)])
  for label,h in [('zero',np.zeros(n)),('random',rng.normal(size=n)*3),('pinned',np.r_[np.zeros(4),12*rng.choice([-1,1],n-4)])]:
   z=xs@A.T; logp=-np.sum(z*z,axis=1)+xs@h; p=np.exp(logp-logp.max());p/=p.sum()
   mean=p@xs; cov=(xs.T*p)@xs-np.outer(mean,mean); diag=np.diag(cov)
   cor=cov/np.sqrt(diag[:,None]*diag[None,:])
   m,t,d=solve_m(A,h)
   W=A*np.sqrt(d)
   cor_guess=np.eye(n)-2*W.T@np.linalg.solve(np.eye(2)+2*W@W.T,W)
   err=np.linalg.norm(cor-cor_guess,2)
   exact_tilt_logp=xs@(h-2*A.T@m)-np.sum((z-m)**2,axis=1)
   residual=(exact_tilt_logp-logp); algebra_err=float(np.ptp(residual))
   results.append(dict(n=n,eta=eta,h=label,spike_norm=float(np.linalg.norm(A,2)**2),cor_max=float(np.linalg.eigvalsh(cor)[-1]),gaussian_cor_error=float(err),scaled_error=float(err/eta**2),exact_tilt_identity_range=algebra_err))
print(json.dumps(results,indent=2))
open('work/probability_sources/rank_two_probe.json','w').write(json.dumps(results,indent=2)+'\n')
