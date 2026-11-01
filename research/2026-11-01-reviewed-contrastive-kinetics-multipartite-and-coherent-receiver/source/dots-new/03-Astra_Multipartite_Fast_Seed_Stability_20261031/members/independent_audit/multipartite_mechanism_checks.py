#!/usr/bin/env python3
"""Exact local mathematical controls; no constructor, web, or accepted-code imports."""
from fractions import Fraction as F
from itertools import product
import json

def ceiling(x):return -(-x.numerator//x.denominator)
def encode(x):
    if type(x) is F:return str(x)
    if isinstance(x,dict):return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [encode(v) for v in x]
    return x

def fixture(parts,t=F(2),varied=False,sparse=False):
    n=1+sum(map(len,parts));assert sorted(i for p in parts for i in p)==list(range(1,n))
    def z(*ids):return tuple(ids.count(i) for i in range(n))
    hubs=[z(i,j) for u in range(len(parts)) for v in range(u+1,len(parts)) for i in parts[u] for j in parts[v]]
    lam=F(2,3) if varied else F(1);mu=F(5,4) if varied else F(1)
    raw=[(z(),z(0),lam),(z(0),z(),mu)]
    for j,h in enumerate(hubs):
        raw.extend([(z(0,0),h,F(j+2,3) if varied else F(1)),(h,z(0,0),F(j+3,2) if varied else F(1))])
    for x in range(1,n):
        for j,h in enumerate(hubs):
            if sparse and j!=(x-1)%len(hubs):continue
            raw.extend([(z(0,x),h,F(x+j+1,4) if varied else F(1)),(h,z(0,x),F(x+2*j+2,5) if varied else F(1))])
    return {'raw':raw,'t':t,'n':n,'parts':parts,'lam':lam,'mu':mu}

def acquire_parts(raw):
    n=len(raw[0][0]);sat=set(range(1,n));hubs={u for u,v,k in raw if sum(u)==2 and u[0]==0}
    edges={tuple(i for i,z in enumerate(h) if z) for h in hubs}
    assert all(len(e)==2 for e in edges)
    assert set().union(*map(set,edges))==sat
    missing={i:set() for i in sat}
    for i in sat:
        for j in sat:
            if i!=j and tuple(sorted((i,j))) not in edges:missing[i].add(j)
    unseen=set(sat);parts=[]
    while unseen:
        todo=[min(unseen)];seen=set(todo)
        while todo:
            i=todo.pop()
            for j in missing[i]-seen:seen.add(j);todo.append(j)
        for i in seen:assert missing[i]==seen-{i}
        unseen-=seen;parts.append(tuple(sorted(seen)))
    assert len(parts)>=2
    assert edges=={tuple(sorted((i,j))) for u in range(len(parts)) for v in range(u+1,len(parts)) for i in parts[u] for j in parts[v]}
    return tuple(parts)

def constants(f):
    raw=f['raw'];n=f['n'];t=f['t'];parts=acquire_parts(raw);table={(u,v):k for u,v,k in raw}
    aa=(2,)+(0,)*(n-1)
    hubs=sorted({u for u,v,k in raw if sum(u)==2 and u[0]==0})
    kX={x:sum((k for u,v,k in raw if u[0]==1 and u[x]==1 and sum(u)==2 and v[0]==0),F(0)) for x in range(1,n)}
    a=sum(table[aa,h] for h in hubs);b={h:table[h,aa] for h in hubs};s={h:sum((k for u,v,k in raw if u==h),F(0)) for h in hubs}
    bmin=min(b.values());smax=max(s.values());eta=bmin/(16*smax)
    c0=min(eta*min(kX.values())/3,bmin/4);gamma=c0/(1+eta)
    S=sum(k for u,v,k in raw if sum(u)==sum(v));F0=2*a+max(kX.values());b0=min(s[h]+b[h] for h in hubs)
    D=f['mu']*(1-1/t);eps=min(F(1,2),D/(4*F0));B=2*f['lam']*(t-1)+5*f['mu']
    delta=min(F(1,4),gamma/(2*(1+eta)*(B+6*S+1)))
    kap=delta/8*min(D,eps*b0/len(parts));Nstar=ceiling((B+6*S/delta**2+1)/kap)
    return dict(parts=parts,hubs=hubs,kX=kX,a=a,b=b,s=s,bmin=bmin,smax=smax,eta=eta,c0=c0,gamma=gamma,
                S=S,F0=F0,b0=b0,D=D,epsilon=eps,B=B,delta=delta,kappa=kap,Nstar=Nstar,zeta=min(F(1),f['lam'])/2,H=4*t)

def geom(x,co):
    z=[sum(x[j] for j in p) for p in co['parts']];N=sum(x);R=N-max(z);P=(1+co['eta'])*R-co['eta']*x[0]
    return N,R,P,z

def h(x,f,co):
    N,R,P,z=geom(x,co)
    return 4*f['t'] if R==0 else 1+1/P-co['epsilon']*F(x[0],N+1)

def propensity(x,u,k):
    for a,b in zip(x,u):
        if a<b:return F(0)
        for j in range(b):k*=a-j
    return k

def check(x,f,co):
    N,R,P,z=geom(x,co);A=x[0];old=h(x,f,co);full=F(0);lintinv=F(0);lintA=F(0);internal=0;ties=0
    assert old>=F(1,2) and old<=co['H']
    dominant=(max(range(len(z)),key=z.__getitem__) if 2*R<N else None)
    for u,v,k in f['raw']:
        rate=propensity(x,u,k)
        if not rate:continue
        y=tuple(a-b+c for a,b,c in zip(x,u,v));NN,RR,PP,zz=geom(y,co)
        full+=rate*(f['t']**(NN-N)*h(y,f,co)-old)
        if sum(u)==sum(v):
            assert R>=1 and RR>=1 and PP>=1
            assert abs(PP-P)<=1+2*co['eta']
            assert abs(1/PP-1/P)<=6/P**2
            lintinv+=rate*(1/PP-1/P);lintA+=rate*(y[0]-A);internal+=1
            if dominant is not None:
                assert z.count(max(z))==1
                assert zz[dominant]==max(zz)
                if zz.count(max(zz))>1:ties+=1
                expected=(1+co['eta'])*(z[dominant]-zz[dominant])-co['eta']*(y[0]-A)
                assert PP-P==expected
    if R==0:
        assert internal==0 and full<=-f['lam']*old/2
    else:
        Q=sum(z[i]*z[j] for i in range(len(z)) for j in range(i+1,len(z)))
        assert lintA>=co['b0']*Q-co['F0']*A*N
        assert lintinv<=6*co['S']*F(N*N,1)/P**2
        if 2*R<N:assert lintinv<=-co['gamma']*(N-R)/P+6*co['S']
        master=co['B']+lintinv-co['D']*A/4-co['epsilon']*co['b0']*Q/F(N+1)
        assert full<=master
        if R<=co['delta']*N:assert full<=-1
        if N>=co['Nstar']:assert full<=-co['zeta']*old
    return internal,ties

def main():
    fixtures=[('triangle',fixture([(1,),(2,),(3,)]),4),
      ('K211_sparse',fixture([(1,2),(3,),(4,)],varied=True,sparse=True),3),
      ('K4_sparse',fixture([(1,),(2,),(3,),(4,)],t=F(101,100),sparse=True),3),
      ('K22',fixture([(1,2),(3,4)],t=F(5),varied=True),3),
      ('K11',fixture([(1,),(2,)],varied=True,t=F(3,2)),4)]
    out=[];states=jumps=ties=targeted=0
    for name,f,cap in fixtures:
        co=constants(f);count=jumpcount=tiecount=0
        for x in product(range(cap),repeat=f['n']):
            j,ti=check(x,f,co);count+=1;jumpcount+=j;tiecount+=ti
        targets=set()
        for mass in [co['Nstar'],10**50]:
            for a in [0,1,2,5]:
                for small in [0,1,2,10]:
                    x=[0]*f['n'];x[0]=a
                    for p in co['parts']:x[p[0]]=small
                    x[co['parts'][0][0]]+=mass;targets.add(tuple(x))
            for a in [0,1,mass]:
                x=[0]*f['n'];x[0]=a
                for p in co['parts']:x[p[0]]=mass
                targets.add(tuple(x))
        for x in targets:j,ti=check(x,f,co);jumpcount+=j;tiecount+=ti
        states+=count;jumps+=jumpcount;ties+=tiecount;targeted+=len(targets)
        out.append({'case':name,'parts':co['parts'],'ordinary_states':count,'targeted_states':len(targets),
          'Nstar':co['Nstar'],'eta':co['eta'],'epsilon':co['epsilon'],'delta':co['delta']})
    # Exact scope counterexample: free passenger not among any part.
    t=F(2);eta=F(1,16);eps=F(1,4);n=10**50
    before=1+1/((1+eta)*n)
    after=1+1/((1+eta)*n+1)-eps/F(n+2)
    lower=t*after-before
    assert lower>F(9,10)
    return {'status':'pending mechanism exact checks passed','cases':out,'ordinary_states':states,
      'targeted_states':targeted,'enabled_internal_jumps':jumps,'boundary_destination_ties':ties,
      'free_passenger_negative_control':{'count':n,'scaled_birth_drift':lower,'strictly_greater_than':'9/10'},
      'scope':'No web; no frozen whole-source acceptance; exact finite tests supplement the ordinary inequalities.'}
if __name__=='__main__':print(json.dumps(encode(main()),sort_keys=True,indent=2))
