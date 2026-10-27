#!/usr/bin/env python3
"""Reconstruct the adopted-141 stored fields from bundled frozen moments.
Run from a materialized research root. Writes to a NEW output directory, never
mutates the scientific source tree. This is replay, not fresh moment acquisition.
"""
import argparse,ast,hashlib,json,sys
from pathlib import Path
from fractions import Fraction as Q
import numpy as np
ap=argparse.ArgumentParser();ap.add_argument('--research-root',type=Path,default=Path('.'));ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
P=(a.research_root/'morrey_law_first_stress_20261026/cube_brownian_completion').resolve();O=P/'fully_corrective141_half_K48'
a.output.mkdir(parents=True,exist_ok=False);sys.path.insert(0,str(P))
from damped_arithmetic_primitives import I,mid_guard
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
receipt=json.loads((O/'full_field_receipt.json').read_text());M=np.load(O/'received_signed_moments.npy')
assert sha(O/'received_signed_moments.npy')==receipt['output_hashes']['received_signed_moments.npy']
assert sha(P/'epsilon_half_discriminator/half_H_table.npy')==receipt['actual_H_table_sha256']
assert sha(P/'acquire_two_new_h41_pair_compact_full_direction.py')==receipt['full_field_functions_sha256']
K=96;k=np.arange(1,97);r=2**-37;ht=np.load(P/'epsilon_half_discriminator/half_H_table.npy');k2=k*k
H1=ht[k2];H2=ht[k2[:,None]+k2[None,:]];H3=ht[k2[:,None,None]+k2[None,:,None]+k2[None,None,:]]
b0,_=mid_guard(I.div(I.rat(2),I.mul(I.PI,I.exact(k))),relative=2**-40);bs={-1:b0,1:b0*(-1.)**(k+1)}
TN,_=mid_guard(I.sincos(I.mul(I.PI,I.exact(np.arange(257)[:,None]*k[None,:]/256)))[0],radius=r);TN[0]=TN[-1]=0
TC,_=mid_guard(I.mul(I.sincos(I.mul(I.PI,I.exact((2*np.arange(512)[:,None]+1)*k[None,:]/1024)))[0],I.sinc_small(I.mul(I.PI,I.exact(k[None,:]/1024)))),radius=r);TE=TN
src=ast.parse((P/'acquire_two_new_h41_pair_compact_full_direction.py').read_text())
exec(compile(ast.Module(body=[n for n in src.body if isinstance(n,ast.FunctionDef)and n.name in ['coeff','field']],type_ignores=[]),'<frozen_received_field_functions>','exec'))
report={'scope':'Stored-moment field reconstruction only; no fresh moment acquisition or new theorem.','numpy':np.__version__,'outputs':[]}
for name,arr in zip(['candidate_volume_nodes.npy','candidate_face_means.npy','candidate_edge_nodes.npy'],field(M)):
 out=a.output/name;np.save(out,arr);got=sha(out);row={'name':name,'sha256':got,'expected_original_sha256':receipt['output_hashes'][name],'bitwise_original_match':got==receipt['output_hashes'][name]}
 original=O/name
 if original.exists():
  diff=float(np.max(abs(np.load(original,mmap_mode='r')-arr)));row['max_absolute_difference_from_original']=diff;row['within_independent_reassembly_guard_2^-58']=diff<=2**-58;assert diff<=2**-58
 report['outputs'].append(row)
(a.output/'reproduction_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
