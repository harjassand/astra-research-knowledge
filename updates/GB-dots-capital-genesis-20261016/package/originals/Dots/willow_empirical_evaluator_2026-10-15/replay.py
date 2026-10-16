"""Read-only packet replay: all generated output goes to a disposable copy."""
import pathlib,hashlib,json,tempfile,shutil,subprocess,sys,os,time,platform
P=pathlib.Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify():
 manifest=json.loads((P/'MANIFEST_SHA256.json').read_text())
 for name,h in manifest.items():assert sha(P/name)==h,('Hash mismatch',name)
 return len(manifest)
def same(a,b):assert a==b,'Saved scientific result differs from replay'
start=time.monotonic();count=verify();steps=[]
with tempfile.TemporaryDirectory(prefix='willow-evaluator-') as temporary:
 Q=pathlib.Path(temporary)/'packet';shutil.copytree(P,Q)
 env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
 for script in ['measured_syndrome_audit/audit.py','measured_syndrome_audit/raw_reference_structure.py','measured_noise_independence/analyze.py','measured_syndrome_audit/audit_dem_pairs.py','calibration_state_response/analyze.py','calibration_state_response/audit_controls.py']:
  t=time.monotonic();r=subprocess.run([sys.executable,str(Q/script)],cwd=Q,env=env,capture_output=True,text=True,timeout=150)
  if r.returncode:raise RuntimeError(script+'\n'+r.stdout+'\n'+r.stderr)
  steps.append({'script':script,'exit_code':r.returncode,'wall_seconds':round(time.monotonic()-t,4)});print('PASS '+script,flush=True)
 for name in ['measured_syndrome_audit/audit_results.json','measured_syndrome_audit/r50_independent_map.json','measured_syndrome_audit/r13_independent_map.json','measured_syndrome_audit/reference_self_checks.json','measured_syndrome_audit/r50_raw_reference_structure.json','measured_syndrome_audit/r13_raw_reference_structure.json','measured_syndrome_audit/independent_dem_pair_audit.json','measured_noise_independence/frozen_family.json','measured_noise_independence/pair_results.csv','calibration_state_response/all_results.json','calibration_state_response/all_results.csv','calibration_state_response/verified_mapping.json']:
  same((P/name).read_bytes(),(Q/name).read_bytes())
 # Remove only runtime/resource/provenance fields that legitimately vary on replay.
 for name,drop in [('measured_noise_independence/results_summary.json',{'cpu_seconds','max_rss_KiB'}),('calibration_state_response/summary.json',{'runtime_seconds','peak_rss_kib','sha256'}),('calibration_state_response/control_design_audit.json',{'source_README_path','sha256'})]:
  a=json.loads((P/name).read_text());b=json.loads((Q/name).read_text());same({k:v for k,v in a.items() if k not in drop},{k:v for k,v in b.items() if k not in drop})
 # Deterministic split, exhaustive disjointness, and original input bytes unchanged.
 order=sorted(range(50000),key=lambda i:hashlib.sha256(('astra-willow-split-v1:'+str(i)).encode()).digest())
 for name,expected in [('diagnostic_indices',order[:25000]),('reserved_indices',order[25000:])]:
  same(list(map(int,(P/'measured_syndrome_audit'/f'{name}.txt').read_text().splitlines())),expected)
 for f in (P/'measured_syndrome_acquisition/data').rglob('*'):
  if f.is_file():same(sha(f),sha(Q/f.relative_to(P)))
verify()
print(json.dumps({'status':'PASS','packet_files_verified':count,'scientific_output_comparisons':'Exact bytes or exact JSON after excluding listed runtime/provenance fields','packet_unchanged':True,'original_data_unchanged':True,'new_reserved_outcome_analyses':0,'steps':steps,'elapsed_seconds':round(time.monotonic()-start,3),'python':sys.version,'platform':platform.platform()},indent=2))
