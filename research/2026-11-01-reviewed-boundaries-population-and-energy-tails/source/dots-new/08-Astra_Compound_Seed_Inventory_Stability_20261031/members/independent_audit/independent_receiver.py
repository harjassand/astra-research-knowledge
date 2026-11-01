#!/usr/bin/env python3
"""Independent exact receiver for the compound-seed research certificate.
No import of the proposed constructor. No stationary-fiber or Lyapunov oracle.
The wire contract is exact canonical JSON, not a hostile-input service.
Import deliberately disables CPython's process-wide decimal conversion guard;
this is trusted research code, not a bit/time/memory cap.
"""
from fractions import Fraction
from collections import deque
import hashlib, json, sys
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
F=Fraction
FAMILY='biclique-compound-seed-active-phase-v1'
class Outside(ValueError): pass

def exact(x):
    if type(x) not in (int,F):raise TypeError('exact int/Fraction required')
    return F(x)
def wire(x):
    if type(x) is F:return str(x)
    if isinstance(x,dict):return {str(k):wire(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [wire(v) for v in x]
    return x
def canon(x):return json.dumps(wire(x),sort_keys=True,separators=(',',':'))
def fingerprint(x):return hashlib.sha256(canon(x).encode()).hexdigest()
def ceiling(x):return (x.numerator+x.denominator-1)//x.denominator

def parse(raw):
    if type(raw) not in (list,tuple) or not raw:raise ValueError('nonempty raw list')
    table={};n=None;coords=0
    for triple in raw:
        if type(triple) not in (list,tuple) or len(triple)!=3:raise ValueError('reaction triple')
        s,t,k=triple
        if type(s) not in (list,tuple) or type(t) not in (list,tuple):raise TypeError('complex vectors')
        if n is None:n=len(s)
        if n<3 or len(s)!=n or len(t)!=n:raise ValueError('fixed dimension n>=3')
        for q in list(s)+list(t):
            coords+=1
            if type(q) is not int or q<0:raise ValueError('nonnegative exact integer counts')
        k=exact(k)
        if k<=0:raise ValueError('strictly positive rate')
        s,t=tuple(s),tuple(t)
        if s!=t:table[s,t]=table.get((s,t),F(0))+k
    channels=tuple((s,t,k) for (s,t),k in sorted(table.items()))
    zero=(0,)*n
    changing=[(s,t,k) for s,t,k in channels if sum(s)!=sum(t)]
    candidates=[]
    for j in range(n):
        ej=tuple(int(i==j) for i in range(n))
        if len(changing)==2 and {(s,t) for s,t,_ in changing}=={(zero,ej),(ej,zero)}:candidates.append(j)
    if len(candidates)!=1:raise Outside('requires one exact reversible port')
    a=candidates[0];one=tuple(int(i==a) for i in range(n));two=tuple(2*int(i==a) for i in range(n))
    internal=tuple(row for row in channels if sum(row[0])==sum(row[1]))
    hubs={}
    for s,t,_ in internal:
        for x in (s,t):
            if sum(x)!=2:raise Outside('only binary nonnull internals')
            occupied=[i for i,q in enumerate(x) if q]
            if x[a]==0:
                if len(occupied)!=2 or any(x[i]!=1 for i in occupied):raise Outside('hub must be square-free satellite pair')
                hubs[x]=tuple(occupied)
            elif x==two:pass
            elif x[a]==1:
                other=[i for i in occupied if i!=a]
                if len(other)!=1 or x[other[0]]!=1:raise Outside('active complex must be A+X')
            else:raise Outside('unrecognized active complex')
    if not hubs:raise Outside('at least one hub required')
    for s,t,_ in internal:
        if (s in hubs)==(t in hubs):raise Outside('only hub/active edges')
        if (t,s) not in table:raise Outside('every included edge must be reversible')
    graph={}
    for i,j in hubs.values():
        graph.setdefault(i,set()).add(j);graph.setdefault(j,set()).add(i)
    colors={};parts=[]
    for root in sorted(graph):
        if root in colors:continue
        colors[root]=0;queue=deque([root]);block=[]
        while queue:
            v=queue.popleft();block.append(v)
            for w in sorted(graph[v]):
                if w not in colors:colors[w]=1-colors[v];queue.append(w)
                elif colors[w]==colors[v]:raise Outside('hub graph has an odd cycle')
        left=tuple(sorted(v for v in block if colors[v]==0));right=tuple(sorted(v for v in block if colors[v]==1))
        if any(j not in graph[i] for i in left for j in right):raise Outside('hub component is not complete bipartite')
        parts.append((left,right))
    sat=[i for i in range(n) if i!=a];forward={i:F(0) for i in sat};rows=[]
    for h,pair in sorted(hubs.items()):
        if (two,h) not in table or (h,two) not in table:raise Outside('every hub needs 2A amplification pair')
        arms=[]
        for x in sat:
            ax=tuple(int(i==a)+int(i==x) for i in range(n))
            if (ax,h) in table:
                arms.append((x,table[ax,h],table[h,ax]));forward[x]+=table[ax,h]
        rows.append({'complex':h,'edge':pair,'to_hub':table[two,h],'to_two_a':table[h,two],
                     'reverse_sum':table[h,two]+sum((r for _,_,r in arms),F(0)),'arms':tuple(arms)})
    if min(forward.values())<=0:raise Outside('each satellite needs a forward/reverse arm')
    bmin=min(row['to_two_a'] for row in rows);asum=sum((row['to_hub'] for row in rows),F(0))
    work={'input_rows':len(raw),'normalized_channels':len(channels),'raw_coordinate_checks':coords,
          'internal_complex_checks':2*len(internal),'reverse_edge_tests':len(internal),
          'hub_graph_edge_visits':2*len(hubs),'biclique_cross_tests':sum(len(l)*len(r) for l,r in parts),
          'amplification_edge_tests':2*len(hubs),'arm_incidence_tests':len(hubs)*(n-1)}
    return {'n':n,'a':a,'lam':table[zero,one],'mu':table[one,zero],'channels':channels,'internal':internal,
      'components':tuple(parts),'free':tuple(x for x in sat if x not in graph),'hubs':tuple(rows),
      'kX':tuple(sorted(forward.items())),'kminus':min(forward.values()),'kplus':max(forward.values()),
      'a_sum':asum,'Kf':asum+2*max(forward.values()),'beta':bmin/(2*len(parts)),
      'sratio':max(row['reverse_sum']/row['to_two_a'] for row in rows),
      'S':sum((k for _,_,k in internal),F(0)),'raw_sha256':fingerprint(channels),'work':work}

def qual_from_record(r):
    w=dict(r['work']);w.update(profile_recurrence_steps=0,finite_head_checks=0,stationary_fiber_laws=0,states_enumerated=0,expanded_Foster_powers=0)
    return {'status':'CERTIFIED_QUALITATIVE','family':FAMILY,'raw_sha256':r['raw_sha256'],
      'conclusion':'irreducible positive recurrence; every finite exponential stationary total-count moment',
      'role':{'dimension':r['n'],'open_coordinate':r['a'],'immigration':r['lam'],'death':r['mu']},
      'inventory':{'bicliques':r['components'],'free_satellites':r['free']},'hubs':r['hubs'],'work':w}

def qualitative(raw):
    try:return qual_from_record(parse(raw))
    except Outside as e:return {'status':'UNKNOWN','family':FAMILY,'reason':str(e),'stability':'UNKNOWN'}

def bitmax(value):
    if type(value) is F:return max(abs(value.numerator).bit_length(),value.denominator.bit_length())
    if type(value) is int:return abs(value).bit_length()
    if isinstance(value,dict):return max([0]+[bitmax(v) for v in value.values()])
    if isinstance(value,(tuple,list)):return max([0]+[bitmax(v) for v in value])
    return 0

def numerical(raw,t,budget=100000):
    t=exact(t)
    if t<=1:raise ValueError('t>1 required')
    if type(budget) is not int or budget<0:raise ValueError('iteration budget')
    try:r=parse(raw)
    except Outside as e:return {'status':'UNKNOWN','family':FAMILY,'reason':str(e),'stability':'UNKNOWN'}
    lam,mu=r['lam'],r['mu'];beta=r['beta'];Kf=r['Kf'];L=lam*(t-1)
    eps=min(F(1),(lam+beta)/2);c=4*(L+eps)/beta;K=max(2,ceiling(2*c))
    D=mu*(1-1/t);J=max(K+1,2,ceiling(4*c*(mu+Kf+beta)/D))
    base={'family':FAMILY,'raw_sha256':r['raw_sha256'],'t':t,'qualitative':qual_from_record(r),
          'budget':{'profile_head_iteration_limit':budget,'required_iterations':K+J-2,
          'scope':'only backward recurrence and finite head scan iterations; not bits/input/total arithmetic/time'}}
    if K+J-2>budget:
        return dict(base,status='NUMERICAL_UNKNOWN',reason='profile/head iteration budget exceeded',
                    preflight={'K':K,'J':J},work={'profile_recurrence_steps':0,'finite_head_checks':0})
    head=[None]*(K+1);head[K]=1+c/K
    for i in reversed(range(1,K)):
        denominator=lam+beta*i*i-eps;assert denominator>0
        head[i]=head[i+1]*(lam*t+beta*i*i)/denominator
    head[0]=2*t*head[1]
    def g(i):return head[i] if i<=K else 1+c/i
    def diff(i):return g(i)-g(i+1)
    dstar=min([c]+[(i+1)**2*diff(i) for i in range(1,K)])
    assert dstar>0 and all(head[i]>head[i+1] for i in range(K))
    best=F(0);arg=None
    for i in range(1,J):
        E=mu*(g(i-1)/t-g(i))+Kf*i*diff(i-1)+2*beta*i*diff(i)
        z=4*(i+1)**2*max(E,F(0))/r['kminus']
        if z>best:best=z;arg=i
    q=1+best;Ce=11*Kf+12*lam*t+12*mu
    threshold=max(F(1),F(4*J),q,22*q*r['sratio']/dstar,2*q*Ce/eps);Nstar=ceiling(threshold)
    zeta=min(lam,eps)/4;H=head[0]+q/4;coefficient=(zeta+lam+mu*Nstar+r['S']*Nstar*Nstar)*H
    out=dict(base,status='CERTIFIED_NUMERICAL',constants={'beta':beta,'Kf':Kf,'kminus':r['kminus'],
      'kplus':r['kplus'],'sratio':r['sratio'],'L':L,'epsilon':eps,'c':c,'K':K,'D':D,'J':J,'dstar':dstar,
      'q':q,'q_argmax':arg,'Ce':Ce,'Nstar':Nstar,'zeta':zeta,'H':H,'S':r['S']},
      profile={'head':tuple(head),'tail':'1+c/r for r>=K'},
      Foster={'coefficient':coefficient,'base':t,'exponent':Nstar+1,
        'inequality':'LW <= -zeta W + coefficient*base^exponent*1_{N<Nstar}'},
      stationary_moment={'coefficient':coefficient/zeta,'base':t,'exponent':Nstar+1},
      implicit_head_states={'binomial_top':Nstar+r['n']-1,'binomial_choose':r['n']},
      work={'profile_recurrence_steps':K-1,'finite_head_checks':J-1,'profile_values_retained':K+1,
        'infinite_tail_checks':1,'states_enumerated':0,'stationary_fiber_laws':0,'expanded_Foster_powers':0})
    out['work']['retained_scalar_bits']=bitmax(out)
    return out

def receive_qualitative(raw,receipt):return canon(qualitative(raw))==canon(receipt)
def receive_numerical(raw,t,receipt,budget=100000):return canon(numerical(raw,t,budget))==canon(receipt)

def inventory(r,x):
    return x[r['a']]+sum(min(sum(x[i] for i in l),sum(x[j] for j in u)) for l,u in r['components'])
def gvalue(cert,k):
    if k<=cert['constants']['K']:return cert['profile']['head'][k]
    return 1+cert['constants']['c']/k

def h(r,cert,x):
    total=sum(x);k=inventory(r,x)
    return gvalue(cert,k)+cert['constants']['q']*F(x[r['a']],(total+1)*(k+1)**2)

def propensity(x,u,rate):
    for xi,ui in zip(x,u):
        if xi<ui:return F(0)
        for j in range(ui):rate*=xi-j
    return rate

def drift(r,cert,x):
    total=F(0);old=h(r,cert,x)
    for u,v,rate in r['channels']:
        q=propensity(x,u,rate)
        if q:
            y=tuple(xi-ui+vi for xi,ui,vi in zip(x,u,v))
            total+=q*(cert['t']**(sum(v)-sum(u))*h(r,cert,y)-old)
    return total

def verify_master(r,cert,x):
    """Full generator and every finite-count algebra join; no power t^N expansion."""
    a=x[r['a']];N=sum(x);R=inventory(r,x);co=cert['constants'];q=co['q'];t=cert['t']
    H=h(r,cert,x);assert 1<=H<=co['H']
    full=drift(r,cert,x)
    f=F(a,(R+1)**2);core_correction=F(0)
    for u,v,rate in r['channels']:
        if sum(u)==sum(v):continue
        rate=propensity(x,u,rate)
        if rate:
            y=tuple(xi-ui+vi for xi,ui,vi in zip(x,u,v));NY=sum(y);RY=inventory(r,y)
            core_correction+=q*rate*(t**(NY-N)*F(y[r['a']],(NY+1)*(RY+1)**2)-f/F(N+1))
    assert core_correction<=q*(12*r['lam']*t+12*r['mu'])/F(N+1)
    if N<co['Nstar']:
        # Conservative factored-head bound, without evaluating t^Nstar.
        assert full+co['zeta']*H<=cert['Foster']['coefficient']*t
    if R==0:
        expected=r['lam']*(t*gvalue(cert,1)-gvalue(cert,0))+q*r['lam']*t/F(4*(N+2))
        assert full==expected
    else:
        gr=gvalue(cert,R);dm=gvalue(cert,R-1)-gr;dp=gr-gvalue(cert,R+1)
        f=F(a,(R+1)**2);lintf=lintg=F(0);reverse=F(0);btotal=F(0)
        for u,v,rate in r['internal']:
            rate=propensity(x,u,rate)
            if not rate:continue
            y=tuple(xi-ui+vi for xi,ui,vi in zip(x,u,v));rr=inventory(r,y)
            change=F(y[r['a']],(rr+1)**2)-f
            assert abs(change)<=F(11,(R+1)**2)
            lintf+=rate*change;lintg+=rate*(gvalue(cert,rr)-gr)
        for row in r['hubs']:
            i,j=row['edge'];reverse+=row['reverse_sum']*x[i]*x[j];btotal+=row['to_two_a']*x[i]*x[j]
        assert lintf<=-r['kminus']*a*F(N-2*R+a,(R+1)**2)+F(11,(R+1)**2)*(r['Kf']*R*R+reverse)
        assert lintg<=r['Kf']*a*R*dm-btotal*dp
        assert btotal>=2*co['beta']*(R-a)**2
        if N+1>=22*q*r['sratio']/co['dstar']:
            E=r['mu']*(gvalue(cert,R-1)/t-gr)+r['Kf']*R*dm+2*co['beta']*R*dp
            master=-co['epsilon']*gr+a*E-q*r['kminus']*a*F(N-2*R+a,(N+1)*(R+1)**2)+q*co['Ce']/F(N+1)
            assert full<=master
    if N>=co['Nstar']:assert full<=-co['zeta']*H
    return full
