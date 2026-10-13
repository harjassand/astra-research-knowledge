"""Exact geometric-gap Majorana algebra on the infinite translation quotient.
Prototype: finite-range hopping and diagonal interactions, fixed finite degree.
Geometric series are never spatially truncated. Contact branches are finite.
"""

if not __debug__:
    raise RuntimeError('Do not run with Python -O: certificate checks must execute.')
from fractions import Fraction as F
from collections import defaultdict
from itertools import product
from functools import lru_cache
from pressure_basis import geo,ip,val
import separable_repair as sr

# Atom: (site types, gap sequences); type 1=a,2=b,3=ab.
def atom(types,gaps):
    types=tuple(types);gaps=tuple(gaps)
    if not types or len(gaps)!=len(types)-1 or any(t not in (1,2,3) for t in types):raise ValueError('Invalid atom')
    if sum(2 if t==3 else 1 for t in types)%2:raise ValueError('Odd total Majorana parity')
    return types,gaps

def clean(f):return {a:F(c) for a,c in f.items() if c}
def add(*terms):
    out=defaultdict(F)
    for s,f in terms:
        for a,c in f.items():out[a]+=s*c
    return clean(out)
def scale(f,s):return {a:c*s for a,c in f.items() if c*s}
def pop(f):return {a:c for a,c in f.items() if all(t==3 for t in a[0])}
def off(f):return {a:c for a,c in f.items() if any(t!=3 for t in a[0])}
def degree(a):return sum(2 if t==3 else 1 for t in a[0])//2

def damping(f,d=F(2),power=1):
    out={}
    for a,c in f.items():
        s=d*sum(t!=3 for t in a[0])/2
        if s:out[a]=c*s**power
    return out

@lru_cache(None)
def atom_inner(a,b):
    if a[0]!=b[0]:return F(0)
    return sr.product_f(ip(u,v) for u,v in zip(a[1],b[1]))
def inner(f,g):
    groups=defaultdict(list)
    for a,c in g.items():groups[a[0]].append((a,c))
    return sum(c*C*atom_inner(a,b) for a,c in f.items() for b,C in groups[a[0]])

def parity(a):
    k=degree(a);nb=sum(t in (2,3) for t in a[0])
    return (-1)**(k+nb)

def from_word(w,c=F(1)):
    sites=sorted(set(i//2 for i in w));types=[]
    for x in sites:types.append(sum(1<<(i%2) for i in w if i//2==x))
    return {atom(types,[geo(0,b-a-1) for a,b in zip(sites,sites[1:])]):F(c)}
def current(t=F(1)):
    return {atom((1,1),(geo(0),)):-t/2,atom((2,2),(geo(0),)):-t/2}

def split_seq(s,K):
    a,q=s
    if q==0 or a>=K:return [(F(1),s)]
    return [(q**(j-a),geo(0,j)) for j in range(a,K)]+[(q**(K-a),geo(q,K))]

def position_add(p,c):return (p[0]+c,)+p[1:]
def psub(a,b):return tuple(x-y for x,y in zip(a,b))
def plus(a,b):return tuple(x+y for x,y in zip(a,b))

def branch_column(types,gaps,t,densities,part):
    vars=[q for a,q in gaps if q]; nv=len(vars);x=(0,)*(nv+1);positions=[x];v=0
    for a,q in gaps:
        dx=[a+1]+[0]*nv
        if q:dx[v+1]=1;v+=1
        x=plus(x,tuple(dx));positions.append(x)
    I=tuple(sorted((p,j) for p,ty in zip(positions,types) for j in range(2) if ty&(1<<j)))
    templates=[]
    if part in('all','hop'):
        templates += [(((0,1),(1,0)),t/2),(((0,0),(1,1)),-t/2)]
    if part in('all','diag'):
        for X,hc in densities:
            templates.append((tuple((a,j) for a in X for j in (0,1)),hc*(-1)**len(X)))
    out=defaultdict(F)
    for temp,hc in templates:
        starts=set(position_add(p,-a) for p,j in I for a,k in temp if j==k)
        for start in starts:
            H=tuple(sorted((position_add(start,a),j) for a,j in temp))
            overlap=len(set(H)&set(I))
            if overlap%2==0:continue
            R=tuple(sorted(set(H)^set(I)))
            inv=sum(a>b for a in H for b in I)
            power=((len(H)*(len(H)-1)+len(I)*(len(I)-1)-len(R)*(len(R)-1))//2+2*inv)%4
            if power not in(1,3):raise AssertionError('Non-real Hermitian commutator')
            factor=2 if power==1 else -2
            P=sorted(set(p for p,j in R));ty=[]
            for p in P:ty.append(sum(1<<j for q,j in R if q==p))
            gs=[];used=[]
            for p,q in zip(P,P[1:]):
                diff=psub(q,p);a=diff[0]-1;active=[j for j,c in enumerate(diff[1:]) if c]
                if a<0 or any(c not in (0,1) for c in diff[1:]) or len(active)>1:
                    raise AssertionError(('Nonseparable local branch',diff))
                if active:gs.append(geo(vars[active[0]],a));used+=active
                else:gs.append(geo(0,a))
            if sorted(used)!=list(range(nv)):raise AssertionError('Lost/duplicated free gap')
            out[atom(ty,gs)]+=hc*factor
    return clean(out)

@lru_cache(None)
def column(a,t=F(1),densities=(),part='all'):
    types,gaps=a
    K=max([2]+[max(X)-min(X)+1 for X,hc in densities])
    out=defaultdict(F)
    branches=[split_seq(s,K) for s in gaps]
    for branch in product(*branches):
        coef=sr.product_f(c for c,s in branch)
        gs=tuple(s for c,s in branch)
        for b,c in branch_column(types,gs,t,densities,part).items():out[b]+=coef*c
    return clean(out)

def apply(f,t=F(1),densities=(),part='all'):
    out=defaultdict(F)
    for a,c in f.items():
        for b,C in column(a,t,densities,part).items():out[b]+=c*C
    return clean(out)

def lift_routes(routes,t=F(1)):
    # Every physical route step moves particle j+1 LEFT.
    out=defaultdict(F);k=len(routes)+1
    for j,field in enumerate(routes):
        for gaps,c in field.items():
            for typ in (1,2):
                types=(3,)*j+(typ,typ)+(3,)*(k-j-1)
                gs=gaps[:j]+(geo(0),)+gaps[j:]
                out[atom(types,gs)]-=c/(2*t)
    return clean(out)

def repair(b,t=F(1),reference=F(0)):
    groups=defaultdict(lambda:defaultdict(F))
    for (types,gaps),c in b.items():
        if any(ty!=3 for ty in types):raise ValueError('Source is not diagonal')
        groups[len(types)][gaps]+=c
    out={}
    for k,source in groups.items():
        source=sr.clean(source)
        if k==1:
            if sr.mass(source):raise ValueError('Nonzero degree-one source')
            continue
        flow=sr.complete(source,[geo(reference)]*(k-1))
        out=add((1,out),(1,lift_routes(sr.route_edges(flow),t)))
    return out

def balance(f,t=F(1),reference=F(0)):
    b=pop(apply(f,t,part='hop'))
    return add((1,f),(-1,repair(b,t,reference)))

def certificate(f,g,t=F(1),d=F(2),densities=()):
    J=current(t);Af=apply(f,t,densities);Ag=apply(g,t,densities)
    if any(parity(a)!=-1 for a in f) or any(parity(a)!=1 for a in g):raise ValueError('Wrong parity')
    bp=pop(Af)
    if inner(bp,bp):raise ValueError('Population imbalance')
    Sf=damping(f,d);Sg=damping(g,d);v=add((1,J),(-1,Ag))
    lo=2*inner(J,f)-inner(f,Sf)-inner(Af,damping(Af,d,-1))
    hi=inner(v,damping(v,d,-1))+inner(g,Sg)
    r1=add((1,Sf),(-1,J),(1,Ag));r2=add((1,Sg),(1,Af))
    gap=inner(r1,damping(r1,d,-1))+inner(r2,damping(r2,d,-1))
    assert hi-lo==gap
    return 4*lo,4*hi,dict(f_atoms=len(f),g_atoms=len(g),Af_atoms=len(Af),Ag_atoms=len(Ag),gap=str(4*gap))

if __name__=='__main__':
    import reference_majorana as ref,random,json,time
    from pathlib import Path
    st=time.perf_counter();rng=random.Random(10013);checks=0
    dens=(((0,1),F(1)),((0,2),F(1,4)))
    for _ in range(40):
        w=tuple(sorted(rng.sample(range(12),rng.choice((2,4,6)))))
        f=from_word(w);observed=apply(f,F(1),dens)
        target={}
        for ww,c in ref.column(w,F(1),dens).items():target=add((1,target),(1,from_word(ww,c)))
        r=add((1,observed),(-1,target));assert inner(r,r)==0;checks+=1
    J=current();r=apply(J,part='hop');assert inner(r,r)==0
    assert inner(J,J)==F(1,2)
    source={(geo(0),geo(0,1)):F(1),(geo(0,1),geo(0)):F(-1)}
    bb={atom((3,3,3),g):c for g,c in source.items()}
    lifted=repair(bb);r=add((1,pop(apply(lifted,part='hop'))),(-1,bb));assert inner(r,r)==0
    # Truly infinite tails; test skewness, contact branching, and repair.
    f={atom((3,1,1,3),(geo(F(1,2)),geo(0),geo(F(1,3)))):F(1),
       atom((3,2,2,3),(geo(F(1,2)),geo(0),geo(F(1,3)))):F(1)}
    ff=balance(f,reference=F(1,4));p=pop(apply(ff,part='hop'));assert inner(p,p)==0
    for h in (J,f,ff):
        Ah=apply(h,F(1),dens);assert inner(h,Ah)==0
        assert inner(J,Ah)==-inner(apply(J,F(1),dens),h)
    lo,hi,meta=certificate(scale(J,F(2,9)),scale(apply(J,F(1),dens),F(-1,9)),densities=dens)
    out=dict(finite_commutator_checks=checks,infinite_repair_exact=True,
      infinite_input_atoms=len(f),balanced_atoms=len(ff),
      exact_skew_tests=6,transport_fixture_lower=str(lo),transport_fixture_upper=str(hi),
      seconds=time.perf_counter()-st,certificate=meta,
      scope='Exact algebra/certificate tests, not a uniformly compressed full solver')
    Path('gap_algebra_checks.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
