"""Independent physical-action covariance and closed-form conditioning checks."""
from pathlib import Path
from fractions import Fraction as F
import math,json,hashlib,numpy as np
root=Path(__file__).resolve().parent
source=root/'ordinary_generic_fast_polynomial_design_baseline_20261028.md'
expected='74e7ff7ee4a02b2b7096602cecc7eec6583aa34e318cebfe66d558b396bb0f84'
assert hashlib.sha256(source.read_bytes()).hexdigest()==expected
rng=np.random.default_rng(28101022)
X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1.,-1.]);paulis=[X,Y,Z]
enc=[np.eye(4)[i] for i in range(4)]
for i in range(4):
 for j in range(i+1,4):enc.append((np.eye(4)[i]+np.eye(4)[j])/math.sqrt(2))
def features(x):return np.array([*(x*x),*(2*x[i]*x[j] for i in range(4) for j in range(i+1,4))])
EA=np.array([features(x) for x in enc]);mine=np.linalg.eigvalsh(EA.T@EA/10).min();assert mine>=1/4000
physical=0;maxlin=0.;maxcov=0.;maxnorm=0.;condition=0
for k in [1,2]:
 hb=[]
 for i in range(k):
  M=np.zeros((k,k),complex);M[i,i]=1;hb.append(M)
 for i in range(k):
  for j in range(i+1,k):
   M=np.zeros((k,k),complex);M[i,j]=M[j,i]=1;hb.append(M)
   M=np.zeros((k,k),complex);M[i,j]=1j;M[j,i]=-1j;hb.append(M)
 fs=[np.kron(H,P) for H in hb for P in paulis];C0=np.eye(2*k)/2
 dec=[C0]+[C0+FF/4 for FF in fs];m=len(dec);D=10*m
 b=np.array([[1]+[float(np.trace(FF@(C-C0)).real/np.trace(FF@FF).real) for FF in fs] for C in dec])
 assert np.linalg.eigvalsh(b.T@b/m).min()>=1/(33*m*m)
 acts=[];means=[]
 def T_of(x):
  if k==1:return np.eye(2)/2
  U=x[0]*np.eye(2)+1j*x[1]*X+1j*x[2]*Y+1j*x[3]*Z
  vv=U.reshape(-1)/math.sqrt(2);J=np.outer(vv,vv.conj());return (np.eye(4)-J)/3
 for x in enc:
  T=T_of(x)
  for bb,C in zip(b,dec):
   acts.append(np.kron(features(x),bb));means.append(np.trace(T@C.T).real)
 A=np.array(acts);q=np.array(means);theta=np.linalg.solve(A,q)
 for _ in range(12):
  x=rng.normal(size=4);x/=np.linalg.norm(x)
  if k==1:
   rr=rng.normal(size=3);rr*=.2/max(1,np.linalg.norm(rr));C=C0+sum(rr[i]*fs[i] for i in range(3))
  else:
   y=rng.normal(size=4);y/=np.linalg.norm(y);U=y[0]*np.eye(2)+1j*y[1]*X+1j*y[2]*Y+1j*y[3]*Z
   vec=U.T.reshape(-1);C=.9*np.outer(vec,vec.conj())+.1*C0
  bb=np.array([1]+[np.trace(FF@(C-C0)).real/np.trace(FF@FF).real for FF in fs]);aa=np.kron(features(x),bb)
  exact=np.trace(T_of(x)@C.T).real;pred=aa@theta
  assert -1e-12<=exact<=1+1e-12;maxlin=max(maxlin,abs(exact-pred));physical+=1
 for tau in [.5,.125,.001]:
  u=2*q+2*tau;pi=np.ones(D)/D;V=A.T@np.diag(pi/u)@A
  lamstar=2**-22/D**2;assert np.linalg.eigvalsh(V).min()>=lamstar
  Vi=np.linalg.inv(V);n=math.ceil(100*D/tau);ni=np.ceil(n*pi)
  middle=A.T@np.diag(pi*pi*q*(1-q)/(u*u*ni))@A
  cov=Vi@middle@Vi
  # Unpivoted SPD LDL, independent of author implementation.
  L=np.eye(D);ds=np.zeros(D)
  for j in range(D):
   ds[j]=V[j,j]-np.dot(L[j,:j]**2,ds[:j])
   for i in range(j+1,D):L[i,j]=(V[i,j]-np.dot(L[i,:j]*L[j,:j],ds[:j]))/ds[j]
  assert np.max(abs(L@np.diag(ds)@L.T-V))<1e-11
  transformed=np.diag(np.sqrt(ds))@L.T@cov@L@np.diag(np.sqrt(ds))*n
  rat=np.linalg.eigvalsh((transformed+transformed.T)/2).max();assert rat<=1+1e-8;maxcov=max(maxcov,float(rat))
  # Deterministic simultaneous error event after coordinate medians.
  ep=4/np.sqrt(n*ds)*rng.uniform(-1,1,size=D);et=np.linalg.solve(L.T,ep)
  norm=math.sqrt(max(0,float(et@V@et)));assert norm<=4*math.sqrt(D/n)+1e-10
  maxnorm=max(maxnorm,norm/(4*math.sqrt(D/n)))
  condition+=1
# Closed conditioning and determinant statements, including D=2 edge case.
condcases=0
for D in [2,3,10,40,130]:
 for rpower in [1,4,16,64]:
  R=2.**rpower;Tmax=math.ceil(D*rpower)+1
  logretain=Tmax*math.log1p(-1/D);loglower=-math.log(4)-4*math.log(R)
  assert logretain>=loglower
  gain=(1-1/D)**D*(1+8*D/(D-1));assert gain>2
  condcases+=1
median_cases=0;maxmed=0.
for D in [2,10,40,130]:
 for J in [1,8,32]:
  beta=F(1,100);bb=math.ceil(8*math.log(float(2*D*J/beta)));bb+=1-bb%2
  failure=sum(F(math.comb(bb,j))*F(1,16)**j*F(15,16)**(bb-j) for j in range((bb+1)//2,bb+1))
  assert failure<=beta/(D*J);maxmed=max(maxmed,float(failure/(beta/(D*J))));median_cases+=1
# Exact envelope/slack constants and final loss budget.
c=1/16;coef=3*c*c+2*c*math.sqrt(32);assert coef<.75
final=1.5*1.25/128+1.5*125/32768;assert final<1/16
out={'status':'PASS_INDEPENDENT_PHYSICAL_COVARIANCE_AND_CONDITIONING','source_sha256':expected,'encoder_anchor_min_eigenvalue':float(mine),'physical_random_decoder_feature_cases':physical,'max_physical_feature_residual':maxlin,'physical_stratified_covariance_cases':condition,'max_whitened_covariance_eigenvalue':maxcov,'max_coordinate_event_norm_ratio':maxnorm,'closed_determinant_lower_bound_cases':condcases,'exact_binomial_median_cases':median_cases,'max_median_failure_over_allocated_budget':maxmed,'affine_envelope_correction_coefficient':coef,'final_comparator_error_coefficient':final,'scope':'Algebra/conditioning checks using physical action features; no full conservative pilot, SDP solver, frame or hardware execution.'}
(root/'ordinary_generic_fast_polynomial_design_baseline_20261028_covariance_check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
