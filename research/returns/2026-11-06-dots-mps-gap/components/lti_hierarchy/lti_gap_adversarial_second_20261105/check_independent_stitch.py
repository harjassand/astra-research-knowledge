"""Independent whole-code stitch implementation; no imports from candidate code."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import itertools,json
from pathlib import Path
import numpy as np

def power(H,p):
    w,v=np.linalg.eigh((H+H.conj().T)/2)
    assert w.min()>1e-13
    return (v*w**p)@v.conj().T

def block(A,L):
    D=A.shape[1]
    words=[]
    for seq in itertools.product(range(len(A)),repeat=L):
        z=np.eye(D,dtype=complex)
        for s in seq:z=z@A[s]
        words.append(z.reshape(-1))
    return np.stack(words)

def apply_local(K,h,sites,d,n):
    shape=K.shape
    x=K.reshape([d]*n+list(shape[1:]))
    order=list(sites)+[i for i in range(n) if i not in sites]+list(range(n,x.ndim))
    y=x.transpose(order)
    y=(h@y.reshape(d*d,-1)).reshape(y.shape)
    return y.transpose(np.argsort(order)).reshape(shape)

def check(seed,L):
    rng=np.random.default_rng(seed);d=3;D=2
    A=rng.normal(size=(d,D,D))+1j*rng.normal(size=(d,D,D))
    A=np.einsum('ab,sbc->sac',power(sum(a@a.conj().T for a in A),-.5),A)
    sigma=np.eye(D)/D
    for _ in range(10000):
        nxt=sum(a.conj().T@sigma@a for a in A)
        if np.linalg.norm(nxt-sigma)<1e-14:break
        sigma=nxt
    S=np.kron(np.eye(D),power(sigma,.5))
    G=block(A,L);G2=block(A,2*L);Ge=block(A,L+1)
    V=G@power(G.conj().T@G,-.5)
    J=G2@power(G2.conj().T@G2,-.5)
    Ve=Ge@power(Ge.conj().T@Ge,-.5)
    decoder_ideal=S@np.linalg.pinv(G)
    encoder_ideal=G2@np.linalg.inv(S)
    Vtwo=block(A,2);Vtwo=Vtwo@power(Vtwo.conj().T@Vtwo,-.5)
    h=np.eye(d*d)-Vtwo@Vtwo.conj().T
    B=d**L;n=2*L+2
    # Whole input code: left interval followed by right interval, without compression assumptions.
    T=np.kron(Ve,Ve).reshape(B,d,d,B,D**4)
    def stitch(dec,enc):
        out=np.einsum('aep,fbq,QPfe,pstqk->PstQabk',dec.reshape(D,D,B),dec.reshape(D,D,B),enc.reshape(B,B,D,D),T,optimize=True)
        return out.reshape(d**n,D*D,D**4)
    K=stitch(V.conj().T,J);K0=stitch(decoder_ideal,encoder_ideal)
    def seams(z):return apply_local(z,h,(L-1,L),d,n)+apply_local(z,h,(L+1,L+2),d,n)
    idealres=np.linalg.norm(seams(K0))
    HK=seams(K).reshape(-1,D**4)
    Kmat=K.reshape(-1,D**4)
    isometry=np.linalg.norm(Kmat.conj().T@Kmat-np.eye(D**4))
    compressed=np.linalg.eigvalsh(HK.conj().T@HK).max()
    actualideal=np.linalg.norm((K-K0).reshape(-1,D**4),2)
    gramerr=np.linalg.norm(G.conj().T@G-S@S,2)
    assert idealres<1e-10
    assert isometry<1e-10
    assert compressed<=4*actualideal**2+1e-11
    return {'seed':seed,'ell':L,'sigma_eigenvalues':np.linalg.eigvalsh(sigma).tolist(),'ideal_seam_Frobenius':float(idealres),'isometry_Frobenius':float(isometry),'actual_compressed_boundary_square':float(compressed),'K_minus_K0_operator':float(actualideal),'gram_error_operator':float(gramerr)}

if __name__=='__main__':
    out=[check(seed,L) for seed in [159,2027,7123] for L in [2,3]]
    Path(__file__).with_name('independent_stitch_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
