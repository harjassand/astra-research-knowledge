#!/usr/bin/env python3
"""Split the 80nt PTC patch into a D/Psi52mer and dense mixed28mer.

The dense mixed chemical synthesis remains untested. This is exact sequence,
join, tree and conditional RNA-feed accounting, not a laboratory result.
"""
from pathlib import Path
import csv
import json
import math

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
old=json.loads((DATA/'full25.json').read_text())
mods={int(x['position']):x for x in json.loads((DATA/'modification_map.json').read_text())}
seq=''.join(x['canonical_sequence'] for x in old['pieces'])
pieces=[];new_patches=[]
for p in old['pieces']:
    if (p['start'],p['end'])!=(2437,2516):
        pieces.append(dict(p));continue
    for name,a,b in [('DP52',2437,2488),('DENSE28',2489,2516)]:
        local={k:v for k,v in mods.items() if a<=k<=b and v['installation']=='synthetic_patch'}
        x=dict(id=name,start=a,end=b,length=b-a+1,marks=list(local),method='chemical_synthesis',
               canonical_sequence=seq[a-1:b],
               modified_sequence=''.join('['+local[k]['modification']+']' if k in local else seq[k-1]
                                         for k in range(a,b+1)),
               terminal_chemistry='5prime_monophosphate__3prime_hydroxyl')
        pieces.append(x);new_patches.append(x)
assert len(pieces)==20 and ''.join(x['canonical_sequence'] for x in pieces)==seq
assert sum(x['length'] for x in pieces if x['method']=='chemical_synthesis')==386
nodes=[dict(id=x['id'],start=x['start'],end=x['end']) for x in pieces]
ops=[];tier=0
while len(nodes)>1:
    tier+=1;new=[]
    for i in range(0,len(nodes),3):
        children=nodes[i:i+3]
        if len(children)==1:
            new.extend(children);continue
        n=dict(id=f'R_T{tier}_B{i//3+1}',start=children[0]['start'],end=children[-1]['end'],
               children=[c['id'] for c in children],tier=tier)
        ops.append(n);new.append(n)
    nodes=new
assert len(ops)==10 and sum(len(x['children'])-1 for x in ops)==19
assert sum(len(x['children'])==2 for x in ops)==1
parent={c:n for n in ops for c in n['children']}

def ledger(q3,q2,r):
    rows=[]
    for p in pieces:
        node=p['id'];ret=1.0;depth=0
        while node in parent:
            n=parent[node];ret*=r*(q3 if len(n['children'])==3 else q2)
            depth+=1;node=n['id']
        rows.append(dict(id=p['id'],start=p['start'],end=p['end'],length=p['length'],depth=depth,
                         chemical=p['method']=='chemical_synthesis',
                         input_mol_per_product=1/ret,input_nt_per_product=p['length']/ret))
    return dict(q3=q3,q2=q2,recovery=r,interpretation='conditional example, not a measured or predicted rRNA yield',
                input_nt=sum(x['input_nt_per_product'] for x in rows),
                chemical_input_nt=sum(x['input_nt_per_product'] for x in rows if x['chemical']),
                IVT_input_nt=sum(x['input_nt_per_product'] for x in rows if not x['chemical']),leaves=rows)

u=.272*.8
uniform=ledger(.272,.272,.8)
mixed=ledger(.272,.318,.8)
assert math.isclose(uniform['input_nt'],2539/u**3+365/u**2)
assert math.isclose(uniform['chemical_input_nt'],308/u**3+78/u**2)
assert math.isclose(mixed['input_nt'],2539/u**3+365/(u*(.318*.8)))
assert sum(x['length'] for x in uniform['leaves'] if x['depth']==3)==2539
assert sum(x['length'] for x in uniform['leaves'] if x['depth']==2)==365
assert math.isclose(ledger(1,1,1)['input_nt'],2904)
new_junction=dict(after_position=2488,acceptor_terminal=seq[2487],donor_initial=seq[2488],
                  canonical_rna_24nt=seq[2476:2500],
                  modified_sites_in_12nt_flanks=[p for p in mods if 2477<=p<=2500 and mods[p]['installation']=='synthetic_patch'],
                  note='Cm2498 lies in right flank; original modification-free NN diagnostic does not transfer')
assert new_junction['modified_sites_in_12nt_flanks']==[2498]
out=dict(status='COMPUTED_CHEMICAL_RISK_LOCALIZATION__DENSE28_SYNTHESIS_NOT_DEMONSTRATED',
         new_patches=new_patches,pieces=pieces,fragment_count=20,junction_count=19,
         chemical_patch_count=10,chemical_nt=386,IVT_nt=2518,
         operations=ops,ligation_operations=10,ternary_operations=9,binary_operations=1,maximum_tiers=3,
         new_junction=new_junction,uniform_net_scenario=uniform,mixed_DALI_value_scenario=mixed,
         uniform_total_formula='2539/u^3 + 365/u^2',uniform_chemical_formula='308/u^3 + 78/u^2',
         equal_input_molar_output_at_uniform_u=u**3,
         stoichiometric_minimum_ligation_ATP=19,stoichiometric_minimum_RlmKL_SAM=2,
         status_of_gain='Avoids processing D in the ho5C deprotection recipe; reduces the unproven mixed patch from80nt to28nt.',
         unearned=['joint Cm/ho5C/m2A/Psi synthesis and deprotection in DENSE28',
                  'exact DP52 and DENSE28 recovery and sequence purity',
                  'ligation of the new junction with a methylated splint flank',
                  'subsequent full RNA manufacture and full-function ribosome assembly'])
(DATA/'refined_cluster_route.json').write_text(json.dumps(out,indent=2)+'\n')
with (DATA/'refined_cluster_patches.fasta').open('w') as f:
    for p in new_patches:
        f.write(f">{p['id']}__{p['start']}_{p['end']}__CANONICAL_ONLY\n{p['canonical_sequence']}\n")
with (DATA/'refined_cluster_ledger.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(uniform['leaves'][0]));w.writeheader();w.writerows(uniform['leaves'])
print(json.dumps({k:out[k] for k in ['status','new_patches','fragment_count','junction_count','ligation_operations','ternary_operations','binary_operations','maximum_tiers','new_junction']},indent=2))
print(json.dumps(dict(uniform_total=uniform['input_nt'],uniform_chemical=uniform['chemical_input_nt'],
                     uniform_IVT=uniform['IVT_input_nt'],mixed_total=mixed['input_nt'],
                     equal_input_output=u**3),indent=2))
