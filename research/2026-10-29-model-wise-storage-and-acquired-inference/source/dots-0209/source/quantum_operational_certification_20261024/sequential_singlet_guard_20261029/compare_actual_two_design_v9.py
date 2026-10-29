"""Equal-candidate/equal-initial-bath good-source baseline, actual TEST CP maps."""
import numpy as np,json,importlib.util,contextlib,io,math
from pathlib import Path
p=Path(__file__).with_name('complete_noreset_learn_and_guard_v8.py');sp=importlib.util.spec_from_file_location('fixture',p);f=importlib.util.module_from_spec(sp)
with contextlib.redirect_stdout(io.StringIO()):sp.loader.exec_module(f)
original=json.load(open(Path(__file__).with_name('complete_noreset_learn_and_guard_v8.json')))
states=[]
for Q in f.P[1:]:
 _,V=np.linalg.eigh(Q);states.extend([V[:,0],V[:,1]])
checks=[]
for variant,U in enumerate([f.Ugood,f.Uburst]):
 maps=[]
 for fail in [False,True]:
  Bs=[]
  for psi in states:
   # Deterministic orthogonal qubit vector; only measurement projector matters.
   other=np.array([-psi[1].conjugate(),psi[0].conjugate()]);outket=other if fail else psi
   Sin=np.kron((f.E@psi).reshape(f.D,1),np.eye(2));sourceout=U@Sin
   for D in f.Ds:
    B=np.kron(outket.conj().reshape(1,2),np.eye(2))@np.kron(D,np.eye(2))@sourceout/np.sqrt(6);Bs.append(B)
  maps.append(f.superof(lambda sig,Bs=Bs:sum(B@sig@B.conj().T for B in Bs)))
 F=f.effect(maps[1]);W=f.effect(f.mp[variant]['bad']);res=np.linalg.norm(F-2*W/3);assert res<1e-12
 f.mp[variant]['testpass']=maps[0];f.mp[variant]['testfail']=maps[1];checks.append({'variant':variant,'full_memory_effect_identity_F_equals_2W_over3_residual':float(res)})
f.s=.4;f.a=.6;f.cap=500;f.Cdeclared=1.5;f.rng=np.random.default_rng(2026102915)
ex=f.exact(False);mc,ledger,accepted=f.trajectories(False);decoded=0
for i in np.flatnonzero(accepted&(np.count_nonzero(ledger,axis=1)>0))[:50]:
 good,flag=f.decode_ledger(ledger[i]);assert good and flag;decoded+=1
n=4;eps=1/128;g0=.35;delta=.05;eta=g0*np.sqrt(eps/(24*np.pi**2*n))/12;mformal=math.ceil(220/eta**2*math.log(288*(n-1)/delta))
print(json.dumps({'seed':2026102915,'same_post_training_frame_and_bath':True,'source':'same fixed collective U0 good continuation; no unequal-time burst comparison','prior_learning_calls':1000000,'weighted_reference':original['executions'][0],'two_design_actual_test':{'C':1.5,'s':.4,'R':1.,'cap':500,'t':6,'required_services':155,'payload_qubits':35,'accepted_sound_halfdiamond_bound':1/128,'effect_checks':checks,'exact_compressed_DP':ex,'sampled_trajectories':mc,'nonzero_accepted_ledgers_actually_decoded':decoded},'conservative_parameter_certification_comparison':{'n':n,'hypothetically_supplied_g0':g0,'learning_failure_delta':delta,'target_uniform_twirled_error':eps,'eta':eta,'declared_scalar_union_bound_calls':mformal,'scope':'Different guarantee: parameter-confidence route additionally assumes common joint algebra and aims uniform-horizon passive service, whereas guard gives finite accepted operation with possible abort. This is NOT a like-for-like superiority theorem.'},'control_cost_scope':'Two-design trials execute actual full inner encoder and decoder plus logical six-state controls; weighted trials use signed matching/constant-seed preparation and pair readout. No calibrated gate-duration/noisy-control total-cost winner claimed.'},indent=2))
