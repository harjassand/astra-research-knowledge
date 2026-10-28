"""Exact physical-channel neighbourhood supported by the acquired kernel."""
import sys
sys.dont_write_bytecode=True
import json
from fractions import Fraction as F
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
raw=json.loads((BASE/'results'/'EXACT_REPAIRED_KERNEL.json').read_text())
nine={0,1,2,3,5,7,9,11,13}
minimum=None;arg=None
for column in raw['kernels']:
 vals={(a,b):F(v) for a,b,v in column['transitions']}
 for a in nine:
  for b in nine:
   p=vals.get((a,b),F())
   if minimum is None or p<minimum:minimum=p;arg=dict(input=column['input'],target=[a,b])
eps=F(1,12000)
assert minimum>4*eps
out=dict(minimum_spanning_basis_weight=str(minimum),minimum_weight_float=float(minimum),
 witness_location=arg,local_dual_operator_norm_bound='2 (actual maximum golden ratio)',
 tensor_dual_norm_bound=4,certified_diamond_radius=str(eps),radius_float=float(eps),
 exact_positive_margin=str(minimum-4*eps),
 meaning='Every supplied trace-preserving two-qutrit channel within this diamond distance of the acquired gate/noise map has nonnegative17x17 frame kernels by fixed-basis correction; actual channel data is still needed to compute them.')
(BASE/'results'/'KERNEL_ROBUSTNESS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
