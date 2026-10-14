#!/usr/bin/env python3
"""Exact retained-vector alpha check in the correct weighted generator geometry.

The inspected producer Compiler/from_transcript are reused explicitly. No source
NPZ or object array is loaded. No new floating solve proposes a local alpha vector.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,hashlib,json,platform,sys,time

def main(source,evidence,out):
 st=time.monotonic();sys.path.insert(0,str(source))
 from model import Compiler,discover_partition,from_transcript
 data=json.loads(evidence.read_text());rows=[]
 for case in data['tensor_replays']:
  name=case['name'];tr=json.loads((source/(name+'_transcript.json')).read_text());model=from_transcript(18,tr);groups,_=discover_partition(model);compiler=Compiler(model,groups)
  wit=case['exact_high_precision_alpha_recertification']['alpha_witness'];block=wit['target_block'];K=compiler.refraw[block];mass=list(map(F,compiler.mass[block]));n=len(K)
  assert n==wit['local_states'] and n==len(wit['u_numerators']) and all(x>0 for x in mass)
  nonsym=any(K[i,j]!=K[j,i] for i in range(n) for j in range(n));assert nonsym
  assert all(mass[i]*F(K[i,j])==mass[j]*F(K[j,i]) for i in range(n) for j in range(n))
  assert all(F(K[i,j])<=0 for i in range(n) for j in range(n) if i!=j)
  kills=[sum(F(K[i,j]) for j in range(n)) for i in range(n)];assert min(kills)>=0 and max(kills)>0
  seen={0};queue=[0]
  while queue:
   i=queue.pop()
   for j in range(n):
    if K[i,j]<0 and j not in seen:seen.add(j);queue.append(j)
  assert len(seen)==n
  den=int(wit['u_denominator']);u=[F(int(x),den) for x in wit['u_numerators']];assert min(u)>0
  delta=max(abs(sum(F(K[i,j])*u[j] for j in range(n))-1) for i in range(n));assert delta<1
  alpha=(1-delta)/max(u);assert alpha==F(wit['alpha_lower'])
  old=json.loads((source/(name+'.json')).read_text());assert F(old['alpha_lower'])<=alpha
  rows.append(dict(case=name,local_states=n,raw_Euclidean_symmetric=not nonsym,weighted_detailed_balance_exact=True,irreducible_Z_matrix_with_positive_killing=True,retained_u_positive=True,retained_u_residual_below_one=True,new_alpha_exact=str(alpha),old_alpha_exact=old['alpha_lower'],old_alpha_le_new_alpha=True,witness_source_sha256=hashlib.sha256(evidence.read_bytes()).hexdigest()))
 report=dict(status='PASS',python=platform.python_version(),seconds=time.monotonic()-st,cases=rows,scope='Exact retained112-bit local vectors validate old scalar alphas in weighted L2,with producer compiler reused explicitly. No new alpha solve,no claim to recover missing historical vector;source default endpoint-equality audit remains FAIL.')
 out.mkdir(parents=True,exist_ok=True);(out/'WEIGHTED_ALPHA_REPLAY.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status=report['status'],cases=len(rows),all_raw_matrices_nonsymmetric=True,seconds=report['seconds'])))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--source-dir',type=Path,required=True);ap.add_argument('--evidence',type=Path,required=True);ap.add_argument('--output-dir',type=Path,required=True);a=ap.parse_args();main(a.source_dir.resolve(),a.evidence.resolve(),a.output_dir.resolve())
