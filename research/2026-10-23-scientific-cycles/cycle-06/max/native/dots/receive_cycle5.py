"""Finite portable receipt. No flow/kinetics/heater/evaluator replay."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile,time,resource,platform
D=Path(__file__).resolve().parent
pins={'nitrogen_admissibility_20261022/recycle_quench/once_through_2700_reference.npz':'85e7a4a2195c75d2376b9b669f27190be81879dcbbc8881afe6e46d4dc9e968a','nitrogen_finite_cycle_20261021/thermo_helper/cache.npz':'2a43019386d848c14eeea2e301932c0844bd429f3ccc362a46b3e5b6d728da4d','preserved/Astra_Amplification_Cycle4_DOTS_20261022.zip':'8bf57ce3a795642284230966bcd82c7af9997c9eacfc5a87b77465cddf9313de'}
for n,h in pins.items():assert hashlib.sha256((D/n).read_bytes()).hexdigest()==h,n
entries=[]
for line in (D/'SHA256SUMS').read_text().splitlines():
 h,n=line.split('  ',1);assert hashlib.sha256((D/n).read_bytes()).hexdigest()==h,n;entries.append(n)
commands=['nozzle_admission/calculate.py','nozzle_admission/heat_grade.py','ordinary_energy_boundary/calculate.py','nozzle_independent/check.py','nozzle_independent/comparator_check.py','expansion_evidence/check_surface_envelope.py']
env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1');rows=[];start=time.monotonic()
def limits():
 resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
with tempfile.TemporaryDirectory(prefix='dots_cycle5_') as td:
 root=Path(td)/'work';shutil.copytree(D,root,ignore=shutil.ignore_patterns('__pycache__','RELOCATION_RECEIPT.json','receiver_logs'))
 logs=D/'receiver_logs';logs.mkdir(exist_ok=True)
 for i,name in enumerate(commands):
  t=time.monotonic();r=subprocess.run([sys.executable,str(root/'nitrogen_cycle5_20261022'/name)],cwd=root,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=30,preexec_fn=limits)
  (logs/f'{i+1}.log').write_text(r.stdout);rows.append({'source_entry':name,'exit_code':r.returncode,'elapsed_s':time.monotonic()-t})
  (D/'RELOCATION_RECEIPT.json').write_text(json.dumps({'jobs':rows,'status':'in_progress' if r.returncode==0 else 'failed'},indent=2))
  if r.returncode:raise RuntimeError(f'{name} failed; see receiver_logs/{i+1}.log')
 # Preserve actual new receipt results separately, without replacing frozen outputs.
 for name in ['nozzle_admission/result.json','nozzle_admission/heat_grade.json','ordinary_energy_boundary/result.json','nozzle_independent/result.json','nozzle_independent/comparator_result.json','expansion_evidence/surface_envelope.json']:
  out=logs/(name.replace('/','__'));shutil.copy2(root/'nitrogen_cycle5_20261022'/name,out)
import numpy,scipy,mpmath
out={'status':'passed_six_finite_checks_not_physical_admission','scientific_input_pins':pins,'manifest_entries_verified':len(entries),'jobs':rows,'elapsed_total_s':time.monotonic()-start,'receiver_RSS_KiB_Linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'children_peak_RSS_KiB_Linux':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'per_child_address_space_limit_GiB':2,'per_child_wall_timeout_s':30,'versions':{'python':platform.python_version(),'numpy':numpy.__version__,'scipy':scipy.__version__,'mpmath':mpmath.__version__},'no_old_trajectory_or_meta_tests':True,'no_new_physical_operation_admitted':True,'cost_scope':'Receipt only; not total discovery/research costs. Child peak is getrusage child high-water, not aggregate parallel memory.'}
(D/'RELOCATION_RECEIPT.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
