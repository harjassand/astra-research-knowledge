"""Explicit-manifest local packaging; no directory walk, upload, or source mutation."""
from pathlib import Path,PurePosixPath
import hashlib,json,zipfile,tempfile,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
R='robustness_dilation_capacity_20261031'
A='audit_radial_envelope_receiver_20261031_2125'
L='homogeneous_entropic_capacity_20261031/audit_latency_theorem_20261031_2117'
selected={};roles={}
def sha(b):return hashlib.sha256(b).hexdigest()
def add(name,expected=None,size=None,role='accepted source/receipt'):
 p=PurePosixPath(name)
 assert not p.is_absolute() and '..' not in p.parts and str(p)==name
 f=ROOT/name;assert f.is_file() and not f.is_symlink(),name
 b=f.read_bytes()
 if expected:assert sha(b)==expected,(name,'hash')
 if size is not None:assert len(b)==size,(name,'size')
 if name in selected:assert selected[name]==b
 selected[name]=b;roles[name]=role
 return b
f=json.loads(add(R+'/FROZEN_SHA256.json','0708f30e620bb4f4015eb292a9b76ec5ac005e345af027e38e7a2d63ca3c7cb5'))
for n,v in f['files'].items():add(R+'/'+n,v['sha256'],v['bytes'],v['role'])
for n,v in f['dependencies'].items():add(n,v['sha256'],v['bytes'],'accepted runtime/proof dependency')
a=json.loads(add(A+'/AUDIT_SHA256.json','fb949af60dbf0360b9e24cced459b3279db11083d0867ccc31adc45198adfec4'))
assert a['author_manifest_sha256']==sha(selected[R+'/FROZEN_SHA256.json'])
for n,v in a['files'].items():add(A+'/'+n,v['sha256'],v['bytes'],'whole executable audit')
l=json.loads(add(L+'/AUDIT_SHA256.json'))
for n,v in l.items():add(L+'/'+n,v['sha256'],v['bytes'],'separately accepted latency audit; initial candidate preserved as history')
add('homogeneous_entropic_capacity_20261031/CONDUCTANCE_LATENCY_SEPARATION_ROOT.md','132ac753d4dff456f61eb3e566a113222935dfde54d46e70dc75b4a81a1ac174',role='separately accepted latency theorem')
for name,expected in [
 ('Astra_Mixed_Degree_Geometric_Conductance_20261031.zip','7a02ac12b6441e5bea46a80c5986e17e06f45068dea6398ca22b92247e2e9d74'),
 ('Astra_Finite_Accuracy_Partition_Free_Conductance_20261031.zip','c01cb8da9c41e5fa00ab72b956acb81cbc8343b41e9e6474586cbce4a018b82a'),
 ('Astra_Unknown_Mobility_Range_Conductance_20261031.zip','f82889a92e713378295bc244a3246787d0c5605e052a8d13d92a7e1c5b84bc75')]:
 add(name,expected,role='unchanged accepted constituent archive; full dependency/history source')
# Exact allowlists above, plus this reproducible packaging source. No unreviewed kinetic notes.
add('rare_conductance_packaging_20261031/package_robustness.py',role='packaging infrastructure, not scientific proof')
private_markers=[b'/home/',b'/Users/',b'producer-workspace/scratch',b'BEGIN PRIVATE KEY',b'BEGIN RSA PRIVATE KEY',b'ghp_']
scan={}
for n,b in selected.items():
 if n.endswith('.zip'):continue # These are hash-bound already accepted local archives, not newly selected trees.
 hits=[x.decode() for x in private_markers if x in b]
 # The packaging script contains its own marker definitions; no actual private path is selected.
 if hits and n!='rare_conductance_packaging_20261031/package_robustness.py':raise AssertionError((n,hits))
 scan[n]='PASS (marker definitions only)' if hits else 'PASS'
readme='''# Reviewed robustness, information boundary, and latency scope\n\nThe executable radial-envelope construction has whole PASS: see audit_radial_envelope_receiver_20261031_2125/WHOLE_REVIEW.md (7,856 author + 2,298 independent + 3 boundary assertions). Earlier immutable documents still correctly record their then-pending review state; later source-bound receipts are authoritative acceptance records.\n\nThe raw rational input and global certificates, not empirical identification, earn a common equilibrium capacity/basin-mass interval over fixed block-SPD mobilities. Two actual 513D non-geometric inputs received total ratios 1.00844524 and 1.00892789. Full costs and failed preliminary numerical routes are preserved. No MFPT, physical membership, angular sampler, or arbitrary-start kinetics claim.\n\nSeparate accepted companions establish finite-local-probe information obstructions and conductance/mean-latency separation. Their own bindings and correction history are retained; they are not executable upgrades. Unchanged accepted constituent ZIPs contain complete mathematical/runtime dependency provenance. No radial-control continuation is included.\n\nTo replay the small saved raw input, use the Python verification snippet in PACKAGE_REPLAY.py from this extracted root. The whole audit already actually recomputed all five saved cases; packaging does not repeat expensive generation.\n'''
selected['PACKAGE_README.md']=readme.encode();roles['PACKAGE_README.md']='package navigation and scope'
replay='''from pathlib import Path\nfrom fractions import Fraction\nimport sys,json\nroot=Path(__file__).resolve().parent\nsys.path.insert(0,str(root/'robustness_dilation_capacity_20261031'))\nimport receive_robustness as r\np=root/'robustness_dilation_capacity_20261031'\nraw=json.loads((p/'small_raw_fixture.json').read_text())\ncert=json.loads((p/'small_certificate.json').read_text())\ntask=dict(cert['task'])\nfor k in ['delta','beta','quad_relative','full_ratio']:\n if task[k] is not None:task[k]=Fraction(task[k])\nprint(json.dumps(r.verify(raw,cert,**task),sort_keys=True))\n'''
selected['PACKAGE_REPLAY.py']=replay.encode();roles['PACKAGE_REPLAY.py']='packaging extracted receiving replay'
index={'schema':'strict_local_robustness_package.v1','scope':'Whole accepted raw radial-envelope conductance; separately accepted information/latency boundaries',
 'files':{n:{'sha256':sha(b),'bytes':len(b),'role':roles[n]} for n,b in sorted(selected.items())},'private_path_scan':scan,'uploads':'NONE'}
selected['PACKAGE_MANIFEST.json']=(json.dumps(index,indent=2)+'\n').encode()
archive=ROOT/'Astra_Robust_Rare_Conductance_and_Information_Boundaries_20261031.zip'
assert not archive.exists(),'Refusing overwrite'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for n,b in sorted(selected.items()):z.writestr(n,b)
with zipfile.ZipFile(archive)as z:
 assert z.testzip()is None and len(z.namelist())==len(set(z.namelist()))==len(selected)
 for n,b in selected.items():assert z.read(n)==b
 with tempfile.TemporaryDirectory(prefix='robustness_package_replay_')as tmp:
  z.extractall(tmp)
  replay=subprocess.run([sys.executable,'-B','PACKAGE_REPLAY.py'],cwd=tmp,capture_output=True,text=True,check=True)
  assert json.loads(replay.stdout)['status']=='PASS'
# All source originals and every constituent ZIP must remain unchanged.
for n,b in selected.items():
 if n not in ['PACKAGE_README.md','PACKAGE_REPLAY.py','PACKAGE_MANIFEST.json']:assert (ROOT/n).read_bytes()==b,n
report={'path':str(archive),'bytes':archive.stat().st_size,'sha256':sha(archive.read_bytes()),'members':len(selected),'CRC_readback_hashes':'PASS','private_path_and_allowlist':'PASS','extracted_small_receiving_replay':json.loads(replay.stdout),'expensive_cases':'not repeated in packaging; five actual cases already replayed in whole audit','all_originals':'UNCHANGED','uploads':'NONE'}
archive.with_suffix('.verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
