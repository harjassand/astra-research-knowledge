from itertools import combinations
import json

def subspaces(m):
    seen={frozenset([0])}; todo=list(seen)
    while todo:
        s=todo.pop()
        for x in range(1,1<<m):
            if x not in s:
                t=s|frozenset(x^y for y in s)
                if t not in seen:seen.add(t);todo.append(t)
    return sorted(seen,key=lambda s:(len(s),tuple(sorted(s))))

def check(m,w):
    ss=subspaces(m); planes=[s for s in ss if len(s)==4]
    full=(1<<len(planes))-1
    masks=[sum(1<<j for j,u in enumerate(planes) if len(u&s)==2)for s in ss]
    checked=0
    for inds in combinations(range(len(ss)),w):
        union=0; common=set(range(1<<m))
        for i in inds:union|=masks[i]; common.intersection_update(ss[i])
        if common!={0}:continue
        checked+=1
        if union==full:
            return {'m':m,'w':w,'subspaces':len(ss),'planes':len(planes),'jointly_injective_cases_checked':checked,'counterexample_kernels':[sorted(ss[i])for i in inds]}
    return {'m':m,'w':w,'subspaces':len(ss),'planes':len(planes),'jointly_injective_cases_checked':checked,'counterexample_kernels':None,'scope':'Exhaustive distinct kernels only. Repetition cannot add plane coverage; padding by full-space kernel covers smaller kernel collections.'}

if __name__=='__main__':
    print(json.dumps([check(3,2),check(4,3)],indent=2))
