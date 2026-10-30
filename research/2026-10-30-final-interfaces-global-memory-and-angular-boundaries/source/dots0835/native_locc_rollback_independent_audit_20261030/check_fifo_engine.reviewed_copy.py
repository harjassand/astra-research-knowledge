"""Finite FIFO regression with one live native Alice engine.
Abstracts only path existence, preserving pending READ across clean abort and
forbidding dequeue of a new request or enqueue of held reply before engine I.
"""
from itertools import product
from collections import deque
from pathlib import Path
import json
# State (phase,count,requestqueue,responsequeue,worker,engine)
# worker idle / ('request', provenance) / ('hold',kind,provenance)
# engine ('I',None), ('A'/'C'/'B',provenance), ('Q',None)
def successors(s,cap):
    m,c,req,resp,w,e=s;G=2*cap+1
    def put(mm=m,cc=c,r=req,z=resp,ww=w,ee=e):return (mm,cc,r,z,ww,ee)
    if m=='FS' and len(req)<cap:yield put(mm='FW',r=req+(('S','new'),)),'send_sync'
    if m=='RS' and len(req)<cap:yield put(mm='RW',r=req+(('R','new'),)),'send_read'
    if resp:
        (kind,prov),rest=resp[0],resp[1:]
        if m=='FW' and kind=='ACK':
            cc=c+1;yield put(mm='RS' if cc==G+1 else 'FS',cc=cc,z=rest),'receive_ack'
        elif m=='RW' and kind=='DATA':yield put(mm='OK_'+prov,z=rest),'receive_data'
        else:yield put(z=rest),'discard_response'
    if e[0]=='I':
        if w[0]=='idle' and req:
            (kind,prov),rest=req[0],req[1:]
            ww=('hold','ACK',prov) if kind=='S' else ('request',prov)
            yield put(r=rest,ww=ww),'process_request'
        if w[0]=='hold' and len(resp)<cap:yield put(z=resp+((w[1],w[2]),),ww=('idle',)),'enqueue_response'
        if w[0]=='request':yield put(ee=('A',w[1])),'load_read'
    if e[0]=='A':yield put(ee=('C',e[1])),'acquire_commit'
    if e[0]=='C':
        yield put(ee=('Q',None),ww=('hold','DATA',e[1])),'read_terminal'
        yield put(ee=('B',e[1])),'watchdog_to_rollback'
    if e[0]=='B':yield put(ee=('Q',None)),'rollback_reset'
    if e[0]=='Q':yield put(ee=('I',None)),'cleanup_ready'
    if e[0] in {'I','A','Q'}:yield put(ee=('Q',None)),'watchdog_safe_reset'
results=[]
for cap in [1,2]:
    reqs=[q for n in range(cap+1) for q in product([('S','old'),('R','old')],repeat=n)]
    resps=[q for n in range(cap+1) for q in product([('ACK','old'),('DATA','old')],repeat=n)]
    workers=[('idle',),('request','old'),('hold','ACK','old'),('hold','DATA','old')]
    engines=[('I',None),('Q',None)]+[(x,'old') for x in ['A','C','B']]
    initial=[('FS',0,r,z,w,e) for r,z,w,e in product(reqs,resps,workers,engines)]
    seen=set(initial);dq=deque(initial);edges=0;oldok=0;dead=0;reverse={}
    while dq:
        s=dq.popleft()
        if s[0]=='OK_old':oldok+=1
        nxt=list(successors(s,cap));edges+=len(nxt)
        progress=[x for x in nxt if x[0]!=s]
        if not s[0].startswith('OK') and not progress:dead+=1
        for ss,kind in nxt:
            reverse.setdefault(ss,[]).append(s)
            if ss not in seen:seen.add(ss);dq.append(ss)
    assert oldok==0 and dead==0,(cap,oldok,dead)
    # Existence of good finite paths from every reachable state, not fairness.
    reachable=set(s for s in seen if s[0]=='OK_new');dq=deque(reachable)
    while dq:
        s=dq.popleft()
        for prev in reverse.get(s,[]):
            if prev not in reachable:reachable.add(prev);dq.append(prev)
    assert reachable==seen,(cap,len(seen-reachable))
    results.append({'capacity_each':cap,'initial_states':len(initial),'reachable_states':len(seen),'transitions':edges,'accepted_stale_data':oldok,'nonterminal_dead_states':dead,'every_state_has_fresh_success_path':True})
# Explicit wrong implementation: if HOLD may enqueue during C, old held+live reply
# are two potential ghosts, so the claimed G=Creq+Cresp+1 inventory is false.
out={'results':results,'critical_rules':['worker pending READ retained across rollback','reply enqueue and new request process require engine I','unconditional Bob receive in every master phase'],'scope':'classical FIFO/engine path abstraction, not quantum amplitudes or full Bob instrument'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
