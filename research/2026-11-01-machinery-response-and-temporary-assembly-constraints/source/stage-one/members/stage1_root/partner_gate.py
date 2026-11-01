"""Inspect the actual deposited mature-contact neighborhood for a gate hypothesis.
This is a graph audit, not a folding/accessibility or sequence-design model.
"""
import csv,json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
p=ROOT.parent/'stage1_biochemical/public_code/PNA_50S/contact_chimerax/contact_matrix.csv'
rows=list(csv.reader(p.open()));names=rows[0][1:]
neighborhoods={}
for target in ['h1','h94','h98','h99','uL13']:
    vals={name:int(float(v)) for name,v in zip(names,rows[1+names.index(target)][1:])
          if float(v)>0 and name!=target}
    neighborhoods[target]={'contacts':vals,'degree':len(vals),
                          'protein_contact_count':sum(v for k,v in vals.items() if not k.startswith('h'))}
result={'input':'Pinned PNA_50S mature contact_matrix.csv; see biochemical provenance',
        'neighborhoods':neighborhoods,
        'construction_hypothesis':'Investigate partner-side H98-facing docking control, preserving H94/H99 folding, instead of strengthening the H1 blocker.',
        'limitation':'Contact graph alone supplies neither nucleotide access, selective kinetic barriers nor a binding sequence. No claimed gate design or folding yield.'}
(ROOT/'results/partner_gate_neighborhood.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
