"""Rep4 tree-resolution auxiliary packets on the complete reduced first blue-step seed.
Physical claim conditional only on chosen Figure24 arm grouping / tree realization;
all three uniform geometric partitions are inventoried. No lifetime no-go inferred.
"""
import json,contextlib,io,itertools
with contextlib.redirect_stdout(io.StringIO()):
 from flat_parent_face_fiber_test import inc
 from first_flat_step_homology_test import r
from sheaf_incidence_compiler import echelon,solve
oldD=r['D1'];oldbasis=echelon(oldD)
crosses=[]
for x in [1,2]:
 for y in [1,2]:
  N=18+(x-1)*3+y;S=N-1;E=24+(y-1)*3+x;W=E-1
  full=sum(1<<f for f in [N,S,E,W])
  assert full in oldD
  crosses.append(dict(x=x,y=y,N=N,S=S,E=E,W=W,full=full))
results={}
for partition in ['NE','NW','NS']:
 pair=[sum(1<<c[k] for k in partition) for c in crosses]
 newD=[v for v in oldD if v not in [c['full'] for c in crosses]]
 for j,c in enumerate(crosses):
  newD.extend([pair[j]|(1<<(30+j)),(pair[j]^c['full'])|(1<<(30+j))])
 nb=echelon(newD);rows=[]
 for mask in range(1,16):
  fine=mask<<30
  try:pauli=solve(nb,fine)
  except ValueError:continue
  choices=[]
  js=[j for j in range(4) if mask>>j&1]
  for sel in range(1<<len(js)):
   coarse=0
   for k,j in enumerate(js):coarse^=pair[j]^(crosses[j]['full'] if sel>>k&1 else 0)
   choices.append((coarse.bit_count(),coarse))
  best=min(choices)
  rows.append(dict(aux_mask=mask,aux_positions=[[crosses[j]['x'],crosses[j]['y']] for j in js],fine_syndrome_weight=len(js),min_coarse_weight_under_local_sections=best[0],coarse_representative=best[1],physical_pauli_column_witness=pauli))
 results[partition]=dict(new_checks=34,new_qubits=len(newD),rank=len(nb),valid_aux_only_packets=rows)
print(json.dumps(dict(scope=__doc__,crosses=crosses,results=results),indent=2))
