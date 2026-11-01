#!/usr/bin/env python3
"""Acquire complete concrete deletion-word coverage of a coupled hard family."""
from pathlib import Path
from collections import deque
from itertools import product
import json
from coverability_clock import cubic,le,rate_at

P=Path(__file__).resolve().parent

def find_word(raw,start,extra=6):
    queue=deque([start]);back={start:None};cap=sum(start)+extra
    found=None
    while queue:
        x=queue.popleft()
        if x!=start and le(x,start):found=x;break
        for i,(y,z,k) in enumerate(raw):
            if rate_at(x,y,k):
                out=tuple(a-u+v for a,u,v in zip(x,y,z))
                if sum(out)<=cap and out not in back:back[out]=(x,i);queue.append(out)
    if found is None:return None
    word=[];x=found
    while back[x] is not None:x0,i=back[x];word.append(i);x=x0
    return list(reversed(word)),found,len(back)

if __name__=='__main__':
    raw=cubic();rows=[]
    for start in [(1,0,0),(0,2,0),(0,0,3)]:
        word,end,searched=find_word(raw,start);assert le(end,start) and end!=start
        path=[start];x=start
        for i in word:
            y,z,k=raw[i];assert rate_at(x,y,k)>0
            x=tuple(a-u+v for a,u,v in zip(x,y,z));path.append(x)
        assert x==end
        rows.append({'source':start,'target':end,'decrement':[a-b for a,b in zip(start,end)],
                     'word':word,'path':path,'length':len(word),'max_count_overshoot':max(map(sum,path))-sum(start),
                     'BFS_states_acquired':searched})
    # The three upward cones cover every state outside this explicit head.
    # No finite enumeration is used to assert that global coverage.
    head=list(product(range(1),range(2),range(3)))
    out={'scope':'Exact full orthant deletion-word coverage for the coupled cubic diagnostic, not a stochastic recurrence proof.',
         'words':rows,'finite_uncovered_box':head,
         'coverage_proof':'Any state outside A<1,B<2,C<3 dominates one displayed axis source. Translate that entire actual word.',
         'linear_path_length_constant':max(r['length'] for r in rows),
         'uniform_count_overshoot':max(r['max_count_overshoot'] for r in rows),
         'uncontrolled_process':'Word-following probability and global weighted exits remain distinct obligations.'}
    (P/'results/deletion_words.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='words'},indent=2))
    print(json.dumps([{k:v for k,v in r.items() if k not in ['path']} for r in rows],indent=2))
