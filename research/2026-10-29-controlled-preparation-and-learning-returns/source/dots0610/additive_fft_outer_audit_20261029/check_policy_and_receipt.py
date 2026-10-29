from pathlib import Path
import json,hashlib,sys,numpy as np
from fractions import Fraction
p=Path(__file__).parent;s=p.parent/'additive_fft_outer_compiler_20261029';d=p.parent/'guard_policy_optimization_20261029'
sys.path.insert(0,str(d));from embedded_chain import evaluate,nb_tail
x=json.load(open(s/'nearby_B2048_policies.json'));a=np.load(d/'reviewed_fixture_arrays.npz');m=np.load(d/'matching_memory_maps.npz');u=np.load(d/'two_MUB_XZ_maps.npz')
maps={'matching':(m['pass_map'],m['fail_map']),'six_state':(a['two_pass'],a['two_fail']),'weighted_exact':(a['weighted_pass'],a['weighted_fail']),'two_MUB_XZ':(u['pass_map'],u['fail_map'])};rows=[]
for row in x['rows']:
 r=evaluate(*maps[row['test']],a['good']+a['bad'],a['sigma'],float(Fraction(row['s'])),row['J'],row['b'])
 err=max(abs(r[k]-row[k]) for k in r);assert err<1e-6
 for eps,key in [(Fraction(1,128),'t_guard_1_over128'),(Fraction(1,256),'radius_for_guard_1_over256_same_policy')]:
  t=row[key];assert nb_tail(t,row['b'],row['R'])<=eps and nb_tail(t-1,row['b'],row['R'])>eps
 assert row['payload_qubits']==11*(2048-4*row['t_guard_1_over128'])
 rows.append({'test':row['test'],'direct_vs_matrixpower_max_difference':err,'tail_radii_exact_fraction_minimal':True})
assert json.load(open(p/'independent_schedule_replay.json'))==json.load(open(s/'parallel_schedule.json'))
for fn in ['circuit_h11_layers.npz']:
 A=np.load(s/fn);B=np.load(p/'replay'/fn);assert A.files==B.files and all(np.array_equal(A[k],B[k]) for k in A.files)
(p/'independent_policy_checks.json').write_text(json.dumps(rows,indent=2)+'\n')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
receipt={'status':'Accepted at scope stated in INDEPENDENT_REVIEW.md; hardware and rounded probability certification excluded','governing_directory':str(s),'reviewed_source_sha256':{f.name:sha(f) for f in s.iterdir() if f.is_file()},'own_evidence_sha256':{f.name:sha(f) for f in p.iterdir() if f.is_file() and f.name!='REVIEW_RECEIPT.json'},'independent_schedule_replay':'exact JSON and array equality','independent_compiler_replay':'exact JSON and all saved circuit array equality'}
(p/'REVIEW_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(rows,indent=2))
