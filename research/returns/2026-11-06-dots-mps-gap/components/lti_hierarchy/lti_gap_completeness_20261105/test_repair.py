"""Construct and numerically test proposed periodic MPS boundary repair.
Floating-point verification of an operator lemma, NOT a proof or SDP solve.
The tested input spans the entire joint local-ground subspace, not sample states.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import numpy as np, scipy.linalg as la, json, time, resource
from pathlib import Path
OUT=Path(__file__).parent

def power(a,p):
 w,v=la.eigh((a+a.conj().T)/2)
 assert w.min()>1e-13,(w,p)
 return (v*w**p)@v.conj().T

def block(A,L):
 d,D,_=A.shape
 B=np.eye(D,dtype=complex)[None]
 for _ in range(L): B=np.einsum('pab,sbc->psac',B,A).reshape(-1,D,D)
 return B.reshape(d**L,D*D)

def iso(A,L):
 G=block(A,L);return G@power(G.conj().T@G,-.5)

def canonical(A):
 d,D,_=A.shape
 E=np.einsum('sij,skl->ikjl',A,A.conj()).reshape(D*D,D*D)
 w,v=la.eig(E);j=np.argmax(w.real);lam=w[j].real
 R=v[:,j].reshape(D,D); R=(R+R.conj().T)/2
 if np.trace(R).real<0:R=-R
 A=np.einsum('ab,sbc,cd->sad',power(R,-.5),A,power(R,.5))/np.sqrt(lam)
 E=np.einsum('sij,skl->ikjl',A,A.conj()).reshape(D*D,D*D)
 w,v=la.eig(E.conj().T); S=v[:,np.argmin(abs(w-1))].reshape(D,D);S=(S+S.conj().T)/2;S/=np.trace(S)
 return A,S

def local_apply(Y,h,axes,d,N):
 tail=Y.shape[1:];T=Y.reshape(*([d]*N),*tail)
 rest=[i for i in range(N+len(tail)) if i not in axes]
 perm=list(axes)+rest;inv=np.argsort(perm)
 T=T.transpose(perm);shape=T.shape
 T=(h@T.reshape(d*d,-1)).reshape(shape).transpose(inv)
 return T.reshape(Y.shape)

def construct(A,L,ideal=False):
 d,D,_=A.shape
 G=block(A,L); V=iso(A,L);Vnext=iso(A,L+1)
 # Raw block Gram limit under our explicit (left,right) vectorization.
 # Finite long block is unnecessary: compute dual transfer fixed point.
 _,sigma=canonical(A)
 Ginf=np.kron(np.eye(D),sigma)
 if ideal:
  decode=power(Ginf,.5)@la.pinv(G)
  encode=block(A,2*L)@power(Ginf,-.5)
 else:decode=V.conj().T;encode=iso(A,2*L)
 TL=np.einsum('up,psx->usx',decode,Vnext.reshape(d**L,d,D*D)).reshape(D,D,d,D*D)
 TR=np.einsum('uq,tqy->tuy',decode,Vnext.reshape(d,d**L,D*D)).reshape(d,D,D,D*D)
 Y=np.einsum('pcb,absx,tcdy->pstadxy',encode.reshape(d**(2*L),D,D),TL,TR,optimize=True)
 return Y.reshape(d**(2*L+2),D*D,D**4)

def run(A,name,L):
 t=time.perf_counter();d,D,_=A.shape
 V2=iso(A,2); h=np.eye(d*d)-V2@V2.conj().T
 Y=construct(A,L); Yi=construct(A,L,True);N=2*L+2
 WY=local_apply(Y,h,(2*L-1,2*L),d,N)+local_apply(Y,h,(2*L+1,0),d,N)
 Wi=local_apply(Yi,h,(2*L-1,2*L),d,N)+local_apply(Yi,h,(2*L+1,0),d,N)
 F=WY.reshape(-1,D**4).conj().T@WY.reshape(-1,D**4)
 gram=Y.reshape(-1,D**4).conj().T@Y.reshape(-1,D**4)
 r={'model':name,'buffer':L,'compressed_boundary_square_norm':float(la.eigvalsh(F).max()),
 'isometry_error':float(la.norm(gram-np.eye(D**4),2)),
 'ideal_boundary_residual_norm':float(la.norm(Wi.reshape(-1,D**4),2)),
 'actual_ideal_stinespring_distance':float(la.norm((Y-Yi).reshape(-1,D**4),2)),
 'gram_limit_distance':float(la.norm(block(A,L).conj().T@block(A,L)-np.kron(np.eye(D),canonical(A)[1]),2)),
 'wall_seconds':time.perf_counter()-t,'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
 print(json.dumps(r),flush=True);return r

def main():
 A=np.array([[[0,np.sqrt(2/3)],[0,0]],[[-1/np.sqrt(3),0],[0,1/np.sqrt(3)]],[[0,0],[-np.sqrt(2/3),0]]],complex)
 rng=np.random.default_rng(8347)
 R=rng.normal(size=(3,2,2))+1j*rng.normal(size=(3,2,2));R,S=canonical(R)
 np.savez(OUT/'mps_inputs.npz',aklt=A,generic=R,generic_sigma=S)
 results=[]
 for name,B in [('AKLT',A),('generic_complex',R)]:
  for L in [2,3,4]:results.append(run(B,name,L))
 (OUT/'repair_results.json').write_text(json.dumps(results,indent=2)+'\n')
if __name__=='__main__':main()
