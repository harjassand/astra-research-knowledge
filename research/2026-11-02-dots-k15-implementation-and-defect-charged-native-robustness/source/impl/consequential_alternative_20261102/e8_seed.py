import numpy as np
from scipy.special import ndtri
from scipy.stats import qmc
import json, sys

def theta(x,v,shift=0):
    z=np.arange(-4,5); w=np.exp(-np.pi/v*(x[:,:,None]+shift+z)**2)
    return w.sum(axis=2), (w*((-1.)**z)).sum(axis=2)

def gf(x,v,vec):
    g=np.zeros(len(x)); f=np.zeros(len(x)); parity=np.array(vec)%2
    for h in [0,.5]:
        A,B=theta(x,v,h)
        g+=(A.prod(axis=1)+B.prod(axis=1))/2
        X=np.where(parity[None,:],B,A);Y=np.where(parity[None,:],A,B)
        f+=np.cos(np.pi*h*sum(vec))*(X.prod(axis=1)+Y.prod(axis=1))/2
    return g,f

def calc(v,power=17,seed=1):
    u=qmc.Sobol(8,scramble=True,seed=seed).random_base2(power)
    x=ndtri(u)*np.sqrt(v/(2*np.pi))
    results=[]
    for vec in [np.array([1,-1,0,0,0,0,0,0]),np.array([2,0,0,0,0,0,0,0])]:
        jvec=vec.reshape(4,2)[:,::-1]*np.array([-1,1]); t=jvec.reshape(8)/2
        rho=[];beta=[]
        for i in range(0,len(x),8192):
            a=x[i:i+8192];g,f=gf(a,v,vec);gt,_=gf(a+t,v,vec)
            rho.extend((f/g)**2);beta.extend(np.sqrt(gt/g))
        rho=np.array(rho);beta=np.array(beta)
        results.append({'v':v,'vec':vec.tolist(),'rho':float(rho.mean()),'beta':float(beta.mean()),'gap':float((rho-beta).mean()),'iid_stderr_proxy':float((rho-beta).std()/np.sqrt(len(x))),'power':power,'seed':seed})
    return results
if __name__=='__main__':
    out=[]
    for v in [.3,.35,1/np.e,.37,.4,.4318,.49]:
       rr=calc(v,int(sys.argv[1]) if len(sys.argv)>1 else 17); out+=rr; print(json.dumps(rr),flush=True)
    open('producer-workspace/e8_results.json','w').write(json.dumps(out,indent=2))
