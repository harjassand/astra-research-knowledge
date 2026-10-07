#!/usr/bin/env python3
"""Exact negative guards for projection compiler interfaces."""
from fractions import Fraction as Q
from math import comb
from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256
import json


def main():
    x=Q(16,25);m,r,b=3,2,0
    z=sum((Q(comb(r,t)**2,comb(m,b+t))*x**t*(1-x)**(r-t) for t in range(r+1)),Q(0))
    false=sum((Q(comb(r,t),comb(m,b+t))*x**t*(1-x)**(r-t) for t in range(r+1)),Q(0))
    assert z==Q(43,75) and false==Q(787,1875) and z!=false
    # Every m_i=1 projection is the identity, so the success mass must be1.
    M,k,u=6,2,2
    count=comb(M,k)*comb(M-k,u)
    false_mass=Q(count,comb(M,k)*comb(M,u))
    assert count==90 and false_mass==Q(2,5)!=1
    # A rank-two projection in a three-dimensional diagonal toy example.
    a,eta=Q(1,64),Q(1,4096)
    rho=[a/2,a/2,1-a];sigma=[a/2+eta/2,a/2-eta/2,1-a]
    original=sum((abs(x-y) for x,y in zip(rho,sigma)),Q(0))
    conditioned=sum((abs(x/a-y/a) for x,y in zip(rho[:2],sigma[:2])),Q(0))
    assert original==eta and conditioned==eta/a==Q(1,64)
    assert all(x>0 for x in rho+sigma)
    result={'status':'PASS exact guards reject incorrect formulas/interfaces',
            'utc':datetime.now(timezone.utc).isoformat(),'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'missing_squared_binomial':{'actual_norm':str(z),'wrong_norm':str(false)},
            'wrong_global_assignment_denominator':{'actual_identity_success':'1','wrong_success':str(false_mass)},
            'conditioning_error_amplification':{'input_trace_norm':str(original),'output_trace_norm':str(conditioned),'amplification':'64'},
            'exact_bounded_fair_bits_guard':'uniform3 categories is impossible with any bounded number B of fair bits, since3 does not divide2^B; dyadic approximation/error budget required',
            'native_state_preparation':'not executed; finite classical description is not physical preparation'}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'actual_norm':str(z),'wrong_norm':str(false),'conditioning_amplification':'64'}))


if __name__=='__main__':main()
