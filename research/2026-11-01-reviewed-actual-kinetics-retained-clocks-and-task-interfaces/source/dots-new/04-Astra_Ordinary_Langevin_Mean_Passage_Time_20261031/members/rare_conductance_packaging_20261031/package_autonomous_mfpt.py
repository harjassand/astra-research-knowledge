"""Strict local package after a pinned whole-review acceptance, never before."""
from pathlib import Path,PurePosixPath
import hashlib,json,zipfile,tempfile,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
S='autonomous_radial_mfpt_20261031';A='audit_autonomous_mfpt_whole_20261031_2234'
# Supply the exact independently delivered whole-audit manifest SHA on invocation.
assert len(sys.argv)==2 and len(sys.argv[1])==64,'required source-bound accepted whole-review manifest SHA'
WHOLE_SHA=sys.argv[1];selected={};roles={}
def sha(b):return hashlib.sha256(b).hexdigest()
def add(name,h=None,size=None,role='accepted source or receipt'):
 p=PurePosixPath(name);assert not p.is_absolute() and '..'not in p.parts and str(p)==name
 f=ROOT/name;assert f.is_file()and not f.is_symlink();b=f.read_bytes()
 if h:assert sha(b)==h,(name,'hash')
 if size is not None:assert len(b)==size,(name,'size')
 selected[name]=b;roles[name]=role;return b
def manifest_tree(folder,filename,expected):
 m=json.loads(add(folder+'/'+filename,expected))
 for n,v in m['files'].items():add(folder+'/'+n,v['sha256'],v['bytes'],v.get('role','source-bound source or review'))
 return m
f=manifest_tree(S,'FROZEN_SHA256.json','d56d3514bff7af7062137347065401df0364823c1223087471f9b036bb73f51e')
a=manifest_tree(A,'AUDIT_SHA256.json',WHOLE_SHA)
# Refuse a receipt that does not bind the exact author manifest.
assert a['author_manifest_sha256']==sha(selected[S+'/FROZEN_SHA256.json'])
k=manifest_tree('radial_kinetic_service_20261031','FROZEN_SHA256.json','edb99e8bc6284fd7bd18a6248cec114ecca83e5b5771d0748193460d81dc81ad')
ka=manifest_tree('audit_kinetic_service_whole_20261031_2153','AUDIT_SHA256.json','0ea0354f562e8476c6345ecbc743823cddc125f889e839083dbff2d135686456')
for n,v in f['dependencies'].items():add(n,v['sha256'],v['bytes'],'exact inherited dependency')
archive_old='Astra_Exact_Kinetic_Lift_and_Clamped_Energy_CDF_20261031.zip'
add(archive_old,'2184b8194297af716a12c89267c49dcc52f83b4dfd1377708bb1acd5296c9f2e',112784,'unchanged accepted constituent archive')
add('rare_conductance_packaging_20261031/package_autonomous_mfpt.py',role='packaging infrastructure only')
markers=[b'/home/',b'/Users/',b'producer-workspace/scratch',b'BEGIN PRIVATE KEY',b'BEGIN RSA PRIVATE KEY',b'ghp_'];scan={}
for n,b in selected.items():
 if n.endswith('.zip'):scan[n]='unchanged already-checked constituent archive';continue
 if n.endswith('/package_autonomous_mfpt.py'):scan[n]='PASS; own marker definitions and historical-path exception';continue
 if n in ['audit_kinetic_service_whole_20261031_2153/WHOLE_REVIEW.md','audit_kinetic_service_whole_20261031_2153/initial_command_scope_error.json']:
  b=b.replace(b'producer-workspace/author_replay_stdout.txt',b'[PRESERVED_GENERIC_DENIED_TARGET]')
 hits=[x.decode()for x in markers if x in b];assert not hits,(n,hits);scan[n]='PASS'
selected['PACKAGE_README.md']=b'''# Reviewed autonomous radial-gain mean hitting-time receiver

This local package contains the newly received autonomous Gibbs|A mean first-passage proof/receiver, and unchanged accepted kinetic-lift dependency with its correction/prior-overlap history. Read the source-bound whole-review receipt before historic candidate status strings.

The actual model has a declared engineered radial mobility gain and tangent diffusion. The observable is an autonomous mean, not capacity inversion or clamped terminal CDF. Exact initialization is required. Approximate finite-bit sampling, physical parameters/actuation, and the original constant-mobility model are NOT authenticated. The separate later constant-SPD extension is deliberately excluded.

Run python -B PACKAGE_REPLAY.py from this extracted root for one small receiving replay with the original external task reconstructed literally. Full tests are in autonomous_radial_mfpt_20261031; SymPy and mpmath diagnostics are separate from the standard-library producer. No upload was performed.
''';roles['PACKAGE_README.md']='scope/navigation'
selected['PACKAGE_REPLAY.py']=b'''from pathlib import Path
from fractions import Fraction as F
import sys,json
p=Path(__file__).resolve().parent/'autonomous_radial_mfpt_20261031'
sys.path.insert(0,str(p))
import receive_mfpt as c
raw=json.loads((p/'small_raw_fixture.json').read_text())
cert=json.loads((p/'small_certificate.json').read_text())
print(json.dumps(c.verify(raw,cert,beta=F(1),kappa=F(1),quad_relative=F(1,1000),full_ratio=F(11,10)),sort_keys=True))
''';roles['PACKAGE_REPLAY.py']='small original-task replay'
index={'schema':'strict_local_autonomous_mfpt_package.v1','files':{n:{'bytes':len(b),'sha256':sha(b),'role':roles[n]}for n,b in sorted(selected.items())},'private_path_check':scan,'uploads':'NONE'}
selected['PACKAGE_MANIFEST.json']=(json.dumps(index,indent=2)+'\n').encode()
archive=ROOT/'Astra_Autonomous_Radial_Mean_Passage_Time_20261031.zip';assert not archive.exists(),'refusing overwrite'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for n,b in sorted(selected.items()):z.writestr(n,b)
with zipfile.ZipFile(archive)as z:
 assert z.testzip()is None and len(z.namelist())==len(set(z.namelist()))==len(selected)
 for n,b in selected.items():assert z.read(n)==b
 with tempfile.TemporaryDirectory(prefix='autonomous_mfpt_package_replay_')as tmp:
  z.extractall(tmp);replay=subprocess.run([sys.executable,'-B','PACKAGE_REPLAY.py'],cwd=tmp,capture_output=True,text=True,check=True);assert json.loads(replay.stdout)['status']=='PASS'
for n,b in selected.items():
 if n not in ['PACKAGE_README.md','PACKAGE_REPLAY.py','PACKAGE_MANIFEST.json']:assert(ROOT/n).read_bytes()==b
report={'path':str(archive),'bytes':archive.stat().st_size,'sha256':sha(archive.read_bytes()),'members':len(selected),'CRC_readback_bindings':'PASS','private_path_allowlist':'PASS; inherited exact historical denied-target disclosure retained','extracted_original_task_receiver':json.loads(replay.stdout),'all_originals_and_constituent_archive':'UNCHANGED','uploads':'NONE'}
archive.with_suffix('.verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
