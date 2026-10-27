"""Exact independent spin-versus-triangle-dimer normalization on K4.
Enumerates this small diagnostic only; no Pfaffian compiler is implemented.
"""
from fractions import Fraction as F
from itertools import combinations,product
from functools import lru_cache
from pathlib import Path
import json
EDGES=list(combinations(range(4),2))
PORTS=[(v,w) for v in range(4) for w in range(4) if v!=w]
IDX={p:i for i,p in enumerate(PORTS)}
def check(case):
    weights={e:(F(k+2),F(k+1,k+3)) if case==0 else (F(k+1),F(2*(k+2))) for k,e in enumerate(EDGES)}
    spin=F(0)
    for s in product(range(2),repeat=4):
        term=F(1)
        for (v,w),(a,b) in weights.items():term*=a if s[v]==s[w] else b
        spin+=term
    A=[[F(0) for _ in PORTS] for _ in PORTS]
    for v in range(4):
        for u,w in combinations([q for q in range(4) if q!=v],2):
            i,j=IDX[v,u],IDX[v,w];A[i][j]=A[j][i]=1
    pref=F(1,4)
    for (v,w),(a,b) in weights.items():
        w0,w1=a+b,a-b;assert w0 and w1
        i,j=IDX[v,w],IDX[w,v];A[i][j]=A[j][i]=w0/w1;pref*=w1
    @lru_cache(None)
    def dimers(mask):
        if mask==0:return F(1)
        i=(mask&-mask).bit_length()-1;rest=mask^(1<<i);total=F(0)
        for j in range(i+1,len(PORTS)):
            if rest>>j&1 and A[i][j]:total+=A[i][j]*dimers(rest^(1<<j))
        return total
    dimer=dimers((1<<len(PORTS))-1);recovered=pref*dimer
    assert spin==recovered
    return {'signed_test':case==1,'spin_partition_exact':str(spin),'dimer_partition_exact':str(dimer),
            'prefactor_exact':str(pref),'normalization_identity':'PASS','enumerated_diagnostic_only':True}
if __name__=='__main__':
    r=[check(0),check(1)];p=Path(__file__).resolve().parent
    (p/'FISHER_CHECK.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
