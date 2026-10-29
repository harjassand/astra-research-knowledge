"""One-call coherent commutator Gram instrument, with retained quantum memory."""
import numpy as np,json
from scipy.linalg import expm,sqrtm
from pathlib import Path
P=Path(__file__).parent;rng=np.random.default_rng(290608)
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);paulis=[X,Y,Z]
D=4;m=2;r=2;ops=[np.kron(a,b) for a in paulis for b in paulis]
psi=rng.normal(size=(m,r))+1j*rng.normal(size=(m,r));psi/=np.linalg.norm(psi);sig=psi@psi.conj().T
rhoMR=np.outer(psi.reshape(-1),psi.reshape(-1).conj())
# Full controlled gates on C,F,S,M. No controlled source operation.
pre=np.eye(9*2*D*m,dtype=complex);post=pre.copy()
for j,p in enumerate(ops):
 for f,mat in [(0,pre),(1,post)]:
  a=(2*j+f)*D*m;mat[a:a+D*m,a:a+D*m]=np.kron(p,I)
# index j,f,s,m,data_reference,memory_reference
state=np.einsum('j,f,su,mv->jfsmuv',np.ones(9)/3,np.ones(2)/np.sqrt(2),np.eye(D)/np.sqrt(D),psi).reshape(9*2*D*m,D*r)

def run(name,Ks,kernel=None):
 assert np.linalg.norm(sum(K.conj().T@K for K in Ks)-np.eye(D*m))<1e-12
 deltas=[[K@np.kron(p,I)-np.kron(p,I)@K for p in ops] for K in Ks]
 gram=np.array([[sum(np.trace(np.kron(np.eye(D),sig)@ds[j].conj().T@ds[k]) for ds in deltas)/(2*D) for k in range(9)] for j in range(9)])
 outputs=[];errors=[]
 for sign in [1,-1]:
  direct=np.zeros((9*m*r,9*m*r),complex);formula=direct.copy()
  for K in Ks:
   w=post@np.kron(np.eye(18),K)@pre@state;w=w.reshape(9,2,D,m,D,r)
   v=(w[:,0]+sign*w[:,1])/np.sqrt(2) # j,s,m,refdata,refmem
   v=v.transpose(0,2,4,1,3).reshape(9*m*r,D*D);direct+=v@v.conj().T
   ds=[K@np.kron(p,I)+sign*np.kron(p,I)@K for p in ops]
   for sout in range(D):
    for sin in range(D):
     L=np.concatenate([A.reshape(D,m,D,m)[sout,:,sin,:] for A in ds],axis=0)/(2*np.sqrt(9*D))
     J=np.kron(L,np.eye(r));formula+=J@rhoMR@J.conj().T
  errors.append(float(np.linalg.norm(direct-formula)));outputs.append(direct)
 control=np.einsum('jaka->jk',outputs[1].reshape(9,m*r,9,m*r))
 residual=float(np.linalg.norm(control-gram.T/18));assert residual<1e-12 and max(errors)<1e-12
 totaltrace=float(sum(np.trace(o).real for o in outputs));assert abs(totaltrace-1)<1e-12
 ordinary=np.zeros((m*r,m*r),complex)
 for K in Ks:
  for sout in range(D):
   for sin in range(D):
    B=K.reshape(D,m,D,m)[sout,:,sin,:]/np.sqrt(D);J=np.kron(B,np.eye(r));ordinary+=J@rhoMR@J.conj().T
 aggregate=np.einsum('jajb->ab',(outputs[0]+outputs[1]).reshape(9,m*r,9,m*r))
 marginal=float(np.linalg.norm(aggregate-ordinary));assert marginal<1e-12
 # Source may leave control entangled with memory/ref; factorization is NOT assumed.
 prob=float(np.trace(control).real);mr=np.einsum('jajb->ab',outputs[1].reshape(9,m*r,9,m*r))
 correlated=float(np.linalg.norm(outputs[1]-np.kron(control,mr)/prob)) if prob>1e-15 else 0.
 res={'unconditioned_memory_matches_one_ordinary_mixed_input_call':marginal,'name':name,'source_Kraus':len(Ks),'source_unitality_defect':float(np.linalg.norm(sum(K@K.conj().T for K in Ks)-np.eye(D*m))),'full_CMR_instrument_residuals_plus_minus':errors,'control_H_transpose_over18_residual':residual,'gram_min_eigenvalue':float(np.linalg.eigvalsh(gram).min()),'minus_probability':prob,'both_branches_total_trace':totaltrace,'control_vs_H_over18_difference':float(np.linalg.norm(control-gram/18)),'minus_control_memory_nonproduct_residual':correlated}
 if kernel is not None:res['known_twisted_swap_kernel_residual']=float(np.linalg.norm(gram@kernel));assert res['known_twisted_swap_kernel_residual']<1e-12
 np.savez_compressed(P/(name+'.npz'),gram=gram,control=control,minus_CMR=outputs[1],memory_reference_input=psi,Kraus=np.array(Ks),kernel=kernel if kernel is not None else np.array([]))
 return res
A=rng.normal(size=(24,8))+1j*rng.normal(size=(24,8));V=np.linalg.qr(A)[0];randomKs=list(V.reshape(3,8,8))
S=np.zeros((4,4))
for a in range(2):
 for b in range(2):S[2*b+a,2*a+b]=1
J=[np.kron(p,I)+np.kron(I,p) for p in paulis]
U=expm(-.31j*(np.kron(J[0],X)+.7*np.kron(J[1],Z)+.4*np.kron(J[2],Y)))
low=np.array([[0,1],[0,0]],complex);jump=(np.kron(low,I)+np.kron(I,low))/np.sqrt(2)
A1=np.sqrt(.37)*jump;A0=np.asarray(sqrtm(np.eye(4)-A1.conj().T@A1),complex)
local=expm(-.39j*(.2*X+.4*Y+.8*Z));W=np.kron(local,I);WW=np.kron(W,I)
Ks=[WW@np.kron(A,I)@U@WW.conj().T for A in [A0,A1]]
T=W@S@W.conj().T;C=np.array([np.trace(p@T).real/2 for p in ops]);assert np.linalg.norm(C.reshape(3,3).T@C.reshape(3,3)-np.eye(3))<1e-12 and np.linalg.det(C.reshape(3,3))>0
results=[run('random_nonunital',randomKs),run('twisted_collective_nonunital',Ks,C),run('identity',[np.eye(8)],C)]
(P/'results.json').write_text(json.dumps({'scope':'Actual dense one-call circuit and full retained control-memory-reference CP instrument, floating checks not hardware or certified intervals.','fixtures':results},indent=2)+'\n');print(json.dumps(results,indent=2))
