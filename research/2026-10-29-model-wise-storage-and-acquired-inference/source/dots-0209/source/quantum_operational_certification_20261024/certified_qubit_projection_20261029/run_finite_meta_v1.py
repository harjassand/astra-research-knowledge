import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import sys,json,gzip,random
from exact_meta_arithmetic_v1 import ExactMeta
from fractions import Fraction as F
from math import isqrt
from certified_projection_v4 import project_certified,coeff,matrix,scale
from pathlib import Path
import numpy as np
base=Path(__file__).parent
sys.path.insert(0,str(base.parent/'compact_prequential_flag_recovery_20261028'))

I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex);pa=[I,X,Y,Z]
def exp(t,P):return np.cos(t)*np.eye(P.shape[0])-1j*np.sin(t)*P
U=np.eye(4,dtype=complex)
for t,P in [(.37,np.kron(X,X)),(.53,np.kron(Z,Y)),(.29,np.kron(Y,I))]:U=exp(t,P)@U
Pis=[np.kron(np.diag([1.,0.]),I),np.kron(np.diag([0.,1.]),I)]
Am=[p@U for p in Pis];c=.2;kappa=.01
phis=[np.array([np.sqrt((1+c)/2),(-1)**m*np.sqrt((1-c)/2)]) for m in range(2)]
C=exp(kappa,np.kron(Z,np.kron(I,X)))
Vs=[C@np.kron(v[:,None],a) for v,a in zip(phis,Am)]
assert np.max(abs(sum(v.conj().T@v for v in Vs)-np.eye(4)))<1e-12
# Cross term vanishes in isometry with logical Pauli labels, too.
assert np.max(abs(Vs[0].conj().T@Vs[1]))<1e-12
labels=[0,15];H=[(I+X)/2,(I-X)/2]
def emit(mem):
 blocks=[v@mem@v.conj().T for v in Vs]
 sig=[np.trace(b.reshape(2,4,2,4),axis1=1,axis2=3) for b in blocks]
 return blocks,np.array(sig)
def update(block,E):return np.einsum('ambn,ba->mn',block.reshape(2,4,2,4),E)
def normrho(rho):
 rho=(rho+rho.conj().T)/2;return rho/np.trace(rho).real
N=int(sys.argv[1]) if len(sys.argv)>1 else 1024
assert isqrt(N)**2==N
xi=F(1,256*N*N);eta=F(1,4*isqrt(N));records=[];runs=[];graderr=0;minH=1.;maxcomm=0.;maxrolechange=0.
for seed in [9301,9302,9303]:
 certs=[]
 exactmeta=ExactMeta(N);private_rng=random.Random(seed+100000)
 rng=np.random.default_rng(seed);T=int(rng.integers(1,N+1));v=np.ones(4)/2;mem=np.outer(v,v)
 known=[0];K=15;effects=[[F(1),F(0),F(0),F(0)],[F(0)]*4]
 M=np.zeros((16,2,2),complex);M[0]=I;lw=np.log([.9,.1]);stats=np.zeros(4);ns=ne=0;terminal=None
 for t in range(1,N+1):
  blocks,sig=emit(mem);pr=np.trace(sig,axis1=1,axis2=2).real;pr/=sum(pr)
  pn,pd=exactmeta.probability();p=np.array([pn/pd,(pd-pn)/pd])
  baseline=float(np.trace(sig[0]).real);learn=float(sum(np.trace(M[x]@s).real for x,s in zip(labels,sig)));hel=float(sum(np.trace(h@s).real for h,s in zip(H,sig)));meta=p[0]*baseline+p[1]*learn
  stats+=[baseline,learn,hel,meta];minH=min(minH,hel)
  if t==T:terminal={'t':t,'baseline_score':baseline,'learner_score':learn,'meta_averaged_score':meta,'meta_probabilities':p.tolist()}
  # Conditional expectation of importance-weighted shadow gradient equals sigma.
  rebuilt=np.zeros_like(sig)
  for m in range(2):
   for W in pa:
    for b in ([1] if np.array_equal(W,I) else [-1,1]):
     E=I if np.array_equal(W,I) else (I+b*W)/2
     probability=float(np.trace(update(blocks[m],E)).real)/4
     rebuilt[m]+=probability*2*b*W
  graderr=max(graderr,float(np.max(abs(rebuilt-sig))))
  m=int(rng.choice(2,p=pr));x=labels[m]
  if private_rng.getrandbits(2)==0:
   ns+=1;wi=int(rng.integers(4));W=pa[wi]
   if wi==0:b=1;E=I
   else:
    plus=float(np.trace(update(blocks[m],(I+W)/2)).real)/pr[m]
    b=1 if rng.random()<np.clip(plus,0,1) else -1;E=(I+b*W)/2
   new=update(blocks[m],E)
   if x not in known:
    default=effects.pop();new_effect=scale(F(1,K),default);K-=1
    effects.append(new_effect);known.append(x)
    if K:effects.append(scale(F(K,K+1),default))
   center=[e[:] for e in effects];center[known.index(x)][wi]+=eta*8*b
   effects,certificate=project_certified(center,[1]*len(known)+([K] if K else []),xi)
   certificate.update(seed=seed,t=t);certs.append(certificate)
   M=np.zeros((16,2,2),complex)
   for j,label in enumerate(known):M[label]=matrix(effects[j])
   if K:
    for label in set(range(16))-set(known):M[label]=matrix(scale(F(1,K),effects[-1]))
   records.append([seed,t,0,x,wi,b,-1,-1])
  else:
   ne+=1;i=exactmeta.select(private_rng)
   if i==0:z=0;E=I
   else:
    probs=np.array([np.trace(e@sig[m]).real for e in M]);probs=np.maximum(probs,0);probs/=sum(probs)
    z=int(rng.choice(16,p=probs));E=M[z]
   new=update(blocks[m],E);loss=int(z!=x);exactmeta.update(i,loss)
   records.append([seed,t,1,x,-1,-1,i,z])
  new=normrho(new);maxcomm=max(maxcomm,float(np.linalg.norm(new@mem-mem@new)))
  # Flag X measurement compared with discard on the SAME returned branch: demonstrates possible steering.
  plus=update(blocks[m],(I+X)/2)
  if np.trace(plus).real>1e-10:
   maxrolechange=max(maxrolechange,float(np.linalg.norm(normrho(plus)-normrho(update(blocks[m],I)))))
  mem=new
 with gzip.open(base/f'meta_certificates_seed{seed}_N{N}_finite_meta_v1.json.gz','wt') as f:json.dump(certs,f,separators=(',',':'))
 print('completed',seed,'certificates',len(certs),flush=True)
 runs.append({'exact_meta_budgets':exactmeta.budgets(),'certified_projection_steps':len(certs),'max_certified_gap':max(c['gap_float'] for c in certs),'seed':seed,'N':N,'shadow_calls':ns,'evaluation_calls':ne,'average_baseline_score':stats[0]/N,'average_predictable_learner_score':stats[1]/N,'average_informed_fixed_X_score':stats[2]/N,'average_meta_score':stats[3]/N,'terminal':terminal,'final_meta_weights':[w/sum(exactmeta.weights) for w in exactmeta.weights],'scope':'conditional-path diagnostics on this actual mixed occupation, not confidence or expected oracle guarantee'})
result={'source_calls_simulated':3*N,'min_informed_fixed_X_conditional_score':minH,'analytic_uniform_fixed_X_score':(1+np.sqrt(1-.2**2)*np.cos(.02))/2,'maximum_conditional_gradient_error':graderr,'maximum_successive_memory_commutator':maxcomm,'maximum_conditional_flag_measurement_steering_Fnorm':maxrolechange,'runs':runs,'scope':'predeclared new high-oracle family, floating full conditional-instrument simulation; exact rational compressed learner projection certificates; floating source instruments; exact rational EXP3 arithmetic with rigorously bounded dyadic exponential factors and capped exact-rational private coins; no hardware or statistical significance claim'}
(base/f'finite_meta_summary_N{N}_v1.json').write_text(json.dumps(result,indent=2)+'\n');np.save(base/f'finite_meta_records_N{N}_v1.npy',np.array(records,dtype=np.int64));print(json.dumps(result))
