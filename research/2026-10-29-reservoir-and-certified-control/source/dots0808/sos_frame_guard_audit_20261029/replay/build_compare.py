"""Frozen-data task-optimized frame versus final Hedge/uniform, no new training."""
import numpy as np,json,itertools,math,hashlib
from fractions import Fraction
from pathlib import Path
from scipy.linalg import expm
P=Path(__file__).parent;SRC=P/'inputs'
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);pa=[X,Y,Z]
def kron(xs):
 r=np.array([[1]],complex)
 for x in xs:r=np.kron(r,x)
 return r
Vs=[];Cs=[]
for k in itertools.product(range(-1,2),repeat=3):
 r=sum(x*x for x in k);q=np.array([1-r,*[2*x for x in k]])/(1+r);v=q[0]*I-1j*sum(q[j+1]*pa[j] for j in range(3));Vs.append(v);Cs.append([[np.trace(pa[a]@v@pa[b]@v.conj().T).real/2 for b in range(3)]for a in range(3)])
Vs=np.array(Vs);Cs=np.array(Cs);M=27
bank=json.loads((SRC/'bank_one_axis.json').read_text());hist=json.loads((SRC/'capture_one_axis_result.json').read_text());B=np.array(bank['B']);C=np.array(bank['C']);count=bank['probe_calls'];eta=hist['eta'];p=hist['p']
loss=.75*count-2.25*np.einsum('iab,vab->iv',B,Cs)-20.25*np.einsum('iabcd,vab,vcd->iv',C,Cs,Cs)
logw=-eta*loss/p;probs=np.exp(logw-logw.max(axis=1)[:,None]);probs/=probs.sum(axis=1)[:,None]
sigma=np.array(hist['final_bath_real'])+1j*np.array(hist['final_bath_imag']);assert np.linalg.eigvalsh(sigma).min()>-1e-12
# Ground-truth hidden frame is used ONLY to construct the fixed declared evaluation source.
hidden=hist['hidden_indices'];V=kron([Vs[j] for j in hidden]);Jz=sum(kron([Z if i==j else I for i in range(4)]) for j in range(4))/2
U=expm(-.8j*(np.kron(V@Jz@V.conj().T,Z)+.37*np.kron(np.eye(16),X)));U4=U.reshape(16,2,16,2)
E0=np.zeros((16,2),complex)
for j,x in [(5,.5),(6,-.5),(9,-.5),(10,.5)]:E0[j,0]=x
for j,x in [(3,1),(12,1),(5,-.5),(6,-.5),(9,-.5),(10,-.5)]:E0[j,1]=x/np.sqrt(3)
match=[]
for pairs in [[(0,1),(2,3)],[(0,2),(1,3)],[(0,3),(1,2)]]:
 v=np.zeros(16)
 for bits in itertools.product([0,1],repeat=2):
  out=[0]*4;s=1
  for (a,b),z in zip(pairs,bits):out[a]=z;out[b]=1-z;s*=(-1)**z
  v[sum(bit<<(3-j) for j,bit in enumerate(out))]=s/2
 match.append(E0.conj().T@v)
six=[]
for a in pa:
 _,W=np.linalg.eigh(a);six.extend([W[:,0],W[:,1]])
def superavg(w,A):
 # A has candidate, Kraus, memoryout, memoryin.
 return np.einsum('v,vrab,vrcd->acbd',w,A,A.conj(),optimize=True).reshape(4,4)
def maps(E,w):
 UE=np.einsum('aibj,vbk->vaikj',U4,E,optimize=True)
 L=np.einsum('val,vaikj->vlikj',E.conj(),UE,optimize=True)
 raw=(L[:,0,:,0,:]+L[:,1,:,1,:])/2
 service=superavg(w,UE.transpose(0,1,3,2,4).reshape(len(w),32,2,2))/2
 good=superavg(w,raw[:,None])
 mp=np.zeros((4,4),complex)
 for c in match:
  vin=np.einsum('val,l->va',E,c);O=np.einsum('vaikj,k->vaij',UE,c);A=np.einsum('va,vaij->vij',vin.conj(),O);mp+=superavg(w,A[:,None])/3
 sp=np.zeros((4,4),complex)
 for c in six:
  vin=np.einsum('val,l->va',E,c);O=np.einsum('vaikj,k->vaij',UE,c);A=np.einsum('va,vaij->vij',vin.conj(),O)
  code=np.einsum('vlikj,k->vlij',L,c)
  sp+=(superavg(w,A[:,None])+abs(c[0])**2*(superavg(w,O)-superavg(w,code)))/6
 extra=(superavg(w,UE[:,:,:,0,:])-superavg(w,L[:,:,:,0,:]))/4
 return dict(service=service,raw_good=good,raw_bad=service-good,matching_pass=mp,matching_fail=service-mp,completed_good=good+extra,completed_bad=service-good-extra,six_pass=sp,six_fail=service-sp)
def choi(T):return T.reshape(2,2,2,2).transpose(0,2,1,3).reshape(4,4)
def effect(T):return (T.conj().T@I.reshape(-1)).reshape(2,2)
def guard(ms,kind):
 C,s,good,bad,pa,fa=(2,1/3,ms['raw_good'],ms['raw_bad'],ms['matching_pass'],ms['matching_fail']) if kind=='matching' else (1.5,.4,ms['completed_good'],ms['completed_bad'],ms['six_pass'],ms['six_fail'])
 J=155;t=6;cap=1400;live=np.zeros((J,t+2,4),complex);live[0,0]=sigma.reshape(-1);acc=np.zeros((t+2,4),complex);abort=0.;calls=0.
 tr=lambda v:float(np.sum(v[...,0]+v[...,3]).real)
 for _ in range(cap):
  calls+=tr(live);G=s*(live@good.T);F=s*(live@bad.T);nxt=(1-s)*(live@pa.T);abort+=(1-s)*tr(live@fa.T)
  nxt[1:]+=G[:-1];nxt[1:,1:]+=F[:-1,:-1];nxt[1:,-1]+=F[:-1,-1]
  acc+=G[-1];acc[1:]+=F[-1,:-1];acc[-1]+=F[-1,-1];live=nxt
 A=tr(acc);assert abs(A+abort+tr(live)-1)<1e-9 and -1e-12<=tr(acc[-1])<=A+1e-12
 cost=35*A/calls
 return dict(test=kind,C=C,s=s,required_services=J,t=t,b=0,cap=cap,payload_qubits=35,acceptance=A,expected_native_calls=calls,expected_accepted_payload=35*A,payload_per_call=cost,validation_abort=abort,cap_abort=tr(live),mass_total=A+abort+tr(live),accepted_bad_weight_above6=tr(acc[-1]),formal_accepted_soundness_bound='1/128',pretraining_probe_calls=count,all_pretraining_source_calls=hist['T'],payload_per_call_including_entire_pretraining=35*A/(hist['T']+calls))
frames=[]
for i in range(3):
 cert=json.loads((SRC/f'oracle_one_axis_edge{i}.json').read_text());q=np.array([float(Fraction(x)) for x in cert['rational_quaternion']]);assert abs(q@q-1)<1e-12
 frames.append(q[0]*I-1j*sum(q[j+1]*pa[j] for j in range(3)))
E_sos=kron([I]+frames)@E0
ordinary=json.loads((P/'ordinary_candidates.json').read_text());nmframes=[]
for row in ordinary['rows']:
 q=np.array([float(Fraction(x)) for x in row['ordinary_Nelder_Mead']['rational_quaternion']]);nmframes.append(q[0]*I-1j*sum(q[j+1]*pa[j] for j in range(3)))
E_nm=kron([I]+nmframes)@E0
combos=np.array(list(itertools.product(range(M),repeat=3)));allE=np.einsum('vab,vcd,vef,gbdfk->vgacek',Vs[combos[:,0]],Vs[combos[:,1]],Vs[combos[:,2]],E0.reshape(2,2,2,2,2),optimize=True).reshape(-1,16,2)
weights=probs[0,combos[:,0]]*probs[1,combos[:,1]]*probs[2,combos[:,2]]
rows=[];saved={}
for name,E,w in [('sos',E_sos[None],np.ones(1)),('ordinary_Nelder_Mead',E_nm[None],np.ones(1)),('hedge_final_distribution',allE,weights),('uniform_net_distribution',allE,np.ones(len(combos))/len(combos))]:
 ms=maps(E,w);diagn={}
 for key,T in ms.items():
  assert np.linalg.norm(choi(T)-choi(T).conj().T)<2e-11
  eig=np.linalg.eigvalsh((choi(T)+choi(T).conj().T)/2);assert eig.min()>-2e-11,(name,key,eig)
  saved[name+'_'+key]=T
 assert np.linalg.norm(effect(ms['service'])-I)<1e-11
 for kind,C,gname,fname in [('matching',2,'raw_bad','matching_fail'),('six',1.5,'completed_bad','six_fail')]:
  assert np.linalg.eigvalsh(C*effect(ms[fname])-effect(ms[gname])).min()>-1e-11
 for key in ['raw_bad','completed_bad','matching_fail','six_fail']:
  H=effect(ms[key]);diagn[key]={'actual_carried_bath_probability':float(np.trace(H@sigma).real),'memory_effect_eigenvalues':np.linalg.eigvalsh(H).tolist()}
 row={'candidate_policy':name,'diagnostics':diagn,'guard_results':[guard(ms,kind) for kind in ['matching','six_state']]};rows.append(row);print(name,json.dumps(row),flush=True)
saved.update(sigma=sigma,source_unitary=U,E_sos=E_sos,E_nm=E_nm,E0=E0,hedge_final_probabilities=probs)
np.savez_compressed(P/'maps_and_fixture.npz',**saved)
(P/'results.json').write_text(json.dumps({'scope':'Finite stationary posttraining-source benchmark on one actually carried bath. All candidates predeclared from same bank; no source-based selection, additional training or hardware claim. Distribution candidates independently resampled and retired per call.','rows':rows},indent=2)+'\n')
