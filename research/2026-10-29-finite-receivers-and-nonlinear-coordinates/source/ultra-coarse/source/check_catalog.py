"""Exact native adsorption-component/rank controls, not a fitted fixture."""
import hashlib,json,time
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent


def main():
    tic=time.perf_counter();m=json.loads((HERE/'MODEL.json').read_text())
    ads=[p for p in m['native_processes'] if p['group']==1]
    assert len(ads)==2
    for typ,p in enumerate(ads):
        assert p['conditions']==[[typ,0,0,0]]
        assert p['actions']==[[typ,0,0,1]]
    assert ads[0]['rate']==ads[1]['rate']>0
    checks=[]
    for M in range(1,5):
        D=3**M;A=s.zeros(D,D)
        for col in range(D):
            for i in range(M):
                if (col//(3**i))%3==0:
                    A[col+3**i,col]+=1;A[col,col]-=1
        assert all(sum(A[:,j])==0 for j in range(D))
        rank=A.rank();assert rank==3**M-2**M
        checks.append(dict(sites=M,dimension=D,exact_rank=int(rank)))
    out=dict(status='PASS literal single-site native adsorption rules and exact integer component ranks',
       controls=checks,rank_at_actual32_sites=3**32-2**32,
       microscopic_configurations_at32_sites=3**32,
       theorem_scope='allM rank=3^M-2^M from fixedO-pattern pure-birth blocks, proof separate; no stationary source law assumed',
       seconds=time.perf_counter()-tic,
       native_model_sha256=hashlib.sha256((HERE/'MODEL.json').read_bytes()).hexdigest())
    (HERE/'CATALOG_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))


if __name__=='__main__':main()
