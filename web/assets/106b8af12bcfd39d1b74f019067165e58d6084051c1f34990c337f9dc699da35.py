"""Assemble user deliverables only after the isolated replay has passed."""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile

BASE = Path(__file__).resolve().parents[2]
PACK = BASE / 'work/portable_replay_v1/Astra_Ultra_2026-10-09'
OUTPUT = BASE / 'outputs'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    results = json.loads((PACK/'checks/REPLAY_RESULTS.json').read_text())
    if results['count'] != 21 or results['passed'] != 21:
        raise RuntimeError('Selected portable replay has not passed')
    additions = [
        'work/sol/observable_separation/build_and_verify_witness_v2.py',
        'work/sol/observable_separation/portable_replay_note_v1.txt',
        'work/root/run_portable_checks_v3.py',
        'work/root/portable_start_here_v2.txt',
        'work/root/portability_repair_v1.txt',
        'work/root/finalize_portable_pack_v1.py',
    ]
    additions.extend(str(p.relative_to(BASE)) for p in sorted(
        (BASE/'work/sol/observable_separation/portable_replay_check_v1').rglob('*')) if p.is_file())
    original = json.loads((PACK/'ORIGINAL_ARTIFACTS_MANIFEST.json').read_text())
    known = {x['path'] for x in original}
    for rel in additions:
        p, q = BASE/rel, PACK/rel
        if q.exists() and q.read_bytes() != p.read_bytes():
            raise RuntimeError('Unexpected differing final addition: ' + rel)
        q.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p,q)
        if rel not in known:
            original.append(dict(path=rel, bytes=p.stat().st_size, sha256=sha(p),
                                 classification='Append-only portable replay repair or final assembly'))
    (PACK/'ORIGINAL_ARTIFACTS_MANIFEST.json').write_text(json.dumps(original,indent=2)+'\n')
    parts = [
        'work/sol/hidden_realization/v1.txt',
        'work/sol/hidden_realization/v2.txt',
        'work/sol/hidden_realization/v3.txt',
        'work/sol/observable_separation/v1.txt',
        'work/sol/observable_separation/v2.txt',
        'work/sol/observable_separation/v3.txt',
        'work/sol/hidden_realization/v4.txt',
        'work/theory/t13_reversible_realization/v1.txt',
        'work/sol/hidden_realization/exact_certificate_v1.json',
    ]
    main_text=(PACK/'work/root/principal_result_front_v3.txt').read_text()
    main_text+='\nPORTABLE CHECKER NOTE\nThe original v1 witness generator embeds an absolute historical source path. Use build_and_verify_witness_v2.py for portable byte-preserving verification. This software-only correction leaves every rational coefficient and proof version unchanged. The archive preserves the initial failed replay and its diagnosed metadata mismatch.\n'
    for i, rel in enumerate(parts,1):
        p=PACK/rel
        main_text+='\n\n'+'='*78+'\n'
        main_text+=f'PROOF RECORD {i}: {rel}\nSHA-256: {sha(p)}\n'
        main_text+='='*78+'\n\n'+p.read_text()+'\n'
    (PACK/'MAIN_RESULT.txt').write_text(main_text)
    shutil.copy2(PACK/'work/root/campaign_report_v1.txt',PACK/'CAMPAIGN_REPORT.txt')
    shutil.copy2(PACK/'work/root/final_claim_ledger_v1.json',PACK/'CLAIM_LEDGER.json')
    shutil.copy2(PACK/'work/root/portable_start_here_v2.txt',PACK/'00_START_HERE.txt')
    mutations=[]
    for x in original:
        q=PACK/x['path']
        if sha(q)!=x['sha256']:
            mutations.append(dict(path=x['path'],before=x['sha256'],after=sha(q)))
    (PACK/'REPLAY_MUTATIONS.json').write_text(json.dumps(dict(
        scope='Comparison of frozen original own-artifact bytes after selected replay; new check logs and final deliverables are separate.',
        changed_original_files=mutations),indent=2)+'\n')
    if mutations:
        raise RuntimeError('Unexpected original-artifact mutations require review')
    verifier='''from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
rows=json.loads((root/'FILE_MANIFEST.json').read_text())
expected={r['path'] for r in rows}
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p.name!='FILE_MANIFEST.json' and '__pycache__' not in p.parts}
if expected!=actual:
    raise RuntimeError('File inventory mismatch: '+str(expected.symmetric_difference(actual)))
for row in rows:
    p=root/row['path']
    if p.stat().st_size!=row['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:
        raise RuntimeError('Digest mismatch: '+row['path'])
print('PASS: '+str(len(rows))+' files; present artifact integrity only, not proof validation')
'''
    (PACK/'verify_package.py').write_text(verifier)
    manifest=[]
    for p in sorted(PACK.rglob('*')):
        if p.is_file() and p.name!='FILE_MANIFEST.json':
            manifest.append(dict(path=str(p.relative_to(PACK)),bytes=p.stat().st_size,sha256=sha(p)))
    (PACK/'FILE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    OUTPUT.mkdir(exist_ok=True)
    for name in ['MAIN_RESULT.txt','CAMPAIGN_REPORT.txt','CLAIM_LEDGER.json']:
        shutil.copy2(PACK/name,OUTPUT/name)
    with zipfile.ZipFile(OUTPUT/'ASTRA_ULTRA_RESEARCH_PACK.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(PACK.rglob('*')):
            if p.is_file(): z.write(p,arcname=str(p.relative_to(PACK.parent)))
    names=['MAIN_RESULT.txt','CAMPAIGN_REPORT.txt','CLAIM_LEDGER.json','ASTRA_ULTRA_RESEARCH_PACK.zip']
    (OUTPUT/'SHA256SUMS.txt').write_text(''.join(sha(OUTPUT/n)+'  '+n+'\n' for n in names))
    print(json.dumps(dict(package_files=len(manifest)+1,original_files=len(original),
                          original_mutations=len(mutations),checks_passed=results['passed'],
                          deliverables=[dict(file=n,bytes=(OUTPUT/n).stat().st_size,sha256=sha(OUTPUT/n)) for n in names]),indent=2))

if __name__=='__main__':
    main()
