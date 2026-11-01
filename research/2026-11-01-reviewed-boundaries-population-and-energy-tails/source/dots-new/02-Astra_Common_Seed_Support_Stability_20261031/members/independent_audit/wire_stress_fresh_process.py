#!/usr/bin/env python3
"""Isolated decimal-guard regression; outputs only finite receipt metadata."""
from pathlib import Path
from fractions import Fraction as F
import sys,os,json,hashlib,importlib.util,subprocess
HERE=Path(__file__).resolve().parent

def raw_for(case):
    if case=='input_rate':
        return [((0,0),(1,0),F(10**5000)),((1,0),(0,0),F(1)),
                ((1,2),(2,1),F(1)),((2,1),(1,2),F(1))]
    assert case=='scalar_output'
    n=4;a=3;p=6;zero=(0,)*n;e=(0,0,0,1);raw=[(zero,e,F(1)),(e,zero,F(1))]
    for j in range(3):
        u=tuple(p*int(i==j)+int(i==a)for i in range(n));z=tuple((p-1)*int(i==j)+int(i==j+1)+int(i==a)for i in range(n))
        raw.extend([(u,z,F(1)),(z,u,F(1))])
    return raw

def child(target,case):
    assert hasattr(sys,'set_int_max_str_digits')
    sys.set_int_max_str_digits(4300)
    name={'candidate':'frozen_seeded_time_change.py','independent':'independent_time_change_receiver.py',
          'original':'original_07a01d55_seeded_time_change.py'}[target]
    spec=importlib.util.spec_from_file_location('isolated_target',HERE/name);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    raw=raw_for(case);z=m.numerical(raw,F(2),100000);canonical=m.canonical if hasattr(m,'canonical')else m.canon
    if target=='original':
        assert sys.get_int_max_str_digits()==4300
        try:canonical(z)
        except ValueError as error:
            assert '4300' in str(error)
            return dict(target=target,case=case,original_decimal_guard_failure_reproduced=True)
        raise AssertionError('expected original guard failure absent')
    assert sys.get_int_max_str_digits()==0
    wire=canonical(z);decoded=json.loads(wire)
    assert m.receive_numerical(raw,F(2),100000,decoded)
    assert z['status']=='CERTIFIED_SAMPLED_CORE_AND_STATIONARY_MOMENT_BOUND'
    return dict(target=target,case=case,guard_reset_to_default_before_import=True,module_disabled_guard=True,
                semantic_roundtrip=True,wire_bytes=len(wire.encode()),wire_sha256=hashlib.sha256(wire.encode()).hexdigest(),
                M_cut_decimal_digits=len(str(z['constants']['M_cut'])),retained_rational_peak_bits=z['work']['retained_rational_peak_bits'],
                support_powers_executed=z['work']['support_powers_executed'],Foster_power_expanded=False)

if __name__=='__main__':
    if len(sys.argv)>1:print(json.dumps(child(sys.argv[1],sys.argv[2]),sort_keys=True))
    else:
        rows=[]
        for target,case in [('original','scalar_output'),('candidate','scalar_output'),('independent','scalar_output'),('candidate','input_rate'),('independent','input_rate')]:
            out=subprocess.check_output([sys.executable,str(Path(__file__).resolve()),target,case],text=True,env={**os.environ,'PYTHONINTMAXSTRDIGITS':'4300'})
            rows.append(json.loads(out))
        assert rows[1]['wire_sha256']==rows[2]['wire_sha256'] and rows[3]['wire_sha256']==rows[4]['wire_sha256']
        expected=json.loads((HERE/'frozen_exercise_results.json').read_text())['large_scalar_wire_roundtrip']
        assert rows[1]['wire_sha256']==expected['wire_sha256'] and rows[1]['wire_bytes']==expected['wire_bytes']
        print(json.dumps(dict(cases=rows,scope='Trusted exact research process, not hostile-input service or resource-cap certification.'),indent=2,sort_keys=True))
