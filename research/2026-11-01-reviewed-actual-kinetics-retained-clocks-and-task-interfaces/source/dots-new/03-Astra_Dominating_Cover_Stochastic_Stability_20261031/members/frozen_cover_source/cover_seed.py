#!/usr/bin/env python3
"""Trusted exact research constructor, not a hostile-input validator.
Qualitative recognition is finite and separate from numerical profile acquisition.
Finite graph scans acquire covers; a finite profile head joins a rational tail.
"""
from fractions import Fraction as F
import hashlib,json,sys
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
FAMILY='dominating-cover-seed-three-energy-v1'
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
    satellites=tuple(i for i in range(n) if i!=a)
    graph={i:set() for i in satellites}
    for i,j in hubs.values():graph[i].add(j);graph[j].add(i)
    # No induced triangle+isolate or P4+isolate: checked on all satellite vertices.
    from itertools import combinations
    pattern_tests=0
    for size,edge_count,degree_pattern in [(4,3,[0,2,2,2]),(5,3,[0,1,1,2,2])]:
        for subset in combinations(satellites,size):
            pattern_tests+=1
            degrees=[sum(j in graph[i] for j in subset) for i in subset]
            if sum(degrees)==2*edge_count and sorted(degrees)==degree_pattern:
                raise Unsupported('forbidden cover-domination pattern on '+str(subset))
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
        satellites=satellites,edges=tuple(sorted(hubs.values())),hubs=tuple(hubrows),
        kX=tuple(sorted(kX.items())),kminus=min(kX.values()),kplus=max(kX.values()),a_sum=as_,
        bmin=bmin,smax=max(h['reverse_sum'] for h in hubrows),
        b0=min(h['reverse_sum']+h['to_two_a'] for h in hubrows),
        F0=2*as_+max(kX.values()),S=sum((k for u,v,k in internal),F(0)),
        raw_sha256=digest(channels),work=dict(input_rows=len(raw),normalized_channels=len(channels),
        raw_coordinate_checks=coordinate_checks,internal_complex_checks=complex_checks,
        reverse_edge_tests=reverse_tests,forbidden_pattern_tests=pattern_tests,
        amplification_edge_tests=amp_tests,arm_incidence_tests=incidence_tests))
    return rec

def covers(rec):
    vs=rec['satellites'];edges=rec['edges'];out=[]
    for mask in range(1<<len(vs)):
        c=frozenset(vs[j] for j in range(len(vs)) if mask>>j&1)
        if not all(i in c or j in c for i,j in edges):continue
        if any(all(i in c-{v} or j in c-{v} for i,j in edges) for v in c):continue
        out.append(tuple(sorted(c)))
    assert out
    return tuple(out)
def _qual(rec):
    return dict(status='CERTIFIED_QUALITATIVE',family=FAMILY,raw_sha256=rec['raw_sha256'],
        conclusion='irreducible positive recurrence; every finite exponential stationary total-count moment',
        role=dict(dimension=rec['n'],open_coordinate=rec['a'],immigration=rec['lam'],death=rec['mu']),
        inventory='A+minimum weighted structural vertex-cover count; no supplied cover oracle',
        graph=dict(vertices=rec['satellites'],edges=rec['edges'],excluded_induced_patterns=['triangle plus isolate','P4 plus isolate']),
        work=dict(**rec['work'],cover_masks_enumerated=0,profile_steps=0,states_enumerated=0,stationary_fiber_laws=0))
def qualitative(raw):
    try:return _qual(recognize(raw))
    except Unsupported as exc:return dict(status='UNKNOWN',family=FAMILY,reason=str(exc),stability='UNKNOWN')

def numerical(raw,t,max_profile_steps=100000,max_cover_masks=1048576):
    t=rat(t)
    if t<=1:raise ValueError('t>1 required')
    for budget in (max_profile_steps,max_cover_masks):
        if type(budget) is not int or budget<0:raise ValueError('nonnegative exact integer budget')
    try:rec=recognize(raw)
    except Unsupported as exc:return dict(status='UNKNOWN',family=FAMILY,reason=str(exc),stability='UNKNOWN')
    lam,mu,S=rec['lam'],rec['mu'],rec['S'];m=rec['n']-1;E=len(rec['edges'])
    Kf=rec['a_sum']+m*rec['kplus'];beta=rec['bmin']/(16*E)
    L=lam*(t-1);eps0=min(F(1),(lam+beta)/2);c=4*(L+eps0)/beta;K=max(2,ceilq(2*c))
    D=mu*(1-1/t);eps=min(F(1,4),D/(4*(rec['F0']+D)),eps0/(4*mu))
    J=max(K+1,2,ceilq(4*c*(mu+Kf+beta)/D))
    required_steps=K-1+J-1;masks=1<<m
    if required_steps>max_profile_steps or masks>max_cover_masks:
        return dict(status='UNKNOWN_NUMERICAL_BUDGET',family=FAMILY,qualitative=_qual(rec),
          required_profile_steps=required_steps,required_cover_masks=masks,
          max_profile_steps=max_profile_steps,max_cover_masks=max_cover_masks,
          scope='qualitative stability CERTIFIED; requested explicit quantitative construction not acquired')
    head={K:1+c/K}
    for r in range(K-1,0,-1):head[r]=(lam*t+beta*r*r)/(lam+beta*r*r-eps0)*head[r+1]
    head[0]=2*t*head[1]
    def g(r):return head[r] if r<K else 1+c/r
    def d(r):return g(r)-g(r+1)
    dstar=min([c]+[(r+1)**2*d(r)for r in range(1,K)])
    G=max([F(3)]+[d(r-1)/d(r) for r in range(1,K+1)])
    q=1+max(4*(r+1)**2*max(mu*(g(r-1)/t-g(r))+Kf*r*d(r-1)+2*beta*r*d(r)+eps*(rec['F0']+D),0)/rec['kminus'] for r in range(1,J))
    delta=min(F(1,2*rec['n']),F(1,2*E),rec['bmin']/(8*E*rec['smax']*G))
    Ccore=12*lam*t+12*mu;Ce=11*Kf+Ccore
    Cint=2*L+2*mu+(2*c+11)*S/delta**2+Ccore
    kap=min(D*delta/4,eps*rec['b0']*delta**2/(32*E))
    Nstar=ceilq(max(F(1),q,F(K)/delta,88*q*rec['smax']/(rec['bmin']*dstar),4*q*Ce/eps0,(Cint+1)/kap))
    zeta=min(eps0,lam)/4;H=g(0)+q/4
    constants=dict(Kf=Kf,beta=beta,L=L,epsilon0=eps0,c=c,K=K,D=D,epsilon=eps,J=J,dstar=dstar,G=G,q=q,delta=delta,Ccore=Ccore,Ce=Ce,Cint=Cint,kappa=kap,Nstar=Nstar,zeta=zeta,H=H)
    cf=(zeta+lam+mu*Nstar+S*Nstar*Nstar)*H
    out=dict(status='CERTIFIED_NUMERICAL',family=FAMILY,raw_sha256=rec['raw_sha256'],t=t,qualitative=_qual(rec),
        covers=covers(rec),constants=constants,profile_head=tuple(head[r] for r in range(K)),
        Foster=dict(coefficient=cf,base=t,exponent=Nstar+1),
        stationary_moment=dict(coefficient=2*cf/zeta,base=t,exponent=Nstar+1),
        work=dict(profile_steps=required_steps,cover_masks_enumerated=masks,retained_covers=0,states_enumerated=0,expanded_Foster_powers=0,stationary_fiber_laws=0),
        cost_scope='Budgets cap only the stated profile-loop and cover-mask counts, not rational bit cost or wall time. Powers stay factored. No polynomial-bit quantitative acquisition claim.')
    out['work']['retained_covers']=len(out['covers']);out['work']['retained_scalar_bits']=bits(out)
    return out

def receive_qualitative(raw,receipt):return canonical(qualitative(raw))==canonical(receipt)
def receive_numerical(raw,t,receipt,**budgets):return canonical(numerical(raw,t,**budgets))==canonical(receipt)
def coordinates(rec,cert,x):
    N=sum(x);A=x[rec['a']];weights=tuple(sum(x[v] for v in c) for c in cert['covers']);tau=min(weights)
    return N,A,tau,A+tau,weights
def profile(cert,r):
    co=cert['constants'];return cert['profile_head'][r]if r<co['K']else 1+co['c']/r
def hvalue(rec,cert,x):
    N,A,tau,R,weights=coordinates(rec,cert,x);co=cert['constants']
    return profile(cert,R)+co['q']*F(A,(N+1)*(R+1)**2)-co['epsilon']*F(A,N+1)
def falling(x,u):
    ans=1
    for a,b in zip(x,u):
        if a<b:return 0
        for j in range(b):ans*=a-j
    return ans
def scaled_drift(rec,cert,x):
    h=hvalue(rec,cert,x);t=cert['t'];out=F(0)
    for u,v,k in rec['channels']:
        rate=k*falling(x,u)
        if not rate:continue
        xp=tuple(a-b+c for a,b,c in zip(x,u,v));delta=sum(v)-sum(u)
        out+=rate*(t**delta*hvalue(rec,cert,xp)-h)
    return out

def fixture(edges=((1,2),(2,3),(3,4)),n=5,a=0,port=(1,1),special=True):
    def z(*inds):return tuple(inds.count(i)for i in range(n))
    raw=[(z(),z(a),F(port[0])),(z(a),z(),F(port[1]))]
    hubs=[z(i,j)for i,j in edges]
    for h in hubs:raw.extend([(z(a,a),h,F(1)),(h,z(a,a),F(1))])
    satellites=[i for i in range(n)if i!=a]
    for off,x in enumerate(satellites):
        h=hubs[off%len(hubs)]
        # Diagnostic P4 uses AE <-> CD rather than default wrap to BC.
        if n==5 and edges==((1,2),(2,3),(3,4)) and off==3:h=hubs[1]
        reverse=F(2)if special and off==len(satellites)-1 else F(1)
        raw.extend([(z(a,x),h,F(1)),(h,z(a,x),reverse)])
    return raw

if __name__=='__main__':
    cert=numerical(fixture(),F(2));co=cert['constants']
    print(json.dumps(encode(dict(status=cert['status'],raw_sha256=cert['raw_sha256'],covers=cert['covers'],constants=co,work=cert['work'],certificate_sha256=digest(cert))),indent=2))
