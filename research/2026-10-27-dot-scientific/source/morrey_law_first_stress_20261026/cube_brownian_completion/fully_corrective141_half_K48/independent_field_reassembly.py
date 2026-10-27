import sys
sys.set_int_max_str_digits(0)
from pathlib import Path
from fractions import Fraction as Q
import numpy as np,json,hashlib,ast,sys
P=Path('morrey_law_first_stress_20261026/cube_brownian_completion').resolve();O=P/'fully_corrective141_half_K48';sys.path.insert(0,str(P));from damped_arithmetic_primitives import I,mid_guard
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r=read(O/'full_field_receipt.json');plan=read(O/'arithmetic_plan_receipt.json');mr=read(P/'received_damped_moments_receipt.json')

for path,h in r['input_proxy_hashes'].items():assert sha(Path(path))==h
for f,h in r['output_hashes'].items():assert sha(O/f)==h
assert r['script_sha256']==sha(P/'receive_corrective141_half_full_field.py');assert r['full_field_functions_sha256']==sha(P/'acquire_two_new_h41_pair_compact_full_direction.py');assert r['blocks']==986 and Q(r['floating_weight_L1_error'])<=Q(plan['signed_weight_L1_error_max']);assert Q(r['max_basis_radius'])<Q(plan['basis_radius']);assert Q(r['b_radius'])<Q(1,2**40)
M=np.load(O/'received_signed_moments.npy');assert M.shape==(98,98,98)and np.all(np.isfinite(M));err=Q(plan['declared_moment_guard']);ep=read(O/'actual_primal_endpoint_proxy_receipt.json');line=read(O/'received_full_Gram_candidate.json');cl,ch=map(Q,line['actual_cubic_interval']);assert abs(Q(float(M[0,0,0])))<err
assert cl-Q(1,4)-err-3*Q(ep['actual_to_exact_proxy_W1_upper'])<=Q(float(M[1,1,1]))<=ch-Q(1,4)+err+3*Q(ep['actual_to_exact_proxy_W1_upper'])
K=96;k=np.arange(1,97);r=2**-37;ht=np.load(P/'epsilon_half_discriminator/half_H_table.npy');k2=k*k;H1=ht[k2];H2=ht[k2[:,None]+k2[None,:]];H3=ht[k2[:,None,None]+k2[None,:,None]+k2[None,None,:]];b0,_=mid_guard(I.div(I.rat(2),I.mul(I.PI,I.exact(k))),relative=2**-40);bs={-1:b0,1:b0*(-1.)**(k+1)}
TN,_=mid_guard(I.sincos(I.mul(I.PI,I.exact(np.arange(257)[:,None]*k[None,:]/256)))[0],radius=r);TN[0]=TN[-1]=0;TC,_=mid_guard(I.mul(I.sincos(I.mul(I.PI,I.exact((2*np.arange(512)[:,None]+1)*k[None,:]/1024)))[0],I.sinc_small(I.mul(I.PI,I.exact(k[None,:]/1024)))),radius=r);TE=TN
src=ast.parse((P/'acquire_two_new_h41_pair_compact_full_direction.py').read_text());exec(compile(ast.Module(body=[n for n in src.body if isinstance(n,ast.FunctionDef)and n.name in ['coeff','field']],type_ignores=[]),'<received_field_only>','exec'))
for name,arr in zip(['candidate_volume_nodes.npy','candidate_face_means.npy','candidate_edge_nodes.npy'],field(M)):
 saved=np.load(O/name);diff=float(np.max(abs(saved-arr)));assert diff<=2**-58,name;assert np.all(np.isfinite(saved));print(name,'GUARDED ARRAY REASSEMBLY',saved.shape,'max_difference',diff,'declared_guard',plan['effective_field_guard'])
print('INDEPENDENT STORED FIELD ASSEMBLY AND CUBIC/SOURCE SIGN PASS')
