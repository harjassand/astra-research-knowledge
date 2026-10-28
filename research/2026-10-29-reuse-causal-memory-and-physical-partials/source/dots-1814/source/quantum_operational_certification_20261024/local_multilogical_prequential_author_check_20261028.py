#!/usr/bin/env python3
"""Deterministic prescribed-matrix/Born-law check, NOT an acquired learner run."""
import itertools,json,hashlib,math
from pathlib import Path
import numpy as np
P=[np.eye(2,dtype=complex),np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1,-1]).astype(complex)]
I=P[0]
def kron(*xs):
 a=np.array([[1]],complex)
 for x in xs:a=np.kron(a,x)
 return a
def word(w):return kron(*(P[i] for i in w))
def ptrace(a,keep,dims):
 n=len(dims); a=a.reshape(tuple(dims)*2); dims=list(dims)
 for i in reversed(range(n)):
  if i not in keep:a=np.trace(a,axis1=i,axis2=i+len(dims));dims.pop(i)
 return a.reshape(math.prod(dims),math.prod(dims))
def embed(a,sites,n):
 sites=list(sites); rest=[i for i in range(n) if i not in sites]; order=sites+rest
 b=kron(a,np.eye(2**len(rest))).reshape([2]*(2*n))
 perm=[order.index(i) for i in range(n)]
 return b.transpose(perm+[i+n for i in perm]).reshape(2**n,2**n)
def rot(pauli,t):
 return ((1-t*t)*np.eye(pauli.shape[0])+2j*t*pauli)/(1+t*t)
def err(a,b):return float(np.linalg.norm(a-b))
def density(v):return np.outer(v,v.conj())
def min_eig(a):return float(np.linalg.eigvalsh((a+a.conj().T)/2).min())
res=[]
def ck(name,v,tol=2e-10):
 v=float(v);res.append((name,v));assert v<=tol,(name,v)
# Rational complex hidden U and a coherent retained-memory isometry.
U=rot(word([3,1,0]),1/7)@rot(word([0,3,1]),2/9)@rot(word([2,0,3]),1/11)
ck('hidden_unitarity',err(U.conj().T@U,np.eye(8)))
t=1/257;a=(1-t*t)/(1+t*t);b=2*t/(1+t*t)
V=np.array([[a,0],[0,b],[0,a],[b,0]],complex)
V1=kron(rot(P[3],1/97),I)@V
ck('memory_isometry',err(V.conj().T@V,I))
# Each tuple is a positive Pauli/gauge CP term. Identity dominates every error map.
terms=[((0,0),.7,V),((0,0),.1,V1),((1,0),.05,V),((3,0),.05,V1),((0,1),.05,V),((0,3),.05,V1)]
Ug=kron(U,I)
def source(l,sigma):
 out=np.zeros((16,16),complex)
 for alpha,p,v in terms:
  g=v@sigma@v.conj().T
  pa=word(alpha);out+=p*kron(pa@l@pa.conj().T,g)
 return Ug@out@Ug.conj().T
# Actual conditional states from a chosen positive-probability record, not supplied independently.
psi=np.array([1,1j])/math.sqrt(2);sigmas=[density(psi)]
branch_ps=[]
for lab in [((1,1),(1,-1),(2,3,1),(1,-1,1)),((3,1),(-1,1),(3,2,1),(-1,1,1))]:
 axes,signs,outaxes,outs=lab
 l=kron(*((I+s*P[j])/2 for j,s in zip(axes,signs)))
 vout=kron(*((I+s*P[j])/2 for j,s in zip(outaxes,outs)))
 post=ptrace(kron(vout,I)@source(l,sigmas[-1])@kron(vout,I),[3],[2]*4)
 p=float(np.trace(post).real);assert p>1e-8
 branch_ps.append(p);sigmas.append(post/p)
comm=max(err(x@y,y@x) for x in sigmas for y in sigmas)
assert comm>1e-4
# Every actual product measurement setting/outcome, including zero-probability records.
records=[]
for axes in itertools.product([1,2,3],repeat=3):
 for outs in itertools.product([-1,1],repeat=3):
  pis=[(I+s*P[j])/2 for j,s in zip(axes,outs)]
  effect=kron(*pis)/27;shadow=kron(*(3*x-I for x in pis))
  records.append((effect,shadow))
EE=np.array([x[0] for x in records]);HH=np.array([x[1] for x in records]);H2=HH@HH
ck('snapshot_F_squared',max(abs(np.trace(x@x).real-125) for x in HH))
ck('snapshot_operator_norm',max(abs(np.linalg.norm(x,2)-8) for x in HH))
phis=lambda rho:sum((2**(3-len(S)))*embed(ptrace(rho,S,[2]*3),S,3) for k in range(4) for S in itertools.combinations(range(3),k))
B={(i,j):U@embed(P[j],[i],3)@U.conj().T for i in range(2) for j in[1,3]}
# Learned hypotheses are prescribed rational-unitary conjugations, not fitted samples.
S={}
for i,j in B:
 v=rot(word([1,2,3] if (i+j)%2 else [3,1,2]),(i+1)/113)
 S[i,j]=v@B[i,j]@v.conj().T
 ck(f'learned_reflection_{i}_{j}',err(S[i,j]@S[i,j],np.eye(8)))
# Build actual coherent receiver (two overlapping blocks), preserving full two-qubit R.
Vrec=np.eye(32,dtype=complex)
for i in range(2):
 x=embed(P[1],[i],2);p0=embed((I+P[3])/2,[i],2);p1=embed((I-P[3])/2,[i],2)
 cz=kron((np.eye(8)+S[i,3])/2,np.eye(4))+kron((np.eye(8)-S[i,3])/2,x)
 cx=kron(np.eye(8),p0)+kron(S[i,1],p1)
 for gate in[cz,cx,cz]:Vrec=gate@Vrec
ck('whole_receiver_unitarity',err(Vrec.conj().T@Vrec,np.eye(32)))
phi=density(np.eye(4).reshape(-1)/2)
UU=kron(np.eye(4),U,np.eye(4));VV=kron(np.eye(4),Vrec)
def bell_fe(rho):
 z=rho.reshape(4,8,4,4,8,4)
 return float(sum(z[a,p,a,b,p,b] for a in range(4) for b in range(4) for p in range(8)).real/4)
def extraction(gauge,noisy=False):
 rho=np.zeros((128,128),complex)
 if noisy:
  for alpha,g in gauge.items():
   pp=kron(np.eye(4),word(alpha));rho+=kron(pp@phi@pp.conj().T,g,np.eye(4)/4)
 else:rho=kron(phi,gauge,np.eye(4)/4)
 rho=UU@rho@UU.conj().T;rho=VV@rho@VV.conj().T
 return 1-bell_fe(rho),rho
law_count=0;moment_count=0;max_oracle_excess=0;details=[]
for hi,sigma in enumerate(sigmas):
 gauges={}
 for alpha,p,v in terms:gauges[alpha]=gauges.get(alpha,0)+p*ptrace(v@sigma@v.conj().T,[0],[2,2])
 gauge=sum(gauges.values());rho=U@kron(np.eye(4)/4,gauge)@U.conj().T
 deltas={};R={}
 for i,j in B:
  h=sum((1 if alpha[i] in[0,j] else -1)*g for alpha,g in gauges.items())
  R[i,j]=U@kron(np.eye(4)/4,h)@U.conj().T
  deltas[i,j]=B[i,j]@R[i,j]
  assert min_eig(R[i,j]-.5*rho)>-1e-12
  assert min_eig(rho-R[i,j])>-1e-12
  ck(f'commuting_gauge_{hi}_{i}_{j}',err(B[i,j]@rho,rho@B[i,j]))
 # Full actual input/measurement law; no synthetic supplied contrast coefficients.
 means={(i,j):np.zeros((8,8),complex) for i,j in B}
 for axes in itertools.product([1,3],repeat=2):
  for signs in itertools.product([-1,1],repeat=2):
   l=kron(*((I+s*P[j])/2 for j,s in zip(axes,signs)))
   out=ptrace(source(l,sigma),[0,1,2],[2]*4)
   probs=np.einsum('rij,ji->r',EE,out).real
   assert probs.min()>-1e-12;ck(f'Born_normalization_{law_count}',abs(probs.sum()-1))
   m=np.einsum('r,rij->ij',probs,HH);m2=np.einsum('r,rij->ij',probs,H2)
   ck(f'shadow_mean_{law_count}',err(m,out));ck(f'shadow_second_{law_count}',err(m2,phis(out)))
   assert min_eig(27*np.eye(8)-m2)>-1e-10
   for i,j in B:
    if axes[i]==j:means[i,j]-=signs[i]*m/16
   law_count+=len(records);moment_count+=1
 for i,j in B:ck(f'conditional_gradient_{hi}_{i}_{j}',err(means[i,j],-deltas[i,j]/2))
 # Coarse own-X-sign law, other current signs explicitly averaged.
 for i in range(2):
  mu=np.zeros((8,8),complex)
  for signs in itertools.product([-1,1],repeat=2):
   l=kron(*((I+s*P[1])/2 for s in signs));mu+=signs[i]*ptrace(source(l,sigma),[0,1,2],[2]*4)/4
  ck(f'coarse_contrast_{hi}_{i}',err(mu,deltas[i,1]))
  assert np.linalg.norm(mu,'nuc')>=.5-1e-12
  # Embed into five physical sites to test a truly disjoint two-site readout.
  expanded=kron(mu,np.eye(4)/4)
  ck(f'disjoint_marginal_{hi}_{i}',np.linalg.norm(ptrace(expanded,[3,4],[2]*5)))
 # Excess -> weighted reflection errors -> one actual full-reference receiver.
 ds={};es={}
 for i,j in B:
  aa=S[i,j];pp=np.eye(8)-(aa@B[i,j]+B[i,j]@aa)/2
  assert min_eig(pp)>-1e-12
  es[i,j]=float(np.trace((B[i,j]-aa)@deltas[i,j]).real/2)
  ds[i,j]=float(np.trace(rho@(aa-B[i,j])@(aa-B[i,j])).real)
  assert ds[i,j]<=4*es[i,j]/.5+1e-10
 virtual,rfull=extraction(gauge)
 cone=3*2*sum(ds[i,3]+ds[i,1]/2 for i in range(2))
 assert virtual<=cone+1e-10
 noisy,_=extraction(gauges,True);oracle=1-float(np.trace(gauges[(0,0)]).real)
 excess=noisy-oracle
 assert excess>=-1e-10 and excess<=virtual+1e-10
 max_oracle_excess=max(max_oracle_excess,excess)
 # True ideal subset/prefix invariance INCLUDING future-accessible memory M'.
 gext=sum(p*v@sigma@v.conj().T for alpha,p,v in terms)
 physical=Ug@kron(np.eye(4)/4,gext)@Ug.conj().T
 extended=kron(physical,np.eye(4)/4) # P(8),M'(2),anc(4)
 for i,j in B:
  # Gate acts on P,anc only and is lifted around untouched memory.
  if j==3:
   c0=(np.eye(8)+B[i,j])/2;c1=(np.eye(8)-B[i,j])/2
   gate=kron(c0,I,np.eye(4))+kron(c1,I,embed(P[1],[i],2))
  else:gate=kron(np.eye(8),I,embed((I+P[3])/2,[i],2))+kron(B[i,j],I,embed((I-P[3])/2,[i],2))
  ck(f'ideal_prefix_memory_invariance_{hi}_{i}_{j}',err(gate@extended@gate.conj().T,extended))
 details.append({'history':hi,'gauge_eigenvalues':np.linalg.eigvalsh(gauge).tolist(),'virtual_joint_Bell_loss':virtual,'cone_upper_bound':cone,'noisy_joint_Bell_loss':noisy,'oracle_joint_Bell_loss':oracle,'oracle_excess':excess})
# Exact integer horizon checks and clipping-margin arithmetic.
caps=[]
for n,q,w in[(3,2,1),(9,4,2),(32,8,3),(100,20,4)]:
 W=min(n,3*w-2);C=min(q,2*W-1);K=min(q,W+2*(C-1)*(W-1));A=min(q,K*K)
 R0=2**((W+1)//2);G0=math.isqrt(5**W)+(math.isqrt(5**W)**2<5**W)
 assert R0**2<=2*2**W and G0**2<=4*5**W
 # epsilon=1/8,kappa=1/2
 target=(1152*A*q*R0*G0*16)**2;N=1
 while N<target:N*=4
 assert target<=N<4*target
 caps.append({'n':n,'q':q,'w':w,'W':W,'A':A,'N':N})
source=Path(__file__).with_name('ordinary_local_multilogical_prequential_contractions_20261028.md')
out={'status':'PASS_DETERMINISTIC_PRESCRIBED_MATRIX_DIAGNOSTIC','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'source_calls':0,'RNG_draws':0,'acquired_learner_run':False,'production_optimizer_or_gate_synthesis_executed':False,'actual_Born_law_terms_enumerated':law_count,'full_shadow_moment_cases':moment_count,'conditional_memory_states':len(sigmas),'actual_prefix_branch_probabilities':branch_ps,'conditional_memory_commutator_norm':comm,'max_checked_residual':max(v for n,v in res),'max_oracle_excess':max_oracle_excess,'full_reference_logical_qubits':2,'histories':details,'horizon_cases':caps,'scope':'Actual ordinary product input/readout laws and coherent retained-memory prefix checks; prescribed learned reflections, NOT count-acquired recovery. All floating residual checks use deterministic matrices and explicit tolerances.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
