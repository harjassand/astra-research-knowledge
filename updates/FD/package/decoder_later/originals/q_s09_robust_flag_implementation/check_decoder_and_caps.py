"""Independent component checks and acquisition failure fixtures."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
HERE=Path(__file__).resolve().parent
from shifted_ball_decoder import ShiftedBallDecoder, monomials, evaluate
from robust_learner import acquire
from run_experiment import run_case
import json
import random
import time


def main():
    start=time.perf_counter()
    cases=[]
    for n,d in ((4,1),(4,2),(5,3),(8,2),(8,3),(16,3),(32,2)):
        for seed in range(8):
            rng=random.Random(970000+1000*n+100*d+seed)
            masks=monomials(n,d)
            if n<=8:
                terms=[s for s in masks if rng.getrandbits(1)]
                # Exactly rho=1/32 where the input domain allows it; density
                # 1/64 at higher d. Nonzero deterministic errors are retained.
                bad_count=max(1,(1<<n)//(64 if d>=3 else 32))
                bad=set(rng.sample(range(1<<n),bad_count))
                rho=bad_count/(1<<n)
                if rho>=2.0**(-d-1):
                    rho=0
                    bad=set()
                def raw(x):
                    return evaluate(terms,x)^int(x in bad)
            else:
                terms=rng.sample(masks,min(25,len(masks)))
                rho=1/128
                def raw(x):
                    return evaluate(terms,x)^int((x&127)==0)
            decoder=ShiftedBallDecoder(n,d,rho,1e-6,random.Random(980000+seed))
            found=decoder.decode(raw)
            assert found==sorted(terms),(n,d,seed)
            cases.append(dict(n=n,d=d,seed=seed,rho=rho,exact_coefficients=True,
                              decoder=decoder.ledger()))
    calls=0
    def forbidden_query(x,y):
        nonlocal calls
        calls+=1
        raise AssertionError('force-zero fixture must never query')
    cap,model,comp=acquire(8,2,1/32,.05,forbidden_query,999,
                           force_zero_directions=True)
    assert model is None and cap['status']=='UNKNOWN'
    assert cap['reason']=='candidate_cap_exhausted' and calls==0
    # A budget stop is surfaced as UNKNOWN without a partially returned model.
    budget=run_case(n=8,r=2,seed=960082,mode='asymmetric_hash',
                    max_requests=10,check=False)
    assert budget['status']=='UNKNOWN' and budget['finite_result']=='UNKNOWN'
    assert budget['oracle']['logical_requests']==10
    out=dict(component_cases=cases,component_case_count=len(cases),
             force_zero_fixture=cap,request_budget_fixture=budget,
             seconds=time.perf_counter()-start,status='PASS')
    (HERE/'decoder_and_caps_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',component_case_count=len(cases),
                         force_zero_requests=calls,budget_requests=10,
                         seconds=out['seconds']),indent=2))

if __name__=='__main__':
    main()
