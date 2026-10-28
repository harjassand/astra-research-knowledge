import numpy as np
from fractions import Fraction as F
from pathlib import Path
import json,hashlib,math
rng=np.random.default_rng(2735); Q=Path(__file__).parent
phi=np.array([1,0,0,1],complex)/np.sqrt(2);Phi=np.outer(phi,phi.conj());psi=np.array([0,1,-1,0],complex)/np.sqrt(2)
def pt(M,k):return M.reshape(2,k,2,k).transpose(2,1,0,3).reshape(2*k,2*k)
def trA(M,k):return np.einsum('aiaj->ij',M.reshape(2,k,2,k))
def filters(v,k):
 U,s,Vh=np.linalg.svd(v.reshape(2,k),full_matrices=False)
 V=Vh.T;J=np.array([[0,-1],[1,0]])
 FA=(U@np.diag(s)@J).T;FB=V.conj().T
 return FA,FB,s*s
cases=0;max_witness=max_scalar=max_O=0.;min_accept_margin=min_fid_margin=1.
for k in [2,3,5,8]:
 for noise in [0,.1,.3,.6]:
  for rep in range(12):
   W=rng.normal(size=(k,2))+1j*rng.normal(size=(k,2));W=np.linalg.qr(W)[0]
   vec=W.T.reshape(-1)/np.sqrt(2);Jp=np.outer(vec,vec.conj())
   A=rng.normal(size=(k,k))+1j*rng.normal(size=(k,k));rho=A@A.conj().T;rho/=np.trace(rho)
   J=(1-noise)*Jp+noise*np.kron(np.eye(2)/2,rho)
   ev,U=np.linalg.eigh(pt(J,k));neg=-ev[0]
   if neg<=1e-10:continue
   v=U[:,0];FA,FB,s=filters(v,k);K=np.kron(FA,FB);Jf=K@J@K.conj().T
   a=np.trace(Jf).real;fid=np.vdot(phi,Jf@phi).real/a
   Wv=pt(np.outer(v,v.conj()),k)
   max_witness=max(max_witness,np.linalg.norm(Wv-2*K.conj().T@(np.eye(4)/2-Phi)@K))
   max_scalar=max(max_scalar,abs(a*(1-2*fid)+neg))
   assert min(s)>=neg*neg-1e-12
   min_accept_margin=min(min_accept_margin,a-neg)
   min_fid_margin=min(min_fid_margin,fid-.5-neg/2)
   assert a>=neg-1e-12 and fid>=.5+neg/2-1e-12
   rb=trA(J,k);T=(2*np.kron(np.eye(2),rb)-J)/3
   Ov=2*np.kron(np.eye(2),trA(np.outer(v,v.conj()),k))-3*Wv
   assert np.linalg.eigvalsh(T)[0]>=-1e-12 and np.linalg.norm(Ov,2)<=5+1e-12
   max_O=max(max_O,abs(np.trace(T@Ov).real+neg));cases+=1
assert max(max_witness,max_scalar,max_O)<1e-11
# Physical 8-input source / four real selectors: quadratic witness and stationary grid bound.
quadcases=0;quad_max=0.
for rep in range(40):
 k=4;r=3;V=np.linalg.qr(rng.normal(size=(k*r,8))+1j*rng.normal(size=(k*r,8)))[0]
 Ks=[V[a*k:(a+1)*k,:] for a in range(r)]
 def choi(x):
  J=np.zeros((2*k,2*k),complex)
  for K in Ks:
   Kx=sum(x[j]*K[:,2*j:2*j+2] for j in range(4));v=Kx.T.reshape(-1)/np.sqrt(2);J+=np.outer(v,v.conj())
  return J
 v=rng.normal(size=2*k)+1j*rng.normal(size=2*k);v/=np.linalg.norm(v)
 def f(x):return np.vdot(v,pt(choi(x),k)@v).real
 Es=np.eye(4);B=np.diag([f(x) for x in Es])
 for i in range(4):
  for j in range(i):B[i,j]=B[j,i]=f((Es[i]+Es[j])/np.sqrt(2))-(B[i,i]+B[j,j])/2
 ev,U=np.linalg.eigh(B);x=U[:,0];u=rng.normal(size=4);y=x+.01*u;y/=np.linalg.norm(y);h=np.linalg.norm(y-x)
 gap=f(y)-f(x);assert gap<=2*h*h+1e-12 and min(ev)>=-1-1e-12 and max(ev)<=1+1e-12
 quad_max=max(quad_max,abs(f(y)-y@B@y));quadcases+=1
# Exact constants and filtered-pair reservoir lower means.
constantcases=0
for den in range(4,84):
 mu=F(1,den);ea=mu/F(4096)
 assert 196*ea<mu/F(20)
 assert -2*mu+mu/F(8)+mu/F(10)+mu/F(16)<-3*mu/F(2)
 for N in [1,5,100]:
  tf=40;n=(2*(N+tf)*mu.denominator+mu.numerator-1)//mu.numerator
  assert n*mu>=2*(N+tf)
  constantcases+=1
# Exact amplitude-damping example: entries use sqrt(r)=1/4.
r=F(1,16);surv=float(r);K0=np.diag([1,np.sqrt(surv)]);K1=np.array([[0,np.sqrt(1-surv)],[0,0]])
J=sum(np.outer(K.T.reshape(-1),K.T.reshape(-1).conj())/2 for K in [K0,K1])
v=np.array([0,1,-np.sqrt(surv),0])/np.sqrt(1+surv);FA=np.diag([1,np.sqrt(surv)])/np.sqrt(1+surv);JF=np.kron(FA,np.eye(2))@J@np.kron(FA,np.eye(2))
a=np.trace(JF).real;fid=np.vdot(phi,JF@phi).real/a
assert abs(np.vdot(v,pt(J,2)@v).real+1/32)<1e-12 and abs(a-.5)<1e-12 and abs(fid-17/32)<1e-12
assert (1+2*F(1,4)+r)/4==F(25,64)
out={'status':'PASS_AUTHOR_NPT_FILTERED_FRONTEND_CHECKS','physical_NPT_choi_filter_cases':cases,'physical_quadratic_source_cases':quadcases,'exact_constant_cap_cases':constantcases,'max_complex_witness_identity_residual':max_witness,'max_acceptance_fidelity_identity_residual':max_scalar,'max_ordinary_witness_identity_residual':max_O,'max_quadratic_interpolation_residual':quad_max,'min_acceptance_slack':min_accept_margin,'min_fidelity_slack':min_fid_margin,'amplitude_damping':{'negative_eigenvalue':'-1/32','filter_acceptance':'1/2','filtered_fidelity':'17/32','best_cptp_fidelity':'25/64'},'source_sha256':hashlib.sha256((Q/'ORDINARY_NPT_FILTERED_SEED_FRONTEND.md').read_bytes()).hexdigest(),'scope':'Actual finite physical Choi/filter/operator matrices and rational scalar constants, not simulated ordinary training samples, complete SDP execution, raw factories or hardware.'}
(Q/'ordinary_npt_frontend_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
