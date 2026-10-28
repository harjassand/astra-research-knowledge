"""Exact finite-MUB + physical-family tests; numerical perturbation tests labeled separately."""
import sympy as S
import numpy as np
import json, pathlib
I=S.eye(2); X=S.Matrix([[0,1],[1,0]]); Y=S.Matrix([[0,-S.I],[S.I,0]]); Z=S.diag(1,-1)
kron=S.kronecker_product
def adj(A):return A.conjugate().T
def simp(A):return A.applyfunc(S.simplify)
def eq(A,B):return all(S.simplify(x)==0 for x in A-B)
def outer(v):return v*adj(v)
def normvec(v):return v/S.sqrt((adj(v)*v)[0])
classes=[(kron(Z,I),kron(I,Z)),(kron(X,I),kron(I,X)),(kron(Y,I),kron(I,Y)),(kron(X,Z),kron(Z,Y)),(kron(X,Y),kron(Y,Z))]
bases=[]
for A,B in classes:
 assert A*B==B*A
 cols=[]
 for val,mult,vs in (A+2*B).eigenvects():
  assert mult==1
  cols.append(normvec(vs[0]))
 Q=S.Matrix.hstack(*cols)
 assert eq(adj(Q)*Q,S.eye(4))
 bases.append(Q)
for i in range(5):
 for j in range(i):
  M=adj(bases[i])*bases[j]
  assert all(S.simplify(x*S.conjugate(x))==S.Rational(1,4) for x in M)
# Exact rational unknown orientation, including complex phases.
U=S.eye(4)
for a,b,c,s in [(0,2,S.Rational(3,5),S.Rational(4,5)),(1,3,S.Rational(5,13),S.Rational(12,13)),(0,1,S.Rational(8,17),S.Rational(15,17))]:
 G=S.eye(4);G[a,a]=G[b,b]=c;G[a,b]=-s;G[b,a]=s;U=G*U
U=S.diag(1,S.I,(3+4*S.I)/5,1)*U
assert eq(adj(U)*U,S.eye(4))
V=U[:,:2];F=U[:,2:]
probes=[outer(S.Matrix([1,1]))/2,outer(S.Matrix([1,-1]))/2,outer(S.Matrix([1,S.I]))/2,outer(S.Matrix([1,-S.I]))/2]
weights=[1,-1,S.I,-S.I]
fixtures=[]
for s,lam in [(S.Rational(3,5),S.Integer(1)),(S.Rational(4,5),S.Rational(1,3))]:
 tau=F*S.diag(lam,1-lam)*adj(F);p=1-s*s
 def native(rho):return V*S.diag(1,s)*rho*S.diag(1,s)*adj(V)+p*rho[1,1]*tau
 C=s*V[:,0]*adj(V[:,1]);mean=S.zeros(4);second=S.zeros(4)
 rhoavg=sum((native(rho) for rho in probes),S.zeros(4))/4
 for rho,w in zip(probes,weights):
  out=native(rho)
  assert S.simplify(S.trace(out))==1
  EY=S.zeros(4);EY2=S.zeros(4)
  for Q in bases:
   for j in range(4):
    psi=Q[:,j];P=outer(psi);prob=S.simplify((adj(psi)*out*psi)[0]/5)
    snap=5*P-S.eye(4)
    EY+=prob*snap;EY2+=prob*snap*snap
  assert eq(EY,out)
  assert eq(EY2,3*out+4*S.eye(4))
  mean+=w*EY/2;second+=EY2
 assert eq(mean,C)
 assert eq(second,4*(3*rhoavg+4*S.eye(4)))
 # Complete physical receiver; complement flags reset to logical |1>.
 R=[adj(V)]+[S.Matrix([0,1])*adj(F[:,j]) for j in range(2)]
 assert eq(sum((adj(r)*r for r in R),S.zeros(4)),S.eye(4))
 E=[V*S.diag(1,s)]+[S.sqrt(p*a)*F[:,j]*S.Matrix([[0,1]]) for j,a in enumerate([lam,1-lam]) if a!=0]
 assert eq(sum((adj(e)*e for e in E),S.zeros(2)),S.eye(2))
 Fe=S.simplify(sum(abs(S.trace(r*e))**2 for r in R for e in E)/4)
 assert Fe==(1+s)/2
 for a in range(2):
  for b in range(2):
   rho=S.zeros(2);rho[a,b]=1
   got=sum((r*native(rho)*adj(r) for r in R),S.zeros(2))
   want=rho.copy()
   if a!=b:want*=s
   assert eq(got,want)
 fixtures.append({'s':str(s),'flag_rank':1 if lam==1 else 2,'Fe':str(Fe),'exact_estimator_moments':'passed','full_receiver_TP_and_action':'passed'})
# Numerical adversarial perturbations, complex phases and nonorthogonal acquired vectors.
rng=np.random.default_rng(20261028)
VV=np.array(V.evalf(),dtype=complex)
ratios=[]
for trial in range(200):
 s=float(rng.uniform(.1,1));C=s*np.outer(VV[:,0],VV[:,1].conj())
 E=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));E*=s*float(rng.uniform(.001,.15))/np.linalg.norm(E,2)
 eta=np.linalg.norm(E,2);Chat=C+E
 left,sv,right=np.linalg.svd(Chat);a=sv[0]
 if a<=4*eta:continue
 W=np.column_stack([left[:,0],right.conj().T[:,0]])
 aa,ss,bb=np.linalg.svd(W,full_matrices=False);Vhat=aa@bb
 phase=np.vdot(VV,W);phase/=abs(phase)
 raw=np.linalg.norm(W-VV*phase,'fro');err=np.linalg.norm(Vhat-VV*phase,2)
 assert raw<=2*eta/a+1e-12
 assert err<=4*eta/a+1e-12
 ratios.append(err/(4*eta/a))
# Conservative confidence radius solves the stated matrix-Freedman exponent.
confidence=[]
for d in [4,16,256]:
 T=100000;delta=.01;v=4*(2*d-1);R=2*d+1;l=np.log(2*d/delta)
 eta=(np.sqrt(2*T*v*l)+2*R*l/3)/T
 exponent=(T*eta)**2/(2*(T*v+R*T*eta/3))
 assert exponent>=l
 confidence.append({'d':d,'T':T,'delta':delta,'eta':eta})
out={'status':'author exact algebra plus numerical stress tests; not independent review','finite_design':'five explicit d=4 Pauli MUBs, exact mutual-unbiased and snapshot moment identities','fixtures':fixtures,'numerical_guarded_trials':len(ratios),'max_isometry_error_to_certified_bound_ratio':max(ratios),'confidence_examples':confidence}
p=pathlib.Path(__file__).with_suffix('.json');p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
