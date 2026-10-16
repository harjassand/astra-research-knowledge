"""Own finite-dimensional illustrative checks; all constants are algebraic test inputs."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import numpy as np,json,itertools
from scipy.linalg import expm
from pathlib import Path
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1.,-1.]);Id=np.eye(8)
def k(a,b,c):return np.kron(np.kron(a,b),c)
ZA=k(Z,I,I);ZC=k(I,Z,I);P={'A':[(Id+ZA)/2,(Id-ZA)/2],'C':[(Id+ZC)/2,(Id-ZC)/2]}
H=.4*k(X,I,X)+.5*k(I,X,Z)+.27*k(I,I,Y)+.19*k(Z,I,Z)+.11*k(I,Z,X)
F={'A':expm(-1j*.61*k(Y,I,Z)),'C':expm(-1j*.53*k(I,X,Y))};eps={'A':.02,'C':.03}
# slot order: A0,C0,C1,A1,C2,A2,C3. Faulty branch need not measure.
steps=[(0,'A',False),(0,'C',False),(1/3,'C',True),(1/6,'A',True),(1/6,'C',True),(1/3,'A',True),(0,'C',True)]
branches=[(Id,{'A':0,'C':0},0,0,0)]
for slot,(dt,parent,compare) in enumerate(steps):
 U=expm(-1j*dt*H);new=[];bit=1 if parent=='A' else 2
 for K,last,fault,changes,pattern in branches:
  K=U@K
  for outcome in [0,1]:
   lastnew=dict(last);lastnew[parent]=outcome
   new.append((np.sqrt(1-eps[parent])*P[parent][outcome]@K,lastnew,fault,changes|(bit if compare and outcome!=last[parent] else 0),pattern))
  new.append((np.sqrt(eps[parent])*F[parent]@K,dict(last),fault|bit,changes,pattern|(1<<slot)))
 branches=new
assert len(branches)==3**7
by_pattern={};total=np.zeros((8,8),complex);event={m:np.zeros((8,8),complex) for m in [1,2,3]}
for K,last,fault,changes,pattern in branches:
 E=K.conj().T@K;total+=E;by_pattern.setdefault(pattern,[]).append((E,fault,changes))
 for m in event:
  if (fault|changes)&m==m:event[m]+=E
assert np.linalg.norm(total-Id,2)<2e-13
p={1:.4**2/2,2:.5**2/3};f={1:1-(1-.02)**3,2:1-(1-.03)**4};r={b:f[b]+(1-f[b])*p[b] for b in [1,2]}
actual=[]
for m,E in event.items():
 bound=np.prod([r[b] for b in [1,2] if m&b]);val=float(np.linalg.eigvalsh((E+E.conj().T)/2)[-1]);assert val<=bound+1e-13;actual.append({'selected_parent_mask':m,'effect_max':val,'bound':float(bound)})
conditional_checks=0
for pattern,es in by_pattern.items():
 weight=np.prod([eps[parent] if pattern>>slot&1 else 1-eps[parent] for slot,(_,parent,_) in enumerate(steps)])
 norm=sum(E for E,_,_ in es)/weight;assert np.linalg.norm(norm-Id,2)<3e-12
 faulty=es[0][1]
 for m in [1,2,3]:
  if m&faulty:continue
  E=sum((E for E,_,change in es if change&m==m),start=np.zeros((8,8),complex))/weight
  val=float(np.linalg.eigvalsh((E+E.conj().T)/2)[-1]);bound=np.prod([p[b] for b in [1,2] if m&b]);assert val<=bound+2e-12;conditional_checks+=1
# Unnormalized Choi convention: J=sum vec(K)vec(K)^dagger.
def choi(kraus):return sum(np.outer(a.reshape(-1,order='F'),a.reshape(-1,order='F').conj()) for a in kraus)
P0=np.diag([1.,0]);P1=np.diag([0.,1]);JD=choi([P0,P1]);coherent=[]
for theta in [.1,.01,.001]:
 U=expm(-1j*theta*X);JE=choi([U@P0,U@P1]);v=np.array([-1j*np.sin(theta),np.cos(theta),0,0]);assert np.linalg.norm(JE@v)<1e-14
 w=.5;witness=float(np.real(v.conj()@(JE-w*JD)@v));assert abs(witness+w*np.sin(theta)**2)<1e-14 and witness<0
 coherent.append({'theta':theta,'tested_positive_weight':w,'kernel_witness':witness,'analytic_witness':-w*np.sin(theta)**2,'channel_diamond_upper_bound':4*np.sin(theta/2)})
out={'status':'PASS','actual_CP_branches':len(branches),'coin_patterns':len(by_pattern),'normalization_error':float(np.linalg.norm(total-Id,2)),'conditional_clean_subset_checks':conditional_checks,'parent_effects':actual,'coherent_Choi_checks':coherent,'constants_are_device_inputs':False,'method':'complete finite-dimensional Kraus enumeration and floating-point dense matrix functions; analytic proof separate'}
Path(__file__).with_name('cp_coin_bridge_check_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
