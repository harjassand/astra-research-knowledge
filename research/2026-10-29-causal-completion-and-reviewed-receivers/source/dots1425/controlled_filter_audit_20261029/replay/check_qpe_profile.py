import numpy as np, json, math
results=[]
for gamma in [1.,.5,.25,.1]:
 M=1<<math.ceil(math.log2(128/gamma)); y=np.arange(M); rep=y/M;rep=np.where(rep>=.75,rep-1,rep)
 worst_low=0.;worst_high=0.;tail=0.
 for lam in np.linspace(0,1,2001):
  phi=lam/2; delta=phi-y/M
  p=np.sinc(M*delta)**2/np.sinc(delta)**2
  p=p/p.sum()
  err=np.abs((delta+.5)%1-.5)
  tail=max(tail,float(p[err>=gamma/8].sum()))
  f=float(p[rep>=gamma/4].sum())
  if lam<=gamma/4:worst_low=max(worst_low,f)
  if lam>=gamma:worst_high=max(worst_high,1-f)
 assert max(tail,worst_low,worst_high)<1/28+1e-10
 results.append(dict(gamma=gamma,M=M,grid=2001,max_tail=tail,max_low_accept=worst_low,max_high_reject=worst_high))
print(json.dumps(dict(scope='Floating point QPE diagnostic, not a proof or controlled-DME deployment',results=results),indent=2))
