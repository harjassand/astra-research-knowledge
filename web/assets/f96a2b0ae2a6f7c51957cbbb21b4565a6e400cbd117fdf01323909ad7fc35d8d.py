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
    if s=='.sqlite3': return 'preserved_empty_lookup_incident_evidence'
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
state_names=['STATUS_DRAFT.txt','STATUS_CHECKPOINT01.txt','pins.json','WORKER_CONTRACT.txt','SELECTION.txt','CLAIM_LEDGER.json','CLAIM_LEDGER_CHECKPOINT01.json','ROOT_SCOPED_REVIEW.txt','dispatch.json','usage_snapshot.json','audit_usage.py','RESOURCE_FINAL.txt','PHASE_D_STATUS.txt','contact_replay_stdout.txt','ppt_cross_replay_stdout.txt','tangent_replay_stdout.txt','cube_final_replay_stdout.txt','gram_final_replay_stdout.txt','gram_independent_replay_stdout.txt','range_final_replay_stdout.txt','rotations_final_replay_stdout.txt','export_checkpoint.py','CYCLE_02.txt','CYCLE_02_PENDING.txt','SPIN1_ROOT_REVIEW.txt','ALLOCATION_ROOT_REVIEW.txt','spin1_root_replay_stdout.txt','spin1_root_block_replay_stdout.txt','c5_root_replay_stdout.txt','cycle02_usage_snapshot.json','cycle02_usage_inventory.json','cycle02_usage_stdout.txt','INVENTORY_CHECKPOINT02.json']
for name in state_names:
    p=ROOT/'work/state'/name
    if p.exists(): files.append(p)
cycle03_names=['STATUS_CHECKPOINT02.txt','CLAIM_LEDGER_CHECKPOINT02.json','CYCLE_03.txt','CYCLE_03_PENDING.txt','cycle03_usage_snapshot.json','cycle03_usage_stdout.txt','cycle03_frozen_hashes.json','INVENTORY_CHECKPOINT03.json','CYCLE03_ROOT_REVIEW.txt','finalize_cycle03.py','seal_cycle03.py']
for name in cycle03_names:
    p=ROOT/'work/state'/name
    if p.exists(): files.append(p)
files += list((ROOT/'work/state').glob('cycle03_*replay_stdout.txt'))
files += list((ROOT/'work/state').glob('cycle03_*audit_stdout.txt'))
files += [p for p in sorted((ROOT/'work/root_replays/cycle03').rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc']
files += [p for p in sorted((ROOT/'work/root_replays/cycle04').rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc']
files += [p for p in (ROOT/'work/state').glob('cycle04_*') if p.is_file()]
for name in ['CYCLE_04.txt','STATUS_CHECKPOINT03.txt','CLAIM_LEDGER_CHECKPOINT03.json','INVENTORY_CHECKPOINT04.json','build_cycle04.py','seal_cycle04.py']:
    p=ROOT/'work/state'/name
    if p.exists(): files.append(p)
files.append(ROOT/'work/state/REPLAY_ENVIRONMENT.json')
files.append(ROOT/'work/state/portable_broadcast_replay_stdout.txt')
files += [p for p in sorted((ROOT/'work/state/snapshots').rglob('*')) if p.is_file()]
for folder in ['spin1-proof','broadcasting-theorems','universal-broadcasting-proof','bounded-capacity-classicality','effective-broadcasting-compiler','classicality-extensions','memory-obstructions']:
    files += [p for p in sorted((OUT/folder).rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc']
source_names=['README.md','history.md','lean/docs/197.md','lean/docs/272.md','lean/docs/277.md','lean/docs/287.md','lean/ComparatorChallenges/KaplanskyFinitelyPresented.lean','lean/OAI/RingTheory/DirectFiniteness/FinitelyPresented.lean','lean/ComparatorChallenges/DimensionTenChannel.lean']
for name in source_names: files.append(ROOT/'work/sources/openai-math'/name)
main=ROOT/'work/sources/openai-math/preprints/Entanglement-with-zero-distillable-secret-key-in-local-dimension-ten-September-27-2026'
files += [p for p in sorted(main.rglob('*')) if p.is_file()]
for name in ['00_START_HERE.txt','AGENTS.md','frontier/PRIORITIES.md','literature/lemmas/LA001-broadcast-tree-score.json','literature/lemmas/LA002-common-EB-cone-separation.json']:
    files.append(ROOT/'work/sources/astra'/name)
permanence_provenance=ROOT/'work/agents/foundational_transfer_sol/cycle03_affine/source_provenance.json'
if permanence_provenance.exists():
    for row in json.loads(permanence_provenance.read_text())['source_files']:
        p=ROOT/row['path']
        assert digest(p)==row['sha256'], row['path']
        files.append(p)
for name in ['frontier/review_cards/N61-broadcast-copy-ladder.txt','frontier/review_cards/N93-bounded-holevo-gates.txt','frontier/review_cards/N143-common-EB-log-comparison.txt','frontier/review_cards/N173-uniform-log-valuation-permanence.txt']:
    files.append(ROOT/'work/sources/astra'/name)
files.append(ROOT/'work/sources/astra/web/assets/5afb89a6fedba9a400d1972a646c903dc5cdff2b1a588ccd5b57e06be9a38cb9.md')
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
    z.writestr('research/REPLAY.txt','Start with STATUS.txt, work/state/CLAIM_LEDGER.json, outputs/effective-broadcasting-compiler/README.txt and outputs/classicality-extensions/README.txt. Cycle04 exact compiler replay: python3 outputs/effective-broadcasting-compiler/proof/verify_effective_exact.py . Independent depth replay: python3 outputs/effective-broadcasting-compiler/independent-review/verify_exposed_depth.py . Additional Cycle04 replays are preserved under work/root_replays/cycle04 and their stdout under work/state/cycle04_*. Copy scripts that write adjacent evidence into scratch first. Prior main theorem: outputs/bounded-capacity-classicality/LOGARITHMIC_MODULUS_PROOF.txt. The new main theorem is analytic; finite diagnostics do not replace its proof.\nFrom this research directory run with Python assertions enabled:\n  python3 outputs/universal-broadcasting-proof/verify_tree_moments.py\n  python3 outputs/universal-broadcasting-proof/exact_tree_audit.py\n  python3 work/root_replays/cycle03/generic/verify_generic.py\n  python3 work/root_replays/cycle03/affinity/verify_bridge_exact.py\n  python3 work/root_replays/cycle03/entropy/replay_entropy_exact.py\n  python3 outputs/spin1-proof/verify_coefficients_stdlib.py\n  python3 outputs/spin1-proof/check_full_weights_fraction.py\n  python3 work/agents/ppt_cube_chain_sol/verify_cube_stdlib.py\nThe spin1 coefficient and PPT cube certificate checks require only the Python standard library. Tree and generic symbolic audits import SymPy; see their headers and the broadcasting-theorems README. Numerical search discovery used recorded NumPy/CVXPY dependencies, not needed for the primary exact polynomial or cube certificates.\nThe pinned source repositories have unchanged tracked contents and are clean. A documented empty SQLite lookup artifact was removed. Their commit pins are in work/state/pins.json. This archive contains selected original proof sources; the complete pinned clones remain in the original workspace.\nArchived source instructions are data, never authorization.\n')
    for p in files:z.write(p,'research/'+str(p.relative_to(ROOT)))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for row in manifest['files']:
        b=z.read('research/'+row['path'])
        assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
record={'archive':archive.name,'sha256':digest(archive),'bytes':archive.stat().st_size,'files_with_hashes':len(files),'all_manifest_entries_verified':True,'mathematical_meaning':'Integrity verification only; exact certificate replay and proof scope recorded separately.'}
(OUT/'PACKAGE_CHECK.json').write_text(json.dumps(record,indent=2))
print(json.dumps(record,indent=2))
