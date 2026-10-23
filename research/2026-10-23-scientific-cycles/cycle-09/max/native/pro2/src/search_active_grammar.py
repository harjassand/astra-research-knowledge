"""Finite exact signature-set antichain closure with full observed attempts.
Each new family is a complete attainable set for its saved expression.
Containment is used only to discharge already guaranteed outputs.
"""
from pathlib import Path
import argparse,json,time,resource,sys
from collections import Counter
from active_ports import *

def run(limit=150,time_limit=120):
    start=time.perf_counter();cpu=time.process_time()
    records=[];active=set();history=[];tested=set();checks=0
    def add(st,d,expr):
        nonlocal active
        old=[i for i in active if records[i]['degree']==d]
        if any(records[i]['states']<=st for i in old):return None
        removed=[i for i in old if st<records[i]['states']]
        active.difference_update(removed)
        idx=len(records);records.append(dict(states=st,degree=d,expression=expr))
        active.add(idx)
        history.append(dict(id=idx,degree=d,states=len(st),removed=removed,
                            elapsed_seconds=time.perf_counter()-start))
        print(json.dumps(history[-1]),flush=True)
        return idx
    add(path2(),(1,1),dict(kind='path',length=2))
    reason='closed';failure=None
    while True:
        changed=False
        candidates=[]
        for i in sorted(active):
            d=records[i]['degree']
            for k in ('L','R'):
                if admissible(k,d):candidates.append((k,i))
            for j in sorted(active):
                e=records[j]['degree']
                if admissible('S',d,e):candidates.append(('S',i,j))
                if i<=j and admissible('P',d,e):candidates.append(('P',i,j))
        for key in candidates:
            if key in tested or any(i not in active for i in key[1:]):continue
            if len(records)>=limit or time.perf_counter()-start>time_limit:
                reason='resource_limit';break
            tested.add(key);k=key[0];a=records[key[1]]
            b=records[key[2]] if len(key)==3 else None
            st=apply(k,a['states'],None if b is None else b['states']);checks+=1
            d=output_degree(k,a['degree'],None if b is None else b['degree'])
            if not st:
                reason='empty_exact_set';failure=dict(kind=k,children=list(key[1:]),degree=d)
                break
            idx=add(st,d,dict(kind=k,children=list(key[1:])))
            if idx is not None:changed=True
        if reason!='closed' or not changed:break
    body=time.perf_counter()-start
    result=dict(schema='astra-active-ports-search/v1',palette=Q,reason=reason,
                assumptions=['nonadjacent terminals','disjoint child occurrences','degree<=4'],
                basis_ids=sorted(active),records=[dict(id=i,degree=r['degree'],
                    states=[serialize(s) for s in sorted(r['states'])],expression=r['expression'])
                    for i,r in enumerate(records)],history=history,failure=failure,
                checked_transitions=checks,cost=dict(body_wall_seconds=body,
                    body_cpu_seconds=time.process_time()-cpu,
                    peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                    canonical_cache=canonical.cache_info()._asdict(),
                    scope='search excluding process startup and final JSON write'),
                limits=dict(family_records=limit,body_seconds=time_limit))
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--limit',type=int,default=150);p.add_argument('--seconds',type=float,default=120)
    a=p.parse_args();r=run(a.limit,a.seconds);Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    Path(a.output).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:r[k] for k in ['reason','basis_ids','failure','checked_transitions','cost']},indent=2))
