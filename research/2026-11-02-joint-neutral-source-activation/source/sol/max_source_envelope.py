from fractions import Fraction as F
from collections import defaultdict
from math import prod
import mpmath as mp
import json
mp.mp.dps=60
def ff(a,b):return 0 if a<b else prod(range(a-b+1,a+1))
def falling(x,y):return prod(ff(a,b) for a,b in zip(x,y))
def mval(x):return mp.mpf(x.numerator)/x.denominator if isinstance(x,F) else mp.mpf(x)
def max_falling(x,sources):return max(falling(x,y) for y in sources)
def factorial_ratio(x,root):
    ans=F(1)
    for a,b in zip(x,root):
        if a>b:ans*=prod(range(b+1,a+1))
        elif a<b:ans/=prod(range(a+1,b+1))
    return ans
def background_ratio(x,root,sources,root_max):
    a=max_falling(x,sources);assert a>0
    return factorial_ratio(x,root)*F(root_max,a)
def actual_steps(raw,root,steps=8,alpha=F(1,2)):
    sources={tuple(y) for y,z,c in raw};assert all(tuple(z) in sources for y,z,c in raw)
    assert all(F(c)>0 and y!=z for y,z,c in raw)
    root=tuple(root);root_max=max_falling(root,sources);assert root_max>0
    mass={root:mp.mpf(1)};values={root:mp.mpf(1)};out=[]
    for step in range(1,steps+1):
        nxt=defaultdict(mp.mpf)
        for x,p in mass.items():
            rr=[F(c)*falling(x,y) for y,z,c in raw];q=sum(rr);assert q>0
            for (y,z,c),r in zip(raw,rr):
                if not r:continue
                dst=tuple(a-b+c for a,b,c in zip(x,y,z));nxt[dst]+=p*mval(r/q)
        mass=dict(nxt);assert abs(sum(mass.values())-1)<mp.mpf('1e-50')
        total=mp.mpf(0)
        for x,p in mass.items():
            if x not in values:values[x]=mp.power(mval(background_ratio(x,root,sources,root_max)),mval(alpha))
            total+=p*values[x]
        out.append({'step':step,'relative_drift':mp.nstr(total-1,30),'states':len(mass)})
    return out
def ordered(k=3,rates=None):
    C=[(0,0,0),(1,1,0)]+[(j,j-1,j-1) for j in range(2,k+1)]
    rates=[F(1)]*(k+1) if rates is None else list(map(F,rates))
    return [(C[i],C[(i+1)%(k+1)],rates[i]) for i in range(k+1)]
def adjacent(k=3):
    a=ordered(k,[1]*k+[2]);b=ordered(k,[1]*k+[3]);raw=[]
    for y,z,c in a:raw.append((tuple(y)+(0,),tuple(z)+(0,),c))
    for y,z,c in b:raw.append(((0,)+tuple(y),(0,)+tuple(z),c))
    return raw
def cycle(C,rates=None):
    rates=[F(1)]*len(C) if rates is None else list(map(F,rates))
    return [(C[i],C[(i+1)%len(C)],rates[i]) for i in range(len(C))]

if __name__=='__main__':
    from pathlib import Path
    rows=[]
    fixtures=[('ordered3',ordered(3,[1,1,1,2]),[(0,100,100),(100,0,0),(0,0,100),(1,0,100)]),('ordered4',ordered(4,[1,1,1,1,2]),[(0,100,100),(100,0,0)]),('adjacent3',adjacent(3),[(0,0,100,100),(0,0,10,1000),(100,0,0,0),(0,100,100,0)]),('ordinary_d0',cycle([(0,0),(1,1),(2,3)],[1,2,3]),[(100,1),(0,100),(100,0)])]
    for name,raw,roots in fixtures:
        for root in roots:
            ss=actual_steps(raw,root,steps=8)
            print(json.dumps({'fixture':name,'root':root,'drifts':[r['relative_drift'] for r in ss],'states':ss[-1]['states']}),flush=True)
    

