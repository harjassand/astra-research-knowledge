#!/usr/bin/env python3
"""Trusted exact circuit compiler; no graph/capacity optimization oracle input.
Finite profile loops and rational bit growth remain fully charged.
"""
from pathlib import Path
import sys,json,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parent/'frozen_cover_source'))
import cover_seed as B
from fractions import Fraction as F
rat,ceilq,encode,canonical,digest,bits=B.rat,B.ceilq,B.encode,B.canonical,B.digest,B.bits
FAMILY='dominating-cover-polynomial-inventory-circuit-v1'

def compile_inventory(rec):
    vs=rec['satellites'];graph={v:set()for v in vs}
    for u,v in rec['edges']:graph[u].add(v);graph[v].add(u)
    anchors=[];work=dict(anchors=0,anti_neighborhood_tests=0,component_neighbor_tests=0,biclique_pair_tests=0)
    for anchor in vs:
        work['anchors']+=1
        universe=[]
        for v in vs:
            work['anti_neighborhood_tests']+=1
            if v!=anchor and v not in graph[anchor]:universe.append(v)
        unseen=set(universe);bicliques=[];isolates=[]
        while unseen:
            seed=min(unseen);color={seed:0};todo=[seed];unseen.remove(seed)
            while todo:
                u=todo.pop()
                for v in universe:
                    work['component_neighbor_tests']+=1
                    if v not in graph[u]:continue
                    if v in color:assert color[v]!=color[u]
                    else:color[v]=1-color[u];unseen.remove(v);todo.append(v)
            if len(color)==1:isolates.append(seed);continue
            left=tuple(sorted(v for v in color if color[v]==0));right=tuple(sorted(v for v in color if color[v]==1))
            for u in left:
                for v in right:work['biclique_pair_tests']+=1;assert v in graph[u]
            bicliques.append((left,right))
        anchors.append(dict(anchor=anchor,isolates=tuple(isolates),bicliques=tuple(bicliques)))
    return dict(vertices=vs,edges=rec['edges'],anchors=tuple(anchors),work=work,
        formula='tau=sum satellite counts-max_anchor(anchor count+isolated counts+sum max(biclique shore totals))')

def independent_weight(circuit,x):
    return max(x[row['anchor']]+sum(x[v]for v in row['isolates'])+sum(max(sum(x[v]for v in l),sum(x[v]for v in r))for l,r in row['bicliques'])for row in circuit['anchors'])
def cover_weight(circuit,x):return sum(x[v]for v in circuit['vertices'])-independent_weight(circuit,x)
def optimal_minimal_cover(circuit,x):
    best=None;chosen=None
    for row in circuit['anchors']:
        chosen_now={row['anchor'],*row['isolates']}
        for l,r in row['bicliques']:
            chosen_now.update(l if sum(x[v]for v in l)>=sum(x[v]for v in r)else r)
        value=sum(x[v]for v in chosen_now)
        if best is None or value>best:best=value;chosen=chosen_now
    graph={v:set()for v in circuit['vertices']}
    for u,v in circuit['edges']:graph[u].add(v);graph[v].add(u)
    for v in circuit['vertices']:
        if v not in chosen and not(graph[v]&chosen):assert x[v]==0;chosen.add(v)
    cover=tuple(v for v in circuit['vertices']if v not in chosen)
    assert sum(x[v]for v in cover)==cover_weight(circuit,x)
    return cover

def bad_active_edges(circuit,x):
    value=independent_weight(circuit,x);out=[]
    for u,v in circuit['edges']:
        if x[u]<=0 or x[v]<=0:continue
        z=list(x);z[u]=z[v]=0
        if independent_weight(circuit,z)==value:out.append((u,v))
    return tuple(out)
def _qual(rec):
    old=B._qual(rec)
    return dict(status='CERTIFIED_QUALITATIVE',family=FAMILY,raw_sha256=rec['raw_sha256'],conclusion=old['conclusion'],
      role=old['role'],graph=old['graph'],inventory=compile_inventory(rec),
      work=dict(raw=rec['work'],cover_masks_enumerated=0,profile_steps=0,states_enumerated=0,stationary_fiber_laws=0),
      cost_scope='Raw forbidden-pattern scans and polynomial-size anti-neighborhood max-plus circuit; explicit profile not materialized')
def qualitative(raw):
    try:return _qual(B.recognize(raw))
    except B.Unsupported as exc:return dict(status='UNKNOWN',family=FAMILY,reason=str(exc),stability='UNKNOWN')

def numerical(raw,t,max_profile_steps=100000):
    t=rat(t)
    if t<=1:raise ValueError('t>1 required')
    for budget in (max_profile_steps,):
        if type(budget) is not int or budget<0:raise ValueError('nonnegative exact integer budget')
    try:rec=B.recognize(raw)
    except B.Unsupported as exc:return dict(status='UNKNOWN',family=FAMILY,reason=str(exc),stability='UNKNOWN')
    lam,mu,S=rec['lam'],rec['mu'],rec['S'];m=rec['n']-1;E=len(rec['edges'])
    Kf=rec['a_sum']+m*rec['kplus'];beta=rec['bmin']/(16*E)
    L=lam*(t-1);eps0=min(F(1),(lam+beta)/2);c=4*(L+eps0)/beta;K=max(2,ceilq(2*c))
    D=mu*(1-1/t);eps=min(F(1,4),D/(4*(rec['F0']+D)),eps0/(4*mu))
    J=max(K+1,2,ceilq(4*c*(mu+Kf+beta)/D))
    required_steps=K-1+J-1
    if required_steps>max_profile_steps:
        return dict(status='UNKNOWN_NUMERICAL_BUDGET',family=FAMILY,qualitative=_qual(rec),
          required_profile_steps=required_steps,
          max_profile_steps=max_profile_steps,
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
        inventory=compile_inventory(rec),constants=constants,profile_head=tuple(head[r] for r in range(K)),
        Foster=dict(coefficient=cf,base=t,exponent=Nstar+1),
        stationary_moment=dict(coefficient=2*cf/zeta,base=t,exponent=Nstar+1),
        work=dict(profile_steps=required_steps,cover_masks_enumerated=0,states_enumerated=0,expanded_Foster_powers=0,stationary_fiber_laws=0),
        cost_scope='Polynomial inventory-circuit acquisition/evaluation after raw scans; profile-loop budget is not rational bit or wall-time cap. Powers stay factored. No polynomial-bit complete quantitative acquisition claim.')
    out['work']['retained_scalar_bits']=bits(out)
    return out


def receive_qualitative(raw,receipt):return canonical(qualitative(raw))==canonical(receipt)
def receive_numerical(raw,t,receipt,**budget):return canonical(numerical(raw,t,**budget))==canonical(receipt)
def coordinates(rec,cert,x):
    A=x[rec['a']];tau=cover_weight(cert['inventory'],x)
    return sum(x),A,tau,A+tau

def hvalue(rec,cert,x):
    N,A,tau,r=coordinates(rec,cert,x);co=cert['constants']
    return B.profile(cert,r)+co['q']*F(A,(N+1)*(r+1)**2)-co['epsilon']*F(A,N+1)
def scaled_drift(rec,cert,x):
    h=hvalue(rec,cert,x);t=cert['t'];ans=F(0)
    for u,v,k in rec['channels']:
        rate=k*B.falling(x,u)
        if rate:
            xp=tuple(xx-uu+vv for xx,uu,vv in zip(x,u,v))
            ans+=rate*(t**(sum(v)-sum(u))*hvalue(rec,cert,xp)-h)
    return ans
if __name__=='__main__':
    raw=B.fixture();cc=numerical(raw,F(2))
    print(json.dumps(encode(dict(status=cc['status'],inventory=cc['inventory'],constants=cc['constants'],work=cc['work'],certificate_sha256=digest(cc))),indent=2))
