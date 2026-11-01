from pathlib import Path
import hashlib,json,zipfile,tempfile,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parent.parent
A=ROOT/'desired_bus_quantum_eraser_20261031';R=ROOT/'desired_bus_independent_audit_20261031_2219UTC'
assert hashlib.sha256((A/'MANIFEST.json').read_bytes()).hexdigest()=='786acaf6a3c99e758a85a4a913658853648166be3394e1ca609114f3a070aee7'
assert hashlib.sha256((R/'AUDIT_MANIFEST.json').read_bytes()).hexdigest()=='9d24bfa43344b3eace2589523c897f17553cf72b3ccd9831eb3d0e6bf625f389'
AUTH=['README.md', 'CLOSED_BUS_ERASURE_CANDIDATE.md', 'certify_bus.py', 'bus_certificates.json', 'test_bus.py', 'test_bus_results.json', 'MANIFEST.json', 'QUALIFIED_BINDING_ROOT.json', 'RECORD_NOISE_SCOPE_CORRECTION.md']
REV=['INDEPENDENT_RECEIPT.md', 'INPUT_MANIFEST.json', 'QUALIFIED_BINDING_ROOT.json', 'RECORD_NOISE_SCOPE_CORRECTION.md', 'independent_bus_audit.py', 'independent_bus_results.json', 'independent_bus_stdout.json', 'independent_interval_and_noise_audit.py', 'independent_interval_and_noise_results.json', 'independent_interval_and_noise_stdout.json', 'author_tests_stdout.json', 'certificate_replay_stdout.json', 'test_bus_results.json', 'AUDIT_MANIFEST.json']
for root,mname in [(A,'MANIFEST.json'),(A,'QUALIFIED_BINDING_ROOT.json'),(R,'AUDIT_MANIFEST.json')]:
 for row in json.loads((root/mname).read_text())['files']:
  p=root/row['path'];b=p.read_bytes();assert not p.is_symlink() and len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
files={f'author/{f}':(A/f).read_bytes() for f in AUTH};files.update({f'review/{f}':(R/f).read_bytes() for f in REV})
readme='''# Gate-producing linear bus with ordinary quantum erasure

Accepted qualified mathematical result, not hardware acquisition, novelty or architectural superiority. The bus supplies the desired maximally entangling ZZ gate itself. Ordinary geometric control, no-knowledge homodyne and local Z corrections are the winning methods.

Read author/RECORD_NOISE_SCOPE_CORRECTION.md first, then author/CLOSED_BUS_ERASURE_CANDIDATE.md and review/INDEPENDENT_RECEIPT.md. The original assertion about arbitrary independent record noise was WRONG: an exact variance-only dephasing identification requires zero-mean GAUSSIAN noise. General independent noise contributes its characteristic function; centered finite-variance noise has a separate conservative complete-error bound. The controlling correction does not change the five-point numerical budget, which never uses that incorrect assertion. Original six source files remain immutable for audit continuity.

Useful scoped results: the finite-slew bus pulse and finite passive filter produce complete-error upper 0.007417123668633808 at beta=8 under the declared services. All closed trajectories in the same fixed-B vacuum force class under the stipulated time, force cap and target phase have unmonitored error lower 0.1614815538202856. The five-point grid retains beta=1,2,4 failures. The receiver is minimax-optimal after the fixed unencoded gate in its certified small-loss regime. Variable-B, encoded, squeezed-input, multi-mode and coherent-reuse architectures are not excluded by that comparison.

The full-access exact erasure identity works for arbitrary warm/correlated linear apparatus; the finite-efficiency numerical certificate is explicitly VACUUM-only. Do not interchange those scopes. Actual spin-dependent force acquisition, faithful linearity, matched-mode homodyne/LO/electronics, calibration, local correction, zero residual force after release, and an extra 0.001 complete-error allowance remain supplied physical services. Finite filter bandwidth does not itself supply an ideal homodyne instrument or finite-slew LO truncation.

All member names are literally allowlisted. Original author/qualified/review bindings and exact bytes are retained. Finite-LO root candidates and taper continuation notes are OUTSIDE this accepted package.

Replay in a fresh directory: merge copies of author/* and review/*, then run python certify_bus.py; python test_bus.py; python independent_bus_audit.py; python independent_interval_and_noise_audit.py. Dependencies: NumPy, SciPy, SymPy and mpmath. Exact rational certificate paths differ from floating finite-Fock diagnostics. The originating BUILD_PACKAGE.py documents the strict source allowlist and extraction/replay process; its original workspace paths are provenance, not needed for portable extracted replay.
'''
files['README.md']=readme.encode();files['BUILD_PACKAGE.py']=Path(__file__).read_bytes()
files['PACKAGE_MANIFEST.json']=(json.dumps({'scope':'Accepted qualified ordinary gate-producing bus; no hardware/novelty or broad architecture claim','members':[{'path':p,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for p,b in sorted(files.items())]},indent=2)+'\n').encode()
out=ROOT/'Astra_Desired_Bus_Gate_and_Ordinary_Eraser_20261031.zip'
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p,b in sorted(files.items()):
  info=zipfile.ZipInfo(p,(2026,10,31,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,b)
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None and set(z.namelist())==set(files)
 assert all(z.read(p)==b for p,b in files.items())
 extracted=Path(tempfile.mkdtemp(prefix='desired_bus_package_replay_'));z.extractall(extracted)
run=extracted/'run';run.mkdir()
for d in ['author','review']:
 for p in (extracted/d).iterdir():
  if p.is_file():shutil.copy2(p,run/p.name)
results=[]
for script in ['certify_bus.py','test_bus.py','independent_bus_audit.py','independent_interval_and_noise_audit.py']:
 p=subprocess.run([sys.executable,script],cwd=run,text=True,capture_output=True)
 assert p.returncode==0,(script,p.stderr,p.stdout[-2000:])
 results.append({'script':script,'returncode':p.returncode,'stdout_bytes':len(p.stdout)})
for f in ['bus_certificates.json']:
 assert (run/f).read_bytes()==files['author/'+f]
# Frozen inputs remain unchanged after package and extracted-run work.
for f in AUTH:assert (A/f).read_bytes()==files[f'author/{f}']
for f in REV:assert (R/f).read_bytes()==files[f'review/{f}']
verification={'zip':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'members':len(files),'exact_member_readback':True,'CRC_pass':True,'extracted_replay':results,'extracted_certificate_byte_identical':True,'originals_unchanged':True,'extraction_directory':str(extracted)}
out.with_suffix('.zip.verification.json').write_text(json.dumps(verification,indent=2)+'\n');print(json.dumps(verification,indent=2))
