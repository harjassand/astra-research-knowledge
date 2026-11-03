"""Exact small-Fock test: combined Gaussian purification incl parity-changing subfactors."""
import os;os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np,json
from scipy.linalg import expm

def fermions(n):
 cs=[]
 for j in range(n):
  c=np.zeros((2**n,2**n),complex)
  for x in range(2**n):
   if x>>j&1:c[x^(1<<j),x]=(-1)**((x&((1<<j)-1)).bit_count())
  cs.append(c)
 return cs

def majoranas(cs):return [g for c in cs for g in (c+c.conj().T,-1j*(c-c.conj().T))]
def cov(psi,gs):
 out=np.zeros((len(gs),len(gs)))
 for j in range(len(gs)):
  for k in range(j+1,len(gs)):
   out[j,k]=np.real(1j*np.vdot(psi,gs[j]@gs[k]@psi));out[k,j]=-out[j,k]
 return out

def run(psi,n,label):
 cs=fermions(n);gs=majoranas(cs);G=cov(psi,gs);assert np.linalg.norm(G@G+np.eye(2*n))<1e-9
 ds=fermions(2*n);gg=majoranas(ds)
 bell=np.eye(2**(2*n),dtype=complex)[:,0]
 for j in range(n):bell=(bell+ds[j].conj().T@ds[n+j].conj().T@bell)/np.sqrt(2)
 # Native basis bit index = a occupation + (b occupation << n).
 D=2**n;canonical=np.zeros(D*D,complex)
 for a in range(D):
  for b in range(D):canonical[a+(b<<n)]=psi[a]*psi[b].conjugate()*((-1)**(b.bit_count()*(b.bit_count()-1)//2))
 # b'=C^T b, C=-X independently on each pair of Majoranas.
 C=np.kron(np.eye(n),np.array([[0.,-1.],[-1.,0.]]))
 S=np.block([[np.eye(2*n),np.zeros((2*n,2*n))],[np.zeros((2*n,2*n)),C]])
 K=np.block([[np.zeros_like(G),G],[G,np.zeros_like(G)]])
 A=S@(-np.pi/4*K)@S.T
 generator=sum(A[j,k]/2*gg[j]@gg[k] for j in range(4*n) for k in range(j+1,4*n))
 prepared=expm(generator)@bell
 err=np.linalg.norm(prepared-canonical)
 # On fixed even parity, graded conjugation is the onsite i^N phase.
 ordinary_phased=np.zeros(D*D,complex)
 for a in range(D):
  for b in range(D):ordinary_phased[a+(b<<n)]=psi[a]*psi[b].conjugate()*1j**b.bit_count()
 overlap=np.vdot(bell,prepared)
 out=dict(label=label,fast_modes=n,purification_error=float(err),onsite_phase_identity_error=float(np.linalg.norm(canonical-ordinary_phased)),bell_overlap_real=float(overlap.real),bell_overlap_imag=float(overlap.imag),expected_positive_overlap=2**(-n/2))
 assert err<1e-9 and out['onsite_phase_identity_error']<1e-9
 return out
out=[]
for n in [2,4]:
 psi=np.eye(2**n,dtype=complex)[:,0];out.append(run(psi,n,'vacuum'))
 psi=np.eye(2**n,dtype=complex)[:,3];out.append(run(psi,n,'free_and_decoration_parity_both_flipped'))
 rng=np.random.default_rng(50+n);gs=majoranas(fermions(n));A=rng.normal(size=(2*n,2*n));A=A-A.T
 gen=sum(A[j,k]/2*gs[j]@gs[k] for j in range(2*n) for k in range(j+1,2*n));psi=expm(gen)@np.eye(2**n)[:,0]
 out.append(run(psi,n,'generic_even_Bogoliubov_state'))
open('producer-workspace/graded_purification_results.json','w').write(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
