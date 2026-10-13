#!/usr/bin/env python3
"""Freeze small inherited numerical references; no experiment or source writes."""
import hashlib
import json
from pathlib import Path
from xml.etree import ElementTree as ET

HERE = Path(__file__).resolve().parent
SOURCE = Path('/Users/harjas/Documents/Codex/2026-10-13/astra-genesis-civilization-enabling-breakthrough-discovery')
FILES = {
    'carrier_reference.json': 'work/phase5/manufacturing_operation/carrier_lifetime_results.json',
    'fructose_primary.xml': 'work/phase5/manufacturing_challenge/fructose_primary.xml',
    'imv_atp_primary.xml': 'work/phase5/manufacturing_challenge/imv_atp_primary.xml',
}

def digest(data):
    return hashlib.sha256(data).hexdigest()

receipts = []
for local, source in FILES.items():
    raw = (SOURCE / source).read_bytes()
    destination = HERE / local
    if destination.exists() and destination.read_bytes() != raw:
        raise RuntimeError(f'Frozen reference differs: {local}')
    destination.write_bytes(raw)
    receipts.append({'source_path': str(SOURCE / source), 'local_path': local,
                     'bytes': len(raw), 'sha256': digest(raw),
                     'status': 'inherited_source_preserved_not_new_validation'})

# A compact, locatable extraction records which primary paragraphs support
# the source-reported benchmark. It deliberately includes no experimental steps.
extraction = []
for file in ('fructose_primary.xml', 'imv_atp_primary.xml'):
    root = ET.parse(HERE / file).getroot()
    paragraphs = list(root.iter('p'))
    for index, element in enumerate(paragraphs):
        value = ' '.join(''.join(element.itertext()).split())
        selected = (
            file == 'fructose_primary.xml' and (
                value.startswith('In vitro synthesis of sn-glycerol') or
                value.startswith('The presence of erythrose isomerase increased') or
                value.startswith('The reason for the incomplete conversion'))
        ) or (file == 'imv_atp_primary.xml' and value.startswith('In this work, we applied'))
        if selected:
            extraction.append({'file': file, 'paragraph_index_zero_based': index,
                               'element_id': element.get('id'),
                               'paragraph_sha256': digest(value.encode()),
                               'text': value})

(HERE / 'primary_paragraph_index.json').write_text(json.dumps(extraction, indent=2) + '\n')
(HERE / 'SOURCE_RECEIPTS.json').write_text(json.dumps({
    'access_date': '2026-10-13',
    'scope': 'Public primary evidence and inherited conditional model, not physical validation',
    'files': receipts,
    'live_new_primary': {
        'title': 'Functional asymmetry of the F0 motor in bacterial ATP synthases',
        'doi': '10.1111/j.1365-2958.2009.06658.x',
        'url': 'https://onlinelibrary.wiley.com/doi/10.1111/j.1365-2958.2009.06658.x',
        'retrieved_evidence': 'primary_wiedenmann2009_web.txt',
        'primary_locations': 'Publisher lines 183-194, especially Fig. 4B caption at line 194',
        'claim_scope': 'ATP synthesis following a 20 micromolar NADH pulse in a distinct E. coli IMV preparation',
        'does_not_supply': 'Continuous native-PDH/IMV throughput at the inherited oxygen, nucleotide, carrier and salt conditions',
        'direct_download': 'Ordinary publisher HTML request returned HTTP 403; not retried or bypassed. Web retrieval supplies saved evidence.'
    }
}, indent=2) + '\n')
print(json.dumps({'pinned_files': len(receipts), 'selected_primary_paragraphs': len(extraction),
                  'source_files_unchanged': all(digest(Path(r['source_path']).read_bytes()) == r['sha256'] for r in receipts)}))
