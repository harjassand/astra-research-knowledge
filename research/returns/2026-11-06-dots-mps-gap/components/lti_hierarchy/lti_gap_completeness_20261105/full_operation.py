"""Full CPTP repair, including complement branch, on an explicit LTI dual witness.
The witness is feasible but is not asserted to optimize the SDP.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import numpy as np, scipy.linalg as la, json,time,resource
from pathlib import Path
from test_repair import iso,local_apply
OUT=Path(__file__).parent

def repair(X,A,n,L):
 """Return a purification matrix for Phi(XX*). Complete joint-reset channel.
 The measurement is P_L tensor P_R vs its complement. On success decode,
 discard outer virtuals, encode joined buffer. On failure trace both buffers
 and prepare a fixed vector in the joined buffer code. Both leave core intact.
 """
 d,D,_=A.shape;B=d**L;C=d**(n-2*L);rank=X.shape[1]
 V=iso(A,L);J=iso(A,2*L)
 T=X.reshape(B,C,B,rank).transpose(0,2,1,3).reshape(B*B,C,rank)
 U=np.kron(V.conj().T,V.conj().T)
 Z=np.einsum('ab,bcr->acr',U,T).reshape(D,D,D,D,C,rank)
 Y=np.einsum('pcb,abcdqr->pqadr',J.reshape(B*B,D,D),Z,optimize=True)
 Y=Y.reshape(B,B,C,D*D*rank).transpose(1,2,0,3).reshape(d**n,-1)
 # Project before tracing: retain the measurement's correct cross-term removal.
 Tbad=T-np.einsum('ba,acr->bcr',U.conj().T,Z.reshape(D**4,C,rank))
 Cfactor=Tbad.transpose(1,0,2).reshape(C,-1)
 core=Cfactor@Cfactor.conj().T
 w,v=la.eigh((core+core.conj().T)/2);w=np.maximum(w,0)
 Cfactor=v*np.sqrt(w)
 fixed=J[:,0].reshape(B,B)
 Ybad=np.einsum('rl,ck->lcrk',fixed,Cfactor).reshape(d**n,C)
 return np.concatenate([Y,Ybad],axis=1),float(np.linalg.norm(Tbad)**2)

def main():
 start=time.perf_counter();A=np.load(OUT/'mps_inputs.npz')['aklt'];d,D,_=A.shape;n=6;L=2;dim=d**n
 V2=iso(A,2);h=np.eye(d*d)-V2@V2.conj().T
 hs=[local_apply(np.eye(dim),h,(i,(i+1)%n),d,n) for i in range(n)]
 H=sum(hs);e,V=la.eigh(H,subset_by_index=[0,6]);j=np.where(e>1e-8)[0][0];gap=e[j];psi=V[:,j]
 shifts=[psi.reshape([d]*n).transpose(list(range(i,n))+list(range(i))).reshape(-1) for i in range(n)]
 X=np.stack(shifts,axis=1)/np.sqrt(gap)
 # Normalize by actual average, preserving all LTI equalities.
 X/=np.sqrt(np.vdot(X,hs[0]@X).real)
 Vn=iso(A,n);mu=X-Vn@(Vn.conj().T@X)
 moments=[np.vdot(X,z@X).real for z in hs[:-1]]
 before=np.vdot(X,(hs[0]@hs[0]+sum(hs[0]@z+z@hs[0] for z in hs[1:-1]))@X).real
 Y,failed=repair(mu,A,n,L)
 Hc=sum(hs[L:n-L-1]);Hb=H-Hc
 inner_indices=list(range(0,L-1))+list(range(n-L,n-1))+[n-1]
 maxinternal=max(np.linalg.norm(hs[i]@Y) for i in inner_indices)
 output_energy=np.vdot(Y,H@Y).real;output_square=np.linalg.norm(H@Y)**2
 result={'n':n,'buffer':L,'periodic_gap_exact_diagonalization':float(gap),
 'feasible_dual_objective_not_optimized':float(before),'local_normalization_max_error':float(max(abs(x-1) for x in moments)),
 'input_projected_trace':float(np.linalg.norm(mu)**2),'output_trace':float(np.linalg.norm(Y)**2),
 'trace_preservation_error':float(abs(np.linalg.norm(mu)**2-np.linalg.norm(Y)**2)),
 'complement_branch_trace':failed,
 'unchanged_core_energy_error':float(abs(np.vdot(mu,Hc@mu)-np.vdot(Y,Hc@Y))),
 'unchanged_core_square_error':float(abs(np.linalg.norm(Hc@mu)**2-np.linalg.norm(Hc@Y)**2)),
 'joined_buffer_internal_annihilation_norm':float(maxinternal),
 'output_boundary_second_moment':float(np.linalg.norm(Hb@Y)**2),
 'output_energy':float(output_energy),'output_second_moment':float(output_square),
 'physical_excitation_quotient':float(output_square/output_energy),
 'spectral_gap_inequality_slack':float(output_square-gap*output_energy),
 'wall_seconds':time.perf_counter()-start,'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
 print(json.dumps(result,indent=2));(OUT/'full_operation_results.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
