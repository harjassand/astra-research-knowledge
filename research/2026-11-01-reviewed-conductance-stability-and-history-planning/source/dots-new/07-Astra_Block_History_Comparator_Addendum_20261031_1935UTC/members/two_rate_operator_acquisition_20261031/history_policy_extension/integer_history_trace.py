#!/usr/bin/env python3
"""Paid exact common-denominator backend for the new capped tree recurrence."""
from pathlib import Path
import hashlib,json,math,sys
import sympy as s
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT))
from receive_history import constants,PARENT
R=s.Rational


def run():
    model=json.loads((PARENT/'history_sensitive_4096_result.json').read_text())
    local=json.loads((PARENT/'feedback_extension'/'block_comparison_results.json').read_text());v=constants(model,local)
    xs=[R(v['c']),R(v['kappa']),R(model['cross_rounds'][-1]['leave']),R(v['fine_bound'])]
    D=math.lcm(*(int(x.q) for x in xs));c,k,e,f=[int(x*D) for x in xs]
    z=0;total=0;den=1;peak=1;products=0;checks=0
    for j in range(model['length']):
        assert R(z,den)==R(v['residual_caps_before_each_step'][j]);checks+=1
        total+=z
        a=c*den;b=k*z;newden=D*den;total*=D;products+=4
        candidate=a+b;peak=max(peak,*(abs(x).bit_length() for x in [a,b,newden,total,candidate]))
        z=min(newden,candidate);den=newden
    a=e*total;b=f*den;finalden=D*den;products+=3;answer=R(a+b,finalden)
    peak=max(peak,*(abs(x).bit_length() for x in [a,b,a+b,finalden]))
    assert answer==R(v['history_error_bound']);checks+=1
    return {'status':'PASS_EXACT_INTEGER_HISTORY_RECURRENCE','checks':checks,
       'common_denominator':D,'common_denominator_bits':D.bit_length(),'recurrence_scalar_products':products,
       'peak_integer_bits':peak,'final_unreduced_denominator_bits':finalden.bit_length(),
       'history_error_bound':str(answer),'scope':'A paid exact backend for deterministic history constants, NOT a replacement for source/probe receiving. lcm/gcd/comparisons, input reading and inherited costs are additional.',
       'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__=='__main__':
    out=run();(ROOT/'integer_history_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='history_error_bound'},indent=2))
