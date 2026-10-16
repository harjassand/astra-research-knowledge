"""No-truncation QR norm of a TT sum, materializing only one core at a time."""
import numpy as np
from scipy.linalg.lapack import dgeqrf
from scipy.linalg import norm

def norm_sum(terms,mu=None,core_gate_bytes=650*1024**2):
    terms=[(x,c) for x,c in terms if c!=0]
    if not terms:return 0.,{'peak_core_bytes':0,'ranks':[]}
    d=len(terms[0][0]);R=None;logscale=0.;maxbytes=0;ranks=[]
    for i in range(d):
        n=terms[0][0][i].shape[1]
        if i==0:
            current=np.concatenate([x[i]*c for x,c in terms],axis=2)
        else:
            right=1 if i==d-1 else sum(x[i].shape[2] for x,c in terms)
            forecast=R.shape[0]*n*right*8
            if forecast>core_gate_bytes:raise MemoryError(f'Streaming residual core forecast {forecast} exceeds {core_gate_bytes}')
            current=np.zeros((R.shape[0],n,right));leftpos=rightpos=0
            for x,c in terms:
                a=x[i];l,r=a.shape[0],a.shape[2]
                block=np.einsum('ab,bnc->anc',R[:,leftpos:leftpos+l],a,optimize=True)
                if i==d-1:current+=block
                else:current[:,:,rightpos:rightpos+r]=block
                leftpos+=l;rightpos+=r
            del block,R
        maxbytes=max(maxbytes,current.nbytes)
        if mu is not None:current/=np.sqrt(mu[i])[None,:,None]
        if i==d-1:return float(np.exp(logscale)*norm(current)),dict(peak_core_bytes=maxbytes,ranks=ranks)
        l,n,r=current.shape
        arr=np.asfortranarray(current.reshape(l*n,r));del current
        qr,tau,work,info=dgeqrf(arr,overwrite_a=1)
        if info:raise ArithmeticError(f'dgeqrf info {info}')
        R=np.triu(qr[:min(l*n,r),:]).copy();del arr,qr,tau,work
        scale=norm(R)
        if not scale:return 0.,dict(peak_core_bytes=maxbytes,ranks=ranks)
        R/=scale;logscale+=np.log(scale);ranks.append(R.shape[0])
    raise AssertionError('unreachable')
