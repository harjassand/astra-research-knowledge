"""Strict local kinetic package: explicit immutable manifests, no recursive selection."""
from pathlib import Path,PurePosixPath
import hashlib,json,zipfile,tempfile,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
S='radial_kinetic_service_20261031';A='audit_kinetic_service_whole_20261031_2153'
selected={};roles={}
def sha(b):return hashlib.sha256(b).hexdigest()
def add(name,h=None,size=None,role='accepted source or receipt'):
 p=PurePosixPath(name);assert not p.is_absolute() and '..'not in p.parts and str(p)==name
 f=ROOT/name;assert f.is_file() and not f.is_symlink();b=f.read_bytes()
 if h:assert sha(b)==h,(name,'hash')
 if size is not None:assert len(b)==size,(name,'size')
 selected[name]=b;roles[name]=role;return b
f=json.loads(add(S+'/FROZEN_SHA256.json','edb99e8bc6284fd7bd18a6248cec114ecca83e5b5771d0748193460d81dc81ad'))
for n,v in f['files'].items():add(S+'/'+n,v['sha256'],v['bytes'],v['role'])
a=json.loads(add(A+'/AUDIT_SHA256.json','0ea0354f562e8476c6345ecbc743823cddc125f889e839083dbff2d135686456'))
assert a['author_manifest_sha256']==sha(selected[S+'/FROZEN_SHA256.json'])
for n,v in a['files'].items():add(A+'/'+n,v['sha256'],v['bytes'],'whole code/receiving audit and preserved launch failure')
add('rare_conductance_packaging_20261031/package_kinetic.py',role='packaging infrastructure only')
scan={};markers=[b'/home/',b'/Users/',b'producer-workspace/scratch',b'BEGIN PRIVATE KEY',b'BEGIN RSA PRIVATE KEY',b'ghp_']
for n,b in selected.items():
 # Keep the immutable disclosure of a denied generic out-of-workspace target.
 # This historical target is never read, written, or retried by packaging.
 if n in [A+'/WHOLE_REVIEW.md',A+'/initial_command_scope_error.json']:
  b=b.replace(b'producer-workspace/author_replay_stdout.txt',b'[PRESERVED_GENERIC_DENIED_TARGET]')
 if n.endswith('/package_kinetic.py'):
  scan[n]='PASS; own marker definitions and exact historical-path exception';continue
 hits=[x.decode()for x in markers if x in b]
 assert not hits,(n,hits)
 scan[n]='PASS; exact historical denied-target disclosure retained' if n in [A+'/WHOLE_REVIEW.md',A+'/initial_command_scope_error.json']else'PASS'
readme='''# Reviewed exact kinetic lift and clamped-energy CDF\n\nWhole conjunction PASS: audit_kinetic_service_whole_20261031_2153/WHOLE_REVIEW.md. 988 author plus 1,152 independent checks; all four saved cases and the standalone raw pair actually replayed. Historical frozen status strings are preserved; later source-bound acceptance receipts resolve them.\n\nThe theorem proves exact all-start (Y,U) path-law projection for a specified engineered radial-plus-tangent divergence-form tensor, allowing full SPD away from the unvisited origin. The executable receives only fixed finite external clamp protocols and terminal energy CDFs to requested ABSOLUTE interval width. It does not solve autonomous latency, relative rare-probability error, empirical model acquisition, full angular Gibbs sampling, or physical actuation. Ordinary CIR/Gamma and metric-design overlap is explicit.\n\nAll proof, code, costs, correction history and independent receipts are local. The only retained absolute workspace reference is the auditor's immutable disclosure of a denied generic out-of-workspace log target; no such target is read or retried. Unreviewed warm notes and later autonomous/control ideas are excluded.\n\nFrom this extracted root run python -B PACKAGE_REPLAY.py for the small original-task receiving replay. Full tests run from radial_kinetic_service_20261031 with SymPy and scipy installed; scipy checks are diagnostics only. Production is standard-library Python.\n'''
selected['PACKAGE_README.md']=readme.encode();roles['PACKAGE_README.md']='scope/navigation'
replay='''from pathlib import Path\nfrom fractions import Fraction as F\nimport sys,json\np=Path(__file__).resolve().parent/'radial_kinetic_service_20261031'\nsys.path.insert(0,str(p))\nimport receive_kinetic as c\nraw=json.loads((p/'small_raw_fixture.json').read_text())\ncert=json.loads((p/'small_certificate.json').read_text())\n# External original task reconstructed literally, not accepted from the certificate.\ntask=dict(initial_state=[F(1)]+[F(0)]*7,protocol=[{'y':F(-1),'duration':F(1,3)},{'y':F(0),'duration':F(1,2)},{'y':F(1,2),'duration':F(2,3)}],threshold=F(1),cdf_absolute_error=F(1,10**10))\nprint(json.dumps(c.verify(raw,cert,**task),sort_keys=True))\n'''
selected['PACKAGE_REPLAY.py']=replay.encode();roles['PACKAGE_REPLAY.py']='extracted original-task receiving replay'
index={'schema':'strict_local_kinetic_package.v1','scope':'accepted engineered-generator fixed-clamp terminal energy CDF, absolute accuracy','files':{n:{'bytes':len(b),'sha256':sha(b),'role':roles[n]}for n,b in sorted(selected.items())},'private_path_check':scan,'uploads':'NONE'}
selected['PACKAGE_MANIFEST.json']=(json.dumps(index,indent=2)+'\n').encode()
archive=ROOT/'Astra_Exact_Kinetic_Lift_and_Clamped_Energy_CDF_20261031.zip';assert not archive.exists(),'refusing overwrite'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for n,b in sorted(selected.items()):z.writestr(n,b)
with zipfile.ZipFile(archive)as z:
 assert z.testzip()is None and len(z.namelist())==len(set(z.namelist()))==len(selected)
 for n,b in selected.items():assert z.read(n)==b
 with tempfile.TemporaryDirectory(prefix='kinetic_package_replay_')as tmp:
  z.extractall(tmp);replay=subprocess.run([sys.executable,'-B','PACKAGE_REPLAY.py'],cwd=tmp,capture_output=True,text=True,check=True)
  assert json.loads(replay.stdout)['status']=='PASS'
for n,b in selected.items():
 if n not in ['PACKAGE_README.md','PACKAGE_REPLAY.py','PACKAGE_MANIFEST.json']:assert (ROOT/n).read_bytes()==b
v=f['earlier_robustness_package_unchanged'];b=(ROOT/v['path']).read_bytes();assert len(b)==v['bytes']and sha(b)==v['sha256']
report={'path':str(archive),'bytes':archive.stat().st_size,'sha256':sha(archive.read_bytes()),'members':len(selected),'CRC_readback_bindings':'PASS','private_path_allowlist':'PASS; exact denied generic log target disclosure retained','extracted_original_task_receiver':json.loads(replay.stdout),'all_originals_and_earlier_robustness_archive':'UNCHANGED','uploads':'NONE'}
archive.with_suffix('.verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
