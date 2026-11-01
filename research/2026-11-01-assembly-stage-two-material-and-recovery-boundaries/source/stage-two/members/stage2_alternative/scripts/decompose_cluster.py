#!/usr/bin/env python3
"""Exact chemistry-separation construction, not a demonstrated synthesis.

Checks sequence/mark coverage, enumerates all six-block boundaries, constructs
a 24-leaf tree, and accounts for RNA input loss under labeled assumptions.
No ligase activity, chemical compatibility, folding or translation is predicted.
"""
from pathlib import Path
import csv
import itertools
import json
import math

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
full = json.loads((DATA / 'full25.json').read_text())
reference = ''.join(x['canonical_sequence'] for x in full['pieces'])
marks = {2449:'D', 2457:'Psi', 2498:'Cm', 2501:'ho5C', 2503:'m2A', 2504:'Psi'}
boundaries = [(2437,2452),(2453,2487),(2488,2499),(2500,2501),(2502,2503),(2504,2516)]
blocks=[]
for i,(start,end) in enumerate(boundaries,1):
    local={p:m for p,m in marks.items() if start<=p<=end}
    assert len(local)==1
    blocks.append(dict(id=f'C{i}', start=start, end=end, length=end-start+1,
                       canonical_sequence=reference[start-1:end],
                       marks=local,
                       modified_sequence=''.join('['+local[p]+']' if p in local else reference[p-1]
                                                 for p in range(start,end+1)),
                       method='chemical_synthesis_separate_deprotection',
                       exact_synthesis_and_ligation_demonstrated=False))
assert ''.join(b['canonical_sequence'] for b in blocks)==reference[2436:2516]
assert sum(b['length'] for b in blocks)==80
assert sorted(p for b in blocks for p in b['marks'])==sorted(marks)

# Enumerate every contiguous six-block cover separating the six ordered marks.
# The two Psi sites are separated by different modification classes, so they
# cannot share a contiguous block under the one-class-per-block restriction.
pos=sorted(marks)
cut_ranges=[range(a,b) for a,b in zip(pos,pos[1:])]
partition_count=0; best_min=0; max_m2a_block=0; witnesses=[]
for cuts in itertools.product(*cut_ranges):
    edges=(2436,)+cuts+(2516,)
    lengths=[b-a for a,b in zip(edges,edges[1:])]
    partition_count+=1
    max_m2a_block=max(max_m2a_block,lengths[4])
    if min(lengths)>best_min:
        best_min=min(lengths);witnesses=[dict(cuts=cuts,lengths=lengths)]
    elif min(lengths)==best_min and len(witnesses)<3:
        witnesses.append(dict(cuts=cuts,lengths=lengths))
assert partition_count==8*41*3*2
assert max_m2a_block==2 and best_min==2

pieces=[]
for p in full['pieces']:
    if (p['start'],p['end'])==(2437,2516):
        pieces.extend(blocks)
    else:
        pieces.append(dict(p))
assert len(pieces)==24
assert ''.join(p['canonical_sequence'] for p in pieces)==reference
assert sum(p['length'] for p in pieces)==2904

nodes=[dict(id=p['id'],start=p['start'],end=p['end'],children=[]) for p in pieces]
ops=[];tier=0
while len(nodes)>1:
    tier+=1;new=[]
    for i in range(0,len(nodes),3):
        group=nodes[i:i+3]
        if len(group)==1:
            new.append(group[0]);continue
        n=dict(id=f'C_T{tier}_B{i//3+1}',start=group[0]['start'],end=group[-1]['end'],
               children=[c['id'] for c in group],tier=tier)
        ops.append(n);new.append(n)
    nodes=new
assert len(ops)==12 and sum(len(n['children'])-1 for n in ops)==23
assert sum(len(n['children'])==2 for n in ops)==1
parents={child:n for n in ops for child in n['children']}

def direct_ledger(q3,q2,r):
    rows=[]
    for p in pieces:
        node=p['id'];retention=1.0;path=[]
        while node in parents:
            n=parents[node]; q=q3 if len(n['children'])==3 else q2
            retention*=q*r;path.append(n['id']);node=n['id']
        assert len(path)==3
        rows.append(dict(id=p['id'],length=p['length'],input_mol_per_product_mol=1/retention,
                         input_nt_per_product=p['length']/retention,path=path))
    return dict(q3=q3,q2=q2,purification_recovery=r,
                source_status='UNVALIDATED_SCENARIO__NOT_RRNA_YIELD',
                input_nt_per_product=sum(x['input_nt_per_product'] for x in rows),
                leaves=rows)

u=.272*.8
old_cost=2617/u**3+287/u
same=direct_ledger(.272,.272,.8)
mixed=direct_ledger(.272,.318,.8)
assert math.isclose(same['input_nt_per_product'],2904/u**3)
assert math.isclose(mixed['input_nt_per_product'],2499/u**3+405/(u*u*(.318*.8)))

# Local preassembly alternative. Four stages have net conversion+recovery
# (a,h,m,f): join C1+C2+C3; append C4 then dephosphorylate; append C5 then
# dephosphorylate; join C6 then phosphorylate the 5prime end. Each stage's
# parameter encompasses its required processing and recoveries.
# Exact modified dinucleotide donors and terminal ligation activity are UNPROVEN.
def local_cost(a,h,m,f):
    if min(a,h,m,f)<=0:
        return None
    return 63/(a*h*m*f)+2/(h*m*f)+2/(m*f)+13/f

scenarios=[]
for v in [1.0,.9,.8,.5,u]:
    local=local_cost(v,v,v,v)
    total=(2537+local)/u**3+287/u
    scenarios.append(dict(each_local_net_stage_retention_assumed=v,
                          local80_input_nt=local,
                          each_starting_block_equal_input_final_fraction=u**3*v**4,
                          full23S_matched_feed_nt=total,
                          chemical_input_nt=(306+local)/u**3,
                          extra_nt_above_original=total-old_cost,
                          interpretation='scenario only; all four local rates unmeasured'))
assert math.isclose(scenarios[0]['full23S_matched_feed_nt'],old_cost)

result=dict(status='COMPUTED_CONSTRUCTION_AND_OBSTRUCTION__NO_NEW_EXPERIMENTAL_PROOF',
            cluster_start=2437,cluster_end=2516,blocks=blocks,
            original_fragments=19,decomposed_fragments=24,
            original_joins=18,decomposed_joins=23,added_joins=5,
            same_chemical_nt=386,same_IVT_nt=2518,
            direct_tree=dict(tiers=3,ligation_operations=12,ternary_operations=11,
                             binary_operations=1,all_leaf_operation_depths=3),
            separation_obstruction=dict(partitions_enumerated=partition_count,
                                        maximum_possible_minimum_block_length=best_min,
                                        maximum_possible_m2A_block_length=max_m2a_block,
                                        witnesses=witnesses),
            uniform_direct_scenario=same,mixed_direct_scenario=mixed,
            original_matched_feed_nt_at_same_u=old_cost,
            local_preassembly=dict(added_ligation_operations=4,added_joins=5,
                                   added_dephosphorylations=2,added_5prime_phosphorylations=1,
                                   extra_protein_species=['T4 RNA ligase 1','recombinant shrimp alkaline phosphatase','T4 polynucleotide kinase'],
                                   formula='63/(a*h*m*f) + 2/(h*m*f) + 2/(m*f) + 13/f',
                                   full_RNA_formula='(2537 + local80_input_nt)/u^3 + 287/u',
                                   scenarios=scenarios),
            unearned_operations=['synthesis of exact blocked ho5C and m2A dinucleotide donors',
                                 'ligation/dephosphorylation at the exact ho5C2501 and m2A2503 contexts',
                                 'efficient assembly of 2nt substrates on a DNA splint',
                                 'survival of the complete chemistry through each processing operation',
                                 'translation, fidelity, lifetime and renewal of the resulting ribosome'],
            rigorous_lower_bound_on_yield=0)
(DATA/'cluster_decomposition.json').write_text(json.dumps(result,indent=2)+'\n')
(DATA/'cluster_decomposition_tree.json').write_text(json.dumps(ops,indent=2)+'\n')
with (DATA/'cluster_decomposition.fasta').open('w') as f:
    for b in blocks:
        f.write(f">{b['id']}__{b['start']}_{b['end']}__CANONICAL_ONLY\n{b['canonical_sequence']}\n")
with (DATA/'cluster_decomposition_scenarios.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(scenarios[0]));w.writeheader();w.writerows(scenarios)
print(json.dumps({k:result[k] for k in ['status','decomposed_fragments','decomposed_joins','direct_tree','separation_obstruction']},indent=2))
print(json.dumps(dict(original_input_nt=old_cost,uniform_direct_input_nt=same['input_nt_per_product'],
                     mixed_direct_input_nt=mixed['input_nt_per_product'],local_scenarios=scenarios),indent=2))
