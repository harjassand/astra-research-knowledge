"""Execute only a disposable package copy; preserve original scientific bytes."""
from pathlib import Path,PurePosixPath
import tempfile,shutil,subprocess,sys,os,json,hashlib
root=Path(__file__).resolve().parent
if len(sys.argv)<2:raise SystemExit('Usage: python run_portable.py topic/program.py [args]')
rel=PurePosixPath(sys.argv[1]);assert not rel.is_absolute() and '..' not in rel.parts
work=Path(tempfile.mkdtemp(prefix='astra_replay_'))/'package';shutil.copytree(root,work)
changes=[]
# Audit stores this dependency under a flattened archival filename. Recreate its
# byte-identical original basename ONLY in the disposable replay directory.
for src in work.rglob('weak_initiation_compiler_20261030__unified_interface__old_bad_fixture_snapshot.py'):
 dst=src.with_name('old_bad_fixture_snapshot.py')
 if not dst.exists():
  shutil.copyfile(src,dst);changes.append(dict(action='temporary_dependency_alias',source=str(src.relative_to(work)),path=str(dst.relative_to(work)),sha256=hashlib.sha256(src.read_bytes()).hexdigest()))
for p in work.rglob('*.py'):
 if p.name=='run_portable.py':continue
 old=p.read_bytes();new=old.replace(b'producer-workspace/shared',(str(work)+'/').encode()).replace(b'producer-workspace/57d8dd795b13',(str(work)+'/').encode())
 if old!=new:
  changes.append(dict(path=str(p.relative_to(work)),original_sha256=hashlib.sha256(old).hexdigest(),relocated_sha256=hashlib.sha256(new).hexdigest()));p.write_bytes(new)
replay_cwd=work if str(rel)=='chemical_joint_shell_20261030/check_actual_joint.py' else work/rel.parent
if replay_cwd==work:changes.append(dict(action='replay_cwd',path='.',reason='program writes package-root-relative output path'))
(work/'PATH_RELOCATION_RECEIPT.json').write_text(json.dumps(changes,indent=2)+'\n')
print('Replay working copy:',work,flush=True)
result=subprocess.run([sys.executable,str(work/rel),*sys.argv[2:]],cwd=replay_cwd,env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1'))
raise SystemExit(result.returncode)
