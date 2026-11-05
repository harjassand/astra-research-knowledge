"""Rebuild deliberately omitted tables from included frozen graphs and source.
The mathematical certificate is necessary but not sufficient for exact replay:
also require equality with the separately preserved frozen-array digests.
"""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,sys,time
ROOT=Path(__file__).resolve().parent
def run(d,check_only=False):
 base=ROOT if d==21 else ROOT/'qec_design_direct_20261105'
 expected=json.loads((ROOT/'expected_frozen_parameters'/f'd{d}.json').read_text())
 graph=base/'canonical_qec_circuit_gate_20261105'/f'd{d}_r{d}_p1_1000_graph.json'
 assert hashlib.sha256(graph.read_bytes()).hexdigest()==expected['source_sha256']
 scripts=[base/'qec_overlap_gate_20261105/fault_tuple_screen.py',base/'qec_fault_tuple_20261105/build.py']
 assert all(p.exists() for p in scripts)
 if check_only:return {'distance':d,'frozen_graph_and_regenerator_present':True,'large_tables_intentionally_omitted':True}
 started=time.perf_counter();env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'}
 for args in [[str(scripts[0]),'--distance',str(d),'--cut-distance','64'],[str(scripts[1]),'--distance',str(d)]]:subprocess.run([sys.executable,*args],cwd=ROOT,env=env,check=True)
 folder=base/'qec_fault_tuple_20261105'/f'd{d}';actual=json.loads((folder/'parameters.json').read_text())
 assert actual['certificate']['integer_certificate_pass']
 assert actual['Z_exact']==expected['Z_exact'] and actual['conversion_TV_upper_exact']==expected['conversion_TV_upper_exact']
 for name,h in expected['sha256'].items():assert hashlib.sha256((folder/name).read_bytes()).hexdigest()==h,(d,name,'regenerated table differs; do not call this a fixed-seed replay')
 return {'distance':d,'all_frozen_array_digests_matched':True,'exact_normalizer_and_TV_matched':True,'wall_seconds':time.perf_counter()-started}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--distances',default='19,21,23');p.add_argument('--check-only',action='store_true');a=p.parse_args()
 r=[run(int(d),a.check_only) for d in a.distances.split(',')];print(json.dumps(r,indent=2));(ROOT/'regeneration_receipt.json').write_text(json.dumps(r,indent=2)+'\n')
