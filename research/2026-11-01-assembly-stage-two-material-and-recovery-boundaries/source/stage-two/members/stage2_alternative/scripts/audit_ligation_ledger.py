#!/usr/bin/env python3
"""Independent parent-chain audit of root's recursive RNA-input ledger.

No physical yield is inferred; q and recovery are specified scenario inputs.
Does not import root's implementation.
"""
from pathlib import Path
from collections import Counter
import json
import math

HERE=Path(__file__).resolve().parents[1]
tree=json.loads((HERE/'data/full25_assembly_tree.json').read_text())
design=json.loads((HERE/'data/full25.json').read_text())
ledger=json.loads((HERE.parent/'stage2_root/results/ligation_input_ledger.json').read_text())
parent={child:node['id'] for node in tree for child in node['children']}
assert len(parent)==sum(len(node['children'])for node in tree), 'This audit requires a tree, not a reused-child DAG.'
u=ledger['q']*ledger['purification']
assert 0 < u <= 1
rows=[]
for piece in design['pieces']:
    child=piece['id'];depth=0
    while child in parent:
        child=parent[child];depth+=1
    required=u**(-depth)
    observed=ledger['fragments'][piece['id']]
    assert observed['purified_operations_on_path']==depth
    assert math.isclose(required,observed['input_moles_per_output_mole'],rel_tol=1e-12)
    rows.append(dict(id=piece['id'],depth=depth,length_nt=piece['length'],
                     input_mol=required,method=piece['method']))
total=sum(x['length_nt']*x['input_mol']for x in rows)
chemical=sum(x['length_nt']*x['input_mol']for x in rows if x['method']=='chemical_synthesis')
assert math.isclose(total,ledger['input_nucleotides_per_output_RNA'],rel_tol=1e-12)
assert math.isclose(chemical,ledger['chemical_nucleotides_per_output_RNA'],rel_tol=1e-12)
assert math.isclose(total,2617/u**3+287/u,rel_tol=1e-12)
assert sum(x['length_nt']for x in rows)==2904
result=dict(status='PASS__SPECIFIED_SCENARIO_ONLY',
    independent_method='Leaf-to-root parent traversal; no import of recursive ledger function',
    q=ledger['q'],purification=ledger['purification'],u=u,
    path_depth_counts=dict(Counter(x['depth']for x in rows)),
    formula='2617/u^3 + 287/u',
    verified_total_input_nt=total,verified_chemical_input_nt=chemical,
    verified_IVT_input_nt=total-chemical,
    equal_per_leaf_input_nt=2904/u**3,
    saved_tail_input_nt=287*(u**-3-u**-1),
    zero_loss_limit_nt=2904,
    limitations=['q is not measured for this rRNA',
                 'RNA losses through q and purification are included',
                 'Initial RNA manufacture, end processing, ATP turnover, enzymes and DNA splints are uncharged',
                 'Ribosome assembly, selection and lifetime are outside this RNA-feed ledger'])
(HERE/'data/independent_ledger_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
