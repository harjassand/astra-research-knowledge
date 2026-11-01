"""Export exact sequences for the refined20-piece chemical construction.

This supplies a sequence specification, not validated synthesis/ligation
conditions. FASTA uses canonical parent bases; modifications remain explicit
in refined_cluster_route.json. Both strands of each proposed long dsDNA
splint are exported. No unmodified-duplex energy is assigned to modified RNA.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'stage2_alternative' / 'data'
route = json.loads((DATA / 'refined_cluster_route.json').read_text())
pieces = route['pieces']
sequence = ''.join(p['canonical_sequence'] for p in pieces)
reference = ''.join(line.strip() for line in
    (DATA / 'reference_23S_V00331_1.fasta').read_text().splitlines()
    if not line.startswith('>'))
assert sequence == reference and len(sequence) == 2904
nodes = {p['id']: p for p in pieces}
nodes.update({n['id']: n for n in route['operations']})

def rc_dna(s):
    return s.translate(str.maketrans('ACGT', 'TGCA'))[::-1]

def fasta_record(name, seq):
    return '>' + name + '\n' + '\n'.join(seq[i:i+80] for i in range(0, len(seq), 80)) + '\n'

fragments = ''
for p in pieces:
    assert p['canonical_sequence'] == sequence[p['start']-1:p['end']]
    fragments += fasta_record(f"{p['id']}__{p['start']}_{p['end']}__PARENT_BASES_ONLY__{p['method']}", p['canonical_sequence'])

splints = ''
for n in route['operations']:
    children = [nodes[c] for c in n['children']]
    assert children[0]['start'] == n['start']
    assert children[-1]['end'] == n['end']
    assert all(a['end'] + 1 == b['start'] for a,b in zip(children, children[1:]))
    sense = sequence[n['start']-1:n['end']].replace('U','T')
    anti = rc_dna(sense)
    assert rc_dna(anti) == sense
    splints += fasta_record(n['id']+'__DNA_SENSE_5to3', sense)
    splints += fasta_record(n['id']+'__DNA_ANTISENSE_5to3', anti)

mods = json.loads((DATA/'modification_map.json').read_text())
junctions = []
for a,b in zip(pieces, pieces[1:]):
    assert a['end']+1 == b['start']
    j=a['end']
    flank_mods=[m for m in mods if j-11 <= int(m['position']) <= j+12]
    junctions.append(dict(after_position=j, left_piece=a['id'],right_piece=b['id'],
        canonical_24nt=sequence[j-12:j+12],
        modification_map_in_flanks=flank_mods,
        physical_ligation_yield=None,
        note='Modifications and structure require separate energetic/ligation qualification.'))
assert len(junctions)==19
(DATA/'refined_full_fragments.fasta').write_text(fragments)
(DATA/'refined_long_dsDNA_splints.fasta').write_text(splints)
(DATA/'refined_junctions.json').write_text(json.dumps(junctions,indent=2)+'\n')
print(json.dumps(dict(status='SEQUENCE_SPECIFICATION_ONLY',pieces=len(pieces),
    RNA_nt=len(sequence),junctions=len(junctions),dsDNA_splints=len(route['operations']),
    modifications_in_FASTA=False,physical_yield_estimated=False),indent=2))
