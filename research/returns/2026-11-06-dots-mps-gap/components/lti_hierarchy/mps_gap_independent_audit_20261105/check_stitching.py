"""Independent tensor/transfer audit; imports no proposed proof-test code."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
from pathlib import Path
import itertools,json,time,hashlib
import numpy as np
from scipy.linalg import eigh,norm,pinv
P=Path(__file__).resolve().parent;source=P.parent/'lti_gap_completeness_20261105'/'mps_inputs.npz'
z=np.load(source);started=time.perf_counter()
def block(A,L):
    d,D,_=A.shape;rows=[]
    for word in itertools.product(range(d),repeat=L):
        B=np.eye(D,dtype=complex)
        for s in word:B=B@A[s]
        rows.append(B.reshape(-1))
    return np.array(rows)
def power(X,p):
    w,V=eigh((X+X.conj().T)/2);assert min(w)>1e-12
    return (V*w**p)@V.conj().T
def transfer_gram(A,L):
    D=A.shape[1];E=sum(np.kron(a,a.conj()) for a in A)
    T=np.linalg.matrix_power(E,L).reshape(D,D,D,D)
    return T.transpose(1,3,0,2).reshape(D*D,D*D)
def channel_on_good_basis(A,R,L,ideal=False):
    d,D,_=A.shape;B=block(A,L);Bn=block(A,L+1);B2=block(A,2*L)
    Vn=Bn@power(Bn.conj().T@Bn,-.5)
    Ginf=np.kron(np.eye(D),R)
    decode=power(Ginf,.5)@pinv(B) if ideal else power(B.conj().T@B,-.5)@B.conj().T
    encode=B2@power(Ginf,-.5) if ideal else B2@power(B2.conj().T@B2,-.5)
    # Start with every orthonormal left/right good-block basis vector, with
    # coefficient index retained as a reference. Explicit matrix operations
    # independently implement both buffer decodes and virtual permutations.
    psi=np.kron(Vn,Vn).reshape(d**L,d,d,d**L,D**4)
    x=(decode@psi.reshape(d**L,-1)).reshape(D*D,d,d,d**L,D**4)
    x=np.tensordot(decode,x,axes=(1,3)).transpose(1,2,3,0,4)
    x=x.reshape(D,D,d,d,D,D,D**4)
    x=x.transpose(4,1,0,5,2,3,6).reshape(D*D,-1)
    y=(encode@x).reshape(d**(2*L),D,D,d,d,D**4)
    # Physical output order: right untouched neighbor, R buffer, L buffer,
    # left untouched neighbor. The discarded outer legs form the environment.
    y=y.transpose(4,0,3,1,2,5).reshape(d**(2*L+2),D*D,D**4)
    return y
def seams(Y,h,d,N):
    first=(h@Y.reshape(d*d,-1)).reshape(Y.shape)
    x=Y.reshape(d**(N-2),d*d,-1)
    last=np.einsum('ab,pbf->paf',h,x).reshape(Y.shape)
    return first+last
rows=[]
for name in ['aklt','generic']:
    A=z[name];d,D,_=A.shape
    E=sum(np.kron(a,a.conj()) for a in A)
    w,V=np.linalg.eig(E.conj().T);R=V[:,np.argmin(abs(w-1))].reshape(D,D)
    R=(R+R.conj().T)/2;R/=np.trace(R)
    G2=block(A,2);assert norm(transfer_gram(A,2)-G2.conj().T@G2)<1e-12
    gram100=transfer_gram(A,100)
    gramcheck={'model':name,'correct_Gram_limit_error':float(norm(gram100-np.kron(np.eye(D),R),2)),
               'incorrect_transposed_limit_error':float(norm(gram100-np.kron(np.eye(D),R.T),2))}
    V2=G2@power(G2.conj().T@G2,-.5);h=np.eye(d*d)-V2@V2.conj().T
    for L in [2,3]:
        Y=channel_on_good_basis(A,R,L);Y0=channel_on_good_basis(A,R,L,True)
        B=seams(Y,h,d,2*L+2);B0=seams(Y0,h,d,2*L+2)
        matrix=Y.reshape(-1,D**4);defect=float(norm(matrix.conj().T@matrix-np.eye(D**4),2))
        residual=float(norm(B0.reshape(-1,D**4),2));error=float(norm((Y-Y0).reshape(-1,D**4),2))
        cost=float(norm(B.reshape(-1,D**4),2)**2)
        assert defect<1e-11 and residual<1e-11 and cost<=4*error**2+1e-12
        rows.append(dict(**gramcheck,buffer=L,actual_isometry_defect=defect,
                         ideal_all_good_subspace_seam_residual=residual,
                         actual_ideal_map_distance=error,compressed_boundary_square_norm=cost))
out={'status':'PASS after correcting Gram metric to I tensor sigma',
     'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
     'scope':'Full joint good-block basis and reference tested; numerical checks support but do not replace the algebraic proof.',
     'cases':rows,'seconds':time.perf_counter()-started}
(P/'stitching_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
