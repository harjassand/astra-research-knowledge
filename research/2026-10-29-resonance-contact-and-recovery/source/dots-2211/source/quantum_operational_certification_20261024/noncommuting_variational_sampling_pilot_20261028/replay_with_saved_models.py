#!/usr/bin/env python3
"""Re-fit existing banks and preserve the actual numerical receivers; ZERO new source calls."""
from pathlib import Path
import importlib.util,json,hashlib
import numpy as np
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('pilot',HERE/'run_pilot.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
V,source,_,Ctrue=p.generator_only_source();Btrue=[V@b@V.conj().T for b in p.B0]
banks=np.load(HERE/'ordinary_counts.npz');models={};rows=[]
for name in banks.files:
 counts=banks[name];N=int(counts.sum());rep=int(name.split('rep')[-1]);seed=202610280000+N+rep
 C=p.learner_contrasts(counts);models[name+'_contrasts']=np.array(C)
 U,A,runs=p.unitary_search(C,seed+900000,starts=4)
 models[name+'_variational_U']=U;models[name+'_variational_A']=np.array(A)
 row={'bank':name,'N':N,'variational':{**p.score_decoder(A,V,source),'search':runs}}
 for method,AA in [('raw_sign',[p.sign(c) for c in C]),('scalar_whitening',p.scalar_whitening(C))]:
  if AA is None:row[method]={'abstained':True}
  else:models[name+'_'+method+'_A']=np.array(AA);row[method]={'abstained':False,**p.score_decoder(AA,V,source)}
 AA,gap=p.operator_whitening(C)
 if AA is None:row['operator_whitening']={'abstained':True,'block_gap':gap}
 else:models[name+'_operator_whitening_A']=np.array(AA);row['operator_whitening']={'abstained':False,'block_gap':gap,**p.score_decoder(AA,V,source)}
 dec,meta,J=p.sdp_recovery(C,return_choi=True);models[name+'_SDP_Choi']=J
 row['full_CPTP_SDP']={**meta,'native_Bell_loss':1-p.bell_fidelity(lambda rho:dec(source(rho)))}
 images=[np.einsum('ba,axby->xy',s,J.reshape(2,4,2,4)).T for s in p.P];images=[(a+a.conj().T)/2 for a in images]
 X=p.sign(images[0]);odd=(images[2]-X@images[2]@X)/2;gap=float(np.min(abs(np.linalg.eigvalsh(odd))))
 if gap<1e-8:row['SDP_rounded']={'abstained':True,'odd_gap':gap}
 else:
  Z=p.sign(odd);A=[X,1j*X@Z,Z];models[name+'_SDP_rounded_A']=np.array(A)
  cgap,res,_=p.fit_block(A,C);a=float(np.sqrt(16*9*16/N));kappa=max(0.,cgap/2);e=res+np.sqrt(12)*a
  row['SDP_rounded']={'abstained':False,'odd_gap':gap,**p.score_decoder(A,V,source),'candidate_gap_float':cgap,'candidate_residual_float':res,'confidence_radius':a,'provisional_kappa_float':kappa,'uniform_inverse_bound_float':None if kappa<=0 else 2*e/kappa,'native_oracle_regret_bound_float':None if kappa<=0 else e*e/(8*kappa)}
 rows.append(row)
np.savez_compressed(HERE/'replayed_models.npz',**models)
out={'status':'REFIT_SAME_BANKS_WITH_SAVED_NUMERICAL_MODELS','new_source_calls':0,'reused_source_blocks':sum(int(banks[k].sum()) for k in banks.files),'runs':rows,'scope':'New numerical optimizer rerun of the same banks, preserving original results. Models saved for direct independent rescoring; not exact rational controls, interval SDP certificates or new acquisition.','sha256':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in [Path(__file__),HERE/'run_pilot.py',HERE/'ordinary_counts.npz',HERE/'replayed_models.npz']}}
(HERE/'replayed_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
