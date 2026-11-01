#!/usr/bin/env python3
"""Trusted exact research constructor, not a hostile-input validator.
Qualitative recognition is finite and separate from numerical profile acquisition.
Numerical constants use fixed rational formulas; Foster powers stay factored.
"""
from fractions import Fraction as F
import hashlib,json,sys
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
FAMILY='multipartite-fast-seed-two-energy-v1'
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
    # The complement components must be cliques: complete multipartite recognition.
    seen=set();parts=[];complement_pair_tests=0;within_tests=cross_tests=0
    for seed in satellites:
        if seed in seen:continue
        seen.add(seed);todo=[seed];part=[]
        while todo:
            i=todo.pop();part.append(i)
            for j in satellites:
                complement_pair_tests+=1
                if j!=i and j not in graph[i] and j not in seen:seen.add(j);todo.append(j)
        parts.append(tuple(sorted(part)))
    if len(parts)<2:raise Unsupported('hub graph must be complete multipartite with at least two parts; no isolated passengers')
    for part in parts:
        for off,i in enumerate(part):
            for j in part[off+1:]:
                within_tests+=1
                if j in graph[i]:raise Unsupported('nonadjacency is not a partition: missing multipartite cross edges')
    for z,left in enumerate(parts):
        for right in parts[z+1:]:
            for i in left:
                for j in right:
                    cross_tests+=1
                    if j not in graph[i]:raise Unsupported('missing multipartite cross edge')
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
        parts=tuple(parts),hubs=tuple(hubrows),
        kX=tuple(sorted(kX.items())),kminus=min(kX.values()),kplus=max(kX.values()),a_sum=as_,
        bmin=bmin,smax=max(h['reverse_sum'] for h in hubrows),
        b0=min(h['reverse_sum']+h['to_two_a'] for h in hubrows),
        F0=2*as_+max(kX.values()),S=sum((k for u,v,k in internal),F(0)),
        raw_sha256=digest(channels),work=dict(input_rows=len(raw),normalized_channels=len(channels),
        raw_coordinate_checks=coordinate_checks,internal_complex_checks=complex_checks,
        reverse_edge_tests=reverse_tests,complement_pair_tests=complement_pair_tests,
        within_part_pair_tests=within_tests,cross_part_pair_tests=cross_tests,
        amplification_edge_tests=amp_tests,arm_incidence_tests=incidence_tests))
    return rec

def _qual(rec):
    return dict(status='CERTIFIED_QUALITATIVE',family=FAMILY,raw_sha256=rec['raw_sha256'],
        conclusion='irreducible positive recurrence; every finite exponential stationary total-count moment',
        role=dict(dimension=rec['n'],open_coordinate=rec['a'],immigration=rec['lam'],death=rec['mu']),
        inventory=dict(parts=rec['parts'],formula='R=N-max(part totals); P=(1+eta)R-eta*A'),
        hubs=rec['hubs'],work=dict(**rec['work'],numerical_formula_blocks=0,profile_recurrence_steps=0,
              states_enumerated=0,stationary_fiber_laws=0,expanded_Foster_powers=0))
def qualitative(raw):
    try:return _qual(recognize(raw))
    except Unsupported as exc:return dict(status='UNKNOWN',family=FAMILY,reason=str(exc),stability='UNKNOWN')

def numerical(raw,t):
    t=rat(t)
    if t<=1:raise ValueError('t>1 required')
    try:rec=recognize(raw)
    except Unsupported as exc:return dict(status='UNKNOWN',family=FAMILY,reason=str(exc),stability='UNKNOWN')
    lam,mu,S=rec['lam'],rec['mu'],rec['S'];q=len(rec['parts'])
    # Fixed formula blocks, not a count of individual rational machine operations.
    eta=rec['bmin']/(16*rec['smax'])
    c0=min(eta*rec['kminus']/3,rec['bmin']/4);gamma=c0/(1+eta)
    D=mu*(1-1/t);eps=min(F(1,2),D/(4*rec['F0']))
    B=2*lam*(t-1)+5*mu
    delta=min(F(1,4),gamma/(2*(1+eta)*(B+6*S+1)))
    kap=delta/8*min(D,eps*rec['b0']/q)
    Cint=B+6*S/(delta*delta)
    Nstar=max(1,ceilq((Cint+1)/kap));zeta=min(F(1),lam)/2;H=4*t
    cf=(zeta+lam+mu*Nstar+S*Nstar*Nstar)*H
    out=dict(status='CERTIFIED_NUMERICAL',family=FAMILY,raw_sha256=rec['raw_sha256'],t=t,qualitative=_qual(rec),
       constants=dict(parts=q,kminus=rec['kminus'],kplus=rec['kplus'],a_sum=rec['a_sum'],bmin=rec['bmin'],
          smax=rec['smax'],b0=rec['b0'],F0=rec['F0'],S=S,eta=eta,c0=c0,gamma=gamma,D=D,epsilon=eps,
          B=B,delta=delta,kappa=kap,Cint=Cint,Nstar=Nstar,zeta=zeta,H=H),
       profile=dict(active='1+1/P-epsilon*A/(N+1)',inactive=H,P='(1+eta)R-eta*A'),
       Foster=dict(coefficient=cf,base=t,exponent=Nstar+1,
           inequality='LW<=-zeta*W+coefficient*base^exponent*1_{N<Nstar}'),
       stationary_moment=dict(coefficient=2*cf/zeta,base=t,exponent=Nstar+1),
       implicit_head_states=dict(binomial_top=Nstar+rec['n']-1,binomial_choose=rec['n']),
       work=dict(numerical_formula_blocks=14,profile_recurrence_steps=0,rate_dependent_iterations=0,
           states_enumerated=0,stationary_fiber_laws=0,expanded_Foster_powers=0),
       cost_scope='14 named scalar formula blocks after finite raw scans; not14 machine operations; polynomial-bit factored outputs, no service resource cap')
    out['work']['retained_scalar_bits']=bits(out)
    return out

def receive_qualitative(raw,receipt):return canonical(qualitative(raw))==canonical(receipt)
def receive_numerical(raw,t,receipt):return canonical(numerical(raw,t))==canonical(receipt)
def coordinates(rec,x):
    N=sum(x);A=x[rec['a']];part=tuple(sum(x[i] for i in group) for group in rec['parts']);M=max(part)
    return N,A,M,N-M,part

def hvalue(rec,cert,x):
    N,A,M,R,parts=coordinates(rec,x);co=cert['constants']
    if R==0:return co['H']
    P=(1+co['eta'])*R-co['eta']*A
    return 1+1/P-co['epsilon']*F(A,N+1)
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

def fixture(parts=((1,),(2,),(3,)),n=4,a=0,port=(1,1),special=True,sparse=True):
    """Trusted finite fixture builder; recognition does not assume its layout."""
    def z(*inds):return tuple(inds.count(i) for i in range(n))
    raw=[(z(),z(a),F(port[0])),(z(a),z(),F(port[1]))]
    hubs=[z(i,j)for g,left in enumerate(parts)for right in parts[g+1:]for i in left for j in right]
    for hub in hubs:raw.extend([(z(a,a),hub,F(1)),(hub,z(a,a),F(1))])
    satellites=[i for i in range(n)if i!=a]
    for off,x in enumerate(satellites):
        for hindex,hub in enumerate(hubs):
            if sparse and hindex!=off%len(hubs):continue
            reverse=F(2)if special and off==0 and hindex==0 else F(1)
            raw.extend([(z(a,x),hub,F(1)),(hub,z(a,x),reverse)])
    return raw

if __name__=='__main__':print(canonical(numerical(fixture(),F(2))))
