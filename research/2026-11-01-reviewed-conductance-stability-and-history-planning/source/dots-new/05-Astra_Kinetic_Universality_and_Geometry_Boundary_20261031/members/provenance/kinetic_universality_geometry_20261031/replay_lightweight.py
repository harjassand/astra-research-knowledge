#!/usr/bin/env python3
"""Copied lightweight receiving replay; never invokes the full 513D recomputation."""
from fractions import Fraction as F
import copy, importlib.util, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    out=importlib.util.module_from_spec(spec);spec.loader.exec_module(out);return out
family=module('packaged_family','homogeneous_entropic_capacity_20261031/transverse_mobility_family/receive_family.py')
raw=family.base.fixture(2)
cert=family.certify(raw,full_ratio=F(2))
receipt=family.verify(raw,cert,full_ratio=F(2))
assert receipt['status']=='PASS'
assert cert['exact_attainable_set']['endpoints_attained'] is False
assert cert['exact_attainable_set']['lower_endpoint_numerically_evaluated'] is False
assert cert['exact_attainable_set']['realizing_mobility_constructed'] is False
bad=copy.deepcopy(cert);bad['kinetic_family']['cross_mobility']='allowed'
try:family.verify(raw,bad,full_ratio=F(2))
except family.Unknown:pass
else:raise AssertionError('cross-mobility contract corruption accepted')
large=json.loads((ROOT/'homogeneous_entropic_capacity_20261031/transverse_mobility_family/family_513D_certificate.json').read_text())
assert F(large['full_ratio_exact'])<F(101,100)
assert large['exact_attainable_set']['lower_endpoint_numerically_evaluated'] is False
assert large['exact_attainable_set']['realizing_mobility_constructed'] is False
counter=module('packaged_counter','cross_mobility_boundary_20261031/receive.py')
src=counter.strict_json_loads((ROOT/'cross_mobility_boundary_20261031/example_input.json').read_text())
cc=counter.receive(src)
assert cc==json.loads((ROOT/'cross_mobility_boundary_20261031/example_certificate.json').read_text())
def q(o):return F(int(o['numerator']),int(o['denominator']))
rate=q(cc['capacity_over_basin_mass']['upper'])
assert rate<F(1441,10**9) and rate>F(144,10**8)
try:counter.strict_json_loads('{"k":1,"k":2}')
except ValueError:pass
else:raise AssertionError('duplicate keys accepted')
try:counter.receive({'schema':counter.SCHEMA,'k':10**20,'epsilon':{'numerator':1,'denominator':2}})
except ValueError as e:assert 'resource_budget' in str(e)
else:raise AssertionError('power budget missing')
print(json.dumps({'status':'PASS','lightweight_family_receipt':receipt,
 'family_cross_contract_corruption_rejected':True,
 'saved_513D_ratio_checked_exactly':large['full_ratio_exact'],
 'full_513D_recomputation':'NOT repeated for packaging; accepted source-bound whole audits retained',
 'counter_example_exact_match':True,
 'counter_conductance_safe_strict_upper':'1.441e-6',
 'counter_positive_tail_preserved':True,
 'counter_duplicate_keys_and_preallocation_budget_rejected':True,
 'scope':'Copied lightweight end-to-end raw family and fixed counter receiving; no new scientific claim'},indent=2))
