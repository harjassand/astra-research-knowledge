#!/usr/bin/env python3
"""New rate-ceiling use of the frozen public representative. No source reads."""
from pathlib import Path
from fractions import Fraction as F
import hashlib, json, time

ROOT=Path(__file__).resolve().parent/'macro_run'

def main():
    start=time.perf_counter();p=ROOT/'POSITIVE_MEAN_REALIZATION.json'
    data=json.loads(p.read_text());m=data['ports'];n=data['states']
    rates=[-F(data['generator'][i][i]) for i in range(n)]
    assert all(x>0 for x in rates)
    assert all(x<=F(3,2) for x in rates[:m])
    assert all(x<=1 for x in rates[m:])
    assert any(x>1 for x in rates[:m])
    report={'status':'PASS','meaning':'Exact clock ceilings of the existing public prepared generator; not ceilings of the original source.',
      'model_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
      'source_observations':0,'source_preparations':0,'private_source_reads':0,
      'model_states':n,'ports':m,'port_ceiling':'3/2','hidden_ceiling':'1',
      'departure_rates':[str(x) for x in rates],
      'port_rate_display':[float(x) for x in rates[:m]],
      'hidden_rate_display':[float(x) for x in rates[m:]],
      'source_native_unit_port_rates_preserved':False,
      'inherited_query_count':data['query_count'],
      'inherited_source_confidence_failure_upper':data['source_confidence_failure_upper'],
      'inherited_coefficient_numerator_bits':data['max_coefficient_numerator_bits'],
      'inherited_coefficient_denominator_bits':data['max_coefficient_denominator_bits'],
      'wall_seconds':time.perf_counter()-start,
      'scope':'Mathematical generator certificate only. Original source uncertainty and preparation/calibration/tail premises remain those of the frozen acquired-record certificate. Hardware realization and finite-precision perturbation are not executed.',
      'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (ROOT/'ACQUIRED_MODEL_CLOCK_CERTIFICATE.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','model_states','ports','port_ceiling','hidden_ceiling','source_native_unit_port_rates_preserved']}))

if __name__=='__main__':main()
