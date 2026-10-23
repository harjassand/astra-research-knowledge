"""Finite relocated source receipt. No old trajectory, heater or continuum solve."""
from pathlib import Path
import hashlib,json,time,subprocess,sys,resource,os
R=Path(__file__).resolve().parent;start=time.monotonic()
PINS={'nitrogen_cycle0001_20261022/mode_evidence/2017_numeric_assignments.txt': '50f5839881d1dc1244a36090fa09bf174f9ef99bed01dbeef54698e9c9c32c55', 'nitrogen_lamella_20261022/restored_cross_width400um_N48_trajectory.npz': '1c1346d781bd155a441fdbfa3f4968b70581bba15becd985edb3f80dfc00449c', 'nitrogen_admissibility_20261022/recycle_quench/result.json': '6421b82f3b8b4399b535dd259d047e6054d612ac50bdf551db0685dbbe0eb29c', 'nitrogen_finite_cycle_20261021/thermo_helper/cache.npz': '2a43019386d848c14eeea2e301932c0844bd429f3ccc362a46b3e5b6d728da4d', 'nitrogen_finite_cycle_20261021/thermo_helper/manifest.json': 'd274e6a10a6dcbb99506484d6ef58d00b9dc5a09e1303dee1389f48520db40f0'}
for rel,h in PINS.items():assert hashlib.sha256((R/rel).read_bytes()).hexdigest()==h,rel
jobs=['headroom_check/check.py','state_contraction/contract_on2.py','state_contraction/moment_bounds.py','state_contraction/synthetic_reverse_probe.py','state_independent/check_contraction.py','state_independent/check_moment_lp.py']
rows=[];env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
for name in jobs:
 p=R/'nitrogen_cycle0001_20261022'/name;t=time.monotonic();sha=hashlib.sha256(p.read_bytes()).hexdigest();a=subprocess.run([sys.executable,str(p)],cwd=R,env=env,capture_output=True,text=True,timeout=60)
 rows.append({'source':str(p.relative_to(R)),'source_sha256_before_execution':sha,'exit_code':a.returncode,'elapsed_s':time.monotonic()-t,'stdout_sha256':hashlib.sha256(a.stdout.encode()).hexdigest(),'stderr':a.stderr})
 (R/'RELOCATION_PROGRESS.json').write_text(json.dumps(rows,indent=2))
 assert a.returncode==0,(name,a.stderr)
import numpy,scipy,mpmath
out={'scope':__doc__,'pins':PINS,'jobs':rows,'versions':{'python':sys.version,'numpy':numpy.__version__,'scipy':scipy.__version__,'mpmath':mpmath.__version__},'total_elapsed_s':time.monotonic()-start,'receiver_peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'children_peak_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'physical_capability_admitted':False,'publication_originality_established':False,'total_research_cost_known':False}
(R/'RELOCATION_RECEIPT.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
