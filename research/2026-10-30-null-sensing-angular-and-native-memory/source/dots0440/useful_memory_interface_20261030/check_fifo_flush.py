#!/usr/bin/env python3
"""Exhaustive asynchronous finite-state check of one fault-free flush epoch.
Every initial packet/held response may be stale. Scheduling is arbitrary.
All packet storage is included; no hidden in-flight queue is modeled.
"""
from collections import deque
from itertools import product
import json

def words(alpha,cap):
    return [tuple(w) for n in range(cap+1) for w in product(alpha,repeat=n)]
def check(cf,cr):
    # state: master phase FS/FW/RS/RW/END, successful flush count,
    # forward FIFO, backward FIFO, Alice-held response or None.
    probes=cf+cr+2
    initial=[('FS',0,f,b,h) for f in words(('OS','OR'),cf)
             for b in words(('OA','OD'),cr) for h in (None,'OA','OD')]
    seen=set(initial);queue=deque(initial);edges=0;terminals=0;deadlocks=0
    while queue:
        phase,i,f,b,h=queue.popleft()
        if phase=='END':terminals+=1;continue
        nxt=[]
        if phase=='FS' and len(f)<cf:
            nxt.append(('FW',i,f+('NS',),b,h))
        if phase=='RS' and len(f)<cf:
            nxt.append(('RW',i,f+('NR',),b,h))
        if h is None and f:
            reply={'OS':'OA','OR':'OD','NS':'NA','NR':'ND'}[f[0]]
            nxt.append((phase,i,f[1:],b,reply))
        if h is not None and len(b)<cr:
            nxt.append((phase,i,f,b+(h,),None))
        if b:
            msg=b[0];p2=phase;i2=i
            if phase=='FW' and msg.endswith('A'):
                i2=i+1;p2='RS' if i2==probes else 'FS'
            elif phase=='RW' and msg.endswith('D'):
                assert msg=='ND',('STALE DATA ACCEPTED',cf,cr,phase,i,f,b,h)
                p2='END'
            nxt.append((p2,i2,f,b[1:],h))
        if not nxt:deadlocks+=1
        for state in nxt:
            edges+=1
            if state not in seen:seen.add(state);queue.append(state)
    assert terminals and deadlocks==0
    return {'request_capacity':cf,'response_capacity':cr,
            'sync_probes':probes,'arbitrary_initial_states':len(initial),
            'reachable_states':len(seen),'transition_edges':edges,
            'terminal_states':terminals,'deadlocks':deadlocks,
            'stale_DATA_acceptances':0}
results=[check(cf,cr) for cf,cr in ((1,1),(1,2),(2,1),(2,2),(3,3))]
print(json.dumps(results,indent=2))
