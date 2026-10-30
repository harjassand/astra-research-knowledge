import numpy as np,json
from pathlib import Path
from itertools import product
# Three Z-type checks on three qubits: S1=ZZI, S2=IZZ, S3=ZIZ=S1*S2.
syndromes=[(b[0]^b[1],b[1]^b[2],b[0]^b[2]) for b in product(range(2),repeat=3)]
admissible=sorted(set(syndromes)); checked=0
# Group has four elements labelled by independent S1,S2, not eight distinct elements.
for delta in admissible:
 for i in range(8):
  for j in range(8):
   actual=tuple(a^b for a,b in zip(syndromes[i],syndromes[j]))
   block=float(actual==delta)
   fourier=sum((-1)**(g[0]*(delta[0]^actual[0])+g[1]*(delta[1]^actual[1])) for g in product(range(2),repeat=2))/4
   assert block==fourier
   if block:
    generator=sum((-1)**d-1 for d in actual)
    assert generator==-2*sum(delta)
   checked+=1
for delta in product(range(2),repeat=3):
 if delta not in admissible:assert not any(tuple(a^b for a,b in zip(x,y))==delta for x in syndromes for y in syndromes)
out=dict(status='pass',matrix_unit_projector_checks=checked,independent_check_rank=2,physical_dephasing_checks=3,admissible_disagreements=admissible,redundant_check_damping_counts_actual_checks=True,scope='Exact small redundant-check Fourier/eigenvalue algebra, not a memory-threshold simulation')
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
