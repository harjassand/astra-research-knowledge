from pathlib import Path
from fractions import Fraction
import sys,json
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'robustness_dilation_capacity_20261031'))
import receive_robustness as r
p=root/'robustness_dilation_capacity_20261031'
raw=json.loads((p/'small_raw_fixture.json').read_text())
cert=json.loads((p/'small_certificate.json').read_text())
task=dict(cert['task'])
for k in ['delta','beta','quad_relative','full_ratio']:
 if task[k] is not None:task[k]=Fraction(task[k])
print(json.dumps(r.verify(raw,cert,**task),sort_keys=True))
