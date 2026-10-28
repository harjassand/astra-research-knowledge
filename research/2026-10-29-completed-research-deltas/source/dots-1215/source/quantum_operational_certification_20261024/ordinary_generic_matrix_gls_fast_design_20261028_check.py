"""Author proof diagnostics, not execution of the imported quantum query or full cap."""
from pathlib import Path
import hashlib,json,math
from fractions import Fraction
import numpy as np
from scipy.linalg import eigvalsh
ROOT=Path(__file__).parent
rng=np.random.default_rng(202610281145)

def h(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def basis(d):
 out=[]
 for i in range(d):
  a=np.zeros((d,d),complex);a[i,i]=1;out.append(a)
 for i in range(d):
  for j in range(i+1,d):
   a=np.zeros((d,d),complex);a[i,j]=a[j,i]=1/np.sqrt(2);out.append(a)
   a=np.zeros((d,d),complex);a[i,j]=1j/np.sqrt(2);a[j,i]=-1j/np.sqrt(2);out.append(a)
 return np.array(out)
def vec(A,B):return np.einsum('aij,ji->a',B,A).real
def unvec(v,B):return np.einsum('a,aij->ij',v,B)
def K(U,B):
 return np.einsum('aij,bji->ab',B,(U@B+B@U)/2).real

def feat(x):return np.array([*x*x,*[2*x[i]*x[j] for i in range(4) for j in range(i+1,4)]])
anchors=[np.eye(4)[i] for i in range(4)]+[(np.eye(4)[i]+np.eye(4)[j])/np.sqrt(2) for i in range(4) for j in range(i+1,4)]
Aanchor=np.array([feat(x) for x in anchors]);mineig_anchor=float(eigvalsh(Aanchor.T@Aanchor/10)[0]);assert mineig_anchor>=1/4000

def loss_from_kraus(Ks,x):
 V=np.kron(x[:,None],np.eye(2));ops=[a@V for a in Ks];k=ops[0].shape[0]
 J=sum(np.outer(a.reshape(-1),a.reshape(-1).conj()) for a in ops)/2
 rho=sum(a@a.conj().T for a in ops)/2
 T=(2*np.kron(rho,np.eye(2))-J)/3
 assert np.linalg.norm(T-T.conj().T)<1e-10
 assert abs(np.trace(T)-1)<1e-10 and eigvalsh(T)[0]>-1e-10
 return T

def physical_random(k):
 r=5;z=rng.normal(size=(k*r,8))+1j*rng.normal(size=(k*r,8));q,_=np.linalg.qr(z);return [q[j*k:(j+1)*k] for j in range(r)]

def erasure_T(x):
 p=float((x@np.ones(4)/2)**2);k=3
 A0=np.zeros((k,2));A0[:2]=np.eye(2)*np.sqrt(max(0,1-p))
 A1=np.zeros((k,2));A1[2,0]=np.sqrt(p)
 A2=np.zeros((k,2));A2[2,1]=np.sqrt(p)
 ops=[A0,A1,A2];J=sum(np.outer(a.reshape(-1),a.reshape(-1).conj()) for a in ops)/2
 rho=sum(a@a.T for a in ops)/2
 return (2*np.kron(rho,np.eye(2))-J)/3

counts={'physical_quadratic_probes':0,'block_design_updates':0,'block_leverage_tests':0,'covariance_and_bias_cases':0,'envelope_operator_cases':0,'full_CPTP_trace_cases':0,'median_regression_cases':0,'exact_scale_cases':0}
max_res={'quadratic':0.,'covariance_positive_violation':0.,'operator_leverage_positive_violation':0.,'envelope_positive_violation':0.,'risk_positive_violation':0.}
models=[]
for k in [2,3]:
 for _ in range(2):
  Ks=physical_random(k);models.append((k,lambda x,Ks=Ks:loss_from_kraus(Ks,x),'random'))
models.append((3,erasure_T,'erasure_valley'))
for modelno,(k,Tfun,label) in enumerate(models):
 d=2*k;B=basis(d);p=d*d;D=10*p
 X=anchors.copy()
 for _ in range(10):
  x=rng.normal(size=4);X.append(x/np.linalg.norm(x))
 if label=='erasure_valley':X += [(np.eye(4)[0]-np.eye(4)[1])/np.sqrt(2),np.ones(4)/2]
 Fs=[np.kron(feat(x)[:,None],np.eye(p)) for x in X]
 Ts=[Tfun(x) for x in X]
 theta=np.linalg.solve(Aanchor,np.array([vec(T,B) for T in Ts[:10]])).reshape(-1)
 for F,T in zip(Fs,Ts):
  e=np.linalg.norm(F.T@theta-vec(T,B));max_res['quadratic']=max(max_res['quadratic'],float(e));assert e<1e-10;counts['physical_quadratic_probes']+=1
 eta=2**(-18) if label=='erasure_valley' else .03
 Us=[2*T+4*eta*np.eye(d) for T in Ts]
 Ks=[K(U,B) for U in Us];Bxs=[F@np.linalg.solve(ku,F.T) for F,ku in zip(Fs,Ks)]
 weights=np.zeros(len(X));weights[:10]=.1
 V=sum(w*b for w,b in zip(weights,Bxs));assert eigvalsh(V)[0]>2**-20
 iterations=0
 while True:
  Vi=np.linalg.inv(V);lev=np.array([np.trace(Vi@bx).real for bx in Bxs]);ix=int(np.argmax(lev))
  if lev[ix]<=8*D:break
  old_log=np.linalg.slogdet(V)[1];weights*=1-1/D;weights[ix]+=1/D
  V=sum(w*b for w,b in zip(weights,Bxs));gain=np.linalg.slogdet(V)[1]-old_log
  assert gain>math.log(2)-1e-6
  iterations+=1;assert iterations<10000
 counts['block_design_updates']+=iterations
 Vi=np.linalg.inv(V)
 for F,ku in zip(Fs,Ks):
  g=F.T@Vi@F;l=np.trace(np.linalg.solve(ku,g))
  vals=eigvalsh(g,ku);violation=float(vals[-1]-l)
  max_res['operator_leverage_positive_violation']=max(max_res['operator_leverage_positive_violation'],violation)
  assert vals[-1]<=l+1e-5 and l<=8*D+1e-5
  counts['block_leverage_tests']+=1
 # Synthetic analytical covariance, using the imported directional bound only.
 for test in range(3):
  n=50000;r=d;mbar=n+math.ceil(2+r/eta)+1;zeta=min(eta/(10**6*D*n),1/mbar**2)
  S=np.zeros((D,D));bias=np.zeros(D)
  for w,F,T,ku in zip(weights,Fs,Ts,Ks):
   if w==0:continue
   mi=math.ceil(n*w)+math.ceil(2+r/eta)
   assert zeta<=1/mi**2
   cov=100*(K(T,B)/mi+r*np.eye(p)/mi**2)
   assert eigvalsh(100*ku/mi-cov)[0]>-1e-7
   op=w*F@np.linalg.inv(ku)
   S+=op@cov@op.T
   bi=rng.normal(size=p);bi*=zeta/np.linalg.norm(bi);bias+=op@bi
  covtheta=Vi@S@Vi;bt=Vi@bias
  assert bt@V@bt<=zeta*zeta/eta*(1+1e-6)
  err=eigvalsh(covtheta+np.outer(bt,bt)-101*Vi/n)[-1]
  max_res['covariance_positive_violation']=max(max_res['covariance_positive_violation'],float(err));assert err<1e-6
  counts['covariance_and_bias_cases']+=1
 # Adversarial coefficient errors saturating a selected projector direction.
 L=8*D;n=math.ceil(2**24*D*L/eta);rad=64*np.sqrt(D/n)
 for test in range(8):
  ix=int(rng.integers(len(X)));v=rng.normal(size=d)+1j*rng.normal(size=d);v/=np.linalg.norm(v)
  z=Fs[ix]@vec(np.outer(v,v.conj()),B);errcoef=Vi@z;errcoef*=rad/np.sqrt(errcoef@V@errcoef)
  for F,T,U in zip(Fs,Ts,Us):
   E=unvec(F.T@errcoef,B);proposed=2*(T+E)+2*eta*np.eye(d)
   lo=eigvalsh(proposed-T-1.25*eta*np.eye(d))[0]
   hi=eigvalsh(3*T+2.75*eta*np.eye(d)-proposed)[0]
   max_res['envelope_positive_violation']=max(max_res['envelope_positive_violation'],float(-min(lo,hi)))
   assert min(lo,hi)>-1e-8;counts['envelope_operator_cases']+=1
   # Genuine CPTP decoder from random Stinespring k -> 2 with k Kraus rows.
   zz=rng.normal(size=(2*k,k))+1j*rng.normal(size=(2*k,k));uu,_=np.linalg.qr(zz)
   ops=[uu[2*j:2*j+2] for j in range(k)]
   C=sum(np.outer(a.T.reshape(-1),a.T.reshape(-1).conj()) for a in ops)
   assert abs(np.trace(C)-k)<1e-10
   assert np.linalg.norm(C.reshape(k,2,k,2).trace(axis1=1,axis2=3)-np.eye(k))<1e-10
   q=float(np.trace(T@C).real);e=abs(np.trace(E@C));tau=k*eta
   bound=np.sqrt(3*tau*q+32*tau*tau)/16
   max_res['risk_positive_violation']=max(max_res['risk_positive_violation'],float(e-bound));assert e<=bound+1e-10
   counts['full_CPTP_trace_cases']+=1
 # Normalized Gaussian coefficient-error fixture, not actual source simulation.
 chol=np.linalg.cholesky(V);b=17
 for _ in range(8):
  samples=rng.normal(size=(b,D))*np.sqrt(101/n)
  median=np.median(samples,axis=0)
  assert np.linalg.norm(median)<=64*np.sqrt(D/n)
  counts['median_regression_cases']+=1
for j in range(1,65):
 eta=Fraction(1,2**j);c=Fraction(1,16)
 # sqrt32<6, so a rational upper certificate is enough for 3/4.
 assert 3*c*c+12*c<Fraction(3,4)+Fraction(1,64) # use exact sqrt bound below
 assert 3*c*c+2*c*Fraction(17,3)<Fraction(3,4)
 assert Fraction(17,3)**2>32
 assert sum(Fraction(2**i) for i in range(1,j+1))<2/eta
 counts['exact_scale_cases']+=1
out={'status':'PASS_AUTHOR_MATRIX_GLS_DIAGNOSTICS','source_sha256':h('ordinary_generic_matrix_gls_fast_design_20261028.md'),'seed':202610281145,'counts':counts,'minimum_encoder_anchor_covariance_eigenvalue':mineig_anchor,'maximum_residuals':max_res,'scope':'Proof diagnostics on physical quadratic loss families, block covariance/design and actual CPTP test matrices. Synthetic Gaussian coefficient medians are NOT the imported matrix-query measurement or full source-cap execution. No independent receipt or hardware claim.'}
(ROOT/'ordinary_generic_matrix_gls_fast_design_20261028_check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
