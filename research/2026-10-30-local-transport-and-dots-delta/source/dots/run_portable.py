"""Run a scientific program in a temporary, path-relocated copy.
Original files/receipts remain intact. Only literal producer-workspace/shared strings
in temporary Python copies are replaced by the temporary tree path. This is
path relocation, not new reviewed scientific source or a new numerical method.
"""
import pathlib,tempfile,shutil,subprocess,sys,os,json,hashlib
root=pathlib.Path(__file__).resolve().parent
if len(sys.argv)<2:raise SystemExit('Usage: python run_portable.py relative/topic/program.py [args]')
rel=pathlib.PurePosixPath(sys.argv[1]);assert not rel.is_absolute() and '..' not in rel.parts
work=pathlib.Path(tempfile.mkdtemp(prefix='astra_replay_'))/'package';shutil.copytree(root,work)
subprocess.run([sys.executable,str(work/'restore_aliases.py')],check=True)
changes=[]
for p in work.rglob('*.py'):
 if p.name in {'run_portable.py','restore_aliases.py'}:continue
 old=p.read_text();new=old.replace('producer-workspace/shared',str(work)+'/').replace('producer-workspace/57d8dd795b13',str(work)+'/')
 if old!=new:
  changes.append({'path':str(p.relative_to(work)),'original_sha256':hashlib.sha256(old.encode()).hexdigest(),'relocated_sha256':hashlib.sha256(new.encode()).hexdigest()});p.write_text(new)
(work/'PATH_RELOCATION_RECEIPT.json').write_text(json.dumps(changes,indent=2)+'\n')
print('Replay working copy:',work,flush=True)
env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
result=subprocess.run([sys.executable,str(work/rel),*sys.argv[2:]],cwd=work/rel.parent,env=env)
raise SystemExit(result.returncode)
