"""Exact positive-contraction witness: short-echo precision versus duration.
This obstructs one acquisition design, not all legal experiment designs.
"""
from fractions import Fraction as F
from pathlib import Path
import json

def response(e, h, coupled):
    return (1+(1-2*e)**h)/2 if coupled else (1-e)**h

def run():
    cases=[]
    for h in [20,100,500,2000]:
        e=F(5,h)
        differences=[abs(response(e,k,True)-response(e,k,False)) for k in range(5)]
        eta=max(differences)/2
        records=[]
        for k in range(5):
            a,b=response(e,k,True),response(e,k,False)
            y=(a+b)/2
            assert abs(a-y)<=eta and abs(b-y)<=eta
            records.append({'length':k,'common_report':str(y),'radius':str(eta)})
        gap=response(e,h,True)-response(e,h,False)
        assert gap>F(49,100)
        assert eta<=3*e*e
        assert gap>2*F(1,100)
        cases.append({'horizon':h,'epsilon':str(e),'short_echo_eta':str(eta),
                      'short_echo_eta_float':float(eta),'short_common_records':records,
                      'long_response_gap':{'numerator_hex':hex(gap.numerator),
                                           'denominator_hex':hex(gap.denominator)},
                      'long_response_gap_float':float(gap),
                      'long_probe_eta':'1/100','long_probe_primitive_executions':h,
                      'short_maximum_length':4})
    p=Path(__file__).resolve().parents[1]/'results'/'SHORT_ECHO_OBSTRUCTION.json'
    p.write_text(json.dumps({'cases':cases,'all_exact_checks_passed':True},indent=2))
    for x in cases:print(x['horizon'],x['short_echo_eta_float'],x['long_response_gap_float'])

if __name__=='__main__':run()
