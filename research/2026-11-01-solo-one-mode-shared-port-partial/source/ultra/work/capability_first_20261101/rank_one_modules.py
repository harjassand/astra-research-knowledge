"""Acquire a global Foster function from a rank-one conservative raw module.

Exact rational rates, falling-factorial propensities, port species at index 0.
No equilibrium, stationary fiber, mixing law, or service oracle is input.
The constructor's arithmetic/enumeration costs are real; no bit-polynomial
complexity claim is made. The proof is RANK_ONE_MODULE_PROOF.md.
"""
from fractions import Fraction as F
from functools import reduce
from math import gcd, factorial, prod


def ceil(q):return -((-q.numerator)//q.denominator)


def fall(n,k):
    return prod(range(n-k+1,n+1)) if n>=k else 0


def rational(x):
    if isinstance(x,bool) or not isinstance(x,(int,str,F)):
        raise ValueError('Rates must be exact integers, rational strings or Fractions.')
    y=F(x)
    if y<=0:raise ValueError('Rates must be positive.')
    return y


def raw_module(reactions,x0):
    if not x0 or any(type(x) is not int or x<0 for x in x0):
        raise ValueError('Initial counts must be nonnegative integers.')
    n=len(x0);out=[]
    for source,target,rate in reactions:
        source,target=tuple(source),tuple(target)
        if len(source)!=n or len(target)!=n or any(type(x) is not int or x<0 for x in source+target):
            raise ValueError('Invalid complex.')
        rate=rational(rate)
        if source!=target:out.append((source,target,rate))
    vertices={z for y,z,k in out}|{y for y,z,k in out}
    adj={y:set() for y in vertices};undir={y:set() for y in vertices}
    for y,z,k in out:adj[y].add(z);undir[y].add(z);undir[z].add(y)
    def reached(start,graph):
        seen={start};todo=[start]
        while todo:
            for y in graph[todo.pop()]:
                if y not in seen:seen.add(y);todo.append(y)
        return seen
    left=set(vertices);components=[]
    while left:
        component=reached(min(left),undir);left-=component
        if any(reached(y,adj)!=component for y in component):
            raise ValueError('Internal module is not weakly reversible.')
        components.append(component)
    if not out:return out,[],None
    delta=tuple(z-y for y,z in zip(out[0][0],out[0][1]))
    gg=reduce(gcd,(abs(x) for x in delta));v=tuple(x//gg for x in delta)
    pivot=next(i for i,x in enumerate(v) if x)
    for y,z,k in out:
        diff=tuple(zz-yy for yy,zz in zip(y,z));multiple=F(diff[pivot],v[pivot])
        if multiple.denominator!=1 or any(dd!=multiple*vv for dd,vv in zip(diff,v)):
            raise ValueError('Internal stoichiometric rank exceeds one.')
    if not any(x>0 for x in v) or not any(x<0 for x in v):
        raise ValueError('Rank-one module is not conservative.')
    return out,components,v


def construct(reactions,x0,lam=1,mu=1,p_override=None,shift_override=None):
    x0=tuple(x0);lam,mu=rational(lam),rational(mu)
    reactions,components,v=raw_module(reactions,x0)
    result=dict(reactions=reactions,x0=x0,lam=lam,mu=mu)
    if v is None:
        return dict(result,kind='a_only',reason='No nonzero internal reaction.')
    pos=sum(x for x in v if x>0);neg=-sum(x for x in v if x<0)
    weight=tuple(neg if x>0 else pos if x<0 else 1 for x in v)
    assert sum(x*y for x,y in zip(weight,v))==0
    outside=v[1:]
    if any(x>0 for x in outside) and any(x<0 for x in outside):
        low=max(ceil(F(-x0[i],v[i])) for i in range(1,len(v)) if v[i]>0)
        high=min(x0[i]//(-v[i]) for i in range(1,len(v)) if v[i]<0)
        bounds=[max(x0[i]+v[i]*low,x0[i]+v[i]*high) for i in range(1,len(v))]
        t=F(2);d=mu*(1-t**(-weight[0]))
        acut=ceil((lam*(t**weight[0]-1)+1)/d)
        head=sum(w*b for w,b in zip(weight[1:],bounds))+weight[0]*acut+1
        return dict(result,kind='bounded_outside',v=v,weight=weight,
                    outside_low=low,outside_high=high,t=t,head=head,nu=F(1))
    if all(x<=0 for x in outside):v=tuple(-x for x in v)
    if not any(x>0 for x in v[1:]) or v[0]>=0:
        raise ValueError('Conservative orientation acquisition failed.')
    r=-v[0];ss=sum(v[1:]);moving=[i for i in range(1,len(v)) if v[i]>0]
    fixed=[i for i in range(1,len(v)) if v[i]==0]
    low=max(ceil(F(-x0[i],v[i])) for i in moving)
    offset=tuple(0 if i==0 else x0[i]+v[i]*low for i in range(len(v)))
    groups=[]
    for component in components:
        first=min(component)
        if any(x0[i]<first[i] for i in fixed):continue
        assert all(all(y[i]==first[i] for i in fixed) for y in component)
        ymin=min(component,key=lambda y:y[0]);m=ymin[0];bb=sum(ymin[i] for i in moving)
        selected=next(z for z in reactions if z[0]==ymin)
        jump=selected[1][0]-m
        assert jump>0 and bb>=ss
        catalyst=prod(fall(x0[i],ymin[i]) for i in fixed)
        members=[z for z in reactions if z[0] in component]
        bad=[z for z in members if z[1][0]<z[0][0]]
        groups.append(dict(ymin=ymin,m=m,b=bb,selected=selected,jump=jump,
                           catalyst=catalyst,members=members,bad=bad))
    if not groups:
        return dict(result,kind='a_only',reason='Every linkage is disabled by fixed catalysts.')
    pp=max(ceil(F(g['m'])+F(r*g['b'],ss)) for g in groups)
    if p_override is not None:
        if p_override<pp:raise ValueError('Insufficient profile exponent override.')
        pp=p_override
    jumpmax=max(abs(z[0]-y[0]) for y,z,k in reactions)
    shift=jumpmax+1
    if shift_override is not None:
        if shift_override<shift:raise ValueError('Insufficient profile shift override.')
        shift=shift_override
    big=F(pp*jumpmax)*F(shift,shift-jumpmax)**(pp+1)
    z0=2*max(y[i] for y,z,k in reactions for i in moving)+2
    for g in groups:
        dj=g['jump'];g['d']=F(pp*dj)*F(shift,shift+dj)**(pp+1);g['c']=g['d']/2
        selected_rate=g['selected'][2]
        ratios=[]
        for y,z,kappa in g['bad']:
            kk=F(y[0]-g['m'],r)
            assert kk.denominator==1 and kk>=1
            assert sum(y[i] for i in moving)==g['b']-ss*kk
            ratios.append(kappa/selected_rate*2**g['b']*prod((offset[i]+v[i])**y[i] for i in moving))
        g['ratio_sum']=sum(ratios,F(0))
    scale=max(2,*(1+ceil(2*big*g['ratio_sum']/g['d']) for g in groups))
    cost=big*mu
    for g in groups:
        small=F(0);lowcost=F(0)
        for y,z,kappa in g['bad']:
            bdegree=sum(y[i] for i in moving)
            upper=kappa*g['catalyst']*prod((offset[i]+v[i])**y[i] for i in moving)
            lowupper=kappa*g['catalyst']*prod((offset[i]+v[i]*z0)**y[i] for i in moving)
            small+=big*upper*scale**bdegree;lowcost+=big*lowupper
        ymin=g['ymin'];rate=g['selected'][2]
        upper=rate*g['catalyst']*prod((offset[i]+v[i])**ymin[i] for i in moving)
        small+=g['c']*upper*scale**g['b']
        cost+=small+lowcost
    m=min(g['m'] for g in groups)
    differences=[];old=F(0)
    for a in range(m):
        old=(1+mu*a*old)/lam;differences.append(old)
    heads=[sum(differences[a:],F(0)) for a in range(m)]+[F(0)]
    hmax=heads[0];gmax=F(1,shift**pp)
    ee=mu*gmax/(2*(cost+1))+2*lam*hmax
    eta=min(F(1,2),F(1,4)/(ee+1));t=1+eta
    death=mu*(1-1/t);epsilon=death/(2*(cost+1));delta=2*lam*eta
    assert 1+epsilon*gmax+delta*hmax<=F(3,2)
    acut=max(m+1,ceil(4*lam*eta/death),1)
    seed=mu*m*heads[m-1] if m else F(0)
    selected_group=next(g for g in groups if g['m']==m)
    sourcecoef=selected_group['selected'][2]*selected_group['catalyst']*F(factorial(m),2**selected_group['b'])
    denominator=(acut-1+shift)**(pp+1)
    target=delta*seed+2*lam*eta
    def enough(q):return epsilon*selected_group['c']*sourcecoef*(q+1)**selected_group['b']>=target*denominator
    qcut=max(1,z0)
    while not enough(qcut):qcut*=2
    assert enough(qcut)
    return dict(result,kind='rank_one_profile',v=v,r=r,s=ss,offset=offset,
                initial_q=-low,groups=groups,p=pp,shift=shift,B=big,Z0=z0,K=scale,C=cost,
                m=m,head_values=heads,seed_cost=seed,t=t,eta=eta,epsilon=epsilon,
                delta=delta,Acut=acut,Qcut=qcut,head=acut+r*qcut,
                nu=lam*eta/2,zeta=lam*eta/3)


def state(cert,a,q):
    return (a,)+tuple(cert['offset'][i]+cert['v'][i]*q for i in range(1,len(cert['v'])))


def h_value(cert,a):
    return 1+cert['epsilon']*F(1,(a+cert['shift'])**cert['p'])+cert['delta']*(cert['head_values'][a] if a<cert['m'] else 0)


def actual_drift(cert,a,q):
    x=state(cert,a,q);h=h_value(cert,a);t=cert['t']
    value=cert['lam']*(t*h_value(cert,a+1)-h)
    if a:value+=cert['mu']*a*(h_value(cert,a-1)/t-h)
    for y,z,kappa in cert['reactions']:
        rate=kappa*prod(fall(xx,yy) for xx,yy in zip(x,y))
        if rate:value+=rate*(h_value(cert,a+z[0]-y[0])-h)
    return value


def profile_bound(cert,a,q):
    x=state(cert,a,q);power=(a+cert['shift'])**(cert['p']+1);service=F(0)
    if q>=cert['Z0']:
        for g in cert['groups']:
            y,z,kappa=g['selected']
            service+=g['c']*kappa*prod(fall(xx,yy) for xx,yy in zip(x,y))/power
    gnow=F(1,(a+cert['shift'])**cert['p'])
    actual=cert['lam']*(F(1,(a+1+cert['shift'])**cert['p'])-gnow)
    if a:actual+=cert['mu']*a*(F(1,(a-1+cert['shift'])**cert['p'])-gnow)
    for y,z,kappa in cert['reactions']:
        rate=kappa*prod(fall(xx,yy) for xx,yy in zip(x,y))
        if rate:actual+=rate*(F(1,(a+z[0]-y[0]+cert['shift'])**cert['p'])-gnow)
    return actual,-service+cert['C']*a,service
