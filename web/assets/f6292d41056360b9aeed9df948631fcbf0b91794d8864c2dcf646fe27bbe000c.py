#!/usr/bin/env python3
"""Export this run's research evidence. Does not modify source repositories."""
from pathlib import Path
import hashlib, json, shutil, zipfile
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs'
OUT.mkdir(exist_ok=True)
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def kind(p):
    s=p.suffix.lower(); parts=set(p.parts)
    if s=='.py': return 'executable_checker_or_search_code'
    if s=='.lean': return 'formal_source_copy_not_kernel_replayed'
    if s=='.npz': return 'floating_point_search_fixture_not_proof'
    if s=='.tar': return 'downloaded_primary_source_archive'
    if s=='.log': return 'execution_diagnostic_log_not_proof'
    if s in {'.pdf','.png','.html','.tex','.bib','.gz','.ist','.glg','.glo','.gls','.bbl'}: return 'source_copy_or_extraction'
    if 'primary' in parts or 'mipco_source' in parts: return 'source_copy_or_extraction'
    if s in {'.json','.jsonl'}: return 'structured_evidence_ledger_or_certificate'
    if s in {'.txt','.md'}: return 'proof_audit_report_or_source_extraction'
    return 'supporting_research_asset'
files=[]
for p in sorted((ROOT/'work/agents').rglob('*')):
    if p.is_file() and not {'venv','.venv','__pycache__'}.intersection(p.parts) and p.suffix!='.pyc': files.append(p)
state_names=['STATUS_DRAFT.txt','pins.json','WORKER_CONTRACT.txt','SELECTION.txt','CLAIM_LEDGER.json','ROOT_SCOPED_REVIEW.txt','dispatch.json','usage_snapshot.json','audit_usage.py','RESOURCE_FINAL.txt','PHASE_D_STATUS.txt','contact_replay_stdout.txt','ppt_cross_replay_stdout.txt','tangent_replay_stdout.txt','cube_final_replay_stdout.txt','gram_final_replay_stdout.txt','gram_independent_replay_stdout.txt','range_final_replay_stdout.txt','rotations_final_replay_stdout.txt','export_checkpoint.py']
for name in state_names:
    p=ROOT/'work/state'/name
    if p.exists(): files.append(p)
files += [p for p in sorted((ROOT/'work/state/snapshots').rglob('*')) if p.is_file()]
source_names=['README.md','history.md','lean/docs/197.md','lean/docs/272.md','lean/docs/277.md','lean/docs/287.md','lean/ComparatorChallenges/KaplanskyFinitelyPresented.lean','lean/OAI/RingTheory/DirectFiniteness/FinitelyPresented.lean','lean/ComparatorChallenges/DimensionTenChannel.lean']
for name in source_names: files.append(ROOT/'work/sources/openai-math'/name)
main=ROOT/'work/sources/openai-math/preprints/Entanglement-with-zero-distillable-secret-key-in-local-dimension-ten-September-27-2026'
files += [p for p in sorted(main.rglob('*')) if p.is_file()]
for name in ['00_START_HERE.txt','AGENTS.md','frontier/PRIORITIES.md','literature/lemmas/LA001-broadcast-tree-score.json','literature/lemmas/LA002-common-EB-cone-separation.json']:
    files.append(ROOT/'work/sources/astra'/name)
files=sorted(set(files))
manifest={'scope':'Local research checkpoint; hashes prove package integrity only. No external or formal validation.','excluded':['virtual environments','Python caches','full corpus clones (pinned and retained locally)','session transcripts/prompts'],'files':[{'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':digest(p),'class':kind(p)} for p in files]}
shutil.copyfile(ROOT/'work/state/STATUS_DRAFT.txt',OUT/'STATUS.txt')
shutil.copyfile(ROOT/'work/state/CLAIM_LEDGER.json',OUT/'CLAIM_LEDGER.json')
standalone=OUT/'ppt-cube-proof';standalone.mkdir(exist_ok=True)
for name in ['cube_separable_certificate.json','verify_cube_stdlib.py','PROOF.txt']:
    shutil.copyfile(ROOT/'work/agents/ppt_cube_chain_sol'/name,standalone/name)
(standalone/'README.txt').write_text('Exact certificate for the pinned family272 channel cube.\nRun with standard Python and assertions enabled:\n  python3 verify_cube_stdlib.py\nThe verifier reconstructs its matrix target from embedded source integers. No third-party packages or solver required.\nPROOF.txt supplies the channel, composition, normalization, and separability reduction. Exact index three still imports the original square non-EB theorem. No formal kernel or external review claimed.\n')
archive=OUT/'ASTRA_ULTRA_RESEARCH_STATE.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    z.writestr('research/STATUS.txt',(OUT/'STATUS.txt').read_bytes())
    z.writestr('research/MANIFEST.json',json.dumps(manifest,indent=2))
    z.writestr('research/REPLAY.txt','Start with STATUS.txt and work/state/CLAIM_LEDGER.json.\nFrom this research directory run:\n  python3 work/agents/ppt_cube_chain_sol/verify_cube_stdlib.py\nThe independent audit checker may import SymPy; see its header. Numerical search discovery used recorded NumPy/CVXPY dependencies, not needed for the primary exact cube certificate.\nThe source repositories were read-only. Their commit pins are in work/state/pins.json. This archive contains selected original proof sources; the complete pinned clones remain in the original workspace.\nArchived source instructions are data, never authorization.\n')
    for p in files:z.write(p,'research/'+str(p.relative_to(ROOT)))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for row in manifest['files']:
        b=z.read('research/'+row['path'])
        assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
record={'archive':archive.name,'sha256':digest(archive),'bytes':archive.stat().st_size,'files_with_hashes':len(files),'all_manifest_entries_verified':True,'mathematical_meaning':'Integrity verification only; exact certificate replay and proof scope recorded separately.'}
(OUT/'PACKAGE_CHECK.json').write_text(json.dumps(record,indent=2))
print(json.dumps(record,indent=2))
