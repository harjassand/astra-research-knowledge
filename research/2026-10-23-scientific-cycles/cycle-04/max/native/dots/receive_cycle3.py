"""Finite relocated receipt. No ODE/PDE integration or scientific-status promotion."""
from pathlib import Path
import hashlib,json,time,resource,subprocess,sys
T=time.monotonic();R=Path(__file__).resolve().parent
PINS={'nitrogen_finite_cycle_20261021/thermo_helper/cache.npz': '2a43019386d848c14eeea2e301932c0844bd429f3ccc362a46b3e5b6d728da4d', 'nitrogen_finite_cycle_20261021/thermo_helper/manifest.json': 'd274e6a10a6dcbb99506484d6ef58d00b9dc5a09e1303dee1389f48520db40f0', 'nitrogen_admissibility_20261022/recycle_quench/once_through_2700_reference.npz': '85e7a4a2195c75d2376b9b669f27190be81879dcbbc8881afe6e46d4dc9e968a', 'nitrogen_admissibility_20261022/recycle_quench/mix_tau_0p0001_trajectory.npz': '8b2b1a698503ed11772380eec623230faf1a0c5407ef4d79cec5bb2976ad589e'}
for p,h in PINS.items():
 assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h,p
p=subprocess.run([sys.executable,str(R/'nitrogen_lamella_20261022/exact_endpoint_certificate.py')],cwd=R,capture_output=True,text=True)
assert p.returncode==0,p.stderr
j=json.loads((R/'nitrogen_lamella_20261022/exact_endpoint_certificate.json').read_text())
x=[r for r in j['rows'] if r['contract']=='enthalpy_isobaric' and r['NOx_cap_factor']=='101/100'][0]
assert abs(x['float_for_display_J_kg_fresh']-53995.1352243)<1e-5
c=json.loads((R/'nitrogen_lamella_20261022/compressible_sparse_width400um_N12_result.json').read_text())
out={'receipt':'input binding and exact stored-coefficient endpoint replay only','pinned_inputs':PINS,'endpoint_J_kg_fresh':x['float_for_display_J_kg_fresh'],'capability_admitted':False,'elapsed_s':time.monotonic()-T,'receiver_peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'child_peak_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'source_hashes_are_current_not_retrospective_execution_proof':True}
(R/'RELOCATION_RECEIPT.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
