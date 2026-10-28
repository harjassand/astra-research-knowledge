#!/usr/bin/env python3
"""Exact nonunital/noncommuting-gauge native oracle identity. Zero source outcomes."""
from pathlib import Path
import sympy as s,json,hashlib,itertools
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);P=[X,Y,Z]
kron=s.kronecker_product
p0=s.diag(1,0);pp=s.ones(2)/2;u=s.Matrix([s.Rational(3,5),0,s.Rational(4,5)])
T0=s.diag(s.Rational(4,5),s.Rational(4,5),s.Rational(16,25));T1=s.Rational(4,5)*s.eye(3)-s.Rational(4,25)*u*u.T
rho0=(I+s.Rational(9,25)*Z)/2;rho1=(I+s.Rational(9,25)*sum((u[j]*P[j] for j in range(3)),s.zeros(2)))/2
rho=(kron(rho0,p0)+kron(rho1,pp))/2
B=[kron(p,I) for p in P];coef=[[kron(I,(T0[k,j]*p0+T1[k,j]*pp)/4) for j in range(3)] for k in range(3)]
C=[sum((B[k]*coef[k][j] for k in range(3)),s.zeros(4)) for j in range(3)]
assert any(coef[j][k]*coef[a][b]!=coef[a][b]*coef[j][k] for j,k,a,b in itertools.product(range(3),repeat=4))

def clean(M):return M.applyfunc(s.simplify)
def channel(M):return clean(s.trace(M)*rho+sum((s.trace(P[j]*M)*C[j] for j in range(3)),s.zeros(4)))
def partialg(M):return s.Matrix(2,2,lambda a,b:sum(M[2*a+g,2*b+g] for g in range(2)))
def bellscore(dec):
 val=0
 for a,b in itertools.product(range(2),repeat=2):
  e=s.zeros(2);e[a,b]=1;val+=dec(channel(e))[a,b]/4
 return s.simplify(val)
def adjoint_from_decoder(dec):
 A=[]
 for p in P:
  a=s.zeros(4)
  for i,j in itertools.product(range(4),repeat=2):
   e=s.zeros(4);e[i,j]=1;a[j,i]=s.trace(p*dec(e))
  A.append(clean(a))
 return A
Ydual=sum((coef[j][j] for j in range(3)),s.zeros(4));H=sum((kron(P[j].T,C[j]) for j in range(3)),s.zeros(8))
D=[kron(P[j].T,s.eye(4))-kron(I,B[j]) for j in range(3)]
Q=clean(kron(I,Ydual)-H)
sos=clean(sum((D[j]*kron(I,coef[j][k])*D[k]/2 for j,k in itertools.product(range(3),repeat=2)),s.zeros(8)))
assert Q==sos
Kstar=(s.eye(8)+sum((kron(P[j].T,B[j]) for j in range(3)),s.zeros(8)))/2
assert Q*Kstar==s.zeros(8)
opt=s.simplify((1+s.trace(Ydual))/4);assert opt==s.Rational(81,100);assert bellscore(partialg)==opt
# Exact physical source realization: two AD channels with different unknown axes and noncommuting gauges.
U=s.Matrix([[3,-1],[1,3]])/s.sqrt(10)
AD=[s.diag(1,s.Rational(4,5)),s.Matrix([[0,s.Rational(3,5)],[0,0]])]
ks=[kron(k,s.Matrix([1,0]))/s.sqrt(2) for k in AD]+[kron(U*k*U.H,s.Matrix([1,1])/s.sqrt(2))/s.sqrt(2) for k in AD]
assert clean(sum((k.H*k for k in ks),s.zeros(2)))==I
entries=0
for a,b in itertools.product(range(2),repeat=2):
 e=s.zeros(2);e[a,b]=1
 assert clean(sum((k*e*k.H for k in ks),s.zeros(4)))==channel(e);entries+=16
rows=[]
# Known physical competing decoders, including nonunital outputs and mixtures.
for m in [2,3,5,10]:
 c=s.Rational(m*m-1,m*m+1);r=s.Rational(2*m,m*m+1)
 W=s.eye(4);W[0,0]=W[3,3]=c;W[0,3]=r;W[3,0]=-r
 assert W.H*W==s.eye(4)
 base=lambda M:partialg(W*M*W.H)
 for kind in ['unitary_subsystem','post_damping','replacement_mixture']:
  if kind=='unitary_subsystem':dec=base
  elif kind=='post_damping':dec=lambda M:sum((k*base(M)*k.H for k in AD),s.zeros(2))
  else:dec=lambda M:s.Rational(2,3)*base(M)+s.trace(M)*p0/3
  A=adjoint_from_decoder(dec)
  direct=bellscore(dec);formula=s.simplify((1+sum(s.trace(A[j]*C[j]) for j in range(3)))/4)
  assert direct==formula and direct<=opt
  rows.append({'decoder':kind,'rational_rotation_parameter':m,'native_Bell_fidelity':str(direct),'oracle_fidelity':str(opt)})
# Completely forgetting source boundary: T=0, no acquisition information, optimal Fe=1/4.
forget=lambda M:s.trace(M)*rho
for outstate in [p0,pp,I/2]:
 val=0
 for a,b in itertools.product(range(2),repeat=2):
  e=s.zeros(2);e[a,b]=1;rr=s.trace(forget(e))*outstate;val+=rr[a,b]/4
 assert val==s.Rational(1,4)
out={'status':'PASS_EXACT_SINGLE_LOGICAL_NATIVE_ORACLE_COROLLARY','source_outcomes':0,'actual_nonunital_source_Kraus_entries_checked':entries,'coefficient_blocks_noncommuting':True,'exact_dual_sum_of_squares_identity':True,'exact_dual_complementarity':True,'full_CPTP_oracle_Bell_fidelity':'81/100','physical_competing_decoders':rows,'forgetting_boundary_fidelity':'1/4','scope':'Exact source-disabled native-channel and convex-dual identities; not sampled acquisition, hardware or collective multi-logical optimality','sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(__file__).with_suffix('.md')]}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
