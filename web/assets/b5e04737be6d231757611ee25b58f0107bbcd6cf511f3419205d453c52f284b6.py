"""Independent dense spectral checks; finite diagnostics, not proof."""
from math import comb, sqrt
import numpy as np

E=np.array([[.5,sqrt(2)/4],[sqrt(2)/4,.75]])
s=1/sqrt(2)

def sym_E(m):
    out=np.zeros((m+1,m+1))
    for i in range(m+1):
        for j in range(m+1):
            out[i,j]=sqrt(comb(m,i)/comb(m,j))*sum(
                comb(i,t)*comb(m-i,j-t)*E[1,1]**t
                *E[0,1]**(i+j-2*t)*E[0,0]**(m-i-j+t)
                for t in range(max(0,i+j-m),min(i,j)+1))
    return out

def sym_T(k,b):
    return np.array([[0. if i<j else
        s**(i-j)*comb(i,j)*sqrt(comb(k,i)/comb(k,j))
        for j in range(b+1)] for i in range(b+1)])

checked=0
max_error=0.
min_gap=float('inf')
for k in range(1,9):
    full=E
    for _ in range(k-1): full=np.kron(full,E)
    for b in range(k+1):
        words=[x for x in range(2**k) if x.bit_count()<=b]
        dense=full[np.ix_(words,words)]
        spectrum=np.linalg.eigvalsh(dense)
        blocks=[]
        for r in range(min(b,k//2)+1):
            m=k-2*r
            q=min(m,b-r)
            vals=np.linalg.eigvalsh(.25**r*sym_E(m)[:q+1,:q+1])
            mult=comb(k,r)-(comb(k,r-1) if r else 0)
            blocks.extend(list(vals)*mult)
            if r: min_gap=min(min_gap, vals[0]-spectrum[0])
        predicted=np.sort(np.array(blocks))
        err=np.max(np.abs(predicted-spectrum))
        max_error=max(max_error,err)
        assert len(blocks)==len(words)
        assert err<1e-11
        T=sym_T(k,b)
        factor=2.**(-k)*T@T.T
        assert np.max(np.abs(factor-sym_E(k)[:b+1,:b+1]))<1e-12
        norm_p=2.**(-k)/np.linalg.norm(T,2)**2
        assert abs(norm_p-spectrum[0])<1e-12
        assert np.max(np.abs(spectrum*spectrum[::-1]-4.**(-k)))<1e-12
        row=T[b,:]
        row_norm=row@row
        psi=row*np.array([(-1.)**j for j in range(b+1)])/sqrt(row_norm)
        witness_p=psi@factor@psi
        assert abs(witness_p-2.**(-k)/row_norm)<1e-12
        checked+=1
print({'checked_k_b_pairs':checked,'maximum_spectral_absolute_error':max_error,
       'smallest_nonzero_r_gap':min_gap})
