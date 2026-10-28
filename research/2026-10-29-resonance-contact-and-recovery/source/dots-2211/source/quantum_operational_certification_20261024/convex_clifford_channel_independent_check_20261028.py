"""Independent exact Choi/dual algebra; floating rounding illustration, no SDP execution."""
from pathlib import Path
import runpy,sympy as s,json,numpy as np
q=Path(__file__).resolve().parent
v=runpy.run_path(str(q/'noncommuting_variational_inverse_independent_check_20261028.py'))
B,C,coef,tau,P=[v[x] for x in ['B','C','coef','tau','P']];d=4
H=sum((s.kronecker_product(p.T,c) for p,c in zip(P,C)),s.zeros(8))
Y=sum((coef[j][j] for j in range(3)),s.zeros(4));Q=s.kronecker_product(s.eye(2),Y)-H
Ds=[s.kronecker_product(p.T,s.eye(d))-s.kronecker_product(s.eye(2),b) for p,b in zip(P,B)]
Q2=sum((Ds[j]*s.kronecker_product(s.eye(2),coef[j][k])*Ds[k] for j in range(3) for k in range(3)),s.zeros(8))/2
assert Q==Q2
E=[s.zeros(2) for _ in range(4)]
for r in range(2):
 for c in range(2):E[2*r+c][r,c]=1
KB=s.BlockMatrix([[s.kronecker_product(E[2*r+c],s.eye(2)) for c in range(2)] for r in range(2)]).as_explicit()
assert KB[:4,:4]+KB[4:,4:]==s.eye(4)
assert s.trace(H*KB)==sum(s.trace(x*y) for x,y in zip(B,C))==s.trace(Y)
assert Q*KB==s.zeros(8)
L=3*s.eye(8)-sum((s.kronecker_product(p.T,b) for p,b in zip(P,B)),s.zeros(8))
assert L==sum((D*D for D in Ds),s.zeros(8))/2
checks=0;rounding=[]
def sign(M):
 e,U=np.linalg.eigh((M+M.conj().T)/2);return (U*np.sign(e))@U.conj().T,float(np.min(abs(e)))
for m in [3,5,10]:
 c=s.Rational(m*m-1,m*m+1);u=s.Rational(2*m,m*m+1)
 U=s.eye(4);U[0,0]=U[3,3]=c;U[0,3]=u;U[3,0]=-u
 KU=s.kronecker_product(s.eye(2),U)*KB*s.kronecker_product(s.eye(2),U.H)
 for t in [s.Rational(1,10),s.Rational(1,4),s.Rational(1,2)]:
  K=(1-t)*KB+t*KU
  A=[sum((p[r,c]*K[4*r:4*r+4,4*c:4*c+4] for r in range(2) for c in range(2)),s.zeros(4)) for p in P]
  assert K[:4,:4]+K[4:,4:]==s.eye(4)
  assert s.trace(H*K)==sum(s.trace(a*c) for a,c in zip(A,C))
  gap=s.trace(Y)-s.trace(H*K);D2=sum(s.trace((a-b)**2) for a,b in zip(A,B))
  interm=3*d-sum(s.trace(a*b) for a,b in zip(A,B))
  assert gap>=tau*interm>=tau*D2/2
  aa=[np.array(a,dtype=complex) for a in A];bb=[np.array(b,dtype=complex) for b in B]
  X,gx=sign(aa[0]);Zo=(aa[2]-X@aa[2]@X)/2;Z,gz=sign(Zo);YY=1j*X@Z
  epsx=np.linalg.norm(aa[0]-bb[0],2);epsz=np.linalg.norm(aa[2]-bb[2],2)
  assert np.linalg.norm(X-bb[0],2)<=2*epsx+1e-12
  assert np.linalg.norm(Z-bb[2],2)<=2*epsz+4*epsx+1e-12
  assert np.linalg.norm(X@Z+Z@X,2)<1e-12
  assert np.linalg.norm(YY-YY.conj().T,2)<1e-12
  rounding.append({'m':m,'t':str(t),'X_gap':gx,'odd_Z_gap':gz,'X_error':float(np.linalg.norm(X-bb[0],2)),'Z_error':float(np.linalg.norm(Z-bb[2],2))})
  checks+=1
# Exact unital repair at a negative spectral boundary.
for eta in [s.Rational(1,100),s.Rational(1,10),s.Rational(1,2)]:
 Kbad=(1+2*eta)*KB-eta*s.eye(8)
 assert Kbad[:4,:4]+Kbad[4:,4:]==s.eye(4)
 Kfix=(Kbad+eta*s.eye(8))/(1+2*eta)
 assert Kfix==KB
 assert abs(s.trace(H*(Kfix-Kbad)))<=6*d*eta
r={'status':'PASS_INDEPENDENT_EXACT_CHOI_DUAL_CURVATURE','dimension_d':4,'choi_dimension':8,'exact_unital_cp_mixture_fixtures':checks,'Q_dual_factorization_exact':True,'Choi_objective_normalization_exact':True,'rounding_checks_floating':rounding,'exact_unital_repair_fixtures':3,'source_calls':0,'generic_SDP_executions':0,'scope':'Exact known feasible matrices and dual identities; no numerical SDP solution or acquired source data.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='rounding_checks_floating'}))
