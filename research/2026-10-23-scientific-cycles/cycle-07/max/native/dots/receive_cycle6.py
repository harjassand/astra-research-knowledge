"""Portable finite source/analysis receipt, not experiment or physical admission."""
from pathlib import Path
import hashlib,json,os,platform,resource,shutil,subprocess,sys,tempfile,time
D=Path(__file__).resolve().parent
pins={'preserved/Astra_Amplification_Cycle5_DOTS_20261022.zip':'7037da7e85b90a6827d01bce778bf5c7740392f47f9720bde596b933c539eb53','nitrogen_cycle6_20261022/electrodeless_evidence/2026_forced_intrinsic.pdf':'33732918a0fd939e7b08dbd9b4c18d63850ce53ebd78f8c8e6011d3b3991a518','nitrogen_cycle6_20261022/observed_operation/intrinsic.jpeg':'8e5a476c15619701cd1c1c033a38d9a8edb993a277ece052658071587e7bcb4b'}
for n,h in pins.items():assert hashlib.sha256((D/n).read_bytes()).hexdigest()==h,n
entries=[]
for l in (D/'SHA256SUMS').read_text().splitlines():
 h,n=l.split('  ',1);assert hashlib.sha256((D/n).read_bytes()).hexdigest()==h,n;entries.append(n)
cmds=['observed_operation/bind_source.py','observed_operation/digitize.py','observed_operation/admission.py','observed_operation/ordering_proof.py','independent_comparison/independent_fig7_read.py','electrodeless_evidence/digitize_figures.py']
env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1');rows=[];start=time.monotonic();logs=D/'receiver_logs';logs.mkdir(exist_ok=True)
def cap():resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
with tempfile.TemporaryDirectory(prefix='dots_cycle6_') as t:
 root=Path(t)/'payload';shutil.copytree(D,root,ignore=shutil.ignore_patterns('__pycache__','receiver_logs','RELOCATION_RECEIPT.json'))
 for i,name in enumerate(cmds):
  s=time.monotonic();r=subprocess.run([sys.executable,str(root/'nitrogen_cycle6_20261022'/name)],cwd=root,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=30,preexec_fn=cap)
  (logs/f'{i+1}.log').write_text(r.stdout);rows.append({'entrypoint':name,'exit_code':r.returncode,'elapsed_s':time.monotonic()-s});(D/'RELOCATION_RECEIPT.json').write_text(json.dumps({'status':'in_progress' if r.returncode==0 else 'failed','jobs':rows},indent=2))
  if r.returncode:raise RuntimeError(f'{name} failed; log {i+1}')
 for name in ['observed_operation/source_binding.json','observed_operation/digitized.json','observed_operation/admission.json','observed_operation/ordering_proof.json','independent_comparison/independent_ratios.json','electrodeless_evidence/digitization_receipt.json']:
  shutil.copy2(root/'nitrogen_cycle6_20261022'/name,logs/name.replace('/','__'))
import numpy,PIL,fitz
r={'status':'passed_six_finite_entrypoints_not_physical_certificate','input_pins':pins,'manifest_files_verified':len(entries),'jobs':rows,'elapsed_total_s':time.monotonic()-start,'receiver_RSS_KiB_Linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'children_peak_RSS_KiB_Linux':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'child_address_space_cap_GiB':2,'child_wall_timeout_s':30,'versions':{'python':platform.python_version(),'numpy':numpy.__version__,'Pillow':PIL.__version__,'PyMuPDF':fitz.VersionBind},'limits':['Only finite chart/arithmetic/proof code, not flow/kinetics or an experimental replication.','Graphical envelopes not confidence intervals; no complete physical/error certificate.','Receipt runtime is not total research/discovery cost; child peak is high-water, not aggregate parallel RSS.'],'no_old_tests_or_trajectories':True}
(D/'RELOCATION_RECEIPT.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
