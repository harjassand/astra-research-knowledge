"""Targeted finite checks for the strict population Lyapunov; not a proof."""
from pathlib import Path
import json
import math
import numpy as np
from check_researcher_c import generator, F_grad


def hessian(q, rho, u):
    rates=generator(q,u).copy();np.fill_diagonal(rates,0)
    w=rho[:,None]*rates
    return (np.diag(w.sum(0)+w.sum(1))-w-w.T)/4


def optimum(q,rho,basis):
    u=np.zeros(len(rho))
    for _ in range(100):
        f,g=F_grad(q,rho,u)
        gh=basis.T@g
        if np.linalg.norm(gh)<1e-9:
            return u
        step=basis@np.linalg.solve(basis.T@hessian(q,rho,u)@basis,gh)
        scale=1.
        while F_grad(q,rho,u-scale*step)[0]>f-.1*scale*np.dot(g,step):
            scale/=2
            assert scale>1e-12
        u-=scale*step
    raise AssertionError(f"Newton did not converge: projected gradient {np.linalg.norm(gh)}")


def main():
    rng=np.random.default_rng(202611052)
    worst_cross=0.;worst_violation=0.;cases=0
    for n in (2,3,4,6):
        for repeat in range(50):
            q=np.exp(rng.uniform(-1,1,(n,n)));np.fill_diagonal(q,0)
            if repeat%2:
                q[:]=0
                for i in range(n):q[i,(i+1)%n]=math.exp(rng.uniform(-1,1))
            rho=(rng.random(n)+.5);rho/=rho.sum()
            p=rng.dirichlet(np.ones(n));k=math.exp(rng.uniform(-1,1))
            raw=np.eye(n)[:,:n-1];raw[-1,:]=-rho[:-1]/rho[-1]
            basis=np.linalg.qr(raw)[0]
            ustar=optimum(q,rho,basis)
            u=rng.normal(size=n);u-=np.dot(rho,u)
            qmin=q[q>0].min();qmax=q.max();r0=rho.min()
            activity=(n-1)*qmax+k/2*math.log(1/r0)
            while F_grad(q,rho,u)[0]>activity:u/=2
            bound=2*(n-1)*math.log(activity/(r0*qmin))
            m=r0*qmin*math.exp(-bound/2)/(4*n*(n-1))
            upper=activity/2;normq=2*activity/r0;a=k*r0*m
            eps=min(m/2,k/4,a/(2*(k/r0+normq**2/(4*m))))
            x=p-rho;y=u-ustar;rates=generator(q,u);f,g=F_grad(q,rho,u)
            xp=p@rates;yp=k*x/rho
            direct=np.dot(xp,y)+np.dot(x,yp)
            identity=k*np.sum(x*x/rho)-2*np.dot(y,g)+np.dot(y,x@rates)
            worst_cross=max(worst_cross,abs(direct-identity))
            rr=p/rho
            diss=rr[:,None]*np.log(rr[:,None]/rr[None,:])-rr[:,None]+rr[None,:]
            off=rates.copy();np.fill_diagonal(off,0)
            edot=-k/2*np.sum(rho[:,None]*off*diss)
            wdot=edot+eps*direct
            target=-a/2*np.dot(x,x)-eps*m*np.dot(y,y)
            worst_violation=max(worst_violation,wdot-target)
            ent=np.dot(p,np.log(rr));fstar=F_grad(q,rho,ustar)[0]
            energy=f-fstar+k/2*ent;w=energy+eps*np.dot(x,y)
            low=min(m/4,k/8)*(np.dot(x,x)+np.dot(y,y))
            high=max((upper+eps)/2,k/(2*r0)+eps/2)*(np.dot(x,x)+np.dot(y,y))
            assert low-1e-10<=w<=high+1e-10
            assert np.linalg.eigvalsh(basis.T@hessian(q,rho,u)@basis).min()>=m-1e-10
            assert np.linalg.norm(rates,2)<=normq+1e-10
            assert wdot<=target+1e-10
            cases+=1
    result=dict(cases=cases,max_cross_derivative_residual=worst_cross,
                max_strict_dissipation_violation=worst_violation,
                scope="Finite algebra checks, not novelty, external validation, or hardware evidence.")
    Path(__file__).with_name("population_addendum_checks.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__":main()
