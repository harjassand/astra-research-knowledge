#!/usr/bin/env python3
"""Append-only exact finite certificate and its conditional acquisition warning."""
from pathlib import Path
import json
from verify_snapshot_operation import F, certificate, need

qrate = F(1,20)
q = [[-(1+qrate),F(1),qrate], [qrate,-(1+qrate),F(1)], [F(1),qrate,-(1+qrate)]]
result, bound, _ = certificate(q,[F(1,3)]*3,[F(0),F(1),F(1)],
                               F(39991,40000),[(F(1),F(1,1000))])
need(bound is not None and bound.lo > F(2,5), 'exact finite-window bound >0.4')
result.update({'status':'PASS', 'scope':'exact supplied-generator calculation, no empirical observation',
               'strict_rational_floor_above_2_over_5':True,
               'acquisition_scope':'the reported iid Hoeffding count is a sufficient planning number only; independent preparation, time resolution, noise and physical parity are not acquired',
               'interpretation':'a larger mathematical certificate need not give a cheaper or physically obtainable test'})
output = Path(__file__).with_name('SMALL_GAP_EXTENSION_v0001.json')
output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
