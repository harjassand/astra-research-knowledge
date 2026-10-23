"""Worklist closure under simulated flag bounds; every basis has a real origin.
Runs only the new loaded-port grammar. No predecessor suite or numeric solver.
"""
from pathlib import Path
from collections import Counter
import argparse,heapq,json,time,resource
from monotone_ports import *

def run(limit,time_limit,resume=None):
    start=time.perf_counter();cpu=time.process_time()
    records=[];active=set();history=[];heap=[];queued=set();tested=[];checks=0
    def queue(key):
        if key in queued:return
        queued.add(key);k=key[0];a=records[key[1]];b=records[key[2]] if len(key)==3 else None
        if not admissible(k,a['degree'],None if b is None else b['degree']):return
        cost=len(a['states'])*(1 if b is None else len(b['states']))
        heapq.heappush(heap,(cost,len(key),key))
    def add(st,d,expr):
        old=[i for i in active if records[i]['degree']==d]
        if any(covers(st,records[i]['states']) for i in old):return None
        removed=[i for i in old if covers(records[i]['states'],st)]
        active.difference_update(removed)
        idx=len(records);records.append(dict(states=st,degree=d,expression=expr));active.add(idx)
        history.append(dict(id=idx,degree=d,states=len(st),removed=removed,elapsed_seconds=time.perf_counter()-start))
        print(json.dumps(history[-1]),flush=True)
        for k in ('L','R'):queue((k,idx))
        for j in sorted(active):
            queue(('S',idx,j));queue(('S',j,idx));queue(('P',min(idx,j),max(idx,j)))
        return idx
    if resume:
        prior=json.loads(Path(resume).read_text())
        records=[dict(states=frozenset(map(deserialize,r['states'])),degree=tuple(r['degree']),expression=r['expression']) for r in prior['records']]
        active=set(prior['basis_ids']);history=prior['history'][:]
        tested=[tuple(t) for t in prior['tested_transitions']];queued=set(tested)
        for i in sorted(active):
            for k in ('L','R'):queue((k,i))
            for j in sorted(active):
                queue(('S',i,j))
                if i<=j:queue(('P',i,j))
    else:add(reduce(path2()),(1,1),dict(kind='path',length=2))
    reason='closed';failure=None
    while heap:
        if len(records)>=limit or time.perf_counter()-start>time_limit:
            reason='resource_limit';break
        _,_,key=heapq.heappop(heap)
        if any(i not in active for i in key[1:]):continue
        tested.append(key);k=key[0];a=records[key[1]];b=records[key[2]] if len(key)==3 else None
        st=reduce(apply(k,a['states'],None if b is None else b['states']));checks+=1
        d=output_degree(k,a['degree'],None if b is None else b['degree'])
        if not st:
            reason='empty_simulation_complete_set';failure=dict(kind=k,children=list(key[1:]),degree=d);break
        add(st,d,dict(kind=k,children=list(key[1:])))
    body=time.perf_counter()-start
    result=dict(schema='astra-monotone-ports-search/v1',palette=Q,reason=reason,
      basis_ids=sorted(active),records=[dict(id=i,degree=r['degree'],states=[serialize(s) for s in sorted(r['states'])],expression=r['expression']) for i,r in enumerate(records)],
      history=history,failure=failure,checked_transitions=checks,tested_transitions=tested,
      resumed_from=resume,
      remaining_queue=len(heap),cost=dict(body_wall_seconds=body,body_cpu_seconds=time.process_time()-cpu,
        peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
        scope='search, excluding startup and final result serialization'),
      limits=dict(family_records=limit,body_seconds=time_limit))
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--limit',type=int,default=2500);p.add_argument('--seconds',type=float,default=120)
    p.add_argument('--resume')
    a=p.parse_args();r=run(a.limit,a.seconds,a.resume);Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    Path(a.output).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:r[k] for k in ['reason','failure','checked_transitions','remaining_queue','cost']},indent=2))
