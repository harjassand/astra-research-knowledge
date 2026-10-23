"""Bounded exact invariant search adding the actual odd-length path leaf.
Failure is scoped to this template search, not to graph colorability.
"""
from itertools import product, combinations_with_replacement
from pathlib import Path
from time import perf_counter,process_time
import json,resource
import star_ports as s
from finite_star_certificate import L,N

def path3_states():
    out=set()
    for a,p,q,b in product(range(4),repeat=4):
        if a==p or p==q or q==b or (a==q and p==b):continue
        out.add(s.canonical((a,b,p,q,int(q==a),int(p==b))))
    return frozenset(out)

def minimal(sets):
    sets=set(sets)
    return sorted([x for x in sets if not any(y<x for y in sets)],key=lambda x:(len(x),sorted(x)))

def run():
    t=perf_counter();cpu=process_time()
    families=minimal([frozenset(L),frozenset(N),path3_states()])
    log=[]
    while True:
        old=list(families);additions=[];cases=[]
        for kind,k in [('S',2),('P',2),('P',3)]:
            cs=product(range(len(old)),repeat=k) if kind=='S' else combinations_with_replacement(range(len(old)),k)
            for ch in cs:
                out=s.operation(kind,tuple(old[i] for i in ch))
                covers=[i for i,b in enumerate(old) if b<=out]
                cases.append({'kind':kind,'child_indices':ch,'covers':covers})
                if not covers:
                    additions.append(out)
                    log.append({'round':len(log),'kind':kind,'children':[sorted(old[i]) for i in ch],'output':sorted(out)})
                    if not out:
                        return {'status':'TEMPLATE_EMPTY','families':[sorted(x) for x in old],'log':log,'wall_seconds':perf_counter()-t}
                if perf_counter()-t>30:
                    return {'status':'BUDGET_STOP','families':[sorted(x) for x in old],'log':log,'wall_seconds':perf_counter()-t}
        if not additions:
            return {'status':'CLOSED','families':[sorted(x) for x in old],'cases':cases,'log':log,
                    'wall_seconds':perf_counter()-t,'cpu_seconds':process_time()-cpu,
                    'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024}
        families=minimal(old+additions)
        print(json.dumps({'family_sizes':[len(x) for x in families],'new_obligations':len(additions),'wall_seconds':perf_counter()-t}),flush=True)
        if len(families)>30:
            return {'status':'BUDGET_STOP','families':[sorted(x) for x in families],'log':log,'wall_seconds':perf_counter()-t}

if __name__=='__main__':
    r=run();p=Path(__file__).resolve().parents[1]/'results/path_leaf_invariant_search.json'
    p.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k not in ('families','cases','log')}))

