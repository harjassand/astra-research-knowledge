#!/usr/bin/env python3
"""Independent all-bank replay, actual circuit/SDP conventions and rounding audit."""
from pathlib import Path
import importlib.util,json,hashlib,itertools,time
import numpy as np
pdir=Path(__file__).parent
sp=importlib.util.spec_from_file_location('pilot',pdir/'run_pilot.py');p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
old=json.loads((pdir/'results.json').read_text());cr=json.loads((pdir/'convex_rounding_results.json').read_text());stored=np.load(pdir/'ordinary_counts.npz');V,source,probs,Ctrue=p.generator_only_source()
assert old['source_sha256']==hashlib.sha256((pdir/'run_pilot_before_sdp_rounding.py').read_bytes()).hexdigest()
for f,h in cr['sha256'].items():assert hashlib.sha256((pdir/f).read_bytes()).hexdigest()==h
# Verify the channel independently on a joint Bell reference and physical output.
Jsrc=np.zeros((8,8),complex)
for a,b in itertools.product(range(2),repeat=2):
 e=np.zeros((2,2),complex);e[a,b]=1;Jsrc[4*a:4*a+4,4*b:4*b+4]=source(e)/2
assert np.linalg.eigvalsh(Jsrc).min()>-1e-12 and abs(np.trace(Jsrc)-1)<1e-12
assert np.linalg.norm(np.trace(Jsrc.reshape(2,4,2,4),axis1=1,axis2=3)-np.eye(2)/2)<1e-12
# Independently enumerate setting probability and shadow mean (not sampled data).
shadowmean=[np.zeros((4,4),complex) for _ in range(3)];bornmax=0.
for l,(j,s,a,b) in enumerate(p.SETTINGS):
 out=source((p.I+s*p.P[j])/2)
 for z,(x,y) in enumerate(p.OUTCOMES):
  E=np.kron((p.I+x*p.P[a])/2,(p.I+y*p.P[b])/2);pr=np.trace(E@out).real
  bornmax=max(bornmax,abs(pr-probs[l,z]));snapshot=np.kron(3*(p.I+x*p.P[a])/2-p.I,3*(p.I+y*p.P[b])/2-p.I)
  shadowmean[j]+=pr*3*s*snapshot/len(p.SETTINGS)
assert max(np.linalg.norm(a-b) for a,b in zip(shadowmean,Ctrue))<1e-12
replay=0;rows=[];audited_controls={};maxscores=0.;maxdual=0.;minchoi=1.;tpmax=0.;adjmax=0.;circuitmax=0.;maxround=0.;allgrad=[]
for row in old['runs']:
 N=row['N'];rep=row['replicate'];key=f'N{N}_rep{rep}';counts=stored[key];assert counts.dtype.kind in 'iu' and counts.min()>=0 and counts.sum()==N
 rng=np.random.default_rng(row['record_seed']);labels=rng.integers(54,size=N);uniform=rng.random(N);out=np.sum(uniform[:,None]>np.cumsum(probs[labels],axis=1),axis=1)
 reconstructed=np.zeros((54,4),np.int64);np.add.at(reconstructed,(labels,out),1);assert np.array_equal(reconstructed,counts);replay+=N
 C=p.learner_contrasts(counts);ind=[np.zeros((4,4),complex) for _ in range(3)]
 for l,(j,s,a,b) in enumerate(p.SETTINGS):
  for z,(x,y) in enumerate(p.OUTCOMES):ind[j]+=counts[l,z]*3*s*np.kron((p.I+3*x*p.P[a])/2,(p.I+3*y*p.P[b])/2)/N
 assert max(np.linalg.norm(a-b) for a,b in zip(C,ind))<1e-12
 _,A,runs=p.unitary_search(C,row['record_seed']+900000,starts=4)
 audited_controls[key+'_variational_axes']=np.array(A)
 ss=p.score_decoder(A,V,source)
 for k in ss:maxscores=max(maxscores,abs(ss[k]-row['variational'][k]))
 assert max(np.linalg.norm(a@a-np.eye(4)) for a in A)<1e-10
 allgrad.extend(r['gradient_tolerance_reached'] for r in runs)
 dec,meta,J=p.sdp_recovery(C,return_choi=True)
 # Independent normalized logical Bell fidelity from the true source and physical Choi.
 Qtrue=sum((np.kron(s,c.T)/4 for s,c in zip(p.P,Ctrue)),np.zeros((8,8),complex))
 fe=.25+np.trace(Qtrue@J).real;direct=p.bell_fidelity(lambda r:dec(source(r)));assert abs(fe-direct)<1e-12
 maxscores=max(maxscores,abs((1-fe)-row['full_CPTP_SDP']['native_Bell_loss']))
 maxdual=max(maxdual,meta['numerical_primal_dual_gap']);minchoi=min(minchoi,np.linalg.eigvalsh(J).min());tpmax=max(tpmax,np.linalg.norm(p.partialout(J)-np.eye(4)))
 # Independent Heisenberg adjoint using explicit Choi blocks.
 adj=[]
 for s in p.P:
  a=sum((s[b,a]*J[4*a:4*a+4,4*b:4*b+4].T for a,b in itertools.product(range(2),repeat=2)),np.zeros((4,4),complex));adj.append((a+a.conj().T)/2)
 for s,aa in zip(p.P,adj):
  for x,y in itertools.product(range(4),repeat=2):
   e=np.zeros((4,4),complex);e[x,y]=1;adjmax=max(adjmax,abs(np.trace(s@dec(e))-np.trace(aa@e)))
 X=p.sign(adj[0]);odd=(adj[2]-X@adj[2]@X)/2;Z=p.sign(odd);Y=1j*X@Z;rounded=[X,Y,Z]
 audited_controls[key+'_recovery_choi']=J
 audited_controls[key+'_rounded_axes']=np.array(rounded)
 rr=p.score_decoder(rounded,V,source);ref=next(r for r in cr['runs'] if r['bank']==key)
 assert not ref['rounding_abstained']
 for k in rr:maxround=max(maxround,abs(rr[k]-ref['rounded_receiver'][k]))
 circuitmax=max(circuitmax,rr['actual_three_reflection_unitarity_residual'])
 assert not row['variational']['passes_target_delta_0_1'] and not ref['target_delta_0_1_pass']
 rows.append({'bank':key,'native_variational_loss':ss['native_Bell_loss'],'native_full_CPTP_loss':1-fe,'native_rounded_loss':rr['native_Bell_loss'],'primal_success':meta['primal_success'],'dual_success':meta['dual_success'],'numerical_duality_gap':meta['numerical_primal_dual_gap']})
print('replay_diagnostics',replay,len(rows),maxscores,maxround,flush=True)
assert replay==344064 and len(rows)==12 and np.isfinite(maxscores) and np.isfinite(maxround)
np.savez_compressed(pdir/'independently_recomputed_controls.npz',**audited_controls)
out={'status':'PASS_INDEPENDENT_REPLAY_AND_NUMERICAL_INTERFACE_AUDIT','replayed_individually_drawn_blocks':replay,'independent_banks':len(rows),'additional_source_acquisition':0,'physical_readouts_in_original':2*replay,'one_fixed_hidden_source':True,'all_original_raw_counts_exactly_reproduced':True,'true_source_choi_min_eigenvalue':float(np.linalg.eigvalsh(Jsrc).min()),'Born_law_max_residual':bornmax,'max_score_replay_difference':maxscores,'max_rounding_score_replay_difference':maxround,'max_Heisenberg_adjoint_identity_residual':float(adjmax),'max_rounding_receiver_unitarity_residual':float(circuitmax),'minimum_numerically_repaired_Choi_eigenvalue':float(minchoi),'maximum_TP_residual':float(tpmax),'maximum_numerical_primal_dual_gap':float(maxdual),'variational_searches_reaching_gradient_tolerance':sum(allgrad),'variational_searches':len(allgrad),'formal_target_acceptances':0,'score_replay_is_bitwise_exact':False,'original_optimizer_controls_saved_by_author':False,'tight_1e_minus_11_score_replay_failed':bool(maxscores>=1e-11 or maxround>=1e-11),'runs':rows,'scope':'Exact seed/count replay and floating mechanism/solver audit, not a rigorous interval SDP or rational gate certificate, not hardware or sampled unknown payload. Replayed counts are not extra independent evidence/source calls.','sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in [Path(__file__),pdir/'run_pilot.py',pdir/'run_pilot_before_sdp_rounding.py',pdir/'results.json',pdir/'ordinary_counts.npz',pdir/'analyze_convex_rounding.py',pdir/'convex_rounding_results.json',pdir/'independently_recomputed_controls.npz']}}
(pdir/'independent_audit_check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
