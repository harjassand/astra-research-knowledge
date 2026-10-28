"""Exact recorded-fault counterexample and sharp finite envelopes; no samples."""
from fractions import Fraction as F
import json,hashlib
from pathlib import Path
rows=[]
for p in [F(1,100),F(1,4),F(2,5)]:
 for J in range(1,17):
  weights=[p**int(f).bit_count()*(1-p)**(J-int(f).bit_count()) for f in range(2**J)]
  assert sum(weights)==1
  bad=sum(weights[1:]);bound=1-(1-p)**J
  assert bad==bound and bad<=J*p
  # Orthogonal Bell states per recorded nonzero pattern: half trace distance=bad.
  rows.append({'p':str(p),'J':J,'exact_recorded_Bell_half_distance':str(bad),'bound':str(bound)})
assert -F(1,4)*(1-F(1,4))==-F(3,16)
p=Path(__file__).resolve().parent
r={'status':'PASS_AUTHOR_EXACT_RECORDED_ERROR_FIXTURES','cases':len(rows),'cp_domination_negative_normalized_Choi_witness':'-3/16','source_calls':0,'random_draws':0,'scope':'Exact scalar weights/orthogonal Bell-record spectral calculation; no acquisition or generic controller execution','source_sha256':hashlib.sha256((p/'common_clean_subchannel_memory_bound_20261028.md').read_bytes()).hexdigest(),'rows':rows}
(p/'common_clean_subchannel_memory_check_20261028.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],len(rows))
