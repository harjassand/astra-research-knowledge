#!/usr/bin/env python3
"""Independent exact receiver for the multipartite-seed research certificate.
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
FAMILY='multipartite-fast-seed-two-energy-v1'
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
    satellites=tuple(i for i in range(n) if i!=a)
    graph={i:set() for i in satellites}
    for i,j in hubs.values():graph[i].add(j);graph[j].add(i)
    remaining=set(satellites);parts=[]
    while remaining:
        root=min(remaining);queue=deque([root]);part={root}
        while queue:
            v=queue.popleft()
            for w in satellites:
                if w!=v and w not in graph[v] and w not in part:part.add(w);queue.append(w)
        remaining-=part;parts.append(tuple(sorted(part)))
    if len(parts)<2:raise Outside('hub graph must be complete multipartite with at least two parts; no isolated passengers')
    for part in parts:
        for j,i in enumerate(part):
            for w in part[j+1:]:
                if w in graph[i]:raise Outside('nonadjacency is not a partition: missing multipartite cross edges')
    for u in range(len(parts)):
        for v in range(u+1,len(parts)):
            if any(j not in graph[i] for i in parts[u] for j in parts[v]):raise Outside('missing multipartite cross edge')
    forward={i:F(0) for i in satellites};rows=[]
    for h,pair in sorted(hubs.items()):
        if (two,h) not in table or (h,two) not in table:raise Outside('every hub needs 2A amplification pair')
        arms=[]
        for x in satellites:
            ax=tuple(int(i==a)+int(i==x) for i in range(n))
            if (ax,h) in table:
                arms.append((x,table[ax,h],table[h,ax]));forward[x]+=table[ax,h]
        rows.append({'complex':h,'edge':pair,'to_hub':table[two,h],'to_two_a':table[h,two],
                     'reverse_sum':table[h,two]+sum((r for _,_,r in arms),F(0)),'arms':tuple(arms)})
    if min(forward.values())<=0:raise Outside('each satellite needs a forward/reverse arm')
    bmin=min(row['to_two_a'] for row in rows);asum=sum((row['to_hub'] for row in rows),F(0))
    work={'input_rows':len(raw),'normalized_channels':len(channels),'raw_coordinate_checks':coords,
      'internal_complex_checks':2*len(internal),'reverse_edge_tests':len(internal),
      'complement_pair_tests':(n-1)**2,'within_part_pair_tests':sum(len(p)*(len(p)-1)//2 for p in parts),
      'cross_part_pair_tests':sum(len(parts[i])*len(parts[j]) for i in range(len(parts)) for j in range(i+1,len(parts))),
      'amplification_edge_tests':2*len(hubs),'arm_incidence_tests':len(hubs)*(n-1)}
    return {'n':n,'a':a,'lam':table[zero,one],'mu':table[one,zero],'channels':channels,'internal':internal,
      'parts':tuple(parts),'hubs':tuple(rows),'kX':tuple(sorted(forward.items())),
      'kminus':min(forward.values()),'kplus':max(forward.values()),'a_sum':asum,'bmin':bmin,
      'smax':max(row['reverse_sum'] for row in rows),'b0':min(row['reverse_sum']+row['to_two_a'] for row in rows),
      'F0':2*asum+max(forward.values()),'S':sum((k for _,_,k in internal),F(0)),
      'raw_sha256':fingerprint(channels),'work':work}

def qual_from_record(r):
    work=dict(r['work']);work.update(numerical_formula_blocks=0,profile_recurrence_steps=0,states_enumerated=0,
      stationary_fiber_laws=0,expanded_Foster_powers=0)
    return {'status':'CERTIFIED_QUALITATIVE','family':FAMILY,'raw_sha256':r['raw_sha256'],
      'conclusion':'irreducible positive recurrence; every finite exponential stationary total-count moment',
      'role':{'dimension':r['n'],'open_coordinate':r['a'],'immigration':r['lam'],'death':r['mu']},
      'inventory':{'parts':r['parts'],'formula':'R=N-max(part totals); P=(1+eta)R-eta*A'},'hubs':r['hubs'],'work':work}

def qualitative(raw):
    try:return qual_from_record(parse(raw))
    except Outside as e:return {'status':'UNKNOWN','family':FAMILY,'reason':str(e),'stability':'UNKNOWN'}

def bitmax(value):
    if type(value) is F:return max(abs(value.numerator).bit_length(),value.denominator.bit_length())
    if type(value) is int:return abs(value).bit_length()
    if isinstance(value,dict):return max([0]+[bitmax(v) for v in value.values()])
    if isinstance(value,(tuple,list)):return max([0]+[bitmax(v) for v in value])
    return 0

def numerical(raw,t):
    t=exact(t)
    if t<=1:raise ValueError('t>1 required')
    try:r=parse(raw)
    except Outside as e:return {'status':'UNKNOWN','family':FAMILY,'reason':str(e),'stability':'UNKNOWN'}
    eta=r['bmin']/(16*r['smax']);c0=min(eta*r['kminus']/3,r['bmin']/4);gamma=c0/(1+eta)
    D=r['mu']*(1-1/t);eps=min(F(1,2),D/(4*r['F0']));B=2*r['lam']*(t-1)+5*r['mu']
    delta=min(F(1,4),gamma/(2*(1+eta)*(B+6*r['S']+1)))
    kap=delta/8*min(D,eps*r['b0']/len(r['parts']));Cint=B+6*r['S']/delta**2
    Nstar=max(1,ceiling((Cint+1)/kap));zeta=min(F(1),r['lam'])/2;H=4*t
    cf=(zeta+r['lam']+r['mu']*Nstar+r['S']*Nstar**2)*H
    out={'status':'CERTIFIED_NUMERICAL','family':FAMILY,'raw_sha256':r['raw_sha256'],'t':t,'qualitative':qual_from_record(r),
      'constants':{'parts':len(r['parts']),'kminus':r['kminus'],'kplus':r['kplus'],'a_sum':r['a_sum'],
        'bmin':r['bmin'],'smax':r['smax'],'b0':r['b0'],'F0':r['F0'],'S':r['S'],'eta':eta,'c0':c0,'gamma':gamma,
        'D':D,'epsilon':eps,'B':B,'delta':delta,'kappa':kap,'Cint':Cint,'Nstar':Nstar,'zeta':zeta,'H':H},
      'profile':{'active':'1+1/P-epsilon*A/(N+1)','inactive':H,'P':'(1+eta)R-eta*A'},
      'Foster':{'coefficient':cf,'base':t,'exponent':Nstar+1,'inequality':'LW<=-zeta*W+coefficient*base^exponent*1_{N<Nstar}'},
      'stationary_moment':{'coefficient':2*cf/zeta,'base':t,'exponent':Nstar+1},
      'implicit_head_states':{'binomial_top':Nstar+r['n']-1,'binomial_choose':r['n']},
      'work':{'numerical_formula_blocks':14,'profile_recurrence_steps':0,'rate_dependent_iterations':0,
        'states_enumerated':0,'stationary_fiber_laws':0,'expanded_Foster_powers':0},
      'cost_scope':'14 named scalar formula blocks after finite raw scans; not14 machine operations; polynomial-bit factored outputs, no service resource cap'}
    out['work']['retained_scalar_bits']=bitmax(out)
    return out

def receive_qualitative(raw,receipt):return canon(qualitative(raw))==canon(receipt)
def receive_numerical(raw,t,receipt):return canon(numerical(raw,t))==canon(receipt)

def coordinates(r,x):
    N=sum(x);A=x[r['a']];totals=tuple(sum(x[i] for i in p) for p in r['parts']);M=max(totals)
    return N,A,M,N-M,totals

def h(r,cert,x):
    N,A,M,R,totals=coordinates(r,x)
    if R==0:return cert['constants']['H']
    P=(1+cert['constants']['eta'])*R-cert['constants']['eta']*A
    return 1+1/P-cert['constants']['epsilon']*F(A,N+1)

def propensity(x,u,rate):
    for xi,ui in zip(x,u):
        if xi<ui:return F(0)
        for j in range(ui):rate*=xi-j
    return rate

def verify_master(r,cert,x):
    N,A,M,R,z=coordinates(r,x);c=cert['constants'];old=h(r,cert,x);t=cert['t']
    assert F(1,2)<=old<=c['H']
    P=(1+c['eta'])*R-c['eta']*A;total=inv=la=F(0);jumps=ties=0
    dominant=z.index(M) if 2*R<N else None
    for u,v,k in r['channels']:
        rate=propensity(x,u,k)
        if not rate:continue
        y=tuple(a-b+d for a,b,d in zip(x,u,v));NN,AA,MM,RR,zz=coordinates(r,y)
        total+=rate*(t**(NN-N)*h(r,cert,y)-old)
        if NN==N:
            PP=(1+c['eta'])*RR-c['eta']*AA
            assert R>=1 and RR>=1 and PP>=1
            assert abs(PP-P)<=1+2*c['eta'] and abs(1/PP-1/P)<=6/P**2
            inv+=rate*(1/PP-1/P);la+=rate*(AA-A);jumps+=1
            if dominant is not None:
                assert z.count(M)==1 and zz[dominant]==MM
                if zz.count(MM)>1:ties+=1
    if R==0:
        assert jumps==0 and total==r['lam']*(t*(2-c['epsilon']/F(N+2))-c['H'])
        assert total<=-r['lam']*old/2
    else:
        assert old<=2;Q=sum(z[i]*z[j] for i in range(len(z)) for j in range(i+1,len(z)))
        assert la>=c['b0']*Q-c['F0']*A*N
        assert inv<=6*c['S']*F(N*N)/P**2
        if 2*R<N:assert inv<=-c['gamma']*(N-R)/P+6*c['S']
        master=c['B']+inv-c['D']*A/4-c['epsilon']*c['b0']*Q/F(N+1)
        assert total<=master
        if R<=c['delta']*N:assert total<=-1
        if N>=c['Nstar']:assert total<=-c['zeta']*old
    if N<c['Nstar']:assert total+c['zeta']*old<=cert['Foster']['coefficient']*t
    return total,jumps,ties
