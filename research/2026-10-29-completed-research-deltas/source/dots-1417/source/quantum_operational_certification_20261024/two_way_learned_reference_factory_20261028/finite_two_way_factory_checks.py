from fractions import Fraction as F
from pathlib import Path
from itertools import product
import numpy as np, json,hashlib,math
Q=Path(__file__).parent
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]).astype(complex);Y=1j*X@Z
Ps=[I,X,Z,X@Z]
phi=np.array([1,0,0,1],complex)/np.sqrt(2); Phi=np.outer(phi,phi.conj())
bells=[np.kron(I,P)@phi for P in Ps]
# Teleportation Kraus contraction with a Bell-labelled resource, including every message.
teleport_max=0.
for P,M in product(Ps,repeat=2):
 K=M.T@P@M.conj()/2
 target=P/2
 teleport_max=max(teleport_max,min(np.linalg.norm(K-target),np.linalg.norm(K+target)))
 assert np.allclose(K.conj().T@K,I/4)
assert teleport_max<1e-12
# A finite 12-element bilateral twirl: Pauli dephase then a 3-cycle.
C=(I-1j*(X+Y+Z))/2
assert np.allclose(C.conj().T@C,I)
Us=[np.linalg.matrix_power(C,j)@P for j in range(3) for P in Ps]
rng=np.random.default_rng(2741);twirl_max=0.
for t in range(20):
 A=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));rho=A@A.conj().T;rho/=np.trace(rho)
 out=sum(np.kron(U.conj(),U)@rho@np.kron(U.conj(),U).conj().T for U in Us)/12
 fid=float(np.vdot(phi,rho@phi).real)
 target=fid*Phi+(1-fid)*(np.eye(4)-Phi)/3
 twirl_max=max(twirl_max,np.linalg.norm(out-target))
assert twirl_max<1e-12
# Actual four-qubit bilateral CNOT, ordering A1 B1 A2 B2.
B=np.zeros((16,16),complex)
for a,b,c,d in product(range(2),repeat=4):
 old=8*a+4*b+2*c+d;new=8*a+4*b+2*(c^a)+(d^b);B[new,old]=1
recurrence_cases=0;fine_max=0.
for den in range(2,42):
 f=F(1,2)+F(1,2*den); aa=(1-f)/3; qs=[f,aa,aa,aa]
 probs={0:F(0),1:F(0)};passnum=F(0);idnum=F(0)
 for u,v in product(range(4),repeat=2):
  state=B@np.kron(bells[u],bells[v]);amp=state.reshape(4,4)
  # Label u encodes x=u mod2,z=u//2; same for v.
  x1,z1=u%2,u//2;x2,z2=v%2,v//2
  expected=bells[x1+2*(z1^z2)]
  if x1==x2:
   passnum+=qs[u]*qs[v]
   if x1==0 and z1==z2:idnum+=qs[u]*qs[v]
   for bit,col in [(0,0),(1,3)]:
    vout=amp[:,col]; vv=np.outer(vout,vout.conj())
    fine_max=max(fine_max,np.linalg.norm(vv-np.outer(expected,expected.conj())/2))
    probs[bit]+=qs[u]*qs[v]/2
  else:
   assert np.linalg.norm(amp[:,0])+np.linalg.norm(amp[:,3])<1e-12
 p=(8*f*f-4*f+5)/9;rr=(10*f*f-2*f+1)/(8*f*f-4*f+5)
 assert passnum==p and idnum/passnum==rr and probs[0]==probs[1]==p/2
 recurrence_cases+=1
assert fine_max<1e-12
# Exact monotonicity and growth-point checks; manuscript supplies polynomial interval proof.
growth_cases=0
for a in range(0,251):
 t=F(a,1000)
 rr_gap=6*t*(1+t)/(5+4*t+8*t*t)
 assert rr_gap>=F(9,8)*t
 f=F(1,2)+t
 assert -4*f*f+14*f-1>0
 growth_cases+=1
f=F(3,4)
for _ in range(9):f=(10*f*f-2*f+1)/(8*f*f-4*f+5)
assert f>F(39,40)
# All deterministic cap arithmetic is exact. No enormous raw bank is generated.
cap_cases=0
for gap in [F(1,4),F(1,8),F(1,16),F(1,32),F(1,64)]:
 k1=0;y=gap
 while y<F(1,4):y*=F(9,8);k1+=1
 K=k1+9
 for q in [1,3,10,100]:
  for dc in [F(1,10),F(1,1000)]:
   L=0
   while F(q,5)*F(1,4)**(2**L)>dc:L+=1
   b=q*5**L;tc=100;ns=b
   for j in range(K):ns=8*(ns+tc)
   formula=8**K*b+8*tc*(8**K-1)//7
   assert ns==formula
   assert F(q,5)*F(1,4)**(2**L)<=dc
   cap_cases+=1
out={'status':'PASS_AUTHOR_FINITE_TWO_WAY_FACTORY_CHECKS','teleport_message_label_cases':16,'twirl_random_density_cases':20,'recurrence_exact_parameter_cases':recurrence_cases,'exact_growth_grid_cases':growth_cases,'exact_cap_cases':cap_cases,'max_teleport_kraus_residual':teleport_max,'max_twirl_residual':twirl_max,'max_fine_recurrence_branch_residual':fine_max,'R9_three_quarters':float(f),'source_sha256':hashlib.sha256((Q/'FINITE_TWO_WAY_LEARNED_REFERENCE_FACTORY.md').read_bytes()).hexdigest(),'scope':'Exact scalar/Pauli-label/cap checks and small actual twirl/recurrence/teleportation matrices. No quantum-source samples, warm SDP, large concatenated circuit or hardware run. General tail/history proofs are in source.'}
(Q/'finite_two_way_factory_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
