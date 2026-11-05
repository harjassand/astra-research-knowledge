"""Numerical tests of the complete periodic-excitation -> GNS-witness operation.
Floating point, not interval-certified physical bounds or a proof by testing.
Independent self-contained implementation; no prior proposal code imported.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import numpy as np
import scipy.linalg as la
from scipy.sparse.linalg import LinearOperator,eigsh
from pathlib import Path
import json,time,resource,hashlib
OUT=Path(__file__).resolve().parent

def block(A,n):
 D=A.shape[1]; T=np.eye(D,dtype=complex)[None]
 for _ in range(n):T=np.einsum('wab,sbc->wsac',T,A).reshape(-1,D,D)
 return T.reshape(-1,D*D)
def fixed(A):
 D=A.shape[1];E=np.einsum('sab,scd->acbd',A,A.conj()).reshape(D*D,D*D)
 w,v=la.eig(E.conj().T);S=v[:,np.argmin(abs(w-1))].reshape(D,D)
 S=(S+S.conj().T)/2;S/=np.trace(S)
 assert la.norm(sum(a@a.conj().T for a in A)-np.eye(D))<1e-10
 return S
def sqrtm(P):
 w,v=la.eigh((P+P.conj().T)/2);return (v*np.sqrt(np.maximum(w,0)))@v.conj().T

def local(Y,h,axes,d,n):
 shape=Y.shape;T=Y.reshape(*([d]*n),-1)
 perm=list(axes)+[i for i in range(n+1) if i not in axes]
 inv=np.argsort(perm);T=T.transpose(perm);ts=T.shape
 return (h@T.reshape(h.shape[0],-1)).reshape(ts).transpose(inv).reshape(shape)

def hamiltonian(h,d,n,periodic=True):
 bonds=[(i,i+1) for i in range(n-1)]+([(n-1,0)] if periodic else [])
 def apply(v):
  return sum((local(v,h,p,d,n) for p in bonds),np.zeros_like(v,dtype=complex))
 return LinearOperator((d**n,d**n),matvec=apply,matmat=apply,dtype=complex),apply

def excitation(A,h,n):
 d,D,_=A.shape;H,apply=hamiltonian(h,d,n)
 rng=np.random.default_rng(908+n)
 e,V=eigsh(H,k=7,which='SA',tol=2e-11,v0=rng.normal(size=d**n)+1j*rng.normal(size=d**n))
 ix=np.argsort(e);e=e[ix];V=V[:,ix];idx=np.flatnonzero(e>1e-7)[0];E=float(e[idx]);psi=V[:,idx]
 shifts=np.stack([psi.reshape([d]*n).transpose(list(range(i,n))+list(range(i))).reshape(-1) for i in range(n)])
 ps=np.fft.fft(shifts,axis=0);p=int(np.argmax(la.norm(ps,axis=1)));psi=ps[p]/la.norm(ps[p]);res=la.norm(apply(psi)-E*psi)
 assert res<1e-7,res
 return E,psi,apply,p,res

def run(A,h,label,n,buffers):
 t0=time.perf_counter();d,D,_=A.shape;S=fixed(A);W=np.kron(S.T,np.eye(D));Ws=sqrtm(W)
 GN=block(A,n);omega=GN@np.eye(D).reshape(-1);Z=np.vdot(omega,omega).real;omega/=np.sqrt(Z)
 E,psi,H,p,res=excitation(A,h,n);M=la.eigvalsh(h).max()
 F=np.eye(D*D).reshape(D,D,D,D).transpose(1,0,2,3).reshape(D*D,D*D)
 records=[]
 for ell in buffers:
  L=n-ell;GL=block(A,L);GB=block(A,ell);P=GB@la.pinv(GB)
  Y=psi.reshape(d**L,d**ell)@P.T;phi=Y.reshape(-1);q=1-np.vdot(phi,phi).real
  X=Y@la.pinv(GB).T;O=np.sqrt(Z)*X@F@la.pinv(GL)
  reconstruction=(O@omega.reshape(d**L,d**ell)).reshape(-1)
  err=float(la.norm(phi-reconstruction));orth=abs(np.vdot(omega,phi));opnorm=la.norm(O,2)
  finite_energy=float(np.vdot(phi,H(phi)).real)
  # Infinite state contractions use only exact virtual boundary metric W.
  T=O@GL@Ws;inorm=float(la.norm(T)**2)
  mean=np.trace(O@GL@W@GL.conj().T)
  variance=inorm-abs(mean)**2
  Gext=block(A,L+2);Text=local(Gext,O,tuple(range(1,L+1)),d,L+2)@Ws
  ien=float(sum(np.vdot(Text,local(Text,h,(j,j+1),d,L+2)).real for j in range(L+1)))
  rq=ien/variance
  HB,hb=hamiltonian(h,d,ell,False)
  eb=la.eigvalsh(hb(np.eye(d**ell)));gell=float(eb[eb>1e-8][0])
  lost_bound=(ell-1)*E/(gell*n)
  # Exact finite buffer marginal formula versus direct partial trace.
  K=GL@F@GB.T/np.sqrt(Z);rho=K@K.conj().T
  direct=omega.reshape(d**L,d**ell);rho_direct=direct@direct.conj().T
  rdm_error=la.norm(rho-rho_direct)
  inf=GL@W@GL.conj().T
  td=la.norm(rho-inf,'nuc')
  Gremain=block(A,ell-2);Gexgram=Gext.conj().T@Gext;Rex=F@(Gremain.conj().T@Gremain).T@F/Z-W
  tdext=la.norm(sqrtm(Gexgram)@Rex@sqrtm(Gexgram),'nuc')
  localenergies=[np.vdot(psi,local(psi,h,(j,(j+1)%n),d,n)).real for j in range(n)]
  checks={
   'eigen_residual':res<1e-7,'uniform_energy':max(abs(np.array(localenergies)-E/n))<1e-8,
   'projection_norm_bound':q<=lost_bound+1e-9,'orthogonality':orth<1e-9,
   'operator_reconstruction':err<1e-9,'energy_projection_bound':finite_energy<=E+2*M*np.sqrt(max(q,0))+1e-9,
   'sharp_positive_seam_bound':finite_energy<=E+2*np.sqrt((2*E/n)*(2*M)*max(q,0))+2*M*max(q,0)+1e-9,
   'rdm_formula':rdm_error<1e-9,'norm_transfer_bound':abs(inorm-(1-q))<=td*opnorm**2+1e-9,
   'mean_transfer_bound':abs(mean)<=td*opnorm+1e-9,
   'energy_transfer_bound':abs(ien-finite_energy)<=tdext*M*(L+1)*opnorm**2+1e-9,
   'positive_variance':variance>0,'gns_energy_nonnegative':ien>=-1e-10}
  checks={k:bool(v) for k,v in checks.items()}
  assert all(checks.values()),checks
  rec={'model':label,'n':n,'buffer':ell,'core':L,'momentum_index':p,'periodic_gap_numerical':E,
   'excitation_residual':res,'projection_lost_norm':float(q),'projection_bound_finite_buffer_gap':lost_bound,
   'finite_projected_energy':finite_energy,'sharp_projection_energy_bound':float(E+2*np.sqrt((2*E/n)*(2*M)*max(q,0))+2*M*max(q,0)),'local_operator_norm':float(opnorm),'operator_reconstruction_error':err,
   'periodic_ground_overlap':float(orth),'infinite_norm':inorm,'infinite_ground_overlap':float(abs(mean)),
   'infinite_energy':ien,'gns_variational_quotient_uncertified':float(rq),'core_rdm_trace_distance':float(td),
   'energy_support_rdm_trace_distance':float(tdext),'direct_rdm_formula_error':float(rdm_error),'checks':checks}
  print(json.dumps(rec),flush=True);records.append(rec)
 return records,{'model':label,'n':n,'wall_seconds':time.perf_counter()-t0,'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}

def main():
 t=time.perf_counter();data=np.load(OUT/'mps_inputs.npz');records=[];costs=[]
 for label,A in [('AKLT',data['aklt']),('generic_complex_projector',data['generic'])]:
  G=block(A,2);Q=np.eye(A.shape[0]**2)-G@la.pinv(G);h=(Q+Q.conj().T)/2
  for n,ells in [(6,[2,3]),(8,[2,3,4])]:
   rs,c=run(A,h,label,n,ells);records+=rs;costs.append(c)
 # Same generic local kernel with a non-projector positive interaction.
 A=data['generic'];G=block(A,2);Q=np.eye(A.shape[0]**2)-G@la.pinv(G)
 rng=np.random.default_rng(415);R=rng.normal(size=Q.shape)+1j*rng.normal(size=Q.shape)
 h=Q@(np.eye(Q.shape[0])+R@R.conj().T/Q.shape[0])@Q;h=(h+h.conj().T)/2;h/=la.eigvalsh(h).max()
 rs,c=run(A,h,'generic_complex_nonprojector',6,[2,3]);records+=rs;costs.append(c)
 out={'status':'all checks passed; floating point only','records':records,'costs':costs,
  'total_wall_seconds':time.perf_counter()-t,'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
  'numpy_version':np.__version__,'scipy_version':__import__('scipy').__version__,
  'input_sha256':hashlib.sha256((OUT/'mps_inputs.npz').read_bytes()).hexdigest()}
 (OUT/'embedding_results.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
