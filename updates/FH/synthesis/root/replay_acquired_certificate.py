"""Re-certify the retained source witness using the newly acquired cycle law.

Imports the inspected source certifier. This is a distinct query transcript
with the same retained witness,not an independent certifier or new optimization.
Independent full finite-operator checks are in the escape audit package.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,hashlib,importlib.util,json,platform,sys,time

def main(source,out):
 here=Path(__file__).resolve().parent;started=time.monotonic()
 law=json.loads((here/'ACQUIRED_CYCLE_TRANSCRIPT.json').read_text());original=json.loads((source/'acquired_n24_t1000.json').read_text())
 assert law['n']==24 and set(law['fields'])=={'1'} and set(law['couplings'].values())=={'1000'} and law['order'][0]==0
 spec=importlib.util.spec_from_file_location('fh_inspected_collective',source/'collective_sector.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 R=m.CollectiveRing(law['n'],F(next(iter(law['couplings'].values()))),F(original['nu']),F(original['kappa']))
 v={int(k):F(value) for k,value in original['witness'].items()};lo,hi,support=R.certificate(v)
 assert lo==F(original['lower_exact']) and hi==F(original['upper_exact']) and lo>0
 receipt=dict(status='PASS',python=platform.python_version(),unique_energy_queries=law['unique_weight_queries'],original_pairwise_queries=original['energy_queries'],
  trial_states=len(v),residual_support=support,lower_exact=str(lo),upper_exact=str(hi),lower=float(lo),upper=float(hi),ratio=float(hi/lo),
  source_code_sha256=hashlib.sha256((source/'collective_sector.py').read_bytes()).hexdigest(),
  witness_sha256=hashlib.sha256((source/'acquired_n24_t1000.json').read_bytes()).hexdigest(),seconds=time.monotonic()-started,
  scope='Conditional exact ring-law acquisition and same-witness recertification;source certifier reused explicitly. No new solve,independent certificate implementation,physical sensor or general hidden-gate closure.')
 out.mkdir(parents=True,exist_ok=True);(out/'ACQUIRED_RETAINED_WITNESS_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k not in ['lower_exact','upper_exact']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source-dir',required=True,type=Path);p.add_argument('--output-dir',required=True,type=Path);a=p.parse_args();main(a.source_dir.resolve(),a.output_dir.resolve())
