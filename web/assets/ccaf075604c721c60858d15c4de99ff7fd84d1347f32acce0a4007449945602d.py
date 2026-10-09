"""Freeze the finite campaign's own artifacts; omit downloaded source bodies."""
from pathlib import Path
import hashlib
import json
import shutil

BASE = Path(__file__).resolve().parents[2]
DEST = BASE / 'work/portable_replay_v1/Astra_Ultra_2026-10-09'
ROOTS = ['theory', 'applied', 'natural', 'sol', 'root']
RUNTIME = {'.venv', '__pycache__', '.git'}
SOURCE_DIRS = {'research', 'source', 'sources', 'source_cache', 'tmp_pdfs'}
EXTRACTS = {
    'work/applied/a12_weighted_design/das26a_v306.txt',
    'work/theory/t14_quantum_decoding/ggj_section7_extract.txt',
    'work/theory/t14_quantum_decoding/np_alg5_extract.txt',
    'work/sol/local_chart_decoder/ggj-layout.txt',
    'work/sol/local_chart_decoder/np-layout.txt',
}
KEEP_SOURCE_METADATA = {'work/applied/research/source_audit_icml26_v1.json'}

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    if DEST.exists():
        raise RuntimeError('Refusing to overwrite an existing replay snapshot')
    DEST.mkdir(parents=True)
    included, omitted = [], []
    for name in ROOTS:
        for p in sorted((BASE / 'work' / name).rglob('*')):
            if not p.is_file() or set(p.parts) & RUNTIME:
                continue
            rel = str(p.relative_to(BASE))
            source = (bool(set(p.parts) & SOURCE_DIRS)
                      or rel in EXTRACTS or p.suffix in {'.pdf', '.png', '.tex'})
            if rel in KEEP_SOURCE_METADATA:
                source = False
            rec = dict(path=rel, bytes=p.stat().st_size, sha256=digest(p))
            if source:
                rec['reason'] = 'Downloaded source body, extraction or source rendering; citation retained in research records'
                omitted.append(rec)
                continue
            if p.name == 'final_assessment_draft.txt':
                rec['reason'] = 'Superseded administrative draft; final assessment included'
                omitted.append(rec)
                continue
            if p.suffix not in {'.txt', '.json', '.py', '.cpp', '.sha256'}:
                raise RuntimeError('Unclassified file: ' + rel)
            dest = DEST / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dest)
            rec['classification'] = 'Own research, diagnostic, source metadata, audit or preservation record; latest claim ledger governs'
            included.append(rec)
    for name in ['CAMPAIGN_CONTRACT.txt', 'MODEL_SELECTION_NOTE_v1.txt', 'SOURCE_PINS.json']:
        p = BASE / 'work' / name
        shutil.copy2(p, DEST / 'work' / name)
        included.append(dict(path='work/' + name, bytes=p.stat().st_size,
                             sha256=digest(p), classification='Campaign scope or source provenance'))
    (DEST / 'ORIGINAL_ARTIFACTS_MANIFEST.json').write_text(json.dumps(included, indent=2) + '\n')
    (DEST / 'OMITTED_SOURCE_MANIFEST.json').write_text(json.dumps(dict(
        policy='No canonical repository, downloaded paper body, private runtime or cache is bundled. Source URLs and versions remain in proof records. Own source audit JSON is retained.',
        omitted_repository_pins=json.loads((BASE / 'work/SOURCE_PINS.json').read_text()),
        file_omissions=omitted), indent=2) + '\n')
    print(json.dumps(dict(destination=str(DEST), included_files=len(included),
                          included_bytes=sum(x['bytes'] for x in included),
                          omitted_source_files=len(omitted)), indent=2))

if __name__ == '__main__':
    main()
