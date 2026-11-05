"""Finite algebra and exact-event numerical checks for researcher C.

These supplement the proofs; they do not establish uniform mixing, novelty,
physical feasibility, or general thermodynamic power claims.
"""
from pathlib import Path
import json
import math
import numpy as np


def generator(q, u):
    a = q * np.exp((u[:, None]-u[None, :])/2)
    np.fill_diagonal(a, 0)
    a -= np.diag(a.sum(axis=1))
    return a


def F_grad(q, rho, u):
    a = generator(q, u)
    value = -np.dot(rho, np.diag(a))
    gradient = -(rho @ a)/2
    return value, gradient


def algebra_checks(rng):
    worst_invariant = worst_lyapunov = 0.0
    for n in [2, 3, 4, 7]:
        for repeat in range(80):
            q = np.exp(rng.uniform(-2, 2, size=(n,n)))
            if repeat % 2:
                # Include a sparse directed cycle; no detailed balance.
                q[:] = 0
                for i in range(n):
                    q[i, (i+1) % n] = math.exp(rng.uniform(-2,2))
            np.fill_diagonal(q, 0)
            rho = rng.dirichlet(np.ones(n))
            p = rng.dirichlet(np.ones(n))
            u = rng.normal(size=n)
            u -= np.dot(rho, u)
            gain = math.exp(rng.uniform(-2,2))
            a = generator(q,u)
            value, grad = F_grad(q,rho,u)
            # Formal forward-equation residual after dividing by common density.
            for i in range(n):
                velocity = gain*(np.eye(n)[i]/rho[i]-1)
                residual = (rho@a)[i] + 2*rho[i]*np.dot(velocity,grad)/gain
                worst_invariant = max(worst_invariant, abs(residual))
            ratio = p/rho
            actual = np.dot(grad,gain*(ratio-1)) + gain/2*np.dot(p@a,np.log(ratio))
            phi = ratio[:,None]*np.log(ratio[:,None]/ratio[None,:])-ratio[:,None]+ratio[None,:]
            positive_rates = a.copy()
            np.fill_diagonal(positive_rates,0)
            expected = -gain/2*np.sum(rho[:,None]*positive_rates*phi)
            scale = 1+abs(actual)+abs(expected)
            worst_lyapunov = max(worst_lyapunov,abs(actual-expected)/scale)
            assert actual < 1e-9*(1+abs(expected))
    assert worst_invariant < 1e-10
    assert worst_lyapunov < 1e-12
    return dict(cases=320,max_forward_residual=worst_invariant,
                max_relative_lyapunov_residual=worst_lyapunov)


def grid_integrals(q,rho,gain):
    # Coordinates (u0,u1) on rho.u=0; area factor cancels in expectations.
    axis = np.linspace(-10,10,801)
    xx,yy = np.meshgrid(axis,axis,indexing="ij")
    u=np.stack([xx,yy,-(rho[0]*xx+rho[1]*yy)/rho[2]],axis=-1)
    a=q*np.exp((u[..., :,None]-u[...,None,:])/2)
    value=np.sum(rho[None,None,:,None]*a,axis=(-2,-1))
    gradient=-(np.sum(rho[None,None,:,None]*a,axis=-2)
               -rho[None,None,:]*np.sum(a,axis=-1))/2
    density=np.exp(-2*(value-value.min())/gain)
    weight=np.ones(len(axis));weight[[0,-1]]=0.5
    density*=weight[:,None]*weight[None,:]
    density/=density.sum()
    def mean(z):
        return np.sum(density*z)
    mean_u=np.sum(density[...,None]*u,axis=(0,1))
    var_u=np.sum(density[...,None]*(u-mean_u)**2,axis=(0,1))
    mean_f=mean(value)
    equip=mean(np.sum(u*gradient,axis=-1))
    f0=float(np.sum(rho[:,None]*q))
    kl=f0-mean_f+gain*(len(rho)-1)/2
    # Compute the same KL integrand directly.
    log_ratio=(u[..., :,None]-u[...,None,:])/2
    direct=np.sum(rho[None,None,:,None]*(a*log_ratio-a+q),axis=(-2,-1))
    assert abs(equip-gain) < 1e-8
    assert abs(mean(direct)-kl) < 1e-8
    return dict(mean_u=mean_u.tolist(),var_u=var_u.tolist(),
                mean_F=float(mean_f),equipartition=float(equip),
                expected_equipartition=gain,
                path_KL_rate=float(kl),
                direct_path_KL_rate=float(mean(direct)),
                stationary_occupation_variance_constant_upper=
                    (4*rho**2*var_u/gain**2).tolist())


def exact_events(q,rho,gain,rng,time_limit=30000.0):
    u=np.zeros(len(rho)); start_u=u.copy()
    state=0;time=0.;events=0;occupation=np.zeros(len(rho))
    total_log_likelihood=0.; integral_f=0.
    while time < time_limit:
        a=q[state]*np.exp((u[state]-u)/2)
        total=a.sum()
        b=gain/(2*rho[state])
        wait=math.log1p(b*rng.exponential()/total)/b
        remaining=time_limit-time
        dt=min(wait,remaining)
        velocity=gain*(np.eye(len(rho))[state]/rho[state]-1)
        # Exact integrated hazard on this holding interval.
        total_log_likelihood-=total*math.expm1(b*dt)/b-q[state].sum()*dt
        occupation[state]+=dt
        u+=velocity*dt
        time+=dt
        if wait>remaining:
            break
        destination=rng.choice(len(rho),p=a/total)
        total_log_likelihood+=(u[state]-u[destination])/2
        state=destination; events+=1
    identity=(rho/gain)*(u-start_u)
    assert np.max(np.abs((occupation-time*rho)-identity))<1e-7
    return dict(time=time,events=events,occupation=(occupation/time).tolist(),
                target=rho.tolist(),final_controller=u.tolist(),
                discrepancy_identity_error=float(np.max(np.abs(occupation-time*rho-identity))),
                empirical_path_KL_rate=total_log_likelihood/time,
                warning="One trajectory from zero controller; no certified burn-in or confidence statement.")


def main():
    rng=np.random.default_rng(20261105)
    q=np.array([[0.,4.,.3],[.2,0.,2.],[1.,.1,0.]])
    rho=np.array([.2,.3,.5]);gain=.7
    result=dict(algebra=algebra_checks(rng),grid=grid_integrals(q,rho,gain),
                exact_event_simulation=exact_events(q,rho,gain,rng),
                scope="Finite/numerical consistency checks; proofs and limits are in researcher_c.txt.")
    target=Path(__file__).with_name("researcher_c_checks.json")
    target.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
