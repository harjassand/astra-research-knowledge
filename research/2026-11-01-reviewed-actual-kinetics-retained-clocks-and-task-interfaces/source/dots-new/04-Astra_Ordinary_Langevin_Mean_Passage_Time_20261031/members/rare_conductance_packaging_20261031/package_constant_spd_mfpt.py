"""Package only after an independently delivered exact whole-review manifest."""
from pathlib import Path,PurePosixPath
import hashlib,json,zipfile,tempfile,subprocess,sys,io
ROOT=Path(__file__).resolve().parents[1];S='constant_spd_mfpt_20261031';T='audit_constant_spd_mfpt_theorem_20261031_2239'
assert len(sys.argv)==3,'whole audit folder and exact delivered manifest SHA required'
A,H=sys.argv[1:];assert len(H)==64 and not PurePosixPath(A).is_absolute()and '..'not in PurePosixPath(A).parts
selected={};roles={}
def sha(b):return hashlib.sha256(b).hexdigest()
def add(name,h=None,size=None,role='accepted source or receipt'):
 p=PurePosixPath(name);assert not p.is_absolute()and '..'not in p.parts and str(p)==name
 f=ROOT/name;assert f.is_file()and not f.is_symlink();b=f.read_bytes()
 if h:assert sha(b)==h,(name,'hash')
 if size is not None:assert len(b)==size,(name,'size')
 if name in selected:assert selected[name]==b
 selected[name]=b;roles[name]=role;return b
def tree(folder,filename,h):
 m=json.loads(add(folder+'/'+filename,h))
 for n,v in m['files'].items():add(folder+'/'+n,v['sha256'],v['bytes'],v.get('role','exact source-bound source or receipt'))
 return m
f=tree(S,'FROZEN_SHA256_v2.json','61ace87427769d160cc0c6121377298f02b914059f5018eafe8bc0e30614c298')
t=tree(T,'AUDIT_SHA256.json','cf939d15d0f957b7c50cf4534925cd3adbea325dc40d46aa767131df4bb81a72')
a=tree(A,'AUDIT_SHA256.json',H);assert a['author_v2_manifest_sha256']==sha(selected[S+'/FROZEN_SHA256_v2.json'])
old='Astra_Autonomous_Radial_Mean_Passage_Time_20261031.zip'
b=add(old,'b101a6a7ab75b5e47d0685f2cd9e143d2ffdc54b7e83478921d08553fe478283',317838,'unchanged accepted constituent archive')
# The earlier archive is a previously verified strict allowlist, not recursive
# filesystem selection. Preserve its source-relative members, excluding only
# its top-level packaging navigation (the complete archive stays unchanged).
with zipfile.ZipFile(io.BytesIO(b))as z:
 assert z.testzip()is None
 oldindex=json.loads(z.read('PACKAGE_MANIFEST.json'))
 assert set(z.namelist())==set(oldindex['files'])|{'PACKAGE_MANIFEST.json'}
 for n,v in oldindex['files'].items():
  data=z.read(n);assert len(data)==v['bytes']and sha(data)==v['sha256']
  if n in ['PACKAGE_README.md','PACKAGE_REPLAY.py']:continue
  add(n,v['sha256'],v['bytes'],'unchanged accepted radial/kinetic dependency tree')
for n,v in f['dependencies'].items():add(n,v['sha256'],v['bytes'],'exact inherited dependency')
add('rare_conductance_packaging_20261031/package_constant_spd_mfpt.py',role='packaging infrastructure only')
add('rare_conductance_packaging_20261031/constant_spd_package_build_history.json',role='packaging failure/correction history, not source repair')
markers=[b'/home/',b'/Users/',b'producer-workspace/scratch',b'BEGIN PRIVATE KEY',b'BEGIN RSA PRIVATE KEY',b'ghp_'];scan={}
for n,b in selected.items():
 if n.endswith('.zip'):scan[n]='unchanged accepted constituent archive';continue
 if n.startswith('rare_conductance_packaging_20261031/')and n.endswith('.py'):scan[n]='PASS; own marker definitions and exact historical exception';continue
 if n in ['audit_kinetic_service_whole_20261031_2153/WHOLE_REVIEW.md','audit_kinetic_service_whole_20261031_2153/initial_command_scope_error.json']:b=b.replace(b'producer-workspace/author_replay_stdout.txt',b'[PRESERVED_GENERIC_DENIED_TARGET]')
 hits=[x.decode()for x in markers if x in b];assert not hits,(n,hits);scan[n]='PASS'
selected['PACKAGE_README.md']=b'''# Reviewed ordinary constant-SPD Langevin mean passage time

The new consumer predicts an exact full Gibbs|A initialized autonomous hitting-time mean for ordinary constant-isotropic/diagonal mobility and acquired positive quartic energy. It does not assume energy Markov closure, angular mixing, an unknown partition oracle or engineered tensor actuation. It does require the complete declared mathematical model and full initial law; no empirical membership or approximate physical preparation is authenticated.

Read the source-bound current whole-review receipt before historical candidate strings. The constant-SPD result, its independent theorem receipt, exact arithmetic/tests/costs/failures and primary comparisons are all preserved. The preceding accepted radial-gain/kinetic source trees and constituent archives remain unchanged, with their narrower and different scopes; they are dependencies, not evidence that the new model inherits their initialization shortcuts.

From this extracted root, python -B PACKAGE_REPLAY.py reruns a small receiver against the literal original external task. Full checks in constant_spd_mfpt_20261031 use SymPy and diagnostic mpmath; the numerical producer is standard-library Python. No upload was performed.
''';roles['PACKAGE_README.md']='scope/navigation'
selected['PACKAGE_REPLAY.py']=b'''from pathlib import Path
from fractions import Fraction as F
import sys,json
p=Path(__file__).resolve().parent/'constant_spd_mfpt_20261031'
sys.path.insert(0,str(p))
import receive_mfpt as c
raw=json.loads((p/'small_raw_fixture.json').read_text())
cert=json.loads((p/'small_certificate.json').read_text())
print(json.dumps(c.verify(raw,cert,beta=F(1),kappa=F(1),quad_relative=F(1,1000),full_ratio=F(11,10)),sort_keys=True))
''';roles['PACKAGE_REPLAY.py']='small original-task receiving replay'
index={'schema':'strict_local_constant_spd_mfpt_package.v1','files':{n:{'bytes':len(b),'sha256':sha(b),'role':roles[n]}for n,b in sorted(selected.items())},'private_path_check':scan,'uploads':'NONE'}
selected['PACKAGE_MANIFEST.json']=(json.dumps(index,indent=2)+'\n').encode()
archive=ROOT/'Astra_Ordinary_Langevin_Mean_Passage_Time_20261031.zip';assert not archive.exists(),'refusing overwrite'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for n,b in sorted(selected.items()):z.writestr(n,b)
with zipfile.ZipFile(archive)as z:
 assert z.testzip()is None and len(z.namelist())==len(set(z.namelist()))==len(selected)
 for n,b in selected.items():assert z.read(n)==b
 with tempfile.TemporaryDirectory(prefix='constant_spd_mfpt_package_replay_')as tmp:
  z.extractall(tmp);replay=subprocess.run([sys.executable,'-B','PACKAGE_REPLAY.py'],cwd=tmp,capture_output=True,text=True,check=True);assert json.loads(replay.stdout)['status']=='PASS'
for n,b in selected.items():
 if n not in ['PACKAGE_README.md','PACKAGE_REPLAY.py','PACKAGE_MANIFEST.json']:assert(ROOT/n).read_bytes()==b
report={'path':str(archive),'bytes':archive.stat().st_size,'sha256':sha(archive.read_bytes()),'members':len(selected),'CRC_readback_bindings':'PASS','private_path_allowlist':'PASS; inherited exact historical denied-target disclosure retained','extracted_original_task_receiver':json.loads(replay.stdout),'all_originals_and_constituent_archives':'UNCHANGED','uploads':'NONE'}
archive.with_suffix('.verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
