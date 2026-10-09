"""Portable smoke checks; no repository clone, network or workspace source needed."""
from pathlib import Path
import hashlib
import importlib.util
import json
import random
import sys
from fractions import Fraction as F

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT/'MANIFEST.sha256.json').read_text())
for name, expected in manifest.items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == expected, name

def module(name, path):
    spec=importlib.util.spec_from_file_location(name, ROOT/path)
    value=importlib.util.module_from_spec(spec)
    sys.modules[name]=value
    spec.loader.exec_module(value)
    return value

cal = module('calibration', 'work/calibration_audit/diagnostics.py')
for h, n in [(4, 6), (16, 26), (64, 104)]:
    plan=cal.ExactPlan(h)
    assert plan.n == n
    assert 1-1/plan.z >= F(1,3)
    rr=cal.ratios(h)
    for j, weight in enumerate(rr):
        assert F(1,2**(j+1))*cal.acceptance(h,j)==weight/2
    rng=random.Random(912+h)
    assert all(cal.conditional_sample(h,rng)[0] % 2 == 0 for _ in range(100))

sys.path.insert(0, str(ROOT/'work/gaussian_transfer'))
from large_herald_arb import LargeHeraldGaussian
paired=LargeHeraldGaussian.from_pure([[F(0),F(1,3)],[F(1,3),F(0)]],0,10**100)
assert paired.sample(random.Random(777),F(1,10**10)) == [10**100]
B=[[F(1,5),F(1,10),F(1,20)],
   [F(1,10),F(1,6),F(1,25)],
   [F(1,20),F(1,25),F(1,7)]]
generic=LargeHeraldGaussian.from_pure(B,0,10**6)
sample=generic.sample(random.Random(778),F(1,10**10))
assert len(sample)==2 and sum(sample)%2==0
assert generic.last_ticket_count<=generic.last_ticket_bound
assert all(type(x) is int and x>=0 for x in sample)
for bad in [True, F(3,2), 1.5]:
    try:
        LargeHeraldGaussian.from_pure(B,0,bad)
    except TypeError:
        pass
    else:
        raise AssertionError('noninteger herald accepted')

from displaced_evaluator import log_H
from displaced_sampler import DisplacedHeraldGaussian, ParityEnvelope
from flint import arb, ctx
coefficient, coefficient_meta=log_H(10**20+1,F(1,3),F(1,10**30),40)
with ctx.workprec(256):
    assert coefficient.is_finite()
    assert coefficient.rad()<=arb(2)**(-42)
bimodal=ParityEnvelope(F(1,4),F(7,40),F(1,100),2,F(1,10**8))
assert len(bimodal.anchors)==2
for k in range(3):
    lo,hi=bimodal.bounds(k)
    assert 0<=lo<=hi and hi-lo<=2
displaced=DisplacedHeraldGaussian.from_pure(B,[F(1,7),F(1,8),F(1,9)],0,31)
displaced_sample=displaced.sample(random.Random(779),F(1,10**8))
assert len(displaced_sample)==2
assert all(type(x) is int and x>=0 for x in displaced_sample)
assert not displaced.last_ticket_fallback
assert displaced.last_ticket_count<=displaced.last_ticket_bound

print(json.dumps({'status':'PASS', 'manifest_files_checked':len(manifest),
    'exact_optimal_copy_counts':{'4':6,'16':26,'64':104},
    'exact_pair_herald':'10^100', 'generic_sample':sample,
    'displaced_sample':displaced_sample, 'coefficient_order':'10^20+1',
    'coefficient_method':coefficient_meta['method'],
    'physical_hardware_executed':False}))
