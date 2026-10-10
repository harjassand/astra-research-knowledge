#!/usr/bin/env python3
"""Execute or replay the uncapped acquired-probability sampler."""
import argparse
import json
from pathlib import Path
import time
import regenerative_solver as rs
import certified_solver as cs

parser=argparse.ArgumentParser()
parser.add_argument('--replay',type=Path)
parser.add_argument('--output',type=Path,default=Path(__file__).with_name('regenerative_sample_receipt.json'))
args=parser.parse_args()
source=None
if args.replay:
    prior=json.loads(args.replay.read_text())
    bits=iter(''.join(d['uniform_bits'] for d in prior['sample']['decisions']))
    source=lambda: int(next(bits))
start=time.monotonic()
sample=rs.exact_sample(cs.make_fixture(),source)
if args.replay:
    assert sample['sample']==prior['sample']['sample']
    assert [d['uniform_bits'] for d in sample['decisions']]==[d['uniform_bits'] for d in prior['sample']['decisions']]
result={'status':'completed_uncapped_acquired_sampler_path','elapsed_seconds':time.monotonic()-start,
        'model':'certified_solver.make_fixture(), rational n=3 k=2 model',
        'sample':sample,'replayed':bool(args.replay),
        'scope':'The mathematical distribution guarantee assumes ideal fair bits and the proved interval oracle; a single executed path is not distributional validation.'}
args.output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'sample':sample['sample'],
                  'levels':[len(d['uniform_bits']) for d in sample['decisions']],
                  'elapsed_seconds':result['elapsed_seconds'],'replayed':bool(args.replay)},indent=2))
