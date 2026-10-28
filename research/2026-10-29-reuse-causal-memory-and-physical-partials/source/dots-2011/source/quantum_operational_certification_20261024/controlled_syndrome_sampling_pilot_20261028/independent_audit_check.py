"""Independent full replay and physical rescoring of stored sampled banks.
Does not import/run author scripts or change their files. Replays declared seeds;
these are NOT new independent experimental banks, source acquisition or hardware.
"""
from pathlib import Path
import numpy as np,itertools,json,hashlib,math,time
ROOT=Path(__file__).resolve().parent
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex)
PA=[I,X,Y,Z]
def kron(*xs):
 out=np.ones((1,1),complex)
 for a in xs:out=np.kron(out,a)
 return out
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=['run_pilot.py','results.json','ordinary_counts.npz','run_large_budget.py','large_budget/results.json','large_budget/ordinary_counts.npz']
frozen={n:digest(ROOT/n) for n in files}
metas=[json.loads((ROOT/n).read_text()) for n in ['results.json','large_budget/results.json']]
V=np.array(metas[0]['source_V_real'])+1j*np.array(metas[0]['source_V_imag'])
assert np.array_equal(V,np.array(metas[1]['source_V_real'])+1j*np.array(metas[1]['source_V_imag']))
assert np.max(abs(V.conj().T@V-np.eye(8)))<2e-15
# Independently reconstruct the stated source QR seed; no learner access to this object.
rng=np.random.default_rng(metas[0]['source_seed']);gauss=rng.normal(size=(8,8))+1j*rng.normal(size=(8,8))
q,r=np.linalg.qr(gauss);vseed=q@np.diag((np.diag(r)/abs(np.diag(r))).conj())
assert np.array_equal(V,vseed)
code=np.zeros((8,2),complex);code[0,0]=code[7,1]=1
reps=[0,4,2,1]
flip=[np.eye(8)[np.arange(8)^f] for f in range(8)]
U=np.column_stack([V@flip[g]@code[:,l] for l in range(2) for g in reps])
# Measurement eigenvectors and all rank-one product projectors reconstructed independently.
eigen=[np.column_stack([np.array([1,sg],complex)/np.sqrt(2) for sg in (1,-1)]),
       np.column_stack([np.array([1,sg*1j],complex)/np.sqrt(2) for sg in (1,-1)]),I]
settings=list(itertools.product(range(3),repeat=3));vectors=np.empty((27,8,8),complex);shadows=np.empty((27,8,8,8),complex)
for k,axes in enumerate(settings):
 for outcome in range(8):
  bits=[(outcome>>(2-j))&1 for j in range(3)]
  vecs=[eigen[axes[j]][:,bits[j]] for j in range(3)]
  vectors[k,outcome]=kron(*[a[:,None] for a in vecs])[:,0]
  shadows[k,outcome]=kron(*[3*np.outer(a,a.conj())-I for a in vecs])
# General encode -> injection -> bit flips -> V -> Born law, without the author's index shortcut.
probs=np.empty((2,2,4,8,27,8));states=np.empty((2,2,4,8,8,8),complex)
for ax,sg,g,f in itertools.product(range(2),range(2),range(4),range(8)):
 sign=2*sg-1
 logical=np.array([1,sign],complex)/np.sqrt(2) if ax==0 else np.array([int(sign==1),int(sign==-1)],complex)
 psi=V@flip[f]@flip[reps[g]]@code@logical
 probs[ax,sg,g,f]=abs(np.einsum('koi,i->ko',vectors.conj(),psi))**2
 states[ax,sg,g,f]=np.outer(psi,psi.conj())
assert np.max(abs(probs.sum(-1)-1))<3e-14
shadow_rebuilt=np.einsum('asgfko,koij->asgfij',probs,shadows)/27
max_shadow_born=float(np.max(abs(shadow_rebuilt-states)));assert max_shadow_born<3e-14
# Actual population signed estimators, including all known injection weights.
injsigns=np.array([[1-2*((g>>(2-j))&1) for j in range(3)] for g in reps])
Zsites=[kron(*[Z if j==i else I for j in range(3)]) for i in range(3)]
Xall=kron(X,X,X);Zall=kron(Z,Z,Z);Zsum=sum(Zsites)
population_errors=[]
for p in (0.,.01,.1,.4):
 w=np.array([p**f.bit_count()*(1-p)**(3-f.bit_count()) for f in range(8)])
 gi=w[reps];gx=w[[7^g for g in reps]];c=1-2*p
 def pop(ax,weights,active):
  out=np.zeros((8,8),complex)
  for sg,g,f in itertools.product(range(2),range(4),range(8)):
   if not active and g!=0:continue
   out+=(2*sg-1)*w[f]*weights[g]*states[ax,sg,g,f]/(8 if active else 2)
  return out
 expected=[V@Xall@V.conj().T/8,
           V@(c*Zsum-c**3*Zall)@V.conj().T/16,
           V@(c*Zsum)@V.conj().T/8]
 actual=[pop(0,np.ones(4),True),pop(1,np.ones(4),True),pop(1,injsigns.sum(1),True)]
 errors=[np.max(abs(a-b)) for a,b in zip(actual,expected)]
 for i in range(3):errors.append(np.max(abs(pop(1,injsigns[:,i],True)-V@(c*Zsites[i])@V.conj().T/8)))
 errors.append(np.max(abs(pop(0,np.ones(4),False)-U@kron(X/2,np.diag(gi+gx))@U.conj().T)))
 errors.append(np.max(abs(pop(1,np.ones(4),False)-U@kron(Z/2,np.diag(gi-gx))@U.conj().T)))
 assert max(errors)<2e-14
 assert np.min(gi-gx)>-1e-15
 assert abs(gx.sum()-(3*p*p-2*p*p*p))<1e-15
 population_errors.append(float(max(errors)))
def reflection(H):
 e,v=np.linalg.eigh((H+H.conj().T)/2)
 return v@np.diag(np.where(e<0,-1.,1.))@v.conj().T

def decoded_effects(sx,sz):
 # Three controlled-reflection gates, ancilla starts maximally mixed, physical output is discarded.
 Cz=kron((np.eye(8)+sz)/2,I)+kron((np.eye(8)-sz)/2,X)
 Cx=kron(np.eye(8),np.diag([1,0]))+kron(sx,np.diag([0,1]))
 W=Cz@Cx@Cz
 T=[np.zeros((4,4),complex) for _ in range(4)]
 # Direct Bell-state projections of the full circuit; no decoder-Kraus Pauli-row helper imported.
 for ain in range(2):
  isom=W@kron(U,np.eye(2)[:,ain:ain+1])
  tensor=isom.reshape(8,2,2,4) # physical output, ancilla output, reference logical, gauge
  for alpha,P in enumerate(PA):
   amp=np.einsum('al,salg->sg',P.conj(),tensor)/2
   T[alpha]+=amp.conj().T@amp/2 # initial ancilla probability 1/2
 return T,W
trueX=U@kron(X,np.eye(4))@U.conj().T;trueZ=U@kron(Z,np.eye(4))@U.conj().T
Ttrue,_=decoded_effects(trueX,trueZ);assert np.max(abs(Ttrue[0]-np.eye(4)))<3e-13
all_rows=[];all_seeds=[];totals=[];max_score_error=0.;max_choi_normalization=0.;max_control_unitarity=0.;max_direct_native=0.;min_effect_eigen=1.;replayed=0
for dataset,(meta,relative) in enumerate(zip(metas,['ordinary_counts.npz','large_budget/ordinary_counts.npz'])):
 path=ROOT/relative;ctsall=np.load(path)['counts']
 assert digest(path)==meta['counts_sha256']
 assert len(ctsall)==meta['independent_calibration_banks']==len(meta['banks'])
 assert sum(b['N'] for b in meta['banks'])==meta['actual_individually_rng_simulated_calls']
 assert len(meta['results'])==meta['decoder_evaluations']
 bybank={b['bank_id']:[] for b in meta['banks']}
 for row in meta['results']:bybank[row['bank_id']].append(row)
 for bank,cts in zip(meta['banks'],ctsall):
  N=bank['N'];p=bank['p'];active=bank['active'];seed=bank['seed'];bid=bank['bank_id']
  assert cts.shape==(2,2,4,27,8) and np.issubdtype(cts.dtype,np.integer) and cts.sum()==N
  if not active:assert cts[:,:,1:].sum()==0
  assert len(bybank[bid])==(3 if active else 1)
  all_seeds.append(seed)
  # Exact seed replay uses independent Born tables, not the author's output probabilities.
  rr=np.random.default_rng(seed);axes=rr.integers(0,2,N);signs=rr.integers(0,2,N)
  gauges=rr.integers(0,4,N) if active else np.zeros(N,dtype=int)
  flipbits=rr.random((N,3))<p;faults=4*flipbits[:,0]+2*flipbits[:,1]+flipbits[:,2]
  settings_draw=rr.integers(0,27,N);coins=rr.random(N)
  dist=probs[axes,signs,gauges,faults,settings_draw]
  outcomes=(coins[:,None]>np.cumsum(dist,axis=1)).sum(axis=1)
  assert outcomes.max()<8
  replay=np.zeros_like(cts);np.add.at(replay,(axes,signs,gauges,settings_draw,outcomes),1)
  assert np.array_equal(replay,cts),(dataset,bid,'raw-count replay mismatch')
  replayed+=N
  # Refit from saved sufficient statistics only; p,V, faults never enter estimator functions.
  def estimate(axis,iw):
   signed=cts[axis,1].astype(np.float64)-cts[axis,0].astype(np.float64)
   aggregate=np.tensordot(iw,signed,axes=(0,0))
   return (2/N)*(aggregate.ravel()@shadows.reshape(216,64)).reshape(8,8)
  sx=reflection(estimate(0,np.ones(4)))
  szs={'active_unlabelled' if active else 'native_unlabelled':reflection(estimate(1,np.ones(4)))}
  if active:
   szs['active_label_sum']=reflection(estimate(1,injsigns.sum(1)))
   zi=[reflection(estimate(1,injsigns[:,i])) for i in range(3)]
   szs['active_label_triple']=reflection(sum(zi))
  w=np.array([p**f.bit_count()*(1-p)**(3-f.bit_count()) for f in range(8)])
  gi=w[reps];gx=w[[7^g for g in reps]];oracle=3*p*p-2*p*p*p
  for reported in bybank[bid]:
   sz=szs[reported['method']];T,W=decoded_effects(sx,sz)
   normerr=np.max(abs(sum(T)-np.eye(4)));uniterr=np.max(abs(W.conj().T@W-np.eye(16)))
   min_eig=min(np.linalg.eigvalsh(t).min() for t in T)
   b=1-np.linalg.eigvalsh(T[0]).min()
   F=float(np.dot(gi,np.diag(T[0]).real)+np.dot(gx,np.diag(T[1]).real))
   # Independently score the native noisy repetition channel before any syndrome decomposition.
   Fdirect=0.
   for f in range(8):
    Af=V@flip[f]@code
    for ain in range(2):
     evolution=(W@kron(Af,np.eye(2)[:,ain:ain+1])).reshape(8,2,2)
     bellamp=np.einsum('saa->s',evolution)/2
     Fdirect+=w[f]*float(np.vdot(bellamp,bellamp).real)/2
   max_direct_native=max(max_direct_native,abs(F-Fdirect))
   computed={'oracle_native_loss':oracle,'native_loss':1-F,'native_excess':1-F-oracle,'worst_gauge_virtual_loss':b}
   err=max(abs(computed[k]-reported[k]) for k in computed)
   max_score_error=max(max_score_error,err);max_choi_normalization=max(max_choi_normalization,float(normerr));max_control_unitarity=max(max_control_unitarity,float(uniterr));min_effect_eigen=min(min_effect_eigen,float(min_eig))
   assert err<2e-11,(dataset,bid,reported['method'],computed,reported)
   assert normerr<3e-12 and uniterr<3e-12 and min_eig>-3e-13 and 1-F-oracle>-3e-12
   all_rows.append(dict(reported,dataset=dataset,computed_native_loss=1-F,computed_worst_gauge=b))
  if (bid+1)%64==0:print('Replayed dataset',dataset,'banks',bid+1,'calls',replayed,flush=True)
 # Verify every stored summary from its individual rows, not rounded summary copies.
 for sm in meta['summary']:
  rr=[r for r in meta['results'] if all(r[k]==sm[k] for k in ['p','N','method'])]
  assert len(rr)==sm['runs']
  assert abs(np.mean([r['native_excess'] for r in rr])-sm['mean_native_excess'])<1e-15
  assert abs(np.mean([r['worst_gauge_virtual_loss'] for r in rr])-sm['mean_worst_gauge_loss'])<1e-15
 totals.append({'banks':len(meta['banks']),'simulated_calls_replayed':sum(b['N'] for b in meta['banks']),'decoder_evaluations':len(meta['results'])})
assert len(set(all_seeds))==len(all_seeds)==512
assert replayed==22347776
# Descriptive standard errors and correct pairing: active methods share a bank; native banks do not.
summary=[];paired=[];independent=[]
for meta in metas:
 for sm in meta['summary']:
  rr=[r for r in meta['results'] if all(r[k]==sm[k] for k in ['p','N','method'])]
  x=np.array([r['native_excess'] for r in rr]);y=np.array([r['worst_gauge_virtual_loss'] for r in rr])
  summary.append(dict(sm,se_native_excess=float(x.std(ddof=1)/np.sqrt(len(x))),se_worst_gauge=float(y.std(ddof=1)/np.sqrt(len(y)))))
 for p,N in sorted({(r['p'],r['N']) for r in meta['results']}):
  data={name:{r['rep']:r for r in meta['results'] if r['p']==p and r['N']==N and r['method']==name} for name in ['native_unlabelled','active_unlabelled','active_label_sum','active_label_triple']}
  for method in ['active_label_sum','active_label_triple']:
   row={'p':p,'N':N,'method_minus_active_unlabelled':method}
   for score in ['native_excess','worst_gauge_virtual_loss']:
    dif=np.array([data[method][rep][score]-data['active_unlabelled'][rep][score] for rep in data[method]])
    row['mean_'+score+'_difference']=float(dif.mean());row['paired_se_'+score]=float(dif.std(ddof=1)/np.sqrt(len(dif)))
   paired.append(row)
  for method in ['active_unlabelled','active_label_sum','active_label_triple']:
   row={'p':p,'N':N,'active_minus_native':method}
   for score in ['native_excess','worst_gauge_virtual_loss']:
    aa=np.array([r[score] for r in data[method].values()]);nn=np.array([r[score] for r in data['native_unlabelled'].values()])
    row['mean_'+score+'_difference']=float(aa.mean()-nn.mean());row['independent_se_'+score]=float(np.sqrt(aa.var(ddof=1)/len(aa)+nn.var(ddof=1)/len(nn)))
   independent.append(row)
for n,old in frozen.items():assert digest(ROOT/n)==old,(n,'author file changed during audit')
result={'status':'PASS_INDEPENDENT_FULL_SEED_REPLAY_BORN_LAW_PHYSICAL_RECEIVER_AND_SCORES','reviewer':'producer-workspace/review_repeated_service_factorization','input_sha256':frozen,'datasets':totals,'all_unique_bank_seeds':512,'simulated_call_records_replayed':replayed,'decoder_evaluations_recomputed':len(all_rows),'new_independent_simulation_banks':0,'hardware_source_calls':0,'author_scripts_imported_or_executed':False,'author_files_modified':False,'Born_shadow_max_residual':max_shadow_born,'population_signal_max_residual':max(population_errors),'reported_score_max_residual':max_score_error,'direct_native_fidelity_max_residual':max_direct_native,'effect_POVM_max_residual':max_choi_normalization,'control_unitarity_max_residual':max_control_unitarity,'minimum_effect_eigenvalue':min_effect_eigen,'summary_with_descriptive_standard_errors':summary,'paired_active_comparisons':paired,'independent_active_vs_native_comparisons':independent,'scope':['One fixed dense source V, four p values, finite budgets','Actual per-call sampling replay; raw errors not visible to learner','Active calibration uses an extra pre-noise syndrome-injection port','All active methods share each bank and reuse labels','All-gauge score is posthoc using true U, not a learner-certified acceptance event','Floating spectral signs and circuit algebra, not finite rational Jacobi/gate synthesis/hardware','No universal advantage or best-conventional-estimator claim']}
(ROOT/'independent_audit_check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['summary_with_descriptive_standard_errors','paired_active_comparisons','independent_active_vs_native_comparisons','input_sha256']},indent=2))
