from pathlib import Path
import hashlib,json,zipfile,tempfile,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parent.parent
A=ROOT/'monitored_phase_resource_20261031';R=ROOT/'monitored_phase_receiver_independent_audit_20261031_2135UTC'
assert hashlib.sha256((A/'MANIFEST.json').read_bytes()).hexdigest()=='20c8f193c616ca7215ad0c63ed79703058567ae7cc4d8ef821ce57e79c8740d5'
assert hashlib.sha256((R/'AUDIT_MANIFEST.json').read_bytes()).hexdigest()=='30b41128f48bc8035da1ad85f2d8a355d01ceca76e6e53b53c701657b1cb347b'
AUTH=['README.md','CONTROLLED_PHASE_RESOURCE_AND_RECEIVER.md','monitored_phase.py','certify_receiver.py','receiver_certificates.json','sweep_diagnostic.json','test_monitored_phase.py','test_results.json','MANIFEST.json']
REV=['INDEPENDENT_RECEIPT.md','audit_independent.py','independent_results.json','audit_full_graph.py','full_graph_results.json','audit_high_precision.py','high_precision_results.json','author_replay_stdout.json','certificate_replay_stdout.json','diagnostic_replay.json','independent_stdout.json','full_graph_stdout.json','INPUT_MANIFEST.json','AUDIT_MANIFEST.json']
for root,mname in [(A,'MANIFEST.json'),(R,'AUDIT_MANIFEST.json')]:
 for row in json.loads((root/mname).read_text())['files']:
  p=root/row['path'];b=p.read_bytes();assert not p.is_symlink() and len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
files={f'author/{f}':(A/f).read_bytes() for f in AUTH};files.update({f'review/{f}':(R/f).read_bytes() for f in REV})
readme='''# Ordinary monitored phase-resource operation and receiver

Accepted scoped known-model result; no calibrated hardware or novelty claim. The actual finite-source/finite-dead-time detector calculation prepares arbitrary commuting graph/weighted-phase layers with local phase correction. Ordinary environment-assisted correction is the winner, not a new correction principle.

Useful service reduction: at four EXACT stipulated loss values (64,256,1024,4096) with the declared other inputs, a photon-only receiver can omit terminal source measurement and attains the optimal noisy-endpoint risk. The independent review certifies all 16 policy signs, not just matching decimals. This is not a continuum claim for every loss>=64. At loss16 endpoint measurement genuinely helps. For arbitrary-channel echo comparisons with an odd number of X pulses the consumer must receive the known final X frame (or pay its correction).

Read author/CONTROLLED_PHASE_RESOURCE_AND_RECEIVER.md, then review/INDEPENDENT_RECEIPT.md. Original author CANDIDATE headers remain immutable; the receipt binds the exact accepted bytes. Spectral collection, source preparation, target/endpoint controls, local independent detector instruments and continuing-noise handoff remain actual paid requirements. The output is at time T, not a detached stable register. Abstract thermal raising channels are not automatically physically observable ports. No full-source simulator, hardware run, purchase, outreach or publication is included.

All files are literally allowlisted. PACKAGE_MANIFEST.json hashes every other member. Original author/review manifests and bytes are preserved. No unreviewed coherent-cavity continuation is included.

Replay in a FRESH directory: merge copies of author/* and review/*, then run python certify_receiver.py; python monitored_phase.py > replay_sweep.json; python test_monitored_phase.py; python audit_independent.py; python audit_full_graph.py; python audit_high_precision.py. Dependencies are NumPy, SciPy, SymPy, mpmath. Exact certificate paths and rational sign checks differ from floating diagnostics. Do not overwrite historical accepted snapshots. BUILD_PACKAGE.py is the originating allowlist/build/replay script; its workspace-specific source paths are construction provenance, not a portable runner.
'''
files['README.md']=readme.encode();files['BUILD_PACKAGE.py']=Path(__file__).read_bytes()
files['PACKAGE_MANIFEST.json']=(json.dumps({'scope':'Accepted known-model ordinary receiver; no hardware/novelty claim','members':[{'path':p,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for p,b in sorted(files.items())]},indent=2)+'\n').encode()
out=ROOT/'Astra_Monitored_Phase_Resource_Receiver_20261031.zip'
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p,b in sorted(files.items()):
  info=zipfile.ZipInfo(p,(2026,10,31,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,b)
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None and set(z.namelist())==set(files)
 assert all(z.read(p)==b for p,b in files.items())
 extracted=Path(tempfile.mkdtemp(prefix='monitored_package_replay_'));z.extractall(extracted)
run=extracted/'run';run.mkdir()
for d in ['author','review']:
 for p in (extracted/d).iterdir():
  if p.is_file():shutil.copy2(p,run/p.name)
results=[]
for script in ['certify_receiver.py','monitored_phase.py','test_monitored_phase.py','audit_independent.py','audit_full_graph.py','audit_high_precision.py']:
 p=subprocess.run([sys.executable,script],cwd=run,text=True,capture_output=True)
 assert p.returncode==0,(script,p.stderr,p.stdout[-2000:])
 results.append({'script':script,'returncode':p.returncode,'stdout_bytes':len(p.stdout)})
 if script=='monitored_phase.py':assert p.stdout.encode()==files['author/sweep_diagnostic.json']
assert (run/'receiver_certificates.json').read_bytes()==files['author/receiver_certificates.json']
# Frozen inputs remain unchanged after package and extracted-run work.
for f in AUTH:assert (A/f).read_bytes()==files[f'author/{f}']
for f in REV:assert (R/f).read_bytes()==files[f'review/{f}']
verification={'zip':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'members':len(files),'exact_member_readback':True,'CRC_pass':True,'extracted_replay':results,'extracted_sweep_byte_identical':True,'extracted_certificate_byte_identical':True,'originals_unchanged':True,'extraction_directory':str(extracted)}
out.with_suffix('.zip.verification.json').write_text(json.dumps(verification,indent=2)+'\n');print(json.dumps(verification,indent=2))
