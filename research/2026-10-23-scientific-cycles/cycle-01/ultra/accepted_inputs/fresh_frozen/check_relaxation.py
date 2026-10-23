"""Exact scalar-relaxation checks. Does not construct physical quantum states."""
import json, math, time
from pathlib import Path
start=time.perf_counter()
rows=[]
for D,kmax in [(2,12),(3,8),(5,5)]:
    for k in range(1,kmax+1):
        T=D**k-1
        L=T-k
        assert L>=0
        checked=0
        equal=[]
        for s in range(L+1,T+1):
            # (T-s+1)/(T+1) <= D**(L-s), cross-multiplied exactly.
            lhs=(T-s+1)*D**(s-L)
            rhs=T+1
            assert lhs<=rhs,(D,k,s,lhs,rhs)
            checked+=1
            if lhs==rhs: equal.append(s)
        rows.append(dict(D=D,k=k,N=T,r=2,schmidt_rank_exponent=L,
                         entropy_over_logD=L,witness_over_logD=T,
                         gap_over_logD=k,nontrivial_s_checked=checked,
                         equality_s=equal))
receipt=dict(status='PASS',scope='exact scalar constraints; no physical realization',
             cases=len(rows),integer_comparisons=sum(x['nontrivial_s_checked'] for x in rows),
             elapsed_seconds=time.perf_counter()-start,observations=rows)
p=Path(__file__).with_name('COMPUTE_RECEIPT.json')
p.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='observations'},indent=2))
