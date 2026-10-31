"""Mixed-spectrum, noncommuting, full-rank perturbed source experiment."""
from dataclasses import asdict
from pathlib import Path
import json
import time
import numpy as np
from demand_solver import AcquiredSolver, hermitian


def fixture(n=192, k=3, latent=5, seed=32171):
    rng=np.random.default_rng(seed)
    u=np.linalg.qr(rng.normal(size=(n,latent)))[0]
    cores=[]
    for j in range(k):
        rotation=np.linalg.qr(rng.normal(size=(latent,latent)))[0]
        values=np.linspace(0.15,1.1,latent)*(0.8+0.2*j)
        cores.append((rotation*values)@rotation.T)
    alpha=np.array([1.0,1.1,0.9])
    tail_size=0.002
    tails=np.array([rng.uniform(-1,1,n)*tail_size for _ in range(k)])
    eta=0.003
    mu,upper,threshold=0.85,2.6,0.060
    calls={'count':0}
    def true_action(j,v):
        return alpha[j]*v+u@(cores[j]@(u.T@v))+tails[j]*v
    def action(j,v):
        calls['count']+=1
        core=u@(cores[j]@(u.T@v))
        norm=float(np.linalg.norm(core))
        # Fixed, continuous masking of the learnable component. Error remains
        # bounded for every vector; it is neither iid nor a fixed linear matrix.
        error=-core*min(1.0,eta*float(np.linalg.norm(v))/max(norm,1e-300))
        return true_action(j,v)+error
    comparator_energy=float(sum(np.linalg.norm(c,'fro')**2 for c in cores))
    def audit(model):
        total=comparator_energy
        if model.rank:
            overlap=u.T@model.q
            for j in range(k):
                total+=float(np.linalg.norm(model.d[j],'fro')**2)
                total-=2*float(np.real(np.trace(model.d[j]@(overlap.T@cores[j]@overlap))))
        return total
    def exact_solution(theta,b):
        diagonal=float(theta@alpha)+theta@tails
        core=sum(t*c for t,c in zip(theta,cores))
        # Independent Woodbury truth calculation, not available to the learner.
        db=b/diagonal
        dinvu=u/diagonal[:,None]
        return db-dinvu@np.linalg.solve(np.linalg.inv(core)+u.T@dinvu,u.T@db)
    tasks=[]
    for t in range(120):
        theta=rng.dirichlet(np.ones(k))
        if t%3==0:
            b=rng.normal(size=n)
        else:
            b=u@rng.normal(size=latent)+0.15*rng.normal(size=n)
        tasks.append((theta,b))
    return locals()


def run(directed):
    f=fixture()
    learner=AcquiredSolver(f['n'],f['alpha'],f['mu'],f['upper'],f['eta'],f['threshold'],
                           f['action'],directed=directed,audit=f['audit'])
    records=[]
    start=time.perf_counter()
    for index,(theta,b) in enumerate(f['tasks']):
        # A subset of requests adapts to the currently acquired model.
        if index%7==0 and learner.rank:
            small=sum(t*d for t,d in zip(theta,learner.d))
            _,vec=np.linalg.eigh(hermitian(small))
            b=learner.q@vec[:,-1]+0.1*b
        x,certificate=learner.solve(theta,b)
        truth=f['exact_solution'](theta,b)
        rel=float(np.linalg.norm(x-truth)/np.linalg.norm(truth))
        residual=sum(t*f['true_action'](j,x) for j,t in enumerate(theta))-b
        relative_residual=float(np.linalg.norm(residual)/np.linalg.norm(b))
        assert rel<=certificate['certificate']+1e-9
        records.append({'task':index,'checks':certificate['checks'],'relative_error':rel,
                        'relative_residual':relative_residual,'certificate':certificate['certificate']})
    elapsed=time.perf_counter()-start
    zeta=f['tail_size']
    gap=(f['threshold']-f['eta'])*(f['threshold']-f['eta']-2*zeta)
    bound=f['comparator_energy']/gap
    minimum_slack=float('inf')
    for event in learner.events:
        a=event['residual_norm']
        guaranteed=(a-f['eta'])*(a-f['eta']-2*zeta)/event['coefficient_norm_squared']
        actual=event['potential_before']-event['potential_after']
        minimum_slack=min(minimum_slack,actual-guaranteed)
        assert actual+1e-8>=guaranteed
    assert learner.count.updates<=bound
    assert learner.count.source_actions==f['k']*(len(records)+(1+directed)*learner.count.updates)
    return {'directed_probes_per_failure':directed,'ambient_dimension':f['n'],
            'generator_count':f['k'],'latent_rank_for_scoring_only':f['latent'],
            'full_rank_tail_norm_bound':zeta,'noise_bound':f['eta'],
            'acceptance_threshold':f['threshold'],'spectral_interval':[f['mu'],f['upper']],
            'tasks':len(records),'retained_dimension':learner.rank,'counters':asdict(learner.count),
            'comparator_energy_for_scoring_only':f['comparator_energy'],
            'proved_failed_trial_bound':bound,'minimum_potential_slack':minimum_slack,
            'max_relative_solution_error':max(r['relative_error'] for r in records),
            'max_reported_certificate':max(r['certificate'] for r in records),
            'last_40_failed_trials':sum(r['checks']-1 for r in records[-40:]),
            'measured_seconds_excluding_truth_setup':elapsed,
            'records':records,'events':learner.events,
            'qualification':'Floating-point mechanism evidence, not interval certification or a speed claim.'}


if __name__=='__main__':
    results=[run(0),run(2)]
    Path(__file__).with_name('demand_solver_results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in r.items() if k not in ('records','events')} for r in results],indent=2))
