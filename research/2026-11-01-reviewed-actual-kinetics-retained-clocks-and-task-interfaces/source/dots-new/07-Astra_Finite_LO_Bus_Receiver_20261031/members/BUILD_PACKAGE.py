from pathlib import Path
import hashlib,json,zipfile,tempfile,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parent.parent
A=ROOT/'finite_lo_bus_receiver_20261031';R=ROOT/'finite_lo_independent_audit_20261031_2307UTC'
assert hashlib.sha256((A/'MANIFEST.json').read_bytes()).hexdigest()=='4c72c3356d10c4e4a3e2b8cc77663875efcf94b049a1822767174b2057fea321'
assert hashlib.sha256((R/'AUDIT_MANIFEST.json').read_bytes()).hexdigest()=='546ae19245e1e9be0f1d153e5060ac4c7361229cab69835f39516ba90e7a445e'
AUTH=['README.md', 'FINITE_LO_ERASER_ROOT_CANDIDATE.md', 'FINITE_LO_RECEIVING_AND_BOUNDARY.md', 'accepted_certify_bus.py', 'accepted_bus_certificates.json', 'certify_finite_lo.py', 'finite_lo_certificates.json', 'test_finite_lo.py', 'test_finite_lo_results.json', 'MANIFEST.json', 'QUALIFIED_BINDING_ROOT.json', 'CONTROL_AND_DETECTOR_SCOPE_ADDENDUM.md']
REV=['INDEPENDENT_RECEIPT.md', 'INPUT_MANIFEST.json', 'QUALIFIED_BINDING_ROOT.json', 'CONTROL_AND_DETECTOR_SCOPE_ADDENDUM.md', 'independent_finite_lo_audit.py', 'independent_finite_lo_results.json', 'independent_finite_lo_stdout.json', 'independent_interval_bucket_audit.py', 'independent_interval_bucket_results.json', 'independent_interval_bucket_stdout.json', 'certificate_replay_stdout.json', 'author_tests_stdout.json', 'test_finite_lo_results.json', 'AUDIT_MANIFEST.json']
for root,mname in [(A,'MANIFEST.json'),(A,'QUALIFIED_BINDING_ROOT.json'),(R,'AUDIT_MANIFEST.json')]:
 for row in json.loads((root/mname).read_text())['files']:
  p=root/row['path'];b=p.read_bytes();assert not p.is_symlink() and len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
files={f'author/{f}':(A/f).read_bytes() for f in AUTH};files.update({f'review/{f}':(R/f).read_bytes() for f in REV})
readme='''# Finite-local-oscillator bus receiver: accepted qualified boundary

Ordinary weak-field homodyne supplies this declared finite optical instrument; no new erasure principle, acquired detector, warm-receiver extension or architecture advantage is claimed. Four observed LO photons, total count cap20, an extra finite PNR readout-time unit and continuing declared data noise give complete-error upper 0.009134838999948075. The nine-point grid retains weak-LO and finite-counter-overflow failures.

Read author/CONTROL_AND_DETECTOR_SCOPE_ADDENDUM.md FIRST, then author/FINITE_LO_RECEIVING_AND_BOUNDARY.md and review/INDEPENDENT_RECEIPT.md. Original nine author files are unchanged. The accepted 1e-6-radian tolerance is each qubit's END-TO-END error versus its exact ideal angle, including finite table rounding; it is not an actuator-only tolerance. Classical mislabeling after the declared instrument, or an explicitly received uniform bad-event CP coupling, may justify a 2 epsilon penalty. A Fock confusion matrix alone does not certify a complete coherent measurement instrument.

This replaces the ideal/infinite-LO homodyne limit with a specified finite beam-splitter/two-number-count instrument. It does NOT construct faithful number measurement, .999 system efficiency, exact mode/phase matching, calibrated readout latency, the required local corrections, or the supplied residual 0.001 complete-error allowance. The finite certificate is vacuum/coherent-signal-specific; the previous arbitrary-warm full-access erasure theorem is separate. The primary weak-field-homodyne experiment is credited as ordinary measurement precedent, not evidence that its reported efficiencies or response satisfy these parameters.

All proofs, source code, exact certificates, failures, qualified bindings and independent receipts/results are literally allowlisted. The nested dependency archive contains the entire accepted qualified desired-gate bus proof and review, not an optional new result. Neither taper extensions nor other unreviewed theorems are included.

Portable replay in a fresh directory: merge copies of author/* and review/*; run python certify_finite_lo.py; python test_finite_lo.py; python independent_finite_lo_audit.py; python independent_interval_bucket_audit.py. Dependencies: NumPy, SciPy and mpmath. The exact interval certifier itself uses the standard library. Floating finite-enumeration and bucket-detector checks are diagnostics, not hardware proofs. BUILD_PACKAGE.py records the exact originating allowlist/build/replay procedure; its workspace source names are provenance only.

## Scientific stopping point

Ordinary geometric-bus control and quantum erasure already supply this declared gate/receiver. Further receiver fixtures do not earn a new architecture. The decisive unearned operation is the actual mediator-to-controller quantum interface: create the specified entangling spin-dependent force and faithfully capture/read (or coherently reuse) its emitted mode with the required loss, modal accuracy, complete instrument error, timing and release. A new claim needs an acquired or fully physically constructed improvement to that operation, compared at equal resources with ordinary low-loss closed buses, coherent reuse, encoded and variable-B alternatives. Merely assuming better detection, an extra controlled interaction, or the residual 0.001 bound is not that improvement.

The energy-injection capital remains valuable for receiving actual finite sources: complete controlled observable decay/energy return can certify all-selected fault amplitudes without simulating every source event. It does not manufacture a bath/port, preparation or control service; with unchanged accessible information it does not beat the exact dephasing floor. These receivers change the information/interface supplied. Their conditional success is not an evasion of that earlier boundary.
'''
files['README.md']=readme.encode();files['BUILD_PACKAGE.py']=Path(__file__).read_bytes()
depname='Astra_Desired_Bus_Gate_and_Ordinary_Eraser_20261031.zip'
dep=(ROOT/depname).read_bytes()
assert hashlib.sha256(dep).hexdigest()=='140a0521116d8051176dbbf7576570c1d50faf980bd1e3cbbab26179f43db232'
with zipfile.ZipFile(ROOT/depname) as dz:
 assert dz.testzip() is None
 assert dz.read('author/certify_bus.py')==files['author/accepted_certify_bus.py']
 assert dz.read('author/bus_certificates.json')==files['author/accepted_bus_certificates.json']
files['dependencies/'+depname]=dep
files['PACKAGE_MANIFEST.json']=(json.dumps({'scope':'Accepted qualified ordinary finite-LO counting receiver; supplied instrument, no hardware/novelty or broad architecture claim','members':[{'path':p,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for p,b in sorted(files.items())]},indent=2)+'\n').encode()
out=ROOT/'Astra_Finite_LO_Bus_Receiver_20261031.zip'
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p,b in sorted(files.items()):
  info=zipfile.ZipInfo(p,(2026,10,31,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,b)
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None and set(z.namelist())==set(files)
 assert all(z.read(p)==b for p,b in files.items())
 extracted=Path(tempfile.mkdtemp(prefix='finite_lo_package_replay_'));z.extractall(extracted)
run=extracted/'run';run.mkdir()
for d in ['author','review']:
 for p in (extracted/d).iterdir():
  if p.is_file():shutil.copy2(p,run/p.name)
results=[]
for script in ['certify_finite_lo.py','test_finite_lo.py','independent_finite_lo_audit.py','independent_interval_bucket_audit.py']:
 p=subprocess.run([sys.executable,script],cwd=run,text=True,capture_output=True)
 assert p.returncode==0,(script,p.stderr,p.stdout[-2000:])
 results.append({'script':script,'returncode':p.returncode,'stdout_bytes':len(p.stdout)})
for f in ['finite_lo_certificates.json']:
 assert (run/f).read_bytes()==files['author/'+f]
# Frozen inputs remain unchanged after package and extracted-run work.
for f in AUTH:assert (A/f).read_bytes()==files[f'author/{f}']
for f in REV:assert (R/f).read_bytes()==files[f'review/{f}']
verification={'zip':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'members':len(files),'exact_member_readback':True,'CRC_pass':True,'extracted_replay':results,'extracted_certificate_byte_identical':True,'originals_unchanged':True,'accepted_dependency_SHA_and_CRC_verified':True,'dependency_source_copies_exact':True,'extraction_directory':str(extracted)}
out.with_suffix('.zip.verification.json').write_text(json.dumps(verification,indent=2)+'\n');print(json.dumps(verification,indent=2))
