"""Independent deterministic exact checks, no source samples or production solver.
A nonorthogonal rational whitening is constructed by LDL and integer square roots.
"""
from pathlib import Path
from math import isqrt
import sympy as S
import hashlib,json
P=Path(__file__).resolve().parent
SRC='ordinary_prequential_small_loss_decoder_bandit_20261028.md'
PIN='6edb6a3af1118947c1a864113a24d77eef437386eafb7d8694a4aa651dc8d1dc'
assert hashlib.sha256((P/SRC).read_bytes()).hexdigest()==PIN
q=S.Rational; ii=S.I
pauli=[S.eye(2),S.Matrix([[0,1],[1,0]]),S.Matrix([[0,-ii],[ii,0]]),S.diag(1,-1)]
kron=S.kronecker_product
basis=[kron(pauli[j],W) for j in [1,2,3] for W in pauli]
d=2;k=4;D=12
C=S.eye(4)/4+kron(pauli[3],pauli[3])/64+kron(pauli[2],pauli[1])/128
Cinv=C.inv()
H=S.Matrix(D,D,lambda a,b:S.simplify(S.trace(Cinv*basis[a]*Cinv*basis[b])))
assert H==H.T and all(x.is_Rational for x in H)
def positive_definite(A):
 try:
  _,dd=A.LDLdecomposition(hermitian=True)
  return all(dd[n,n]>0 for n in range(A.rows))
 except (ValueError,ZeroDivisionError): return False
assert positive_definite(C) and positive_definite(H)
L,dd=H.LDLdecomposition(hermitian=False)
B=64; scale=2**B
invsqrt=[]
for n in range(D):
 a=dd[n,n]
 invsqrt.append(q(isqrt((scale*scale*int(a.q))//int(a.p)),scale))
Vraw=q(3,4)*L.T.inv()*S.diag(*invsqrt)
# Round the real rational entries to a fixed dyadic entry mesh.
V=Vraw.applyfunc(lambda x:q((int(x.p)*scale)//int(x.q),scale))
A=S.simplify(V.T*H*V)
assert positive_definite(A-S.eye(D)/2) and positive_definite(S.eye(D)-A)
assert V.T*H*V!=S.diag(*[A[i,i] for i in range(D)]) # genuinely nonorthogonal finite frame
Udual=V.T.inv(); Hinv=H.inv()
metric=S.simplify(Udual.T*Hinv*Udual)
assert metric==A.inv()
assert all(metric[i,i]<=2 for i in range(D))
# Coherent retained-memory source, complete unitary before actual decoding/return measurement.
swap=S.Matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
U=q(3,5)*S.eye(4)+ii*q(4,5)*swap
mem0=S.Matrix([[q(3,5),q(1,5)+ii*q(1,10)],[q(1,5)-ii*q(1,10),q(2,5)]])
def ptr_second(r,da=2,db=2):
 return S.Matrix(da,da,lambda a,b:S.simplify(sum(r[a*db+j,b*db+j] for j in range(db))))
def ptr_first(r,da=2,db=2):
 return S.Matrix(db,db,lambda a,b:S.simplify(sum(r[j*db+a,j*db+b] for j in range(da))))
def source(r,m): return ptr_second(U*kron(r,m)*U.H)
# One actual exploratory-decoder return-mismatch instrument gives a new memory.
prior=U*kron((pauli[0]+pauli[1])/2,mem0)*U.H
prefixplay=C+sum((V[a,0]*basis[a] for a in range(D)),S.zeros(4))/2
mismatch_projector=(pauli[0]-pauli[1])/2
return_effect=2*ptr_first(kron(mismatch_projector,pauli[0])*prefixplay).T
assert positive_definite(return_effect) and positive_definite(pauli[0]-return_effect)
mem1=ptr_first(kron(return_effect,pauli[0])*prior)
mem1=S.simplify(mem1/S.trace(mem1))
assert mem0*mem1!=mem1*mem0
memos=[mem0,mem1]
def decode(C,r):
 return S.Matrix(2,2,lambda o,p:S.simplify(2*sum(C[2*o+a,2*p+b]*r[a,b] for a in range(2) for b in range(2))))
probability_laws=0; reports=[]
for mem in memos:
 states={(j,s):source((pauli[0]+s*pauli[j])/2,mem) for j in [1,2,3] for s in [-1,1]}
 effect=sum((kron((pauli[0]-s*pauli[j])/2,states[j,s].T)/6 for j,s in states),S.zeros(4))
 ell=S.Matrix([S.simplify(2*S.trace(E*effect)) for E in basis])
 mean_loss=S.simplify(2*S.trace(C*effect))
 gmean=S.zeros(D,1); variance=0; playedmean=0
 for i in range(D):
  direction=sum((V[a,i]*basis[a] for a in range(D)),S.zeros(4))
  for z in [-1,1]:
   play=C+z*direction/2
   assert positive_definite(play-C/2)
   # Exact TP: trace over first/output system.
   assert ptr_first(play)==S.eye(2)/2
   p=0
   for j,s in states:
    decoded=decode(play,states[j,s])
    mismatch=S.simplify(S.trace((pauli[0]-s*pauli[j])*decoded)/2)
    assert mismatch.is_Rational and 0<=mismatch<=1
    assert S.trace(decoded)==1
    p+=mismatch/6; probability_laws+=1
   p=S.simplify(p)
   assert p==S.simplify(2*S.trace(play*effect))
   playedmean+=p/(2*D)
   g=2*D*z*Udual[:,i]
   gmean+=p*g/(2*D)
   variance+=p*(g.T*Hinv*g)[0]/(2*D)
 assert S.simplify(gmean-ell)==S.zeros(D,1)
 assert S.simplify(playedmean-mean_loss)==0
 variance=S.simplify(variance)
 assert variance<=8*D*D*mean_loss
 reports.append({'mean_loss':str(mean_loss),'variance_over_mean_loss':str(S.simplify(variance/mean_loss)),'variance_bound_over_mean_loss':8*D*D})
# Nonzero ACTUAL-gradient commuting prox, solved solely by exact rational bisection.
# C0, H0=64I, V0=I/10 obey 1/2 I <= V0^T H0 V0 <= I.
C0=S.eye(4)/4; H0=64*S.eye(D); V0=S.eye(D)/10
assert V0.T*H0*V0==q(16,25)*S.eye(D)
eta=q(1,64*D*D); epsilon=q(1,4); delta=eta*epsilon/64
prox=[]
for z in [-1,1]:
 g=2*D*z*10 # y=1 and exact dual vector, one Pauli coordinate
 beta=eta*g
 f=lambda x:beta+4*x/(q(1,16)-x*x)
 lo=q(-1,64);hi=q(1,64)
 assert f(lo)<0 and f(hi)>0
 for _ in range(80):
  mid=(lo+hi)/2
  if f(mid)<=0:lo=mid
  else:hi=mid
 x=(lo+hi)/2
 nxt=C0+x*basis[-1]
 grad=S.Matrix([-S.trace(nxt.inv()*E) for E in basis])
 actualg=S.zeros(D,1);actualg[-1]=g
 residual=eta*actualg+grad
 radius=64*x*x
 assert radius<=q(1,4) and (residual.T*residual)[0]<=delta*delta
 assert positive_definite(nxt) and ptr_first(nxt)==S.eye(2)/2
 prox.append({'sign':z,'bisection_iterations':80,'center_coordinate':str(x),'radius_squared':str(radius),'residual_squared':str((residual.T*residual)[0]),'delta_squared':str(delta*delta)})
# Constant checks, including first-order beta coefficient and resource ceiling.
assert q(3,2)*q(8,7)*(q(1,16)+q(1,8)+q(1,64))==q(39,112)
assert 1024*9*2==18432
out={'status':'PASS','source_sha256':PIN,'evidence_kind':'Independent exact rational deterministic matrix/bisection checks; no samples',
'whitening':{'D':D,'dyadic_entry_bits':B,'exact_strict_PSD_interval_certificate':True,'nonorthogonal_frame':True,'exact_inverse_dual':True},
'actual_bit_law_checks':probability_laws,'conditional_memories':2,'memories_noncommuting':True,'second_memory_from_actual_decoder_return_instrument':True,'conditional_unbiasedness_checks':2,'small_loss_variance_checks':reports,
'nonzero_exact_bisection_prox_certificates':prox,'additive_constant':'39/112','source_cap_coefficient':18432,
'source_calls':0,'random_samples':0,'generic_convex_solver_executed':False,'hardware_executions':0,
'limitations':'The exact one-coordinate prox cases test certificates, not a generic ellipsoid implementation or a sampled learning run.'}
print(json.dumps(out,indent=2,sort_keys=True))
