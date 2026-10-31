"""Three noisy actions, then a safe halfspace update on the final observation."""
from pathlib import Path
import json
import numpy as np


def normop_hermitian(A):
    return float(np.max(np.abs(np.linalg.eigvalsh(A))))


def run():
    rng=np.random.default_rng(960641)
    records=[]
    n,beta,eta,zeta,mu,L=64,1.,.001,.001,.3,1.7
    delta=eta+zeta
    for lam in [-.5,-.04,.04,.5]:
        for project_observations in [False,True]:
            u=rng.normal(size=n)+1j*rng.normal(size=n);u/=np.linalg.norm(u)
            v=rng.normal(size=n)+1j*rng.normal(size=n)
            v-=u*np.vdot(u,v);v/=np.linalg.norm(v)
            overlap=.024/abs(lam)
            v=overlap*u+np.sqrt(1-overlap**2)*v
            Q,_=np.linalg.qr(rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)))
            eigs=zeta*rng.uniform(.5,1,size=n)*rng.choice([-1.,1.],size=n)
            tail=(Q*eigs)@Q.conj().T
            target=lam*np.outer(u,u.conj())
            A=beta*np.eye(n)+target+tail
            calls=0
            def observe(x):
                nonlocal calls
                calls+=1
                noise=rng.normal(size=n)+1j*rng.normal(size=n)
                noise+=3j*x
                noise*=eta/np.linalg.norm(noise)
                y=A@x+noise
                if project_observations:
                    y-=1j*np.vdot(x,y).imag*x
                assert np.linalg.norm(y-A@x)<=eta+1e-12
                return y
            residuals=[]
            directions=[]
            for _ in range(3):
                r=observe(v)-beta*v
                directions.append(v)
                residuals.append(r)
                v=r/np.linalg.norm(r)
            norms=[float(np.linalg.norm(r)) for r in residuals]
            assert norms[0]>=8*delta
            w,r=directions[-1],residuals[-1]
            a=norms[-1]
            G=(np.outer(r,w.conj())+np.outer(w,r.conj()))/2
            g2=np.linalg.norm(G,'fro')**2
            h=a*(a-eta)
            D=h/g2*G
            model=beta*np.eye(n)+D
            vals,V=np.linalg.eigh(model)
            clipped=(V*np.clip(vals,mu,L))@V.conj().T
            err=normop_hermitian(D-target)
            clipped_source_error=normop_hermitian(clipped-A)
            potential_before=np.linalg.norm(target,'fro')**2
            potential_after=np.linalg.norm(D-target,'fro')**2
            comparison_drop=(a-eta)*(a-eta-2*zeta)
            assert err<5*delta
            assert clipped_source_error<10*delta+zeta
            assert potential_before-potential_after>=comparison_drop-1e-10
            assert calls==3
            records.append({'lambda_for_scoring_only':lam,
                'projected_hermitian_observation':project_observations,
                'residual_norms':norms,
                'final_comparator_operator_error':err,
                'proved_preclip_comparator_bound':5*delta,
                'clipped_actual_source_operator_error':clipped_source_error,
                'proved_postclip_source_bound':10*delta+zeta,
                'potential_drop':float(potential_before-potential_after),
                'proved_comparator_drop':float(comparison_drop),
                'original_actions':calls})
    return {'status':'safe_amplification_checks_passed','complex_hermitian_sources':True,
            'ambient_dimension':n,'full_rank_generic_tail':True,
            'eta':eta,'zeta':zeta,'records':records,
            'qualification':'Mechanism checks; the general rank-r acceleration remains unproved.'}


if __name__=='__main__':
    result=run()
    Path(__file__).with_name('safe_amplification_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'cases':len(result['records']),
        'maximum_model_error':max(r['final_comparator_operator_error'] for r in result['records']),
        'proved_model_error_bound':5*(result['eta']+result['zeta']),
        'maximum_original_actions':max(r['original_actions'] for r in result['records'])},indent=2))
