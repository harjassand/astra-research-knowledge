"""Execution and certified resource bounds for acquired signed observable rules.
A negative rule multiplies the trajectory's sign by -1; no unaccounted
absolute weights are permitted, and the learned cemetery intensity must be >=0.
"""
import math,time
import numpy as np
from dataclasses import dataclass
from execute import mean_spin

MODE_IDS=('baseline','reduced_noise','weak_field')

def common_programs(v1,v2):
    data={}
    for k,p in v1['programs'].items():
        data[k]={'kill':p['kill'],'rho':p['local_residual_bound'],
                 'jumps':[{'offsets':q['offsets'],'rate':q['rate'],'sign':1} for q in p['jumps']]}
    new=v2['new_mode']
    data['weak_field']={'kill':new['kill'],'rho':new['local_residual_bound'],
                        'jumps':new['rules']}
    return data

def growth_and_error(prog,T,k):
    growth={}
    for name,p in prog.items():
        enter=0.
        for q in p['jumps']:
            B=q['offsets'];enter+=q['rate']*max(0,len(B)-2*int(0 in B))
        margin=p['kill']-enter
        total=p['kill']+sum(v['rate'] for v in p['jumps'])
        growth[name]={'positive_count_drift':enter,'killing_rate':p['kill'],
                      'margin':margin,'event_rate_per_particle':total,
                      'number_signed_rules':sum(q['sign']<0 for q in p['jumps'])}
    kappa=min(x['margin'] for x in growth.values())
    rho=max(x['rho'] for x in prog.values())
    if kappa<=0:return {'valid':False,'kappa':kappa}
    factor=-math.expm1(-kappa*T)/kappa
    return {'valid':True,'kappa':kappa,'rho':rho,
            'model_error':k*rho*factor,'max_expected_events_per_path':k*max(g['event_rate_per_particle'] for g in growth.values())*factor,
            'growth':growth}

def policy_map(n,policy,site):
    m=np.zeros(n,dtype=np.int8)
    if policy=='baseline':return m
    if policy=='field_patch':
        width=max(3,n//4)
        for k in range(-width,width+1):m[(site+k)%n]=2
        return m
    if policy=='field_stripes':
        m[np.arange(n)%11 < 8]=2
        return m
    if policy=='mixed':
        m[np.arange(n)%7 < 5]=1
        patch=max(2,n//3)
        for k in range(-patch,patch+1):m[(site+k)%n]=2
        return m
    raise ValueError(policy)

def intervention_schedule(n,policy,site):
    if policy=='baseline':return [(0.5,policy_map(n,'baseline',site)),(.7,policy_map(n,'baseline',site))]
    if policy=='field':return [(0.5,policy_map(n,'field_patch',site)),(.7,policy_map(n,'field_stripes',site))]
    if policy=='field_reversed':return [(0.5,policy_map(n,'field_stripes',site)),(.7,policy_map(n,'field_patch',site))]
    if policy=='mixed':return [(0.5,policy_map(n,'mixed',site)),(.7,policy_map(n,'field_stripes',site))]
    raise ValueError(policy)

class SignedInterpreter:
    def __init__(self,programs):
        self.programs=programs
        self.modes=[]
        for m in MODE_IDS:
            d=programs[m]
            v=[(tuple(q['offsets']),q['rate'],q['sign']) for q in d['jumps']]
            self.modes.append((d['kill'],v,d['kill']+sum(z[1] for z in v)))

    def estimate(self,n,query,schedule,N,seed=123,delta=.0005):
        rng=np.random.default_rng(seed)
        ini=np.array([mean_spin(n,i) for i in range(n)])
        count={'events':0,'site_scans':0,'negative_transitions':0,'branches':0,'killed':0,
               'max_active':0,'trajectories':N,'sign_negative_at_end':0}
        tot=0.;tot2=0.
        start=time.perf_counter()
        for run in range(N):
            active=set(query);sign=1;dead=False
            for duration,sites in reversed(schedule):
                remaining=duration
                while active:
                    ks=len(active);count['max_active']=max(count['max_active'],ks)
                    per=[];total=0.
                    for i in active:
                        r=self.modes[int(sites[i])][2]
                        per.append((i,r));total+=r
                    count['site_scans']+=ks
                    if total<=0:break
                    dt=rng.exponential(1/total)
                    if dt>=remaining:break
                    remaining-=dt
                    u=rng.random()*total
                    selected=per[-1][0]
                    for i,r in per:
                        if u<r:selected=i;break
                        u-=r
                    kill,rs,_=self.modes[int(sites[selected])]
                    count['events']+=1
                    if u<kill:
                        dead=True;count['killed']+=1;break
                    u-=kill
                    for offsets,q,sig in rs:
                        if u<q:
                            if sig<0:sign=-sign;count['negative_transitions']+=1
                            if 0 not in offsets and len(offsets)==2:count['branches']+=1
                            for offset in offsets:
                                j=(selected+offset)%n
                                if j in active:active.remove(j)
                                else:active.add(j)
                            break
                        u-=q
                if dead:break
            if dead:val=0.
            else:
                val=sign
                for i in active:val*=ini[i]
                if sign<0:count['sign_negative_at_end']+=1
            tot+=val;tot2+=val*val
        elapsed=time.perf_counter()-start
        mean=tot/N
        eps=math.sqrt(2*math.log(2/delta)/N) # [-1,1] bound, not positive-only
        return {'n':n,'query':query,'N':N,'estimator':mean,'empirical_sd':math.sqrt(max(0.,tot2/N-mean**2)),
                'MC_halfwidth':eps,'delta':delta,'counters':count,'wall_seconds':elapsed}
