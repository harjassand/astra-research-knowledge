from max_source_envelope import *
from functools import lru_cache
def optimal_stop(raw,root,horizon=12,alpha=F(1,2),beta=F(1,4)):
    sources={tuple(y) for y,z,c in raw};root=tuple(root);mx=max_falling(root,sources)
    logbase=sum(mp.loggamma(x+1) for x in root)-mp.log(mx)
    costscale=mp.exp((mval(beta)-mval(alpha))*logbase)
    @lru_cache(None)
    def val(x):
        return mp.power(mval(background_ratio(x,root,sources,mx)),mval(alpha))
    @lru_cache(None)
    def trans(x):
        rr=[F(c)*falling(x,y) for y,z,c in raw];q=sum(rr);assert q>0
        out=[]
        for (y,z,c),r in zip(raw,rr):
            if r:out.append((tuple(a-b+c for a,b,c in zip(x,y,z)),mval(r/q)))
        return out,mval(q)
    @lru_cache(None)
    def best(x,t):
        now=val(x)
        if t==0:return now
        tr,q=trans(x)
        cost=costscale*mp.power(now,mval(beta/alpha))*(1+1/q)
        cont=cost+sum(p*best(y,t-1) for y,p in tr)
        return min(now,cont)
    tr,q=trans(root)
    cost=costscale*(1+1/q)
    out=[]
    for h in range(1,horizon+1):
        out.append(mp.nstr(cost+sum(p*best(y,h-1) for y,p in tr)-1,30))
    return out,best.cache_info().currsize

