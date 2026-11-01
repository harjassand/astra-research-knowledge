#!/usr/bin/env python3
from compound_seed import *
from itertools import product,permutations
import copy

def increments(rec,x):
    for u,v,k in rec['channels']:
        rate=k*falling(x,u)
        if rate:yield u,v,rate,tuple(a-b+c for a,b,c in zip(x,u,v))

def local_checks(rec,cert,x):
    N=sum(x);a=x[rec['a']];r=inventory(rec,x);co=cert['constants'];q=co['q'];t=cert['t']
    if r==0:
        assert all(not falling(x,u) for u,v,k in rec['internal'])
        return 1
    f=F(a,(r+1)**2);g=profile(cert,r);d=g-profile(cert,r+1);dm=profile(cert,r-1)-g
    lintf=lintg=corecorr=F(0);edge_count=0
    for u,v,rate,xp in increments(rec,x):
        rp=inventory(rec,xp);ap=xp[rec['a']];fp=F(ap,(rp+1)**2)
        assert abs(fp-f)<=F(11,(r+1)**2)
        if sum(u)==sum(v):
            edge_count+=1;assert abs(rp-r)<=1;assert rp>=1
            lintf+=rate*(fp-f);lintg+=rate*(profile(cert,rp)-g)
        else:
            corecorr+=rate*q*(t**(sum(v)-sum(u))*fp/(sum(xp)+1)-f/(N+1))
    P=[x[h['edge'][0]]*x[h['edge'][1]] for h in rec['hubs']]
    bsum=sum(h['to_two_a']*p for h,p in zip(rec['hubs'],P))
    ssum=sum(h['reverse_sum']*p for h,p in zip(rec['hubs'],P))
    assert lintg<=co['Kf']*a*r*dm-bsum*d
    assert lintf<=-co['kminus']*a*F(N-2*r+a,(r+1)**2)+11*co['Kf']*F(r*r,(r+1)**2)+11*ssum/F((r+1)**2)
    assert corecorr<=q*(12*rec['lam']*t+12*rec['mu'])/(N+1)
    assert sum(P)>=F((r-a)**2,len(rec['components']))
    if N>=co['Nstar']:
        assert scaled_drift(rec,cert,x)<=-co['zeta']*hvalue(rec,cert,x)
    else:
        # Stronger sufficient finite-head check: the true bound has an extra t-power >=1.
        assert scaled_drift(rec,cert,x)+co['zeta']*hvalue(rec,cert,x)<=cert['Foster']['coefficient']
    return edge_count+5

def permute(raw,p):return [(tuple(u[i] for i in p),tuple(v[i] for i in p),k) for u,v,k in raw]

def leaves(o,path=()):
    if isinstance(o,dict):
        for k,v in o.items():yield from leaves(v,path+(k,))
    elif isinstance(o,(tuple,list)):
        for k,v in enumerate(o):yield from leaves(v,path+(k,))
    else:yield path,o

def alter(o,path,v):
    if not path:return v
    key=path[0]
    if isinstance(o,dict):out=dict(o);out[key]=alter(out[key],path[1:],v);return out
    out=list(o);out[key]=alter(out[key],path[1:],v);return tuple(out) if isinstance(o,tuple) else out

def run():
    cases=[('main',fixture(),F(2)),('shared_hubs',fixture((((2,3),(4,5)),),6),F(2)),
        ('two_components',fixture((((2,),(3,)),((4,),(5,))),6),F(2)),
        ('no_free_passenger',fixture((((1,),(2,)),),3,special=False),F(2)),
        ('near_one',fixture(),F(101,100)),('large_t',fixture(),F(5)),
        ('rate_ratio',fixture(port=(F(1,10),F(10))),F(3,2))]
    summaries=[];state_checks=local_assertions=outside_checks=0
    for name,raw,t in cases:
        rec=recognize(raw);cert=numerical(raw,t);assert cert['status']=='CERTIFIED_NUMERICAL'
        assert receive_qualitative(raw,qualitative(raw));assert receive_numerical(raw,t,cert)
        co=cert['constants'];K,J=co['K'],co['J']
        for r in list(range(1,J+2))+[10**6,10**30]:
            g=profile(cert,r);gp=profile(cert,r+1);d=g-gp
            assert rec['lam']*(t*gp-g)-co['beta']*r*r*d<=-co['epsilon']*g
            assert (r+1)**2*d>=co['dstar']
            if r>=J:
                dm=profile(cert,r-1)-g
                E=rec['mu']*(profile(cert,r-1)/t-g)+co['Kf']*r*dm+2*co['beta']*r*d
                assert E<=-co['D']/2
        limit=4 if rec['n']<=4 else 2
        for x in product(range(limit),repeat=rec['n']):
            local_assertions+=local_checks(rec,cert,x);state_checks+=1
        # Large pure, latent, active, balanced, and equality-crossing states.
        ns=[co['Nstar'],co['Nstar']+1,10**12,10**30]
        for size in ns:
            for j in range(rec['n']):
                for aa in [0,1,2,K,J,2*J]:
                    x=[0]*rec['n'];x[j]=size;x[rec['a']]+=aa
                    local_assertions+=local_checks(rec,cert,tuple(x));state_checks+=1;outside_checks+=1
            for level in [1,2,K,J,10**6]:
                x=[level]*rec['n'];x[rec['a']]=0;x[1 if rec['a']!=1 else 0]+=size
                local_assertions+=local_checks(rec,cert,tuple(x));state_checks+=1;outside_checks+=1
            x=tuple(size+i%2 for i in range(rec['n']))
            local_assertions+=local_checks(rec,cert,x);state_checks+=1;outside_checks+=1
        summaries.append(dict(name=name,n=rec['n'],hubs=len(rec['hubs']),components=len(rec['components']),
            t=t,K=K,J=J,Nstar=co['Nstar'],work=cert['work'],certificate_sha256=digest(cert)))
    raw=fixture();cert=numerical(raw,F(2));qc=qualitative(raw);tamper=0
    for obj,receiver in [(cert,lambda z:receive_numerical(raw,F(2),z)),(qc,lambda z:receive_qualitative(raw,z))]:
        for path,value in leaves(obj):
            changed=value+1 if type(value) in (int,F) else (not value if type(value) is bool else str(value)+'!')
            assert not receiver(alter(obj,path,changed));tamper+=1
    permutation_count=0
    for p in permutations(range(4)):
        rp=permute(raw,p);cp=numerical(rp,F(2));assert cp['constants']==cert['constants'];permutation_count+=1
    unknown=[]
    # An actual induced P4 of hub edges is unsupported, not declared unstable.
    pathraw=fixture((((1,),(2,)),((2,),(3,)),((3,),(4,))),5,special=False)
    oddraw=fixture((((1,),(2,)),((2,),(3,)),((3,),(1,))),4,special=False)
    for name,rr in [('missing_cross_edge',pathraw),('odd_cycle',oddraw)]:
        out=qualitative(rr);assert out['status']=='UNKNOWN';unknown.append((name,out['reason']))
    for name,rr,t,budget in [('zero_budget',raw,F(2),0),('extreme_death',fixture(port=(1,F(1,10**30))),F(2),100000),
                            ('huge_t',raw,F(10**50),100000)]:
        out=numerical(rr,t,budget);assert out['status']=='NUMERICAL_UNKNOWN';assert out['qualitative']['status']=='CERTIFIED_QUALITATIVE'
        assert out['work']['profile_recurrence_steps']==0;unknown.append((name,out['reason']))
    invalid=0
    for t,budget in [(1,100),(True,100),(2.0,100),(F(2),False),(F(2),-1)]:
        try:numerical(raw,t,budget)
        except (TypeError,ValueError):invalid+=1
        else:raise AssertionError('accepted invalid numerical domain')
    for badrate in [0,-1,True,1.5,'1']:
        rr=copy.deepcopy(raw);u,v,k=rr[0];rr[0]=(u,v,badrate)
        try:qualitative(rr)
        except (TypeError,ValueError):invalid+=1
        else:raise AssertionError('accepted invalid rate')
    return dict(status='PASS',cases=summaries,state_checks=state_checks,local_assertions=local_assertions,
        outside_Foster_checks=outside_checks,semantic_leaf_mutations_rejected=tamper,permutations=permutation_count,
        unknown_controls=unknown,invalid_domain_controls=invalid,
        no_simulation=True,no_head_enumeration=True,no_Foster_power_expansion=True)
if __name__=='__main__':print(canonical(run()))
