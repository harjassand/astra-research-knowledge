"""Conventional secant solvers versus certificate-driven halfspace learning.

All methods see the same fixed task sequence and the same imperfect source.
The hidden core and exact inverse in the fixture are used only for scoring.
Source work includes every final validation, failed validation and directed
probe. Individual methods reuse all per-generator results already paid for
by a mixed action; they do not receive uncharged source information.

Run with OPENBLAS_NUM_THREADS=1 python robust_solver/compare_conventional.py.
The root prototype is imported unchanged.
"""
from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import json
import sys
import time

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'robust_computation'))
from demand_solver import AcquiredSolver, Counters, hermitian
from check_demand_solver import fixture


class IndividualSecantSolver(AcquiredSolver):
    """Persistent per-generator models with one of three clipped updates.

    On a failed mixed validation every individually failing generator is
    eligible. Directed probes, if requested, inspect only the generator with
    the largest predicted halfspace gain and retain its best observation.
    Each eligible generator is then updated once using its retained pair.
    """

    def __init__(self, *args, update_kind='halfspace', **kwargs):
        super().__init__(*args, **kwargs)
        if update_kind not in ('halfspace', 'psb', 'bfgs'):
            raise ValueError('Unknown update rule.')
        self.update_kind = update_kind
        self.individual_updates = 0
        self.curvature_skips = 0

    def _single_observation(self, j, v, directed=False):
        y = np.asarray(self.action(j, v), dtype=complex).copy()
        self.count.source_actions += 1
        y -= 1j * np.imag(np.vdot(v, y)) * v
        theta = np.eye(self.k)[j]
        r = y - self.apply_model(theta, v)
        a = float(np.linalg.norm(r))
        d = float(np.real(np.vdot(v, r)))
        g2 = 0.5 * (a*a+d*d)
        h = a * max(a-self.eta, 0.0)
        if directed:
            self.count.directed_experiments += 1
        return dict(j=j, v=v, y=y, r=r, a=a, g2=g2, h=h,
                    gain=h*h/g2 if g2 else 0.0)

    def observe(self, theta, v, directed=False):
        if directed:
            raise ValueError('Individual directed observations require an index.')
        theta = np.asarray(theta)
        individual = {j:self._single_observation(j, v)
                      for j,coefficient in enumerate(theta) if coefficient}
        y = sum(theta[j]*obs['y'] for j,obs in individual.items())
        r = y - self.apply_model(theta, v)
        a = float(np.linalg.norm(r))
        d = float(np.real(np.vdot(v, r)))
        g2 = float(theta@theta) * 0.5 * (a*a+d*d)
        h = a * max(a-self.eta, 0.0)
        return dict(v=v, y=y, r=r, a=a, g2=g2, h=h,
                    gain=h*h/g2 if g2 else 0.0, individual=individual)

    def _update_one(self, observation):
        j, v, r = observation['j'], observation['v'], observation['r']
        before = self.audit(self) if self.audit else None
        self._extend_basis((v, r))
        vs, rs = self.q.conj().T@v, self.q.conj().T@r
        old = self.alpha[j]*np.eye(self.rank) + self.d[j]
        if self.update_kind == 'halfspace':
            correction = (observation['h']/observation['g2']) * hermitian(np.outer(rs,vs.conj()))
        elif self.update_kind == 'psb':
            scalar = float(np.real(np.vdot(vs,rs)))
            correction = (np.outer(rs,vs.conj()) + np.outer(vs,rs.conj())
                          - scalar*np.outer(vs,vs.conj()))
        else:
            bs = old@vs
            ys = self.q.conj().T@observation['y']
            vb = float(np.real(np.vdot(vs,bs)))
            vy = float(np.real(np.vdot(vs,ys)))
            if min(vb,vy) <= 0:
                self.curvature_skips += 1
                raise RuntimeError('Positive curvature failed despite the calibrated SPD source.')
            correction = -np.outer(bs,bs.conj())/vb + np.outer(ys,ys.conj())/vy
        trial = hermitian(old+correction)
        values,vectors = np.linalg.eigh(trial)
        bounded = np.clip(values,self.mu,self.upper)
        self.d[j] = hermitian((vectors*(bounded-self.alpha[j]))@vectors.conj().T)
        self.individual_updates += 1
        after = self.audit(self) if self.audit else None
        self.events.append(dict(individual_update=self.individual_updates,
                                generator=j, rank=self.rank,
                                residual_norm=observation['a'],
                                exact_source_gain=observation['gain'],
                                squared_clipping_distance=float(np.sum((values-bounded)**2)),
                                potential_before=before, potential_after=after))

    def solve(self, theta, b, max_updates=20000):
        theta = np.asarray(theta,dtype=float)
        if np.min(theta)<0 or abs(float(np.sum(theta))-1)>1e-10:
            raise ValueError('theta must be in the simplex.')
        b = np.asarray(b,dtype=complex)
        if not np.linalg.norm(b):
            return np.zeros_like(b),dict(checks=0,certificate=0.0)
        trials_before = self.count.trials
        while True:
            x = self.candidate(theta,b)
            length = float(np.linalg.norm(x))
            observation = self.observe(theta,x/length)
            self.count.trials += 1
            if observation['a'] <= self.threshold:
                self.count.accepted += 1
                certificate = (observation['a']+self.eta)/(self.mu-observation['a']-self.eta)
                return x,dict(checks=self.count.trials-trials_before,
                              observed_defect=observation['a'],certificate=certificate)
            self.count.failed_trials += 1
            selected = {j:obs for j,obs in observation['individual'].items()
                        if obs['a']>self.threshold}
            if not selected:
                raise RuntimeError('A failing convex mixture had no failing component.')
            current = max(selected.values(),key=lambda obs:obs['gain'])
            target = current['j']
            for _ in range(self.directed):
                if not current['a']:
                    break
                current = self._single_observation(target,current['r']/current['a'],directed=True)
                if (current['a']>self.threshold and
                        current['gain']>selected[target]['gain']):
                    selected[target] = current
            for obs in selected.values():
                self._update_one(obs)
            self.count.updates += 1
            if self.count.updates>max_updates:
                raise RuntimeError('Reached explicit experiment cap before certification.')


class FreshCheckedCG:
    """Fresh scalar-preconditioned CG with certified residual replacement.

    The oracle may be nonlinear, so the CG recurrence alone is not a
    certificate. An independent source action validates each returned vector.
    When a recursively small residual fails that validation, CG restarts from
    the freshly observed residual. No solution or Krylov directions persist
    across tasks. Every source action is counted.
    """

    def __init__(self,n,alpha,mu,upper,eta,threshold,action,**kwargs):
        self.n=n
        self.alpha=np.asarray(alpha)
        self.mu,self.upper,self.eta,self.threshold=mu,upper,eta,threshold
        self.action=action
        self.count=Counters()
        self.iterations=0
        self.restarts=0
        self.rank=0
        self.events=[]

    def _action(self,theta,v):
        length=float(np.linalg.norm(v))
        if not length:
            return np.zeros_like(v)
        unit=v/length
        y=np.zeros(self.n,dtype=complex)
        for j,coefficient in enumerate(theta):
            if coefficient:
                y+=coefficient*self.action(j,unit)
                self.count.source_actions+=1
        y-=1j*np.imag(np.vdot(unit,y))*unit
        return length*y

    def _check(self,theta,b,x):
        residual=b-self._action(theta,x)
        a=float(np.linalg.norm(residual)/np.linalg.norm(x))
        self.count.trials+=1
        if a<=self.threshold:
            self.count.accepted+=1
            return residual,dict(observed_defect=a,
                                 certificate=(a+self.eta)/(self.mu-a-self.eta))
        self.count.failed_trials+=1
        return residual,None

    def solve(self,theta,b,max_updates=20000):
        theta=np.asarray(theta,dtype=float)
        b=np.asarray(b,dtype=complex)
        if not np.linalg.norm(b):
            return np.zeros_like(b),dict(checks=0,certificate=0.0)
        trials_before=self.count.trials
        x=b/float(theta@self.alpha)
        r,certificate=self._check(theta,b,x)
        if certificate is not None:
            certificate['checks']=self.count.trials-trials_before
            return x,certificate
        p=r.copy()
        r2=float(np.real(np.vdot(r,r)))
        for iteration in range(max_updates):
            ap=self._action(theta,p)
            curvature=float(np.real(np.vdot(p,ap)))
            if curvature<=0:
                raise RuntimeError('CG lost positive curvature under the SPD oracle.')
            step=r2/curvature
            x=x+step*p
            r=r-step*ap
            self.iterations+=1
            new_r2=float(np.real(np.vdot(r,r)))
            # A strict inner target limits avoidable restarts while retaining
            # ordinary CG's cheap recursive residual between validations.
            if np.sqrt(new_r2)<=0.5*self.threshold*np.linalg.norm(x):
                r,certificate=self._check(theta,b,x)
                if certificate is not None:
                    certificate['checks']=self.count.trials-trials_before
                    return x,certificate
                self.restarts+=1
                p=r.copy()
                r2=float(np.real(np.vdot(r,r)))
            else:
                p=r+(new_r2/r2)*p
                r2=new_r2
        raise RuntimeError('Fresh CG reached its explicitly reported iteration cap.')


def run_one(label,solver_type,directed=0,update_kind=None):
    f=fixture()
    kwargs=dict(directed=directed,audit=f['audit'])
    if update_kind is not None:
        kwargs['update_kind']=update_kind
    model=solver_type(f['n'],f['alpha'],f['mu'],f['upper'],f['eta'],
                      f['threshold'],f['action'],**kwargs)
    records=[]
    start=time.perf_counter()
    for index,(theta,b) in enumerate(f['tasks']):
        x,cert=model.solve(theta,b)
        truth=f['exact_solution'](theta,b)
        rel=float(np.linalg.norm(x-truth)/np.linalg.norm(truth))
        assert rel<=cert['certificate']+1e-9,(label,index,rel,cert)
        records.append(dict(task=index,checks=cert['checks'],relative_error=rel,
                            certificate=cert['certificate']))
    elapsed=time.perf_counter()-start
    assert model.count.source_actions==f['calls']['count']
    audit_summary={}
    zeta=f['tail_size']
    if update_kind in ('halfspace','psb'):
        slacks=[]
        for event in model.events:
            a=event['residual_norm']
            if update_kind=='halfspace':
                guaranteed=(a-f['eta'])*(a-f['eta']-2*zeta)
            else:
                guaranteed=a*(a-4*(f['eta']+zeta))
            actual=event['potential_before']-event['potential_after']
            slacks.append(actual-guaranteed)
            assert actual+1e-8>=guaranteed,(label,event,guaranteed)
        audit_summary['minimum_proved_potential_slack']=min(slacks) if slacks else None
    if update_kind=='bfgs':
        decreases=[e['potential_before']-e['potential_after'] for e in model.events]
        audit_summary['minimum_empirical_frobenius_potential_decrease']=min(decreases) if decreases else None
        audit_summary['qualification']='No noisy BFGS lifetime guarantee is claimed.'
    return dict(method=label,directed_probes_per_failure=directed,tasks=len(records),
                retained_dimension=model.rank,counters=asdict(model.count),
                individual_updates=getattr(model,'individual_updates',None),
                cg_iterations=getattr(model,'iterations',None),
                cg_residual_restarts=getattr(model,'restarts',None),
                max_relative_solution_error=max(r['relative_error'] for r in records),
                max_reported_certificate=max(r['certificate'] for r in records),
                last_40_failed_validations=sum(r['checks']-1 for r in records[-40:]),
                measured_seconds_including_audits_and_scoring=elapsed,
                audit=audit_summary,records=records,events=model.events)


def main():
    specifications=[
        ('aggregate_halfspace',AcquiredSolver,0,None),
        ('aggregate_halfspace_directed2',AcquiredSolver,2,None),
        ('individual_halfspace',IndividualSecantSolver,0,'halfspace'),
        ('individual_halfspace_directed2',IndividualSecantSolver,2,'halfspace'),
        ('individual_psb',IndividualSecantSolver,0,'psb'),
        ('individual_psb_directed2',IndividualSecantSolver,2,'psb'),
        ('individual_bfgs',IndividualSecantSolver,0,'bfgs'),
        ('individual_bfgs_directed2',IndividualSecantSolver,2,'bfgs'),
        ('fresh_checked_cg',FreshCheckedCG,0,None),
    ]
    results=[]
    for args in specifications:
        result=run_one(*args)
        results.append(result)
        print(json.dumps({key:value for key,value in result.items()
                          if key not in ('records','events')},sort_keys=True),flush=True)
    output=dict(configuration=dict(dimension=192,generators=3,latent_rank_for_scoring_only=5,
                                  generic_diagonal_tail_bound=.002,oracle_error_bound=.003,
                                  validation_threshold=.060,task_count=120,task_seed=32171),
                qualification='Fixed identical tasks; every source action charged; truth and comparator only score results. Floating-point checks are not interval certification. Timings include unequal audit costs and are not speed claims.',
                results=results)
    Path(__file__).with_name('conventional_comparison_results.json').write_text(json.dumps(output,indent=2)+'\n')


if __name__=='__main__':
    main()
