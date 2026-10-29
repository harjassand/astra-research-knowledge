#!/usr/bin/env python3
"""Numerical diagnostics, not interval proof or experiment."""
import json, math, pathlib, hashlib
import numpy as np
from scipy.linalg import expm, eigh
ROOT=pathlib.Path(__file__).resolve().parent
rng=np.random.default_rng(202610290412)
I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex); Z=np.diag([1.,-1.]).astype(complex)
H=np.array([[1,1],[1,-1]],complex)/np.sqrt(2); S=np.diag([1,1j])
CX=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],complex)
SW=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],complex)
def embed(A,qs,n):
    D=2**n; out=np.zeros((D,D),complex)
    for x in range(D):
        old=sum(((x>>(n-1-q))&1)<<(len(qs)-1-k) for k,q in enumerate(qs))
        for new in range(2**len(qs)):
            y=x
            for k,q in enumerate(qs):
                mask=1<<(n-1-q); bit=(new>>(len(qs)-1-k))&1
                y=(y|mask) if bit else (y&~mask)
            out[y,x]=A[new,old]
    return out
def matchings(v):
    if not v:yield ();return
    for j in range(1,len(v)):
        for t in matchings(v[1:j]+v[j+1:]):yield ((v[0],v[j]),)+t
def prep(M,n):
    W=np.eye(2**n,dtype=complex)
    for a,b in M:
        for A,qs in ((X,(b,)),(H,(a,)),(CX,(a,b)),(Z,(a,))):W=embed(A,qs,n)@W
    return W
def inv_exchange(theta):
    rz=expm(-.5j*theta*Z)
    ZZ=CX@np.kron(I,rz)@CX
    XX=np.kron(H,H)@ZZ@np.kron(H,H)
    B=H@S.conj().T
    YY=np.kron(B.conj().T,B.conj().T)@ZZ@np.kron(B,B)
    return ZZ@YY@XX
out={'seed':202610290412,'circuit_checks':[],'channel_checks':[]}
for theta in (0,.13,np.pi/4,np.pi/2,-.77):
    U=expm(1j*theta*SW)
    residual=float(np.linalg.norm(inv_exchange(theta)-np.exp(.5j*theta)*U.conj().T))
    assert residual<1e-12
    for n in (4,6):
        Ms=list(matchings(tuple(range(n))))
        V=np.column_stack([prep(M,n)[:,0] for M in Ms])
        d=math.comb(n,n//2)//(n//2+1)
        w,Q=eigh(V@V.conj().T); Q=Q[:,-d:]
        Ubig=embed(U,(0,1),n); Ub=Q.conj().T@Ubig@Q
        max_projector_error=0.
        for M in Ms:
            W=prep(M,n); v=W[:,0]; target=Ubig@v
            same=(0,1) in M
            readout=W.conj().T if same else W.conj().T@embed(inv_exchange(theta),(0,1),n)
            actual=np.outer(readout[0].conj(),readout[0])
            max_projector_error=max(max_projector_error,float(np.linalg.norm(actual-np.outer(target,target.conj()))))
            assert max_projector_error<2e-12
        out['circuit_checks'].append({'n':n,'theta':theta,'exchange_decomposition_error':residual,'max_target_projector_error':max_projector_error})
        coords=Q.conj().T@V
        for trial in range(8):
            # Arbitrary CPTP maps from singlet input to full physical output.
            A=rng.normal(size=(3*2**n,d))+1j*rng.normal(size=(3*2**n,d))
            W,_=np.linalg.qr(A); Ks=list(W.reshape(3,2**n,d))
            pp=sum(np.mean(abs(np.einsum('ij,ij->j', (Ubig@V).conj(),K@coords))**2) for K in Ks)
            fe=sum(abs(np.trace(Q.conj().T@Ubig.conj().T@K)/d)**2 for K in Ks)
            C=(n+2)/(n-1)
            assert 1-fe<=C*(1-pp)+2e-12
            out['channel_checks'].append({'n':n,'theta':theta,'trial':trial,'raw_target_infidelity':float(1-fe),'bound':float(C*(1-pp))})
out['all_checks_passed']=True
out['script_sha256']=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
(ROOT/'check_exchange.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'all_checks_passed':True,'circuit_checks':len(out['circuit_checks']),'channel_checks':len(out['channel_checks'])}))
