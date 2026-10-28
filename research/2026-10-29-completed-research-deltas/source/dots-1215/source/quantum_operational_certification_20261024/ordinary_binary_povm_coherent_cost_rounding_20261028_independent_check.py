from pathlib import Path
from fractions import Fraction as F
import numpy as np,json,hashlib,math
import sympy as s
rng=np.random.default_rng(202610281154)
root=Path(__file__).parent
ct={'exact_completion_cases':0,'noncommuting_cost_and_offset_cases':0,'exact_probability_cases':0,'precision_cases':0}
for a,b in [(1,1),(1,2),(2,1),(2,2),(2,3),(3,2)]:
 for j in range(8):
  Z=s.Matrix(a,b,lambda i,j:s.Integer(int(rng.integers(-3,4)))+s.I*int(rng.integers(-3,4)))
  denom=4*(1+sum(abs(int(s.re(z)))+abs(int(s.im(z))) for z in Z))
  B=Z/denom;X=B*B.conjugate().T;Y=B.conjugate().T*B
  E=s.BlockMatrix([[s.eye(a)-2*X,B],[B.conjugate().T,2*Y]]).as_explicit()
  expected=s.diag(X-4*X*X,Y-4*Y*Y)
  assert s.simplify(E-E*E-expected)==s.zeros(a+b)
  ct['exact_completion_cases']+=1
  En=np.array(E,complex);Bn=np.array(B,complex)
  assert np.linalg.eigvalsh(En).min()>-1e-12 and np.linalg.eigvalsh(En).max()<1+1e-12
  Zm=rng.normal(size=(a,a))+1j*rng.normal(size=(a,a));Zm=Zm@Zm.conj().T
  Zp=rng.normal(size=(b,b))+1j*rng.normal(size=(b,b));Zp=Zp@Zp.conj().T
  m=2.**(-j*10);q=np.trace(Zm@(Bn@Bn.conj().T)).real+np.trace(Zp@(Bn.conj().T@Bn)).real
  cost=m+np.trace(Zm@(np.eye(a)-En[:a,:a])).real+np.trace(Zp@En[a:,a:]).real
  assert abs(cost-m-2*q)<1e-10
  L=rng.normal(size=(5,(a+b)**2));c=rng.normal(size=5)
  Em=En.copy();Em[:a,a:]*=-1;Em[a:,:a]*=-1
  C=np.zeros_like(En);C[:a,a:]=Bn;C[a:,:a]=Bn.conj().T
  # Real parts suffice as a legitimate real-linear numerator fixture.
  np_=np.linalg.norm(c+L@En.real.reshape(-1))**2;nm=np.linalg.norm(c+L@Em.real.reshape(-1))**2
  nc=np.linalg.norm(L@C.real.reshape(-1))**2
  assert max(np_,nm)>=nc-1e-10
  ct['noncommuting_cost_and_offset_cases']+=1
for d in range(2,102):
 R=2*math.ceil(math.sqrt(math.ceil(math.log2(48*d))))
 assert d*math.exp(-R*R/2)<=1/48
 assert F(1,12)-F(1,48)-F(1,48)==F(1,24)
 assert F(1,24)-F(1,96)==F(1,32)
 assert 32*R*R+2<=64*R*R
 ct['exact_probability_cases']+=1
for e in range(-50,51):
 S=F(2)**e;m=F(2)**(-e);Hb=F(2)**max(e,0)+1;Kb=F(2)**max(-e,0)+1
 delta=min(F(1,8),S/(16*(1+S)*Hb),m/(16*(1+m)*Kb))
 assert delta*delta*Hb<=S/16 and delta*delta*Kb<=m/16
 ct['precision_cases']+=1
p='ordinary_binary_povm_coherent_cost_rounding_20261028.md'
o={'status':'PASS_INDEPENDENT_SCOPED_COHERENT_ROUNDING','source_sha256':hashlib.sha256((root/p).read_bytes()).hexdigest(),'counts':ct,'scope':'Exact completion/constant checks and noncommuting finite fixtures; no production SDP or finite Gaussian implementation, no diagonal branch or CPTP transfer.'}
(root/'ordinary_binary_povm_coherent_cost_rounding_20261028_independent_check.json').write_text(json.dumps(o,indent=2)+'\n');print(json.dumps(o,indent=2))
