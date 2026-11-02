"""Diagnostic optimization of scalar GKP reliability flags; no interval certificate."""
import json, math
import numpy as np
from scipy.special import ndtr, xlogy
from scipy.integrate import quad
from scipy.optimize import minimize, minimize_scalar

L=math.sqrt(math.pi); HALF=L/2
M=np.arange(-12,13); ODD=M%2!=0

def h2(p):
    p=np.asarray(p)
    return -(xlogy(p,p)+xlogy(1-p,1-p))/math.log(2)

def interval_prob(a,b):
    a=np.asarray(a); b=np.asarray(b)
    return np.where(a>0,ndtr(-a)-ndtr(-b),ndtr(b)-ndtr(a))

def bins(v, thresholds):
    edges=np.r_[0,np.sort(thresholds),HALF]
    aa=(edges[:-1,None]+L*M)/math.sqrt(v)
    bb=(edges[1:,None]+L*M)/math.sqrt(v)
    z=2*interval_prob(aa,bb)
    w=z.sum(1); e=z[:,ODD].sum(1)
    p=np.divide(e,w,out=np.zeros_like(e),where=w>0)
    H=float(np.dot(w,h2(p)))
    return H,w,e,p

def point(v,s):
    vals=np.exp(-(s+L*M)**2/(2*v))/math.sqrt(2*math.pi*v)
    return vals.sum(), vals[ODD].sum()

def cost(v,t): return bins(v,t)[0]
def grad(v,t):
    H,w,e,p=bins(v,t)
    ans=[]
    for j,x in enumerate(t):
        g,a=point(v,x); g*=2; a*=2
        pl=p[j];pr=p[j+1]
        ans.append(g*math.log2((1-pr)/(1-pl))+a*math.log2((1-pl)*pr/(pl*(1-pr))))
    return np.array(ans)

def one(v):
    hc,err=quad(lambda s:2*point(v,s)[0]*h2(point(v,s)[1]/point(v,s)[0]),0,HALF,epsabs=3e-14,epsrel=3e-14)
    records=[]
    rng=np.random.default_rng(20261102)
    for B in [2,3,4]:
        if B==2:
            sol=minimize_scalar(lambda t:cost(v,[t]),bounds=(1e-8,HALF-1e-8),method='bounded',options={'xatol':1e-14})
            t=np.array([sol.x]); opt=sol
        else:
            best=None
            starts=[np.linspace(0,HALF,B+1)[1:-1]]+[np.sort(rng.uniform(.02,HALF-.02,B-1)) for _ in range(64)]
            cons={'type':'ineq','fun':lambda t:np.diff(t)-1e-8,'jac':lambda t:np.diff(np.eye(len(t)),axis=0)}
            for start in starts:
                sol=minimize(lambda t:cost(v,t),start,jac=lambda t:grad(v,t),bounds=[(1e-8,HALF-1e-8)]*(B-1),constraints=cons,method='SLSQP',options={'ftol':1e-14,'maxiter':500})
                if best is None or sol.fun<best.fun:best=sol
            opt=best;t=opt.x
        H,w,e,p=bins(v,t)
        records.append(dict(B=B,thresholds=t.tolist(),thresholds_over_halfcell=(t/HALF).tolist(),w=w.tolist(),p=p.tolist(),entropy_per_quadrature=H,one_use_coherent_info=1-2*H,rate_loss_against_continuous=2*(H-hc),gradient=grad(v,t).tolist(),optimizer_success=bool(opt.success)))
    return dict(v=v,sigma=math.sqrt(v),halfcell=HALF,continuous_entropy_per_quadrature=hc,continuous_one_use_coherent_info=1-2*hc,quadrature_error_estimate=err,records=records)

if __name__=='__main__':
    output={'status':'diagnostic float64 quadrature and multistart optimization; not interval-certified or global optimization proof','results':[one(1/math.e),one(.37)]}
    print(json.dumps(output,indent=2))
