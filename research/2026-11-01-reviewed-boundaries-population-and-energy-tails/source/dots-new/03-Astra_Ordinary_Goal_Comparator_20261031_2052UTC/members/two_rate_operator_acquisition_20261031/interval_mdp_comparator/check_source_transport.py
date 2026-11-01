#!/usr/bin/env python3
"""Source-side exact audit, not an extra observation supplied to the learner."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parent;PARENT=ROOT.parent;sys.path.insert(0,str(PARENT))
from large_routing_source import RoutingSource

class Capture:
    def __init__(self):self.rows=[]
    def multinomial(self,N,p):
        # Ideal argument-law convention: last category is remaining mass.
        q=[F(float(v)) for v in p[:-1]];q.append(1-sum(q));assert min(q)>=0
        self.rows.append(q);return np.array([N]+[0]*(len(p)-1))

def run():
    model=json.loads((PARENT/'history_sensitive_4096_result.json').read_text());n=model['n'];parts=model['partition'];r=len(parts)
    q=RoutingSource(n);q._tau=.04;which=np.zeros(n,dtype=np.int64)
    for g,p in enumerate(parts):which[p]=g
    b,e,d=q.public_task();assert (b,e,d)==(model['task_b'],model['task_ell_numer'],model['task_ell_denominator'])
    assert n==4096 and r==4 and all(len(p)==1024 for p in q._groups) and q._degree==16
    maxerr=F(0);checks=0;records=[]
    for a in range(2):
        capture=Capture();q.rng=capture;q.row_block_batch(a,1,which,r,'transport_audit')
        reset=[sum(int(which[j]==h) for j in q._reset[a]) for h in range(r)]
        group=[[sum(int(which[j]==h) for j in p) for h in range(r)] for p in q._groups]
        for i,observed in enumerate(capture.rows):
            adj=[sum(int(which[j]==h) for j in q._adj[a][i]) for h in range(r)];g=q._actions[a][int(q._which[i])]
            exact=[F(95998,100000)*F(adj[h],16)+F(4000,100000)*F(group[g][h],1024)+F(int(which[q._global[a][i]]==h),100000)+F(reset[h],100000*2048) for h in range(r)]
            assert sum(exact)==1;err=sum(abs(x-y) for x,y in zip(exact,observed));assert err<=F(1,10**9)
            maxerr=max(maxerr,err);checks+=2
        records.append(len(capture.rows))
    return {'status':'PASS_SOURCE_ARGUMENT_TRANSPORT','checks':checks,'rows_per_action':records,'max_l1_error':str(maxerr),'max_l1_float':float(maxerr),'reserve':'1/1000000000','scope':'Exact binary64 argument-law comparison for this pinned source implementation. Ideal iid multinomial/integer-draw interpretation and authentic fresh provenance remain premises; not verification of numpy PRNG distribution or physical truth. Private wiring is confined to source audit, never used for policy or hazard estimation.','source_sha256':hashlib.sha256((PARENT/'large_routing_source.py').read_bytes()).hexdigest()}
if __name__=='__main__':
    out=run();(ROOT/'source_transport_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
