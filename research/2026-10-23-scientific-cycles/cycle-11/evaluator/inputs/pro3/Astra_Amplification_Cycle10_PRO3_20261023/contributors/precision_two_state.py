#!/usr/bin/env python3
"""New exact diagnostic only; B=log(4), alpha=1/2, n=64 frozen in source."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,resource,time
from datetime import datetime,timezone

def run():
    cpu0,wall0=time.process_time(),time.monotonic()
    t,alpha,n=F(2),F(1,2),64
    q=[t/(1+t),1/(1+t)]
    target=[1/(1+t),t/(1+t)]
    G=[[1-q[1],q[1]],[q[0]/(t*t),1-q[0]/(t*t)]]
    C=[[(1-alpha/2)*int(i==j)+(alpha/2)*G[i][j] for j in range(2)] for i in range(2)]
    law=q[:]
    for _ in range(n): law=[sum(law[i]*C[i][j] for i in range(2)) for j in range(2)]
    eigenvalue=1-alpha/(2*t)
    formula=[target[i]+eigenvalue**n*(q[i]-target[i]) for i in range(2)]
    tv=sum(abs(law[i]-q[i]) for i in range(2))/2
    predicted=(t-1)/(t+1)*(1-eigenvalue**n)
    assert all(sum(row)==1 for row in G+C)
    assert target[0]*C[0][1]==target[1]*C[1][0]
    assert law==formula and tv==predicted
    def s(x): return f'{x.numerator}/{x.denominator}'
    result={'inputs':{'t':s(t),'B':'log(4)','alpha':s(alpha),'n':n,'Q':'identity','true_pi_equals_q':True,'true_KL':'0'},
            'q':[s(x) for x in q],'computed_target':[s(x) for x in target],
            'G':[[s(x) for x in row] for row in G],'C':[[s(x) for x in row] for row in C],
            'law':[s(x) for x in law],'TV':s(tv),'stationary_bias':'1/3','eigenvalue':s(eigenvalue),
            'checks_pass':True,'scope':'Exact diagnostic for the stated CHANGED target-evaluation contract, not a native exact-target failure',
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'recorded_utc':datetime.now(timezone.utc).isoformat(),
            'cpu_seconds':time.process_time()-cpu0,'wall_seconds':time.monotonic()-wall0,
            'peak_RSS_KiB_linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'inference_cost':None,'total_discovery_cost':None}
    p=Path(__file__).with_name('PRECISION_TWO_STATE_RESULT.json')
    if p.exists(): raise RuntimeError('Refusing to overwrite prior result')
    p.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': run()
