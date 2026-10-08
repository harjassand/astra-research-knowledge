import numpy as np,json
from numpy.polynomial.legendre import leggauss
x,w=leggauss(500);r=4*(x+1);w=4*w
logp=np.log(8*np.sqrt(2/np.pi))+2*np.log(r)-2*r*r
mu=np.linspace(-5,5,1001)
ts=np.geomspace(.0001,100,181)
def ls(z):return z+np.log(-np.expm1(-2*z))-np.log(2)
results=[]
for c in [.3282,.33,.35,.4,.5,1.]:
    q=1/c;best=(-np.inf,None,None)
    for t in ts:
        k=q-2*t*mu
        kr=np.abs(k)[:,None]*r[None,:]
        with np.errstate(divide='ignore',invalid='ignore'):
            logratio=np.log(q/np.abs(k))[:,None]+ls(kr)-ls(q*r)[None,:]
        tiny=np.abs(k)<1e-10
        logratio[tiny,:]=np.log(q*r/np.sinh(q*r))[None,:]
        log_integrand=logp[None,:]-t*(r[None,:]**2+mu[:,None]**2)+logratio
        F=np.sum(w[None,:]*np.exp(log_integrand),axis=1)
        gaps=F-1/(1+t/2)
        kbest=int(np.argmax(gaps))
        if gaps[kbest]>best[0]:best=(float(gaps[kbest]),float(t),float(mu[kbest]))
    results.append({'c':c,'max_grid_gap':best[0],'t':best[1],'mu':best[2]})
print(json.dumps(results,indent=2))
with open('work/agents/thermal_blind/results/broad_center_scan.json','w') as f:json.dump(results,f,indent=2)
