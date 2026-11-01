#!/usr/bin/env python3
"""Trusted exact research constructor, not a hostile-input validator.
Qualitative recognition is finite and separate from numerical profile acquisition.
The optional budget counts profile/backward and head-scan iterations ONLY.
"""
from fractions import Fraction as F
import hashlib,json,sys
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
FAMILY='biclique-compound-seed-active-phase-v1'
class Unsupported(ValueError):pass

def rat(x):
    if type(x) not in (int,F):raise TypeError('exact int/Fraction required')
    return F(x)
def ceilq(x):return -(-x.numerator//x.denominator)
def encode(x):
    if type(x) is F:return str(x)
    if isinstance(x,dict):return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [encode(v) for v in x]
    return x
def canonical(x):return json.dumps(encode(x),sort_keys=True,separators=(',',':'))
def digest(x):return hashlib.sha256(canonical(x).encode()).hexdigest()
def bits(x):
    if type(x) is F:return max(abs(x.numerator).bit_length(),x.denominator.bit_length())
    if type(x) is int:return abs(x).bit_length()
    if isinstance(x,dict):return max([0]+[bits(v) for v in x.values()])
    if isinstance(x,(list,tuple)):return max([0]+[bits(v) for v in x])
    return 0

def recognize(raw):
    if type(raw) not in (list,tuple) or not raw:raise ValueError('nonempty raw list')
    n=None;rates={};coordinate_checks=0
    for row in raw:
        if type(row) not in (list,tuple) or len(row)!=3:raise ValueError('reaction triple')
        u,v,k=row
        if type(u) not in (list,tuple) or type(v) not in (list,tuple):raise TypeError('complex vectors')
        if n is None:n=len(u)
        if n<3 or len(u)!=n or len(v)!=n:raise ValueError('fixed dimension n>=3')
        for z in tuple(u)+tuple(v):
            coordinate_checks+=1
            if type(z) is not int or z<0:raise ValueError('nonnegative exact integer counts')
        k=rat(k)
        if k<=0:raise ValueError('strictly positive rate')
        u,v=tuple(u),tuple(v)
        if u!=v:rates[u,v]=rates.get((u,v),F(0))+k
    channels=tuple((u,v,k) for (u,v),k in sorted(rates.items()))
    zero=(0,)*n;noncon=[(u,v,k) for u,v,k in channels if sum(u)!=sum(v)];roles=[]
    for a in range(n):
        e=tuple(int(i==a) for i in range(n))
        if len(noncon)==2 and {(u,v) for u,v,k in noncon}=={(zero,e),(e,zero)}:roles.append(a)
    if len(roles)!=1:raise Unsupported('requires one exact reversible port')
    a=roles[0];e=tuple(int(i==a) for i in range(n));aa=tuple(2*int(i==a) for i in range(n))
    internal=tuple(row for row in channels if sum(row[0])==sum(row[1]));hubs={};active={};complex_checks=0
    for u,v,k in internal:
        for z in (u,v):
            complex_checks+=1
            if sum(z)!=2:raise Unsupported('only binary nonnull internals')
            if z[a]==0:
                inds=[i for i,q in enumerate(z) if q]
                if len(inds)!=2 or any(z[i]!=1 for i in inds):raise Unsupported('hub must be square-free satellite pair')
                hubs[z]=tuple(inds)
            elif z==aa:active[z]=None
            elif z[a]==1:
                inds=[i for i,q in enumerate(z) if q and i!=a]
                if len(inds)!=1 or z[inds[0]]!=1:raise Unsupported('active complex must be A+X')
                active[z]=inds[0]
            else:raise Unsupported('unrecognized active complex')
    if not hubs:raise Unsupported('at least one hub required')
    reverse_tests=0
    for u,v,k in internal:
        if (u in hubs)==(v in hubs):raise Unsupported('only hub/active edges')
        reverse_tests+=1
        if (v,u) not in rates:raise Unsupported('every included edge must be reversible')
    graph={i:set() for edge in hubs.values() for i in edge}
    for i,j in hubs.values():graph[i].add(j);graph[j].add(i)
    color={};components=[];edge_visits=0;cross_tests=0
    for seed in sorted(graph):
        if seed in color:continue
        color[seed]=0;todo=[seed];comp=[]
        while todo:
            i=todo.pop();comp.append(i)
            for j in sorted(graph[i]):
                edge_visits+=1
                if j not in color:color[j]=1-color[i];todo.append(j)
                elif color[j]==color[i]:raise Unsupported('hub graph has an odd cycle')
        left=tuple(sorted(i for i in comp if color[i]==0));right=tuple(sorted(i for i in comp if color[i]==1))
        for i in left:
            for j in right:
                cross_tests+=1
                if j not in graph[i]:raise Unsupported('hub component is not complete bipartite')
        components.append((left,right))
    kX={i:F(0) for i in range(n) if i!=a};hubrows=[];amp_tests=0;incidence_tests=0
    for h,ij in sorted(hubs.items()):
        amp_tests+=2
        if (aa,h) not in rates or (h,aa) not in rates:raise Unsupported('every hub needs 2A amplification pair')
        arms=[]
        for x in sorted(kX):
            ax=tuple(int(i==a)+int(i==x) for i in range(n));incidence_tests+=1
            if (ax,h) in rates:
                kX[x]+=rates[ax,h];arms.append((x,rates[ax,h],rates[h,ax]))
        hubrows.append(dict(complex=h,edge=ij,to_hub=rates[aa,h],to_two_a=rates[h,aa],
                            reverse_sum=rates[h,aa]+sum((v for x,u,v in arms),F(0)),arms=tuple(arms)))
    if min(kX.values())<=0:raise Unsupported('each satellite needs a forward/reverse arm')
    as_=sum((h['to_hub'] for h in hubrows),F(0));bmin=min(h['to_two_a'] for h in hubrows)
    rec=dict(n=n,a=a,lam=rates[zero,e],mu=rates[e,zero],channels=channels,internal=internal,
        components=tuple(components),free=tuple(i for i in kX if i not in graph),hubs=tuple(hubrows),
        kX=tuple(sorted(kX.items())),kminus=min(kX.values()),kplus=max(kX.values()),a_sum=as_,
        Kf=as_+2*max(kX.values()),beta=bmin/F(2*len(components)),
        sratio=max(h['reverse_sum']/h['to_two_a'] for h in hubrows),S=sum((k for u,v,k in internal),F(0)),
        raw_sha256=digest(channels),work=dict(input_rows=len(raw),normalized_channels=len(channels),
        raw_coordinate_checks=coordinate_checks,internal_complex_checks=complex_checks,
        reverse_edge_tests=reverse_tests,hub_graph_edge_visits=edge_visits,biclique_cross_tests=cross_tests,
        amplification_edge_tests=amp_tests,arm_incidence_tests=incidence_tests))
    return rec

def _qual(rec):
    return dict(status='CERTIFIED_QUALITATIVE',family=FAMILY,raw_sha256=rec['raw_sha256'],
        conclusion='irreducible positive recurrence; every finite exponential stationary total-count moment',
        role=dict(dimension=rec['n'],open_coordinate=rec['a'],immigration=rec['lam'],death=rec['mu']),
        inventory=dict(bicliques=rec['components'],free_satellites=rec['free']),
        hubs=rec['hubs'],work=dict(**rec['work'],profile_recurrence_steps=0,finite_head_checks=0,
             stationary_fiber_laws=0,states_enumerated=0,expanded_Foster_powers=0))
def qualitative(raw):
    try:return _qual(recognize(raw))
    except Unsupported as exc:return dict(status='UNKNOWN',family=FAMILY,reason=str(exc),stability='UNKNOWN')

def _numerical(rec,t,budget):
    t=rat(t)
    if t<=1:raise ValueError('t>1 required')
    if type(budget) is not int or budget<0:raise ValueError('nonnegative exact iteration budget')
    lam,mu,beta,Kf=rec['lam'],rec['mu'],rec['beta'],rec['Kf'];L=lam*(t-1)
    eps=min(F(1),(lam+beta)/2);c=4*(L+eps)/beta;K=max(2,ceilq(2*c));D=mu*(1-1/t)
    J=max(K+1,2,ceilq(4*c*(mu+Kf+beta)/D));needed=K-1+J-1
    base=dict(family=FAMILY,raw_sha256=rec['raw_sha256'],t=t,qualitative=_qual(rec),
        budget=dict(profile_head_iteration_limit=budget,required_iterations=needed,
        scope='only backward recurrence and finite head scan iterations; not bits/input/total arithmetic/time'))
    if needed>budget:
        return dict(status='NUMERICAL_UNKNOWN',reason='profile/head iteration budget exceeded',
                    preflight=dict(K=K,J=J),work=dict(profile_recurrence_steps=0,finite_head_checks=0),**base)
    gs={K:1+c/F(K)}
    for r in range(K-1,0,-1):gs[r]=(lam*t+beta*r*r)/(lam+beta*r*r-eps)*gs[r+1]
    gs[0]=2*t*gs[1]
    def g(r):return gs[r] if r<=K else 1+c/F(r)
    def d(r):return g(r)-g(r+1)
    dstar=min([c]+[(r+1)**2*d(r) for r in range(1,K)])
    q=F(1);arg=None;emax=F(0)
    for r in range(1,J):
        E=mu*(g(r-1)/t-g(r))+Kf*r*d(r-1)+2*beta*r*d(r)
        trial=4*(r+1)**2*max(E,F(0))/rec['kminus']
        if trial>emax:emax=trial;arg=r
    q+=emax;Ce=11*Kf+12*lam*t+12*mu
    Nstar=ceilq(max(F(1),F(4*J),q,22*q*rec['sratio']/dstar,2*q*Ce/eps))
    zeta=min(eps,lam)/4;H=gs[0]+q/4
    cfcoef=(zeta+lam+mu*Nstar+rec['S']*Nstar*Nstar)*H
    receipt=dict(status='CERTIFIED_NUMERICAL',constants=dict(beta=beta,Kf=Kf,kminus=rec['kminus'],
        kplus=rec['kplus'],sratio=rec['sratio'],L=L,epsilon=eps,c=c,K=K,D=D,J=J,dstar=dstar,
        q=q,q_argmax=arg,Ce=Ce,Nstar=Nstar,zeta=zeta,H=H,S=rec['S']),
        profile=dict(head=tuple(gs[r] for r in range(K+1)),tail='1+c/r for r>=K'),
        Foster=dict(coefficient=cfcoef,base=t,exponent=Nstar+1,
            inequality='LW <= -zeta W + coefficient*base^exponent*1_{N<Nstar}'),
        stationary_moment=dict(coefficient=cfcoef/zeta,base=t,exponent=Nstar+1),
        implicit_head_states=dict(binomial_top=Nstar+rec['n']-1,binomial_choose=rec['n']),
        work=dict(profile_recurrence_steps=K-1,finite_head_checks=J-1,profile_values_retained=K+1,
             infinite_tail_checks=1,states_enumerated=0,stationary_fiber_laws=0,expanded_Foster_powers=0),**base)
    receipt['work']['retained_scalar_bits']=bits(receipt)
    return receipt

def numerical(raw,t,max_profile_steps=100000):
    # Domain validation precedes unsupported-family status.
    t=rat(t)
    if t<=1:raise ValueError('t>1 required')
    if type(max_profile_steps) is not int or max_profile_steps<0:raise ValueError('iteration budget')
    try:rec=recognize(raw)
    except Unsupported as exc:return dict(status='UNKNOWN',family=FAMILY,reason=str(exc),stability='UNKNOWN')
    return _numerical(rec,t,max_profile_steps)

def receive_qualitative(raw,receipt):return canonical(qualitative(raw))==canonical(receipt)
def receive_numerical(raw,t,receipt,max_profile_steps=100000):
    return canonical(numerical(raw,t,max_profile_steps))==canonical(receipt)

def profile(receipt,r):
    co=receipt['constants'];head=receipt['profile']['head']
    return head[r] if r<=co['K'] else 1+co['c']/r

def inventory(rec,x):
    return x[rec['a']]+sum(min(sum(x[i] for i in l),sum(x[i] for i in r)) for l,r in rec['components'])
def hvalue(rec,receipt,x):
    N=sum(x);r=inventory(rec,x)
    return profile(receipt,r)+receipt['constants']['q']*F(x[rec['a']],(N+1)*(r+1)**2)
def falling(x,u):
    ans=1
    for a,b in zip(x,u):
        if a<b:return 0
        for j in range(b):ans*=a-j
    return ans
def scaled_drift(rec,receipt,x):
    h=hvalue(rec,receipt,x);t=receipt['t'];out=F(0)
    for u,v,k in rec['channels']:
        rate=k*falling(x,u)
        if not rate:continue
        xp=tuple(a-b+c for a,b,c in zip(x,u,v));delta=sum(v)-sum(u)
        out+=rate*(t**delta*hvalue(rec,receipt,xp)-h)
    return out

def fixture(bicliques=(((2,),(3,)),),n=4,a=0,port=(1,1),special=True):
    """Build full arm incidence for test inputs; recognition never assumes this builder."""
    def z(*inds):return tuple(inds.count(i) for i in range(n))
    raw=[(z(),z(a),F(port[0])),(z(a),z(),F(port[1]))]
    for left,right in bicliques:
        for i in left:
            for j in right:
                hub=z(i,j);raw.extend([(z(a,a),hub,F(1)),(hub,z(a,a),F(1))])
                for x in range(n):
                    if x==a:continue
                    reverse=F(2) if special and n==4 and x==2 else F(1)
                    raw.extend([(z(a,x),hub,F(1)),(hub,z(a,x),reverse)])
    return raw

if __name__=='__main__':
    raw=fixture();q=qualitative(raw);c=numerical(raw,F(2));print(canonical(c))
