"""Independent finite matrix diagnostics and exact teleportation identity tests."""
import numpy as np,json
from pathlib import Path
from fractions import Fraction as F
import sympy as S
rng=np.random.default_rng(291112)
def adj(x):return x.conj().T
def unitary(n):
 z=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));q,r=np.linalg.qr(z);return q@np.diag(np.diag(r)/abs(np.diag(r))).conj()
def choi(kraus):return sum(np.outer(k.reshape(-1,order='F'),k.reshape(-1,order='F').conj()) for k in kraus)/kraus[0].shape[1]
def noise(U,eta):
 d=len(U);ks=[np.sqrt(1-eta)*U]
 for i in range(d):
  for j in range(d):
   k=np.zeros((d,d),complex);k[i,j]=np.sqrt(eta/d);ks.append(k)
 return ks
def td(a,b):return np.linalg.svd(a-b,compute_uv=False).sum()/2
# Same-support programs through a fixed physical CP processor on program and data.
program_checks=0;min_order=1.;maxsupport=0.
for trial in range(24):
 rs=[]
 for _ in range(2):
  z=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2));x=z@adj(z)+np.eye(2)/5;x/=np.trace(x);r=np.zeros((3,3),complex);r[:2,:2]=x;rs.append(r)
 rb=rs[1][:2,:2];v,e=np.linalg.eigh(rb);ib=e@np.diag(v**-.5)@adj(e);eig=np.linalg.eigvalsh(ib@rs[0][:2,:2]@ib);lo,hi=eig[0],eig[-1]
 ks=[rng.normal(size=(2,6))+1j*rng.normal(size=(2,6)) for _ in range(3)];norm=np.linalg.eigvalsh(sum(adj(k)@k for k in ks))[-1];ks=[k/np.sqrt(norm*1.1) for k in ks]
 js=[]
 for rho in rs:
  j=np.zeros((4,4),complex)
  for a in range(2):
   for b in range(2):
    x=np.zeros((2,2));x[a,b]=1;out=sum(k@np.kron(rho,x)@adj(k) for k in ks);j+=np.kron(x,out)/2
  js.append(j)
 margin=min(np.linalg.eigvalsh(js[0]-lo*js[1])[0],np.linalg.eigvalsh(hi*js[1]-js[0])[0]);assert margin>-1e-11;min_order=min(min_order,margin);program_checks+=1
# Two-query adaptive instrument, protected coherent memory and actual intermediate outcomes.
adaptive_checks=0;minadaptive=1.;floor_checks=0
I=np.eye(2);embed=np.kron(I,np.array([[1],[0]]));traceks=[np.kron(I,np.eye(2)[i:i+1]) for i in range(2)]
for trial in range(12):
 U,V=unitary(2),unitary(2);eta=.07+.07*trial;r=eta/(4*(1-eta)+eta);c=r*r
 first=unitary(4);feedback=[unitary(4),unitary(4)];filt=unitary(4)@np.diag([.3,.5,.7,.9]);measure=[np.diag([.8,.8,.6,.6]),np.diag([.6,.6,.8,.8])]
 js=[]
 for Q in [U,V]:
  nk=noise(Q,eta);outks=[]
  for k1 in nk:
   for outcome in range(2):
    for k2 in nk:
     mid=filt@np.kron(k2,I)@feedback[outcome]@measure[outcome]@first@np.kron(k1,I)@embed
     outks.extend(t@mid for t in traceks)
  js.append(choi(outks))
 for a,b in [(0,1),(1,0)]:
  margin=np.linalg.eigvalsh(js[a]-c*js[b])[0];assert margin>-1e-11;minadaptive=min(minadaptive,margin);adaptive_checks+=1
 pa,pb=np.trace(js[0]).real,np.trace(js[1]).real;PU,PV=choi([U]),choi([V]);ea,eb=td(js[0]/pa,PU),td(js[1]/pb,PV);s=np.trace(PU@PV).real
 assert ea+1e-10>=c*pb/pa*max(0,1-s-eb);floor_checks+=1
# Exact Choi-resource postselected teleportation on ALL matrix units.
tele_checks=0
for d in [2,3]:
 U=S.Matrix([[S.Rational(3,5),-S.Rational(4,5)],[S.Rational(4,5),S.Rational(3,5)]]) if d==2 else S.Matrix([[0,1,0],[0,0,1],[1,0,0]])
 phi=S.zeros(d*d,1)
 for i in range(d):phi[i*d+i]=1/S.sqrt(d)
 PU=S.kronecker_product(S.eye(d),U)*phi;PU=PU*PU.T
 W=S.zeros(d,d**3)
 for i in range(d):
  for b in range(d):W[b,(i*d+i)*d+b]=1/S.sqrt(d)
 for eta in [S.Rational(1,7),S.Rational(1,2),S.Rational(1)]:
  resource=(1-eta)*PU+eta*S.eye(d*d)/(d*d)
  for a in range(d):
   for b in range(d):
    x=S.zeros(d);x[a,b]=1;actual=W*S.kronecker_product(x,resource)*W.T;expected=((1-eta)*U*x*U.T+eta*S.trace(x)*S.eye(d)/d)/(d*d)
    assert actual==expected;tele_checks+=1
out=dict(same_support_processor_checks=program_checks,min_program_CP_order_margin=float(min_order),adaptive_two_query_CP_order_checks=adaptive_checks,min_adaptive_margin=float(minadaptive),accepted_Choi_error_floor_checks=floor_checks,exact_teleportation_matrix_unit_checks=tele_checks,scope='Finite matrix diagnostics plus exact rational teleportation identity. General no-go/finite-stopping claims rely on separately reviewed proof, not finite simulations.')
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
