"""Independent endpoint audit: no author implementation imported; no originals changed."""
from pathlib import Path
import json,hashlib,itertools
import numpy as np
H=Path(__file__).resolve().parents[1];Q=H.parent
P=np.array([np.eye(2),[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex)
def ptm(ks):return np.array([[sum(np.trace(a@k@b@k.conj().T).real/2 for k in ks) for b in P] for a in P])
def unit(t):
 t=np.array(t);return ((1-t@t)*P[0]-2j*np.einsum('i,ijk->jk',t,P[1:]))/(1+t@t)
axes=[(1/3,1/5,0),(-1/4,2/7,1/6),(1/5,-1/3,2/9),(2/5,0,-1/4),(1/7,3/8,-2/9)]
frames=[(2/3,1/7,-1/5),(1/4,-2/5,1/3),(-2/7,3/5,1/6),(2/9,1/2,-2/3),(3/7,-1/5,2/5)]
raw=[]
for ax,fr,m in zip(axes,frames,[20,19,18,17,16]):
 A,V=unit(ax),unit(fr);t=1/m;c=(1-t*t)/(1+t*t);j=2*t/(1+t*t)
 raw.append(ptm([V@A@k@A.conj().T for k in [np.diag([1,c]),np.array([[0,j],[0,0]])]]))
# Quaternion quadratic objective provides an independent oracle computation,
# not the author's SVD. Each q denotes U=q0 I-i q.sigma.
def qoracle(M):
 basis=[P[0],-1j*P[1],-1j*P[2],-1j*P[3]]
 def score(q):
  U=sum(x*b for x,b in zip(q,basis));return np.trace(ptm([U])[1:,1:]@M[1:,1:])/4
 K=np.zeros((4,4));E=np.eye(4)
 for i in range(4):K[i,i]=score(E[i])
 for i in range(4):
  for j in range(i):K[i,j]=K[j,i]=(score(E[i]+E[j])-K[i,i]-K[j,j])/2
 return .25+np.linalg.eigvalsh(K)[-1]
def near(a,b):
 e=float(np.max(np.abs(np.array(a)-np.array(b))));errors.append(e);assert e<2e-11,e
errors=[];count_total=0;settings=list(itertools.product(range(3),[-1,1],range(3)))
def checkfit(M,counts,row,v2):
 global count_total
 n=int(counts.sum());alloc=np.full(18,n//18);alloc[:n%18]+=1;assert np.array_equal(counts.sum(1),alloc)
 prob=np.array([(1+M[k+1,0]+sg*M[k+1,j+1])/2 for j,sg,k in settings]);assert np.min(prob)>-1e-12 and np.max(prob)<1+1e-12
 plus=np.random.default_rng(row['seed']).binomial(alloc,np.clip(prob,0,1));assert np.array_equal(counts[:,1],plus)
 means=(counts[:,1]-counts[:,0])/alloc;A=np.zeros((3,3))
 for j,sg,k in settings:A[k,j]+=sg*means[settings.index((j,sg,k))]/2
 R=np.array(row['fitted_terminal_recovery_PTM' if v2 else 'fitted_recovery_PTM']);near(R[1:,1:]@R[1:,1:].T,np.eye(3));near(np.linalg.det(R[1:,1:]),1)
 near(A,row['fitted_Bloch_matrix' if v2 else 'fitted_endpoint_Bloch_estimate'])
 Mhat=np.eye(4);Mhat[1:,1:]=A;near((1+np.trace(R[1:,1:]@A))/4,qoracle(Mhat))
 score=(1+np.trace((R@M)[1:,1:]))/4;opt=qoracle(M)
 near(1-score,row['scorer_true_entanglement_infidelity' if v2 else 'scorer_true_infidelity_of_sampled_fit']);near(1-opt,row['source_informed_full_CPTP_oracle_infidelity' if v2 else 'source_informed_oracle_infidelity']);assert score<=opt+1e-12
 count_total+=n
v2=json.loads((H/'direct_endpoint_no_per_round_inverse_v2.json').read_text());cnt=np.load(H/'direct_endpoint_counts_v2.npz');end={}
for ss in v2['oracle_rows']:
 strength={'zero_clock_v1':0,'rate_0.01_v1':.01,'rate_0.1_v1':.1}[ss['scenario']]
 for site in ss['sites']:
  for rr in site['results']:
   M=np.linalg.matrix_power(np.diag([1,np.exp(-strength),np.exp(-strength),1])@raw[site['site']],rr['T']);end[ss['scenario'],site['site'],rr['T']]=M;near(M,rr['raw_endpoint_PTM']);near(1-qoracle(M),rr['full_CPTP_final_oracle_infidelity'])
for r in v2['runs']:
 N=r['budget_total_native_uses']//(5*r['T']);assert N==r['endpoint_shots_per_site'];assert r['actual_native_uses']==5*N*r['T'];assert r['native_uses_for_prior_inverse_training']==0
 clock=json.loads((Q/'clocked_flagged_storage_20261028'/f"{r['scenario']}.json").read_text());duration=clock['timing']['total_EC_time']+2;assert duration==203
 assert r['aggregate_channel_elapsed_time_reference_units']==5*N*r['T']*duration;assert r['ideal_five_site_parallel_channel_time_reference_units']==N*r['T']*duration
 assert [s['site'] for s in r['sites']]==list(range(5))
 for s in r['sites']:assert cnt[s['counts_key']].sum()==N;checkfit(end[r['scenario'],s['site'],r['T']],cnt[s['counts_key']],s,True)
v2shots=count_total
v1=json.loads((H/'oracle_and_endpoint_fit_v1.json').read_text());cnt=np.load(H/'endpoint_sampled_counts_v1.npz');ends={}
for source in v1['oracle_rows']:
 p=Q/source['source_file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==source['source_sha256'];j=json.loads(p.read_text());bs=j.get('same_elapsed_unencoded',j.get('matched_unencoded'))
 for site,original in zip(source['sites'],bs):
  assert site['site']==original['site']
  for r,rr in zip(site['results'],original['results']):
   assert r['T']==rr['T'];M=np.array(rr['logical_PTM']);near(M,r['endpoint_PTM']);near(1-qoracle(M),r['full_CPTP_endpoint_oracle_infidelity']);ends[source['source_label'],site['site'],r['T']]=M
for r in v1['endpoint_fit_pilots']:
 assert r['actual_total_native_exposures']==5*r['T']*r['endpoint_shots_per_site']<=r['total_native_exposure_budget']
 for s in r['sites']:checkfit(ends[r['source_label'],s['site'],r['T']],cnt[s['raw_key']],s,False)
manifest=json.loads((H/'AUTHOR_MANIFEST_v1.json').read_text())
for p,sha in manifest['files'].items():assert hashlib.sha256((H/p).read_bytes()).hexdigest()==sha
out={'status':'PASS_SCOPED_INDEPENDENT_RECONSTRUCTION','maximum_numeric_discrepancy':max(errors),'numeric_comparisons':len(errors),'v2_sampled_binary_trials':v2shots,'v1_sampled_binary_trials':count_total-v2shots,'source_model':'independent NumPy Kraus reconstruction from declared rational constants','oracle':'independent quaternion quadratic-form eigenvalue; analytical CPTP reduction audited separately','sample_provenance':'exact seeded binomial replay of all saved per-setting counts; not laboratory observations','external_dependencies':{str(p.relative_to(Q)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Q/'five_qubit_acquired_frame_pilot_20261028/code_and_channels.py']+[Q/r['source_file'] for r in v1['oracle_rows']]}}
(H/'independent_audit/results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
