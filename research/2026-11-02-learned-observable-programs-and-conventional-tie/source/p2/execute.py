"""Generic interpreter for frozen probabilistic observable-rewrite programs.

No source-rate read, no model-type assumptions apart from compiled program
and 1D periodic index geometry. A schedule is a sequence of OPEN-LOOP mode maps.
The reverse order of the schedule is essential for backward observable evolution.
"""
import math, time
import numpy as np
from dataclasses import dataclass

@dataclass
class ExecutionCounter:
    paths:int=0
    events:int=0
    inspections:int=0
    terminal_evaluations:int=0
    total_active_scans:int=0
    branch_events:int=0
    transport_events:int=0
    killing_events:int=0
    max_particles:int=0
    elapsed_seconds:float=0.

def mean_spin(n,i):
    return 0.72 + .12*math.cos(2*math.pi*i/n)+.025*math.sin(6*math.pi*i/n)

def programs_growth(programs):
    # Each toggle causes at most max(0, |B|-2*1(center-in-B))
    # additional particles. A two-neighbour toggle can add two.
    # For masks with center included, it can remove center and add at most |B|-1 sites.
    result={}
    for mode,p in programs.items():
        incoming=0.
        for rule in p['jumps']:
            m=rule['toggle_mask'];has_center=bool(m&2)
            growth=(m.bit_count()-2*int(has_center))
            incoming+=max(0,growth)*rule['rate']
        result[mode]={"kill":p['kill'],"positive_growth_rate_bound":incoming,"contractivity_margin":p['kill']-incoming,
                      "exit_rate_per_particle":p['kill']+sum(q['rate'] for q in p['jumps'])}
    return result

def model_error_envelope(programs,horizon,query_size):
    growth=programs_growth(programs)
    kappa=min(p['contractivity_margin'] for p in growth.values())
    rho=max(p['local_residual_bound'] for p in programs.values())
    if kappa<=0:
        return {'valid':False,'reason':'no certified subcritical dual', 'kappa':kappa, 'rho':rho}
    err=rho*query_size*(-math.expm1(-kappa*horizon))/kappa
    events_per_path=query_size*max(v['exit_rate_per_particle'] for v in growth.values())*(-math.expm1(-kappa*horizon))/kappa
    return {"valid":True,"model_error_upper":err,"kappa":kappa,"rho":rho,
            "expected_native_event_upper_per_path":events_per_path,
            "growth":growth}

def mode_map(n,kind,query_site=None):
    """Heterogeneous intervention at previously untested spatial scales."""
    a=np.zeros(n,dtype=np.int8)
    if kind=='baseline':return a
    if kind=='contiguous':
        mid=(n//2 if query_site is None else query_site)
        span=max(2,n//3)
        for k in range(-span,span+1):a[(mid+k)%n]=1
        return a
    if kind=='striped':
        a[np.arange(n)%7<5]=1
        return a
    if kind=='alternating':
        a[np.arange(n)%2==0]=1
        return a
    raise ValueError(kind)

def make_schedule(n,policy,query_site=None):
    if policy=='baseline':
        return [(0.55,mode_map(n,'baseline')), (0.65,mode_map(n,'baseline'))]
    if policy=='intervene':
        return [(0.55,mode_map(n,'contiguous',query_site)), (0.65,mode_map(n,'striped'))]
    if policy=='reverse_intervene':
        return [(0.55,mode_map(n,'striped')), (0.65,mode_map(n,'contiguous',query_site))]
    raise ValueError(policy)

class LearnedInterpreter:
    def __init__(self,programs,mode_ids=('baseline','reduced_noise')):
        self.prog=[]
        for name in mode_ids:
            p=programs[name]
            rules=[(tuple(x['offsets']),float(x['rate'])) for x in p['jumps']]
            self.prog.append((float(p['kill']),rules))
        self.counter=ExecutionCounter()

    def one_path(self,rng,n,initial_m,query_indices,forward_schedule):
        active=set(query_indices)
        cemetery=False
        self.counter.paths+=1
        for duration,mode_map in reversed(forward_schedule):
            remaining=duration
            while active:
                nactive=len(active)
                self.counter.inspections+=1
                self.counter.max_particles=max(nactive,self.counter.max_particles)
                centers=[];total=0.
                for i in active:
                    k,rules=self.prog[int(mode_map[i])]
                    r=k+sum(v for _,v in rules)
                    centers.append((i,r))
                    total+=r
                self.counter.total_active_scans+=nactive
                assert total>=0
                if total==0:break
                dt=rng.exponential(1.0/total)
                if dt>=remaining:
                    self.counter.events+=0
                    break
                remaining-=dt
                u=rng.random()*total
                choice=centers[-1][0]
                for i,r in centers:
                    if u<r:
                        choice=i;break
                    u-=r
                self.counter.events+=1
                kill,rules=self.prog[int(mode_map[choice])]
                if u<kill:
                    cemetery=True
                    self.counter.killing_events+=1
                    break
                u-=kill
                for offsets,rate in rules:
                    if u<rate:
                        for o in offsets:
                            j=(choice+o)%n
                            if j in active:active.remove(j)
                            else:active.add(j)
                        if len(offsets)>=2 and (0 not in offsets):self.counter.branch_events+=1
                        else:self.counter.transport_events+=1
                        break
                    u-=rate
            if cemetery:break
        self.counter.terminal_evaluations+=1
        if cemetery:return 0.
        result=1.
        for i in active:
            result*=initial_m[i]
        return result

    def monte_carlo(self,n,query,forward_schedule,N,seed=2026,confidence_failure=0.002):
        rng=np.random.default_rng(seed)
        ini=np.array([mean_spin(n,i) for i in range(n)],dtype=float)
        before=ExecutionCounter(**vars(self.counter))
        t0=time.perf_counter()
        ret=0.;ret2=0.
        for _ in range(N):
            x=self.one_path(rng,n,ini,query,forward_schedule)
            ret+=x;ret2+=x*x
        elapsed=time.perf_counter()-t0
        self.counter.elapsed_seconds+=elapsed
        estimator=ret/N
        # Hoeffding for each sample in [-1,1]: P(|mean-E|>=eta)<=2 exp(-N eta^2/2).
        eta=math.sqrt(2*math.log(2/confidence_failure)/N)
        model=model_error_envelope({'baseline':self._p_to_json(0),'reduced_noise':self._p_to_json(1)},
                                   sum(v[0] for v in forward_schedule),len(query)) if False else None
        diff={a:vars(self.counter)[a]-vars(before)[a] for a in vars(before)}
        return {"n":n,"query":list(query),"N":N,"sample_mean":estimator,"empirical_sd":math.sqrt(max(0,ret2/N-estimator**2)),
                "statistical_halfwidth":eta,"confidence_failure":confidence_failure,
                "total_events":diff['events'],"total_scans":diff['total_active_scans'],
                "branch_events":diff['branch_events'],"kill_events":diff['killing_events'],
                "wall_seconds":elapsed,"max_particles":self.counter.max_particles}
