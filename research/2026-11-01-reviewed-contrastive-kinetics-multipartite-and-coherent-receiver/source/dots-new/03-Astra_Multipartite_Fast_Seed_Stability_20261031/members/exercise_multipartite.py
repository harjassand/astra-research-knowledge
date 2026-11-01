#!/usr/bin/env python3
from multipartite_seed import *
from itertools import product,permutations
import copy

def local(rec,cert,x):
    N,A,M,R,parts=coordinates(rec,x);co=cert['constants'];t=cert['t'];eta=co['eta'];eps=co['epsilon']
    h=hvalue(rec,cert,x);assert F(1,2)<=h<=co['H']
    if R==0:
        assert A==0 and all(not falling(x,u)for u,v,k in rec['internal'])
        assert scaled_drift(rec,cert,x)<=-rec['lam']*h/2
        return 2,0,0
    P=(1+eta)*R-eta*A;assert R<=P<=(1+eta)*R and h<=2
    li=la=F(0);jumps=ties=0
    for u,v,k in rec['internal']:
        rate=k*falling(x,u)
        if not rate:continue
        xp=tuple(xx-uu+vv for xx,uu,vv in zip(x,u,v));Np,Ap,Mp,Rp,pp=coordinates(rec,xp)
        Pp=(1+eta)*Rp-eta*Ap;dp=Pp-P
        assert Rp>=1 and abs(Rp-R)<=1 and abs(dp)<=1+2*eta
        assert abs(1/Pp-1/P)<=6/(P*P)
        li+=rate*(1/Pp-1/P);la+=rate*(Ap-A);jumps+=1
        if 2*R<N and pp.count(max(pp))>1:ties+=1
    Q=sum(x[z['edge'][0]]*x[z['edge'][1]]for z in rec['hubs'])
    assert li<=6*co['S']*N*N/(P*P)
    if 2*R<N:assert li<=-co['gamma']*M/P+6*co['S']
    assert la>=co['b0']*Q-co['F0']*A*N
    drift=scaled_drift(rec,cert,x)
    master=co['B']+li-co['D']*A/4-eps*co['b0']*F(Q,N+1)
    assert drift<=master,(x,drift,master)
    if R<=co['delta']*N:assert drift<=-1
    if N>=co['Nstar']:assert drift<=-co['zeta']*h
    else:assert drift+co['zeta']*h<=cert['Foster']['coefficient']
    return 9+jumps,jumps,ties

def permute(raw,p):return [(tuple(u[i]for i in p),tuple(v[i]for i in p),k)for u,v,k in raw]
def leaves(x,path=()):
    if isinstance(x,dict):
        for k,v in x.items():yield from leaves(v,path+(k,))
    elif isinstance(x,(list,tuple)):
        for k,v in enumerate(x):yield from leaves(v,path+(k,))
    else:yield path,x

def alter(x,p,v):
    if not p:return v
    k=p[0]
    if isinstance(x,dict):o=dict(x);o[k]=alter(o[k],p[1:],v);return o
    o=list(x);o[k]=alter(o[k],p[1:],v);return tuple(o)if isinstance(x,tuple)else o

def radial(rec,cert,x):
    eta=cert['constants']['eta'];t=cert['t']
    def hr(z):
        N,A,M,R,_=coordinates(rec,z)
        return 1+1/((1+eta)*R-eta*A)
    hx=hr(x);value=F(0)
    for u,v,k in rec['channels']:
        rate=k*falling(x,u)
        if rate:
            xp=tuple(xx-uu+vv for xx,uu,vv in zip(x,u,v));value+=rate*(t**(sum(v)-sum(u))*hr(xp)-hx)
    return value

def general_hub_raw(n,edges,a=0):
    def z(*ix):return tuple(ix.count(i)for i in range(n))
    hs=[z(i,j)for i,j in edges];rr=[(z(),z(a),F(1)),(z(a),z(),F(1))]
    for h in hs:
        rr.extend([(z(a,a),h,F(1)),(h,z(a,a),F(1))])
        for x in range(n):
            if x!=a:rr.extend([(z(a,x),h,F(1)),(h,z(a,x),F(1))])
    return rr

def run():
    cases=[('triangle',fixture(),F(2)),('shared_bipartite',fixture(((1,2),(3,4)),5),F(2)),
      ('three_nonsingleton_parts',fixture(((1,2),(3,4),(5,)),6),F(2)),
      ('four_part_clique',fixture(((1,),(2,),(3,),(4,)),5),F(3,2)),
      ('near_one',fixture(),F(1001,1000)),('large_t',fixture(),F(1000)),
      ('tiny_death',fixture(port=(1,F(1,10**80))),F(2))]
    summaries=[];states=assertions=jumps=ties=outside=0
    for name,raw,t in cases:
        rec=recognize(raw);cert=numerical(raw,t);assert cert['status']=='CERTIFIED_NUMERICAL'
        assert receive_numerical(raw,t,cert)and receive_qualitative(raw,qualitative(raw))
        bound=4 if rec['n']==4 else 2
        for x in product(range(bound),repeat=rec['n']):
            c,j,z=local(rec,cert,x);assertions+=c;jumps+=j;ties+=z;states+=1
        ns=[cert['constants']['Nstar'],cert['constants']['Nstar']+1,10**30,10**100]
        for size in ns:
            for xindex in range(rec['n']):
                for active in [0,1,2,10]:
                    x=[0]*rec['n'];x[xindex]=size;x[rec['a']]+=active
                    c,j,z=local(rec,cert,tuple(x));assertions+=c;jumps+=j;ties+=z;states+=1;outside+=int(sum(x)>=cert['constants']['Nstar'])
            for active in [0,1,2]:
                # Exact multiway maximum ties, and one-off switching configurations.
                for perturb in [0,1,-1]:
                    x=[0]*rec['n'];x[rec['a']]=active
                    for part in rec['parts']:x[part[0]]=size
                    x[rec['parts'][0][0]]+=perturb
                    c,j,z=local(rec,cert,tuple(x));assertions+=c;jumps+=j;ties+=z;states+=1;outside+=int(sum(x)>=cert['constants']['Nstar'])
        summaries.append(dict(name=name,n=rec['n'],parts=len(rec['parts']),t=t,Nstar=cert['constants']['Nstar'],
            work=cert['work'],receipt_sha256=digest(cert)))
    raw=fixture();q=qualitative(raw);c=numerical(raw,F(2));tamper=0
    for obj,receiver in [(q,lambda z:receive_qualitative(raw,z)),(c,lambda z:receive_numerical(raw,F(2),z))]:
        for path,value in leaves(obj):
            changed=value+1 if type(value)in(int,F)else str(value)+'!'
            assert not receiver(alter(obj,path,changed));tamper+=1
    perms=0
    for p in permutations(range(4)):
        cp=numerical(permute(raw,p),F(2));assert cp['constants']==c['constants'];perms+=1
    # The radial inverse alone fails on every three-way balanced ray.
    rec=recognize(raw);radial_checks=[]
    for size in [1,10,100,10**12,c['constants']['Nstar']]:
        x=(0,size,size,size);r=radial(rec,c,x);full=scaled_drift(rec,c,x)
        assert r>0
        if sum(x)>=c['constants']['Nstar']:assert full<0
        radial_checks.append(dict(n=size,radial_positive=True,full_scaled_drift=full))
    # Matching loses two at an actual admitted non-complex-balanced triangle arm.
    # At (0,M,2M,M), BD->AC removes both minority species and adds majority C.
    eta=c['constants']['eta'];matching_witnesses=[]
    for M in [1,2,100,10**30]:
        x=(0,M,2*M,M);xp=(1,M-1,2*M+1,M-1)
        nu=lambda z:min(sum(z[1:])//2,sum(z[1:])-max(z[1:]))
        assert nu(x)-nu(xp)==2 and x[0]+nu(x)-(xp[0]+nu(xp))==1
        matching_witnesses.append(M)
    repartitions=[]
    for name,n,edges,wanted in [('triangle_minus_edge',4,[(1,2),(1,3)],2),
        ('K4_minus_edge',5,[(i,j)for i in range(1,5)for j in range(i+1,5)if(i,j)!=(1,2)],3)]:
        rr=general_hub_raw(n,edges);rc=recognize(rr);cc=numerical(rr,F(2))
        assert cc['status']=='CERTIFIED_NUMERICAL' and len(rc['parts'])==wanted
        repartitions.append(dict(name=name,parts=rc['parts'],status='CERTIFIED_NUMERICAL'))
    controls=[]
    for name,rr in [('P4',general_hub_raw(5,[(1,2),(2,3),(3,4)])),
      ('free_passenger',general_hub_raw(4,[(2,3)])),('disconnected_pairs',general_hub_raw(5,[(1,2),(3,4)]))]:
        got=qualitative(rr);assert got['status']=='UNKNOWN';controls.append((name,got['reason'],'unit-rate detailed-balanced control'))
    # Extrapolating the new formula to a free passenger has positive drift.
    free=general_hub_raw(4,[(2,3)]);N=10**30
    h=lambda aa,nn:1+1/((1+eta)*nn-eta*aa)-c['constants']['epsilon']*F(aa,nn+1)
    free_drift=2*h(1,N+1)-h(0,N);assert free_drift>0
    invalid=0
    for bad in [0,-1,True,1.5,'1']:
        rr=copy.deepcopy(raw);u,v,k=rr[0];rr[0]=(u,v,bad)
        try:qualitative(rr)
        except(TypeError,ValueError):invalid+=1
        else:raise AssertionError('invalid rate admitted')
    for t in [1,0,True,2.0,'2',None]:
        try:numerical(raw,t)
        except(TypeError,ValueError):invalid+=1
        else:raise AssertionError('invalid t admitted')
    # Polynomial-size compact output across huge numerical rate magnitudes.
    huge=fixture(port=(1,F(1,10**5000)));hc=numerical(huge,F(2));wire=canonical(hc)
    assert hc['status']=='CERTIFIED_NUMERICAL' and receive_numerical(huge,F(2),json.loads(wire))
    assert hc['work']['rate_dependent_iterations']==0
    return dict(status='PASS',cases=summaries,states=states,local_assertions=assertions,enabled_internal_jumps=jumps,
       actual_destination_ties=ties,outside_Foster_checks=outside,semantic_mutations_rejected=tamper,
       coordinate_permutations=perms,radial_obstructions=radial_checks,matching_drop_two_witnesses=matching_witnesses,
       stable_UNKNOWN_controls=controls,admitted_repartitions=repartitions,free_passenger_scaled_drift_positive=True,invalid_domains=invalid,
       huge_rate_wire=dict(bytes=len(wire),sha256=hashlib.sha256(wire.encode()).hexdigest(),scalar_bits=hc['work']['retained_scalar_bits'],
           Nstar_digits=len(str(hc['constants']['Nstar'])),formula_blocks=hc['work']['numerical_formula_blocks']),
       no_simulation=True,no_exception_enumeration=True,no_Foster_power_expansion=True)
if __name__=='__main__':print(canonical(run()))
