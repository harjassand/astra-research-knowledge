#!/usr/bin/env python3
"""Exact population-model checks; no measured/acquisition-precision claims."""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import hashlib, json

def zero(n, m=None):
    return [[F(0) for _ in range(n if m is None else m)] for _ in range(n)]

def solve(a,b):
    n,m=len(a),len(b[0]); z=[list(a[i])+list(b[i]) for i in range(n)]
    for j in range(n):
        p=next(i for i in range(j,n) if z[i][j]); z[j],z[p]=z[p],z[j]
        q=z[j][j]; z[j]=[v/q for v in z[j]]
        for i in range(n):
            if i!=j:
                q=z[i][j]; z[i]=[x-q*y for x,y in zip(z[i],z[j])]
    return [r[n:n+m] for r in z]

def rowmul(v,a):
    return [sum(v[i]*a[i][j] for i in range(len(v))) for j in range(len(a[0]))]

def normalize(v):
    return [x/sum(v) for x in v]

def stationary(p):
    n=len(p)
    a=[[p[i][j]-F(i==j) for i in range(n)] for j in range(n-1)]+[[F(1)]*n]
    return [r[0] for r in solve(a,[[F(0)]]*(n-1)+[[F(1)]])]

def invariant(p,mu,balanced=True):
    assert all(sum(row)==1 and min(row)>=0 for row in p)
    assert rowmul(mu,p)==list(mu)
    if balanced:
        assert all(mu[i]*p[i][j]==mu[j]*p[j][i] for i in range(len(p)) for j in range(len(p)))

def hitting(p,target):
    n=len(p); target=list(target); outside=[i for i in range(n) if i not in target]
    a=[[F(i==j)-p[i][j] for j in outside] for i in outside]
    b=[[p[i][j] for j in target] for i in outside]; h=zero(n)
    for j in target: h[j][j]=F(1)
    for i,row in zip(outside,solve(a,b)):
        for j,v in zip(target,row): h[i][j]=v
    return h

def repair(p,labels,w,prechoose=False):
    n=len(p); k=zero(n)
    h={y:hitting(p,[i for i in range(n) if labels[i]==y]) for y in set(labels)}
    for i in range(n):
        for j in range(n):
            a=1/w[i] if prechoose else min(F(1),w[j]/w[i])
            k[i][j]+=p[i][j]*a
            for z in range(n): k[i][z]+=p[i][j]*(1-a)*h[labels[i]][j][z]
    return k

def marked(p,w):
    n=len(p); a=[v/max(w) for v in w]
    lhs=[[F(i==j)-p[i][j]*(1-a[j]) for j in range(n)] for i in range(n)]
    rhs=[[p[i][j]*a[j] for j in range(n)] for i in range(n)]
    return solve(lhs,rhs),[r[0] for r in solve(lhs,[[F(1)]]*n)]

def compile_paths(p,is_b,horizon):
    """Literal physical controller recursion, no block-polynomial formula."""
    n=len(p); cap=max(horizon); r=sum(F(h)*v for h,v in horizon.items())
    residual={ell:sum(v for h,v in horizon.items() if h>ell)/r for ell in range(cap)}
    @lru_cache(None)
    def until_b(x,remaining):
        ep,occ=[F(0)]*n,[F(0)]*n
        if not remaining: ep[x]=F(1); return tuple(ep),tuple(occ)
        occ[x]=F(1)
        for y,prob in enumerate(p[x]):
            if is_b[y]: ep[y]+=prob
            else:
                e,o=until_b(y,remaining-1)
                for j in range(n): ep[j]+=prob*e[j]; occ[j]+=prob*o[j]
        return tuple(ep),tuple(occ)
    k,o=zero(n),zero(n)
    for x in range(n):
        if not is_b[x]:
            for h,prob in horizon.items():
                e,v=until_b(x,h)
                for j in range(n): k[x][j]+=prob*e[j]; o[x][j]+=prob*v[j]
        else:
            o[x][x]=F(1)
            for y,prob in enumerate(p[x]):
                if is_b[y]: k[x][y]+=prob
                else:
                    for ell,pl in residual.items():
                        e,v=until_b(y,ell)
                        for j in range(n): k[x][j]+=prob*pl*e[j]; o[x][j]+=prob*pl*v[j]
    return k,o

def counter_paths(p, weights, direction):
    """Root's general phase compiler, using the minimum-weight stride."""
    n=len(p); maximum=max(weights); stride=min(weights); cap=(maximum+stride-1)//stride
    @lru_cache(None)
    def walk(x,c,left):
        assert left>0
        phase=1+((c-1+direction*stride)%maximum)
        ep,occ=[F(0)]*n,[F(0)]*n; occ[x]=F(1)
        for y,prob in enumerate(p[x]):
            if not prob: continue
            if phase<=weights[y]: ep[y]+=prob
            else:
                a,b=walk(y,phase,left-1)
                for j in range(n): ep[j]+=prob*a[j]; occ[j]+=prob*b[j]
        return tuple(ep),tuple(occ)
    k,o=zero(n),zero(n)
    for x in range(n):
        for c in range(1,weights[x]+1):
            ep,occ=walk(x,c,cap)
            for j in range(n): k[x][j]+=ep[j]/weights[x]; o[x][j]+=occ[j]/weights[x]
    return k,o,cap

def trim(v):
    v=list(v)
    while len(v)>1 and not v[-1]: v.pop()
    return tuple(v)

def add(a,b):
    return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])

@lru_cache(None)
def trees(depth):
    if not depth: return (None,)
    p=trees(depth-1); return (None,)+tuple((a,b) for a in p for b in p)

@lru_cache(None)
def poly(tree,parity):
    if tree is None: return (F(parity),)
    a,b=poly(tree[0],parity),poly(tree[1],1-parity)
    return add(add(a,(F(0),)+tuple(-x for x in a)),(F(0),)+b)

def holdlength(tree):
    return 0 if tree is None else 1+holdlength(tree[0])

def peval(coeff,p):
    ans=F(0)
    for c in reversed(coeff): ans=ans*p+c
    return ans

def main():
    out={}
    p=[[F(1,2),F(1,4),F(1,4),F(0)], [F(1,4),F(1,2),F(0),F(1,4)],
       [F(1,4),F(0),F(1,2),F(1,4)], [F(0),F(1,4),F(1,4),F(1,2)]]
    mu=[F(1,4)]*4; labels=[0,0,1,2]; w=[F(3),F(3),F(2),F(1)]
    nu=normalize([a*b for a,b in zip(mu,w)]); invariant(p,mu)
    wrong=repair(p,labels,w)
    expected=[[F(5,9),F(5,18),F(1,6),F(0)], [F(11,36),F(11,18),F(0),F(1,12)],
              [F(1,4),F(0),F(5,8),F(1,8)], [F(0),F(1,4),F(1,4),F(1,2)]]
    assert wrong==expected
    drift=[a-b for a,b in zip(rowmul(nu,wrong),nu)]; assert drift==[F(1,108),F(-1,108),0,0]
    stat=stationary(wrong); assert stat==[F(x,529) for x in (183,168,120,58)]
    vtv=(abs(stat[0]+stat[1]-nu[0]-nu[1])+abs(stat[2]-nu[2])+abs(stat[3]-nu[3]))/2
    htv=sum(abs(a-b) for a,b in zip(stat,nu))/2
    assert vtv==F(22,4761) and htv==F(82,4761)
    out['multilabel_failure']=dict(kernel=wrong,target=nu,drift=drift,actual=stat,visible_tv=vtv,hidden_tv=htv)
    trace=repair(p,labels,w,True); invariant(trace,nu)
    mark,calls=marked(p,w); invariant(mark,nu)
    mean=sum(x*y for x,y in zip(nu,calls)); assert mean==F(4,3)
    out['ordinary_exact']=dict(trace=trace,marked=mark,marked_calls=calls,marked_mean=mean)
    bw=[F(1),F(1),F(4),F(4)]; bn=normalize([a*b for a,b in zip(mu,bw)])
    binary=repair(p,[0,0,1,1],bw); invariant(binary,bn); out['binary_hidden_repair']=binary
    gw=[F(4),F(4),F(3),F(2)]; gamma=F(3,7); z=sum(a*b for a,b in zip(mu,gw)); q=zero(8); rho=[]
    for i in range(4):
        rho.extend([mu[i]/z,mu[i]*(gw[i]-1)/z])
        for j in range(4):
            if i!=j: q[2*i][2*j]=p[i][j]
        q[2*i][2*i+1]=gamma*(1-1/gw[i]); q[2*i+1][2*i]=gamma/gw[i]
    for i in range(8): q[i][i]=-sum(q[i])
    assert rowmul(rho,q)==[0]*8
    assert all(rho[i]*q[i][j]==rho[j]*q[j][i] for i in range(8) for j in range(8))
    out['physical_gate']=dict(generator=q,stationary=rho)
    hm=[F(1,8),F(3,8),F(1,6),F(1,3)]; hp=zero(4); isb=[False,False,True,True]
    for i in range(4):
        for j in range(4):
            if i!=j: hp[i][j]=F(i+j+1,100)/hm[i]
        hp[i][i]=1-sum(hp[i])
    invariant(hp,hm); assert sum(hp[0][2:])!=sum(hp[1][2:])
    # Include a directed native cycle: stationarity, not reversibility, suffices.
    directed=[[F(i==((j-1)%4)) for j in range(4)] for i in range(4)]
    fixtures=[]
    for native,base,bal in ((hp,hm,True),(directed,mu,False)):
        invariant(native,base,bal)
        for horizons in ({4:F(1)},{2:F(1,2),3:F(1,2)},{1:F(1)}):
            r=sum(F(h)*v for h,v in horizons.items()); z=sum(m*(r if b else 1) for m,b in zip(base,isb))
            target=[m*(r if b else 1)/z for m,b in zip(base,isb)]
            endpoint,occ=compile_paths(native,isb,horizons); invariant(endpoint,target,bal)
            occupancy=rowmul(target,occ); assert occupancy==[r*m/z for m in base]
            c=[sum(row) for row in occ]; assert all(1<=v<=max(horizons) for v in c)
            assert sum(x*y for x,y in zip(target,c))==r/z
            fixtures.append(dict(native_reversible=bal,horizon=horizons,target=target,kernel=endpoint,calls=c,mean=r/z,occupation=occupancy))
    out['root_literal_path_checks']=dict(reversible_native=hp,baseline=hm,fixtures=fixtures)
    counter_fixtures=[]
    for native,base,bal in ((hp,hm,True),(directed,mu,False)):
        for weights in ([2,3,5,7],[1,2,4,8],[2,2,4,4]):
            z=sum(m*w for m,w in zip(base,weights)); target=[m*w/z for m,w in zip(base,weights)]
            plus,po,cap=counter_paths(native,weights,1); minus,mo,_=counter_paths(native,weights,-1)
            invariant(plus,target,False); invariant(minus,target,False)
            for kernel,occupation in ((plus,po),(minus,mo)):
                occ=rowmul(target,occupation); assert occ==[max(weights)*m/z for m in base]
                assert sum(occ)==max(weights)/z
            mixed=[[(a+b)/2 for a,b in zip(ra,rb)] for ra,rb in zip(plus,minus)]
            invariant(mixed,target,bal)
            if bal:
                assert all(target[i]*plus[i][j]==target[j]*minus[j][i] for i in range(4) for j in range(4))
            counter_fixtures.append(dict(native_reversible=bal,weights=weights,cap=cap,target=target,plus=plus,minus=minus,stationary_calls=max(weights)/z))
    out['general_counter_checks']=counter_fixtures
    tt=[(a,b) for a in trees(3) for b in trees(3)]; groups={}
    for tree in tt:
        f=poly(tree,0); d=f[1]; assert d==holdlength(tree) and 1<=d<=4
        groups.setdefault(tuple(v/d for v in f),[]).append(d)
        for p0 in (F(1,17),F(1,4),F(1,2),F(3,4),F(16,17)):
            assert 0<=peval(f,p0)<=1-(1-p0)**4
    ratio=max(max(v)/min(v) for v in groups.values()); assert len(tt)==676 and ratio==4
    out['sharp_cap']=dict(trees=len(tt),cap=4,polynomial_classes=len(groups),largest_ratio=ratio)
    means=[3*a/(1-a+3*a) for a in (F(1,4),F(3,4))]; assert means==[F(1,2),F(9,10)]
    eps=F(1,100); trap=[[F(1,2),F(1,2),F(0)],[eps,1-2*eps,eps],[F(0),eps/(1-2*eps),1-eps/(1-2*eps)]]
    tm=[eps,F(1,2),F(1,2)-eps]; invariant(trap,tm)
    tc=[1+trap[i][1]/(2*eps) for i in (0,2)]; av=(tm[0]*tc[0]+tm[2]*tc[1])/F(1,2)
    assert tc[0]==26 and av==2
    out['scope_examples']=dict(sector_means=means,unchanged_mix=sum(means)/2,global_tilt=F(3,4),trace_calls=tc,trace_stationary_mean=av)
    dest=Path(__file__).with_name('PHYSICAL_SUPPLIER_CHECK_RESULTS.json'); dest.write_text(json.dumps(out,default=str,indent=2)+'\n')
    print('Exact checks passed: repair failure, binary hidden repair, trace, marked acceptance, gate,')
    print('six excursion and six general counter fixtures including irreversible native dynamics, cost/occupation,')
    print('all 676 mandatory-call stopping trees at cap4, and conserved-class/transient-cost examples.')
    print('Results SHA256:',hashlib.sha256(dest.read_bytes()).hexdigest())

if __name__=='__main__': main()
