"""Exploratory energy-moment-only SDP. Floating-point values are not certificates."""
import os,sys
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
sys.path[:0]=['/tmp/lti_solver',str(__import__('pathlib').Path(__file__).resolve().parents[1])]
import numpy as np, scipy.linalg as la, scipy.sparse as sp, clarabel, time,json,resource
from pathlib import Path
from test_repair import iso,local_apply
OUT=Path(__file__).parent

def svec(a):
 n=a.shape[0];i,j=np.triu_indices(n);o=np.lexsort((i,j));i,j=i[o],j[o]
 return a[i,j]*np.where(i==j,1,np.sqrt(2))
def run(A,n):
 t=time.perf_counter();d,D,_=A.shape;dim=d**n
 V2=iso(A,2).real;h=np.eye(d*d)-V2@V2.T
 hs=[local_apply(np.eye(dim),h,(i,i+1),d,n).real for i in range(n-1)]
 H=sum(hs);E=la.eigvalsh(H);gap=min(E[E>1e-9]);knabe=(n-1)/(n-2)*(gap-1/(n-1))
 U=la.null_space(iso(A,n).T).real;r=U.shape[1]
 # Energy first/square moments coincide for this projector interaction.
 diffs=[hs[i+1]-hs[i] for i in range(n-2)]
 for i in range(n-2):
  for j in range(i+1,n-2):
   diffs.append(hs[i+1]@hs[j+1]+hs[j+1]@hs[i+1]-hs[i]@hs[j]-hs[j]@hs[i])
 G=hs[0]@hs[0]+sum(hs[0]@z+z@hs[0] for z in hs[1:])
 b=svec(U.T@G@U);hvec=svec(U.T@hs[0]@U)
 B=np.stack([svec(U.T@z@U) for z in diffs],axis=1)
 # Orthonormalize the actual divergence span; singular vectors merely change coordinates.
 left,s,_=la.svd(B,full_matrices=False);keep=s>1e-10;B=left[:,keep]
 mat=sp.csc_matrix(np.column_stack([hvec,-B]));nv=mat.shape[1]
 q=np.zeros(nv);q[0]=-1
 settings=clarabel.DefaultSettings();settings.verbose=False;settings.tol_gap_abs=1e-8;settings.tol_feas=1e-8;settings.tol_gap_rel=1e-8;settings.max_iter=100
 build=time.perf_counter()-t;t2=time.perf_counter()
 solver=clarabel.DefaultSolver(sp.csc_matrix((nv,nv)),q,mat,b,[clarabel.PSDTriangleConeT(r)],settings)
 sol=solver.solve();delta=sol.x[0]
 residual=b-mat@np.array(sol.x);i,j=np.triu_indices(r);o=np.lexsort((i,j));i,j=i[o],j[o]
 Q=np.zeros((r,r));Q[i,j]=residual/np.where(i==j,1,np.sqrt(2));Q=Q+Q.T-np.diag(np.diag(Q))
 result={'n':n,'physical_dimension':dim,'cone_dimension':r,'raw_moment_divergences':len(diffs),'independent_divergences':int(sum(keep)),
 'solver_scalar_variables':nv,'full_Y_real_symmetric_variables':d**(n-1)*(d**(n-1)+1)//2,
 'status':str(sol.status),'delta_exploratory':float(delta),'minimum_complement_eigenvalue':float(la.eigvalsh(Q).min()),
 'open_chain_gap':float(gap),'knabe_bound':float(knabe),'build_seconds':build,'solve_seconds':time.perf_counter()-t2,'total_seconds':time.perf_counter()-t,
 'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
 print(json.dumps(result),flush=True);return result
A=np.load(OUT.parent/'mps_inputs.npz')['aklt'];results=[]
for n in [3,4]:results.append(run(A,n))
(OUT/'results.json').write_text(json.dumps(results,indent=2)+'\n')
