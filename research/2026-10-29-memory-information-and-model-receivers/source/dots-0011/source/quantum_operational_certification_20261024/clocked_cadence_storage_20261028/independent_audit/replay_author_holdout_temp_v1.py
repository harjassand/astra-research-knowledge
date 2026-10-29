from pathlib import Path
import json,hashlib,importlib.util,tempfile,shutil,contextlib,io,numpy as np
A=Path(__file__).parent;S=A.parent
spec=importlib.util.spec_from_file_location('holdout_author_temp',S/'learn_cadence_holdout_v1.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
originals={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in S.iterdir() if f.is_file()}
with tempfile.TemporaryDirectory(prefix='cadence_holdout_replay_') as td:
 t=Path(td)
 for name in ['HOLDOUT_PLAN_v1.json','results_v2.json']:shutil.copy2(S/name,t/name)
 m.HERE=t
 with contextlib.redirect_stdout(io.StringIO()):m.main()
 a=np.load(S/'holdout_counts_v1.npz');b=np.load(t/'holdout_counts_v1.npz');assert set(a.files)==set(b.files);assert all(np.array_equal(a[k],b[k]) for k in a.files)
 x=json.loads((S/'holdout_results_v1.json').read_text());y=json.loads((t/'holdout_results_v1.json').read_text());assert x==y
 assert json.loads((S/'holdout_CDFs_v1.json').read_text())==json.loads((t/'holdout_CDFs_v1.json').read_text())
assert originals=={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in S.iterdir() if f.is_file()}
out={'status':'PASS_AUTHOR_HOLDOUT_REPLAY_IN_TEMPORARY_DIRECTORY','raw_counts_equal':True,'full_results_JSON_equal':True,'CDF_JSON_equal':True,'original_source_directory_hashes_unchanged':True}
(A/'replay_author_holdout_temp_v1.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
