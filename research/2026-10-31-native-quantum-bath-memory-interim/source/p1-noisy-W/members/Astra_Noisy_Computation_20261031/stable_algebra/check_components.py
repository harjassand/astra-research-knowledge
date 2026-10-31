"""Numerical checks of noisy secant-ball projection and residual amplification.

These checks support the ordinary proofs; they are not interval-arithmetic
certificates and do not establish historical novelty or optimized performance.
"""
from pathlib import Path
import json
import numpy as np
from scipy.optimize import minimize


def secant_ball_update(B,u,y,omega):
    e=y-B@u
    t=np.linalg.norm(e)
    if t<=omega: return B.copy()
    a=u@e
    b=e-a*u
    b2=b@b
    if omega==0:
        v=e
    else:
        def f(lam): return a*a/(1+lam)**2+4*b2/(2+lam)**2
        lo,hi=0.0,1.0
        while f(hi)>omega**2: hi*=2
        for _ in range(100):
            mid=(lo+hi)/2
            if f(mid)>omega**2: lo=mid
            else: hi=mid
        lam=hi
        v=(lam/(1+lam)*a)*u+(lam/(2+lam))*b
    return B+np.outer(v,u)+np.outer(u,v)-(u@v)*np.outer(u,u)


def clip(B,mu,L):
    d,Q=np.linalg.eigh(B)
    return (Q*np.clip(d,mu,L))@Q.T


def projection_checks():
    rng=np.random.default_rng(71813)
    n,mu,L=7,.25,2.0
    min_fejer_slack=float('inf')
    max_constraint=0.0
    max_rank=0
    max_scalar_optimizer_gap=0.0
    for _ in range(120):
        X=rng.normal(size=(n,n)); C=clip((X+X.T)/2,mu,L)
        X=rng.normal(size=(n,n)); B=clip((X+X.T)/2,mu,L)
        u=rng.normal(size=n);u/=np.linalg.norm(u)
        eta=.01+.09*rng.random()
        e=rng.normal(size=n);e*=eta*rng.random()/np.linalg.norm(e)
        y=C@u+e
        omega=eta
        Bp=secant_ball_update(B,u,y,omega)
        D=Bp-B
        v=D@u
        t=np.linalg.norm(y-B@u)
        assert np.linalg.norm(Bp@u-y)<=omega+1e-11
        assert np.linalg.norm(D,'fro')+1e-11>=max(0,t-omega)
        assert np.allclose(Bp,Bp.T)
        fejer=np.linalg.norm(B-C,'fro')**2-np.linalg.norm(Bp-C,'fro')**2-np.linalg.norm(D,'fro')**2
        assert fejer>=-1e-10
        Bc=clip(Bp,mu,L)
        assert np.linalg.norm(Bc-C,'fro')**2<=np.linalg.norm(Bp-C,'fro')**2+1e-10
        min_fejer_slack=min(min_fejer_slack,fejer)
        max_constraint=max(max_constraint,np.linalg.norm(Bp@u-y)-omega)
        max_rank=max(max_rank,int(np.count_nonzero(np.linalg.svd(D,compute_uv=False)>1e-10)))

        # Independently solve the two-coordinate convex problem.
        err=y-B@u; a=u@err; b=err-a*u; bn=np.linalg.norm(b)
        objective=lambda z:z[0]**2+2*z[1]**2
        constraint=lambda z:omega**2-(a-z[0])**2-(bn-z[1])**2
        opt=minimize(objective,[a,bn],constraints={'type':'ineq','fun':constraint},
                     method='SLSQP',options={'ftol':1e-12,'maxiter':1000})
        assert opt.success or abs(constraint(opt.x))<1e-9
        gap=abs(np.linalg.norm(D,'fro')**2-opt.fun)
        assert gap<1e-7
        max_scalar_optimizer_gap=max(max_scalar_optimizer_gap,gap)
    return {'cases':120,'maximum_update_rank':max_rank,
            'minimum_fejer_slack':min_fejer_slack,
            'maximum_observation_ball_constraint_excess':max_constraint,
            'maximum_gap_against_independent_scalar_optimizer':max_scalar_optimizer_gap}


def amplification_checks():
    rng=np.random.default_rng(61921)
    n,a,eta,zeta=96,1.0,.001,.001
    records=[]
    for lam in [-.6,-.2,-.032,.032,.2,.6]:
        for mode in ['random_errors','adversarial_denominator']:
            u=rng.normal(size=n);u/=np.linalg.norm(u)
            h=rng.normal(size=n);h-=u*(u@h);h/=np.linalg.norm(h)
            overlap=min(.8,.024/abs(lam))
            v=overlap*u+np.sqrt(1-overlap**2)*h
            Q,_=np.linalg.qr(rng.normal(size=(n,n)))
            eigs=zeta*rng.uniform(.5,1,size=n)*rng.choice([-1.,1.],size=n)
            tail=(Q*eigs)@Q.T
            A=a*np.eye(n)+lam*np.outer(u,u)+tail
            calls=0
            def oracle(x):
                nonlocal calls
                calls+=1
                if mode=='adversarial_denominator' and calls==2:
                    e=-np.sign(lam)*eta*x
                else:
                    e=rng.normal(size=n);e*=eta*np.linalg.norm(x)/np.linalg.norm(e)
                return A@x+e
            r=oracle(v)-a*v
            t=np.linalg.norm(r)
            assert t>=8*(eta+zeta)
            w=r/t
            z=oracle(w)-a*w
            denom=w@z
            B=np.outer(z,z)/denom
            model=a*np.eye(n)+B
            comparator_error=np.max(np.abs(np.linalg.eigvalsh(B-lam*np.outer(u,u))))
            source_error=np.max(np.abs(np.linalg.eigvalsh(model-A)))
            model_min=np.linalg.eigvalsh(model)[0]
            preconditioner_error=np.linalg.norm(np.eye(n)-A@np.linalg.inv(model),2)
            assert comparator_error<4*(eta+zeta)
            assert source_error<4*eta+5*zeta
            assert model_min>0
            assert preconditioner_error<=(4*eta+5*zeta)/model_min+1e-12
            assert calls==2
            records.append({'lambda_for_scoring_only':lam,'noise_mode':mode,
                            'initial_observed_residual':float(t),
                            'new_probe_overlap_for_scoring_only':float(abs(u@w)),
                            'comparator_operator_error':float(comparator_error),
                            'actual_source_operator_error':float(source_error),
                            'proved_source_error_bound':4*eta+5*zeta,
                            'preconditioner_operator_error':float(preconditioner_error),
                            'original_source_actions':calls})
    return {'ambient_dimension':n,'cases':len(records),'full_rank_tail':True,
            'eta':eta,'zeta':zeta,'records':records}


if __name__=='__main__':
    result={'status':'component_checks_passed','secant_ball':projection_checks(),
            'residual_amplification':amplification_checks(),
            'qualification':'Mechanism checks, not formal numerical certificates or novelty evidence.'}
    Path(__file__).with_name('component_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'secant_ball':result['secant_ball'],
        'amplification_cases':result['residual_amplification']['cases'],
        'maximum_source_error':max(r['actual_source_operator_error'] for r in result['residual_amplification']['records'])},indent=2))
