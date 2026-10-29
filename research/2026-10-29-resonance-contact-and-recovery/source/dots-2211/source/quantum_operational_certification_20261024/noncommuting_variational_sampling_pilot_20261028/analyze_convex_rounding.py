#!/usr/bin/env python3
"""Reuse the already sampled banks; no new outcomes or source calls."""
from pathlib import Path
import importlib.util,json,hashlib
import numpy as np
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('pilot',HERE/'run_pilot.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
V,source,probs,Ctrue=p.generator_only_source();Btrue=[V@b@V.conj().T for b in p.B0]
counts=np.load(HERE/'ordinary_counts.npz');rows=[]
def analyze(C):
 dec,meta,J=p.sdp_recovery(C,return_choi=True)
 images=[np.einsum('ba,axby->xy',s,J.reshape(2,4,2,4)).T for s in p.P]
 images=[(a+a.conj().T)/2 for a in images]
 X=p.sign(images[0]);odd=(images[2]-X@images[2]@X)/2;gap=float(np.min(abs(np.linalg.eigvalsh(odd))))
 if gap<1e-8:return {'SDP':meta,'rounding_abstained':True,'odd_gap':gap}
 Z=p.sign(odd);Y=1j*X@Z;A=[X,Y,Z]
 alg=max(np.linalg.norm(a@a-np.eye(4),2) for a in A)
 anti=max(np.linalg.norm(a@b+b@a,2) for i,a in enumerate(A) for b in A[i+1:])
 cgap,res,S=p.fit_block(A,C)
 return {'SDP':meta,'rounding_abstained':False,'odd_gap':gap,'X_gap':float(np.min(abs(np.linalg.eigvalsh(images[0])))),'rounded_algebra_square_error':float(alg),'rounded_anticommutator_error':float(anti),'rounded_Y_Hermiticity_error':float(np.linalg.norm(Y-Y.conj().T,2)), 'rounded_candidate_gap':cgap,'rounded_candidate_residual':res,'rounded_generator_Frobenius_error':float(np.sqrt(sum(np.linalg.norm(a-b,'fro')**2 for a,b in zip(A,Btrue)))),'rounded_receiver':p.score_decoder(A,V,source)}
noiseless=analyze(Ctrue)
for name in counts.files:
 N=int(counts[name].sum());C=p.learner_contrasts(counts[name]);r=analyze(C);r['bank']=name;r['N']=N
 a=float(np.sqrt(16*9*16/N));kap=max(0.,r.get('rounded_candidate_gap',0)/2)
 cert=None if kap==0 else 2*(r['rounded_candidate_residual']+np.sqrt(12)*a)/kap
 r['declared_confidence_radius']=a;r['provisional_float_kappa']=kap;r['theorem_error_bound_float']=cert;r['target_delta_0_1_pass']=bool(cert is not None and cert<=.1)
 rows.append(r)
out={'status':'PASS_NUMERICAL_CONVEX_ROUNDING_ON_REUSED_BANKS','new_source_calls':0,'reused_individually_sampled_blocks':sum(int(counts[k].sum()) for k in counts.files),'noiseless':noiseless,'runs':rows,'scope':'Numerical primal/dual SDP and numerical Pauli rounding, not exact rational certified controls. No extra acquisition and no statistical target acceptance. Same original saved raw banks.','sha256':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in [Path(__file__),HERE/'run_pilot.py',HERE/'ordinary_counts.npz']}}
(HERE/'convex_rounding_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
