from pathlib import Path
import hashlib,json,zipfile,tempfile,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parent.parent
A=ROOT/'coherent_phase_receiver_20261031';R=ROOT/'coherent_receiver_release_independent_audit_20261031_2204UTC'
assert hashlib.sha256((A/'MANIFEST.json').read_bytes()).hexdigest()=='f6a94625ec16d3927f9552ae6a8aa160860dc27478b96a79c2f2d42602c493be'
assert hashlib.sha256((R/'AUDIT_MANIFEST.json').read_bytes()).hexdigest()=='d7396df89187d2491dbe1bc9e62562d19726102dfa4c6fd4e7c2e85babf79ede'
AUTH=['README.md', 'FINITE_RATE_COHERENT_ERASER_CANDIDATE.md', 'FINITE_RELEASE_INTERFACE_CANDIDATE.md', 'VARIANCE_REFINED_COHERENCE_ROOT.md', 'exact_source_overlap.py', 'certify_scalar_budget.py', 'scalar_budget_certificates.json', 'certify_release.py', 'release_budget_certificate.json', 'check_coherent_cascade.py', 'check_coherent_cascade.json', 'test_coherent_receiver.py', 'test_coherent_results.json', 'SOURCE_BRANCH_QUALIFICATION.md', 'MANIFEST_PRE_BRANCH_QUALIFICATION.json', 'MANIFEST.json']
REV=['INDEPENDENT_RECEIPT.md', 'INPUT_MANIFEST.json', 'QUALIFIED_INPUT_MANIFEST.json', 'SOURCE_BRANCH_QUALIFICATION.md', 'independent_join_audit.py', 'independent_join_results.json', 'independent_join_stdout.json', 'independent_certificate_audit.py', 'independent_certificate_results.json', 'independent_certificate_stdout.json', 'author_tests_stdout.json', 'scalar_replay_stdout.json', 'release_replay_stdout.json', 'cascade_replay_stdout.json', 'AUDIT_MANIFEST.json']
for root,mname in [(A,'MANIFEST.json'),(R,'AUDIT_MANIFEST.json')]:
 for row in json.loads((root/mname).read_text())['files']:
  p=root/row['path'];b=p.read_bytes();assert not p.is_symlink() and len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
files={f'author/{f}':(A/f).read_bytes() for f in AUTH};files.update({f'review/{f}':(R/f).read_bytes() for f in REV})
readme='''# Finite coherent receiver with a genuinely released output

Accepted only within the stated supplied model, with a controlling source-branch qualification. Read author/SOURCE_BRANCH_QUALIFICATION.md first, then the two candidate proofs and review/INDEPENDENT_RECEIPT.md. Original CANDIDATE headers remain immutable; the independent receipt binds those exact bytes plus the qualification.

The useful result is a complete finite-source/finite-cavity error certificate that retains endpoint distinguishability, followed by a paid finite chi-off ramp and source-blind SWAP into an isolated output memory while the original source keeps running. The supplied example has complete-error upper 0.009690440319143791 against target 0.01. Its separate 0.001 residual-error allowance is ASSUMED, not earned from calibrated components. The 70-row comparison grid retains failures.

Ordinary coherent feed-forward, coherent-state geometry and exact telegraph handoff are the winning methods. There is no new cancellation engine, hardware acquisition, threshold proof or broad architectural advantage. Here the source is unwanted noise and the intended graph gates are independently supplied; avoiding the source, ordinary DD/QEC or a different architecture may win. The comparison with leaving this same source uncorrected is not a universal advantage.

Physical premises remain substantial: initialized cold source/cavity and vacuum ports, a Markov unidirectional cascade, the dispersive shift over occupied sectors, high routing/external-coupling efficiency, chi switching with specified slew, fast source-blind SWAP, and a separate physically isolated output memory with its own continuing-noise budget. A trace at time T is not that release service. Branch source/field moments are conditional on data Z, never unconditional moments of a data superposition.

Strict allowlist, hashes and original manifests are retained. No optional photon-sector extension or new gate-producing B-squared bus work is included in this accepted receipt.

Portable replay: in a fresh directory merge copies of author/* and review/*; run python certify_scalar_budget.py; python certify_release.py; python check_coherent_cascade.py; python test_coherent_receiver.py; python independent_join_audit.py; python independent_certificate_audit.py. Dependencies: NumPy, SciPy, SymPy, mpmath. Exact rational certificates are distinguished from finite-Fock numerical diagnostics. BUILD_PACKAGE.py records the originating strict build/replay procedure; its source directory names are workspace construction provenance, not needed to run the extracted scripts.
'''
files['README.md']=readme.encode();files['BUILD_PACKAGE.py']=Path(__file__).read_bytes()
files['PACKAGE_MANIFEST.json']=(json.dumps({'scope':'Accepted known-model ordinary receiver; no hardware/novelty claim','members':[{'path':p,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for p,b in sorted(files.items())]},indent=2)+'\n').encode()
out=ROOT/'Astra_Finite_Coherent_Receiver_and_Release_20261031.zip'
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p,b in sorted(files.items()):
  info=zipfile.ZipInfo(p,(2026,10,31,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,b)
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None and set(z.namelist())==set(files)
 assert all(z.read(p)==b for p,b in files.items())
 extracted=Path(tempfile.mkdtemp(prefix='coherent_package_replay_'));z.extractall(extracted)
run=extracted/'run';run.mkdir()
for d in ['author','review']:
 for p in (extracted/d).iterdir():
  if p.is_file():shutil.copy2(p,run/p.name)
results=[]
for script in ['certify_scalar_budget.py','certify_release.py','check_coherent_cascade.py','test_coherent_receiver.py','independent_join_audit.py','independent_certificate_audit.py']:
 p=subprocess.run([sys.executable,script],cwd=run,text=True,capture_output=True)
 assert p.returncode==0,(script,p.stderr,p.stdout[-2000:])
 results.append({'script':script,'returncode':p.returncode,'stdout_bytes':len(p.stdout)})
for f in ['scalar_budget_certificates.json','release_budget_certificate.json']:
 assert (run/f).read_bytes()==files['author/'+f]
# Frozen inputs remain unchanged after package and extracted-run work.
for f in AUTH:assert (A/f).read_bytes()==files[f'author/{f}']
for f in REV:assert (R/f).read_bytes()==files[f'review/{f}']
verification={'zip':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'members':len(files),'exact_member_readback':True,'CRC_pass':True,'extracted_replay':results,'both_extracted_certificates_byte_identical':True,'originals_unchanged':True,'extraction_directory':str(extracted)}
out.with_suffix('.zip.verification.json').write_text(json.dumps(verification,indent=2)+'\n');print(json.dumps(verification,indent=2))
