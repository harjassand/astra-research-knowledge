"""Actual Alice terminal: local raw killing, conservative tilt and Q-zero range.
All W columns and incomplete forest masks retained. This is not a whole-FSM test.
"""
import numpy as np,json
from pathlib import Path
from scipy.linalg import eigh,eigvalsh
I2=np.eye(2);I4=np.eye(4);X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]);H=np.array([[1,1],[1,-1]])/np.sqrt(2)
S=[np.kron(Z,Z),np.kron(X,X)]
Pi=[(I4+(-1)**(s&1)*S[0])@(I4+(-1)**((s>>1)&1)*S[1])/4 for s in range(4)]
def one(a,q,U):
 b=np.zeros_like(a)
 for n in range(len(a)):
  for v in range(2):b[(n&~(1<<q))|(v<<q)]+=U[v,(n>>q)&1]*a[n]
 return b
def controlled(a,c,t,P):
 b=np.zeros_like(a)
 for n in range(len(a)):
  if not (n>>c)&1:b[n]+=a[n]
  else:
   for v in range(2):b[(n&~(1<<t))|(v<<t)]+=P[v,(n>>t)&1]*a[n]
 return b
def block(f):
 out=np.zeros((16,16),complex)
 for w in range(4):out[4*w:4*w+4,4*w:4*w+4]=sum(f(w,s)*Pi[s] for s in range(4))
 return out
def sqrtmat(a,inverse=False):
 d,u=eigh(a);return (u*(d**(-.5 if inverse else .5)))@u.conj().T
rateexp=.17;Rt=3.;RA=12.;cases=0;comm=0.;minDelta=1.;maxZero=0.;minHeal=1.;maxComplete=0.
for mask in range(4):
 U=np.eye(16,dtype=complex)
 for j,P in enumerate([Z,X]):
  U=one(U,2+j,H) if mask&1 else np.eye(16,dtype=complex)
  for r in [0,1]:U=controlled(U,2+j,r,P) if (mask>>r)&1 else np.eye(16,dtype=complex)
  U=one(U,2+j,H) if mask&1 else np.eye(16,dtype=complex)
 for old in [None,0,1,2,3]:
  for other in range(4):
   for sb in range(4):
    B=block(lambda w,sa:float(mask!=3 or w!=0))
    qin=block(lambda w,sa:float(mask!=3 or w!=0 or (old is not None and old!=sa) or other!=sa))
    qout=block(lambda y,sa:float(y!=sa or other!=sa))
    Vin=block(lambda w,sa:np.exp(rateexp*((sa^sb).bit_count()+Rt*((old is not None and old!=sa)+(other!=sa))+RA*(mask!=3 or w!=0))))
    Vout=block(lambda y,sa:np.exp(rateexp*((sa^sb).bit_count()+Rt*((y!=sa)+(other!=sa)))))
    rinv=sqrtmat(Vin,True);rout=sqrtmat(Vout)
    # Completely resolved pointer output; distinct Kraus branches, no coherent erasure.
    js=[]
    for y in range(4):
     K=np.zeros((16,16),complex);K[4*y:4*y+4,:]=U[4*y:4*y+4,:]
     js.append(rout@K@rinv)
    Gamma=sum(J.conj().T@J for J in js);Delta=np.eye(16)-Gamma
    comm=max(comm,float(np.linalg.norm(Delta@qin-qin@Delta)),float(np.linalg.norm(Delta@B-B@Delta)))
    minDelta=min(minDelta,float(eigvalsh(Delta)[0]))
    gain=sum(J.conj().T@qout@J for J in js)
    # Conservative tilted loss is Gamma, NOT the original identity loss.
    Lq=gain-(Gamma@qin+qin@Gamma)/2
    minHeal=min(minHeal,float(eigvalsh(-Lq)[0]))
    maxZero=max(maxZero,float(np.linalg.norm(Lq@(np.eye(16)-qin))))
    maxComplete=max(maxComplete,float(np.linalg.norm(Gamma+Delta-np.eye(16))))
    cases+=1
assert comm<1e-10 and minDelta>-1e-10 and minHeal>-1e-10 and maxZero<1e-10
out={'actual_Alice_terminal_cases':cases,'all_workspace_inputs_retained':True,'all_ownership_masks_retained':True,'maximum_killing_B_or_Q_commutator':comm,'minimum_killing_eigenvalue':minDelta,'minimum_conservative_Q_healing_eigenvalue':minHeal,'maximum_conservative_Q_zero_corner_error':maxZero,'maximum_gain_plus_killing_completion_error':maxComplete,'all_checks_pass':True,'scope':'one-step actual terminal commutants and analytic conservative tilt; no whole-FSM useful service or logical threshold'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
