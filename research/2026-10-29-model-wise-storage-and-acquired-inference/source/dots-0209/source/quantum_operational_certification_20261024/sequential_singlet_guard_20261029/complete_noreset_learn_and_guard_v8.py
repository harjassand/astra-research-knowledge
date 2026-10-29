"""Compressed exact source-memory/count execution plus actual sampled Pauli ledgers.
This simulator uses a known source generator to compute CP instruments. The physical
protocol has no Kraus-label or bath-state access. Full outer amplitudes are not simulated.
"""
import numpy as np,json,math,importlib.util,contextlib,io,hashlib
from pathlib import Path
from scipy.linalg import expm,null_space,eigh
root=Path(__file__).resolve().parent.parent
acq=root/'nonunital_collective_frame_acquisition_20261029'/'check_retained_memory_bank_v4.py'
spec=importlib.util.spec_from_file_location('prior_acquisition',acq);old=importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):spec.loader.exec_module(old)
rng=np.random.default_rng(2026102914)
D=16;K=2;Mdim=2;P=list(old.P)
Jlab=[sum(old.kron([P[a] if i==j else P[0] for i in range(4)]) for j in range(4))/2 for a in [1,2,3]]
vals,Z=eigh(sum(A@A for A in Jlab));Ebase=Z[:,vals<1e-8];frames=[np.eye(3)]
for i in range(3):
 _,_,vt=np.linalg.svd(old.sums[i]/1000000-old.Jembed);frames.append(old.rounding(vt[-1]))
Vhat=old.kron([old.su(R) for R in frames]);E=Vhat@Ebase;PH=E@E.conj().T
Ds=[E.conj().T]+[np.outer(np.array([1,0]),q.conj()) for q in null_space(E.conj().T).T]
Ss=[]
for i in range(4):
 for j in range(i+1,4):
  ids=[]
  for x in range(16):
   u=(x>>(3-i))&1;v=(x>>(3-j))&1;ids.append(x^((u^v)<<(3-i))^((u^v)<<(3-j)))
  Ss.append(Vhat@np.eye(16)[ids]@Vhat.conj().T)
Ugood=old.Us[0]
Zfirst=np.kron(P[3],np.eye(8));Uburst=np.kron(Zfirst,np.eye(2))@Ugood
Cdeclared=6.;s=1/7;a=1-s;target=155;t=6;cap=1400;B=31;hbits=5;burst_calls=set(range(500,512))
def ptrD(r):return np.einsum('abad->bd',r.reshape(D,2,D,2))
def superof(fn):
 cols=[]
 for x in range(4):
  z=np.zeros((2,2),complex);z.reshape(-1)[x]=1;cols.append(fn(z).reshape(-1))
 return np.stack(cols,axis=1)
def effect(S):return (S.conj().T@np.eye(2).reshape(-1)).reshape(2,2)
mp=[];checks=[]
for U in [Ugood,Uburst]:
 As=[np.kron(A,np.eye(2))@U@np.kron(E,np.eye(2)) for A in Ds];phis=[]
 for pauli in P:
  Bs=[np.einsum('aiaj->ij',(np.kron(pauli.conj().T,np.eye(2))@A).reshape(2,2,2,2))/2 for A in As]
  phis.append(superof(lambda sig,Bs=Bs:sum(A@sig@A.conj().T for A in Bs)))
 Ts=[]
 for fail in [False,True]:
  def fun(sig):
   out=np.zeros((2,2),complex)
   for S in Ss:
    for sign in [-1,1]:
     Pi=(np.eye(D)+sign*S)/2;Pt=(np.eye(D)+(-sign if fail else sign)*S)/2;Y=np.kron(Pt,np.eye(2));rho=np.kron(Pi@PH/2,sig);out+=ptrD(Y@U@rho@U.conj().T@Y)/6
   return out
  Ts.append(superof(fun))
 W=effect(sum(phis[1:]));F=effect(Ts[1]);assert np.linalg.eigvalsh(Cdeclared*F-W).min()>-1e-10
 # full joint instrument identity on correlated logical/bath input
 x=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));rho=x@x.conj().T;rho/=np.trace(rho)
 tw=sum(np.kron(Q,np.eye(2))@A@np.kron(Q,np.eye(2))@rho@np.kron(Q,np.eye(2))@A.conj().T@np.kron(Q,np.eye(2)) for Q in P for A in As)/4
 ins=np.zeros((4,4),complex)
 for pauli in P:
  for A in As:
   bb=np.einsum('aiaj->ij',(np.kron(pauli.conj().T,np.eye(2))@A).reshape(2,2,2,2))/2;AA=np.kron(pauli,bb);ins+=AA@rho@AA.conj().T
 assert np.linalg.norm(tw-ins)<1e-11
 checks.append({'test_failure_effect_eigenvalues':np.linalg.eigvalsh(F).real.tolist(),'service_bad_effect_eigenvalues':np.linalg.eigvalsh(W).real.tolist(),'hazard_slack_min_eigenvalue':float(np.linalg.eigvalsh(Cdeclared*F-W).min()),'joint_twirl_identity_residual':float(np.linalg.norm(tw-ins)),'memory_map_noncommutation_norm':float(np.linalg.norm(phis[0]@Ts[0]-Ts[0]@phis[0]))})
 mp.append({'good':phis[0],'bad':sum(phis[1:]),'paulis':phis,'testpass':Ts[0],'testfail':Ts[1]})
sigma=np.outer(old.bath,old.bath.conj());tridx=[0,3]
def trsum(x):return float(np.sum(x[...,tridx]).real)
def exact(runburst):
 state=np.zeros((target,t+2,4),complex);state[0,0]=sigma.reshape(-1);accepted=np.zeros((t+2,4),complex);abort=0.;expectedcalls=0
 for r in range(1,cap+1):
  expectedcalls+=trsum(state);m=mp[int(runburst and r in burst_calls)]
  gp=s*(state@m['good'].T);bp=s*(state@m['bad'].T);tp=a*(state@m['testpass'].T);abort+=a*trsum(state@m['testfail'].T)
  nxt=tp;nxt[1:]+=gp[:-1];nxt[1:,1:]+=bp[:-1,:-1];nxt[1:,-1]+=bp[:-1,-1]
  accepted+=gp[-1];accepted[1:]+=bp[-1,:-1];accepted[-1]+=bp[-1,-1];state=nxt
 abortcap=trsum(state);abort+=abortcap;acc=trsum(accepted);bad=trsum(accepted[-1]);assert abs(acc+abort-1)<2e-9
 return {'accept_probability':acc,'accepted_more_than_t_fault_weight':bad,'accepted_fault_count_weights':[trsum(z) for z in accepted],'abort_probability':abort,'cap_abort_probability':abortcap,'expected_source_calls':expectedcalls}
def trajectories(runburst,N=1000):
 mem=np.tile(sigma.reshape(1,4),(N,1));active=np.ones(N,bool);accepted=np.zeros(N,bool);services=np.zeros(N,int);faults=np.zeros(N,int);ledger=np.zeros((N,target),np.uint8);lastcall=np.zeros(N,int)
 for r in range(1,cap+1):
  ids=np.flatnonzero(active)
  if not len(ids):break
  role=rng.random(len(ids))<s;m=mp[int(runburst and r in burst_calls)]
  for service,group in [(True,ids[role]),(False,ids[~role])]:
   if not len(group):continue
   operators=m['paulis'] if service else [m['testpass'],m['testfail']]
   outs=np.stack([mem[group]@A.T for A in operators],axis=1);probs=outs[:,:,[0,3]].sum(axis=2).real;probs=np.maximum(probs,0);probs/=probs.sum(axis=1)[:,None]
   choices=(rng.random(len(group))[:,None]>np.cumsum(probs,axis=1)).sum(axis=1);choices=np.minimum(choices,len(operators)-1);selected=outs[np.arange(len(group)),choices];norm=selected[:,[0,3]].sum(axis=1).real;mem[group]=selected/norm[:,None]
   if service:
    ledger[group,services[group]]=choices;services[group]+=1;faults[group]+=choices!=0;done=group[services[group]==target];accepted[done]=True;active[done]=False;lastcall[done]=r
   else:
    done=group[choices==1];active[done]=False;lastcall[done]=r
 lastcall[active]=cap
 return {'runs':N,'accepted_count':int(sum(accepted)),'accepted_more_than_t_fault_count':int(sum(accepted&(faults>t))),'mean_native_calls':float(lastcall.mean()),'accepted_fault_histogram':{str(f):int(sum(accepted&(faults==f))) for f in np.unique(faults[accepted])}},ledger,accepted
# Actual reviewed finite-field total decoder on all nonzero sampled accepted patterns (up to50), plus predeclared correctable challenges.
outer=root/'outer_grs_distillation_20261028'/'grs_wrapper_v1.py';spec=importlib.util.spec_from_file_location('grs',outer);grs=importlib.util.module_from_spec(spec);spec.loader.exec_module(grs);g=grs.GF(5,0b100101)
for x in range(1,32):assert g.mul(x,g.inv(x))==1
code=grs.construct(g,B,t);duals=[next(b for b in range(32) if all(g.trace(g.mul(b,1<<l))==int(l==j) for l in range(5))) for j in range(5)]
def decode_ledger(labels):
 ee=[0]*B;ff=[0]*B
 for pos,p in enumerate(labels):
  i,j=divmod(pos,5)
  if p in [1,2]:ee[i]^=1<<j
  if p in [2,3]:ff[i]^=duals[j]
 x,z,ok=grs.one_way_correction(g,code,ee,ff);return all(v==0 for v in x+z),ok
out=[]
for burst in [False,True]:
 ex=exact(burst);mc,ledger,accepted=trajectories(burst);selected=np.flatnonzero(accepted&(np.count_nonzero(ledger,axis=1)>0))[:50];correct=0
 for i in selected:
  good,flag=decode_ledger(ledger[i]);correct+=good
  if np.count_nonzero(ledger[i])<=t:assert good and flag
 out.append({'source':'predeclared_calls500_to511_local_Z_burst' if burst else 'noreset_acquired_frame_collective_retained_bath','exact_compressed_memory_DP':ex,'sampled_actual_instrument_trajectories':mc,'nonzero_accepted_ledgers_actually_outer_decoded':len(selected),'those_outer_outputs_correct':int(correct)})
challenges=[]
for w in [0,1,3,6]:
 for repeat in range(3):
  labels=np.zeros(target,np.uint8);loc=rng.choice(target,w,replace=False);labels[loc]=rng.integers(1,4,size=w);good,flag=decode_ledger(labels);assert good and flag;challenges.append({'inner_faults':w,'outer_correct':good})
R=Cdeclared*s/a;tail=(R/(1+R))**(t+1)
print(json.dumps({'seed':2026102914,'predeclared_design':{'n':4,'inner_logical_qubits':1,'declared_C':Cdeclared,'exact_weighted_C':3,'s':s,'R':R,'test_fail_budget_b':0,'fault_radius_t':t,'outer_GF':32,'outer_J':B,'outer_logical_symbols':B-4*t,'payload_qubits':(B-4*t)*5,'required_inner_services':target,'cap_native_calls':cap,'soundness_halfdiamond_accepted_bound':tail,'endpoint_buffer_qubits_each':target,'burst_calls_1based':[500,511]},'charged_prior_frame_acquisition':{'replayed_file':str(acq.relative_to(root)),'sha256':hashlib.sha256(acq.read_bytes()).hexdigest(),'final_bank_full_array_calls':1000000,'all_finite_banks_in_replayed_fixture_full_array_calls':1000000,'no_bath_reset_between_learning_and_guard':True,'acquisition_confidence_stop_claimed':False},'primitive_instrument_checks':checks,'executions':out,'actual_outer_challenges':challenges,'scope':'Known-generator compressed mathematical execution, not physical access to bath/latent fault labels; actual protocol uses only test records. No full outer amplitude simulation or physical error-free endpoint claim.'},indent=2))
