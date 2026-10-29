"""n6 physical permutation orbit, full 64-dimensional output and memory2.
Simulation checks, not a replacement for all-n representation proof.
"""
import numpy as np,itertools,json,hashlib
from pathlib import Path
from scipy.linalg import expm,null_space
rng=np.random.default_rng(202610290416);n=6;D=64;d=5;K=4;m=2

def matchings(items):
 if not items:yield [];return
 a=items[0]
 for j in range(1,len(items)):
  b=items[j]
  for rest in matchings(items[1:j]+items[j+1:]):yield [(a,b)]+rest
Ms=list(matchings(list(range(n))))
def singlet(M):
 v=np.zeros(D)
 for x in range(D):
  bits=[(x>>(n-1-j))&1 for j in range(n)]
  if all(bits[a]!=bits[b] for a,b in M):v[x]=np.prod([1 if bits[a]==0 else -1 for a,b in M])/np.sqrt(2**(n//2))
 return v
states=np.array([singlet(M) for M in Ms]);V=[]
for a in states:
 v=a.copy()
 for w in V:v-=w*np.vdot(w,v)
 if np.linalg.norm(v)>1e-10:V.append(v/np.linalg.norm(v))
V=np.array(V).T;assert V.shape==(D,d);Q=V[:,:K];VP=np.kron(V,np.eye(m));QP=np.kron(Q,np.eye(m))
perms=list(itertools.permutations(range(n)));indices=[];Ds=[]
for p in perms:
 ids=[]
 for x in range(D):
  bits=[(x>>(n-1-j))&1 for j in range(n)];ids.append(sum(bits[p[j]]<<(n-1-j) for j in range(n)))
 ids=np.array(ids);# U_p rows e_ids, inverse implemented by argsort.
 Uv=V[ids];R=V.conj().T@Uv;assert np.linalg.norm(Uv-V@R)<1e-12
 indices.append(np.argsort(ids));Ds.append(R)
assert np.linalg.norm(sum(R@np.diag([1,1,1,1,0])@R.conj().T for R in Ds)/720-K/d*np.eye(d))<1e-12
# TP decoder Q back to K, with physical complement reset to logical0.
Dkraus=[Q.conj().T]+[np.outer(np.eye(K)[0],v.conj()) for v in null_space(Q.conj().T).T]
def decoder(r):
 out=np.zeros((K*m,K*m),complex)
 # Preserve full physical output, including bath correlations on leakage.
 for A in Dkraus:
  B=np.kron(A,np.eye(m));out+=B@r@B.conj().T
 return out

def scalar(W):return np.einsum('aiaj->ij',(VP.conj().T@W).reshape(d,m,d,m))/d

def matching_failure(Ws,sig):
 q=0.
 for v in states:
  x=V.conj().T@v;rho=np.kron(np.outer(x,x.conj()),sig);out=sum(W@rho@W.conj().T for W in Ws);P=np.kron(np.outer(v,v.conj()),np.eye(m));q+=np.trace(out-P@out).real/len(states)
 return float(q)

def fixed_fe(Ws,sig):
 vals,U=np.linalg.eigh(sig);out=0.
 for W in Ws:
  for A in Dkraus:
   Z=np.kron(A,np.eye(m))@W@np.kron(np.eye(d)[:,:K],np.eye(m))
   for j in range(m):
    for ev,u in zip(vals,U.T):
     B=np.einsum('aibj,j->aib',Z.reshape(K,m,K,m),u)[:,j,:]*np.sqrt(max(ev,0));out+=abs(np.trace(B))**2/K**2
 return float(out)

def run(name,Ws):
 assert np.linalg.norm(sum(W.conj().T@W for W in Ws)-np.eye(d*m))<1e-11
 Bs=[scalar(W) for W in Ws];good=sum(B.conj().T@B for B in Bs);H=np.eye(m)-good
 meanR=[np.zeros_like(W) for W in Ws];eff=np.zeros((d*m,d*m),complex)
 # Include genuinely correlated logical/bath test states, not bath product only.
 x=rng.normal(size=(K*m,K*m))+1j*rng.normal(size=(K*m,K*m));rho=x@x.conj().T;rho/=np.trace(rho);emb=np.kron(np.eye(d)[:,:K],np.eye(m));rin=emb@rho@emb.conj().T
 tw=np.zeros((D*m,D*m),complex);bad=np.zeros_like(tw)
 for ids,R in zip(indices,Ds):
  right=np.kron(R,np.eye(m))
  for ai,(W,B) in enumerate(zip(Ws,Bs)):
   T=(W@right).reshape(D,m,d*m)[ids].reshape(D*m,d*m);Remainder=T-np.kron(V,B);meanR[ai]+=Remainder/720;eff+=Remainder.conj().T@Remainder/720;tw+=T@rin@T.conj().T/720;bad+=Remainder@rin@Remainder.conj().T/720
 g=sum(np.kron(V,B)@rin@np.kron(V,B).conj().T for B in Bs)
 targetgood=sum(np.kron(np.eye(K),B)@rho@np.kron(np.eye(K),B).conj().T for B in Bs)
 sig=np.array([[.63,.11+.17j],[.11-.17j,.37]])
 q=matching_failure(Ws,sig);pb=float(np.trace(H@sig).real)
 out={'name':name,'CP_Kraus_count':len(Ws),'mean_remainder_norms':[float(np.linalg.norm(R)) for R in meanR],'bad_effect_tensor_residual':float(np.linalg.norm(eff-np.kron(np.eye(d),H))),'full_correlated_output_split_residual':float(np.linalg.norm(tw-g-bad)),'decoded_good_identity_residual':float(np.linalg.norm(decoder(g)-targetgood)),'decoded_correlated_split_residual':float(np.linalg.norm(decoder(tw)-targetgood-decoder(bad))),'bad_effect_eigenvalues':np.linalg.eigvalsh(H).tolist(),'matching_failure':q,'full_P_bad_probability':pb,'C_full_times_q':1.6*q,'fixed_Q_Bell_loss':1-fixed_fe(Ws,sig),'source_output_leakage':float(np.trace((np.eye(D*m)-VP@VP.conj().T)@sum(W@np.kron(np.eye(d)/d,sig)@W.conj().T for W in Ws)).real)}
 assert max(out['mean_remainder_norms'])<1e-11
 assert out['bad_effect_tensor_residual']<1e-11 and out['decoded_correlated_split_residual']<1e-11
 assert pb<=1.6*q+1e-11
 return out
# Exact fixed-subcode failure of coefficient without orbit: reflection in one matching state.
v=states[0];U=np.eye(D)-2*np.outer(v,v);rows=[run('matching_state_reflection_fixed_Q_counterexample',[np.kron(U,np.eye(m))@VP])]
# Actual orbit Bell loss for the reflection, including Q-complement reset contribution.
fe=[]
for ids in indices:
 w=Q.conj().T@v[ids];ss=float(np.vdot(w,w).real);fe.append((1-2*ss/K)**2+4*(1-ss)*abs(w[0])**2/K**2)
rows[0]['actual_orbit_Q_Bell_loss']=float(1-np.mean(fe))
# Arbitrary coherent joint source, including physical leakage outside singlet space.
A=rng.normal(size=(D*m,D*m))+1j*rng.normal(size=(D*m,D*m));A=(A+A.conj().T)/np.sqrt(D*m);U=expm(-.31j*A);rows.append(run('coherent_joint_memory_with_leakage',[U@VP]))
# Nonunital physical amplitude damping, coherently preceded by the same joint source.
gamma=.37;A0=np.diag([1,np.sqrt(1-gamma)]);A1=np.array([[0,np.sqrt(gamma)],[0,0]])
Ws=[np.kron(np.kron(A,np.eye(32)),np.eye(m))@U@VP for A in [A0,A1]];rows.append(run('nonunital_damping_plus_joint_memory',[*Ws]))
out={'seed':202610290416,'n':n,'full_singlet_dimension':d,'logical_subcode_dimension':K,'permutations':720,'matchings':15,'memory_dimension':m,'physical_output_dimension':D,'C_full':1.6,'C_old_subcode':2.,'checks':rows,'scope':'Exact physical finite construction with numerical floating checks; not hardware or interval certification. Uniform private permutation before source, inverse after source, then complete CPTP Q-reset decoder. No logical Pauli pad used.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
