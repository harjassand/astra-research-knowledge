import tempfile,pathlib,shutil,subprocess,sys,numpy as np,json
p=pathlib.Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as td:
 root=pathlib.Path(td);q=root/p.name;q.mkdir();other=root/'compact_prequential_flag_recovery_20261028';other.mkdir()
 shutil.copy2(p/'negative_source_meta_fixture_v1.py',q/'negative_source_meta_fixture_v1.py')
 for name in ['quantum_memory_fixture_v1.py','check_compressed_projection_v1.py']:shutil.copy2(p.parent/other.name/name,other/name)
 subprocess.run([sys.executable,str(q/'negative_source_meta_fixture_v1.py')],check=True,capture_output=True,text=True)
 rec=np.array_equal(np.load(q/'negative_source_meta_records_v1.npy'),np.load(p/'negative_source_meta_records_v1.npy'))
 res=json.loads((q/'negative_source_meta_fixture_v1.json').read_text())==json.loads((p/'negative_source_meta_fixture_v1.json').read_text())
 assert rec and res
out={'records_identical':rec,'results_identical':res,'simulated_records':192,'scope':'Temporary replay of new mixed-role occupation on previously checked source; reused seeds are not independent evidence.'}
pathlib.Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
