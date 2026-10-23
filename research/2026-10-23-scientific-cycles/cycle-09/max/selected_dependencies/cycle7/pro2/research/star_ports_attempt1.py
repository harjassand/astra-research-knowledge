"""Exact star-color port algebra, four colors, degree-one nonadjacent terminals.
A signature is (s,t,neighbor_s,neighbor_t,flag_s,flag_t).
No numerical optimization. State-set closure is a finite mathematical obligation.
"""
from itertools import permutations, product, combinations_with_replacement
from functools import lru_cache
from time import perf_counter
import json

PERMS=tuple(permutations(range(4)))

def canonical(s):
    d={}
    c=[]
    for x in s[:4]:
        if x not in d: d[x]=len(d)
        c.append(d[x])
    return tuple(c)+tuple(s[4:])

def recolor(s,p):
    return tuple(p[x] for x in s[:4])+tuple(s[4:])

@lru_cache(None)
def aligned(s,a,b):
    return tuple(sorted({recolor(s,p) for p in PERMS if p[s[0]]==a and p[s[1]]==b}))

@lru_cache(None)
def series_signatures(s,t):
    out=set()
    for u in {recolor(t,p) for p in PERMS if p[t[0]]==s[1]}:
        if s[3]==u[2] and (s[5] or u[4]): continue
        out.add(canonical((s[0],u[1],s[2],u[3],s[4],u[5])))
    return frozenset(out)

@lru_cache(None)
def parallel_signatures(children):
    first=children[0];c,d=first[:2]
    out=set()
    rest=[aligned(t,c,d) for t in children[1:]]
    for tail in product(*rest):
        ch=(first,)+tail
        left=[s[2] for s in ch]; right=[s[3] for s in ch]
        if any(s[4] and left.count(s[2])>1 for s in ch): continue
        if any(s[5] and right.count(s[3])>1 for s in ch): continue
        for a,b in product(range(4),repeat=2):
            if a==c or b==d:continue
            if any(s[4] and s[2]==a for s in ch):continue
            if any(s[5] and s[3]==b for s in ch):continue
            out.add(canonical((a,b,c,d,int(a in left),int(b in right))))
    return frozenset(out)

def operation(kind,types):
    out=set()
    if kind=='S':
        for s,t in product(*types):out.update(series_signatures(s,t))
    else:
        for ch in product(*types):out.update(parallel_signatures(tuple(ch)))
    return frozenset(out)

LEAF=frozenset(((0,1,2,2,0,0),(0,0,1,1,1,1)))

def closure(seconds=30, maximum_types=100):
    t0=perf_counter()
    types=[LEAF];index={LEAF:0};records=[];done=set();rounds=0
    while True:
        rounds+=1
        todo=[]
        n=len(types)
        for i,j in product(range(n),repeat=2):todo.append(('S',(i,j)))
        for b in (2,3):
            for ch in combinations_with_replacement(range(n),b):todo.append(('P',ch))
        changed=False
        for kind,ch in todo:
            key=(kind,ch)
            if key in done:continue
            out=operation(kind,tuple(types[i] for i in ch))
            done.add(key)
            if out not in index:
                index[out]=len(types);types.append(out);changed=True
                print(json.dumps({'new_type':index[out],'states':len(out),'kind':kind,'children':ch,'elapsed':perf_counter()-t0}),flush=True)
            records.append({'kind':kind,'children':ch,'output':index[out]})
            if not out:
                return {'status':'EMPTY_REACHABLE','types':[sorted(x) for x in types],'transitions':records,'elapsed':perf_counter()-t0}
            if perf_counter()-t0>seconds or len(types)>maximum_types:
                return {'status':'BUDGET_STOP','types':[sorted(x) for x in types],'transitions':records,'elapsed':perf_counter()-t0}
        if not changed:
            return {'status':'CLOSED','types':[sorted(x) for x in types],'transitions':records,'rounds':rounds,'elapsed':perf_counter()-t0}

if __name__=='__main__':
    from pathlib import Path
    r=closure()
    r['cache_sizes']={'series':series_signatures.cache_info()._asdict(),'parallel':parallel_signatures.cache_info()._asdict()}
    p=Path(__file__).resolve().parents[1]/'results'
    p.mkdir(exist_ok=True)
    (p/'star_closure_attempt1.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k not in ('types','transitions')}))

