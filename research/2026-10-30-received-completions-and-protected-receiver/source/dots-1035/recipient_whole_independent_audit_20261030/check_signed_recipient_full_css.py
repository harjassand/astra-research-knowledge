"""Independent full-distance CSS signed-resource / common-bath Bell contraction.
Steane [[7,1,3]], all physical Bell outcomes, coherent gauge/error correlations.
The finite diagnostic does not prove the native or rate-separation theorem.
"""
import numpy as np,json
from pathlib import Path
n=7;D=128;K=2
H=np.array([[(i>>j)&1 for i in range(1,8)] for j in range(3)],int)
def bitsint(b):return sum(int(v)<<j for j,v in enumerate(b))
CX=[bitsint((np.array([(u>>j)&1 for j in range(3)])@H)%2) for u in range(8)]
V=np.zeros((D,K),complex)
for l in range(K):
 for c in CX:V[c^(127 if l else 0),l]=1/np.sqrt(8)
idx=np.arange(D)
def pp(v,x,z,adj=False):
 # P=X^x Z^z; real representatives, including anti-Hermitian XZ.
 signs=np.array([(-1)**((z*0+(int(i)&z)).bit_count()) for i in idx])
 if adj:return signs[:,None]*v[idx^x]
 out=np.empty_like(v);out[idx^x]=signs[:,None]*v;return out

def syndrome(x,z):
 sx=0;sz=0
 for j in range(7):
  if (x>>j)&1:sx^=j+1
  if (z>>j)&1:sz^=j+1
 return sx|(sz<<3)
reps={}
for wt in range(8):
 for x in range(D):
  for z in range(D):
   if (x|z).bit_count()==wt:reps.setdefault(syndrome(x,z),(x,z))
 if len(reps)==64:break
C=np.zeros((K,64,D),complex)
for s,(x,z) in reps.items():C[:,s,:]=pp(V,x,z).conj().T
assert np.linalg.norm(C.reshape(D,D)@C.reshape(D,D).conj().T-np.eye(D))<1e-12
# Four coherent terms; E/F both supported on site0, so output FE stays weight<=1.
Es=[(0,0),(1,0),(0,1),(1,1)]
Fs=[(0,0),(0,1),(1,0),(1,1)]
gauge=[(0,0),(8,0),(0,16),(32,64)]
c=np.array([1,1j,-.7,.3+.2j],complex);c/=np.linalg.norm(c)
bath=np.array([[1,0],[1,1],[1,1j],[.4,1]],complex)
bath/=np.linalg.norm(bath,axis=1)[:,None]
Vs=[pp(V,*p) for p in gauge];EV=[pp(V,*e) for e in Es]
# Source/resource isometry Gram using the exact tensor contractions.
Gram=np.zeros((K,K),complex)
for a in range(4):
 for b in range(4):
  FaPi=pp(Vs[a],*Fs[a])@Vs[a].conj().T
  FbPi=pp(Vs[b],*Fs[b])@Vs[b].conj().T
  ab=np.vdot(FaPi,FbPi)/K
  Gram+=c[a].conjugate()*c[b]*np.vdot(bath[a],bath[b])*ab*(EV[a].conj().T@EV[b])
assert np.linalg.norm(Gram-np.eye(K))<1e-12
normal=np.zeros((K,K),complex);max_formula=0.;max_factor=0.;nonzero=0
for x in range(D):
 for z in range(D):
  sP=syndrome(x,z)
  if not any(syndrome(*gauge[a])^sP==syndrome(*Es[a]) for a in range(4)):continue
  actual=np.zeros((D,2,K),complex);pred=np.zeros_like(actual)
  for a in range(4):
   inside=Vs[a].conj().T@pp(EV[a],x,z,adj=True)
   Y=pp(pp(Vs[a],*Fs[a]),x,z)@inside/np.sqrt(K*D)
   actual+=c[a]*Y[:,None,:]*bath[a][None,:,None]
   if syndrome(*gauge[a])^sP==syndrome(*Es[a]):
    # Pauli conjugation sign: P F P† = (-1)^(x·zF+z·xF) F.
    fx,fz=Fs[a];phase=(-1)**(((x&fz).bit_count()+(z&fx).bit_count())%2)
    Z=phase*pp(EV[a],fx,fz)/np.sqrt(K*D)
    pred+=c[a]*Z[:,None,:]*bath[a][None,:,None]
  max_formula=max(max_formula,float(np.linalg.norm(actual-pred)))
  out=np.einsum('lsd,dbk->lsbk',C,actual)
  aux=(out[0,:,:,0]+out[1,:,:,1])/2
  target=np.zeros_like(out);target[0,:,:,0]=aux;target[1,:,:,1]=aux
  max_factor=max(max_factor,float(np.linalg.norm(out-target)))
  aa=actual.reshape(D*2,K);normal+=aa.conj().T@aa;nonzero+=1
assert max_formula<1e-12 and max_factor<1e-12 and np.linalg.norm(normal-np.eye(K))<1e-12
# Separate physical CNOT / X_Q / Z_A ordering check on a maximally entangled Q-reference.
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]);Y=1j*X@Z
psi=np.zeros((2,2,2,2),complex) # Q,A,B,ref
for q in range(2):
 for a in range(2):psi[q,a,a,q]=.5
post=np.zeros_like(psi)
for q in range(2):
 for a in range(2):post[q,a^q]=psi[q,a]
ref_target=np.eye(2)/np.sqrt(2);max_bell=0.
for qbit in range(2):
 for abit in range(2):
  bra=np.array([1,(-1)**qbit])/np.sqrt(2)
  branch=np.einsum('q,qbr->br',bra,post[:,abit])
  P={(0,0):I,(0,1):X,(1,0):Z,(1,1):Y}[(qbit,abit)]
  corrected=P@branch
  phase=np.vdot(ref_target,corrected)/.5
  max_bell=max(max_bell,float(np.linalg.norm(corrected-phase*.5*ref_target)))
assert max_bell<1e-12
result={'status':'PASS','code':'Steane [[7,1,3]], full X/Y/Z weight-one correction','all_physical_Bell_labels':D*D,'nonzero_compatible_labels':nonzero,'source_isometry_residual':float(np.linalg.norm(Gram-np.eye(K))),'corrected_channel_normalization_residual':float(np.linalg.norm(normal-np.eye(K))),'joint_signed_formula_residual':max_formula,'ordinary_canonical_logical_factor_residual':max_factor,'physical_CNOT_XQ_ZA_mask_order_residual':max_bell,'explicit_table':'(Q-X-bit,A-Z-bit): 00 I, 01 X, 10 Z, 11 Y','scope':'Finite exact-algebra diagnostic only; supports the independent whole proof, not native rates/absorption'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
