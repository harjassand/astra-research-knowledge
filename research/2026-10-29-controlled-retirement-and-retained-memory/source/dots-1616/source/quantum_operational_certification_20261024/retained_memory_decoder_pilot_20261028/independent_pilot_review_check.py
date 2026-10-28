"""Read-only deterministic numerical audit; never imports or calls simulator.
Uses existing records only. No sample acquisition, no scoring-file rewrites.
"""
from pathlib import Path
import json,hashlib,os,sys,tempfile,shutil,subprocess
import numpy as np
from learner import Learner
from ordinary_comparator import OrdinaryComparator
ROOT=Path(__file__).resolve().parent
manifest_blob=(ROOT/'DELIVERY_MANIFEST.json').read_bytes()
assert hashlib.sha256(manifest_blob).hexdigest()=='bf2a83b5f287c48cbfbe7be30a553a0dd11fcf6c7952ed61ef37681641bfb940'
manifest=json.loads(manifest_blob)['files']
for name,entry in manifest.items():
 b=(ROOT/name).read_bytes();assert len(b)==entry['bytes'] and hashlib.sha256(b).hexdigest()==entry['sha256'],name
roots=sys.argv[1:] or ['runs']
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1.,-1.]).astype(complex)
P=[I,X,Y,Z];B=np.array([np.kron(a,b) for a in P[1:] for b in P]);C0=np.eye(4)/4
mat=lambda x:np.array(x['real'])+1j*np.array(x['imag'])
partial=lambda x:np.trace(x.reshape(2,2,2,2),axis1=0,axis2=2)
Ctheta=lambda x:C0+np.einsum('a,aij->ij',x,B)
def decoder_kraus(c):
 v,w=np.linalg.eigh(c)
 assert v.min()>-1e-12
 return [np.sqrt(2*max(a,0))*w[:,i].reshape(2,2) for i,a in enumerate(v)]
def bell_loss(c,masses,u):
 ks=decoder_kraus(c)
 return 1-sum(m*sum(abs(np.trace(k@u@p))**2 for k in ks)/4 for m,p in zip(masses,P))
res={};checkcounts={};mins={};bounds={};runrows=[];allpublic={};allaudits={};usedfiles={}
def track(key,val,count=1):
 val=float(abs(val));res[key]=max(res.get(key,0.),val);checkcounts[key]=checkcounts.get(key,0)+count
 assert val<1e-9,(key,val)
def low(key,val):mins[key]=min(mins.get(key,float('inf')),float(val))
def read(path):
 b=path.read_bytes();usedfiles[str(path.relative_to(ROOT))]=hashlib.sha256(b).hexdigest();return json.loads(b)
def lines(path):
 b=path.read_bytes();usedfiles[str(path.relative_to(ROOT))]=hashlib.sha256(b).hexdigest();return [json.loads(x) for x in b.decode().splitlines()]
for root in roots:
 for directory in sorted((ROOT/root).iterdir()):
  if not directory.is_dir():continue
  meta=read(directory/'metadata.json');pub=lines(directory/'public_records.jsonl');priv=lines(directory/'private_source_audit.jsonl');scores=lines(directory/'posthoc_scores.jsonl');summary=read(directory/'summary.json');fails=read(directory/'failures.json')
  assert len(pub)==len(priv)==len(scores)==meta['plant']['source_calls']==meta['requested_N'] and not fails and meta['failure_count']==0
  assert not meta['terminal_payload_executed'] and not meta['hardware_executed'] and not meta['exact_rational_certification_executed']
  assert meta['gamma']==1 and meta['epsilon']==.25
  u=mat(meta['plant']['unitary']);kx=mat(meta['plant']['KX']);kz=mat(meta['plant']['KZ']);h=mat(meta['plant']['H'])
  maps=[[kx,kz,h],[kx],[],[kz]]
  track('source_TP',np.linalg.norm(2*kx.conj().T@kx+2*kz.conj().T@kz+h.conj().T@h-I))
  track('source_U_unitarity',np.linalg.norm(u.conj().T@u-I))
  learner=Learner() if meta['algorithm']=='bandit' else OrdinaryComparator()
  private_rng=np.random.default_rng(meta['seed'])
  expected_source_uniforms=np.random.default_rng(meta['source_seed']).random(len(pub))
  oldpost=None;risks=[];oracles=[];identities=[];centerrisks=[];bits=0;maxmove=0.
  for t,(r,a,sc) in enumerate(zip(pub,priv,scores),1):
   assert t==r['t']==a['call']==sc['t']
   assert a['private_bernoulli_uniform']==expected_source_uniforms[t-1]
   if meta['algorithm']=='bandit':
    for value in r['i_rejection_draws']:assert int(private_rng.integers(0,16))==value
    assert 2*int(private_rng.integers(0,2))-1==r['z']
   for value in r['j_rejection_draws']:assert int(private_rng.integers(0,4))==value
   assert 2*int(private_rng.integers(0,2))-1==r['s']
   if meta['algorithm']=='ordinary':
    for value in r['m_rejection_draws']:assert int(private_rng.integers(0,4))==value
    assert r['m_rejection_draws'][-1]==r['m'] and all(x>=3 for x in r['m_rejection_draws'][:-1])
   assert r['j_rejection_draws'][-1]==r['j'] and all(x>=3 for x in r['j_rejection_draws'][:-1])
   sig=np.array(a['memory_prior_real'])+1j*np.array(a['memory_prior_imag'])
   stored=np.array(a['memory_post_real'])+1j*np.array(a['memory_post_imag'])
   if oldpost is not None:track('memory_chain_continuity',np.linalg.norm(sig-oldpost))
   oldpost=stored
   low('prior_memory_min_eigen',np.linalg.eigvalsh(sig).min());low('post_memory_min_eigen',np.linalg.eigvalsh(stored).min())
   track('memory_trace',abs(np.trace(sig)-1));track('stored_memory_trace',abs(np.trace(stored)-1))
   blocks=[sum((k@sig@k.conj().T for k in ks),np.zeros((2,2),complex)) for ks in maps]
   masses=np.array([np.trace(x).real for x in blocks]);track('branch_mass_reconstruction',np.linalg.norm(masses-a['branch_masses']))
   track('branch_mass_sum',abs(masses.sum()-1))
   assert masses[0]>=max(masses[1:])-1e-12
   j=r['j'];s=r['s'];rho=(I+s*P[j+1])/2
   if meta['algorithm']=='bandit':
    center=Ctheta(learner.theta);play,diag=learner.act(r['i'],r['z']);dec=decoder_kraus(play)
    obs=r['y'];effect=(I-s*P[j+1])/2
    low('played_Choi_min_eigen',np.linalg.eigvalsh(play).min());track('played_TP',np.linalg.norm(partial(play)-I/2))
    for label in ('whitening_eigen_min','whitening_eigen_max','center_eigen_min','played_eigen_min','played_tp_residual'):
     track('replayed_'+label,abs(diag[label]-r['diagnostics'][label]))
    # Independent direct Choi/Kraus action on a generic noncommuting test input.
    test=(I+.21*X-.17*Y+.39*Z)/2
    direct=2*np.einsum('aibj,ij->ab',play.reshape(2,2,2,2),test)
    track('played_Kraus_Choi_action',np.linalg.norm(direct-sum(k@test@k.conj().T for k in dec)))
    bits+=4*len(r['i_rejection_draws'])+2*len(r['j_rejection_draws'])+2
    assert r['i_rejection_draws'][-1]==r['i'] and all(x>=12 for x in r['i_rejection_draws'][:-1])
    assert r['j_rejection_draws'][-1]==j and all(x>=3 for x in r['j_rejection_draws'][:-1])
   else:
    center,diag=learner.decoder();play=center;dec=[I]
    track('ordinary_preupdate_SVD_singular_values',np.linalg.norm(np.array(diag['singular_values'])-r['diagnostics']['singular_values']))
    obs=(1-r['b'])//2;effect=(I-P[r['m']+1])/2
    bits+=2*(len(r['j_rejection_draws'])+len(r['m_rejection_draws']))+1
   # Independent FULL joint source + decoder + projector instrument, for every recorded call.
   joint=sum((np.kron(u@p,k)@np.kron(rho,sig)@np.kron(u@p,k).conj().T for p,ks in zip(P,maps) for k in ks),np.zeros((4,4),complex))
   decoded=sum(np.kron(k,I)@joint@np.kron(k,I).conj().T for k in dec)
   ef=np.kron(effect,I);post1=partial(ef@decoded@ef);prob=float(np.trace(post1).real)
   track('all_call_Born_probability',abs(prob-a['born_mismatch_probability']))
   assert obs==int(a['private_bernoulli_uniform']<a['born_mismatch_probability'])
   chosen=post1 if obs else partial(decoded)-post1
   chosen/=np.trace(chosen)
   track('all_call_full_joint_memory_poststate',np.linalg.norm(chosen-stored))
   track('nonselective_memory',np.linalg.norm(partial(decoded)-sum(blocks)))
   cp=bell_loss(play,masses,u);cc=bell_loss(center,masses,u);oracle=1-masses[0]
   identity=np.outer(I.reshape(-1),I.reshape(-1))/2
   idrisk=bell_loss(identity,masses,u)
   track('played_Bell_score_independent_Kraus',cp-sc['played_policy_bell_loss'])
   track('center_Bell_score_independent_Kraus',cc-sc['center_policy_bell_loss'])
   track('oracle_Bell_score',oracle-sc['known_U_oracle_bell_loss'])
   track('identity_Bell_score',idrisk-sc['identity_no_learning_bell_loss'])
   track('depolarizing_Bell_score',.75-sc['depolarizing_no_learning_bell_loss'])
   risks.append(cp);centerrisks.append(cc);oracles.append(oracle);identities.append(idrisk)
   if meta['algorithm']=='bandit':
    prior=learner.theta.copy();upd=learner.observe(r['y'])
    track('bit_only_theta_replay',np.linalg.norm(learner.theta-r['update']['theta_after']))
    for key in ('stationarity_residual','locality_squared','dual_norm_squared','variance_bound'):
     track('replayed_'+key,abs(upd[key]-r['update'][key]))
    assert upd['prox_success'] and upd['stationarity_residual']<=meta['delta'] and upd['locality_squared']<=.25
    maxmove=max(maxmove,float(np.linalg.norm(learner.theta-prior)))
   else:learner.observe(j,s,r['m'],r['b'])
  assert bits==meta['private_rng_bits_consumed']
  track('mean_policy_score',np.mean(risks)-summary['played_policy_mean_bell_loss'])
  final=Ctheta(learner.theta) if meta['algorithm']=='bandit' else learner.decoder()[0]
  retrospective=float(np.mean([bell_loss(final,a['branch_masses'],u) for a in priv]))
  track('retrospective_final_score',retrospective-summary['final_decoder_retrospective_past_occupation_loss'])
  row={'batch':root,'run':directory.name,'calls':len(pub),'mean_policy_loss':float(np.mean(risks)),'mean_center_loss':float(np.mean(centerrisks)),'own_occupation_oracle':float(np.mean(oracles)),'identity_on_same_occupation':float(np.mean(identities)),'retrospective_final_loss':retrospective,'source_seed':meta['source_seed'],'private_seed':meta['seed'],'private_bits':bits,'terminal_payload_calls':0,'max_theta_step_norm':maxmove}
  runrows.append(row);allpublic[(root,directory.name)]=pub;allaudits[(root,directory.name)]=priv
# Establish repeated-prefix and common-random-number facts directly from raw records.
prefix=[];coupling=[]
for root in roots:
 for alg in ('bandit','ordinary'):
  names=[name for rr,name in allpublic if rr==root and name.startswith(alg+'_N128_')]
  for name in names:
   longer=name.replace('_N128_','_N512_')
   if (root,longer) not in allpublic:continue
   a=allpublic[root,name];b=allpublic[root,longer]
   keys=['i','z','j','s','y'] if alg=='bandit' else ['j','s','m','b']
   same=all(all(x[k]==y[k] for k in keys) for x,y in zip(a,b))
   memsame=all(x==y for x,y in zip(allaudits[root,name],allaudits[root,longer]))
   assert same and memsame
   prefix.append({'short':root+'/'+name,'long':root+'/'+longer,'identical_integer_records_and_private_memory_prefix':True})
 for n in (128,512):
  for seed in (17,31,47,73):
   a=(root,f'bandit_N{n}_seed{seed}');b=(root,f'ordinary_N{n}_seed{seed}')
   if a in allaudits and b in allaudits:
    identical=all(x['private_bernoulli_uniform']==y['private_bernoulli_uniform'] for x,y in zip(allaudits[a],allaudits[b]))
    assert identical;coupling.append({'N':n,'seed':seed,'identical_source_uniform_stream':True})
# Public-only execution in a directory with NO simulator, source audit or metadata file.
with tempfile.TemporaryDirectory(prefix='source_disabled_independent_') as tmp:
 base=Path(tmp)
 for f in ('learner.py','ordinary_comparator.py','quantum_math.py','replay.py'):shutil.copy2(ROOT/f,base/f)
 dst=base/'public_runs';dst.mkdir()
 for root in roots:
  for path in sorted((ROOT/root).iterdir()):
   if path.is_dir():
    out=dst/path.name;out.mkdir();shutil.copy2(path/'public_records.jsonl',out/'public_records.jsonl')
 env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
 proc=subprocess.run([sys.executable,str(base/'replay.py'),str(dst)],cwd=base,env=env,text=True,capture_output=True,check=True)
 isolated=json.loads(proc.stdout)
 assert all(x['max_theta_replay_error']==0 for x in isolated if x['run'].startswith('bandit'))
 assert all(x['max_theta_replay_error'] is None and x['max_singular_values_replay_error']==0 and x['theta_comparison_status']=='not_applicable' for x in isolated if x['run'].startswith('ordinary'))
 assert not (base/'simulator.py').exists()
summary=[]
for root in roots:
 for alg in ('bandit','ordinary'):
  for n in (128,512):
   rr=[r for r in runrows if r['batch']==root and r['run'].startswith(f'{alg}_N{n}_')]
   if rr:summary.append({'batch':root,'algorithm':alg,'N':n,'seeds':len(rr),'mean_policy_loss':float(np.mean([r['mean_policy_loss'] for r in rr])),'mean_own_occupation_oracle':float(np.mean([r['own_occupation_oracle'] for r in rr])),'mean_identity_same_occupation':float(np.mean([r['identity_on_same_occupation'] for r in rr])),'mean_center_loss':float(np.mean([r['mean_center_loss'] for r in rr]))})
analysis=read(ROOT/'ANALYSIS.json')
for agg in analysis['primary_aggregate']:
 sourcebatch='runs' if agg['algorithm']=='bandit' else 'runs_independent_comparator'
 ours=next(x for x in summary if x['batch']==sourcebatch and x['algorithm']==agg['algorithm'] and x['N']==agg['N'])
 track('primary_aggregate_policy',ours['mean_policy_loss']-agg['prequential_decoder_conditional_bell_loss']['mean'])
 track('primary_aggregate_oracle',ours['mean_own_occupation_oracle']-agg['known_U_oracle_mean_bell_loss']['mean'])
for pr in analysis['theorem_worst_case_precision']:
 n=pr['N'];assert pr['mu_power_of_two_exponent']==-(n+4) and pr['fixed_coordinate_grid_min_binary_fraction_bits']==2*n+42 and pr['weak_solve_objective_tolerance_min_binary_fraction_bits']==4*n+73
assert analysis['source_call_ledger']['total_actual_simulated_source_calls']==sum(x['calls'] for x in runrows)==7680
out={'delivery_manifest_sha256':hashlib.sha256(manifest_blob).hexdigest(),'status':'PASS_WITH_EXPLICIT_DIAGNOSTIC_LIMITATIONS','frozen_manifest_entries_verified':len(manifest),'total_existing_simulated_calls_checked':sum(x['calls'] for x in runrows),'new_source_calls':0,'source_simulator_imported':False,'existing_source_uniform_streams_replayed_from_seeds':True,'existing_private_sampler_draws_replayed_from_seeds':True,'max_residuals':res,'check_counts':checkcounts,'minimum_eigenvalues':mins,'run_results':runrows,'aggregate_results':summary,'identical_horizon_prefixes':prefix,'original_common_random_number_coupling':coupling,'isolated_public_only_replay':{'runs':len(isolated),'records':sum(x['records_replayed'] for x in isolated),'bandit_max_theta_error':max(x['max_theta_replay_error'] for x in isolated if x['run'].startswith('bandit')),'simulator_and_private_files_absent':True,'ordinary_saved_theta_error_field_correctly_null':True,'ordinary_SVD_replay_error':max(x['max_singular_values_replay_error'] for x in isolated if x['run'].startswith('ordinary')),'ordinary_singular_values_independently_checked':True},'data_sha256':usedfiles,'limitations':['Floating certificates only; no exact rational/gate synthesis execution','All-probe trajectories only; no terminal payload executed','Retrospective final scores are not future scores','Different algorithms have different actual occupations','Original equal seeds couple source uniforms; N128 reruns N512 prefixes','Historical ordinary theta-error zero was vacuous; corrected replay uses null and verifies saved SVD singular values']}
print(json.dumps(out,indent=2,sort_keys=True))
