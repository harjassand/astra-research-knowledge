"""Exact extension of root 36D test: bare-data syndrome is contained in physical combined flag."""
from pathlib import Path
import json
src=Path('producer-workspace/check_graph_state_factory.py').read_text()
exec(src.split("out={'scope'")[0])
checks={}
bare=[full((I(D)-S)/2,I(A)) for S in stab]
for y in range(2):
 checks[f'bare_syndrome{y}_contained_in_physical_flag']=flags[y]*bare[y]==bare[y] and bare[y]*flags[y]==bare[y]
 checks[f'other_dressing_commutes_{y}']=U[1-y]*bare[y]==bare[y]*U[1-y]
 small=I(n)-(I(n)-bare[y])*(I(n)-full(I(D),clock_bad[y]))
 dressed=W.T*bare[y]*W
 checks[f'dressed_bare_syndrome{y}_contained_in_small_union']=small*dressed==dressed and dressed*small==dressed
checks['joint_bare_syndromes_contained_in_joint_flags']=flags[0]*flags[1]*bare[0]*bare[1]==bare[0]*bare[1]
assert all(checks.values())
out={'checks':checks,'scope':'Exact finite regression for general bare graph-state DATA-syndrome domination proof; not independently certifying the sparse combined-flag theorem.'}
Path('producer-workspace/check_bare_graph_syndrome.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
